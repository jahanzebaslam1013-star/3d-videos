// "He Sued Time" — loop short. Last frame of the final shot == first frame of shot 0.
import {THREE,camera,cam,loadTiming,run,clamp,ease,eout,back,lerp,V,box,cyl,grp,mat,lights,makeMan,flail,paintTex,textTex,
  canvasTex,label,skyScene,cloud,beachWorld,lounger,palm,room,pajamaMan,setSeed,rnd,sunDisc} from './engine.js';
const T=await loadTiming(); const T0=0.05;
const L=i=>T[i].start+T0, E=i=>T[i].end+T0;
const wordT=(i,w)=>{const x=T[i].words.find(q=>q.w.toLowerCase().replace(/[^a-z0-9]/g,'').startsWith(w));return (x?x.start:T[i].start)+T0};
const shots=[];const LOOK=[];const face=(o,rz=0)=>LOOK.push([o,rz]);
const shot=(start,build)=>shots.push({start,build:()=>{const I=build();const u=I.u;I.u=t=>{LOOK.length=0;u(t);for(const [o,rz] of LOOK){o.lookAt(camera.position);if(rz)o.rotateZ(rz)}};return I}});
const END=E(T.length-1)+0.07;
const PI=Math.PI;
const shake=(t,t0,a=.12,d=.25)=>{const k=t-t0;if(k<0||k>d)return 0;return Math.sin(k*90)*a*(1-k/d)};
const pop=(t,t0,d=.25)=>t<t0?0:back((t-t0)/d);

// ---------- textures ----------
function clockTex(){return canvasTex(512,512,(g,w,h,ang,mood='grumpy')=>{
  g.clearRect(0,0,w,h);g.fillStyle='#5a3a1e';g.beginPath();g.arc(256,256,252,0,7);g.fill();
  g.fillStyle='#fbf6e8';g.beginPath();g.arc(256,256,222,0,7);g.fill();
  g.fillStyle='#2a1d12';for(let i=0;i<12;i++){const a=i/12*PI*2;g.save();g.translate(256+Math.sin(a)*195,256-Math.cos(a)*195);g.rotate(a);g.fillRect(-5,-16,10,32);g.restore()}
  if(mood){for(const s of[-1,1]){const ex=256+s*62,ey=300;g.fillStyle='#fff';g.strokeStyle='#2a1d12';g.lineWidth=6;g.beginPath();g.ellipse(ex,ey,34,40,0,0,7);g.fill();g.stroke();
      g.fillStyle='#111';g.beginPath();g.arc(ex,ey+(mood==='grumpy'?10:4),17,0,7);g.fill();
      g.strokeStyle='#2a1d12';g.lineWidth=14;g.lineCap='round';g.beginPath();
      if(mood==='grumpy'){g.moveTo(ex-s*40,ey-62);g.lineTo(ex+s*30,ey-42)}else{g.moveTo(ex-30,ey-58);g.lineTo(ex+30,ey-58)}g.stroke()}
    g.strokeStyle='#2a1d12';g.lineWidth=10;g.beginPath();if(mood==='grumpy'){g.arc(256,410,40,PI*1.15,PI*1.85)}else{g.moveTo(226,395);g.lineTo(286,395)}g.stroke()}
  const hand=(a,len,wd,col)=>{g.save();g.translate(256,256);g.rotate(a);g.fillStyle=col;g.fillRect(-wd/2,-len,wd,len+18);g.restore()};
  hand(ang/12,110,16,'#2a1d12');hand(ang,175,10,'#2a1d12');g.fillStyle='#d23a2a';g.beginPath();g.arc(256,256,14,0,7);g.fill()})}
function wallClock(p,r,mood='grumpy'){const g=grp(p);const ct=clockTex();ct.draw(0,mood);
  cyl(g,r*1.02,r*1.02,.12,0x4a2e16,0,0,-.07,24).rotation.x=PI/2;
  const f=new THREE.Mesh(new THREE.CircleGeometry(r,48),new THREE.MeshBasicMaterial({map:ct.tex,transparent:true}));f.position.z=.0;g.add(f);
  g.userData={ct,mood};g.set=(a,m)=>ct.draw(a,m??mood);return g}
const PAPER='#fbf8ef';
function folder(p,w=1.15,h=.85,t=.2){const g=grp(p);box(g,w,h,t,0xd9a94e,0,0,0);box(g,w-.08,h-.1,t+.02,0xfbf8ef,.0,-.03,0);box(g,w*.3,.1,t+.04,0xd9a94e,-w*.3,h/2+.03,0);
  const lb=label(g,'',w*.9,h*.62,{});lb.material.map=canvasTexOnce(512,350,(c,W,H)=>{c.fillStyle='#d9a94e';c.fillRect(0,0,W,H);c.fillStyle='#fff7e0';c.fillRect(18,18,W-36,H-36);
    c.textAlign='center';c.fillStyle='#d23a2a';c.font='900 92px M';c.fillText('LAWSUIT',W/2,140);c.fillStyle='#1b2330';c.font='900 66px M';c.fillText('ME vs. TIME',W/2,250)});
  lb.position.z=t/2+.025;return g}
function canvasTexOnce(w,h,draw){const c=canvasTex(w,h,draw);c.draw();return c.tex}
function stamp(p,txt,w=1.2,col='#d23a2a'){const m=label(p,'',w,w*.38,{});m.material.map=canvasTexOnce(512,196,(g,W,H)=>{g.strokeStyle=col;g.lineWidth=16;g.strokeRect(10,10,W-20,H-20);
  g.fillStyle=col;g.font='900 116px M';g.textAlign='center';g.textBaseline='middle';g.fillText(txt,W/2,H/2+6)});return m}
function sign(p,txt,w,col='#d23a2a',fg='#fff',fs=110){const m=label(p,'',w,w*.36,{});m.material.map=canvasTexOnce(560,200,(g,W,H)=>{g.fillStyle=col;g.beginPath();g.roundRect(6,6,W-12,H-12,36);g.fill();
  g.strokeStyle='#fff';g.lineWidth=8;g.beginPath();g.roundRect(16,16,W-32,H-32,28);g.stroke();g.fillStyle=fg;g.font=`900 ${fs}px M`;g.textAlign='center';g.textBaseline='middle';g.fillText(txt,W/2,H/2+6)});return m}
function bub(p,lines,w=2,fs=84){const m=label(p,'',w,w*.62,{});m.material.map=canvasTexOnce(560,348,(g,W,H)=>{g.fillStyle='#fff';g.strokeStyle='#111';g.lineWidth=8;
  g.beginPath();g.roundRect(10,10,W-20,H-90,60);g.fill();g.stroke();g.beginPath();g.moveTo(150,H-84);g.lineTo(110,H-12);g.lineTo(230,H-84);g.closePath();g.fill();g.stroke();
  g.fillStyle='#fff';g.fillRect(150,H-92,80,14);g.fillStyle='#111';g.font=`900 ${fs}px M`;g.textAlign='center';g.textBaseline='middle';
  lines.forEach((l,i)=>g.fillText(l,W/2,(H-80)/2+(i-(lines.length-1)/2)*fs*1.05+4))});return m}
function contractTex(){let last=-1;return canvasTex(600,780,(g,w,h,n)=>{if(n===last)return;last=n;
  g.fillStyle=PAPER;g.fillRect(0,0,w,h);g.fillStyle='#1b2330';g.font='900 66px M';g.textAlign='center';g.fillText('SETTLEMENT',w/2,96);
  g.font='700 34px M';g.fillStyle='#666';g.fillText('Plaintiff vs. TIME',w/2,146);g.fillStyle='#ccc';g.fillRect(50,172,w-100,4);
  g.textAlign='left';
  if(n>=1){g.fillStyle='#1f8a3a';g.font='900 46px M';g.fillText('1. SUNDAYS =',50,262);g.fillText('    48 HOURS ✓',50,322)}
  if(n>=2){g.fillStyle='#d23a2a';g.font='900 46px M';g.fillText('2. MONDAYS START',50,430);g.fillText('    2x EARLIER',50,490)}
  g.fillStyle='rgba(0,0,0,.18)';for(let y=560;y<640;y+=28)g.fillRect(50,y,w-100-(y*7%120),8);
  g.fillStyle='#111';g.font='700 40px M';g.fillText('X',50,724);g.fillRect(90,716,300,4)})}
function haloTex(col){const c=document.createElement('canvas');c.width=c.height=256;const g=c.getContext('2d');const r=g.createRadialGradient(128,128,0,128,128,128);
  r.addColorStop(0,col);r.addColorStop(1,'rgba(0,0,0,0)');g.fillStyle=r;g.fillRect(0,0,256,256);const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;return t}

// ---------- characters ----------
function judgeMan(p){const m=makeMan(p,{suit:0x15161c});const w=0xf2f0ea;
  box(m.head,.36,.14,.36,w,0,.48,-.01);for(const s of[-1,1])for(const y of[.38,.26,.14])box(m.head,.09,.1,.3,w,s*.19,y,-.03);box(m.head,.3,.36,.1,w,0,.22,-.2);
  box(m.torso,.62,.74,.34,0x0c0d12,0,.37,0);box(m.torso,.12,.1,.02,0xffffff,0,.7,.175);
  const gv=grp(m.arms[0].el,0,-.42,0);cyl(gv,.035,.035,.55,0x5a3418,0,0,-.22,8).rotation.x=PI/2;const hd=cyl(gv,.09,.09,.3,0x4a2a12,0,0,-.5,12);hd.rotation.z=PI/2;
  m.face('neutral');m.gavel=gv;return m}
function fatherTime(p){const g=grp(p);const robeM=new THREE.MeshLambertMaterial({color:0x6c5bb8,emissive:0x2c2170,flatShading:true});
  const robe=new THREE.Mesh(new THREE.ConeGeometry(.78,2.1,10),robeM);robe.position.y=1.05;robe.castShadow=true;g.add(robe);
  const hood=new THREE.Mesh(new THREE.SphereGeometry(.44,12,10),robeM);hood.position.set(0,2.2,-.04);hood.scale.set(1,1.12,1);g.add(hood);
  const skin=mat(0xebc9a6);box(g,.44,.42,.12,skin,0,2.18,.33);
  const beard=new THREE.Mesh(new THREE.ConeGeometry(.27,.9,8),mat(0xf6f6f2));beard.rotation.x=PI;beard.position.set(0,1.62,.36);g.add(beard);
  box(g,.4,.1,.12,0xf6f6f2,0,2.04,.38);for(const s of[-1,1]){box(g,.13,.035,.02,0x1d1b22,s*.1,2.24,.4);box(g,.14,.05,.03,0xf6f6f2,s*.1,2.33,.4).rotation.z=-s*.15}
  const arm=grp(g,.42,1.55,.1);const sl=cyl(arm,.12,.16,.6,robeM,0,-.2,.15,8);sl.rotation.x=1.2;
  const hg=grp(arm,0,-.35,.5);const gold=mat(0xe0b33a);cyl(hg,.15,.15,.04,gold,0,.22,0,10);cyl(hg,.15,.15,.04,gold,0,-.22,0,10);
  const gl=new THREE.MeshLambertMaterial({color:0xdff3ff,transparent:true,opacity:.55});
  const c1=new THREE.Mesh(new THREE.ConeGeometry(.13,.2,10),gl);c1.position.y=.1;c1.rotation.x=PI;hg.add(c1);const c2=new THREE.Mesh(new THREE.ConeGeometry(.13,.2,10),gl);c2.position.y=-.1;hg.add(c2);
  const sand=new THREE.Mesh(new THREE.ConeGeometry(.09,.1,10),mat(0xe8c070));sand.position.y=-.15;hg.add(sand);
  for(const x of[-.12,.12])cyl(hg,.015,.015,.44,gold,x,0,0,5);
  const halo=new THREE.Mesh(new THREE.PlaneGeometry(4,4.6),new THREE.MeshBasicMaterial({map:haloTex('rgba(190,170,255,.65)'),transparent:true,depthWrite:false}));halo.position.set(0,1.3,-.7);g.add(halo);
  g.userData={arm,hg};return g}

// ---------- courtroom ----------
function court({judge=false,man=true}={}){const s=new THREE.Scene();s.background=new THREE.Color(0x5e3f26);setSeed(9);
  const fl=new THREE.Mesh(new THREE.PlaneGeometry(30,30),new THREE.MeshLambertMaterial({map:paintTex('#8a5a36',512,512,900,14,6,[30,120])}));fl.rotation.x=-PI/2;fl.receiveShadow=true;s.add(fl);
  const rug=new THREE.Mesh(new THREE.PlaneGeometry(2.4,9),mat(0x8e2a2a));rug.rotation.x=-PI/2;rug.position.set(0,.01,-2.5);rug.receiveShadow=true;s.add(rug);
  const panel=new THREE.MeshLambertMaterial({map:paintTex('#7a5232',512,512,900,12,3)});
  const bw=new THREE.Mesh(new THREE.PlaneGeometry(20,10),panel);bw.position.set(0,5,7);bw.rotation.y=PI;bw.receiveShadow=true;s.add(bw);
  for(let i=-4;i<=4;i++)box(s,.12,4.2,.1,0x5a3a20,i*1.3,2.1,6.92);box(s,14,.18,.14,0x4a2e16,0,4.25,6.9);
  const fw=new THREE.Mesh(new THREE.PlaneGeometry(20,10),new THREE.MeshLambertMaterial({map:paintTex('#b49a78',512,512,900,12,3)}));fw.position.set(0,5,-7);fw.receiveShadow=true;s.add(fw);
  for(const sx of[-1,1]){box(s,1.3,2.9,.12,0x5b3b22,sx*.68,1.45,-6.92);box(s,.5,.7,.13,0xbfd8e8,sx*.68,2.0,-6.9);box(s,.08,.3,.15,0xd9b44a,sx*.18,1.4,-6.88)}
  box(s,2.8,.2,.15,0x4a2e16,0,2.98,-6.9);
  for(const sx of[-1,1]){const sw=new THREE.Mesh(new THREE.PlaneGeometry(14,10),new THREE.MeshLambertMaterial({map:paintTex('#a88a66',512,512,700,12,3)}));sw.position.set(sx*6,5,0);sw.rotation.y=-sx*PI/2;s.add(sw)}
  for(const z of[-2.3,-3.6,-4.9])for(const sx of[-1,1]){box(s,3.2,.12,.6,0x6e4426,sx*2.9,.5,z);box(s,3.2,.7,.1,0x6e4426,sx*2.9,.85,z-.3);for(const x of[1.4,-1.4])box(s,.1,.5,.5,0x5a3418,sx*2.9+x,.25,z)}
  box(s,5.2,.9,.1,0x6e4426,0,.45,-1.2).visible=false;
  // judge bench (front face at z=3.0)
  const bench=grp(s,0,0,3.6);box(bench,4.4,1.7,1.2,0x6e4426,0,.85,0);box(bench,4.6,.1,1.4,0x4f2f18,0,1.75,0);
  for(const x of[-1.5,0,1.5])box(bench,1.2,1.1,.04,0x83532f,x,.85,-.61);
  box(s,3,.5,1.6,0x5a3418,0,.25,4.6);
  const stand=grp(s,-3.1,0,2.4);stand.rotation.y=.5;box(stand,1.3,1.15,1.1,0x6e4426,0,.575,0);box(stand,1.4,.08,1.2,0x4f2f18,0,1.17,0);
  box(stand,.6,.08,.6,0x3a2a1a,0,.6,.15);box(stand,.6,.8,.08,0x3a2a1a,0,1.0,.45);
  const plaque=label(stand,'',1.0,.24,{});plaque.material.map=canvasTexOnce(512,124,(g,W,H)=>{g.fillStyle='#d9b44a';g.fillRect(0,0,W,H);g.fillStyle='#2a1d12';g.font='900 64px M';g.textAlign='center';g.textBaseline='middle';g.fillText('WITNESS',W/2,H/2+4)});
  plaque.position.set(0,.85,-.565);plaque.rotation.y=PI;
  for(const sx of[-1,1]){const bn=grp(s,sx*3.4,0,6.85);box(bn,1.1,3.2,.05,0x24345e,0,3.0,0);box(bn,1.1,.14,.06,0xd9b44a,0,1.45,0);box(bn,.08,3.6,.08,0xd9b44a,0,2.9,.05)}
  const clock=wallClock(s,1.0);clock.position.set(0,5.4,6.85);clock.rotation.y=PI;
  const lamp=new THREE.PointLight(0xffe2b0,10,14,1.4);lamp.position.set(0,5,1);s.add(lamp);
  lights(s,{sky:0xfff1dc,ground:0x6b4a30,hemi:1.5,dir:1.7,pos:[4,12,-3],target:[0,1,2],sh:9});
  const R={s,bench,stand,clock};
  if(judge){const j=judgeMan(s);j.legs.rotation.x=PI/2;j.root.position.set(0,1.52,4.35);j.root.rotation.y=PI;R.judge=j}
  if(man){const m=makeMan(s);m.legs.rotation.x=PI/2;m.root.position.set(0,1.02,2.2);m.face('angry');R.man=m}
  return R}
// folder held in both hands overhead (arm angle a) relative to man at root position
function holdOverhead(m,f,a,{flat=0}={}){for(const ar of m.arms){ar.sh.rotation.x=a;ar.sh.rotation.z=ar.s*.18;ar.el.rotation.x=-.25}
  const Lr=.8,r=m.root.position;const y=r.y+.67-Lr*Math.cos(a),z=r.z-Lr*Math.sin(a);
  f.position.set(r.x,y+.25*(1-flat),z+.12+.15*flat);f.rotation.set(-flat*PI/2+(1-flat)*.15,0,0)}
// S0 / loop pose camera
const C0={fov:44,pos:[.25,2.9,6.1],look:[0,2.1,1.8]};

// ===== S0: "He sued Time." — slam (first frame == last frame of S14)
shot(0,()=>{const R=court();const {s,man}=R;const f=folder(s);const tS=wordT(0,'sued')-.02;
  return{s,u(t){const k=clamp((t-.02)/(tS-.02));const a=lerp(-2.7,-1.72,k*k);holdOverhead(man,f,a,{flat:k*k});
    if(t>tS){f.position.y=1.9;f.rotation.x=-PI/2;f.position.z=3.1}
    man.torso.rotation.x=lerp(0,.28,k*k);man.face('angry');const sk=shake(t,tS,.1);const e=ease(t/1.1);
    cam(C0.fov,[C0.pos[0]+sk,C0.pos[1]-e*.15+sk*.6,C0.pos[2]-e*.55],[C0.look[0],C0.look[1]-e*.05,C0.look[2]])}}});

// ===== S1: "Last Tuesday, a guy walked into the Supreme Court" — courthouse exterior
shot(L(1)-.05,()=>{const s=skyScene('#9fd6f0');lights(s,{sky:0xffffff,ground:0x9a8f80,hemi:1.5,dir:2.2,pos:[6,12,8],target:[0,1,-2],sh:12});
  const gr=new THREE.Mesh(new THREE.PlaneGeometry(200,200),new THREE.MeshLambertMaterial({map:paintTex('#cfc8b8',512,512,900,10,20,[10,40])}));gr.rotation.x=-PI/2;gr.receiveShadow=true;s.add(gr);
  const st=0xe9e4d8;const b=grp(s,0,0,-4);for(let i=0;i<5;i++)box(b,9-i*.25,.22,1.2+ (4-i)*.5,st,0,.11+i*.22,2.4-i*.25);
  box(b,8,.3,3,0xdcd6c8,0,1.25,0);for(let i=0;i<6;i++){cyl(b,.25,.28,3.2,0xf4f1ea,-3.2+i*1.28,2.95,1.1,12);box(b,.6,.15,.6,st,-3.2+i*1.28,4.6,1.1)}
  box(b,8.4,.7,2.8,0xe2dccf,0,5.0,.2);box(b,8,3.2,.3,0xcfc8b8,0,2.95,-.3);box(b,1.4,2.2,.1,0x5b3b22,0,2.2,-.12);
  const ped=new THREE.Mesh(new THREE.CylinderGeometry(4.9,4.9,2.6,3),mat(0xf4f1ea));ped.rotation.x=-PI/2;ped.scale.z=.32;ped.position.set(0,5.35+.79,.1);ped.castShadow=true;b.add(ped);
  const tl=label(b,'',6.2,.55,{});tl.material.map=textTex('SUPREME COURT',{w:1024,h:96,bg:'#e2dccf',fg:'#5a4a3a',font:'900 76px M'});tl.position.set(0,5.0,1.62);
  for(const x of[-8,9])cloud(s,x,9,-14,1.4);cloud(s,-2,11,-20,1.8);
  const tue=sign(s,'TUESDAY',1.7,'#2f86d8');
  const m=makeMan(s);m.legs.rotation.x=PI/2;m.face('angry');const f=folder(m.torso,1.0,.75,.18);f.position.set(-.42,.38,.15);f.rotation.set(0,PI/2,.1);
  const tw=wordT(1,'walked');
  return{s,u(t){const p=clamp(t/2.5);const x=lerp(-2.6,-.3,p),z=lerp(4.2,1.6,p);m.root.position.set(x,1.02+Math.abs(Math.sin(t*9))*.07,z);m.root.rotation.y=PI+.75;m.root.rotation.z=Math.sin(t*9)*.05;
    m.arms[0].sh.rotation.x=0;m.arms[1].sh.rotation.x=Math.sin(t*9)*.6;m.legs.rotation.x=PI/2;
    tue.position.set(.2,4.3,2.2);tue.scale.setScalar(pop(t,.05));face(tue);tue.visible=t<tw-L(1)+.9;
    const e=ease(t/2.5);cam(46,[lerp(3.6,3.0,e),lerp(2.0,2.3,e),lerp(8.8,7.8,e)],[lerp(-.4,0,e),2.5,-1])}}});

// ===== S2: "and officially filed a lawsuit against Time." — folder on bench, FILED stamp
shot(wordT(1,'and')-.05,()=>{const R=court();const {s,man}=R;const f=folder(s);f.position.set(0,1.9,3.1);f.rotation.x=-PI/2;
  holdOverhead(man,new THREE.Object3D(),-1.72,{flat:1});man.torso.rotation.x=.28;
  const st=stamp(s,'FILED',1.0);st.rotation.x=-PI/2;st.rotation.z=.25;const t0=wordT(1,'filed')-(wordT(1,'and')-.05);
  const tt=wordT(1,'time')-(wordT(1,'and')-.05);const vs=sign(s,'vs. TIME',1.2,'#1b2330');
  return{s,u(t){st.visible=t>t0;const k=clamp((t-t0)/.12);st.position.set(.18,lerp(2.6,2.03,k),3.15);st.scale.setScalar(lerp(1.6,1,k));
    man.face(t>tt?'angry':'angry');vs.visible=t>tt;vs.scale.setScalar(pop(t,tt));vs.position.set(.2,2.75,3.1);face(vs);
    const sk=shake(t,t0,.06);const e=ease(t/2.4);cam(42,[.3+sk,lerp(4.0,3.8,e),lerp(5.6,5.2,e)],[.05,2.0,2.6])}}});

// ===== S3: "His claim? Fraud and unfair business practices."
shot(L(2)-.05,()=>{const R=court({judge:true});const {s,man,judge,clock}=R;man.root.position.set(.5,1.02,1.2);man.root.rotation.y=-.35;
  const fr=sign(s,'FRAUD!',1.7),un=sign(s,'UNFAIR!',1.7,'#1b2330');const t0=L(2)-.05,tf=wordT(2,'fraud')-t0,tu=wordT(2,'unfair')-t0;
  return{s,u(t){const a=clamp((t-.2)/.4);man.arms[1].sh.rotation.x=lerp(0,-2.35,eout(a));man.arms[1].sh.rotation.z=-.2;man.arms[0].sh.rotation.z=.3;man.face('angry');
    man.root.position.y=1.02+(t>tf&&t<tf+.3?Math.sin((t-tf)*30)*.03:0);
    clock.set(t*.8+1.2,'grumpy');judge.face('neutral');
    for(const [sg,t1,x,y,rz] of [[fr,tf,-1.0,5.9,.12],[un,tu,1.05,4.7,-.1]]){sg.visible=t>t1;sg.scale.setScalar(pop(t,t1));sg.position.set(x,y,6.2);face(sg,rz)}
    const sk=shake(t,tf,.05)+shake(t,tu,.05);const e=ease(t/2.8);cam(46,[lerp(1.9,1.5,e)+sk,lerp(2.2,2.5,e),lerp(-3.6,-2.6,e)],[0,3.7,5])}}});

// ===== S4: "Exhibit A: work hours feel like forty days," — office, clock ticking backwards
shot(L(3)-.05,()=>{const s=room();const desk=grp(s,0,0,.2);box(desk,2.4,.1,1.1,0x9a6a3c,0,.95,0);for(const x of[-1.1,1.1])box(desk,.1,.95,1.0,0x7a5230,x,.475,0);
  const mon=grp(desk,-.75,0,-.1);mon.rotation.y=.6;box(mon,.8,.55,.06,0x2b2f38,0,1.32,0);box(mon,.74,.48,.01,0x3a7bd5,0,1.32,.035);box(mon,.2,.25,.12,0x2b2f38,0,1.06,0);
  for(let i=0;i<6;i++)box(desk,.5,.04,.65,i%2?0xfbf8ef:0xeee8d8,.8,1.02+i*.045,.1);
  const m=makeMan(s);m.root.position.set(0,.47,-.55);m.legs.rotation.x=0;m.face('sad');
  const ck=wallClock(s,.55,'grumpy');ck.position.set(.1,3.35,-3.1);
  const ex=sign(s,'EXHIBIT A',1.6,'#1b2330','#ffd52e',92);
  const cal=label(s,'',.95,1.1,{});cal.material.map=canvasTexOnce(400,460,(g,W,H)=>{g.fillStyle=PAPER;g.fillRect(0,0,W,H);g.fillStyle='#d23a2a';g.fillRect(0,0,W,110);
    g.fillStyle='#fff';g.font='900 64px M';g.textAlign='center';g.fillText('WORK',W/2,80);g.fillStyle='#1b2330';g.font='900 150px M';g.fillText('40',W/2,300);g.font='800 60px M';g.fillText('DAYS',W/2,400)});
  const t0=L(3)-.05,tf=wordT(3,'forty')-t0;
  return{s,u(t){ck.set(-t*1.4+2.0,'grumpy');m.arms[0].sh.rotation.x=-1.9;m.arms[0].el.rotation.x=-1.6;m.head.rotation.z=.18;m.torso.rotation.x=.12;
    m.arms[1].sh.rotation.x=-.9;m.head.rotation.x=Math.sin(t*1.3)*.04;
    ex.visible=true;ex.scale.setScalar(pop(t,.05));ex.position.set(-.35,2.8,.9);face(ex);
    cal.visible=t>tf;cal.scale.setScalar(pop(t,tf));cal.position.set(1.05,2.55,-2.0);cal.rotation.z=-.08;
    const e=ease(t/2.9);cam(44,[lerp(.5,.3,e),2.3,lerp(5.4,4.7,e)],[0,2.25,-1])}}});

// ===== S5: "but weekends expire in four seconds flat." — beach weekend + countdown
const tFlat=wordT(4,'flat');
shot(L(4)-.05,()=>{const s=beachWorld();lights(s,{sky:0xdff2ea,ground:0x9c8660,pos:[5,10,6],sh:8});
  const lo=lounger(s,0,0,0);const m=makeMan(s,{suit:0x3aa0c8});m.legs.rotation.x=0;m.root.position.set(0,.56,.15);m.torso.rotation.x=-1.0;m.face('happy');
  const sg=grp(m.head);for(const sx of[-1,1])box(sg,.12,.07,.02,0x111111,sx*.07,.28,.16);
  const sun=sunDisc(s,5);sun.position.set(-3,7,-20);
  const cd=canvasTex(560,250,(g,W,H,txt,col)=>{g.clearRect(0,0,W,H);g.fillStyle=col;g.beginPath();g.roundRect(6,6,W-12,H-12,40);g.fill();g.fillStyle='#fff';g.textAlign='center';
    g.font='900 58px M';g.fillText('WEEKEND',W/2,82);g.font='900 120px M';g.fillText(txt,W/2,200)});
  const pl=new THREE.Mesh(new THREE.PlaneGeometry(2.2,.98),new THREE.MeshBasicMaterial({map:cd.tex,transparent:true}));s.add(pl);
  const t0=L(4)-.05,t4=wordT(4,'four')-t0,tF=tFlat-t0;let last='';
  return{s,u(t){const r=clamp((t-t4)/(tF-t4));const sec=t<t4?4:Math.max(0,4-r*4);const txt='0:0'+Math.ceil(sec-1e-6).toString();const col=sec<1.5?'#d23a2a':'#1f8a3a';
    if(txt+col!==last){cd.draw(txt,col);last=txt+col}
    m.face(t>tF-.4?'scared':'happy');for(const a of m.arms){a.sh.rotation.z=a.s*2.6;a.el.rotation.x=-1.2}
    pl.position.set(0,2.95,.4);pl.scale.setScalar(pop(t,.05)*(1+(t>t4?Math.sin(t*40)*.03:0)));face(pl);
    const e=ease(t/2.1);cam(44,[.4,lerp(2.2,2.0,e),lerp(5.6,4.8,e)+(t>t4?Math.sin(t*50)*.02:0)],[0,1.8,0])}}});
// S5b: hard cut — Monday at desk
shot(tFlat,()=>{const s=room();const desk=grp(s,0,0,.2);box(desk,2.4,.1,1.1,0x9a6a3c,0,.95,0);for(const x of[-1.1,1.1])box(desk,.1,.95,1.0,0x7a5230,x,.475,0);
  const mon=grp(desk,-.75,0,-.1);mon.rotation.y=.6;box(mon,.8,.55,.06,0x2b2f38,0,1.32,0);const m=makeMan(s);m.root.position.set(0,.47,-.55);m.legs.rotation.x=0;m.face('scared');
  const mo=sign(s,'MONDAY',1.4);
  return{s,u(t){for(const a of m.arms){a.sh.rotation.z=a.s*(1.9+Math.sin(t*30)*.2);a.el.rotation.x=-.4}
    mo.scale.setScalar(pop(t,0,.18));mo.position.set(.1,3.1,.9);face(mo,-.06);
    const sk=shake(t,0,.08,.3);cam(46,[.3+sk,2.2,4.4-t*.4],[0,2.15,-1])}}});

// ===== S6: "The judge actually subpoenaed Father Time."
shot(L(5)-.03,()=>{const R=court({judge:true,man:false});const {s,judge}=R;const pa=label(judge.arms[1].el,'',.75,.95,{});
  pa.material.map=canvasTexOnce(400,500,(g,W,H)=>{g.fillStyle=PAPER;g.fillRect(0,0,W,H);g.fillStyle='#d23a2a';g.font='900 62px M';g.textAlign='center';g.fillText('SUBPOENA',W/2,90);
    g.fillStyle='#1b2330';g.font='800 40px M';g.fillText('TO:',W/2,180);g.font='900 56px M';g.fillText('FATHER',W/2,255);g.fillText('TIME',W/2,320);g.fillStyle='rgba(0,0,0,.2)';for(let y=370;y<470;y+=30)g.fillRect(50,y,W-100-(y%90),8)});
  pa.position.set(-.1,-.62,.12);pa.rotation.set(0,PI,PI);
  const t0=L(5)-.03,tsb=wordT(5,'subpoenaed')-t0;
  return{s,u(t){const a=clamp((t-tsb+.25)/.3);const ar=judge.arms[1];ar.sh.rotation.x=lerp(-.2,-2.3,eout(a));ar.el.rotation.x=lerp(0,-.3,a);
    pa.visible=a>0;pa.scale.setScalar(.3+.7*eout(a));judge.face(t>tsb?'angry':'neutral');judge.arms[0].sh.rotation.x=-.5;
    const e=ease(t/1.8);cam(42,[.55,lerp(2.85,2.95,e),lerp(.9,1.5,e)],[.45,2.75,4.3])}}});

// ===== S7: "Father Time. But Time didn't show up," — empty witness stand
shot(wordT(5,'father')-.03,()=>{const R=court({man:false});const {s,stand}=R;
  const pl=label(stand,'',.95,.22,{});pl.material.map=canvasTexOnce(512,120,(g,W,H)=>{g.fillStyle='#1b2330';g.fillRect(0,0,W,H);g.fillStyle='#ffd52e';g.font='900 60px M';g.textAlign='center';g.textBaseline='middle';g.fillText('FATHER TIME',W/2,H/2+4)});
  pl.position.set(0,1.45,-.4);pl.rotation.y=PI;
  const spot=new THREE.SpotLight(0xfff2c8,40,10,.45,.5,1.2);spot.position.set(-2.4,5.5,.5);spot.target=stand;s.add(spot);
  const ns=stamp(s,'NO SHOW',1.5);const t0=wordT(5,'father')-.03,tn=wordT(6,'show')-t0;
  return{s,u(t){ns.visible=t>tn;const k=clamp((t-tn)/.12);ns.scale.setScalar(lerp(1.8,1,k));ns.position.set(-3.0,1.6,1.6);face(ns,.2);
    const e=ease(t/2.3);cam(42,[lerp(-.6,-1.0,e),lerp(2.3,2.1,e),lerp(-1.6,-.9,e)],[-3.0,1.3,2.4])}}});

// ===== S8: "stating he was running late." — Father Time strolling, unbothered
shot(wordT(6,'stating')-.05,()=>{const s=skyScene('#f6c58a');lights(s,{sky:0xffe8cc,ground:0x8a7a6a,hemi:1.5,dir:2,pos:[-5,9,8],sh:10});
  const gr=new THREE.Mesh(new THREE.PlaneGeometry(200,200),new THREE.MeshLambertMaterial({map:paintTex('#8f8a80',512,512,900,10,20,[10,40])}));gr.rotation.x=-PI/2;gr.receiveShadow=true;s.add(gr);
  const sw=new THREE.Mesh(new THREE.PlaneGeometry(200,2.4),mat(0xcfc8b8));sw.rotation.x=-PI/2;sw.position.set(0,.02,0);sw.receiveShadow=true;s.add(sw);
  for(let i=0;i<12;i++)box(s,.6,.02,.12,0xf4f1ea,-14+i*3,.02,2.4);
  setSeed(5);for(let i=0;i<9;i++){const h=3+rnd()*4;box(s,2.6,h,2.6,[0xe0a46a,0xc87a5a,0xe6d2a8,0x9fb7c8][i%4],-12+i*3.2,h/2,-3.5)}
  const sun=sunDisc(s,4);sun.position.set(3,6,-16);
  const ft=fatherTime(s);const b=bub(s,['RUNNING','LATE'],1.75,90);const t0=wordT(6,'stating')-.05,tr=wordT(6,'running')-t0;
  return{s,u(t){const x=lerp(-1.2,-.4,t/1.4);ft.position.set(x,Math.abs(Math.sin(t*4))*.04,.3);ft.rotation.y=.35;ft.rotation.z=Math.sin(t*4)*.03;
    ft.userData.arm.rotation.x=Math.sin(t*2)*.08;
    b.visible=t>tr;b.scale.setScalar(pop(t,tr));b.position.set(x+1.05,3.2,.4);face(b);
    cam(44,[x+.9,2.0,6.2-t*.3],[x+.5,1.9,0])}}});

// ===== S9: "By default, the judge granted a settlement:" — gavel bang + flying papers
shot(L(7)-.05,()=>{const R=court({judge:true});const {s,judge,man}=R;man.root.position.set(-.3,1.02,1.4);man.root.rotation.y=-.3;man.face('scared');
  setSeed(44);const P=[];const pm=new THREE.MeshLambertMaterial({color:0xfbf8ef,side:THREE.DoubleSide});
  for(let i=0;i<18;i++){const q=new THREE.Mesh(new THREE.PlaneGeometry(.26,.34),pm);s.add(q);P.push({q,v:V((rnd()-.5)*3.2,2.4+rnd()*2.5,-(.5+rnd()*2)),r:V(rnd()*8,rnd()*8,rnd()*8)})}
  const st=sign(s,'SETTLEMENT',1.0,'#1f8a3a','#fff',86);
  const t0=L(7)-.05,tb=wordT(7,'default')-t0,ts=wordT(7,'settlement')-t0;
  return{s,u(t){const ar=judge.arms[0];const up=t<tb-.25?clamp(t/(tb-.25)):1;const dn=clamp((t-tb+.08)/.08);
    ar.sh.rotation.x=lerp(-1.45,-2.6,up)*(1-dn)+(-1.45)*dn;if(t>tb+.25){const k=clamp((t-tb-.25)/.3);ar.sh.rotation.x=lerp(-1.45,-1.0,k)}
    judge.face('angry');
    const pt=t-tb;for(const p of P){p.q.visible=pt>0;if(pt>0){const tt=Math.min(pt,1.8);p.q.position.set(p.v.x*tt,2.0+p.v.y*tt-3.0*tt*tt*.5+Math.sin(pt*5+p.r.x)*.1,3.4+p.v.z*tt);
      p.q.rotation.set(p.r.x+pt*p.r.y*.6,p.r.y+pt*2,p.r.z);if(p.q.position.y<.03){p.q.position.y=.03}}}
    st.visible=t>ts;st.scale.setScalar(pop(t,ts));st.position.set(.12,3.55,2.6);face(st);
    const sk=shake(t,tb,.1,.3);const e=ease(t/2.1);cam(44,[.8+sk,lerp(2.4,2.6,e)+sk,lerp(-1.6,-.9,e)],[0,2.6,3.8])}}});

// ===== S10: "Sundays are now legally forty-eight hours long... but Mondays start" — contract
shot(L(8)-.04,()=>{const s=new THREE.Scene();s.background=paintTex('#6e4426',512,1024,1200,14,1,[40,140]);
  s.add(new THREE.HemisphereLight(0xfff6ea,0x6b4a30,2.2));const d=new THREE.DirectionalLight(0xfff0dd,1.2);d.position.set(2,4,6);s.add(d);
  const ct=contractTex();ct.draw(0);const pg=new THREE.Mesh(new THREE.PlaneGeometry(2.4,3.12),new THREE.MeshBasicMaterial({map:ct.tex}));s.add(pg);
  const sh=new THREE.Mesh(new THREE.PlaneGeometry(2.4,3.12),new THREE.MeshBasicMaterial({color:0x000000,transparent:true,opacity:.3}));sh.position.set(.08,-.1,-.02);s.add(sh);
  const t0=L(8)-.04,t1=wordT(8,'sundays')-t0,t2=wordT(9,'mondays')-t0;
  const ck=label(s,'',.55,.55,{});ck.material.map=canvasTexOnce(256,256,(g)=>{g.fillStyle='#1f8a3a';g.beginPath();g.arc(128,128,120,0,7);g.fill();g.strokeStyle='#fff';g.lineWidth=26;g.lineCap='round';g.beginPath();g.moveTo(70,130);g.lineTo(112,172);g.lineTo(190,88);g.stroke()});
  const xm=label(s,'',.55,.55,{});xm.material.map=canvasTexOnce(256,256,(g)=>{g.fillStyle='#d23a2a';g.beginPath();g.arc(128,128,120,0,7);g.fill();g.fillStyle='#fff';g.font='900 150px M';g.textAlign='center';g.textBaseline='middle';g.fillText('!',128,138)});
  return{s,u(t){ct.draw(t>t2?2:t>t1?1:0);pg.position.set(0,.55,0);pg.rotation.z=-.04;sh.rotation.z=-.04;
    ck.visible=t>t1+.6;ck.scale.setScalar(pop(t,t1+.6));ck.position.set(.95,1.05,.05);
    xm.visible=t>t2+.2;xm.scale.setScalar(pop(t,t2+.2));xm.position.set(.95,-.15,.05);
    const e=ease(t/3.8);const fy=t>t2?lerp(.85,.15,ease((t-t2)/.6)):.85;cam(40,[.1,fy,lerp(5.9,5.0,e)],[0,fy-.05,0])}}});

// ===== S11: "twice as early." — 4 AM alarm
shot(wordT(9,'twice')-.05,()=>{const s=new THREE.Scene();s.background=paintTex('#1d2550',512,1024,1000,10,1,[40,140]);
  s.add(new THREE.HemisphereLight(0x9fb0ee,0x1a1d33,1.4));const d=new THREE.DirectionalLight(0xbfcaff,1.4);d.position.set(3,6,5);d.castShadow=true;s.add(d);
  const fl=new THREE.Mesh(new THREE.PlaneGeometry(30,30),mat(0x2b3350));fl.rotation.x=-PI/2;fl.receiveShadow=true;s.add(fl);
  const wall=new THREE.Mesh(new THREE.PlaneGeometry(30,12),mat(0x3a4470));wall.position.z=-2;s.add(wall);
  box(s,2.4,.5,3.2,0x6b4a30,0,.25,0);box(s,2.2,.25,3.0,0xeef2ff,0,.62,0);box(s,1.6,.25,.6,0xffffff,0,.85,-1.1);
  const bl=box(s,2.25,.18,2.0,0x5a7fd0,0,.83,.55);
  const m=pajamaMan(s);m.legs.rotation.x=0;m.root.position.set(0,.98,-.6);
  const ns=box(s,.7,.8,.7,0x6b4a30,1.5,.4,-.6);
  const al=grp(s,1.5,.8,-.5);const body=cyl(al,.32,.32,.22,0xd23a2a,0,.3,0,20);body.rotation.x=PI/2;
  const afc=canvasTex(256,256,(g,W,H)=>{g.fillStyle='#fff';g.beginPath();g.arc(128,128,124,0,7);g.fill();g.fillStyle='#111';g.font='900 74px M';g.textAlign='center';g.textBaseline='middle';g.fillText('4:00',128,112);g.font='800 46px M';g.fillText('AM',128,180)});afc.draw();
  const fc=new THREE.Mesh(new THREE.CircleGeometry(.28,24),new THREE.MeshBasicMaterial({map:afc.tex}));fc.position.set(0,.3,.115);al.add(fc);
  for(const sx of[-1,1]){const b=new THREE.Mesh(new THREE.SphereGeometry(.12,10,8,0,PI*2,0,PI/2),mat(0xe0b33a));b.position.set(sx*.22,.58,0);b.rotation.z=-sx*.5;al.add(b)}
  const mon=sign(s,'MONDAY',1.5,'#d23a2a');
  const t0=wordT(9,'twice')-.05,te=wordT(9,'early')-t0;
  return{s,u(t){al.rotation.z=Math.sin(t*60)*.12;al.position.y=.8+Math.abs(Math.sin(t*60))*.03;
    const k=clamp((t-te)/.18);m.torso.rotation.x=lerp(-1.45,-.1,eout(k));m.root.position.y=.98+Math.sin(k*PI)*.25;m.face(k>0?'scared':'neutral');
    if(k>0)flail(m,t,.6);else for(const a of m.arms){a.sh.rotation.z=a.s*.3}
    m.legs.rotation.x=0;bl.position.y=.83;
    mon.scale.setScalar(pop(t,.05));mon.position.set(.55,2.85,.3);face(mon);
    const sk=shake(t,te,.05);cam(46,[.75+sk,2.2,5.6-t*.3],[.75,1.6,-.4])}}});

// ===== S12: "Would you sign that deal?" — man holds contract, asks viewer
shot(L(10)-.04,()=>{const R=court();const {s,man}=R;man.root.position.set(0,1.02,1.9);man.face('neutral');
  const ct=contractTex();ct.draw(2);const cp=new THREE.Mesh(new THREE.PlaneGeometry(.75,.97),new THREE.MeshBasicMaterial({map:ct.tex,side:THREE.DoubleSide}));s.add(cp);
  const pen=grp(man.arms[0].el,0,-.42,.05);cyl(pen,.025,.025,.35,0x1b2330,0,0,0,6).rotation.x=.4;
  const q=bub(s,['SIGN?'],.85,110);const t0=L(10)-.04,tq=wordT(10,'sign')-t0;
  return{s,u(t){const a1=man.arms[1];a1.sh.rotation.x=-1.0;a1.sh.rotation.z=-.15;a1.el.rotation.x=-.6;const a0=man.arms[0];a0.sh.rotation.x=-.9+Math.sin(t*3)*.05;a0.sh.rotation.z=.25;a0.el.rotation.x=-.9;
    cp.position.set(-.12,1.72,2.55);cp.rotation.set(-.15,0,.05);man.head.rotation.z=Math.sin(t*2)*.08;man.head.rotation.y=.0;
    q.visible=t>tq;q.scale.setScalar(pop(t,tq));q.position.set(.2,2.95,2.4);face(q);
    const e=ease(t/1.3);cam(42,[.25,2.55,lerp(5.4,5.0,e)],[.05,2.3,1.9])}}});

// ===== S13: "He hated the compromise" — tears contract
shot(L(11)-.04,()=>{const R=court();const {s,man}=R;man.root.position.set(0,1.02,1.9);
  const ct=contractTex();ct.draw(2);const mk=(o)=>{const g=new THREE.PlaneGeometry(.375,.97);const uv=g.attributes.uv;for(let i=0;i<uv.count;i++)uv.setX(i,uv.getX(i)*.5+o);
    const m=new THREE.Mesh(g,new THREE.MeshBasicMaterial({map:ct.tex,side:THREE.DoubleSide}));s.add(m);return m};const hl=mk(0),hr=mk(.5);
  setSeed(71);const P=[];const pm=new THREE.MeshBasicMaterial({color:0xfbf8ef,side:THREE.DoubleSide});for(let i=0;i<14;i++){const q=new THREE.Mesh(new THREE.PlaneGeometry(.08,.1),pm);s.add(q);P.push({q,v:V((rnd()-.5)*2.4,1+rnd()*1.6,rnd()*.8),r:rnd()*6})}
  const t0=L(11)-.04,th=wordT(11,'hated')-t0+.05;
  return{s,u(t){const k=clamp((t-th)/.25);man.face('angry');
    for(const a of man.arms){a.sh.rotation.x=-1.05;a.sh.rotation.z=a.s*(.15+.5*eout(k));a.el.rotation.x=-.5}
    const sp=eout(k);hl.position.set(-.19-sp*.55,2.1-sp*.1,2.6);hl.rotation.set(-.1,0,sp*.6);hr.position.set(.19+sp*.55,2.1-sp*.1,2.6);hr.rotation.set(-.1,0,-sp*.6);
    const pt=t-th;for(const p of P){p.q.visible=pt>0;p.q.position.set(p.v.x*pt,2.1+p.v.y*pt-2*pt*pt,2.65+p.v.z*pt);p.q.rotation.set(p.r+pt*6,pt*4,p.r)}
    man.root.position.y=1.02+(pt>0&&pt<.3?Math.abs(Math.sin(pt*30))*.04:0);
    const sk=shake(t,th,.07);const e=ease(t/1.2);cam(42,[.25+sk,2.55,lerp(4.6,4.9,e)],[.05,2.25,1.9])}}});

// ===== S14: "so much, so..." — marches back with a fresh folder; ends on S0's first frame
shot(wordT(11,'so')-.04,()=>{const R=court();const {s,man}=R;const f=folder(s);const t0=wordT(11,'so')-.04;const D=END-t0;
  return{s,u(t){const p=clamp(t/(D-.12));const z=lerp(-.4,2.2,eout(p));man.root.position.set(0,1.02+(p<1?Math.abs(Math.sin(t*11))*.06*(1-p):0),z);
    man.root.rotation.z=p<1?Math.sin(t*11)*.04*(1-p):0;man.face('angry');man.torso.rotation.x=0;
    const a=lerp(-.9,-2.7,eout(clamp(t/(D*.7))));holdOverhead(man,f,a);
    const e=eout(p);cam(C0.fov,[lerp(.6,C0.pos[0],e),lerp(3.0,C0.pos[1],e),lerp(6.2,C0.pos[2],e)],[C0.look[0],lerp(1.8,C0.look[1],e),lerp(.2,C0.look[2],e)])}}});

run(shots,END);
