# HCI-CNQ v2.0.0 -- Compositional Navigation Quaternion engine (R port)
# =========================================================================
#
# Native dataset producer. Reads compositional time series (rows-by-carriers
# CSV), produces a deterministic JSON record covering the trajectory's
# quaternion-algebraic structure: bearing trajectory, radial trajectory,
# helmsman family channels, attractor fit, twin-quaternion factoring (D=8
# native), and CHSH joint-coherence diagnostic.
#
# CNQ v2 stands on its own. It does not require CNT input. If a CNT JSON is
# provided, its hash is recorded in cnt_reference as informational metadata
# only -- the CNQ canonical hash is independent (push #32 engine-independence).
#
# Cross-language parity (Python <-> R) is verified per-field, not byte-identical
# hash. Each language's canonical_dumps is its own determinism contract; the
# parity script compares numerical content within tolerance.
#
# Lessons applied from v1.0.0 R port (catalogued bugs, all fixed in v2):
#   * canonical_dumps now recursively sorts keys (v1 used jsonlite::toJSON
#     with insertion order, breaking parity with Python's sort_keys=True).
#   * metadata.reference_implementation field removed (v1 added it in R but
#     not Python, guaranteeing different hashes).
#   * No hardcoded "python3" anywhere (v1 hardcoded subprocess invocation;
#     v2 R port doesn't shell out at all -- CSV ingest is direct in R).
#   * compute_depth missing energy_cycle binding (v1 R port NameError on
#     IR-disambiguation branch; v2 R port carries the fix from the start).
#
# Dependencies: jsonlite, digest (no other CRAN packages required).
#
# Doctrine references:
#   * docs/SUSPICION_OF_EVERY_ASSUMPTION.md (SEA discipline)
#   * docs/SELF_TEST_PROTOCOL.md (BIST receipts)
#   * ai-refresh/CNT_V3_CNQ_V2_DESIGN.md (engine-independence policy)
#   * HCI-CNQ/engine/ANTI_SPECIFICATION.md (failure-mode catalog)
#
# License: Apache-2.0

suppressPackageStartupMessages({
  library(jsonlite)
  library(digest)
})


# -------------------------------------------------------------------------
# USER CONFIG -- mirrors cnq.py constants exactly
# -------------------------------------------------------------------------

ENGINE_NAME <- "HCI-CNQ"
ENGINE_VERSION <- "2.0.0"
SCHEMA_VERSION <- "cnq/2.0.0"
ENGINE_PRINCIPLE <- "CNT measures invariance. CNQ names the algebra it lives in."

DEFAULT_DELTA <- 1e-15
GATE_THRESHOLD <- 1e-12
HELMSMAN_ROLLING_WINDOW <- 8L

CLASSICAL_BOUND <- 2.0
TSIRELSON_BOUND <- 2.0 * sqrt(2.0)


# -------------------------------------------------------------------------
# Math primitives -- mirror hci_shared/geometry.py
# -------------------------------------------------------------------------

closure_op <- function(x, delta = DEFAULT_DELTA) {
  if (is.null(dim(x))) {
    s <- sum(x)
    if (s <= delta) return(x)
    return(x / s)
  }
  sums <- rowSums(x)
  sums <- ifelse(sums > delta, sums, 1.0)
  sweep(x, 1, sums, "/")
}

clr_op <- function(x) {
  if (is.null(dim(x))) {
    log_x <- log(x)
    return(log_x - mean(log_x))
  }
  log_x <- log(x)
  row_means <- rowMeans(log_x)
  sweep(log_x, 1, row_means, "-")
}

helmert_basis_op <- function(D) {
  if (D < 2) stop("dimension D must be >= 2")
  H <- matrix(0.0, nrow = D - 1, ncol = D)
  for (k in seq_len(D - 1)) {  # 1..D-1
    n <- k  # n = k in 1-indexed convention; Python's k+1 with 0-index = R's k with 1-index
    norm_val <- 1.0 / sqrt(n * (n + 1))
    H[k, 1:n] <- norm_val
    H[k, n + 1] <- -n * norm_val
  }
  H
}

compositions_to_ilr <- function(rows, D = NULL) {
  if (is.null(D)) D <- ncol(rows)
  closed <- closure_op(rows)
  clr_mat <- clr_op(closed)
  H <- helmert_basis_op(D)
  ilr <- clr_mat %*% t(H)
  radii <- sqrt(rowSums(ilr * ilr))
  list(ilr = ilr, radii = radii)
}

compositions_to_helmert_unit_vectors <- function(rows, D = NULL, eps = 1e-15) {
  res <- compositions_to_ilr(rows, D)
  ilr <- res$ilr
  radii <- res$radii
  units <- ilr
  safe <- radii > eps
  for (i in seq_along(radii)) {
    if (safe[i]) {
      units[i, ] <- ilr[i, ] / radii[i]
    } else {
      units[i, ] <- 0.0
    }
  }
  list(units = units, radii = radii)
}


# -------------------------------------------------------------------------
# Quaternion algebra -- scalar-first Hamilton convention
# -------------------------------------------------------------------------

quat_conj <- function(q) c(q[1], -q[2], -q[3], -q[4])

quat_mul <- function(p, q) {
  c(
    p[1] * q[1] - p[2] * q[2] - p[3] * q[3] - p[4] * q[4],
    p[1] * q[2] + p[2] * q[1] + p[3] * q[4] - p[4] * q[3],
    p[1] * q[3] - p[2] * q[4] + p[3] * q[1] + p[4] * q[2],
    p[1] * q[4] + p[2] * q[3] - p[3] * q[2] + p[4] * q[1]
  )
}

quat_rotate <- function(q, v) {
  v_quat <- c(0.0, v[1], v[2], v[3])
  rotated <- quat_mul(quat_mul(q, v_quat), quat_conj(q))
  rotated[2:4]
}

quat_from_axis_angle <- function(axis, angle) {
  n <- sqrt(sum(axis * axis))
  if (n < 1e-15) return(c(1.0, 0.0, 0.0, 0.0))
  ua <- axis / n
  half <- angle / 2.0
  s <- sin(half)
  c(cos(half), s * ua[1], s * ua[2], s * ua[3])
}

rotation_quaternion_between <- function(u1, u2, eps = 1e-15) {
  d <- sum(u1 * u2)
  cr <- c(
    u1[2] * u2[3] - u1[3] * u2[2],
    u1[3] * u2[1] - u1[1] * u2[3],
    u1[1] * u2[2] - u1[2] * u2[1]
  )
  cn <- sqrt(sum(cr * cr))
  if (cn < eps) {
    if (d > 0) return(c(1.0, 0.0, 0.0, 0.0))
    if (abs(u1[1]) < 0.9) {
      ax <- c(u1[2] * 0 - u1[3] * 0, u1[3] * 1 - u1[1] * 0, u1[1] * 0 - u1[2] * 1)
      ax <- c(0, u1[3], -u1[2])  # cross(u1, ex)
    } else {
      ax <- c(-u1[3], 0, u1[1])  # cross(u1, ey)
    }
    an <- sqrt(sum(ax * ax))
    if (an < eps) ax <- c(u1[2], -u1[1], 0)
    ax <- ax / sqrt(sum(ax * ax))
    return(c(0.0, ax[1], ax[2], ax[3]))
  }
  angle <- atan2(cn, d)
  axis <- cr / cn
  quat_from_axis_angle(axis, angle)
}

quaternion_sandwich_residuals <- function(unit_vectors_3d) {
  n <- nrow(unit_vectors_3d)
  if (n < 2) {
    return(list(
      residuals = numeric(0),
      quats = matrix(0, nrow = 0, ncol = 4),
      angles = numeric(0)
    ))
  }
  residuals <- numeric(n - 1)
  quats <- matrix(0.0, nrow = n - 1, ncol = 4)
  angles <- numeric(n - 1)
  for (t in seq_len(n - 1)) {
    u1 <- unit_vectors_3d[t, ]
    u2 <- unit_vectors_3d[t + 1, ]
    q <- rotation_quaternion_between(u1, u2)
    quats[t, ] <- q
    u_rot <- quat_rotate(q, u1)
    residuals[t] <- max(abs(u_rot - u2))
    angles[t] <- 2.0 * atan2(sqrt(sum(q[2:4] * q[2:4])), q[1])
  }
  list(residuals = residuals, quats = quats, angles = angles)
}


# -------------------------------------------------------------------------
# Helmsman family -- mirror hci_shared.helmsman
# -------------------------------------------------------------------------

compute_helmsman_family <- function(rows, window = HELMSMAN_ROLLING_WINDOW) {
  T <- nrow(rows)
  D <- ncol(rows)
  if (T < 2) {
    return(list(
      sigma = rep(0L, T),
      sign = rep(0L, T),
      flips = list(total = 0L, rolling = integer(0), rolling_window = window),
      stability_S_sigma = list(global = 1.0, rolling = numeric(0), rolling_window = window),
      chaos_indicator = NULL,
      torque_proxy = rep(0.0, T)
    ))
  }
  closed <- closure_op(rows)
  h <- clr_op(closed)
  delta <- h[2:T, , drop = FALSE] - h[1:(T - 1), , drop = FALSE]
  abs_delta <- abs(delta)
  sigma_internal <- max.col(abs_delta, ties.method = "first") - 1L  # 0-indexed
  sigma <- c(0L, sigma_internal)
  sign_arr <- rep(0L, T)
  for (t in 2:T) {
    s <- sigma[t] + 1L  # to 1-indexed for R
    d <- delta[t - 1, s]
    sign_arr[t] <- if (d > 0) 1L else if (d < 0) -1L else 0L
  }
  flips_per_t <- rep(0L, T)
  for (t in 3:T) {
    if (sigma[t] != sigma[t - 1]) flips_per_t[t] <- 1L
  }
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
  if (T >= 3) {
    for (t in 2:(T - 1)) {
      torque[t] <- abs(sigma[t + 1] - 2 * sigma[t] + sigma[t - 1])
    }
  }
  chaos <- detect_period_doubling(sigma_internal)
  list(
    sigma = sigma,
    sign = sign_arr,
    flips = list(total = as.integer(flips_total),
                 rolling = as.integer(rolling_flips),
                 rolling_window = eff_window),
    stability_S_sigma = list(global = stab_global,
                             rolling = rolling_stab,
                             rolling_window = eff_window),
    chaos_indicator = chaos,
    torque_proxy = torque
  )
}

detect_period_doubling <- function(sigma_seq) {
  n <- length(sigma_seq)
  if (n < 4) return(NULL)
  for (depth in 0:3) {
    period <- 2^depth
    if (period >= n) break
    matches <- sigma_seq[1:(n - period)] == sigma_seq[(period + 1):n]
    if (length(matches) > 0) {
      mf <- mean(matches)
      if (mf >= 0.9) return(as.integer(depth))
    }
  }
  NULL
}


# -------------------------------------------------------------------------
# Attractor fit -- mirror hci_shared.attractors
# -------------------------------------------------------------------------

fit_attractor <- function(rows, T_min = 8L, period_threshold = 0.6,
                          amplitude_threshold = 1e-10) {
  T <- nrow(rows)
  warnings_list <- character(0)
  unfit_block <- function(reason) {
    warnings_list <<- c(warnings_list, reason)
    list(
      fitted = FALSE,
      period = 1L,
      period_stability = 0.0,
      dominant_pair = list(axis_a = 0L, axis_b = 0L),
      contraction_lambda = 0.0,
      amplitude_A = 0.0,
      damping_zeta = 0.0,
      confidence = list(oscillation_ratio = 0.0,
                        period_stability_score = 0.0),
      warnings = warnings_list
    )
  }
  if (T < T_min) return(unfit_block(sprintf("trajectory too short for attractor fit (T=%d < T_min=%d)", T, T_min)))
  res <- compositions_to_ilr(rows)
  ilr <- res$ilr
  centered <- sweep(ilr, 2, colMeans(ilr), "-")
  var_per_axis <- colSums(centered * centered)
  total_var <- sum(var_per_axis)
  if (total_var < amplitude_threshold) {
    return(unfit_block("ILR variance below amplitude threshold; trajectory near fixed point"))
  }
  autocorr_lag1 <- colSums(centered[1:(T - 1), , drop = FALSE] *
                           centered[2:T, , drop = FALSE])
  safe_var <- ifelse(var_per_axis > 1e-30, var_per_axis, 1.0)
  period_2_score <- -autocorr_lag1 / safe_var
  max_var <- max(var_per_axis)
  if (max_var < amplitude_threshold) {
    return(unfit_block("no axis has substantive variance; trajectory near fixed point"))
  }
  relative_floor <- max(1e-12 * max_var, 1e-30)
  valid_mask <- var_per_axis > relative_floor
  if (sum(valid_mask) < 1L) {
    return(unfit_block("no axes pass relative variance threshold"))
  }
  sorted_idx <- order(period_2_score, decreasing = TRUE)
  sorted_valid <- sorted_idx[valid_mask[sorted_idx]]
  axis_a <- as.integer(sorted_valid[1] - 1L)  # 0-indexed for output
  if (length(sorted_valid) >= 2L) {
    axis_b <- as.integer(sorted_valid[2] - 1L)
    period_stability <- max(0.0, (period_2_score[sorted_valid[1]] +
                                   period_2_score[sorted_valid[2]]) / 2.0)
    pair_variance <- var_per_axis[sorted_valid[1]] + var_per_axis[sorted_valid[2]]
    envelope <- abs(centered[, sorted_valid[1]]) + abs(centered[, sorted_valid[2]])
  } else {
    axis_b <- axis_a
    period_stability <- max(0.0, period_2_score[sorted_valid[1]])
    pair_variance <- var_per_axis[sorted_valid[1]]
    envelope <- abs(centered[, sorted_valid[1]])
    warnings_list <- c(warnings_list, "1-D limit cycle: only one ILR axis carries variance; axis_b = axis_a in dominant_pair")
  }
  oscillation_ratio <- pair_variance / max(total_var, 1e-30)
  amplitude_A <- sqrt(pair_variance / T)
  log_env <- log(pmax(envelope, 1e-15))
  t_vec <- 0:(T - 1)
  fit <- lm(log_env ~ t_vec)
  slope <- as.numeric(coef(fit)["t_vec"])
  if (is.na(slope)) slope <- 0.0
  contraction_lambda <- slope
  damping_zeta <- -slope
  fitted_ok <- period_stability >= period_threshold && amplitude_A >= amplitude_threshold
  if (!fitted_ok) {
    if (period_stability < period_threshold) {
      warnings_list <- c(warnings_list, sprintf("period_stability %.3f below threshold %g; no clean period-2 structure", period_stability, period_threshold))
    }
    if (amplitude_A < amplitude_threshold) {
      warnings_list <- c(warnings_list, sprintf("amplitude_A %.3e below threshold %g", amplitude_A, amplitude_threshold))
    }
  }
  list(
    fitted = fitted_ok,
    period = if (fitted_ok) 2L else 1L,
    period_stability = period_stability,
    dominant_pair = list(axis_a = axis_a, axis_b = axis_b),
    contraction_lambda = contraction_lambda,
    amplitude_A = amplitude_A,
    damping_zeta = damping_zeta,
    confidence = list(oscillation_ratio = oscillation_ratio,
                      period_stability_score = period_stability),
    warnings = warnings_list
  )
}


# -------------------------------------------------------------------------
# Twin-quaternion factoring + CHSH -- mirror hci_shared.factoring
# -------------------------------------------------------------------------

twin_quaternion_factor <- function(rows,
                                    partition_A = c(1L, 2L, 3L),
                                    partition_B = c(4L, 5L, 6L),
                                    residual_axis = 7L) {
  D <- ncol(rows)
  if (D != 8L) stop(sprintf("twin_quaternion_factor: expected D=8, got D=%d", D))
  # Convert from 1-indexed R input to 1-indexed ILR matrix columns.
  res <- compositions_to_ilr(rows, D = 8L)
  ilr <- res$ilr  # T x 7
  sub_A <- ilr[, partition_A, drop = FALSE]
  sub_B <- ilr[, partition_B, drop = FALSE]
  norms_A <- sqrt(rowSums(sub_A * sub_A))
  norms_B <- sqrt(rowSums(sub_B * sub_B))
  units_A <- sub_A
  units_B <- sub_B
  for (i in seq_len(nrow(ilr))) {
    if (norms_A[i] > 1e-15) units_A[i, ] <- sub_A[i, ] / norms_A[i] else units_A[i, ] <- 0
    if (norms_B[i] > 1e-15) units_B[i, ] <- sub_B[i, ] / norms_B[i] else units_B[i, ] <- 0
  }
  qsra <- quaternion_sandwich_residuals(units_A)
  qsrb <- quaternion_sandwich_residuals(units_B)
  rho_AB <- if (length(qsra$residuals) > 0) {
    dot_q <- abs(rowSums(qsra$quats * qsrb$quats))
    dot_q <- pmax(0, pmin(1, dot_q))
    2.0 * acos(dot_q)
  } else numeric(0)
  rho_summary <- if (length(rho_AB) > 0) {
    list(min = min(rho_AB), max = max(rho_AB), mean = mean(rho_AB),
         median = median(rho_AB), std = sd(rho_AB))
  } else list(min = NA, max = NA, mean = NA, median = NA, std = NA)
  coh_class <- if (length(rho_AB) == 0) "indeterminate"
               else if (rho_summary$mean < 0.2) "tightly_coupled"
               else if (rho_summary$mean < 0.5) "loosely_coupled"
               else "decoupled"
  build_per_step <- function(qsr) {
    if (length(qsr$residuals) == 0L) return(list())
    lapply(seq_along(qsr$residuals), function(t) {
      list(t = as.integer(t - 1L),
           q_w = qsr$quats[t, 1], q_x = qsr$quats[t, 2],
           q_y = qsr$quats[t, 3], q_z = qsr$quats[t, 4],
           angle_rad = qsr$angles[t], residual_linf = qsr$residuals[t])
    })
  }
  list(
    enabled = TRUE,
    partition = list(factor_A = as.integer(partition_A - 1L),
                     factor_B = as.integer(partition_B - 1L),
                     residual_axis = as.integer(residual_axis - 1L)),
    factor_A = list(per_step = build_per_step(qsra),
                    max_residual = if (length(qsra$residuals) > 0) max(qsra$residuals) else NA,
                    mean_residual = if (length(qsra$residuals) > 0) mean(qsra$residuals) else NA),
    factor_B = list(per_step = build_per_step(qsrb),
                    max_residual = if (length(qsrb$residuals) > 0) max(qsrb$residuals) else NA,
                    mean_residual = if (length(qsrb$residuals) > 0) mean(qsrb$residuals) else NA),
    coupling = list(rho_AB_per_step = rho_AB,
                    rho_AB_summary = rho_summary,
                    coherence_class = coh_class)
  )
}

chsh_S_value <- function(quats_A, quats_B,
                          angle_offset_a = 0.0, angle_offset_b = pi / 4.0) {
  T <- nrow(quats_A)
  if (T < 2L || T != nrow(quats_B)) {
    return(list(enabled = FALSE, S_value = 0.0,
                classical_bound = CLASSICAL_BOUND, tsirelson_bound = TSIRELSON_BOUND,
                coherence_score = 0.0, coherence_verdict = "indeterminate",
                n_steps = T))
  }
  vec_A <- quats_A[, 2:4, drop = FALSE]
  vec_B <- quats_B[, 2:4, drop = FALSE]
  axis_fn <- function(angle) c(cos(angle), sin(angle), 0)
  a <- axis_fn(angle_offset_a)
  ap <- axis_fn(angle_offset_a + pi / 2)
  b <- axis_fn(angle_offset_b)
  bp <- axis_fn(angle_offset_b + pi / 2)
  sgn <- function(vec_traj, ax) ifelse(vec_traj %*% ax >= 0, 1, -1)
  s_a <- sgn(vec_A, a); s_ap <- sgn(vec_A, ap)
  s_b <- sgn(vec_B, b); s_bp <- sgn(vec_B, bp)
  E_ab <- mean(s_a * s_b); E_abp <- mean(s_a * s_bp)
  E_apb <- mean(s_ap * s_b); E_apbp <- mean(s_ap * s_bp)
  S <- abs(E_ab + E_abp + E_apb - E_apbp)
  coh_score <- (S - CLASSICAL_BOUND) / (TSIRELSON_BOUND - CLASSICAL_BOUND)
  verdict <- if (S > TSIRELSON_BOUND + 1e-9) "anomalous"
             else if (S < CLASSICAL_BOUND - 1e-9) "independent"
             else if (S < CLASSICAL_BOUND + 0.4) "borderline"
             else "coupled"
  list(enabled = TRUE, S_value = S,
       classical_bound = CLASSICAL_BOUND, tsirelson_bound = TSIRELSON_BOUND,
       coherence_score = coh_score, coherence_verdict = verdict,
       n_steps = T,
       correlations = list(E_ab = E_ab, E_ab_prime = E_abp,
                            E_a_prime_b = E_apb, E_a_prime_b_prime = E_apbp))
}


# -------------------------------------------------------------------------
# Dimension policy classifier -- locked text matches Python verbatim
# -------------------------------------------------------------------------

classify_dimension <- function(D) {
  if (D == 8L) return(list(
    D = 8L, label = "twin_quaternion_native",
    algebra = "D=8 admits twin-quaternion factoring: two coupled SU(2) elements (q_A, q_B) acting on disjoint 3-dim ILR subspaces; coupling angle rho_AB(t) is the load-bearing joint diagnostic",
    processing = "Helmert -> R^7 -> twin-quaternion sandwich on (axes [0,1,2], axes [3,4,5]) plus residual axis 6 -> rho_AB coupling -> CHSH S-value",
    claim_strength = "load-bearing -- smallest case where full algebraic structure (factoring + joint coherence) becomes simultaneously non-trivial and necessary"
  ))
  if (D == 16L) return(list(
    D = 16L, label = "quad_quaternion_native_future",
    algebra = "D=16 admits quad-quaternion factoring: four coupled SU(2) elements (q_A, q_B, q_C, q_D); 6 pairwise coupling angles + 4-way joint correlation",
    processing = "Helmert -> R^15 -> four 3-dim subspaces -> per-channel sandwich + 6 coupling angles + CHSH-4",
    claim_strength = "schema locked; full implementation in v2.1 when first dataset of this dimension lands"
  ))
  if (D == 4L) return(list(
    D = 4L, label = "single_quaternion_native",
    algebra = "SU(2) double cover of SO(3); single-quaternion sandwich on R^3 ILR space; no factoring required",
    processing = "Helmert -> R^3 -> unit-quaternion sandwich",
    claim_strength = "simplest closed-form case; widely useful for cross-domain validation (Backblaze drives, Planck CMB photons, SM neutrinos all sit here)"
  ))
  if (D == 3L) return(list(
    D = 3L, label = "boundary_3part_planar_embed",
    algebra = "SO(2) in R^2; embedded in SO(3) by zero-padding the third axis",
    processing = "Helmert -> R^2 -> embed (z=0) -> sandwich",
    claim_strength = "degenerate boundary; planar consistency support"
  ))
  if (D == 2L) return(list(
    D = 2L, label = "degenerate_2part_bearing_only",
    algebra = "scalar log-ratio only; no rotation degree of freedom",
    processing = "bearing_only path; quaternion_path null",
    claim_strength = "degenerate boundary; bearing diagnostic only"
  ))
  if (D >= 5L && D <= 15L) return(list(
    D = as.integer(D), label = "reduced_or_projected",
    algebra = "SO(D-1); CNQ view projects onto first 3 ILR axes (lossy)",
    processing = "Helmert -> R^(D-1) -> first 3 axes -> sandwich; captured_step_fraction reported global+mean",
    claim_strength = "projection diagnostic -- useful when neither twin nor quad factoring applies natively"
  ))
  if (D >= 17L) return(list(
    D = as.integer(D), label = "reduced_or_projected_high_D",
    algebra = "SO(D-1); first 3 ILR axes (lossy); future Cl(D-1) extension",
    processing = "same as D=5..15 path",
    claim_strength = "projection diagnostic; native algebra extension is INV-044 (open)"
  ))
  list(D = as.integer(D), label = "unsupported", algebra = "n/a",
       processing = "n/a", claim_strength = "out of scope")
}


# -------------------------------------------------------------------------
# Canonical hashing -- v2 RECURSIVE KEY SORT (the v1 R-port bug fixed)
# -------------------------------------------------------------------------

VOLATILE_FIELDS <- c("generated", "timestamp", "wall_clock", "wall_clock_ms",
                     "_run_clock", "environment", "content_sha256",
                     "cnt_content_sha256", "cnq_content_sha256")

strip_volatile <- function(obj) {
  if (is.list(obj) && !is.null(names(obj))) {
    keep <- setdiff(names(obj), VOLATILE_FIELDS)
    out <- lapply(obj[keep], strip_volatile)
    names(out) <- keep
    return(out)
  }
  if (is.list(obj)) {
    return(lapply(obj, strip_volatile))
  }
  obj
}

sort_keys_recursive <- function(obj) {
  if (is.list(obj) && !is.null(names(obj))) {
    sorted_names <- sort(names(obj))
    out <- lapply(sorted_names, function(k) sort_keys_recursive(obj[[k]]))
    names(out) <- sorted_names
    return(out)
  }
  if (is.list(obj)) return(lapply(obj, sort_keys_recursive))
  obj
}

canonical_dumps <- function(obj) {
  cleaned <- sort_keys_recursive(strip_volatile(obj))
  # jsonlite serialiser; ensure_ascii via asJSON's default unicode escaping.
  toJSON(cleaned, auto_unbox = TRUE, null = "null", na = "null",
         pretty = FALSE, digits = 17)
}

canonical_sha256 <- function(obj) {
  txt <- canonical_dumps(obj)
  digest(txt, algo = "sha256", serialize = FALSE)
}

file_sha256 <- function(path) {
  digest(file = path, algo = "sha256")
}


# -------------------------------------------------------------------------
# I/O
# -------------------------------------------------------------------------

ingest_csv <- function(input_csv) {
  if (!file.exists(input_csv)) stop(sprintf("input CSV not found: %s", input_csv))
  df <- read.csv(input_csv, stringsAsFactors = FALSE, check.names = FALSE,
                 fileEncoding = "UTF-8")
  if (ncol(df) < 2) stop("input CSV must have at least 2 columns (label + 1 carrier)")
  labels <- as.character(df[[1]])
  carriers <- colnames(df)[-1]
  rows <- as.matrix(df[, -1, drop = FALSE])
  storage.mode(rows) <- "double"
  if (any(is.na(rows)) || any(!is.finite(rows))) stop("input CSV contains NA or non-finite values")
  if (any(rows < 0)) stop("input CSV contains negative carrier values")
  zero_count <- sum(rows == 0)
  rows[rows == 0] <- DEFAULT_DELTA
  list(labels = labels, carriers = carriers, rows = rows,
       zero_replacement_count = as.integer(zero_count))
}


# -------------------------------------------------------------------------
# Top-level orchestration
# -------------------------------------------------------------------------

cnq_run <- function(input_csv, out_path = NULL, cnt_json_path = NULL) {
  t0 <- Sys.time()
  ing <- ingest_csv(input_csv)
  rows <- ing$rows
  T <- nrow(rows); D <- ncol(rows)
  if (D < 2L) stop("D < 2 not supported")
  dim_policy <- classify_dimension(as.integer(D))
  H <- helmert_basis_op(D)
  ilr_res <- compositions_to_ilr(rows, D)
  ilr <- ilr_res$ilr; radii <- ilr_res$radii

  # Bearing trajectory dispatch
  bearing_only_block <- NULL
  twin_block <- NULL
  quad_block <- NULL
  chsh_block <- NULL

  bearing_block <- list(n_pairs_tested = 0L, max_residual = NA,
                        mean_residual = NA, gate_threshold = GATE_THRESHOLD,
                        gate_pass = FALSE, per_step = list())

  if (D == 4L) {
    huv <- compositions_to_helmert_unit_vectors(rows, 4L)
    qsr <- quaternion_sandwich_residuals(huv$units)
    n_pairs <- length(qsr$residuals)
    bearing_block$n_pairs_tested <- as.integer(n_pairs)
    if (n_pairs > 0) {
      bearing_block$max_residual <- max(qsr$residuals)
      bearing_block$mean_residual <- mean(qsr$residuals)
      bearing_block$gate_pass <- bearing_block$max_residual < GATE_THRESHOLD
      bearing_block$per_step <- lapply(seq_len(n_pairs), function(t) list(
        t = as.integer(t - 1L),
        q_w = qsr$quats[t, 1], q_x = qsr$quats[t, 2],
        q_y = qsr$quats[t, 3], q_z = qsr$quats[t, 4],
        angle_rad = qsr$angles[t], residual_linf = qsr$residuals[t]))
    }
    bearing_block$projection_method <- "exact"
  } else if (D == 8L) {
    twin_block <- twin_quaternion_factor(rows)
    if (length(twin_block$factor_A$per_step) > 0) {
      qA <- t(sapply(twin_block$factor_A$per_step, function(s)
        c(s$q_w, s$q_x, s$q_y, s$q_z)))
      qB <- t(sapply(twin_block$factor_B$per_step, function(s)
        c(s$q_w, s$q_x, s$q_y, s$q_z)))
      chsh_block <- chsh_S_value(qA, qB)
    }
    bearing_block$projection_method <- "reduced_for_overall_view"
  } else if (D == 2L) {
    bearing_only_block <- list(ilr = as.numeric(ilr),
                                note = "D=2 has no rotation degree of freedom; bearing-only path.")
  } else if (D == 16L) {
    quad_block <- list(enabled = FALSE,
                       `_note` = "D=16 quad-quaternion factoring is schema-locked but not yet implemented (INV-043; v2.1 ships when first D=16 dataset lands).")
    bearing_block$projection_method <- "reduced_for_overall_view"
  }

  radial_block <- if (length(radii) > 0) {
    list(ilr_norms = as.numeric(radii),
         min = min(radii), max = max(radii), mean = mean(radii),
         median = median(radii), std = sd(radii))
  } else list(ilr_norms = numeric(0))

  helmsman <- compute_helmsman_family(rows, window = HELMSMAN_ROLLING_WINDOW)
  attractor <- fit_attractor(rows)

  source_hash <- file_sha256(input_csv)
  wall_clock_ms <- as.integer(round(as.numeric(difftime(Sys.time(), t0, units = "secs")) * 1000))

  cnt_ref <- NULL
  if (!is.null(cnt_json_path) && file.exists(cnt_json_path)) {
    cnt_data <- tryCatch(fromJSON(cnt_json_path), error = function(e) NULL)
    if (!is.null(cnt_data)) {
      cnt_ref <- list(
        cnt_engine_version = cnt_data$metadata$engine_version,
        cnt_schema_version = cnt_data$metadata$schema_version,
        cnt_content_sha256 = if (!is.null(cnt_data$diagnostics$cnt_content_sha256))
          cnt_data$diagnostics$cnt_content_sha256
        else cnt_data$diagnostics$content_sha256,
        cnt_json_path = as.character(cnt_json_path)
      )
    }
  }

  payload <- list(
    metadata = list(
      engine = ENGINE_NAME,
      engine_version = ENGINE_VERSION,
      schema_version = SCHEMA_VERSION,
      engine_implementation = "r",
      implementation_lang_version = paste("R", paste(R.version$major, R.version$minor, sep = ".")),
      principle = ENGINE_PRINCIPLE,
      generated = format(Sys.time(), "%Y-%m-%dT%H:%M:%SZ", tz = "UTC"),
      wall_clock_ms = wall_clock_ms,
      environment = list(
        r_version = paste(R.version$major, R.version$minor, sep = "."),
        platform = R.version$platform,
        hostname_hash = substr(digest(Sys.info()["nodename"], algo = "sha256",
                                       serialize = FALSE), 1, 16)
      )
    ),
    input = list(
      source_file = as.character(input_csv),
      source_file_sha256 = source_hash,
      n_records = T, n_carriers = D,
      carriers = ing$carriers, labels = ing$labels,
      zero_replacement_count = ing$zero_replacement_count
    ),
    cnt_reference = cnt_ref,
    cnq_view = list(
      dimension_policy = dim_policy,
      frame = list(
        type = "Helmert orthonormal contrast",
        signature = "row k has (k+1) entries +1/sqrt(n*(n+1)) followed by -n/sqrt(n*(n+1))",
        basis_matrix = H
      ),
      bearing_trajectory = bearing_block,
      radial_trajectory = radial_block,
      bearing_only = bearing_only_block
    ),
    helmsman_family = helmsman,
    attractor_fit = attractor,
    twin_quaternion_factoring = twin_block,
    quad_quaternion_factoring = quad_block,
    chsh_diagnostic = chsh_block,
    bundle_view = NULL,
    diagnostics = list(warnings = list())
  )

  digest_val <- canonical_sha256(payload)
  payload$diagnostics$cnq_content_sha256 <- digest_val

  if (!is.null(out_path)) {
    out_dir <- dirname(out_path)
    if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
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
    cat("Usage: Rscript cnq.R --input-csv <path> [-o <output.json>] [--cnt-json <path>]\n")
    return(invisible(0))
  }
  args <- list()
  i <- 1
  while (i <= length(argv)) {
    a <- argv[i]
    if (a == "--input-csv") { args$input_csv <- argv[i + 1]; i <- i + 2 }
    else if (a %in% c("-o", "--output")) { args$output <- argv[i + 1]; i <- i + 2 }
    else if (a == "--cnt-json") { args$cnt_json <- argv[i + 1]; i <- i + 2 }
    else { i <- i + 1 }
  }
  if (is.null(args$input_csv)) {
    message("error: --input-csv is required")
    return(invisible(2))
  }
  payload <- cnq_run(args$input_csv,
                      out_path = args$output,
                      cnt_json_path = args$cnt_json)
  cat(sprintf("engine             = %s v%s (schema %s)\n",
              payload$metadata$engine, payload$metadata$engine_version,
              payload$metadata$schema_version))
  cat(sprintf("T x D              = %d x %d\n",
              payload$input$n_records, payload$input$n_carriers))
  cat(sprintf("dimension_policy   = %s\n", payload$cnq_view$dimension_policy$label))
  if (!is.na(payload$cnq_view$bearing_trajectory$max_residual)) {
    cat(sprintf("bearing.max_residual = %.3e (gate: %s)\n",
                payload$cnq_view$bearing_trajectory$max_residual,
                if (payload$cnq_view$bearing_trajectory$gate_pass) "PASS" else "FAIL"))
  }
  cat(sprintf("cnq_content_sha256 = %s\n", payload$diagnostics$cnq_content_sha256))
  invisible(0)
}

if (!interactive() && length(commandArgs(trailingOnly = TRUE)) > 0) {
  main()
}
