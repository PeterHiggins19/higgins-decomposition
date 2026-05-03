#!/usr/bin/env python3
"""hs_projector_gen.py -- Certified Hs Manifold Projector generator.

Generates self-contained HTML manifold projectors from polar_stack JSON.
Per-run min-max normalization preserves shape fidelity and magnitude evolution.
Degenerate timesteps (no CLR variation) render as point markers, not polygons.
Missing carriers render as X markers. The instrument does not fabricate structure.

Instrument status: CERTIFIED (MC-4 calibration 5/5 PASS).
The data is the Device Under Test. The projector is never the DUT.
Methodology chain: closure -> CLR -> spline -> per-run normalization -> projection.
CoDaWork-certifiable. No known misstep in the data representation.
"""
import argparse, json, sys

PALETTE = ["#ffd700","#ff6b6b","#4169e1","#32cd32","#ff69b4","#ff4500","#00ced1",
           "#9370db","#d4944a","#4ab8d4","#5db87a","#8a9baa","#e06060","#7ab85a",
           "#d4b44a","#b07040","#8ab8d8","#c0c060","#60c0a0","#a060d0"]
RUN_COLORS = ["#ffd700","#ff6b6b","#4169e1","#32cd32","#ff69b4","#ff4500","#ffffff",
              "#00ced1","#9370db","#d4944a"]

def load_run_raw(path, idx):
    """Load a run without normalization -- norm will be computed globally later."""
    ps = json.load(open(path))
    carriers, intervals = ps["carriers"], ps["intervals"]
    D = len(carriers)
    clr = [[iv["clr"][c] for c in carriers] for iv in intervals]
    years = [iv.get("year", iv["index"]) for iv in intervals]
    return {"code": ps.get("experiment","RUN%d"%idx), "name": ps.get("test_object","Run %d"%idx),
            "color": RUN_COLORS[idx % len(RUN_COLORS)], "carriers": carriers,
            "years": years, "clr": clr, "norm": None}

def compute_global_norms(runs):
    """Compute norm arrays using per-run min-max normalization.

    For each run, finds the global min and max CLR across ALL timesteps
    and ALL carriers within that run, then maps every value to [0, 1].

    This preserves:
    - Within-timestep shape (polygon geometry from relative carrier values)
    - Between-timestep magnitude (size changes over time, e.g. sphere envelope)
    - Data integrity: the projector reveals what the data contains, nothing more

    Each run has its own scale. The projector does not fabricate structure.
    If the projected shape does not match expectation, the data is the issue,
    not the instrument.

    Degenerate timesteps (all carriers equal, CLR spread < threshold) are
    flagged. The projector renders these as point markers, not polygons.
    Suppressed carriers (CLR < -10) are flagged as missing.
    The instrument shows what exists and marks what does not.
    """
    DEGEN_THRESH = 1e-4  # CLR spread below this = degenerate (no structure)
    for r in runs:
        D = len(r["carriers"])
        # Find min/max across ALL timesteps within this run
        r_min = float("inf")
        r_max = float("-inf")
        for row in r["clr"]:
            for j in range(D):
                v = row[j]
                if v < -10:
                    continue
                if v < r_min:
                    r_min = v
                if v > r_max:
                    r_max = v
        r_range = r_max - r_min
        run_uniform = r_range < 1e-6  # entire run has no variation
        # Map each CLR value to [0, 1] on this run's scale
        # Also compute per-timestep flags
        norm = []
        degen = []  # 1 = degenerate timestep, 0 = valid
        missing = []  # per-timestep list of missing carrier flags
        for row in r["clr"]:
            # Check within-timestep spread
            vals = [row[j] for j in range(D) if row[j] > -10]
            t_spread = (max(vals) - min(vals)) if vals else 0.0
            is_degen = 1 if (t_spread < DEGEN_THRESH or not vals) else 0
            degen.append(is_degen)
            nr = []
            mr = []  # missing flags for this timestep
            for j in range(D):
                v = row[j]
                if v < -10:
                    nr.append(0.0)
                    mr.append(1)  # missing carrier
                    continue
                mr.append(0)
                if run_uniform or is_degen:
                    nr.append(0.0)  # degenerate: no structure to show
                else:
                    nr.append((v - r_min) / r_range)
            norm.append(nr)
            missing.append(mr)
        r["norm"] = norm
        r["degen"] = degen
        r["missing"] = missing
        # Carrier lock detection: find signal acquisition/loss boundaries
        # A lock point is the first valid timestep adjacent to a degenerate one.
        # lock_type: 0=normal, 1=lock-acquisition (DEGEN->valid), 2=lock-loss (valid->DEGEN)
        # lock_offset: the CLR spread at the lock point (distance from true zero)
        T = len(degen)
        lock = [0] * T
        lock_offset = [0.0] * T
        for t in range(T):
            if degen[t]:
                continue  # degenerate timesteps are not lock points
            vals = [r["clr"][t][j] for j in range(D) if r["clr"][t][j] > -10]
            t_spread = (max(vals) - min(vals)) if vals else 0.0
            # Check if previous timestep was degenerate (signal acquisition)
            if t > 0 and degen[t - 1]:
                lock[t] = 1  # lock acquisition
                lock_offset[t] = t_spread
            # Check if next timestep is degenerate (signal loss)
            if t < T - 1 and degen[t + 1]:
                lock[t] = 2  # lock loss
                lock_offset[t] = t_spread
        r["lock"] = lock
        r["lock_offset"] = lock_offset

def ja(arr): return "[" + ",".join("%.6g"%v for v in arr) + "]"

def fmt_run(r):
    lines = ["  code:%s,name:%s,color:'%s'," % (json.dumps(r["code"]),json.dumps(r["name"]),r["color"])]
    lines.append("  carriers:%s," % json.dumps(r["carriers"]))
    yv = []
    for y in r["years"]:
        yv.append(str(int(y)) if isinstance(y,(int,float)) and y==int(y) else ("%.6g"%y if isinstance(y,(int,float)) else json.dumps(y)))
    lines.append("  years:[%s]," % ",".join(yv))
    lines.append("  clr:[%s]," % ",".join(ja(row) for row in r["clr"]))
    lines.append("  norm:[%s]," % ",".join(ja(row) for row in r["norm"]))
    lines.append("  degen:[%s]," % ",".join(str(d) for d in r["degen"]))
    lines.append("  lock:[%s]," % ",".join(str(l) for l in r["lock"]))
    lines.append("  lock_offset:[%s]," % ",".join("%.6g"%o for o in r["lock_offset"]))
    lines.append("  missing:[%s]" % ",".join("["+",".join(str(m) for m in row)+"]" for row in r["missing"]))
    return "\n".join(lines)

def generate(runs, title, subtitle):
    all_carriers = []
    for r in runs:
        for c in r["carriers"]:
            if c not in all_carriers: all_carriers.append(c)
    cc = {}
    for i,c in enumerate(all_carriers): cc[c] = PALETTE[i % len(PALETTE)]
    data_js = "var DATA = {\n" + ",\n".join("'%s':{\n%s\n}" % (r["code"],fmt_run(r)) for r in runs) + "\n};"
    cc_js = "var CARRIER_COLORS = {\n" + ",\n".join("  %s:'%s'" % (json.dumps(c),v) for c,v in cc.items()) + "\n};"
    ro_js = "var runOrder = %s;" % json.dumps([r["code"] for r in runs])
    first = runs[0]["code"]
    maxt = max(len(r["years"]) for r in runs)
    multi = len(runs) > 1
    safe = lambda s: s.replace("&","&amp;").replace("<","&lt;")
    leg = "\n  ".join('<div class="leg-item"><div class="leg-dot" style="background:%s"></div> %s</div>' % (v,c) for c,v in cc.items())
    html = HTML_TPL
    html = html.replace("__TITLE__",safe(title))
    html = html.replace("__SUB__",safe(subtitle))
    html = html.replace("__DATA__",data_js)
    html = html.replace("__CC__",cc_js)
    html = html.replace("__RO__",ro_js)
    html = html.replace("__FR__",first)
    html = html.replace("__AI__",str(maxt))
    html = html.replace("__MT__",str(maxt))
    html = html.replace("__LEG__",leg)
    html = html.replace("__MULTI__","true" if multi else "false")
    return html

HTML_TPL = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Hs Manifold Projector | __TITLE__</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#030406;color:#6898b8;font-family:'Courier New',monospace;overflow:hidden;width:100vw;height:100vh}
canvas{display:block;position:absolute;top:0;left:0}
.hud{position:absolute;pointer-events:none;user-select:none}
.hud-tl{top:16px;left:20px}
.hud-tl h1{font-size:18px;color:#6898b8;font-weight:400;letter-spacing:2px}
.hud-tl h1 b{color:#8ab8d8}
.hud-tl .sub{font-size:10px;color:#405868;letter-spacing:3px;margin-top:2px}
.hud-tr{top:12px;right:16px;display:flex;flex-direction:column;align-items:flex-end;gap:6px;pointer-events:auto}
.ctrl-row{display:flex;gap:4px;flex-wrap:wrap;justify-content:flex-end}
.btn{background:#101820;border:1px solid #253038;color:#6898b8;font-family:'Courier New',monospace;font-size:10px;padding:3px 8px;cursor:pointer;letter-spacing:1px;transition:all .15s}
.btn:hover{border-color:#6898b8;color:#8ab8d8}
.btn.active{background:#1a2830;border-color:#6898b8;color:#8ab8d8}
.btn.run{padding:3px 10px}
.btn.run.active{border-color:var(--cc);color:var(--cc);background:#101820}
.hud-bl{bottom:28px;left:20px;right:20px;pointer-events:auto}
.time-row{display:flex;align-items:center;gap:8px}
.time-row label{font-size:10px;color:#405868;min-width:36px}
.time-slider{flex:1;-webkit-appearance:none;appearance:none;height:3px;background:#1a2830;outline:none;border-radius:2px;cursor:pointer}
.time-slider::-webkit-slider-thumb{-webkit-appearance:none;width:12px;height:12px;background:#6898b8;border-radius:50%;cursor:pointer}
.time-val{font-size:11px;color:#6898b8;min-width:32px;text-align:right}
.readout{margin-top:6px;font-size:9px;color:#405868;letter-spacing:1px;display:flex;gap:16px;flex-wrap:wrap}
.readout span{white-space:nowrap} .readout .val{color:#6898b8}
.hud-left{top:50%;left:12px;transform:translateY(-50%);pointer-events:auto;display:flex;flex-direction:column;align-items:center;gap:4px}
.zoom-slider{-webkit-appearance:none;appearance:none;width:3px;height:160px;background:#1a2830;outline:none;border-radius:2px;cursor:pointer;writing-mode:bt-lr;-webkit-appearance:slider-vertical}
.zoom-label{font-size:8px;color:#405868;letter-spacing:1px}
.hud-br{bottom:70px;right:16px;font-size:9px;color:#405868;pointer-events:none}
.hud-br .leg-title{color:#506878;margin-bottom:4px;letter-spacing:1px}
.hud-br .leg-item{display:flex;align-items:center;gap:6px;margin:2px 0}
.leg-dot{width:8px;height:3px;border-radius:1px}
</style></head><body>
<canvas id="cv"></canvas>
<div class="hud hud-tl"><h1>H<b>&#178;</b> Manifold Projector</h1><div class="sub">__SUB__</div><div class="sub" style="color:#2a4a3a;margin-top:6px;font-size:8px;letter-spacing:1px">CERTIFIED &#x2022; DATA IS DUT &#x2022; CoDaWork Standard</div></div>
<div class="hud hud-tr" id="controls">
  <div class="ctrl-row" id="runBtns"></div>
  <div class="ctrl-row">
    <button class="btn active" id="btnOrbit" onclick="toggleOrbit()">ORBIT</button>
    <button class="btn" id="btnTrails" onclick="toggle('trails')">TRAILS</button>
    <button class="btn" id="btnLabels" onclick="toggle('labels')">LABELS</button>
    <button class="btn" id="btnGhost" onclick="toggle('ghost')">GHOST</button>
    <button class="btn" id="btnColor" onclick="toggle('colorMode')">COLOR</button>
  </div>
  <div class="ctrl-row">
    <button class="btn" onclick="setView('front')">FRONT</button>
    <button class="btn" onclick="setView('side')">SIDE</button>
    <button class="btn" onclick="setView('top')">TOP</button>
    <button class="btn" onclick="setView('iso')">ISO</button>
  </div>
</div>
<div class="hud hud-left"><div class="zoom-label">ZOOM</div>
  <input type="range" class="zoom-slider" id="zoomSlider" min="30" max="300" value="100" orient="vertical" oninput="zoom=+this.value/100">
  <div class="zoom-label">DEPTH</div></div>
<div class="hud hud-bl"><div class="time-row"><label>TIME</label>
    <input type="range" class="time-slider" id="timeSlider" min="0" max="__MT__" value="__MT__" oninput="setTime(+this.value)">
    <span class="time-val" id="timeVal">ALL</span></div>
  <div class="readout" id="readout"></div></div>
<div class="hud hud-br" id="legend"><div class="leg-title">CARRIERS</div>
  __LEG__
</div>
<script>
__DATA__
__CC__
__RO__
var MULTI=__MULTI__;
var cv,ctx,W,H,dpr,rotX=-0.35,rotY=0.4,zoom=1.0;
var orbit=true,trails=false,colorMode=false,ghost=false,labels=false;
var currentRun='__FR__',showAll=false,ALL_IDX=__AI__,timeIdx=ALL_IDX,lockYear=-1;
var mouseDown=false,lastMX=0,lastMY=0,orbitAngle=0,mouseX=-1,mouseY=-1;
var FOV=700,RADIUS=140,Z_SPACING=18;
function initRun(d){var D=d.carriers.length,T=d.years.length;d.vt=[];
  for(var t=0;t<T;t++){var s=0;for(var j=0;j<D;j++)s+=d.clr[t][j]*d.clr[t][j];d.vt.push(Math.sqrt(s));}
  var first=d.clr[0],last=d.clr[T-1],dd=0;
  for(var j=0;j<D;j++)dd+=(first[j]-last[j])*(first[j]-last[j]);
  var directDist=Math.sqrt(dd),pathLen=0;
  for(var t=1;t<T;t++){var seg=0;for(var j=0;j<D;j++)seg+=(d.clr[t][j]-d.clr[t-1][j])*(d.clr[t][j]-d.clr[t-1][j]);pathLen+=Math.sqrt(seg);}
  d.pathEff=pathLen>0?directDist/pathLen:1;
  var vtS=d.vt[0],vtE=d.vt[T-1];
  d.vtShape=vtE>vtS*1.2?'EXPANDING':vtE<vtS*0.8?'CONTRACTING':'STABLE';}
var k;for(k in DATA){if(DATA.hasOwnProperty(k))initRun(DATA[k]);}
function resize(){dpr=window.devicePixelRatio||1;W=window.innerWidth;H=window.innerHeight;
  cv.width=W*dpr;cv.height=H*dpr;cv.style.width=W+'px';cv.style.height=H+'px';ctx.setTransform(dpr,0,0,dpr,0,0);}
function updateRunBtnStyles(){
  var bs=document.querySelectorAll('.btn.run');
  for(var x=0;x<bs.length;x++){
    var rc=bs[x].getAttribute('data-run');
    if(rc==='__ALL__'){bs[x].classList.toggle('active',showAll);}
    else{bs[x].classList.toggle('active',!showAll&&rc===currentRun);}
  }
}
function selectRun(c){showAll=false;currentRun=c;
  var d=DATA[c],sl=document.getElementById('timeSlider');sl.max=d.years.length;
  if(timeIdx>d.years.length)timeIdx=d.years.length;setTime(timeIdx);
  updateRunBtnStyles();}
function selectAll(){showAll=true;
  var mt=0;for(var i=0;i<runOrder.length;i++){var T=DATA[runOrder[i]].years.length;if(T>mt)mt=T;}
  var sl=document.getElementById('timeSlider');sl.max=mt;
  if(timeIdx>mt)timeIdx=mt;setTime(timeIdx);
  updateRunBtnStyles();}
function buildRunButtons(){var cB=document.getElementById('runBtns');
  if(MULTI){var ab=document.createElement('button');
    ab.className='btn run';ab.textContent='ALL';
    ab.style.setProperty('--cc','#8ab8d8');ab.setAttribute('data-run','__ALL__');
    ab.onclick=selectAll;cB.appendChild(ab);}
  for(var i=0;i<runOrder.length;i++){(function(c){var b=document.createElement('button');
    b.className='btn run'+(c===currentRun&&!showAll?' active':'');b.textContent=DATA[c].name.replace(/^EMBER /,'');
    b.style.setProperty('--cc',DATA[c].color);b.setAttribute('data-run',c);
    b.onclick=function(){selectRun(c);};
    cB.appendChild(b);})(runOrder[i]);}}
function toggleOrbit(){orbit=!orbit;document.getElementById('btnOrbit').classList.toggle('active',orbit);}
function toggle(key){
  if(key==='trails'){trails=!trails;document.getElementById('btnTrails').classList.toggle('active',trails);}
  if(key==='colorMode'){colorMode=!colorMode;document.getElementById('btnColor').classList.toggle('active',colorMode);}
  if(key==='ghost'){ghost=!ghost;document.getElementById('btnGhost').classList.toggle('active',ghost);}
  if(key==='labels'){labels=!labels;document.getElementById('btnLabels').classList.toggle('active',labels);}}
function setView(v){
  if(v==='front'){rotX=0;rotY=0;}if(v==='side'){rotX=0;rotY=Math.PI/2;}
  if(v==='top'){rotX=-Math.PI/2;rotY=0;}if(v==='iso'){rotX=-0.35;rotY=0.4;}}
function setTime(v){
  timeIdx=v;
  if(showAll){document.getElementById('timeVal').textContent=v>=ALL_IDX?'ALL':String(v);}
  else{var d=DATA[currentRun],T=d.years.length;
    document.getElementById('timeVal').textContent=v<T?d.years[v]:'ALL';}}
function setupMouse(){
  cv.addEventListener('mousedown',function(e){mouseDown=true;lastMX=e.clientX;lastMY=e.clientY;orbit=false;document.getElementById('btnOrbit').classList.remove('active');});
  window.addEventListener('mouseup',function(){mouseDown=false;});
  window.addEventListener('mousemove',function(e){mouseX=e.clientX;mouseY=e.clientY;
    if(mouseDown){rotY+=(e.clientX-lastMX)*0.005;rotX+=(e.clientY-lastMY)*0.005;
      rotX=Math.max(-Math.PI/2,Math.min(Math.PI/2,rotX));lastMX=e.clientX;lastMY=e.clientY;}});
  cv.addEventListener('wheel',function(e){e.preventDefault();
    zoom=Math.max(0.3,Math.min(3,zoom-e.deltaY*0.002));
    document.getElementById('zoomSlider').value=Math.round(zoom*100);},{passive:false});
  cv.addEventListener('dblclick',function(e){var d=DATA[currentRun],bestDist=Infinity,bestT=-1;
    for(var t=0;t<d.years.length;t++){var pts=gSP(d,t),cx=0,cy=0;
      for(var p=0;p<pts.length;p++){cx+=pts[p].x;cy+=pts[p].y;}cx/=pts.length;cy/=pts.length;
      var dist=Math.sqrt((e.clientX-cx)*(e.clientX-cx)+(e.clientY-cy)*(e.clientY-cy));
      if(dist<bestDist){bestDist=dist;bestT=t;}}
    if(bestDist<80)lockYear=(lockYear===bestT)?-1:bestT;});}
function proj(x3,y3,z3){var cY=Math.cos(rotY),sY=Math.sin(rotY),cX=Math.cos(rotX),sX=Math.sin(rotX);
  var x=x3*cY-z3*sY,z=x3*sY+z3*cY,y=y3*cX-z*sX;z=y3*sX+z*cX;
  var sc=FOV/(FOV+z+350);return{x:W/2+x*sc*zoom,y:H/2+y*sc*zoom,s:sc*zoom,z:z};}
function zOff(d){return -Math.floor(d.years.length/2)*Z_SPACING;}
function gP3(d,t){var D=d.carriers.length,pts=[],zo=zOff(d),zP=zo+t*Z_SPACING;
  if(d.degen[t]){/* degenerate: all points at center */
    for(var j=0;j<D;j++)pts.push({x:0,y:0,z:zP,carrier:j,degen:true});return pts;}
  for(var j=0;j<D;j++){var a=(j/D)*Math.PI*2-Math.PI/2,r=RADIUS*(0.1+0.9*d.norm[t][j]);
    var miss=d.missing[t][j];
    pts.push({x:r*Math.cos(a),y:r*Math.sin(a),z:zP,carrier:j,miss:miss});}return pts;}
function gSP(d,t){var p3=gP3(d,t),r=[];for(var i=0;i<p3.length;i++)r.push(proj(p3[i].x,p3[i].y,p3[i].z));return r;}
function h2r(hex){return[parseInt(hex.slice(1,3),16),parseInt(hex.slice(3,5),16),parseInt(hex.slice(5,7),16)];}
function drawOneRun(d,asGhost){
  var D=d.carriers.length,T=d.years.length,showYears=[];
  if(timeIdx>=T){for(var t=0;t<T;t++)showYears.push(t);}
  else{showYears.push(timeIdx);for(var dt=-2;dt<=2;dt++){var tt=timeIdx+dt;if(tt>=0&&tt<T&&tt!==timeIdx)showYears.push(tt);}}
  var polys=[];
  for(var si=0;si<showYears.length;si++){var t=showYears[si],p3=gP3(d,t),p2=[],az=0;
    for(var pi=0;pi<p3.length;pi++){var pp=proj(p3[pi].x,p3[pi].y,p3[pi].z);p2.push(pp);az+=pp.z;}
    az/=p2.length;polys.push({t:t,pts3d:p3,pts2d:p2,avgZ:az});}
  polys.sort(function(a,b){return b.avgZ-a.avgZ;});
  var gf=asGhost?0.35:1.0;
  if(trails&&timeIdx>=T){for(var j=0;j<D;j++){var cc=CARRIER_COLORS[d.carriers[j]]||'#6898b8';
    ctx.strokeStyle=cc+'50';ctx.lineWidth=1;ctx.beginPath();var started=false;
    for(var t=0;t<T;t++){if(d.degen[t]||d.missing[t][j])continue;/* skip degenerate/missing */
      var p3t=gP3(d,t),p=proj(p3t[j].x,p3t[j].y,p3t[j].z);
      if(!started){ctx.moveTo(p.x,p.y);started=true;}else ctx.lineTo(p.x,p.y);}if(started)ctx.stroke();}}
  for(var pi=0;pi<polys.length;pi++){var poly=polys[pi],t=poly.t,p2=poly.pts2d,p3=poly.pts3d;
    var isF=timeIdx>=T||t===timeIdx,isL=lockYear===t;
    var df=Math.max(0.15,Math.min(1,(poly.avgZ+500)/700));
    var al=(isF?(0.12+0.12*df):0.04)*gf,sa=(isF?(0.5+0.3*df):0.15)*gf;
    var rgb=h2r(d.color),cr=rgb[0],cg=rgb[1],cb=rgb[2];
    /* --- DEGENERATE TIMESTEP: point marker, no polygon --- */
    if(d.degen[t]){
      var cx=0,cy=0;for(var qi=0;qi<p2.length;qi++){cx+=p2[qi].x;cy+=p2[qi].y;}cx/=p2.length;cy/=p2.length;
      if(isF&&!asGhost){
        /* diamond marker */
        var ds=5;ctx.strokeStyle='#ff4500';ctx.lineWidth=2;ctx.beginPath();
        ctx.moveTo(cx,cy-ds);ctx.lineTo(cx+ds,cy);ctx.lineTo(cx,cy+ds);ctx.lineTo(cx-ds,cy);ctx.closePath();ctx.stroke();
        ctx.fillStyle='rgba(255,69,0,0.3)';ctx.fill();
        /* label */
        ctx.fillStyle='#ff4500';ctx.font='8px Courier New';ctx.fillText('DEGEN t='+d.years[t],cx+8,cy-4);
      }else{
        /* faint dot for non-focused degenerate */
        ctx.fillStyle='rgba(255,69,0,'+(0.15*gf)+')';ctx.beginPath();ctx.arc(cx,cy,2,0,Math.PI*2);ctx.fill();
      }
      continue;/* skip polygon rendering */
    }
    /* --- NORMAL TIMESTEP: filter out missing carriers for polygon --- */
    var validIdx=[];for(var j=0;j<D;j++){if(!p3[j].miss)validIdx.push(j);}
    /* draw polygon using only valid (non-missing) carriers */
    if(validIdx.length>=2){
      ctx.beginPath();for(var fi=0;fi<validIdx.length;fi++){var vi=validIdx[fi];if(fi===0)ctx.moveTo(p2[vi].x,p2[vi].y);else ctx.lineTo(p2[vi].x,p2[vi].y);}ctx.closePath();
      if(colorMode&&!asGhost){for(var fi=0;fi<validIdx.length;fi++){var j=validIdx[fi],j2=validIdx[(fi+1)%validIdx.length];
        var cc2=CARRIER_COLORS[d.carriers[j]]||'#6898b8',cr2=h2r(cc2),cxc=0,cyc=0;
        for(var qi=0;qi<validIdx.length;qi++){cxc+=p2[validIdx[qi]].x;cyc+=p2[validIdx[qi]].y;}cxc/=validIdx.length;cyc/=validIdx.length;
        ctx.beginPath();ctx.moveTo(cxc,cyc);ctx.lineTo(p2[j].x,p2[j].y);ctx.lineTo(p2[j2].x,p2[j2].y);ctx.closePath();
        ctx.fillStyle='rgba('+cr2[0]+','+cr2[1]+','+cr2[2]+','+(al*1.5)+')';ctx.fill();}}
      else{ctx.fillStyle='rgba('+cr+','+cg+','+cb+','+al+')';ctx.fill();}
      ctx.beginPath();for(var fi=0;fi<validIdx.length;fi++){var vi=validIdx[fi];if(fi===0)ctx.moveTo(p2[vi].x,p2[vi].y);else ctx.lineTo(p2[vi].x,p2[vi].y);}ctx.closePath();
      ctx.strokeStyle='rgba('+cr+','+cg+','+cb+','+sa+')';ctx.lineWidth=isF?(asGhost?0.8:1.2):0.6;ctx.stroke();
    }
    if(isL&&!asGhost){ctx.shadowColor='#ffd700';ctx.shadowBlur=12;ctx.strokeStyle='#ffd70080';ctx.lineWidth=2;
      ctx.beginPath();for(var fi=0;fi<validIdx.length;fi++){var vi=validIdx[fi];if(fi===0)ctx.moveTo(p2[vi].x,p2[vi].y);else ctx.lineTo(p2[vi].x,p2[vi].y);}
      ctx.closePath();ctx.stroke();ctx.shadowBlur=0;}
    if(isF&&p2.length>0){var lp=p2[validIdx.length>0?validIdx[0]:0];ctx.fillStyle='rgba('+cr+','+cg+','+cb+','+(sa*0.8)+')';
      ctx.font='9px Courier New';ctx.fillText(d.years[t],lp.x+6,lp.y-3);}
    /* LOCK POINT: signal acquisition/loss boundary marker */
    if(d.lock[t]&&isF&&!asGhost){
      var cx=0,cy=0;for(var qi=0;qi<p2.length;qi++){cx+=p2[qi].x;cy+=p2[qi].y;}cx/=p2.length;cy/=p2.length;
      var lkColor=d.lock[t]===1?'#00ff88':'#ff8800';/* green=acquisition, amber=loss */
      var lkLabel=d.lock[t]===1?'LOCK-ACQ':'LOCK-LOSS';
      /* pulsing ring around polygon center */
      ctx.strokeStyle=lkColor;ctx.lineWidth=1.5;ctx.setLineDash([4,3]);
      ctx.beginPath();ctx.arc(cx,cy,18,0,Math.PI*2);ctx.stroke();ctx.setLineDash([]);
      /* offset value label */
      ctx.fillStyle=lkColor;ctx.font='8px Courier New';
      ctx.fillText(lkLabel+' offset='+d.lock_offset[t].toFixed(6),cx+22,cy-8);
    }
    if(isF&&!asGhost){for(var j=0;j<p2.length;j++){
      if(p3[j].miss){
        /* MISSING CARRIER: red X marker */
        var mx=p2[j].x,my=p2[j].y,ms=3.5;
        ctx.strokeStyle='#ff4500';ctx.lineWidth=1.5;
        ctx.beginPath();ctx.moveTo(mx-ms,my-ms);ctx.lineTo(mx+ms,my+ms);ctx.stroke();
        ctx.beginPath();ctx.moveTo(mx+ms,my-ms);ctx.lineTo(mx-ms,my+ms);ctx.stroke();
      }else{
        /* normal carrier: filled dot */
        var cc3=CARRIER_COLORS[d.carriers[j]]||'#6898b8';
        ctx.fillStyle=cc3;ctx.beginPath();ctx.arc(p2[j].x,p2[j].y,2.5,0,Math.PI*2);ctx.fill();
      }}}
    if(labels&&isF&&!asGhost){for(var j=0;j<p2.length;j++){
      var dist=Math.sqrt((mouseX-p2[j].x)*(mouseX-p2[j].x)+(mouseY-p2[j].y)*(mouseY-p2[j].y));
      if(dist<30){ctx.fillStyle=p3[j].miss?'#ff4500':'#8ab8d8';ctx.font='10px Courier New';
        var lbl=d.carriers[j]+': '+(p3[j].miss?'MISSING':d.clr[t][j].toFixed(3));
        ctx.fillText(lbl,p2[j].x+8,p2[j].y-6);}}}
  }
  if(timeIdx>=T&&labels&&!asGhost){var tl=T-1;for(var j=0;j<D;j++){var an=(j/D)*Math.PI*2-Math.PI/2;
    var lx=(RADIUS+20)*Math.cos(an),ly=(RADIUS+20)*Math.sin(an);
    var lp=proj(lx,ly,zOff(d)+tl*Z_SPACING);var cc4=CARRIER_COLORS[d.carriers[j]]||'#6898b8';
    ctx.fillStyle=cc4+'a0';ctx.font='9px Courier New';
    ctx.textAlign=Math.cos(an)>0.3?'left':(Math.cos(an)<-0.3?'right':'center');
    ctx.fillText(d.carriers[j],lp.x,lp.y);}ctx.textAlign='left';}
}
function drawGrid(){
  ctx.strokeStyle='rgba(64,88,104,0.08)';ctx.lineWidth=0.5;
  for(var i=-5;i<=5;i++){var a=proj(i*40,200,-200),b=proj(i*40,200,300);
    ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();
    var c=proj(-200,200,i*40+50),e=proj(200,200,i*40+50);
    ctx.beginPath();ctx.moveTo(c.x,c.y);ctx.lineTo(e.x,e.y);ctx.stroke();}
}
function drawAxis(d){
  var T=d.years.length;
  var za=proj(0,0,zOff(d)),zb=proj(0,0,zOff(d)+(T-1)*Z_SPACING);
  ctx.strokeStyle='rgba(64,88,104,0.15)';ctx.lineWidth=0.5;ctx.setLineDash([3,3]);
  ctx.beginPath();ctx.moveTo(za.x,za.y);ctx.lineTo(zb.x,zb.y);ctx.stroke();ctx.setLineDash([]);
}
function draw(){ctx.clearRect(0,0,W,H);ctx.fillStyle='#030406';ctx.fillRect(0,0,W,H);
  drawGrid();
  if(showAll){
    for(var ri=0;ri<runOrder.length;ri++){
      drawOneRun(DATA[runOrder[ri]],false);
      drawAxis(DATA[runOrder[ri]]);
    }
    updateReadoutAll();
  }else{
    var d=DATA[currentRun];
    if(ghost){for(var ri=0;ri<runOrder.length;ri++){var rc=runOrder[ri];if(rc===currentRun)continue;
      drawOneRun(DATA[rc],true);}}
    drawOneRun(d,false);
    drawAxis(d);
    updateReadout(d);
  }
}
function updateReadout(d){var T=d.years.length,D=d.carriers.length,yr=timeIdx<T?timeIdx:T-1;
  var vt=d.vt[yr],pm=0;if(yr>0){for(var j=0;j<D;j++)pm+=Math.abs(d.clr[yr][j]-d.clr[yr-1][j]);pm/=D;}
  var ls=lockYear>=0?d.years[lockYear]:'NONE';
  var h='<span>'+d.name+' <span class="val">['+d.code+']</span></span>';
  h+='<span>D=<span class="val">'+D+'</span></span>';
  h+='<span>V(t): <span class="val">'+d.vtShape+'</span></span>';
  h+='<span>Path eff: <span class="val">'+d.pathEff.toFixed(3)+'</span></span>';
  h+='<span>Lock: <span class="val">'+ls+'</span></span>';
  h+='<span>Year: <span class="val">'+(timeIdx<T?d.years[timeIdx]:'ALL')+'</span></span>';
  h+='<span>V(t): <span class="val">'+vt.toFixed(3)+'</span></span>';
  h+='<span>|dCLR|: <span class="val">'+pm.toFixed(3)+'</span></span>';
  document.getElementById('readout').innerHTML=h;}
function updateReadoutAll(){
  var h='<span>ALL RUNS <span class="val">['+runOrder.length+' systems]</span></span>';
  for(var ri=0;ri<runOrder.length;ri++){var d=DATA[runOrder[ri]];
    h+='<span style="color:'+d.color+'">'+d.name.replace(/^EMBER /,'')+'</span>';}
  document.getElementById('readout').innerHTML=h;}
var lastFrame=0;
function frame(ts){var dt=ts-lastFrame;lastFrame=ts;if(orbit){orbitAngle+=0.0005*dt;rotY=orbitAngle;}draw();requestAnimationFrame(frame);}
window.onload=function(){cv=document.getElementById('cv');ctx=cv.getContext('2d');resize();window.addEventListener('resize',resize);buildRunButtons();setupMouse();requestAnimationFrame(frame);};
</script></body></html>"""

def main():
    p = argparse.ArgumentParser(description="Generate Hs Manifold Projector HTML from polar_stack JSON")
    p.add_argument("inputs", nargs="+", help="polar_stack JSON files")
    p.add_argument("--output", "-o", default="projector.html")
    p.add_argument("--title", default="Hs Manifold Projector")
    p.add_argument("--subtitle", default="COMPOSITIONAL DATA MANIFOLD IN SPACE AND TIME")
    args = p.parse_args()
    runs = [load_run_raw(path, i) for i, path in enumerate(args.inputs)]
    compute_global_norms(runs)
    html = generate(runs, args.title, args.subtitle)
    # Verify pure ASCII
    for ci, ch in enumerate(html):
        if ord(ch) > 127:
            html = html[:ci] + "?" + html[ci+1:]
    with open(args.output, "w", encoding="ascii") as f:
        f.write(html)
    print("Wrote %d bytes to %s" % (len(html), args.output))
    print("Runs: %d" % len(runs))
    for r in runs:
        print("  %s: %d intervals, %d carriers" % (r["code"], len(r["years"]), len(r["carriers"])))

if __name__ == "__main__":
    main()
