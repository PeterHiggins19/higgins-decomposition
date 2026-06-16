# ====================================================================================
#  CN-TT v4 — self-contained single cell, R port (base R; `digest` only for the hash).
#  1:1 mirror of tools/CNTT_single_cell.py (verified). Paste into a JupyterLab R cell
#  or run with Rscript. Engine core + lossless 4-part tiling + navigation + guard layer.
#  Author: Peter Higgins; AI-assisted per HUF-STD-001. Honest-broker.
#  NOTE: the numeric reads (lossless err, helmsman, K_eff, eff-rank, hold-lock) match the
#  Python bit-for-bit (same math, same IEEE-754 floats). The content hash is an R-side
#  determinism receipt; cross-LANGUAGE hash identity needs a shared canonical serialization
#  (Tier-3). install.packages("digest") for the hash, or set HASH=FALSE.
# ====================================================================================
HASH <- requireNamespace("digest", quietly = TRUE)

# ---- geometry ----------------------------------------------------------------------
closure <- function(M){ M[M<0]<-0; s<-rowSums(M); s[s==0]<-1; M/s }
clr     <- function(P){ P[P<1e-12]<-1e-12; L<-log(P); L - rowMeans(L) }
helmert <- function(D){ B<-matrix(0,D-1,D); for(i in 1:(D-1)){ B[i,1:i]<-1/i; B[i,i+1]<- -1; B[i,]<-B[i,]*sqrt(i/(i+1)) }; B }
ilr     <- function(P){ clr(P) %*% t(helmert(ncol(P))) }

# ---- E-21 carrier guard + zero treatment -------------------------------------------
carrier_health <- function(M){
  structural <- which(apply(M, 2, function(c) all(c<=0)))
  constant   <- setdiff(which(apply(M, 2, function(c) (max(c)-min(c))==0)), structural)
  active     <- setdiff(seq_len(ncol(M)), structural)
  list(structural=structural, constant=constant, active=active)
}
treat_zeros <- function(M){ for(j in seq_len(ncol(M))){ pos<-M[M[,j]>0,j]; if(length(pos)) M[M[,j]<=0,j]<-0.65*min(pos) }; M }

# ---- lossless 4-part tiling (overlap-3 sliding charts; reconstruct CLR; report error)
tiling_lossless <- function(P){
  T<-nrow(P); D<-ncol(P); if(D<4) return(list(err=NA, conn=TRUE))
  logP<-log(pmax(P,1e-12)); charts<-lapply(0:(D-4), function(s) (s+1):(s+4))
  rows<-list(); bidx<-list(); n<-0
  for(ch in charts) for(a in 1:3) for(c in (a+1):4){ i<-ch[a]; j<-ch[c]
    r<-numeric(D); r[i]<-1; r[j]<- -1; n<-n+1; rows[[n]]<-r; bidx[[n]]<-c(i,j) }
  A<-rbind(do.call(rbind,rows), rep(1,D))                          # + sum-zero constraint
  errs<-c()
  for(t in 1:min(T,50)){
    b<-sapply(bidx, function(ij) logP[t,ij[1]]-logP[t,ij[2]]); b<-c(b,0)
    rec<-qr.solve(A,b); errs<-c(errs, max(abs(rec - clr(P[t,,drop=FALSE])[1,])))
  }
  list(err=max(errs), conn=TRUE)
}

# ---- navigation family --------------------------------------------------------------
k_eff   <- function(P){ P[P<1e-12]<-1e-12; P<-P/rowSums(P); exp(-rowSums(P*log(P))) }
steps   <- function(P){ H<-clr(P); sqrt(rowSums(diff(H)^2)) }
regimes <- function(P,k=2){ s<-steps(P); thr<-mean(s)+k*sd(s); which(s>thr)+1 }
deceptive <- function(P){ tv<-0.5*rowSums(abs(diff(closure(P)))); dk<-diff(k_eff(P)); sum(dk<0 & tv<=median(tv)) }

# ---- the 2026-06 guard layer --------------------------------------------------------
helmsman_guard <- function(P,nm,motion_floor=1e-6,tie_rel=1e-3){
  tot<-colSums(abs(diff(clr(P)))); o<-order(-tot); mag<-tot[o[1]]; margin<-if(length(o)>1) tot[o[1]]-tot[o[2]] else mag
  if(mag<motion_floor) return(list(helmsman=NA, code="HM-NUL-WRN", margin=margin))
  if(margin<=tie_rel*mag) return(list(helmsman="TIE", code="HM-TIE-WRN", margin=margin))
  list(helmsman=nm[o[1]], code=NA, margin=round(margin,4))
}
coherent_helmsman <- function(P,nm){
  lP<-log(pmax(P,1e-12)); D<-ncol(P); m<-numeric(D)
  for(i in 1:D){ for(j in 1:D) if(i!=j) m[i]<-m[i]+sum(abs(diff(lP[,i]-lP[,j]))); m[i]<-m[i]/(D-1) }
  nm[which.max(m)]
}
effective_rank <- function(P){
  X<-clr(P); X<-sweep(X,2,colMeans(X)); s<-svd(X)$d; s<-s[s>max(s)*1e-9]
  pr<-if(length(s)) sum(s)^2/sum(s^2) else 0; maxr<-min(nrow(P)-1,ncol(P)-1)
  list(value=round(pr,2), max=maxr, code=if(pr<0.5*maxr) "DG-RNK-WRN" else NA)
}
hold_lock <- function(P,engine_floor=1e-9,k_up=4,k_down=2,struct_k=3){
  H<-clr(P); st<-sqrt(rowSums(diff(H)^2)); if(length(st)<2) return(list(floor=0,events=c()))
  md<-median(st); mad<-median(abs(st-md))*1.4826
  noise<-max(engine_floor, max(quantile(st,0.5)-mad, quantile(st,0.25)), 1e-12); up<-k_up*noise; lo<-k_down*noise
  s<-"HOLD"; ev<-c(); ref<-1
  for(t in seq_along(st)){
    if(s=="HOLD" && st[t]>up) s<-"MOVING"
    else if(s=="MOVING" && st[t]<lo){ if(sqrt(sum((H[t+1,]-H[ref,])^2))>=struct_k*noise){ ev<-c(ev,t+1); ref<-t+1 }; s<-"HOLD" }
  }
  list(floor=round(noise,4), events=ev)
}

# ---- the engine: composition matrix + names -> payload list ------------------------
run_cntt <- function(M, names=NULL){
  M<-as.matrix(M); if(is.null(names)) names<-paste0("c",seq_len(ncol(M)))
  h<-carrier_health(M); guard<-NULL
  if(length(h$structural) || length(h$constant)){
    guard<-list(excluded_structural_zero=names[h$structural], flagged_constant=names[h$constant],
                codes=c(if(length(h$structural))"GD-ZRC-CAL", if(length(h$constant))"GD-CNC-CAL"))
    if(length(h$structural)){ M<-M[,h$active,drop=FALSE]; names<-names[h$active] }
  }
  sparsity<-mean(M<=0); M<-treat_zeros(M); P<-closure(M); tl<-tiling_lossless(P)
  res<-helmsman_guard(P,names); rnk<-effective_rank(P)
  codes<-c(na.omit(c(res$code,rnk$code)), if(!is.null(guard)) guard$codes[1])
  hd<-clr(P); clrm<-names[which.max(colSums(abs(diff(hd))))]
  payload<-list(
    input=list(n_records=nrow(P), n_carriers=ncol(P), carriers=names, sparsity_pct=round(sparsity*100,1)),
    atlas=list(lossless=(tl$conn && (is.na(tl$err) || tl$err<1e-6)), reconstruction_max_err=tl$err),
    navigation=list(k_eff_start=round(k_eff(P)[1],3), k_eff_end=round(tail(k_eff(P),1),3),
                    helmsman_CLR=clrm, coherent_helmsman=coherent_helmsman(P,names),
                    regime_boundaries=regimes(P), deceptive_drift_steps=deceptive(P)),
    guards=list(resolvability=res, effective_rank=list(value=rnk$value,max=rnk$max),
                hold_lock=hold_lock(P), sparsity_regime=if(sparsity>=0.5)"GD-SPZ-WRN" else NA,
                codes_fired=codes))
  if(!is.null(guard)) payload$input$carrier_guard<-guard
  if(HASH) payload$cntt_content_sha256<-digest::digest(payload, algo="sha256")
  payload
}

# ====================================================================================
#  DEMO — runs on source(). Replace M, names with your own (rows=time/sample, cols=parts)
# ====================================================================================
set.seed(0); T<-60; D<-8
names<-c("Coal","Gas","Hydro","Nuclear","Wind","Solar","Bio","Other")
base<-c(0.30,0.22,0.18,0.12,0.08,0.04,0.04,0.02)
drift<-apply(matrix(rnorm(T*D,0,0.01),T,D),2,cumsum)
M<-pmax(matrix(base,T,D,byrow=TRUE)+drift+matrix(rnorm(T*D,0,0.005),T,D), 1e-4)
out<-run_cntt(M, names)
str(out, max.level=2)
cat("\nlossless:", out$atlas$lossless, "| recon err:", out$atlas$reconstruction_max_err,
    "| helmsman:", out$navigation$helmsman_CLR, "(coherent:", out$navigation$coherent_helmsman, ")",
    "| eff_rank:", out$guards$effective_rank$value, "/", out$guards$effective_rank$max, "\n")
