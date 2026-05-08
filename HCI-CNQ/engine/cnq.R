#!/usr/bin/env Rscript
# CNQ Engine — R Reference Implementation
# ========================================
#
# Schema version : cnq/1.0.0       (see CNQ_SCHEMA.md for the contract)
# Engine version : 1.0.0
# Algorithm ref  : CNQ_PSEUDOCODE.md
#
# This R implementation is a faithful translation of cnq.py. It reads a
# CNT JSON (or runs CNT via the adapter on a raw CSV) and emits ONE
# canonical CNQ JSON conforming to the cnq/1.0.0 schema.
#
# Cross-language parity contract:
#   The canonical_sha256 of the same payload computed in Python and in R
#   must be IDENTICAL. The numerical max_residual must agree to <= 1 ULP.
#   Two runs on the same CNT JSON (within a single language) produce
#   bit-identical cnq_content_sha256.
#
# Mathematical lineage:
#   Aitchison (1986)  — CLR transform, simplex geometry
#   Egozcue (2003)    — ILR, Helmert basis, orthonormal coordinates
#   Hamilton (1843)   — Quaternion algebra
#   Higgins (2026)    — CNQ engine: quaternion-native view of CNT trajectories
#
# Dependencies (install once):
#   install.packages(c("jsonlite", "digest"))
#
# Usage (CLI):
#   Rscript cnq.R --cnt-json PATH --input-csv PATH --out PATH \
#                 [--repo-root PATH] [--cnt-engine PATH]
#
# Usage (interactive):
#   source("cnq.R")
#   payload <- cnq_run(
#       cnt_json_path = "planck_cmb_boson_cnt.json",
#       input_csv_path = "planck_cmb_boson_input.csv",
#       out_path = "cnq_run.json"
#   )
#
# The instrument reads. The expert decides. The hashes carry the receipts.
# Public use: yes. License: per repository LICENSE file.

suppressPackageStartupMessages({
  library(jsonlite)
  library(digest)
})

# ============================================================
# CONSTANTS (do not edit unless modifying the engine)
# ============================================================

CNQ_ENGINE_VERSION <- "1.0.0"
CNQ_SCHEMA_VERSION <- "cnq/1.0.0"
GATE_THRESHOLD <- 1e-12

# Fields excluded from the canonical-hash payload (clock-dependent).
EXCLUDED_FIELDS <- c("generated", "timestamp", "wall_clock", "_run_clock")

# ============================================================
# SECTION 1 — Geometry primitives
# ============================================================

# Aitchison closure: rescale a row to sum to 1.
closure <- function(x) {
  x <- as.numeric(x)
  x / sum(x)
}

# Centred log-ratio of a closed (or unclosed but positive) row.
# clr(x)_i = log(x_i) - mean_j(log(x_j))
clr <- function(x) {
  x <- as.numeric(x)
  g <- exp(mean(log(x)))
  log(x / g)
}

# Helmert orthonormal contrast matrix, (D-1) x D.
# Row k (1-indexed in R, 0-indexed in pseudocode):
#   norm = 1/sqrt(n*(n+1)) where n = k_zero_indexed + 1
#   first n entries: +norm
#   entry at index n: -n*norm
#   remaining entries: 0
# This convention matches QD_round_2.py exactly.
helmert_basis <- function(D) {
  H <- matrix(0, nrow = D - 1, ncol = D)
  for (k in seq_len(D - 1)) {
    n <- k                                  # 1-indexed n matches pseudocode k_zero+1
    norm <- 1 / sqrt(n * (n + 1))
    H[k, 1:n] <- norm
    H[k, n + 1] <- -n * norm
  }
  H
}

# ============================================================
# SECTION 2 — Quaternion algebra
# ============================================================

# Quaternions are stored as length-4 numeric vectors: c(w, x, y, z).

quat_from_axis_angle <- function(axis, angle) {
  axis <- as.numeric(axis)
  n <- sqrt(sum(axis^2))
  if (n < 1e-15) return(c(1, 0, 0, 0))
  axis <- axis / n
  half <- angle / 2
  c(cos(half),
    sin(half) * axis[1],
    sin(half) * axis[2],
    sin(half) * axis[3])
}

quat_conj <- function(q) c(q[1], -q[2], -q[3], -q[4])

quat_mul <- function(p, q) {
  c(
    p[1]*q[1] - p[2]*q[2] - p[3]*q[3] - p[4]*q[4],
    p[1]*q[2] + p[2]*q[1] + p[3]*q[4] - p[4]*q[3],
    p[1]*q[3] - p[2]*q[4] + p[3]*q[1] + p[4]*q[2],
    p[1]*q[4] + p[2]*q[3] - p[3]*q[2] + p[4]*q[1]
  )
}

# Sandwich rotation: returns the xyz part of (q . [0;v] . q*).
quat_rotate <- function(q, v) {
  p <- c(0, v[1], v[2], v[3])
  rotated <- quat_mul(quat_mul(q, p), quat_conj(q))
  rotated[2:4]
}

# atan2-stable rotation quaternion that takes unit-3-vec u1 -> unit-3-vec u2.
# Matches cnq.py's rotation_quaternion_between exactly.
rotation_quaternion_between <- function(u1, u2, eps = 1e-15) {
  u1 <- u1 / sqrt(sum(u1^2))
  u2 <- u2 / sqrt(sum(u2^2))
  d <- max(-1, min(1, sum(u1 * u2)))         # clipped dot product

  if (d > 1 - eps) return(c(1, 0, 0, 0))     # already aligned

  if (d < -1 + eps) {
    # antiparallel: pick any axis perpendicular to u1
    axis <- c(u1[2]*0 - u1[3]*0, u1[3]*1 - u1[1]*0, u1[1]*0 - u1[2]*1)
    axis <- c(0, u1[3], -u1[2])              # cross(u1, (1,0,0))
    if (sqrt(sum(axis^2)) < 1e-10) {
      axis <- c(-u1[3], 0, u1[1])            # cross(u1, (0,1,0))
    }
    axis <- axis / sqrt(sum(axis^2))
    return(quat_from_axis_angle(axis, pi))
  }

  cross <- c(u1[2]*u2[3] - u1[3]*u2[2],
             u1[3]*u2[1] - u1[1]*u2[3],
             u1[1]*u2[2] - u1[2]*u2[1])
  angle <- atan2(sqrt(sum(cross^2)), d)
  quat_from_axis_angle(cross, angle)
}

# ============================================================
# SECTION 3 — Dimension policy
# ============================================================

classify_dimension <- function(D) {
  if (D == 4) return(list(
    D = 4L,
    label = "native_quaternion",
    algebra = "SU(2) double cover of SO(3); Aitchison rotation in R^3",
    processing = "Helmert -> R^3 -> unit-quaternion sandwich",
    claim_strength = "confirmed (load-bearing case for the framework)"
  ))
  if (D == 3) return(list(
    D = 3L,
    label = "boundary_or_degenerate_support",
    algebra = "SO(2)-equivalent in R^2; promoted to R^3 by zero-padding",
    processing = "Helmert -> R^2 -> embed in R^3 with z=0 -> sandwich",
    claim_strength = "consistency support, not native D=4 quaternion proof"
  ))
  if (D == 2) return(list(
    D = 2L,
    label = "degenerate_below_quaternion",
    algebra = "scalar log-ratio only; no rotation degree of freedom",
    processing = "bearing computation only",
    claim_strength = "boundary diagnostic; quaternion view does not apply"
  ))
  if (D == 8) return(list(
    D = 8L,
    label = "bi_quaternion_factoring_candidate",
    algebra = "SO(8) sup SU(2) x SU(2); two coupled quaternion paths",
    processing = paste(
      "Helmert -> R^7; reduced view = first 3 axes;",
      "twin-quaternion factoring scaffolded but DEFERRED (INV-029)"
    ),
    claim_strength = "experimental; full algebra extension pending pilot"
  ))
  if (D >= 5) return(list(
    D = as.integer(D),
    label = "reduced_or_projected",
    algebra = sprintf("SO(%d); projection to first 3 ILR axes for the CNQ view", D - 1),
    processing = sprintf("Helmert -> R^%d -> first 3 axes -> sandwich (lossy)", D - 1),
    claim_strength = "projection diagnostic only; full Cl(D-1) extension is DEFERRED"
  ))
  list(D = as.integer(D),
       label = "unsupported",
       algebra = "n/a",
       processing = "n/a",
       claim_strength = "out of scope")
}

# ============================================================
# SECTION 4 — Input handling
# ============================================================

# Read a CCTT-style CSV: first column label, remaining columns positive carriers.
read_csv_compositions <- function(input_csv) {
  df <- read.csv(input_csv, stringsAsFactors = FALSE, check.names = FALSE)
  carrier_names <- colnames(df)[-1]
  rows <- as.matrix(df[, -1, drop = FALSE])
  storage.mode(rows) <- "double"
  list(
    label_col = colnames(df)[1],
    carrier_names = carrier_names,
    labels = df[[1]],
    rows = rows
  )
}

# CNT 2.1.x stores input rows under input.rows or input.compositions
# depending on schema version.
reconstruct_compositions_from_cnt <- function(cnt_json) {
  inp <- cnt_json[["input"]]
  if (is.null(inp)) return(list(carriers = NULL, rows = NULL))
  rows <- inp[["rows"]]
  if (is.null(rows)) rows <- inp[["compositions"]]
  carriers <- inp[["carrier_names"]]
  if (is.null(carriers)) carriers <- inp[["carriers"]]
  if (is.null(rows) || is.null(carriers)) {
    return(list(carriers = NULL, rows = NULL))
  }
  list(carriers = unlist(carriers),
       rows = do.call(rbind, lapply(rows, function(r) as.numeric(unlist(r)))))
}

# Best-effort extraction of CNT diagnostics (parent_cnt_content_sha256, etc.)
extract_cnt_diagnostics <- function(cnt_json) {
  diag <- cnt_json[["diagnostics"]]
  metadata <- cnt_json[["metadata"]]
  inp <- cnt_json[["input"]]
  list(
    D = inp$n_carriers %||% inp$D %||% cnt_json$D,
    T_records = inp$n_records %||% inp$T %||% cnt_json$T,
    content_sha256 = diag$content_sha256 %||% cnt_json$content_sha256,
    source_file_sha256 = inp$source_file_sha256 %||% cnt_json$source_file_sha256,
    cnt_engine_version = metadata$engine_version %||% metadata$version,
    cnt_schema_version = metadata$schema %||% metadata$schema_version,
    cnt_termination = diag$curvature_termination %||% diag$termination,
    ir_class = diag$ir_class %||% NULL,
    amplitude_A = diag$amplitude_A %||% diag$A,
    damping_zeta = diag$damping_zeta %||% diag$zeta,
    helmsman_sigma = if (!is.null(diag$helmsman))
                       diag$helmsman$sigma %||% diag$helmsman$sigma_HS
                     else NULL
  )
}

# Null-coalesce operator — used like Python's `a or b`.
`%||%` <- function(a, b) if (is.null(a)) b else a

# ============================================================
# SECTION 5 — CNQ view computation
# ============================================================

run_cnq_view <- function(rows, carrier_names, dimension_policy) {
  T <- nrow(rows)
  D <- ncol(rows)
  if (D != dimension_policy$D) {
    stop(sprintf("Row dimension %d != declared policy D=%d", D, dimension_policy$D))
  }

  # 5a. closure -> CLR -> Helmert
  closed <- t(apply(rows, 1, closure))
  clr_vecs <- t(apply(closed, 1, clr))
  H <- helmert_basis(D)
  ilr <- clr_vecs %*% t(H)                         # (T, D-1)
  radii_full <- sqrt(rowSums(ilr^2))

  # 5b. project to R^3 according to dimension policy
  if (D == 4) {
    ilr3 <- ilr
    capture_note <- "exact (D=4 native; no projection loss)"
  } else if (D == 3) {
    ilr3 <- cbind(ilr, rep(0, T))
    capture_note <- "D=3 boundary; embedded in R^3 with z=0"
  } else if (D == 2) {
    return(list(
      dimension_policy = dimension_policy,
      quaternion_path = NULL,
      bearing_only = list(
        ilr = as.vector(ilr),
        note = "D=2 has no rotation degree of freedom; bearing only."
      )
    ))
  } else {
    ilr3 <- ilr[, 1:3, drop = FALSE]
    capture_note <- sprintf("D=%d; first 3 ILR axes used as reduced view. Full ILR has %d axes.",
                            D, D - 1)
  }

  # 5c. captured energy fraction
  if (D %in% c(2, 3, 4)) {
    captured_step_fraction <- 1.0
  } else {
    full_steps <- diff(ilr)
    red_steps <- diff(ilr3)
    full_norm2 <- rowSums(full_steps^2)
    red_norm2 <- rowSums(red_steps^2)
    ratio <- ifelse(full_norm2 > 1e-30, red_norm2 / full_norm2, 1.0)
    captured_step_fraction <- mean(ratio)
  }

  # 5d. normalize to S^2
  radii3 <- sqrt(rowSums(ilr3^2))
  safe_radii <- ifelse(radii3 > 1e-15, radii3, 1.0)
  units <- ilr3 / safe_radii
  zero_mask <- radii3 <= 1e-15
  if (any(zero_mask)) units[zero_mask, ] <- 0

  # 5e. per-step quaternion sandwich reconstruction
  n_pairs <- T - 1L
  if (n_pairs <= 0) {
    residuals <- numeric(0); quats <- matrix(0, 0, 4); angles <- numeric(0)
  } else {
    residuals <- numeric(n_pairs)
    quats <- matrix(0, n_pairs, 4)
    angles <- numeric(n_pairs)
    for (t in seq_len(n_pairs)) {
      q <- rotation_quaternion_between(units[t, ], units[t + 1, ])
      u_rec <- quat_rotate(q, units[t, ])
      residuals[t] <- max(abs(u_rec - units[t + 1, ]))
      quats[t, ] <- q
      angles[t] <- 2 * atan2(sqrt(sum(q[2:4]^2)), q[1])
    }
  }

  if (n_pairs > 0) {
    max_residual <- max(residuals)
    mean_residual <- mean(residuals)
    gate_pass <- max_residual <= GATE_THRESHOLD
  } else {
    max_residual <- NaN; mean_residual <- NaN; gate_pass <- FALSE
  }

  # 5f. per-step ledger
  per_step <- vector("list", n_pairs)
  for (t in seq_len(n_pairs)) {
    per_step[[t]] <- list(
      t = t - 1L,
      u_start = as.numeric(units[t, ]),
      u_end = as.numeric(units[t + 1, ]),
      q_w = as.numeric(quats[t, 1]),
      q_x = as.numeric(quats[t, 2]),
      q_y = as.numeric(quats[t, 3]),
      q_z = as.numeric(quats[t, 4]),
      angle_rad = as.numeric(angles[t]),
      residual_linf = as.numeric(residuals[t])
    )
  }

  list(
    dimension_policy = dimension_policy,
    n_records_T = T,
    n_carriers_D = D,
    carrier_names = as.list(carrier_names),
    frame_type = "Helmert orthonormal contrast (legacy QD convention)",
    frame_signature = "row k: 1/sqrt(k(k+1)) [k blocks of +1, then -k]",
    projection_to_R3 = list(
      method = if (D == 4) "exact"
               else if (D == 3) "zero-padded R^2 -> R^3"
               else if (D >= 5) "first 3 ILR axes"
               else "n/a",
      note = capture_note
    ),
    captured_step_fraction = captured_step_fraction,
    quaternion_path = list(
      n_pairs_tested = n_pairs,
      max_residual = max_residual,
      mean_residual = mean_residual,
      gate_threshold = GATE_THRESHOLD,
      gate_pass = gate_pass,
      per_step = per_step
    ),
    radii = list(
      min = if (T > 0) min(radii3) else 0.0,
      max = if (T > 0) max(radii3) else 0.0,
      mean = if (T > 0) mean(radii3) else 0.0
    )
  )
}

# ============================================================
# SECTION 6 — Canonical hashing (determinism contract)
# ============================================================

# Recursively strip clock-dependent fields. Pure function.
strip_volatile <- function(obj) {
  if (is.list(obj) && !is.null(names(obj)) && length(obj) > 0) {
    keep <- !(names(obj) %in% EXCLUDED_FIELDS)
    obj <- obj[keep]
    for (k in names(obj)) obj[[k]] <- strip_volatile(obj[[k]])
    return(obj)
  }
  if (is.list(obj)) {
    return(lapply(obj, strip_volatile))
  }
  obj
}

# Canonical JSON string: sorted keys, no whitespace, ASCII-safe.
canonical_dumps <- function(obj) {
  stripped <- strip_volatile(obj)
  toJSON(stripped,
         auto_unbox = TRUE,
         null = "null",
         na = "null",
         pretty = FALSE,
         digits = 17)        # full float64 precision
}

canonical_sha256 <- function(obj) {
  payload <- canonical_dumps(obj)
  digest(payload, algo = "sha256", serialize = FALSE)
}

# SHA-256 of a file's bytes.
file_sha256 <- function(path) {
  digest(file = path, algo = "sha256")
}

# ============================================================
# SECTION 7 — Output assembly
# ============================================================

assemble_cnq_output <- function(cnt_json, cnt_diag, cnq_view,
                                cnt_json_path = NULL,
                                input_csv_path = NULL) {
  parent_hash <- cnt_diag$content_sha256
  source_hash <- cnt_diag$source_file_sha256
  if (!is.null(input_csv_path) && is.null(source_hash)) {
    source_hash <- file_sha256(input_csv_path)
  }

  payload <- list(
    metadata = list(
      schema = CNQ_SCHEMA_VERSION,
      engine = "HCI-CNQ",
      engine_version = CNQ_ENGINE_VERSION,
      generated = format(Sys.time(), "%Y-%m-%dT%H:%M:%SZ", tz = "UTC"),
      principle = "CNT measures invariance. CNQ names the algebra it lives in.",
      reference_implementation = "R port (cnq.R); parity contract with cnq.py"
    ),
    provenance = list(
      parent_engine = "HCI-CNT",
      parent_engine_version = cnt_diag$cnt_engine_version,
      parent_schema = cnt_diag$cnt_schema_version,
      parent_cnt_content_sha256 = parent_hash,
      source_file_sha256 = source_hash,
      cnt_json_path = if (!is.null(cnt_json_path)) as.character(cnt_json_path) else NULL,
      input_csv_path = if (!is.null(input_csv_path)) as.character(input_csv_path) else NULL
    ),
    cnt_diagnostics_carried_forward = list(
      cnt_termination = cnt_diag$cnt_termination,
      ir_class = cnt_diag$ir_class,
      amplitude_A = cnt_diag$amplitude_A,
      damping_zeta = cnt_diag$damping_zeta,
      helmsman_sigma = cnt_diag$helmsman_sigma
    ),
    cnq_view = cnq_view
  )

  cnq_hash <- canonical_sha256(payload)
  payload$cnq_content_sha256 <- cnq_hash
  payload
}

# ============================================================
# SECTION 8 — CNT adapter (portable engine resolution)
# ============================================================

find_repo_root <- function(start = NULL, explicit = NULL) {
  if (!is.null(explicit)) {
    p <- normalizePath(explicit, mustWork = FALSE)
    if (!file.exists(p)) stop("--repo-root not found: ", p)
    return(p)
  }
  env_root <- Sys.getenv("REPO_ROOT", unset = "")
  if (nzchar(env_root) && file.exists(env_root)) return(normalizePath(env_root))

  if (is.null(start)) start <- normalizePath(getwd())
  current <- if (file.info(start)$isdir) start else dirname(start)
  markers <- c(".git", "HCI-CNQ", "HCI-CNT", "ai-refresh")
  while (TRUE) {
    for (m in markers) {
      if (file.exists(file.path(current, m))) return(current)
    }
    if (file.exists(file.path(current, "Hs", "HCI-CNT"))) {
      return(file.path(current, "Hs"))
    }
    parent <- dirname(current)
    if (parent == current) break
    current <- parent
  }
  stop("Could not locate Hs repository root. Pass --repo-root /path/to/higgins-decomposition.")
}

find_cnt_engine <- function(repo_root, explicit = NULL) {
  if (!is.null(explicit)) {
    p <- normalizePath(explicit, mustWork = FALSE)
    if (!file.exists(p)) stop("--cnt-engine not found: ", p)
    return(p)
  }
  candidates <- c(
    file.path(repo_root, "HCI-CNT", "engine", "cnt.py"),
    file.path(repo_root, "Hs", "HCI-CNT", "engine", "cnt.py")
  )
  for (c in candidates) if (file.exists(c)) return(c)
  stop("cnt.py not found under ", repo_root)
}

run_cnt <- function(input_csv, output_json, cnt_engine, extra_args = NULL) {
  cmd_args <- c(cnt_engine, "--input", input_csv, "--output", output_json, extra_args)
  res <- system2("python3", args = cmd_args, stdout = TRUE, stderr = TRUE)
  if (!file.exists(output_json)) {
    stop("CNT engine did not produce ", output_json, "; stdout/stderr:\n",
         paste(res, collapse = "\n"))
  }
  output_json
}

# ============================================================
# SECTION 9 — Top-level entry point
# ============================================================

cnq_run <- function(cnt_json_path = NULL,
                    input_csv_path = NULL,
                    out_path,
                    repo_root = NULL,
                    cnt_engine = NULL,
                    cnt_extra_args = NULL) {
  if (is.null(cnt_json_path) && is.null(input_csv_path)) {
    stop("Provide either cnt_json_path or input_csv_path.")
  }

  # Step A: ensure CNT JSON
  if (is.null(cnt_json_path)) {
    repo_root_resolved <- find_repo_root(explicit = repo_root)
    engine_path <- find_cnt_engine(repo_root_resolved, explicit = cnt_engine)
    cnt_json_path <- sub("\\.json$", ".cnt.json", out_path, fixed = FALSE)
    run_cnt(input_csv_path, cnt_json_path, engine_path, extra_args = cnt_extra_args)
  }

  cnt_json <- fromJSON(cnt_json_path, simplifyVector = FALSE)
  cnt_diag <- extract_cnt_diagnostics(cnt_json)

  # Step B: get rows
  reconstructed <- reconstruct_compositions_from_cnt(cnt_json)
  carriers <- reconstructed$carriers
  rows <- reconstructed$rows
  if (is.null(rows)) {
    if (is.null(input_csv_path)) {
      stop("CNT JSON does not contain input rows; pass input_csv_path")
    }
    csv <- read_csv_compositions(input_csv_path)
    carriers <- csv$carrier_names
    rows <- csv$rows
  }

  # Step C: CNQ view
  D <- ncol(rows)
  policy <- classify_dimension(D)
  cnq_view <- run_cnq_view(rows, carriers, policy)

  # Step D: assemble + write
  payload <- assemble_cnq_output(cnt_json, cnt_diag, cnq_view,
                                 cnt_json_path = cnt_json_path,
                                 input_csv_path = input_csv_path)

  dir.create(dirname(out_path), showWarnings = FALSE, recursive = TRUE)
  writeLines(toJSON(payload, auto_unbox = TRUE, pretty = TRUE, digits = 17),
             con = out_path)

  payload
}

# ============================================================
# SECTION 10 — CLI
# ============================================================

parse_cli <- function(argv) {
  args <- list(cnt_json = NULL, input_csv = NULL, out = NULL,
               repo_root = NULL, cnt_engine = NULL, cnt_extra = c())
  i <- 1
  while (i <= length(argv)) {
    a <- argv[i]
    if (a == "--cnt-json")        { args$cnt_json   <- argv[i+1]; i <- i + 2 }
    else if (a == "--input-csv")  { args$input_csv  <- argv[i+1]; i <- i + 2 }
    else if (a == "--out")        { args$out        <- argv[i+1]; i <- i + 2 }
    else if (a == "--repo-root")  { args$repo_root  <- argv[i+1]; i <- i + 2 }
    else if (a == "--cnt-engine") { args$cnt_engine <- argv[i+1]; i <- i + 2 }
    else if (a == "--cnt-extra-arg") { args$cnt_extra <- c(args$cnt_extra, argv[i+1]); i <- i + 2 }
    else if (a == "-h" || a == "--help") {
      cat("Usage: Rscript cnq.R --cnt-json PATH [--input-csv PATH] --out PATH",
          "                     [--repo-root PATH] [--cnt-engine PATH]\n", sep = "\n")
      quit(status = 0)
    }
    else { stop("Unknown argument: ", a) }
  }
  if (is.null(args$out)) stop("--out is required")
  if (is.null(args$cnt_json) && is.null(args$input_csv)) {
    stop("Provide --cnt-json or --input-csv")
  }
  args
}

main <- function() {
  argv <- commandArgs(trailingOnly = TRUE)
  args <- tryCatch(parse_cli(argv), error = function(e) {
    cat("cnq.R: ERROR:", conditionMessage(e), "\n", file = stderr())
    quit(status = 2)
  })

  payload <- tryCatch(
    cnq_run(
      cnt_json_path = args$cnt_json,
      input_csv_path = args$input_csv,
      out_path = args$out,
      repo_root = args$repo_root,
      cnt_engine = args$cnt_engine,
      cnt_extra_args = args$cnt_extra
    ),
    error = function(e) {
      cat("cnq.R: ERROR:", conditionMessage(e), "\n", file = stderr())
      quit(status = 2)
    }
  )

  cv <- payload$cnq_view
  qp <- if (!is.null(cv$quaternion_path)) cv$quaternion_path else list()
  cat(sprintf("CNQ: D=%d T=%d label=%s max_residual=%s gate_pass=%s cnq_content_sha256=%s\n",
              cv$n_carriers_D, cv$n_records_T,
              cv$dimension_policy$label,
              format(qp$max_residual %||% NA, digits = 17),
              if (!is.null(qp$gate_pass)) qp$gate_pass else "n/a",
              payload$cnq_content_sha256))
  invisible(payload)
}

# Run main only when invoked as script (not when sourced).
if (sys.nframe() == 0L && !interactive()) {
  main()
}
