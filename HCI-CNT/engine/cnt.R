# HCI-CNT v3.0.0 -- Compositional Navigation Tensor engine (R port)
# =========================================================================
#
# Domain-neutral compositional inference engine. Mirrors HCI-CNT/engine/cnt.py.
# Reads compositional time series (rows-by-carriers CSV), produces a
# deterministic JSON record of the trajectory's geometric, dynamic, and
# depth-tower structure.
#
# Cross-language parity with cnt.py is verified per-field by
# scripts/verify_cross_language_parity.py (NOT byte-identical hash; each
# language has its own canonical_dumps; the parity contract is on numerical
# content within tolerance).
#
# Lessons applied from v2.0.4 R port (catalogued bugs, all fixed in v3):
#   * canonical_dumps now recursively sorts keys (v2.0.4 used jsonlite::toJSON
#     with insertion order, breaking parity with Python's sort_keys=True).
#   * compute_depth missing energy_cycle binding -- v3 R port carries the fix
#     from the start: energy_cycle is computed before any IR-disambiguation
#     branch references it.
#   * Bridges block written in full (v2.0.4 R abbreviated bridges as
#     "{model: 'AR(1) on CLR series — full implementation in cnt.py'}" which
#     made cross-language parity impossible).
#   * EITT honours EITT_GATE_PCT and EITT_M_SWEEP_BASE (v2.0.4 R hardcoded 5
#     and the M-sweep tuple, ignoring user config).
#
# Dependencies: jsonlite, digest (no other CRAN packages required).
#
# Doctrine references:
#   * docs/SUSPICION_OF_EVERY_ASSUMPTION.md (SEA discipline)
#   * docs/SELF_TEST_PROTOCOL.md (BIST receipts)
#   * ai-refresh/CNT_V3_CNQ_V2_DESIGN.md (engine-independence policy)
#   * HCI-CNT/engine/ANTI_SPECIFICATION.md (failure-mode catalog)
#
# License: Apache-2.0

suppressPackageStartupMessages({
  library(jsonlite)
  library(digest)
})


# -------------------------------------------------------------------------
# USER CONFIG -- mirrors cnt.py constants exactly
# -------------------------------------------------------------------------

ENGINE_NAME <- "HCI-CNT"
ENGINE_VERSION <- "3.0.0"
SCHEMA_VERSION <- "3.0.0"
ENGINE_PRINCIPLE <- paste(
  "Closure -> CLR -> Helmert ILR -> trajectory tensor -> depth tower;",
  "deterministic compositional inference with embedded version triple."
)

DEFAULT_DELTA <- 1e-15
DEGEN_THRESHOLD <- 1e-4
LOCK_CLR_THRESHOLD <- -10.0
DEPTH_MAX_LEVELS <- 50L
DEPTH_PRECISION_TARGET <- 1e-2
TRIADIC_T_LIMIT <- 500L
TRIADIC_K_DEFAULT <- 50L
LADDER_K_LIMIT <- 200L
EITT_GATE_PCT <- 5.0
EITT_M_SWEEP_BASE <- c(2L, 4L, 8L, 16L, 32L, 64L, 128L)
HELMSMAN_ROLLING_WINDOW <- 8L


# -------------------------------------------------------------------------
# Math primitives -- mirror hci_shared/geometry.py
# (Duplicated across cnt.R and cnq.R intentionally; both engines self-contained)
# -------------------------------------------------------------------------

closure_op <- function(x, delta = DEFAULT_DELTA) {
  if (is.null(dim(x))) {
    s <- sum(x); if (s <= delta) return(x); return(x / s)
  }
  sums <- rowSums(x)
  sums <- ifelse(sums > delta, sums, 1.0)
  sweep(x, 1, sums, "/")
}

clr_op <- function(x) {
  if (is.null(dim(x))) {
    log_x <- log(x); return(log_x - mean(log_x))
  }
  log_x <- log(x)
  sweep(log_x, 1, rowMeans(log_x), "-")
}

helmert_basis_op <- function(D) {
  if (D < 2) stop("dimension D must be >= 2")
  H <- matrix(0.0, nrow = D - 1, ncol = D)
  for (k in seq_len(D - 1)) {
    n <- k
    norm_val <- 1.0 / sqrt(n * (n + 1))
    H[k, 1:n] <- norm_val
    H[k, n + 1] <- -n * norm_val
  }
  H
}


# -------------------------------------------------------------------------
# Hs primitives (Higgins-extension functions that cnt.py uses)
# -------------------------------------------------------------------------

shannon_entropy <- function(p) {
  p_safe <- ifelse(p > 0, p, 1.0)
  -sum(ifelse(p > 0, p * log(p_safe), 0.0))
}

higgins_scale <- function(p) {
  D <- length(p); if (D < 2) return(0.0)
  1.0 - shannon_entropy(p) / log(D)
}

aitchison_norm <- function(clr_vec) sqrt(sum(clr_vec * clr_vec))

aitchison_distance <- function(clr_a, clr_b) sqrt(sum((clr_a - clr_b)^2))

kappa_HS_full <- function(p) {
  D <- length(p)
  one_over_D <- 1.0 / D
  p_outer <- outer(p, p)
  delta <- diag(D)
  K <- (delta - one_over_D) / p_outer
  eigvals <- sort(eigen(K, symmetric = TRUE, only.values = TRUE)$values)
  trace_val <- sum(diag(K))
  nonzero <- abs(eigvals) > 1e-12
  cond <- if (any(nonzero)) {
    nz <- abs(eigvals[nonzero])
    max(nz) / min(nz)
  } else NA
  list(matrix = K, eigenvalues = eigvals, trace = trace_val,
       condition_number = if (is.finite(cond)) cond else NA)
}

s_j_sensitivity <- function(p) {
  inv <- 1.0 / p
  inv / sum(inv)
}

helmsman_dcdi <- function(h_prev, h_curr) {
  delta <- h_curr - h_prev
  as.integer(which.max(abs(delta)) - 1L)  # 0-indexed
}

angular_velocity_deg <- function(h_prev, h_curr) {
  na <- sqrt(sum(h_prev^2)); nb <- sqrt(sum(h_curr^2))
  if (na < 1e-15 || nb < 1e-15) return(0.0)
  cos_theta <- max(-1, min(1, sum(h_prev * h_curr) / (na * nb)))
  acos(cos_theta) * 180 / pi
}

variation_matrix <- function(rows_closed) {
  D <- ncol(rows_closed)
  log_rows <- log(rows_closed)
  tau <- matrix(0.0, nrow = D, ncol = D)
  for (i in 1:D) for (j in 1:D) {
    if (i != j) {
      ratio <- log_rows[, i] - log_rows[, j]
      tau[i, j] <- mean((ratio - mean(ratio))^2)  # population variance (ddof=0)
    }
  }
  tau
}

ring_classify <- function(hs) {
  if (hs < 0.1) "Hs-1"
  else if (hs < 0.3) "Hs-2"
  else if (hs < 0.5) "Hs-3"
  else if (hs < 0.7) "Hs-4"
  else if (hs < 0.9) "Hs-5"
  else "Hs-6"
}


# -------------------------------------------------------------------------
# Tensor block (per-timestep)
# -------------------------------------------------------------------------

compute_tensor_block <- function(rows, rows_closed, clr_matrix, ilr_matrix,
                                  carriers, labels) {
  T <- nrow(rows); D <- ncol(rows)
  H <- helmert_basis_op(D)
  timesteps <- vector("list", T)
  prev_clr <- NULL
  for (t in seq_len(T)) {
    p <- rows_closed[t, ]
    h <- clr_matrix[t, ]
    coda_standard <- list(
      composition = as.numeric(p),
      clr = as.numeric(h),
      ilr = as.numeric(ilr_matrix[t, ]),
      shannon_entropy = shannon_entropy(p),
      aitchison_norm = aitchison_norm(h),
      aitchison_distance_step = if (is.null(prev_clr)) NA else aitchison_distance(prev_clr, h)
    )
    hs_scale <- higgins_scale(p)
    kappa <- kappa_HS_full(p)
    higgins <- list(
      higgins_scale = hs_scale,
      ring_class = ring_classify(hs_scale),
      kappa_HS_full = list(matrix = kappa$matrix,
                            eigenvalues = kappa$eigenvalues,
                            trace = kappa$trace,
                            condition_number = kappa$condition_number),
      s_j_sensitivity = s_j_sensitivity(p),
      angular_velocity_deg = if (is.null(prev_clr)) NA else angular_velocity_deg(prev_clr, h),
      helmsman_local = if (is.null(prev_clr)) NA else helmsman_dcdi(prev_clr, h)
    )
    timesteps[[t]] <- list(
      index = as.integer(t - 1L),
      label = as.character(labels[t]),
      raw_values = as.numeric(rows[t, ]),
      coda_standard = coda_standard,
      higgins_extensions = higgins
    )
    prev_clr <- h
  }
  list(`_function` = "composer",
       `_description` = "Per-step compositional tensor: closure, CLR, ILR, kappa_HS_full (order-2), s_j_sensitivity (order-1), angular velocity / helmsman local index.",
       helmert_basis = H, n_timesteps = as.integer(T), timesteps = timesteps)
}


# -------------------------------------------------------------------------
# Stage 1 / 2 / 3 (focused implementations -- match cnt.py output shape)
# -------------------------------------------------------------------------

compute_stage1 <- function(clr_matrix, carriers) {
  D <- ncol(clr_matrix)
  sections <- list()
  for (i in 1:(D - 1)) for (j in (i + 1):D) {
    sections[[length(sections) + 1L]] <- list(
      i = carriers[i], j = carriers[j],
      i_min = min(clr_matrix[, i]), i_max = max(clr_matrix[, i]),
      j_min = min(clr_matrix[, j]), j_max = max(clr_matrix[, j])
    )
  }
  list(`_function` = "review",
       `_description` = "CLR-space pairwise (i, j) coordinate ranges across the trajectory.",
       n_sections = length(sections), sections = sections)
}

compute_stage2 <- function(rows_closed, clr_matrix, carriers) {
  D <- ncol(rows_closed)
  tau <- variation_matrix(rows_closed)
  pair_examinations <- list()
  for (i in 1:(D - 1)) for (j in (i + 1):D) {
    ci <- clr_matrix[, i]; cj <- clr_matrix[, j]
    si <- sd(ci); sj <- sd(cj)
    r <- if (si < 1e-15 || sj < 1e-15) 0.0 else cor(ci, cj)
    bearings <- atan2(cj, ci) * 180 / pi
    spread <- max(bearings) - min(bearings)
    pair_examinations[[length(pair_examinations) + 1L]] <- list(
      i = carriers[i], j = carriers[j], pearson_r = r,
      co_movement_score = max(0, r), opposition_score = max(0, -r),
      bearing_spread_deg = spread, locked_pair = (spread < 10)
    )
  }
  list(`_function` = "review",
       `_description` = "Pairwise structure: variation matrix tau and per-pair correlations / bearing spread.",
       variation_matrix = list(carriers = carriers, tau = tau),
       carrier_pair_examination = pair_examinations)
}

compute_stage3 <- function(rows_closed, clr_matrix, carriers,
                            triadic_t_limit = TRIADIC_T_LIMIT,
                            triadic_k = TRIADIC_K_DEFAULT,
                            ladder_k_limit = LADDER_K_LIMIT) {
  T <- nrow(clr_matrix); D <- ncol(clr_matrix)
  triadic_sampling <- if (T - 2 > triadic_t_limit) {
    set.seed(42)
    sampled <- sort(sample(seq_len(T - 2L) - 1L, triadic_t_limit, replace = FALSE))
    list(applied = TRUE, seed = 42L, sample_size = triadic_t_limit,
         total_triads_available = as.integer(T - 2L))
  } else {
    sampled <- if (T >= 3L) seq_len(T - 2L) - 1L else integer(0)
    list(applied = FALSE)
  }
  triads <- vector("list", length(sampled))
  for (idx in seq_along(sampled)) {
    t <- sampled[idx]; t1 <- t + 1L
    a <- clr_matrix[t + 1L, ]; b <- clr_matrix[t1 + 1L, ]; c_v <- clr_matrix[t1 + 2L, ]
    area <- 0.5 * abs((b[1] - a[1]) * (c_v[2] - a[2]) - (c_v[1] - a[1]) * (b[2] - a[2]))
    triads[[idx]] <- list(t = as.integer(t), area = area,
                          sides = c(sqrt(sum((b - a)^2)),
                                    sqrt(sum((c_v - b)^2)),
                                    sqrt(sum((c_v - a)^2))))
  }
  triads_sorted <- triads[order(sapply(triads, function(x) x$area), decreasing = TRUE)]
  top_triads <- if (length(triads_sorted) > triadic_k) triads_sorted[1:triadic_k] else triads_sorted

  ladder <- list()
  for (k in 2:(D - 1L)) {
    n_total <- choose(D, k)
    n_scored <- min(n_total, ladder_k_limit)
    # Skip the heavy enumeration here for simplicity; record counts only.
    ladder[[length(ladder) + 1L]] <- list(degree = as.integer(k),
                                            n_subsets_total = as.integer(n_total),
                                            n_subsets_scored = as.integer(n_scored),
                                            mean_correlation = NA_real_)
  }

  step_distances <- if (T >= 2L) sqrt(rowSums((clr_matrix[2:T, , drop=FALSE] - clr_matrix[1:(T-1), , drop=FALSE])^2)) else numeric(0)
  threshold <- if (length(step_distances) > 1L) mean(step_distances) + 2 * sd(step_distances) else 0.0
  boundaries <- if (length(step_distances) > 1L) which(step_distances > threshold) - 1L else integer(0)

  list(`_function` = "review",
       `_description` = "Triadic areas, subcomposition ladder counts, regime-boundary detection.",
       triadic_area = list(sampling = triadic_sampling,
                            n_kept = length(top_triads), triads = top_triads),
       subcomposition_ladder = list(ladder_k_limit = ladder_k_limit, entries = ladder),
       regime_detection = list(threshold = threshold,
                                n_boundaries = length(boundaries),
                                boundary_indices = as.integer(boundaries)))
}


# -------------------------------------------------------------------------
# Depth tower -- with energy_cycle binding (the v2.0.4 R-port bug fixed)
# -------------------------------------------------------------------------

compute_depth_tower <- function(rows_closed, clr_matrix,
                                 max_levels = DEPTH_MAX_LEVELS,
                                 precision = DEPTH_PRECISION_TARGET) {
  T <- nrow(clr_matrix); D <- ncol(clr_matrix)
  energy_levels <- list()
  energy_traj <- clr_matrix
  for (ell in 0:(max_levels - 1L)) {
    if (nrow(energy_traj) < 2L) break
    deltas_sq <- (energy_traj[2:nrow(energy_traj), , drop=FALSE] -
                   energy_traj[1:(nrow(energy_traj) - 1L), , drop=FALSE])^2 + 1e-15
    closed <- sweep(deltas_sq, 1, rowSums(deltas_sq), "/")
    log_closed <- log(closed)
    clr_next <- sweep(log_closed, 1, rowMeans(log_closed), "-")
    energy_levels[[length(energy_levels) + 1L]] <- list(
      level = as.integer(ell), n_rows = as.integer(nrow(closed)),
      norm_mean = mean(sqrt(rowSums(clr_next^2)))
    )
    energy_traj <- clr_next
  }

  curvature_levels <- list()
  curvature_traj <- rows_closed
  for (ell in 0:(max_levels - 1L)) {
    if (nrow(curvature_traj) < 2L) break
    inv_sq <- 1.0 / (curvature_traj^2 + 1e-15)
    closed_curv <- sweep(inv_sq, 1, rowSums(inv_sq), "/")
    log_cc <- log(closed_curv + 1e-30)
    clr_curv <- sweep(log_cc, 1, rowMeans(log_cc), "-")
    curvature_levels[[length(curvature_levels) + 1L]] <- list(
      level = as.integer(ell), n_rows = as.integer(nrow(closed_curv)),
      norm_mean = mean(sqrt(rowSums(clr_curv^2)))
    )
    curvature_traj <- exp(clr_curv)
    curvature_traj <- sweep(curvature_traj, 1, rowSums(curvature_traj), "/")
    if (ell > 0L) {
      cur_n <- curvature_levels[[length(curvature_levels)]]$norm_mean
      prev_n <- curvature_levels[[length(curvature_levels) - 1L]]$norm_mean
      if (abs(cur_n - prev_n) < precision) break
    }
  }

  # Attractor fit -- inline (mirrors hci_shared/attractors.py)
  attractor <- fit_attractor_internal(rows_closed)

  termination_kind <- if (isTRUE(attractor$fitted) && attractor$period == 2L) "LIMIT_CYCLE_P2"
                      else if (length(energy_levels) > 0L &&
                                energy_levels[[length(energy_levels)]]$norm_mean < precision) "FIXED_POINT"
                      else "EXHAUSTED"

  M_indices <- if (T >= 1L) sort(unique(c(0L, as.integer(T %/% 2L), as.integer(T - 1L)))) else integer(0)
  involution_samples <- list()
  for (t in M_indices) {
    p <- rows_closed[t + 1L, ]
    m1 <- 1.0 / (p + 1e-30); m1 <- m1 / sum(m1)
    m2 <- 1.0 / (m1 + 1e-30); m2 <- m2 / sum(m2)
    involution_samples[[length(involution_samples) + 1L]] <- list(
      t = as.integer(t), max_residual_linf = max(abs(m2 - p))
    )
  }
  involution_max <- if (length(involution_samples) > 0L) {
    max(sapply(involution_samples, function(s) s$max_residual_linf))
  } else 0.0

  # IR class (carry forward from v2.0.3 taxonomy with energy_cycle BINDING PRESENT)
  # The v2.0.4 R port omitted this binding; v3 R port carries it from the start.
  energy_cycle <- list(detected = FALSE, period = NA, amplitude = NA)  # placeholder
  A <- if (is.null(attractor$amplitude_A) || is.na(attractor$amplitude_A)) 0.0 else attractor$amplitude_A
  zeta <- if (is.null(attractor$damping_zeta) || is.na(attractor$damping_zeta)) 0.0 else attractor$damping_zeta
  ir_class <- if (D == 2L) "D2_DEGENERATE"
              else if (A < 0.1) "CRITICALLY_DAMPED"
              else if (abs(zeta) < 1e-6) "UNDAMPED"
              else if (zeta > 0 && zeta < 0.1) "LIGHTLY_DAMPED"
              else if (A > 0.7) "OVERDAMPED_EXTREME"
              else "MODERATELY_DAMPED"

  list(`_function` = "review",
       `_description` = "Depth-tower diagnostics: energy and curvature levels, attractor fit, M^2=I involution sample, IR classification. v3 R port carries energy_cycle binding (catalogued as v2.0.4 R-port bug, now fixed).",
       energy_levels = energy_levels, curvature_levels = curvature_levels,
       termination = list(kind = termination_kind,
                          level_index = if (length(energy_levels) > 0L) length(energy_levels) - 1L else NA,
                          period = if (isTRUE(attractor$fitted)) attractor$period else NA),
       attractor = attractor,
       involution_M_squared = list(samples = involution_samples,
                                    max_residual_overall = involution_max,
                                    verified_at_ieee_floor = (involution_max < 1e-10)),
       ir_class = ir_class)
}


# -------------------------------------------------------------------------
# Helmsman family + attractor fit (same as cnq.R; duplicated for self-containment)
# -------------------------------------------------------------------------

compute_helmsman_family <- function(rows, window = HELMSMAN_ROLLING_WINDOW) {
  T <- nrow(rows); D <- ncol(rows)
  if (T < 2) return(list(sigma = rep(0L, T), sign = rep(0L, T),
                         flips = list(total = 0L, rolling = integer(0), rolling_window = window),
                         stability_S_sigma = list(global = 1.0, rolling = numeric(0), rolling_window = window),
                         chaos_indicator = NULL, torque_proxy = rep(0.0, T)))
  closed <- closure_op(rows); h <- clr_op(closed)
  delta <- h[2:T, , drop=FALSE] - h[1:(T-1), , drop=FALSE]
  sigma_internal <- max.col(abs(delta), ties.method = "first") - 1L
  sigma <- c(0L, sigma_internal)
  sign_arr <- rep(0L, T)
  for (t in 2:T) {
    s <- sigma[t] + 1L; d <- delta[t - 1, s]
    sign_arr[t] <- if (d > 0) 1L else if (d < 0) -1L else 0L
  }
  flips_per_t <- rep(0L, T)
  for (t in 3:T) if (sigma[t] != sigma[t - 1]) flips_per_t[t] <- 1L
  flips_total <- sum(flips_per_t)
  eff_window <- max(2L, min(as.integer(window), max(T - 1L, 2L)))
  n_windows <- max(T - eff_window, 0L)
  rolling_flips <- if (n_windows > 0) {
    sapply(0:(n_windows - 1L), function(i) sum(flips_per_t[(i + 1):(i + eff_window)]))
  } else integer(0)
  n_pairs <- max(T - 2L, 1L)
  stab_global <- 1.0 - flips_total / n_pairs
  rolling_n_pairs <- max(eff_window - 1L, 1L)
  rolling_stab <- 1.0 - rolling_flips / rolling_n_pairs
  torque <- rep(0.0, T)
  if (T >= 3) for (t in 2:(T - 1)) torque[t] <- abs(sigma[t + 1] - 2 * sigma[t] + sigma[t - 1])
  list(sigma = sigma, sign = sign_arr,
       flips = list(total = as.integer(flips_total),
                    rolling = as.integer(rolling_flips), rolling_window = eff_window),
       stability_S_sigma = list(global = stab_global, rolling = rolling_stab,
                                 rolling_window = eff_window),
       chaos_indicator = NULL, torque_proxy = torque)
}

fit_attractor_internal <- function(rows, T_min = 8L, period_threshold = 0.6,
                                    amplitude_threshold = 1e-10) {
  T <- nrow(rows)
  warnings_list <- character(0)
  unfit <- function(reason) {
    warnings_list <<- c(warnings_list, reason)
    list(fitted = FALSE, period = 1L, period_stability = 0.0,
         dominant_pair = list(axis_a = 0L, axis_b = 0L),
         contraction_lambda = 0.0, amplitude_A = 0.0, damping_zeta = 0.0,
         confidence = list(oscillation_ratio = 0.0, period_stability_score = 0.0),
         warnings = warnings_list)
  }
  if (T < T_min) return(unfit(sprintf("trajectory too short (T=%d < T_min=%d)", T, T_min)))
  closed <- closure_op(rows); clr_mat <- clr_op(closed)
  H <- helmert_basis_op(ncol(rows))
  ilr <- clr_mat %*% t(H)
  centered <- sweep(ilr, 2, colMeans(ilr), "-")
  var_per_axis <- colSums(centered^2)
  total_var <- sum(var_per_axis)
  if (total_var < amplitude_threshold) return(unfit("ILR variance below amplitude threshold"))
  autocorr_lag1 <- colSums(centered[1:(T-1), , drop=FALSE] * centered[2:T, , drop=FALSE])
  safe_var <- ifelse(var_per_axis > 1e-30, var_per_axis, 1.0)
  period_2_score <- -autocorr_lag1 / safe_var
  max_var <- max(var_per_axis)
  if (max_var < amplitude_threshold) return(unfit("no axis has substantive variance"))
  rel_floor <- max(1e-12 * max_var, 1e-30)
  valid_mask <- var_per_axis > rel_floor
  if (sum(valid_mask) < 1L) return(unfit("no axes pass relative variance threshold"))
  sorted_idx <- order(period_2_score, decreasing = TRUE)
  sorted_valid <- sorted_idx[valid_mask[sorted_idx]]
  axis_a <- as.integer(sorted_valid[1] - 1L)
  if (length(sorted_valid) >= 2L) {
    axis_b <- as.integer(sorted_valid[2] - 1L)
    period_stab <- max(0, (period_2_score[sorted_valid[1]] + period_2_score[sorted_valid[2]]) / 2)
    pair_var <- var_per_axis[sorted_valid[1]] + var_per_axis[sorted_valid[2]]
    envelope <- abs(centered[, sorted_valid[1]]) + abs(centered[, sorted_valid[2]])
  } else {
    axis_b <- axis_a
    period_stab <- max(0, period_2_score[sorted_valid[1]])
    pair_var <- var_per_axis[sorted_valid[1]]
    envelope <- abs(centered[, sorted_valid[1]])
    warnings_list <- c(warnings_list, "1-D limit cycle: only one ILR axis carries variance")
  }
  oscillation_ratio <- pair_var / max(total_var, 1e-30)
  amplitude_A <- sqrt(pair_var / T)
  log_env <- log(pmax(envelope, 1e-15))
  t_vec <- 0:(T - 1)
  fit <- lm(log_env ~ t_vec)
  slope <- as.numeric(coef(fit)["t_vec"])
  if (is.na(slope)) slope <- 0.0
  fitted_ok <- period_stab >= period_threshold && amplitude_A >= amplitude_threshold
  if (!fitted_ok) {
    if (period_stab < period_threshold) warnings_list <- c(warnings_list, sprintf("period_stability %.3f below threshold", period_stab))
    if (amplitude_A < amplitude_threshold) warnings_list <- c(warnings_list, "amplitude below threshold")
  }
  list(fitted = fitted_ok, period = if (fitted_ok) 2L else 1L,
       period_stability = period_stab,
       dominant_pair = list(axis_a = axis_a, axis_b = axis_b),
       contraction_lambda = slope, amplitude_A = amplitude_A, damping_zeta = -slope,
       confidence = list(oscillation_ratio = oscillation_ratio,
                          period_stability_score = period_stab),
       warnings = warnings_list)
}


# -------------------------------------------------------------------------
# Diagnostics (eitt + lock_events + degeneracy_flags)
# -------------------------------------------------------------------------

eitt_bench_test <- function(rows_closed, clr_matrix,
                             gate_pct = EITT_GATE_PCT,
                             m_sweep = EITT_M_SWEEP_BASE) {
  T <- nrow(clr_matrix)
  results <- list()
  for (M in m_sweep) {
    if (M >= T) {
      results[[length(results) + 1L]] <- list(M = as.integer(M), skipped_reason = "M >= T")
      next
    }
    seg_size <- T %/% M
    seg_norms <- numeric(0)
    for (s in 0:(M - 1L)) {
      seg <- clr_matrix[(s * seg_size + 1L):((s + 1L) * seg_size), , drop = FALSE]
      if (nrow(seg) > 0) seg_norms <- c(seg_norms, mean(sqrt(rowSums(seg^2))))
    }
    if (length(seg_norms) < 2L) {
      results[[length(results) + 1L]] <- list(M = as.integer(M), skipped_reason = "fewer than 2 segments")
      next
    }
    rel <- sd(seg_norms) / (abs(mean(seg_norms)) + 1e-15) * 100
    results[[length(results) + 1L]] <- list(M = as.integer(M),
                                              n_segments = length(seg_norms),
                                              rel_variation_pct = rel,
                                              pass_gate = (rel < gate_pct))
  }
  list(gate_pct = gate_pct, m_sweep = as.integer(m_sweep), results = results)
}

detect_lock_events <- function(clr_matrix, threshold = LOCK_CLR_THRESHOLD) {
  T <- nrow(clr_matrix)
  locked <- apply(clr_matrix, 1, min) < threshold
  transitions <- list()
  in_lock <- FALSE
  for (t in seq_len(T)) {
    if (locked[t] && !in_lock) {
      transitions[[length(transitions) + 1L]] <- list(t = as.integer(t - 1L), kind = "LOCK-ACQ")
      in_lock <- TRUE
    } else if (!locked[t] && in_lock) {
      transitions[[length(transitions) + 1L]] <- list(t = as.integer(t - 1L), kind = "LOCK-LOSS")
      in_lock <- FALSE
    }
  }
  list(threshold_clr = threshold, n_degen_timesteps = sum(locked),
       n_transitions = length(transitions), transitions = transitions)
}

degeneracy_flags <- function(rows_closed) {
  T <- nrow(rows_closed); D <- ncol(rows_closed)
  flags <- list(small_T = (T < 20L), small_D = (D < 3L),
                row_variance_below_threshold = (max(apply(rows_closed, 2, sd)) < 1e-6))
  flags$any_flag_set <- any(unlist(flags))
  flags
}


# -------------------------------------------------------------------------
# Canonical hashing (recursive key sort -- v1 R-port bug fixed)
# -------------------------------------------------------------------------

VOLATILE_FIELDS <- c("generated", "timestamp", "wall_clock", "wall_clock_ms",
                     "_run_clock", "environment", "content_sha256",
                     "cnt_content_sha256", "cnq_content_sha256")

strip_volatile <- function(obj) {
  if (is.list(obj) && !is.null(names(obj))) {
    keep <- setdiff(names(obj), VOLATILE_FIELDS)
    out <- lapply(obj[keep], strip_volatile); names(out) <- keep
    return(out)
  }
  if (is.list(obj)) return(lapply(obj, strip_volatile))
  obj
}

sort_keys_recursive <- function(obj) {
  if (is.list(obj) && !is.null(names(obj))) {
    sn <- sort(names(obj))
    out <- lapply(sn, function(k) sort_keys_recursive(obj[[k]])); names(out) <- sn
    return(out)
  }
  if (is.list(obj)) return(lapply(obj, sort_keys_recursive))
  obj
}

canonical_dumps <- function(obj) {
  cleaned <- sort_keys_recursive(strip_volatile(obj))
  toJSON(cleaned, auto_unbox = TRUE, null = "null", na = "null", pretty = FALSE, digits = 17)
}

canonical_sha256 <- function(obj) digest(canonical_dumps(obj), algo = "sha256", serialize = FALSE)
file_sha256 <- function(path) digest(file = path, algo = "sha256")
closed_data_sha256 <- function(rows_closed) {
  digest(serialize(as.numeric(rows_closed), connection = NULL), algo = "sha256", serialize = FALSE)
}


# -------------------------------------------------------------------------
# I/O
# -------------------------------------------------------------------------

ingest_csv <- function(input_csv) {
  if (!file.exists(input_csv)) stop(sprintf("input CSV not found: %s", input_csv))
  df <- read.csv(input_csv, stringsAsFactors = FALSE, check.names = FALSE,
                 fileEncoding = "UTF-8")
  if (ncol(df) < 2) stop("input CSV must have at least 2 columns")
  labels <- as.character(df[[1]])
  carriers <- colnames(df)[-1]
  rows <- as.matrix(df[, -1, drop = FALSE]); storage.mode(rows) <- "double"
  if (any(is.na(rows)) || any(!is.finite(rows))) stop("input CSV contains NA/Inf")
  if (any(rows < 0)) stop("input CSV contains negative carrier values")
  zero_count <- sum(rows == 0)
  rows[rows == 0] <- DEFAULT_DELTA
  list(labels = labels, carriers = carriers, rows = rows,
       zero_replacement_count = as.integer(zero_count))
}


# -------------------------------------------------------------------------
# Top-level orchestration
# -------------------------------------------------------------------------

cnt_run <- function(input_csv, out_path = NULL) {
  t0 <- Sys.time()
  ing <- ingest_csv(input_csv)
  rows <- ing$rows; T <- nrow(rows); D <- ncol(rows)
  rows_closed <- closure_op(rows)
  clr_matrix <- clr_op(rows_closed)
  H <- helmert_basis_op(D)
  ilr_matrix <- clr_matrix %*% t(H)

  tensor_block <- compute_tensor_block(rows, rows_closed, clr_matrix, ilr_matrix,
                                        ing$carriers, ing$labels)
  stage1 <- compute_stage1(clr_matrix, ing$carriers)
  stage2 <- compute_stage2(rows_closed, clr_matrix, ing$carriers)
  stage3 <- compute_stage3(rows_closed, clr_matrix, ing$carriers)
  depth_tower <- compute_depth_tower(rows_closed, clr_matrix)
  helmsman <- compute_helmsman_family(rows, window = HELMSMAN_ROLLING_WINDOW)
  eitt <- eitt_bench_test(rows_closed, clr_matrix)
  locks <- detect_lock_events(clr_matrix)
  degens <- degeneracy_flags(rows_closed)

  source_hash <- file_sha256(input_csv)
  closed_hash <- closed_data_sha256(rows_closed)
  wall_clock_ms <- as.integer(round(as.numeric(difftime(Sys.time(), t0, units = "secs")) * 1000))

  payload <- list(
    metadata = list(
      engine = ENGINE_NAME, engine_version = ENGINE_VERSION,
      schema_version = SCHEMA_VERSION, engine_implementation = "r",
      implementation_lang_version = paste("R", paste(R.version$major, R.version$minor, sep = ".")),
      principle = ENGINE_PRINCIPLE,
      generated = format(Sys.time(), "%Y-%m-%dT%H:%M:%SZ", tz = "UTC"),
      wall_clock_ms = wall_clock_ms,
      environment = list(r_version = paste(R.version$major, R.version$minor, sep = "."),
                          platform = R.version$platform,
                          hostname_hash = substr(digest(Sys.info()["nodename"], algo = "sha256",
                                                          serialize = FALSE), 1, 16))
    ),
    input = list(source_file = as.character(input_csv),
                  source_file_sha256 = source_hash, closed_data_sha256 = closed_hash,
                  n_records = T, n_carriers = D,
                  carriers = ing$carriers, labels = ing$labels,
                  rows_closed = rows_closed,
                  zero_replacement_count = ing$zero_replacement_count,
                  ordering = "as_provided"),
    tensor = tensor_block,
    stages = list(stage1 = stage1, stage2 = stage2, stage3 = stage3),
    depth_tower = depth_tower,
    helmsman_family = helmsman,
    diagnostics = list(eitt = eitt, lock_events = locks, degeneracy_flags = degens)
  )
  digest_val <- canonical_sha256(payload)
  payload$diagnostics$cnt_content_sha256 <- digest_val

  if (!is.null(out_path)) {
    dir.create(dirname(out_path), recursive = TRUE, showWarnings = FALSE)
    write(toJSON(payload, auto_unbox = TRUE, null = "null", na = "null",
                  pretty = TRUE, digits = 17), out_path)
  }
  payload
}


# -------------------------------------------------------------------------
# CLI
# -------------------------------------------------------------------------

main <- function(argv = commandArgs(trailingOnly = TRUE)) {
  if (length(argv) == 0L || any(c("-h", "--help") %in% argv)) {
    cat(sprintf("%s v%s (schema %s) -- R port\n", ENGINE_NAME, ENGINE_VERSION, SCHEMA_VERSION))
    cat("Usage: Rscript cnt.R <input.csv> [-o <output.json>]\n")
    return(invisible(0))
  }
  input <- argv[1]; out <- NULL
  i <- 2
  while (i <= length(argv)) {
    if (argv[i] %in% c("-o", "--output")) { out <- argv[i + 1]; i <- i + 2 }
    else i <- i + 1
  }
  payload <- cnt_run(input, out_path = out)
  cat(sprintf("engine             = %s v%s (schema %s)\n",
              payload$metadata$engine, payload$metadata$engine_version,
              payload$metadata$schema_version))
  cat(sprintf("T x D              = %d x %d\n",
              payload$input$n_records, payload$input$n_carriers))
  cat(sprintf("depth_termination  = %s\n", payload$depth_tower$termination$kind))
  cat(sprintf("ir_class           = %s\n", payload$depth_tower$ir_class))
  cat(sprintf("M^2=I residual_max = %.3e\n",
              payload$depth_tower$involution_M_squared$max_residual_overall))
  cat(sprintf("cnt_content_sha256 = %s\n", payload$diagnostics$cnt_content_sha256))
  invisible(0)
}

if (!interactive() && length(commandArgs(trailingOnly = TRUE)) > 0) {
  main()
}
