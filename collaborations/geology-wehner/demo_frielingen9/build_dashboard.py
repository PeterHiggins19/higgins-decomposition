#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_dashboard.py -- regenerate the single-screen 16:9 dashboard.

Reads projector_data.json (produced by cnt_cnq_analysis.py) and writes
frielingen9_projector_16x9.html -- a self-contained, offline HTML viewer.
No third-party packages; Python stdlib only.   Run:  python build_dashboard.py
"""
import os, json
HERE=os.path.dirname(os.path.abspath(__file__))
DATA=json.load(open(os.path.join(HERE,"projector_data.json")))
TEMPLATE=r'''


<!DOCTYPE html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>Frielingen-9 mudstone — 16:9 dashboard (Hs/CNT/CNQ)</title>
<style>
:root{--ink:#3a372f;--acc:#6b1f2a;--si:#2a6b9a;--al:#3a8a3a;--rb:#caa000;--zr:#6b1f2a;--bg:#efe9df;--tile:#fff;--mut:#8a857c}
*{box-sizing:border-box;margin:0} html,body{height:100%;overflow:hidden;background:#d9d2c6;font-family:Helvetica,Arial,sans-serif;color:var(--ink)}
#fit{position:relative;width:100vw;height:100vh;overflow:hidden}
#stage{width:1600px;height:900px;position:absolute;left:50%;top:50%;background:var(--bg);transform-origin:center center}
.tile{position:absolute;background:var(--tile);border:1px solid #cfc7b8;border-radius:6px;overflow:hidden}
#hdr{left:8px;top:8px;width:1584px;height:60px;display:flex;align-items:center;gap:8px;padding:0 12px;flex-wrap:wrap;background:var(--tile)}
#hdr h1{font-size:15px;margin-right:6px} #hdr .s{font-size:10.5px;color:var(--acc)}
button{font:inherit;font-size:11px;border:1px solid var(--ink);background:#fff;color:var(--ink);border-radius:5px;padding:3px 7px;cursor:pointer}
button.on{background:var(--ink);color:#fff} b{font-size:11px}
.lab{position:absolute;top:3px;left:7px;font-size:10px;color:var(--acc);font-weight:bold;z-index:2}
#right{padding:20px 12px 8px;font-size:11px;overflow:hidden}
#stat{padding:20px 12px 8px;font-size:11px;overflow:hidden}
.kv{display:flex;justify-content:space-between;border-bottom:1px solid #f0ece4;padding:1.5px 0}
.kv b{font-variant-numeric:tabular-nums} .sw{display:inline-block;width:9px;height:9px;border-radius:2px;margin-right:4px}
h4{font-size:10px;color:var(--acc);margin:5px 0 2px} .cols{display:flex;gap:14px} .cols>div{flex:1}
.psbar{height:7px;background:#eee;border-radius:3px;overflow:hidden;display:inline-block;width:74px;vertical-align:middle}
.psbar>i{display:block;height:100%}
#tip{position:fixed;pointer-events:none;background:#222;color:#fff;font-size:10.5px;padding:5px 7px;border-radius:4px;opacity:0;white-space:pre;z-index:99;line-height:1.35}
.foot{position:absolute;bottom:3px;left:8px;font-size:9px;color:var(--mut)}
</style></head><body>
<div id=fit><div id=stage>
  <div class=tile id=hdr>
    <h1>Frielingen-9 mudstone &mdash; Hs/CNT/CNQ dashboard</h1>
    <span class=s>219 samples &middot; 15&ndash;250 m &middot; PANGAEA 897615</span>
    <span style="flex:1"></span>
    <b>view</b><button id=mRadar class=on>Radar</button><button id=mBary>Barycenter</button><button id=mShock>SHOCK</button>
    &nbsp;<b>depth</b><input id=sl type=range min=0 value=0 style="width:230px"><span id=dlab></span>
    <button id=play>&#9654;</button>
    &nbsp;<b>zoom</b><input id=zoom type=range min=1 max=40 value=10 style="width:110px"><span id=zlab>&times;1</span>
  </div>
  <div class=tile id=tlog style="left:8px;top:76px;width:476px;height:816px"><div class=lab>chemostratigraphic log</div><canvas id=clog width=474 height=792 style="position:absolute;top:18px;left:1px"></canvas></div>
  <div class=tile id=tmid style="left:492px;top:76px;width:516px;height:476px"><div class=lab id=midlab>radar — CLR deviation @ depth</div><canvas id=cmid width=514 height=452 style="position:absolute;top:20px;left:1px"></canvas></div>
  <div class=tile id=tscat style="left:492px;top:560px;width:516px;height:332px"><div class=lab>calibration: CNT step vs |&Delta;CaCO3|</div><canvas id=cscat width=514 height=306 style="position:absolute;top:20px;left:1px"></canvas></div>
  <div class=tile id=tright style="left:1016px;top:76px;width:576px;height:476px"><div class=lab>readout @ depth <span id=pdepth></span> m</div><div id=right></div></div>
  <div class=tile id=tstat style="left:1016px;top:560px;width:576px;height:332px"><div class=lab>summary — whole core</div><div id=stat></div></div>
</div></div>
<div id=tip></div>
<script>
const DATA=__DATAJSON__;
const css=v=>getComputedStyle(document.documentElement).getPropertyValue(v);
const cols=[css('--si'),css('--al'),css('--rb'),css('--zr')];
const N=DATA.depth.length,$=id=>document.getElementById(id),tip=$('tip');
let mode='radar',shock=false,cur=0,playing=false,timer=null,gain=1.0; $('sl').max=N-1;
function clrOf(c){const l=c.map(Math.log);const m=l.reduce((a,b)=>a+b)/l.length;return l.map(v=>v-m);}
const siAl=[],zrRb=[],keff=[],CLR=[];let CLRMAX=0.001;
for(let i=0;i<N;i++){const c=DATA.comp[i];siAl.push(Math.log(c[0]/c[1]));zrRb.push(Math.log(c[3]/c[2]));keff.push(Math.exp(-c.reduce((a,v)=>a+v*Math.log(v),0)));const cl=clrOf(c);CLR.push(cl);for(const v of cl)CLRMAX=Math.max(CLRMAX,Math.abs(v));}
const ps=[null],act=[null];
for(let i=1;i<N;i++){const d=CLR[i].map((v,k)=>v-CLR[i-1][k]);const ss=d.reduce((a,v)=>a+v*v,0)||1;ps.push(d.map(v=>v*v/ss));act.push(d.map((v,k)=>{const r=DATA.comp[i-1][k];return r>0?(v*v/ss)/r:0;}));}
const ddflag=i=>i>0&&act[i]&&act[i].some((a,k)=>a>=3&&DATA.comp[i-1][k]>=1e-3);
function corr(a,b){const n=a.length,ma=a.reduce((x,y)=>x+y)/n,mb=b.reduce((x,y)=>x+y)/n;let s=0,p=0,q=0;for(let i=0;i<n;i++){s+=(a[i]-ma)*(b[i]-mb);p+=(a[i]-ma)**2;q+=(b[i]-mb)**2;}return s/Math.sqrt(p*q);}
const dCa=[],dTo=[],stp=[];for(let i=1;i<N;i++){dCa.push(Math.abs(DATA.caco3[i]-DATA.caco3[i-1]));dTo.push(Math.abs(DATA.toc[i]-DATA.toc[i-1]));stp.push(DATA.step[i]);}
const hc=[0,0,0,0];for(let i=0;i<N;i++)if(DATA.helm[i]>=0)hc[DATA.helm[i]]++;
let flips=0;for(let i=2;i<N;i++)if(DATA.helm[i]!==DATA.helm[i-1])flips++;
const directness=1-flips/(N-2),regCount=DATA.regime.reduce((a,b)=>a+b,0),rCa=corr(stp,dCa),rTo=corr(stp,dTo);
const topIdx=[...Array(N).keys()].slice(1).sort((a,b)=>DATA.step[b]-DATA.step[a]).slice(0,6);
const D0=DATA.depth[0],D1=DATA.depth[N-1];
function rng(a){return [Math.min(...a),Math.max(...a)];}
const TOPY=22;
function line(x,T,vals,color,BOT){const [a,b]=rng(vals);x.strokeStyle=color;x.lineWidth=1.1;x.beginPath();for(let i=0;i<N;i++){const px=T.x+(vals[i]-a)/((b-a)||1)*T.w,py=Y(DATA.depth[i],BOT);i?x.lineTo(px,py):x.moveTo(px,py);}x.stroke();}
function Y(d,BOT){return TOPY+(d-D0)/(D1-D0)*(BOT-TOPY);}
let tracks;
function drawLog(){const c=$('clog'),x=c.getContext('2d'),W=c.width,He=c.height,BOT=He-8;x.clearRect(0,0,W,He);
 tracks=[{x:38,w:96,t:"comp"},{x:140,w:78,t:"Si/Al·Zr/Rb"},{x:224,w:78,t:"CaCO3·TOC"},{x:308,w:64,t:"CNT step"},{x:378,w:30,t:"helm"},{x:414,w:56,t:"CNQ r"}];
 x.font='8.5px sans-serif';for(const T of tracks){x.fillStyle='#666';x.fillText(T.t,T.x,10);x.strokeStyle='#eee';x.strokeRect(T.x,TOPY,T.w,BOT-TOPY);}
 x.fillStyle='#999';for(let d=Math.ceil(D0/25)*25;d<D1;d+=25){const y=Y(d,BOT);x.fillText(d,2,y+3);x.strokeStyle='#f1efe9';x.beginPath();x.moveTo(34,y);x.lineTo(W-2,y);x.stroke();}
 const T1=tracks[0];for(let i=0;i<N;i++){const y=Y(DATA.depth[i],BOT),y2=(i<N-1)?Y(DATA.depth[i+1],BOT):y+2;let xx=T1.x;for(let k=0;k<4;k++){const seg=DATA.comp[i][k]*T1.w;x.fillStyle=cols[k];x.fillRect(xx,y,seg,Math.max(1.1,y2-y));xx+=seg;}}
 line(x,tracks[1],siAl,'#3a372f',BOT);line(x,tracks[1],zrRb,'#caa000',BOT);
 line(x,tracks[2],DATA.toc,'#2a6b9a',BOT);
 const T3=tracks[2],[c0,c1]=rng(DATA.caco3);x.lineJoin='round';x.beginPath();for(let i=0;i<N;i++){const px=T3.x+(DATA.caco3[i]-c0)/(c1-c0)*T3.w,py=Y(DATA.depth[i],BOT);i?x.lineTo(px,py):x.moveTo(px,py);}x.strokeStyle='rgba(18,16,12,.9)';x.lineWidth=3;x.stroke();x.strokeStyle='#fff';x.lineWidth=1.3;x.stroke();x.lineWidth=1;
 const T4=tracks[3],sm=Math.max(...DATA.step);x.fillStyle='rgba(58,55,47,.32)';x.beginPath();x.moveTo(T4.x,Y(D0,BOT));for(let i=0;i<N;i++)x.lineTo(T4.x+DATA.step[i]/sm*T4.w,Y(DATA.depth[i],BOT));x.lineTo(T4.x,Y(D1,BOT));x.fill();
 for(let i=0;i<N;i++)if(DATA.regime[i]){x.fillStyle='#6b1f2a';x.fillRect(T4.x,Y(DATA.depth[i],BOT)-1,T4.w,1.8);}
 const T5=tracks[4];for(let i=1;i<N;i++){const k=DATA.helm[i];if(k<0)continue;const y=Y(DATA.depth[i],BOT);x.fillStyle=cols[k];x.fillRect(T5.x+(k/3)*(T5.w-9),y-1,9,2.4);}
 for(let i=0;i<N;i++)if(ddflag(i)){x.fillStyle='#000';const y=Y(DATA.depth[i],BOT);x.beginPath();x.moveTo(T5.x-7,y-3);x.lineTo(T5.x-2,y);x.lineTo(T5.x-7,y+3);x.fill();}
 line(x,tracks[5],DATA.radial,'#6b1f2a',BOT);
 const yc=Y(DATA.depth[cur],BOT);x.strokeStyle='#000';x.lineWidth=1.3;x.beginPath();x.moveTo(30,yc);x.lineTo(W-2,yc);x.stroke();x.lineWidth=1;x.fillStyle='#000';x.beginPath();x.moveTo(30,yc-4);x.lineTo(36,yc);x.lineTo(30,yc+4);x.fill();
}
function drawRadar(){const c=$('cmid'),x=c.getContext('2d'),W=c.width,He=c.height;x.clearRect(0,0,W,He);$('midlab').textContent='radar — CLR deviation @ depth (zoom ×'+gain.toFixed(1)+')';
 const cx=W/2,cy=He/2,Rr=Math.min(W,He)*0.38;const clr=CLR[cur];
 x.strokeStyle='#eee';for(let g=1;g<=4;g++){x.beginPath();for(let k=0;k<=4;k++){const a=-Math.PI/2+k/4*2*Math.PI,rr=Rr*g/4;const px=cx+rr*Math.cos(a),py=cy+rr*Math.sin(a);k?x.lineTo(px,py):x.moveTo(px,py);}x.closePath();x.stroke();}
 x.strokeStyle='#c9b8bc';x.setLineDash([4,3]);x.beginPath();x.arc(cx,cy,Rr*0.5,0,7);x.stroke();x.setLineDash([]);
 const rad=k=>Rr*Math.max(0.05,Math.min(1,0.5+gain*0.42*clr[k]/CLRMAX));
 x.beginPath();for(let k=0;k<4;k++){const a=-Math.PI/2+k/4*2*Math.PI,rr=rad(k);const px=cx+rr*Math.cos(a),py=cy+rr*Math.sin(a);k?x.lineTo(px,py):x.moveTo(px,py);}x.closePath();x.fillStyle='rgba(107,31,42,.12)';x.fill();x.strokeStyle='#6b1f2a';x.lineWidth=2;x.stroke();
 for(let k=0;k<4;k++){const a=-Math.PI/2+k/4*2*Math.PI,rr=rad(k);x.fillStyle=cols[k];x.beginPath();x.arc(cx+rr*Math.cos(a),cy+rr*Math.sin(a),4.5,0,7);x.fill();x.fillStyle='#3a372f';x.textAlign='center';x.font='12px sans-serif';x.fillText(DATA.names[k],cx+(Rr+15)*Math.cos(a),cy+(Rr+17)*Math.sin(a));}x.textAlign='left';
}
function drawBary(){const c=$('cmid'),x=c.getContext('2d'),W=c.width,He=c.height;x.clearRect(0,0,W,He);$('midlab').textContent='barycenter trajectory (ILR-PCA)'+(shock?' + SHOCK':'');
 const xs=DATA.bary.map(p=>p[0]),ys=DATA.bary.map(p=>p[1]);const x0=Math.min(...xs),x1=Math.max(...xs),y0=Math.min(...ys),y1=Math.max(...ys),pad=34;
 const PX=v=>pad+(v-x0)/(x1-x0)*(W-2*pad),PY=v=>He-pad-(v-y0)/(y1-y0)*(He-2*pad);x.strokeStyle='#eee';x.strokeRect(pad,pad,W-2*pad,He-2*pad);
 for(let i=1;i<=cur;i++){const a=DATA.bary[i-1],b=DATA.bary[i];if(shock){const t=Math.min(1,DATA.step[i]/(DATA.stepmax*0.8));x.strokeStyle='rgb('+Math.round(110+90*t)+','+Math.round(110-80*t)+','+Math.round(110-70*t)+')';x.lineWidth=1+2.6*t;}else{x.strokeStyle='rgba(58,55,47,.5)';x.lineWidth=1.1;}x.beginPath();x.moveTo(PX(a[0]),PY(a[1]));x.lineTo(PX(b[0]),PY(b[1]));x.stroke();}
 for(let i=0;i<=cur;i++)if(DATA.regime[i]){x.fillStyle='#6b1f2a';x.beginPath();x.arc(PX(DATA.bary[i][0]),PY(DATA.bary[i][1]),3,0,7);x.fill();}
 const p=DATA.bary[cur];x.fillStyle='#caa000';x.strokeStyle='#3a372f';x.lineWidth=1.5;x.beginPath();x.arc(PX(p[0]),PY(p[1]),6,0,7);x.fill();x.stroke();
}
function drawScat(){const c=$('cscat'),x=c.getContext('2d'),W=c.width,He=c.height,pad=34;x.clearRect(0,0,W,He);
 const [a,b]=rng(dCa),sm=Math.max(...stp);const PX=v=>pad+v/(b||1)*(W-pad-12),PY=v=>He-22-v/sm*(He-38);
 x.strokeStyle='#eee';x.strokeRect(pad,6,W-pad-12,He-28);x.fillStyle='#8a857c';x.font='10px sans-serif';x.fillText('|ΔCaCO3| →   r='+rCa.toFixed(2),W-150,He-6);x.save();x.translate(11,He/2+20);x.rotate(-Math.PI/2);x.fillText('CNT step',0,0);x.restore();
 for(let i=1;i<N;i++){x.fillStyle=(i===cur)?'#caa000':'rgba(42,107,154,.45)';x.beginPath();x.arc(PX(dCa[i-1]),PY(stp[i-1]),i===cur?5.5:2.6,0,7);x.fill();}
}
function draw(){drawLog();(mode==='bary'?drawBary():drawRadar());drawScat();panel();}
function bar(k,v){return '<span class=psbar><i style="width:'+Math.round(v*100)+'%;background:'+cols[k]+'"></i></span>';}
function panel(){const i=cur;$('pdepth').textContent=DATA.depth[i].toFixed(2);$('dlab').textContent=' '+DATA.depth[i].toFixed(1)+'m';
 const c=DATA.comp[i],rw=DATA.raw[i],un=DATA.units;let L='';for(let k=0;k<4;k++){const p=c[k]*100,rv=un[k]==='%'?rw[k].toFixed(1):Math.round(rw[k]);L+='<div class=kv><span><span class=sw style="background:'+cols[k]+'"></span>'+DATA.names[k]+'</span><b>'+rv+' '+un[k]+' <small style=color:#bbb>'+(p<0.1?p.toFixed(3):p.toFixed(1))+'% &middot; clr '+CLR[i][k].toFixed(2)+'</small></b></div>';}
 let P='<h4>power share &amp; activation α <small style=color:#999>(*below 0.1% share guard)</small></h4>';if(i>0)for(let k=0;k<4;k++){const av=act[i][k],bg=DATA.comp[i-1][k]<1e-3,as=av<10?av.toFixed(1):Math.round(av);P+='<div class=kv><span>'+DATA.names[k]+' '+bar(k,ps[i][k])+'</span><b'+(bg?' style=color:#b8860b':'')+'>α '+as+(bg?'*':'')+'</b></div>';}
 const R='<h4>diagnostic ratios</h4><div class=kv><span>log Si/Al</span><b>'+siAl[i].toFixed(3)+'</b></div><div class=kv><span>log Zr/Rb</span><b>'+zrRb[i].toFixed(3)+'</b></div>'+
  '<h4>independent calibration</h4><div class=kv><span>CaCO3 %</span><b>'+DATA.caco3[i].toFixed(1)+'</b></div><div class=kv><span>TOC %</span><b>'+DATA.toc[i].toFixed(2)+'</b></div>'+
  '<h4>CNT / CNQ</h4><div class=kv><span>Aitchison step</span><b>'+DATA.step[i].toFixed(3)+'</b></div><div class=kv><span>helmsman</span><b>'+(DATA.helm[i]<0?'—':DATA.names[DATA.helm[i]])+(ddflag(i)?' ▼dd':'')+'</b></div>'+
  '<div class=kv><span>K_eff</span><b>'+keff[i].toFixed(3)+'</b></div><div class=kv><span>regime?</span><b>'+(DATA.regime[i]?'YES':'no')+'</b></div><div class=kv><span>CNQ radial</span><b>'+DATA.radial[i].toFixed(3)+'</b></div>';
 $('right').innerHTML='<div class=cols><div>'+L+R+'</div><div>'+P+'</div></div>';
}
$('stat').innerHTML=
 '<div class=kv><span>samples / range</span><b>'+N+' / '+D0+'–'+D1+' m</b></div>'+
 '<div class=kv><span>helmsman (driver)</span><b>Zr '+hc[3]+' · Rb '+hc[2]+' · Al '+hc[1]+' · Si '+hc[0]+'</b></div>'+
 '<div class=kv><span>flips / directness</span><b>'+flips+' / '+directness.toFixed(2)+'</b></div>'+
 '<div class=kv><span>regime surfaces</span><b>'+regCount+'</b></div>'+
 '<div class=kv><span>r(step,|ΔCaCO3|) / r(step,|ΔTOC|)</span><b>'+rCa.toFixed(2)+' / '+rTo.toFixed(2)+'</b></div>'+
 '<h4>biggest compositional steps (click to jump)</h4><div class=cols><div>'+
 topIdx.slice(0,3).map(i=>'<div class=kv data-i="'+i+'" style="cursor:pointer"><span>'+DATA.depth[i].toFixed(1)+' m</span><b>'+DATA.step[i].toFixed(2)+'·'+DATA.names[DATA.helm[i]]+'</b></div>').join('')+
 '</div><div>'+topIdx.slice(3).map(i=>'<div class=kv data-i="'+i+'" style="cursor:pointer"><span>'+DATA.depth[i].toFixed(1)+' m</span><b>'+DATA.step[i].toFixed(2)+'·'+DATA.names[DATA.helm[i]]+'</b></div>').join('')+'</div></div>';
function setMode(m){mode=m;$('mRadar').classList.toggle('on',m==='radar');$('mBary').classList.toggle('on',m==='bary');draw();}
$('mRadar').onclick=()=>setMode('radar');$('mBary').onclick=()=>setMode('bary');
$('mShock').onclick=function(){shock=!shock;this.classList.toggle('on',shock);if(mode!=='bary')setMode('bary');else draw();};
$('sl').oninput=function(){cur=+this.value;draw();};
$('zoom').oninput=function(){gain=(+this.value)/10;$('zlab').innerHTML='&times;'+gain.toFixed(1);draw();};
$('play').onclick=function(){playing=!playing;this.innerHTML=playing?'&#10073;&#10073;':'&#9654;';if(playing){timer=setInterval(()=>{cur=(cur+1)%N;$('sl').value=cur;draw();},90);}else clearInterval(timer);};
document.addEventListener('click',e=>{const t=e.target.closest('[data-i]');if(t){cur=+t.dataset.i;$('sl').value=cur;draw();}});
const cl=$('clog');
cl.addEventListener('mousemove',e=>{const r=cl.getBoundingClientRect();const sy=cl.height/r.height;const ly=(e.clientY-r.top)*sy;const BOT=cl.height-8;let d=D0+(ly-TOPY)/(BOT-TOPY)*(D1-D0),best=0,bd=1e9;for(let i=0;i<N;i++){const q=Math.abs(DATA.depth[i]-d);if(q<bd){bd=q;best=i;}}cur=best;$('sl').value=cur;draw();
 tip.style.opacity=1;tip.style.left=(e.clientX+12)+'px';tip.style.top=(e.clientY+8)+'px';tip.textContent=DATA.depth[best].toFixed(2)+' m\nstep '+DATA.step[best].toFixed(3)+'  helm '+(DATA.helm[best]<0?'—':DATA.names[DATA.helm[best]])+'\nCaCO3 '+DATA.caco3[best].toFixed(1)+'%  TOC '+DATA.toc[best].toFixed(2)+'%'+'\nRb '+DATA.raw[best][2]+'  Zr '+DATA.raw[best][3]+' mg/kg';});
cl.addEventListener('mouseleave',()=>tip.style.opacity=0);
function fit(){const s=Math.min(window.innerWidth/1600,window.innerHeight/900);$('stage').style.transform='translate(-50%,-50%) scale('+s+')';}
window.addEventListener('resize',fit);fit();draw();
</script></body></html>


'''
open(os.path.join(HERE,"frielingen9_projector_16x9.html"),"w",encoding="utf-8").write(TEMPLATE.replace("__DATAJSON__",json.dumps(DATA)))
print("wrote frielingen9_projector_16x9.html")
