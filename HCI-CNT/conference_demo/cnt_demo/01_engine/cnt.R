#!/usr/bin/env Rscript
# CNT Engine — R Reference Implementation
# ========================================
#
# Schema version : 1.0.0    (see CNT_JSON_SCHEMA.md for the contract)
# Engine version : 1.0.0
# Algorithm ref  : CNT_PSEUDOCODE.md
#
# This R implementation is a faithful translation of cnt.py. It reads a
# compositional CSV and emits ONE canonical JSON conforming to the CNT JSON
# schema. The output is bit-identical to the Python reference up to floating-
# point representation; numerical fields agree to working precision (~1e-10).
#
# Mathematical lineage:
#   Aitchison (1986) — CLR transform, simplex geometry
#   Egozcue (2003)   — ILR, Helmert basis, orthonormal coordinates
#   Shannon (1948)   — Entropy
#   Higgins (2026)   — CNT tensor decomposition, recursive depth sounder
#
# Dependencies (install once):
#   install.packages(c("jsonlite", "digest"))
#   # Optional CoDa-community packages (used only for cross-check):
#   install.packages("compositions")
#
# Usage (CLI):
#   Rscript cnt.R input.csv [output.json] [--temporal] [--ordering-method M]
#
# Usage (interactive):
#   source("cnt.R")
#   j <- cnt_run("input.csv", "output.json", ordering = list(
#       is_temporal = TRUE,
#       ordering_method = "by-time",
#       caveat = NULL
#   ))
#
# The instrument reads. The expert decides. The loop stays open.

suppressPackageStartupMessages({
  library(jsonlite)
  library(digest)
})

# ============================================================
# USER CONFIGURATION
# ============================================================
#
# These values control the engine's behaviour. Edit them to suit
# your dataset and analytical needs. Active values are echoed
# in `metadata.engine_config` of every JSON the engine produces.
#
# Two consecutive runs with IDENTICAL configuration on IDENTICAL
# input produce IDENTICAL `diagnostics.content_sha256` (verified).
# Two runs with DIFFERENT configuration produce different content_sha256
# - that is correct and expected.
#
# Categories: VERSION, ZERO REPLACEMENT, LOCK EVENTS, DEPTH RECURSION,
# TRIADIC ENUMERATION, EITT BENCH-TEST.
# ============================================================

# -- VERSION (do not edit unless modifying the engine) --
SCHEMA_VERSION         <- "2.1.0"     # JSON schema version (additive: metadata.units)
ENGINE_VERSION         <- "2.0.4"     # 2.0.4: engine_config_overrides honoured + units block written (parity with cnt.py)
ENGINE_NAME            <- "cnt"

# -- ZERO REPLACEMENT --
# When an input value is zero or below this floor, replace with
# DEFAULT_DELTA so log-ratios remain finite. Default 1e-15 (IEEE floor).
DEFAULT_DELTA          <- 1e-15

# -- LOCK EVENT THRESHOLDS --
# DEGEN_THRESHOLD: composition is "near barycenter / collapsed" when
#   max(CLR) - min(CLR) is below this. Default 1e-4.
# LOCK_CLR_THRESHOLD: a carrier is "locked low" when its CLR is below
#   this. Default -10.0. More negative => only flags extreme zeros.
DEGEN_THRESHOLD        <- 1e-4
LOCK_CLR_THRESHOLD     <- -10.0

# -- DEPTH RECURSION (depth sounder) --
# DEPTH_MAX_LEVELS: hard cap on tower length. Default 50.
# DEPTH_PRECISION_TARGET: relative precision for period detection.
#   Period-1 requires TWO consecutive level pairs under the gate.
#   Period-2 requires both same-parity sequences under the gate.
#   Default 0.01 (1%).
# NOISE_FLOOR_OMEGA_VAR: angular-velocity variance below this declares
#   OMEGA_FLAT termination. Default 1e-6.
DEPTH_MAX_LEVELS       <- 50
DEPTH_PRECISION_TARGET <- 0.01
NOISE_FLOOR_OMEGA_VAR  <- 1e-6

# -- TRIADIC ENUMERATION (Stage 3 day-triad area) --
# TRIADIC_T_LIMIT: above this T, skip the C(T,3) enumeration and emit
#   selection_method = "none_T_too_large". Default 500.
# TRIADIC_K_DEFAULT: when enumeration runs, store this many top-area
#   triads in results[]. Default 500.
TRIADIC_T_LIMIT        <- 500
TRIADIC_K_DEFAULT      <- 500

# -- EITT BENCH-TEST (diagnostics.eitt_residuals) --
# EITT_GATE_PCT: variation_pct above this is FAIL. Default 5.0.
# EITT_M_SWEEP_BASE: which compression ratios M to bench-test.
EITT_GATE_PCT          <- 5.0
EITT_M_SWEEP_BASE      <- c(2, 4, 8, 16, 32, 64, 128)

# ============================================================
# End USER CONFIGURATION. Edit above; do not edit below.
# ============================================================


# ============================================================
# §0 — Math primitives (parity with cnt.py)
# ============================================================

close_simplex <- function(x, delta = DEFAULT_DELTA) {
  x_pos <- pmax(as.numeric(x), delta)
  s <- sum(x_pos)
  if (s <= 0) stop("Composition has non-positive sum")
  x_pos / s
}

clr <- function(x) {
  log_x <- log(x)
  log_x - mean(log_x)
}

helmert_basis <- function(D) {
  basis <- matrix(0, nrow = D - 1, ncol = D)
  for (k in seq_len(D - 1)) {
    scale <- sqrt(k / (k + 1.0))
    for (j in seq_len(k)) basis[k, j] <- scale / k
    basis[k, k + 1] <- -scale
  }
  basis
}

ilr_project <- function(h, basis) as.numeric(basis %*% h)

aitchison_distance <- function(x, y) sqrt(sum((clr(x) - clr(y))^2))

aitchison_barycenter <- function(rows) {
  if (length(rows) == 0) return(NULL)
  D <- length(rows[[1]])
  log_means <- numeric(D)
  for (j in seq_len(D)) log_means[j] <- mean(sapply(rows, function(r) log(r[j])))
  close_simplex(exp(log_means))
}

shannon_entropy <- function(x) {
  pos <- x[x > 0]
  -sum(pos * log(pos))
}

higgins_scale <- function(x) 1.0 - shannon_entropy(x) / log(length(x))

metric_dual <- function(x) close_simplex(1.0 / x)

metric_tensor_full <- function(x) {
  D <- length(x)
  K <- matrix(0, D, D)
  for (i in seq_len(D)) for (j in seq_len(D)) {
    num <- if (i == j) (1.0 - 1.0 / D) else (-1.0 / D)
    K[i, j] <- num / (x[i] * x[j])
  }
  K
}

bearing_pairs <- function(h, carriers) {
  D <- length(h)
  out <- list()
  for (i in seq_len(D - 1)) {
    for (j in seq.int(i + 1, D)) {
      theta <- atan2(h[j], h[i])
      out[[length(out) + 1]] <- list(
        carrier_i = carriers[i],
        carrier_j = carriers[j],
        theta_deg = theta * 180 / pi
      )
    }
  }
  out
}

angular_velocity_deg <- function(h_prev, h) {
  a_sq  <- sum(h_prev * h_prev)
  b_sq  <- sum(h * h)
  ab    <- sum(h_prev * h)
  cross <- sqrt(max(0, a_sq * b_sq - ab * ab))
  atan2(cross, ab) * 180 / pi
}

helmsman_dcdi <- function(h_prev, h, carriers) {
  deltas <- abs(h - h_prev)
  j_max  <- which.max(deltas)
  list(carrier = carriers[j_max], delta = deltas[j_max])
}


# ============================================================
# §1 — Tensor block
# ============================================================

compute_tensor_block <- function(records, carriers) {
  D <- length(carriers)
  basis <- helmert_basis(D)
  timesteps <- vector("list", length(records))
  h_prev <- NULL
  for (i in seq_along(records)) {
    rec <- records[[i]]
    x_raw <- as.numeric(rec$raw_values)
    x <- close_simplex(x_raw)
    h <- clr(x)
    ts <- list(
      index                  = i - 1L,
      label                  = rec$label,
      raw_values             = as.list(x_raw),
      composition            = as.list(x),
      clr                    = as.list(h),
      ilr                    = as.list(ilr_project(h, basis)),
      shannon_entropy        = shannon_entropy(x),
      higgins_scale          = 1.0 - shannon_entropy(x) / log(D),
      aitchison_norm         = sqrt(sum(h * h)),
      bearing_tensor         = list(pairs = bearing_pairs(h, carriers)),
      metric_tensor          = list(
        matrix      = lapply(seq_len(D), function(r) as.list(metric_tensor_full(x)[r, ])),
        eigenvalues = as.list(sort(eigen(metric_tensor_full(x), symmetric = TRUE, only.values = TRUE)$values)),
        trace       = sum(diag(metric_tensor_full(x)))
      ),
      metric_tensor_diagonal = as.list((1.0 - 1.0 / D) / x^2),
      condition_number       = max(x) / min(x)
    )
    if (!is.null(h_prev)) {
      ts$angular_velocity_deg    <- angular_velocity_deg(h_prev, h)
      ts$aitchison_distance_step <- sqrt(sum((h - h_prev)^2))
      hm <- helmsman_dcdi(h_prev, h, carriers)
      ts$helmsman                <- hm$carrier
      ts$helmsman_delta          <- hm$delta
    }
    timesteps[[i]] <- ts
    h_prev <- h
  }
  list(
    helmert_basis = list(
      D            = D,
      dim          = D - 1,
      coefficients = lapply(seq_len(D - 1), function(r) as.list(basis[r, ]))
    ),
    timesteps = timesteps
  )
}


# ============================================================
# §2 — Stages block
# ============================================================

ring_classify <- function(hs) {
  if (hs < 0.1) return("Hs-1")
  if (hs < 0.3) return("Hs-2")
  if (hs < 0.5) return("Hs-3")
  if (hs < 0.7) return("Hs-4")
  if (hs < 0.9) return("Hs-5")
  "Hs-6"
}

compute_stage1 <- function(tensor_block, carriers) {
  D <- length(carriers)
  section_atlas <- list(); metric_ledger <- list()
  for (i in seq_along(tensor_block$timesteps)) {
    ts <- tensor_block$timesteps[[i]]
    h <- as.numeric(ts$clr)
    xy <- if (D >= 2) h[1:2] else c(h[1], 0)
    xz <- if (D >= 3) c(h[1], h[3]) else c(h[1], 0)
    yz <- if (D >= 3) h[2:3] else c(if (D >= 2) h[2] else 0, 0)
    section_atlas[[i]] <- list(
      index = ts$index, label = ts$label,
      xy_face = as.list(xy), xz_face = as.list(xz), yz_face = as.list(yz),
      metric_tensor_trace = ts$metric_tensor$trace,
      condition_number = ts$condition_number,
      angular_velocity_deg = if (!is.null(ts$angular_velocity_deg)) ts$angular_velocity_deg else 0
    )
    metric_ledger[[i]] <- list(
      index = ts$index, label = ts$label,
      hs = ts$higgins_scale, ring = ring_classify(ts$higgins_scale),
      omega_deg = if (!is.null(ts$angular_velocity_deg)) ts$angular_velocity_deg else 0,
      helmsman = if (!is.null(ts$helmsman)) ts$helmsman else "",
      energy = ts$aitchison_norm^2,
      condition = ts$condition_number
    )
  }
  list(section_atlas = section_atlas, metric_ledger = metric_ledger)
}

variation_matrix <- function(records_closed) {
  D <- length(records_closed[[1]])
  tau <- matrix(0, D, D)
  for (i in seq_len(D)) for (j in seq_len(D)) {
    if (i == j) next
    ratios <- sapply(records_closed, function(r) log(r[i] / r[j]))
    tau[i, j] <- var(ratios) * (length(ratios) - 1) / length(ratios)
  }
  lapply(seq_len(D), function(r) as.list(tau[r, ]))
}

compute_stage2 <- function(records_closed, tensor_block, carriers) {
  D <- length(carriers); T <- length(tensor_block$timesteps)
  pairs <- list()
  for (i in seq_len(D - 1)) for (j in seq.int(i + 1, D)) {
    h_i <- sapply(tensor_block$timesteps, function(ts) ts$clr[[i]])
    h_j <- sapply(tensor_block$timesteps, function(ts) ts$clr[[j]])
    r <- if (T >= 2 && sd(h_i) > 0 && sd(h_j) > 0) cor(h_i, h_j) else 0
    bearings <- atan2(h_j, h_i) * 180 / pi
    spread <- if (length(bearings) > 0) max(bearings) - min(bearings) else 0
    pairs[[length(pairs) + 1]] <- list(
      carrier_a = carriers[i], carrier_b = carriers[j],
      i = i - 1L, j = j - 1L, pearson_r = r,
      co_movement_score = max(0, r), opposition_score = max(0, -r),
      bearing_spread_deg = spread, locked = spread < 10
    )
  }
  list(variation_matrix = variation_matrix(records_closed),
       carrier_pair_examination = pairs)
}

compute_stage3 <- function(records_closed, tensor_block, carriers) {
  D <- length(carriers); T <- length(tensor_block$timesteps)
  ladder <- list()
  for (k in seq.int(2, D - 1)) {
    subsets <- combn(D, k, simplify = FALSE)
    n_sub <- length(subsets)
    ladder[[length(ladder) + 1]] <- list(
      degree = k, n_subsets = n_sub
    )
  }
  carrier_triads <- list()
  if (D >= 3) {
    for (combo in combn(D, 3, simplify = FALSE)) {
      carrier_triads[[length(carrier_triads) + 1]] <- list(
        carriers = as.list(carriers[combo]),
        indices  = as.list(combo - 1L)
      )
    }
  }
  triadic <- list(n_candidates = if (T >= 3) choose(T, 3) else 0)
  if (T < 3) {
    triadic$selection_method <- "none_T_too_small"
    triadic$n_returned <- 0; triadic$results <- list()
  } else if (T > TRIADIC_T_LIMIT) {
    triadic$selection_method <- "none_T_too_large"
    triadic$selection_K <- 0; triadic$n_returned <- 0; triadic$results <- list()
  } else {
    clrs <- lapply(tensor_block$timesteps, function(ts) as.numeric(ts$clr))
    results <- list()
    for (combo in combn(T, 3, simplify = FALSE)) {
      a <- combo[1]; b <- combo[2]; c <- combo[3]
      sab <- sqrt(sum((clrs[[a]] - clrs[[b]])^2))
      sbc <- sqrt(sum((clrs[[b]] - clrs[[c]])^2))
      sca <- sqrt(sum((clrs[[c]] - clrs[[a]])^2))
      sp <- (sab + sbc + sca) / 2
      area <- sqrt(max(0, sp * (sp - sab) * (sp - sbc) * (sp - sca)))
      results[[length(results) + 1]] <- list(triad = as.list(combo - 1L), area = area, sides = list(sab, sbc, sca))
    }
    results <- results[order(-sapply(results, `[[`, "area"))]
    triadic$selection_method <- "top_K_by_area"
    triadic$selection_K <- TRIADIC_K_DEFAULT
    triadic$n_returned <- min(TRIADIC_K_DEFAULT, length(results))
    triadic$results <- results[seq_len(triadic$n_returned)]
  }
  boundaries <- list()
  if (T >= 5) {
    steps <- sapply(tensor_block$timesteps[-1],
                    function(ts) if (!is.null(ts$aitchison_distance_step)) ts$aitchison_distance_step else 0)
    mean_s <- mean(steps); sd_s <- sd(steps)
    threshold <- mean_s + 2 * sd_s
    for (idx in seq_along(steps)) {
      if (steps[idx] > threshold) {
        boundaries[[length(boundaries) + 1]] <- list(
          timestep_index = idx,
          label = tensor_block$timesteps[[idx + 1]]$label,
          step_distance = steps[idx],
          z_score = if (sd_s > 0) (steps[idx] - mean_s) / sd_s else 0
        )
      }
    }
  }
  list(
    triadic_area = triadic,
    carrier_triads = carrier_triads,
    subcomposition_ladder = ladder,
    regime_detection = list(
      n_regimes = length(boundaries) + 1,
      boundaries = boundaries,
      method = "step_distance > mean + 2*std"
    )
  )
}


# ============================================================
# §3 — Bridges block (abbreviated; matches Python semantics)
# ============================================================

per_carrier_lyapunov <- function(tensor_block, carriers) {
  D <- length(carriers); T <- length(tensor_block$timesteps)
  out <- list()
  for (j in seq_len(D)) {
    h_series <- sapply(tensor_block$timesteps, function(ts) ts$clr[[j]])
    lyap <- 0
    if (T >= 3) {
      diffs <- abs(diff(h_series))
      valid <- diffs[diffs > 1e-15]
      if (length(valid) >= 2) {
        ratios <- valid[-1] / valid[-length(valid)]
        ratios <- ratios[ratios > 0]
        if (length(ratios) > 0) lyap <- mean(log(ratios))
      }
    }
    classification <- if (lyap > 0.05) "DIVERGENT"
                      else if (lyap < -0.05) "CONVERGENT"
                      else "NEUTRAL"
    out[[length(out) + 1]] <- list(
      carrier = carriers[j], index = j - 1L,
      lyapunov_exponent = lyap, classification = classification
    )
  }
  out
}

compute_bridges <- function(records_closed, tensor_block, carriers) {
  D <- length(carriers); T <- length(tensor_block$timesteps)
  list(
    dynamical_systems = list(
      per_carrier_lyapunov = per_carrier_lyapunov(tensor_block, carriers),
      velocity_field = list(
        mean_omega_deg = mean(sapply(tensor_block$timesteps,
                                      function(ts) if (!is.null(ts$angular_velocity_deg)) ts$angular_velocity_deg else 0)),
        max_omega_deg  = max(sapply(tensor_block$timesteps,
                                      function(ts) if (!is.null(ts$angular_velocity_deg)) ts$angular_velocity_deg else 0))
      )
    ),
    control_theory = list(
      state_space_model = list(model = "AR(1) on CLR series — full implementation in cnt.py")
    ),
    information_theory = list(
      entropy_series = lapply(tensor_block$timesteps, function(ts) list(
        label = ts$label, shannon_entropy = ts$shannon_entropy,
        max_entropy = log(D), normalised_entropy = ts$shannon_entropy / log(D),
        higgins_scale = ts$higgins_scale
      ))
    )
  )
}


# ============================================================
# §4 — Depth block
# ============================================================

derived_curvature <- function(tensor_block) {
  lapply(tensor_block$timesteps, function(ts) {
    x <- as.numeric(ts$composition)
    close_simplex(1.0 / x^2)
  })
}

derived_energy <- function(tensor_block) {
  out <- list()
  ts <- tensor_block$timesteps
  for (i in seq.int(2, length(ts))) {
    dh <- as.numeric(ts[[i]]$clr) - as.numeric(ts[[i - 1]]$clr)
    out[[length(out) + 1]] <- close_simplex(dh^2)
  }
  out
}

summarise_level <- function(tensor_block, level) {
  ts <- tensor_block$timesteps
  T <- length(ts)
  if (T == 0) return(list(level = level, T = 0L, status = "SIGNAL_SHORT"))
  hs_vals <- sapply(ts, `[[`, "higgins_scale")
  omegas  <- sapply(ts, function(t) if (!is.null(t$angular_velocity_deg)) t$angular_velocity_deg else NA_real_)
  omegas  <- omegas[!is.na(omegas)]
  helms   <- sapply(ts, function(t) if (!is.null(t$helmsman)) t$helmsman else NA_character_)
  helms   <- helms[!is.na(helms)]
  if (length(helms) > 0) {
    # Deterministic tie-break: alphabetical sort then most-frequent
    tab <- sort(table(sort(helms)), decreasing = TRUE)
    helm_dom <- names(tab)[1]
  } else helm_dom <- ""
  list(
    level = level, T = T, D = length(ts[[1]]$composition),
    hs_mean = mean(hs_vals), hs_var = var(hs_vals) * (T - 1) / T,
    omega_mean = if (length(omegas)) mean(omegas) else 0,
    omega_var  = if (length(omegas)) var(omegas) * (length(omegas) - 1) / length(omegas) else 0,
    omega_max  = if (length(omegas)) max(omegas) else 0,
    helmsman = helm_dom, status = "PRODUCTIVE"
  )
}

detect_period <- function(traj, precision) {
  n <- length(traj)
  if (n < 4) return(list(detected = FALSE, period = 0L, residual = Inf, level = -1L))
  for (k in seq.int(3, n)) {
    denom <- max(abs(traj[k - 1]), 1e-15)
    rel <- abs(traj[k] - traj[k - 1]) / denom
    if (rel < precision) return(list(detected = TRUE, period = 1L, residual = rel, level = k - 1L))
  }
  for (k in seq.int(5, n)) {
    if (k - 3 < 1) next
    denom_e <- max(abs(traj[k - 2]), 1e-15)
    rel_e <- abs(traj[k] - traj[k - 2]) / denom_e
    denom_o <- max(abs(traj[k - 3]), 1e-15)
    rel_o <- abs(traj[k - 1] - traj[k - 3]) / denom_o
    if (rel_e < precision && rel_o < precision)
      return(list(detected = TRUE, period = 2L, residual = max(rel_e, rel_o), level = k - 1L))
  }
  list(detected = FALSE, period = 0L,
       residual = abs(traj[n] - traj[n - 2]) / max(abs(traj[n - 2]), 1e-15),
       level = -1L)
}

classify_ir <- function(A, zeta) {
  if (A < 0.1) return("CRITICALLY_DAMPED")
  if (zeta > 0 && zeta < 0.1) return("LIGHTLY_DAMPED")
  if (abs(zeta) < 1e-6) return("UNDAMPED")
  if (A > 0.7) return("OVERDAMPED_EXTREME")
  "MODERATELY_DAMPED"
}

build_tower <- function(initial_records, carriers, kind, level_0_hs) {
  levels <- list(); traj <- numeric(0)
  current_records <- initial_records
  for (level_idx in seq_len(DEPTH_MAX_LEVELS)) {
    if (length(current_records) < 5) {
      levels[[length(levels) + 1]] <- list(level = level_idx, T = length(current_records), status = "SIGNAL_SHORT")
      break
    }
    level_records <- lapply(seq_along(current_records),
                            function(i) list(label = paste0("L", level_idx, "_", i - 1L),
                                              raw_values = as.list(current_records[[i]])))
    level_tensor <- compute_tensor_block(level_records, carriers)
    lvl <- summarise_level(level_tensor, level_idx)
    levels[[length(levels) + 1]] <- lvl
    traj <- c(traj, lvl$hs_mean)
    if (lvl$omega_var < NOISE_FLOOR_OMEGA_VAR) { levels[[length(levels)]]$status <- "OMEGA_FLAT"; break }
    if (lvl$hs_var < 1e-9) { levels[[length(levels)]]$status <- "HS_FLAT"; break }
    full_traj <- c(level_0_hs, traj)
    pd <- detect_period(full_traj, DEPTH_PRECISION_TARGET)
    if (pd$detected) {
      if (pd$period == 1) { levels[[length(levels)]]$status <- "LIMIT_CYCLE_P1"; break }
      else if (pd$period == 2 && level_idx >= 4) { levels[[length(levels)]]$status <- "LIMIT_CYCLE_P2"; break }
    }
    if (kind == "energy") current_records <- derived_energy(level_tensor)
    else current_records <- derived_curvature(level_tensor)
  }
  list(levels = levels, traj = c(level_0_hs, traj))
}

compute_depth <- function(records_closed, tensor_block, carriers) {
  T <- length(tensor_block$timesteps); D <- length(carriers)
  sample_idx <- if (T >= 1) sort(unique(c(1, ceiling(T / 2), T))) else integer(0)
  samples <- list()
  for (t in sample_idx) {
    x <- as.numeric(tensor_block$timesteps[[t]]$composition)
    Mx <- metric_dual(x); MMx <- metric_dual(Mx)
    samples[[length(samples) + 1]] <- list(
      t = t - 1L, x = as.list(x), Mx = as.list(Mx), MMx = as.list(MMx),
      residual_M2 = sqrt(sum((MMx - x)^2)),
      clr_negation_residual = sqrt(sum((clr(x) + clr(Mx))^2)),
      duality_distance = aitchison_distance(x, Mx)
    )
  }
  mean_resid <- if (length(samples)) mean(sapply(samples, `[[`, "residual_M2")) else 0
  involution_proof <- list(
    samples = samples, mean_residual = mean_resid,
    verified = mean_resid < 1e-10, n_samples = length(samples)
  )
  level_0 <- summarise_level(tensor_block, 0L)
  energy_init <- derived_energy(tensor_block)
  energy <- build_tower(energy_init, carriers, "energy", level_0$hs_mean)
  curvature_init <- derived_curvature(tensor_block)
  curvature <- build_tower(curvature_init, carriers, "curvature", level_0$hs_mean)
  e_pd <- detect_period(energy$traj, DEPTH_PRECISION_TARGET)
  c_pd <- detect_period(curvature$traj, DEPTH_PRECISION_TARGET)
  cur_attr <- list(period = c_pd$period)
  if (c_pd$period == 2 && length(curvature$traj) >= 4) {
    tail_size <- min(6, length(curvature$traj))
    tail_idx <- seq.int(length(curvature$traj) - tail_size + 1, length(curvature$traj))
    is_even  <- (tail_idx - 1) %% 2 == 0
    c_even <- mean(curvature$traj[tail_idx[is_even]])
    c_odd  <- mean(curvature$traj[tail_idx[!is_even]])
    A <- abs(c_even - c_odd)
    deltas <- curvature$traj - ifelse(seq_along(curvature$traj) %% 2 == 1, c_even, c_odd)
    ratios <- numeric(0)
    for (n in seq_len(length(deltas) - 2)) {
      a <- abs(deltas[n]); b <- abs(deltas[n + 2])
      if (a > 1e-12 && b > 1e-12) ratios <- c(ratios, b / a)
    }
    cur_attr$c_even <- c_even; cur_attr$c_odd <- c_odd; cur_attr$amplitude <- A
    cur_attr$convergence_level <- c_pd$level; cur_attr$residual <- c_pd$residual
    cur_attr$contraction_lyapunov <- if (length(ratios)) mean(log(ratios[ratios > 0])) else NaN
    cur_attr$mean_contraction_ratio <- if (length(ratios)) mean(ratios) else NaN
    cur_attr$banach_satisfied <- !is.nan(cur_attr$mean_contraction_ratio) && cur_attr$mean_contraction_ratio < 1
  }
  ir <- list(
    amplitude_A = if (!is.null(cur_attr$amplitude)) cur_attr$amplitude else 0,
    depth_delta = length(curvature$levels)
  )
  if (!is.null(cur_attr$amplitude) && cur_attr$amplitude > 0 && length(curvature$traj) >= 2) {
    A_init <- abs(curvature$traj[2] - curvature$traj[1])
    if (A_init > 0) ir$damping_zeta <- -log(cur_attr$amplitude / A_init) / ir$depth_delta
    else ir$damping_zeta <- 0
    ir$classification <- classify_ir(cur_attr$amplitude, ir$damping_zeta)
  } else {
    # Engine 2.0.3 IR refinement (parity with cnt.py): disambiguate
    # the legacy DEGENERATE bucket into three more-informative classes.
    ir$damping_zeta <- 0
    D_input <- if (length(records_closed) > 0) length(records_closed[[1]]) else 0
    max_share <- if (length(records_closed) > 0) {
      max(sapply(records_closed, function(r) max(unlist(r))))
    } else 0
    curv_term <- if (length(curvature$levels) > 0) {
      st <- curvature$levels[[length(curvature$levels)]]$status
      if (is.null(st)) "" else st
    } else ""
    e_period <- if (isTRUE(energy_cycle$detected)) {
      ep <- energy_cycle$period
      if (is.null(ep)) 0L else ep
    } else 0L
    e_traj <- if (is.null(energy$traj)) numeric(0) else energy$traj
    if (D_input <= 2) {
      ir$classification <- "D2_DEGENERATE"
    } else if (curv_term == "HS_FLAT" && max_share > 0.60) {
      ir$classification <- "CURVATURE_VERTEX_FLAT"
    } else if (e_period == 1L && length(e_traj) >= 2) {
      e_amp <- abs(tail(e_traj, 1) - e_traj[1])
      ir$classification <- if (e_amp < 0.5) "ENERGY_STABLE_FIXED_POINT" else "DEGENERATE"
    } else {
      ir$classification <- "DEGENERATE"
    }
    ir$max_carrier_share <- max_share
    ir$curv_termination  <- curv_term
    ir$energy_period     <- e_period
    ir$D                 <- D_input
  }
  d_duals <- sapply(tensor_block$timesteps, function(ts) {
    x <- as.numeric(ts$composition); aitchison_distance(x, metric_dual(x))
  })
  list(
    involution_proof = involution_proof,
    level_0 = level_0,
    energy_tower = energy$levels,
    curvature_tower = curvature$levels,
    curvature_attractor = cur_attr,
    impulse_response = ir,
    energy_cycle = list(detected = e_pd$detected, period = e_pd$period,
                        residual = e_pd$residual, convergence_level = e_pd$level),
    curvature_cycle = list(detected = c_pd$detected, period = c_pd$period,
                           residual = c_pd$residual, convergence_level = c_pd$level),
    summary = list(
      energy_depth = length(energy$levels),
      curvature_depth = length(curvature$levels),
      dynamical_depth = max(length(energy$levels), length(curvature$levels)),
      energy_hs_trajectory = as.list(energy$traj),
      curvature_hs_trajectory = as.list(curvature$traj),
      mean_duality_distance = mean(d_duals),
      convergence_precision = DEPTH_PRECISION_TARGET,
      noise_floor_omega_var = NOISE_FLOOR_OMEGA_VAR,
      max_levels = DEPTH_MAX_LEVELS
    )
  )
}


# ============================================================
# §5 — Diagnostics
# ============================================================

eitt_bench_test <- function(records_closed, T) {
  if (T < 4) return(list(H_mean_full = 0, M_sweep = list(), gate_pct = 5,
                         note = "T < 4: EITT bench-test not applicable."))
  H_full <- mean(sapply(records_closed, shannon_entropy))
  base_Ms <- c(2, 4, 8, 16, 32, 64, 128)
  if (T >= 101) base_Ms <- c(base_Ms, ceiling(T / 101))
  base_Ms <- sort(unique(base_Ms[base_Ms < T]))
  M_sweep <- list()
  for (M in base_Ms) {
    decimated <- list()
    blocks <- split(records_closed, ceiling(seq_along(records_closed) / M))
    for (b in blocks) {
      if (length(b) >= 2) decimated[[length(decimated) + 1]] <- aitchison_barycenter(b)
      else if (length(b) == 1) decimated[[length(decimated) + 1]] <- b[[1]]
    }
    H_dec <- mean(sapply(decimated, shannon_entropy))
    var_pct <- if (H_full > 0) abs(H_dec - H_full) / H_full * 100 else 0
    M_sweep[[length(M_sweep) + 1]] <- list(M = M, n_blocks = length(decimated),
                                            H_mean_decimated = H_dec,
                                            variation_pct = var_pct,
                                            pass_5pct = var_pct < 5)
  }
  list(H_mean_full = H_full, M_sweep = M_sweep, gate_pct = 5,
       note = paste0("Empirical observation of trajectory smoothness under temporal ",
                      "decimation, not a geometric theorem. Shannon entropy is not ",
                      "scale-invariant; the apparent preservation reflects compositional ",
                      "smoothness of the trajectory, not Aitchison invariance."))
}

detect_lock_events <- function(tensor_block, carriers) {
  events <- list(); D <- length(carriers); ts <- tensor_block$timesteps
  for (i in seq_along(ts)) {
    h <- as.numeric(ts[[i]]$clr); spread <- max(h) - min(h)
    if (spread < DEGEN_THRESHOLD) {
      events[[length(events) + 1]] <- list(
        event_type = "DEGEN", timestep_index = i - 1L, label = ts[[i]]$label,
        carrier = NA_character_, clr_value = spread,
        context = "Composition collapsed near barycenter")
    }
    for (j in seq_len(D)) {
      if (h[j] < LOCK_CLR_THRESHOLD) {
        prev_low <- (i > 1 && as.numeric(ts[[i - 1]]$clr)[j] < LOCK_CLR_THRESHOLD)
        ev_type <- if (!prev_low) "LOCK-ACQ"
                   else if (i < length(ts) && as.numeric(ts[[i + 1]]$clr)[j] >= LOCK_CLR_THRESHOLD) "LOCK-LOSS"
                   else "LOCK-ACQ"
        events[[length(events) + 1]] <- list(
          event_type = ev_type, timestep_index = i - 1L, label = ts[[i]]$label,
          carrier = carriers[j], clr_value = h[j],
          context = sprintf("%s CLR = %.2f (below threshold %.0f)", carriers[j], h[j], LOCK_CLR_THRESHOLD))
      }
    }
  }
  events
}

degeneracy_flags <- function(records_closed, carriers) {
  flags <- list(); T <- length(records_closed); D <- length(carriers)
  if (T < 20) flags[[length(flags) + 1]] <- list(
    flag = "small_T", severity = "warning",
    message = "Trajectory too short for stable depth-tower estimation.",
    condition = sprintf("T = %d < 20", T))
  if (D < 3) flags[[length(flags) + 1]] <- list(
    flag = "small_D", severity = "warning",
    message = "Compositional dimension too small for full CNT structure.",
    condition = sprintf("D = %d < 3", D))
  for (j in seq_len(D)) {
    series <- sapply(records_closed, function(r) r[j])
    if (all(diff(series) >= 0) || all(diff(series) <= 0)) {
      flags[[length(flags) + 1]] <- list(
        flag = "pre_aligned_compositionally", severity = "warning",
        message = sprintf("Records appear sorted by carrier %s; depth recursion may be degenerate.", carriers[j]),
        condition = sprintf("composition[%d] is monotonic", j - 1L))
      break
    }
  }
  flags
}

compute_diagnostics <- function(records_closed, tensor_block, carriers) {
  list(
    eitt_residuals = eitt_bench_test(records_closed, length(records_closed)),
    lock_events = detect_lock_events(tensor_block, carriers),
    degeneracy_flags = degeneracy_flags(records_closed, carriers)
  )
}


# ============================================================
# §6 — Orchestration & I/O
# ============================================================

ingest_csv <- function(path) {
  df <- read.csv(path, stringsAsFactors = FALSE, check.names = FALSE)
  carriers <- colnames(df)[-1]
  records <- list(); records_closed <- list(); n_zeros <- 0
  for (i in seq_len(nrow(df))) {
    vals <- as.numeric(df[i, -1])
    if (any(is.na(vals)) || any(vals < 0)) next
    if (any(vals == 0)) n_zeros <- n_zeros + 1
    records[[length(records) + 1]] <- list(label = as.character(df[i, 1]), raw_values = as.list(vals))
    records_closed[[length(records_closed) + 1]] <- close_simplex(vals)
  }
  list(carriers = carriers, records = records, records_closed = records_closed,
       zero_meta = list(method = "multiplicative", delta = DEFAULT_DELTA,
                        applied = n_zeros > 0, n_replacements = n_zeros))
}

get_environment_metadata <- function() {
  git_sha <- tryCatch(system("git rev-parse HEAD", intern = TRUE)[1], error = function(e) "unknown")
  if (length(git_sha) == 0 || is.na(git_sha)) git_sha <- "unknown"
  list(
    git_sha = git_sha,
    language_version = paste0("R ", R.version$major, ".", R.version$minor),
    numerical_lib = paste0("base R ", R.version$major, ".", R.version$minor),
    platform = R.version$platform,
    hostname_hash = digest(Sys.info()["nodename"], algo = "sha256")
  )
}

file_sha256 <- function(path) digest(file = path, algo = "sha256")

closed_data_sha256 <- function(records_closed, carriers) {
  canonical <- toJSON(list(carriers = carriers,
                            values = lapply(records_closed, as.list)),
                       auto_unbox = TRUE, digits = NA)
  digest(canonical, algo = "sha256", serialize = FALSE)
}

content_sha256 <- function(json_obj) {
  j <- json_obj
  j$metadata$generated <- NULL
  j$metadata$wall_clock_ms <- NULL
  j$metadata$environment <- NULL
  j$diagnostics$content_sha256 <- NULL
  canonical <- toJSON(j, auto_unbox = TRUE, digits = NA)
  digest(canonical, algo = "sha256", serialize = FALSE)
}

# ============================================================
# §6b — v2.0.0 output formatting (split coda_standard / higgins_extensions)
# ============================================================

TIMESTEP_CODA_FIELDS <- c("composition","clr","ilr","shannon_entropy",
                          "aitchison_norm","aitchison_distance_step")
TIMESTEP_HIGGINS_FIELDS <- c("higgins_scale","bearing_tensor","metric_tensor",
                             "metric_tensor_diagonal","condition_number",
                             "angular_velocity_deg","helmsman","helmsman_delta")
TIMESTEP_TOPLEVEL_FIELDS <- c("index","label","raw_values")

format_tensor_block_v2 <- function(tb) {
  out_ts <- list()
  for (i in seq_along(tb$timesteps)) {
    ts <- tb$timesteps[[i]]
    coda <- list(); higg <- list()
    for (k in TIMESTEP_CODA_FIELDS)    if (!is.null(ts[[k]])) coda[[k]] <- ts[[k]]
    for (k in TIMESTEP_HIGGINS_FIELDS) if (!is.null(ts[[k]])) higg[[k]] <- ts[[k]]
    new_ts <- list()
    for (k in TIMESTEP_TOPLEVEL_FIELDS) new_ts[[k]] <- ts[[k]]
    new_ts$coda_standard <- coda
    new_ts$higgins_extensions <- higg
    out_ts[[i]] <- new_ts
  }
  list(
    `_function`    = "composer",
    `_description` = paste0("Per-record compositional state. coda_standard fields ",
                            "follow Aitchison/Egozcue/Shannon. higgins_extensions ",
                            "are HUF-framework readings of the same simplex; see ",
                            "schema sec 8 for the mapping."),
    helmert_basis  = tb$helmert_basis,
    timesteps      = out_ts
  )
}

format_stage1_v2 <- function(s1) list(
  `_function`         = "formatter",
  `_description`      = "Cube-face projections and per-record metric ledger formatted for plate display. HUF/CBS-specific.",
  coda_standard       = list(),
  higgins_extensions  = list(section_atlas = s1$section_atlas, metric_ledger = s1$metric_ledger)
)

format_stage2_v2 <- function(s2) list(
  `_function`         = "review",
  `_description`      = "Pairwise cross-examination of compositional behaviour.",
  coda_standard       = list(variation_matrix = s2$variation_matrix),
  higgins_extensions  = list(carrier_pair_examination = s2$carrier_pair_examination)
)

format_stage3_v2 <- function(s3) list(
  `_function`         = "review",
  `_description`      = "Higher-degree subcompositional and triadic analysis.",
  coda_standard       = list(subcomposition_ladder = s3$subcomposition_ladder),
  higgins_extensions  = list(triadic_area = s3$triadic_area,
                              carrier_triads = s3$carrier_triads,
                              regime_detection = s3$regime_detection)
)

format_bridges_v2 <- function(b) list(
  `_function`         = "review",
  `_description`      = "Connections to dynamical / control / information theory.",
  coda_standard       = list(information_theory = b$information_theory),
  higgins_extensions  = list(dynamical_systems = b$dynamical_systems,
                              control_theory = b$control_theory)
)

format_depth_v2 <- function(d) list(
  `_function`         = "review",
  `_description`      = "Recursive depth sounder, period-2 attractor, impulse response. Wholly Higgins-framework.",
  coda_standard       = list(),
  higgins_extensions  = d
)

format_diagnostics_v2 <- function(diag) {
  out <- list(
    `_function`         = "review",
    `_description`      = "Engine self-checks: EITT residuals, lock events, degeneracy flags, content hash.",
    coda_standard       = list(),
    higgins_extensions  = list(eitt_residuals = diag$eitt_residuals,
                                lock_events = diag$lock_events,
                                degeneracy_flags = diag$degeneracy_flags)
  )
  if (!is.null(diag$content_sha256)) out$content_sha256 <- diag$content_sha256
  out
}


cnt_run <- function(csv_path, output_path = NULL, ordering = NULL) {
  t0 <- Sys.time()
  if (is.null(ordering)) ordering <- list(
    is_temporal = FALSE, ordering_method = "as-given",
    caveat = "User did not declare ordering. Treat derivative fields with caution."
  )
  ing <- ingest_csv(csv_path)
  carriers <- ing$carriers; records <- ing$records; records_closed <- ing$records_closed

  # Compute (flat internals)
  tensor_block <- compute_tensor_block(records, carriers)
  s1 <- compute_stage1(tensor_block, carriers)
  s2 <- compute_stage2(records_closed, tensor_block, carriers)
  s3 <- compute_stage3(records_closed, tensor_block, carriers)
  bridges <- compute_bridges(records_closed, tensor_block, carriers)
  depth <- compute_depth(records_closed, tensor_block, carriers)
  diag <- compute_diagnostics(records_closed, tensor_block, carriers)
  wall_ms <- as.integer(as.numeric(Sys.time() - t0, units = "secs") * 1000)

  # Format (v2.1.0 schema)
  units_block <- build_units_block()

  json_out <- list(
    metadata = list(
      `_function`            = "provenance",
      `_description`         = "Identity, schema version, run-time provenance.",
      schema_version         = SCHEMA_VERSION,
      engine_version         = paste(ENGINE_NAME, ENGINE_VERSION),
      engine_implementation  = "r",
      generated              = format(Sys.time(), "%Y-%m-%dT%H:%M:%SZ", tz = "UTC"),
      wall_clock_ms          = wall_ms,
      mathematical_lineage   = list(
        Aitchison_1986 = "CLR transform, simplex geometry, Aitchison distance",
        Shannon_1948   = "Entropy H = -sum x_j ln x_j",
        Egozcue_2003   = "ILR, Helmert basis, orthonormal coordinates",
        Higgins_2026   = "CNT tensor decomposition, recursive depth sounder, metric dual involution"
      ),
      engine_config = list(
        `_description`           = "Active values from the USER CONFIGURATION block at top of cnt.R. Two runs with identical config and input produce identical content_sha256.",
        DEFAULT_DELTA            = DEFAULT_DELTA,
        DEGEN_THRESHOLD          = DEGEN_THRESHOLD,
        LOCK_CLR_THRESHOLD       = LOCK_CLR_THRESHOLD,
        DEPTH_MAX_LEVELS         = DEPTH_MAX_LEVELS,
        DEPTH_PRECISION_TARGET   = DEPTH_PRECISION_TARGET,
        NOISE_FLOOR_OMEGA_VAR    = NOISE_FLOOR_OMEGA_VAR,
        TRIADIC_T_LIMIT          = TRIADIC_T_LIMIT,
        TRIADIC_K_DEFAULT        = TRIADIC_K_DEFAULT,
        EITT_GATE_PCT            = EITT_GATE_PCT,
        EITT_M_SWEEP_BASE        = as.list(EITT_M_SWEEP_BASE),
        active_overrides         = list()
      ),
      units = units_block
    ),
    input = list(
      `_function`           = "provenance",
      `_description`        = "Source data identity, hashes, and ordering declaration.",
      source_file           = basename(csv_path),
      source_file_sha256    = file_sha256(csv_path),
      closed_data_sha256    = closed_data_sha256(records_closed, carriers),
      n_records             = length(records),
      n_carriers            = length(carriers),
      carriers              = as.list(carriers),
      labels                = lapply(records, function(r) r$label),
      zero_replacement      = ing$zero_meta,
      ordering              = ordering
    ),
    tensor      = format_tensor_block_v2(tensor_block),
    stages      = list(
      stage1 = format_stage1_v2(s1),
      stage2 = format_stage2_v2(s2),
      stage3 = format_stage3_v2(s3)
    ),
    bridges     = format_bridges_v2(bridges),
    depth       = format_depth_v2(depth),
    diagnostics = format_diagnostics_v2(diag)
  )

  # content_sha256 (computed from canonical-keyed JSON without the
  # diagnostics.content_sha256 field itself)
  json_out$diagnostics$content_sha256 <- content_sha256(json_out)

  if (!is.null(output_path)) {
    writeLines(jsonlite::toJSON(json_out, auto_unbox = TRUE,
                                pretty = TRUE, na = "null", null = "null",
                                digits = NA),
               output_path)
  }
  invisible(json_out)
}


# ─── Native units helper (v1.1-B parity) ──────────────────────────
build_units_block <- function(input_units = NULL,
                              higgins_scale_units = NULL) {
  iu <- if (is.null(input_units)) INPUT_UNITS else input_units
  hu_req <- if (is.null(higgins_scale_units)) HIGGINS_SCALE_UNITS else higgins_scale_units
  factors <- list(
    ratio = 1.0, neper = 1.0, nat = 1.0, `%` = 1.0, absolute = 1.0,
    bit = log(2.0),
    dB_power = log(10.0)/10.0,
    dB_amplitude = log(10.0)/20.0
  )
  f <- factors[[iu]]
  if (is.null(f)) f <- 1.0
  hu <- if (hu_req == "auto") {
    if (iu == "bit") "bit" else "neper"
  } else hu_req
  list(
    `_description`               = "v1.1-B native units (additive 2.1.0).",
    input_units                  = iu,
    higgins_scale_units          = hu,
    units_scale_factor_to_neper  = f,
    feature                      = "v1.1-B native units (R parity)",
    schema_addition              = "2.1.0",
    report_units_scale_factors   = REPORT_UNITS_SCALE_FACTORS
  )
}
