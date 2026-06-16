## ============================================================================
## Hˢ Kinematics Engine — R port (v1.0), a 1:1 mirror of hs_kinematics_engine.py
##
## OFFERED AS IS — and that is deliberate. Neither the author nor the build
## environment had R available to execute this port, so it has NOT been run. It
## is a faithful transcription of the Python reference, provided TOGETHER WITH
## three things an experienced R user can check it against and correct from:
##   1. HS_KINEMATICS_PSEUDOCODE.md  — the language‑agnostic logic
##   2. hs_kinematics_engine.py      — the verified Python reference
##   3. HS_KINEMATICS_SPECIFICATION.md — the full spec + the conformance anchor
## It very likely works; the intent is maximum cross‑platform usefulness. Where it
## does not, the three references above are the ground truth to adjust against —
## fixes are welcome and expected, in the open‑correctable spirit of the project.
##
## CONFORMANCE GATE (same as every port): reproduce the reference content_hash in
## SPEC §11 — fcae0ebe5c4f443aa076d1900d3d04219c2628591323cd7745621e740a3d7ae7 —
## on the reference 12x6 matrix. Treat the NUMERICS as authoritative (they mirror
## the spec); treat the HASH as TO‑VERIFY, since exact parity needs the JSON
## canonicalization to match Python's (sorted keys, 12‑dp floats) — the most
## likely place a real R run will need a small adjustment.
##
## Deps: jsonlite (JSON), digest (sha256). Author: Peter Higgins; AI-assisted
## per HUF-STD-001. Honest-broker — offered transparently, corrected in the open.
## ============================================================================
suppressMessages({ library(jsonlite); library(digest) })

closure <- function(M){ M[M<0] <- 0; s <- rowSums(M); s[s==0] <- 1; M / s }
clr <- function(P){ P[P<1e-12] <- 1e-12; L <- log(P); L - rowMeans(L) }
keff <- function(P){ P <- closure(P); P[P<1e-12] <- 1e-12; exp(-rowSums(P*log(P))) }
shannon_mean <- function(P){ P <- closure(P); mean(-rowSums(P*log(pmax(P,1e-12)))) }

carrier_health <- function(M){
  D <- ncol(M)
  structural <- which(sapply(1:D, function(j) all(M[,j]<=0)))
  constant   <- which(sapply(1:D, function(j) (max(M[,j])-min(M[,j]))==0 & !(j %in% structural)))
  active     <- setdiff(1:D, structural)
  list(structural=structural, constant=constant, active=active)
}
treat_zeros <- function(M){
  for(j in 1:ncol(M)){ p <- M[M[,j]>0,j]; if(length(p)) M[M[,j]<=0,j] <- 0.65*min(p) }
  M
}

tiling_lossless <- function(P){
  T <- nrow(P); D <- ncol(P)
  if(D<4) return(list(err=NA, connected=TRUE))
  logP <- log(pmax(P,1e-12)); charts <- lapply(1:(D-3), function(s) s:(s+3))
  rows <- list(); bij <- list()
  for(ch in charts) for(ai in 1:3) for(ci in (ai+1):4){
    i <- ch[ai]; j <- ch[ci]; r <- numeric(D); r[i] <- 1; r[j] <- -1
    rows[[length(rows)+1]] <- r; bij[[length(bij)+1]] <- c(i,j) }
  A <- rbind(do.call(rbind, rows), rep(1,D)); errs <- c()
  for(t in 1:min(T,50)){
    b <- c(sapply(bij, function(p) logP[t,p[1]]-logP[t,p[2]]), 0)
    rec <- qr.solve(A, b); errs <- c(errs, max(abs(rec - clr(P[t,,drop=FALSE])[1,]))) }
  list(err=max(errs), connected=TRUE)
}

regimes <- function(P,k=2.0){ s <- sqrt(rowSums(diff(clr(P))^2)); thr <- mean(s)+k*sd(s); which(s>thr) }
deceptive <- function(P){ tv <- 0.5*rowSums(abs(diff(closure(P)))); dk <- diff(keff(P)); sum(dk<0 & tv<=median(tv)) }

helmsman_guard <- function(P,nm,floor=1e-6,tie=1e-3){
  tot <- colSums(abs(diff(clr(P)))); o <- order(-tot); mag <- tot[o[1]]
  margin <- if(length(o)>1) tot[o[1]]-tot[o[2]] else mag
  if(mag<floor) return(list(name=NA, code="HM-NUL-WRN"))
  if(margin<=tie*mag) return(list(name="TIE", code="HM-TIE-WRN"))
  list(name=nm[o[1]], code=NA)
}
coherent_helmsman <- function(P,nm){
  lP <- log(pmax(P,1e-12)); D <- ncol(P); m <- numeric(D)
  for(i in 1:D){ for(j in 1:D) if(i!=j) m[i] <- m[i]+sum(abs(diff(lP[,i]-lP[,j]))); m[i] <- m[i]/(D-1) }
  nm[which.max(m)]
}
effective_rank <- function(P){
  X <- clr(P); X <- sweep(X,2,colMeans(X)); s <- svd(X)$d; s <- s[s>max(s)*1e-9]
  pr <- if(length(s)) (sum(s)^2)/sum(s^2) else 0; maxr <- min(nrow(P)-1, ncol(P)-1)
  list(pr=round(pr,2), maxr=maxr, code=if(pr<0.5*maxr) "DG-RNK-WRN" else NA, s=s)
}
hold_lock <- function(P, engine_floor=1e-9){
  H <- clr(P); st <- sqrt(rowSums(diff(H)^2)); if(length(st)<2) return(list(noise=engine_floor, ev=c()))
  md <- median(st); mad <- median(abs(st-md))*1.4826
  noise <- max(engine_floor, max(quantile(st,.5)-mad, quantile(st,.25)), 1e-12)
  up <- 4*noise; lo <- 2*noise; s <- "HOLD"; ev <- c(); ref <- 1
  for(t in 1:length(st)){
    m <- st[t]
    if(s=="HOLD" && m>up){ s <- "MOVING" }
    else if(s=="MOVING" && m<lo){ if(sqrt(sum((H[t+1,]-H[ref,])^2))>=3*noise){ ev <- c(ev,t+1); ref <- t+1 }; s <- "HOLD" } }
  list(noise=round(noise,5), ev=ev)
}

mechanics <- function(P,nm,dt=1.0,noise_ratio=1.5){
  R <- clr(P); lab <- c("position","velocity","acceleration","jerk","snap","crackle"); d <- list(R)
  for(i in 1:5){ if(nrow(d[[length(d)]])<3) break; d[[length(d)+1]] <- diff(d[[length(d)]])/dt }
  mag <- sapply(d, function(x) mean(sqrt(rowSums(x^2)))); order <- 1; ratios <- list()
  if(length(d)>=3) for(k in 3:length(d)){ r <- mag[k]/(mag[k-1]+1e-30); ratios[[lab[k]]] <- round(r,2)
    if(r<noise_ratio){ order <- k-1 } else break }
  v <- d[[2]]; a <- if(length(d)>2) d[[3]] else matrix(0,nrow(v)-1,ncol(v)); mass <- (P[-nrow(P),]+P[-1,])/2
  vv <- v[1:nrow(a),,drop=FALSE]; That <- vv/(sqrt(rowSums(vv^2))+1e-30)
  kappa <- sqrt(rowSums((a-rowSums(a*That)*That)^2))/(rowSums(vv^2)+1e-30)
  p <- mass*v; Fmat <- diff(p)/dt; Tk <- 0.5*rowSums(mass*v*v)
  Pnet <- colSums(p); permag <- sqrt(rowSums(p^2)); coh <- sqrt(sum(colSums(p)^2))/(sum(permag)+1e-30)
  o <- order(-Pnet)
  pathlen <- sum(sqrt(rowSums(v^2))); disp <- sqrt(sum((R[nrow(R),]-R[1,])^2))
  list(arrow_to=nm[o[Pnet[o]>0]][1:3], arrow_from=nm[rev(o)[Pnet[rev(o)]<0]][1:3], coherence=round(coh,3),
       curvature=round(median(kappa),4), force=round(mean(sqrt(rowSums(Fmat^2))),4),
       kinetic=round(mean(Tk),5), action=round(sum(Tk),3), pathlen=round(pathlen,3),
       displacement=round(disp,3), efficiency=round(disp/(pathlen+1e-30),3),
       max_order=paste0(order," (",lab[order+1],")"), ratios=ratios)
}

eitt_boundary <- function(P, levels=c(1,2,4), gate=0.01){
  gm <- function(k){ Pc <- closure(P); Tn <- (nrow(Pc)%/%k)*k
    if(Tn<k) return(Pc[1,,drop=FALSE])
    G <- t(sapply(seq(1,Tn,by=k), function(i) exp(colMeans(log(Pc[i:(i+k-1),,drop=FALSE]))))); closure(G) }
  Hs <- sapply(levels[sapply(levels,function(k) nrow(P)%/%k>=2)], function(k) shannon_mean(gm(k)))
  drift <- if(length(Hs)) (max(Hs)-min(Hs))/(abs(mean(Hs))+1e-12) else 0
  list(entropy_by_level=round(Hs,4), relative_drift=round(drift,4),
       verdict=if(drift<gate) "within-regime (EITT holds; coherent structure)" else "BOUNDARY (edge of analysable structure)",
       code=if(drift<gate) NA else "FR-BND-INF", tier="Tier 3 fringe -- a clue, never a claim")
}

## stable hash: round floats to 12 dp, canonicalize, sha256 (parity with Python TO-VERIFY)
stable_hash <- function(obj){
  digest(toJSON(obj, auto_unbox=TRUE, digits=12, null="null"), algo="sha256", serialize=FALSE)
}

run <- function(M, names=NULL, dt=1.0){
  M <- as.matrix(M); if(is.null(names)) names <- paste0("c",0:(ncol(M)-1))
  ch <- carrier_health(M); guard <- NULL
  if(length(ch$structural) || length(ch$constant)){
    guard <- list(excluded_structural_zero=names[ch$structural], flagged_constant=names[ch$constant],
                  codes=c(if(length(ch$structural))"GD-ZRC-CAL", if(length(ch$constant))"GD-CNC-CAL"))
    if(length(ch$structural)){ M <- M[,ch$active,drop=FALSE]; names <- names[ch$active] } }
  sparsity <- mean(M<=0); M <- treat_zeros(M); P <- closure(M)
  recon <- tiling_lossless(P); helm <- helmsman_guard(P,names); er <- effective_rank(P); hl <- hold_lock(P)
  mech <- mechanics(P,names,dt)
  codes <- c(na.omit(c(helm$code, er$code)), if(sparsity>=0.5)"GD-SPZ-WRN", if(!is.null(guard)) guard$codes)
  payload <- list(
    identity="Hs kinematics engine (R port; named for navigator + physicist; to the computational floor)",
    input=list(records=nrow(P), carriers=ncol(P), names=names, sparsity_pct=round(sparsity*100,1)),
    lossless_reconstruction=list(exact=(recon$connected && (is.na(recon$err) || recon$err<1e-6)), reconstruction_error=recon$err),
    navigation_reads=list(
      effective_spread=list(start=round(keff(P)[1],3), end=round(keff(P)[nrow(P)],3)),
      helmsman=list(clr=names[which.max(colSums(abs(diff(clr(P)))))], resolvable=helm$name, coherent_robust=coherent_helmsman(P,names)),
      waypoints=regimes(P), silent_drift=deceptive(P)),
    kinematics_and_dynamics=mech,
    spectral_modes=list(singulars=round(er$s[1:min(5,length(er$s))],3), effective_dimensionality=er$pr),
    station_keeping=list(discovered_noise_floor=hl$noise, structural_changes_at=hl$ev),
    guards_codes_fired=codes,
    fringe_boundary_TIER3=eitt_boundary(P),
    computational_floors=list(ieee_reconstruction_floor=recon$err, determinism_decimals=12,
                              discovered_noise_floor=hl$noise, max_meaningful_derivative_order=mech$max_order))
  if(!is.null(guard)) payload$input$carrier_guard <- guard
  payload$content_hash <- stable_hash(payload)
  payload
}

## ---- diagnosis language ----
diagnose <- function(M, names=NULL){
  M <- as.matrix(M); if(is.null(names)) names <- paste0("c",0:(ncol(M)-1))
  P <- closure(M); Ks <- keff(P)[1]; Ke <- keff(P)[nrow(P)]; hl <- hold_lock(P)
  st <- sqrt(rowSums(diff(clr(P))^2)); maxstep <- max(st)
  er <- effective_rank(P); rank <- er$pr
  if(maxstep < 4*hl$noise && maxstep < 1e-6)
    return(list(narrative="The system is holding steady — at rest below its own noise floor. Nothing to report.", active_voices=0))
  mass <- (P[-nrow(P),]+P[-1,])/2; v <- diff(clr(P)); mom <- colSums(mass*v)
  mag <- abs(mom); thr <- 0.12*(max(mag)+1e-30); ord <- order(-mag); movers <- ord[mag[ord]>=thr]
  dirn <- ifelse(mom[movers]>0,"gaining","shedding")
  gaining <- names[movers[dirn=="gaining"]]; shedding <- names[movers[dirn=="shedding"]]
  trend <- if(Ke<Ks-0.05) "concentrating" else if(Ke>Ks+0.05) "diversifying" else "steady"
  sent <- c(paste0(names[movers[1]]," is steering (",dirn[1],")."))
  if(length(movers)>1){
    if(length(gaining)) sent <- c(sent, paste0("Weight is moving toward ", paste(head(gaining,8),collapse=", "),"."))
    if(length(shedding)) sent <- c(sent, paste0("It is moving away from ", paste(head(shedding,8),collapse=", "),".")) }
  sent <- c(sent, sprintf("The mixture is %s (effective spread %.2f -> %.2f).", trend, Ks, Ke))
  if(length(hl$ev)) sent <- c(sent, sprintf("It changed state %d time(s).", length(hl$ev)))
  if(rank>1.5) sent <- c(sent, sprintf("The motion runs in about %d independent directions.", round(rank)))
  sent <- c(sent, sprintf("(%d of %d parts have something to say; the rest are quiet.)", length(movers), ncol(P)))
  list(narrative=paste(sent, collapse=" "), active_voices=length(movers))
}

## ---- reference self-test (run on an R install to check against spec §11) ----
if(sys.nframe()==0){
  names <- c("Coal","Gas","Hydro","Nuclear","Wind","Solar")
  ref <- matrix(c(40,25,15,12,5,3, 38,25,15,12,6,4, 35,25,16,12,8,4, 33,24,16,12,9,6,
                  30,24,16,13,10,7, 28,23,17,13,11,8, 25,23,17,13,13,9, 22,22,18,13,14,11,
                  20,22,18,14,15,11, 18,21,18,14,17,12, 16,21,19,14,18,12, 15,20,19,14,19,13),
                ncol=6, byrow=TRUE)
  o <- run(ref, names)
  cat("lossless exact:", o$lossless_reconstruction$exact, " err:", o$lossless_reconstruction$reconstruction_error, "\n")
  cat("content_hash:", o$content_hash, "  (target fcae0ebe…a3d7ae7 — verify JSON canonicalization)\n")
  cat("diagnosis:", diagnose(ref, names)$narrative, "\n")
}
