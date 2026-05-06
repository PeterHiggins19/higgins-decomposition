#!/usr/bin/env Rscript
# HCI-Atlas Stage 2 — R port (metric computation; PDF rendering is Python-only)
#
# This R port computes the navigation and Order-2 metrics defined in
# atlas/STAGE2_PSEUDOCODE.md. PDF rendering of the locked 19-plate
# atlas remains a Python responsibility (atlas/stage2_locked.py); the R
# port exposes the metric algorithms so R-native users can reproduce
# the numbers and emit their own plots in base R or ggplot2.
#
# Conforms to OUTPUT_DOCTRINE v1.0.1.
#
# Usage:
#   source("atlas/stage2.R")
#   j <- jsonlite::read_json("path/to/cnt.json", simplifyVector = FALSE)
#   m <- stage2_metrics(j)
#   m$navigation                # System course plot metrics
#   m$d_mat                     # Pairwise distance matrix
#   m$Hs                        # Higgins scale trajectory
#   ...

if (!requireNamespace("jsonlite", quietly = TRUE)) {
  stop("Package 'jsonlite' required. install.packages('jsonlite')")
}


# --------------------------------------------------------------
# Internal helpers
# --------------------------------------------------------------
.unlist_num <- function(x) {
  # Convert a list-of-numerics to a numeric vector
  as.numeric(unlist(x))
}

.matrix_from_basis <- function(basis_list) {
  # tensor.helmert_basis.coefficients comes in as list-of-lists.
  # Convert to (D-1) × D matrix.
  do.call(rbind, lapply(basis_list, .unlist_num))
}


# --------------------------------------------------------------
# stage2_metrics — core computation, pseudocode §3
# --------------------------------------------------------------
stage2_metrics <- function(j) {
  inp <- j$input
  T   <- inp$n_records
  D   <- inp$n_carriers
  carriers <- vapply(inp$carriers, as.character, character(1))
  labels   <- vapply(inp$labels,   as.character, character(1))

  # CLR matrix (T × D)
  clr_mat <- matrix(0.0, nrow = T, ncol = D)
  closed_mat <- matrix(0.0, nrow = T, ncol = D)
  for (t in seq_len(T)) {
    cs <- j$tensor$timesteps[[t]]$coda_standard
    if (!is.null(cs)) {
      clr_mat[t, ]    <- .unlist_num(cs$clr)
      closed_mat[t, ] <- .unlist_num(cs$composition)
    }
  }

  # Helmert basis × CLR → ILR
  basis <- .matrix_from_basis(j$tensor$helmert_basis$coefficients)
  ilr_mat <- clr_mat %*% t(basis)

  # Per-step Aitchison distance
  d_step <- numeric(T)
  for (t in 2:T) {
    d_step[t] <- sqrt(sum((clr_mat[t, ] - clr_mat[t-1, ])^2))
  }

  # Pairwise distance matrix
  d_mat <- matrix(0.0, nrow = T, ncol = T)
  for (a in seq_len(T)) {
    for (b in seq_len(T)) {
      d_mat[a, b] <- sqrt(sum((clr_mat[a, ] - clr_mat[b, ])^2))
    }
  }

  # Aitchison norm per timestep
  norm_t <- vapply(seq_len(T),
                    function(t) sqrt(sum(clr_mat[t, ]^2)),
                    numeric(1))

  # Metric ledger
  ml <- j$stages$stage1$higgins_extensions$metric_ledger
  Hs       <- vapply(ml, function(m) as.numeric(m$hs),       numeric(1))
  omega    <- vapply(ml, function(m) as.numeric(m$omega_deg), numeric(1))
  ring     <- vapply(ml, function(m) as.character(m$ring),    character(1))
  helmsman <- vapply(ml, function(m) as.character(m$helmsman), character(1))
  cond     <- vapply(ml, function(m) as.numeric(m$condition), numeric(1))

  metric_trace <- vapply(j$tensor$timesteps,
                          function(ts) {
                            mt <- ts$higgins_extensions$metric_tensor
                            if (!is.null(mt) && !is.null(mt$trace))
                              as.numeric(mt$trace) else 0.0
                          }, numeric(1))

  # Bearings (T × n_pairs)
  pairs_idx <- combn(D, 2)
  n_pairs <- ncol(pairs_idx)
  bearings <- matrix(NA_real_, nrow = T, ncol = n_pairs)
  pair_names <- character(n_pairs)
  pair_lookup <- list()
  for (k in seq_len(n_pairs)) {
    i <- pairs_idx[1, k]; jj <- pairs_idx[2, k]
    pair_names[k] <- paste0(carriers[i], "-", carriers[jj])
    pair_lookup[[paste0(min(i, jj), "_", max(i, jj))]] <- k
  }
  for (t in seq_len(T)) {
    bp <- j$tensor$timesteps[[t]]$higgins_extensions$bearing_tensor$pairs
    if (!is.null(bp)) for (p in bp) {
      ci <- match(p$carrier_i, carriers)
      cj <- match(p$carrier_j, carriers)
      if (!is.na(ci) && !is.na(cj)) {
        key <- paste0(min(ci, cj), "_", max(ci, cj))
        k <- pair_lookup[[key]]
        if (!is.null(k)) bearings[t, k] <- as.numeric(p$theta_deg)
      }
    }
  }

  # Variation matrix
  var_mat <- do.call(rbind, lapply(j$stages$stage2$coda_standard$variation_matrix,
                                    .unlist_num))

  # Pair correlation
  cpe <- j$stages$stage2$higgins_extensions$carrier_pair_examination
  R <- diag(D)
  for (p in cpe) {
    i <- p$i + 1; jj <- p$j + 1   # R is 1-indexed
    R[i, jj] <- R[jj, i] <- as.numeric(p$pearson_r)
  }

  # ── Navigation metrics (pseudocode §3.4) ────────────────────
  h_start <- clr_mat[1, ]
  h_final <- clr_mat[T, ]
  V_net   <- h_final - h_start
  net_distance <- sqrt(sum(V_net^2))
  path_length  <- sum(d_step)
  course_directness <- if (path_length > 0) net_distance / path_length else 0.0
  navigation <- list(
    h_start          = h_start,
    h_final          = h_final,
    V_net            = V_net,
    net_distance     = net_distance,
    path_length      = path_length,
    course_directness= course_directness,
    dynamic_range_S  = max(h_start) - min(h_start),
    dynamic_range_F  = max(h_final) - min(h_final),
    label_S          = labels[1],
    label_F          = labels[T]
  )

  # ── PCA for system course plot (pseudocode §3.5) ────────────
  X <- scale(clr_mat, scale = FALSE)   # row-mean removed
  sv <- svd(X)
  PC1 <- (sv$u[, 1] * sv$d[1])
  PC2 <- (sv$u[, 2] * sv$d[2])
  var_pc <- sv$d^2 / sum(sv$d^2)
  course_pca <- list(
    PC1 = PC1, PC2 = PC2,
    var_explained_PC1 = var_pc[1],
    var_explained_PC2 = var_pc[2]
  )

  # ── Helmsman aggregates (pseudocode §3.7) ───────────────────
  helmsman_count <- table(helmsman)
  transition <- matrix(0L, nrow = D, ncol = D,
                       dimnames = list(carriers, carriers))
  for (k in seq_len(T - 1)) {
    a <- helmsman[k]; b <- helmsman[k + 1]
    if (a %in% carriers && b %in% carriers) {
      transition[a, b] <- transition[a, b] + 1L
    }
  }

  # ── Pairwise divergence top-15 (pseudocode §3.9) ────────────
  div <- list()
  for (a in seq_len(T)) {
    for (b in (a + 1):T) {
      if (b > T) next
      div[[length(div) + 1]] <- list(a = a, b = b, d = d_mat[a, b])
    }
  }
  div <- div[order(-vapply(div, function(x) x$d, numeric(1)))]
  top15 <- head(div, 15)

  list(
    T = T, D = D, carriers = carriers, labels = labels,
    closed_mat = closed_mat, clr_mat = clr_mat, ilr_mat = ilr_mat,
    d_step = d_step, d_mat = d_mat, norm = norm_t,
    Hs = Hs, ring = ring, omega = omega, helmsman = helmsman,
    cond = cond, metric_trace = metric_trace,
    bearings = bearings, pair_names = pair_names,
    var_mat = var_mat, R = R, cpe = cpe,
    locks = j$diagnostics$higgins_extensions$lock_events,
    navigation = navigation,
    course_pca = course_pca,
    helmsman_count = helmsman_count,
    transition = transition,
    pairwise_divergence_top15 = top15
  )
}


# --------------------------------------------------------------
# stage2_summary — print numeric summary (pseudocode §4 plate 19)
# --------------------------------------------------------------
stage2_summary <- function(m) {
  cat(sprintf("Stage 2 summary  T=%d  D=%d\n", m$T, m$D))
  cat(sprintf("  carriers: %s\n", paste(m$carriers, collapse = ", ")))
  cat("\n  Navigation (System Course Plot):\n")
  cat(sprintf("    net_distance      = %.4f HLR\n", m$navigation$net_distance))
  cat(sprintf("    path_length       = %.4f HLR\n", m$navigation$path_length))
  cat(sprintf("    course_directness = %.4f\n",     m$navigation$course_directness))
  cat(sprintf("\n  ω         : min=%.2f mean=%.2f max=%.2f deg\n",
              min(m$omega), mean(m$omega), max(m$omega)))
  cat(sprintf("  Hs        : min=%.4f mean=%.4f max=%.4f\n",
              min(m$Hs), mean(m$Hs), max(m$Hs)))
  cat(sprintf("  Aitch norm: min=%.4f mean=%.4f max=%.4f HLR\n",
              min(m$norm), mean(m$norm), max(m$norm)))
  cat(sprintf("  pairs     : %d  (|r|>0.7: %d)\n",
              length(m$cpe),
              sum(vapply(m$cpe, function(p) abs(as.numeric(p$pearson_r)) > 0.7,
                         logical(1)))))
  cat(sprintf("  lock events: %d\n", length(m$locks)))
  cat("\n  Helmsman top 5:\n")
  hc <- sort(m$helmsman_count, decreasing = TRUE)
  for (i in seq_len(min(5, length(hc)))) {
    cat(sprintf("    %-14s %4d\n", names(hc)[i], hc[i]))
  }
  invisible(NULL)
}


# --------------------------------------------------------------
# stage2_course_plot — emit a System Course Plot to a PDF (R native)
# Lightweight — for full 19-plate atlas, use atlas/stage2_locked.py
# --------------------------------------------------------------
stage2_course_plot <- function(m, output_pdf) {
  pdf(output_pdf, width = 11, height = 8.5)
  on.exit(dev.off())
  par(mar = c(5, 5, 4, 2), pty = "s")
  PC1 <- m$course_pca$PC1
  PC2 <- m$course_pca$PC2
  plot(PC1, PC2, type = "o", pch = 19, cex = 1.2,
       xlab = sprintf("PC1 (%.1f%% var)",
                      100 * m$course_pca$var_explained_PC1),
       ylab = sprintf("PC2 (%.1f%% var)",
                      100 * m$course_pca$var_explained_PC2),
       main = "System Course Plot — PCA 2D path",
       col = "#888")
  text(PC1, PC2, labels = m$labels, pos = 4, cex = 0.7)
  points(PC1[1], PC2[1], pch = 22, bg = "#2ca02c", cex = 2.5)
  points(PC1[m$T], PC2[m$T], pch = 23, bg = "#d62728", cex = 2.5)
  arrows(PC1[1], PC2[1], PC1[m$T], PC2[m$T],
         col = "#1f4e79", lwd = 2, length = 0.15)
  abline(h = 0, lty = 3, col = "#bbb")
  abline(v = 0, lty = 3, col = "#bbb")
  legend("topright",
         legend = c(sprintf("S = %s", m$labels[1]),
                    sprintf("F = %s", m$labels[m$T]),
                    sprintf("course_directness = %.4f",
                            m$navigation$course_directness)),
         pch = c(22, 23, NA), pt.bg = c("#2ca02c", "#d62728", NA),
         cex = 0.85, bty = "n")
  invisible(output_pdf)
}


# --------------------------------------------------------------
# Run as a script
# --------------------------------------------------------------
if (!interactive()) {
  args <- commandArgs(trailingOnly = TRUE)
  if (length(args) >= 1) {
    j <- jsonlite::read_json(args[1], simplifyVector = FALSE)
    m <- stage2_metrics(j)
    stage2_summary(m)
    if (length(args) >= 2) stage2_course_plot(m, args[2])
  } else {
    cat("Usage: Rscript stage2.R <input.json> [course_plot.pdf]\n")
  }
}
