// "Only coffee for 3 days" — clean explainer style; all titles are screen-pinned (HUD) so they always stay in frame
import {faceEyes,W,H,THREE,camera,cam,loadTiming,run,clamp,ease,eout,back,lerp,V,grp,RB,SPH,sm,cyl,paintTex,setSeed,rnd,carSimple,lamp} from './engine.js';
const T=await loadTiming(); const T0=0.15;
const L=i=>T[i].start+T0, E=i=>T[i].end+T0;
const wordT=(i,w)=>{const x=T[i].words.find(q=>q.w.toLowerCase().replace(/[^a-z0-9]/g,'').startsWith(w));return (x?x.start:T[i].start)+T0};
const shots=[];let CURH=[];
// HUD text: pinned to the screen (yf = height fraction from bottom, wf = width fraction) so it can never leave the frame
function hud(text,o={}){const {yf=.8,wf=.76,...rest}=o;const g=new THREE.Group();const m=txt(g,text,{...rest,w:1});g.remove(m);m.material.depthTest=false;m.material.fog=false;m.renderOrder=30;m.userData.hud={yf,wf};m.userData.k=0;CURH.push(m);return m}
const hpop=(m,t0,t,dur=.28,t1=1e9)=>{m.userData.k=t<t0||t>t1?0:back((t-t0)/dur)};
const shot=(start,build)=>shots.push({start,build:()=>{CURH=[];const i=build();const hs=CURH;hs.forEach(m=>i.s.add(m));const u=i.u;
  i.u=(t)=>{BB.clear();u(t);BB.forEach(m=>m.quaternion.copy(camera.quaternion));camera.aspect=W/H;camera.updateProjectionMatrix();
    const D=.5,h=2*Math.tan(camera.fov*Math.PI/360)*D,w=h*camera.aspect;const f=V(0,0,-1).applyQuaternion(camera.quaternion),up=V(0,1,0).applyQuaternion(camera.quaternion);
    for(const m of hs){const k=m.userData.k,{yf,wf}=m.userData.hud;m.visible=k>.001;const sc=Math.max(.0001,k*wf*w);m.scale.set(sc,sc,1);
      m.position.copy(camera.position).addScaledVector(f,D).addScaledVector(up,(yf-.5)*h);m.quaternion.copy(camera.quaternion)}};return i}});
const END=E(T.length-1)+0.25;

// ---------- look helpers ----------
const sstep=x=>{x=clamp(x);return x*x*(3-2*x)};
function gradTex(top,bot,mid=null){const c=document.createElement('canvas');c.width=8;c.height=512;const g=c.getContext('2d');const gr=g.createLinearGradient(0,0,0,512);
  gr.addColorStop(0,top);if(mid)gr.addColorStop(.55,mid);gr.addColorStop(1,bot);g.fillStyle=gr;g.fillRect(0,0,8,512);const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;return t}
const GLOW=(()=>{const c=document.createElement('canvas');c.width=c.height=128;const g=c.getContext('2d');const r=g.createRadialGradient(64,64,0,64,64,64);
  r.addColorStop(0,'rgba(255,255,255,1)');r.addColorStop(.25,'rgba(255,255,255,.55)');r.addColorStop(1,'rgba(255,255,255,0)');g.fillStyle=r;g.fillRect(0,0,128,128);return new THREE.CanvasTexture(c)})();
function glow(p,col,size,op=1){const s=new THREE.Sprite(new THREE.SpriteMaterial({map:GLOW,color:col,blending:THREE.AdditiveBlending,depthWrite:false,transparent:true,opacity:op}));s.scale.set(size,size,1);p.add(s);return s}
// bold outlined text on a plane; auto-shrinks the font to fit
function txt(p,text,{w=1.6,cw=1024,ch=256,fg='#ffffff',stroke='#0b0f1a',size=170,weight=900,bg=null,radius=60,sw=26}={}){
  const c=document.createElement('canvas');c.width=cw;c.height=ch;const g=c.getContext('2d');
  if(bg){g.fillStyle=bg;g.beginPath();g.roundRect(8,8,cw-16,ch-16,radius);g.fill()}
  let fs=size;g.font=`${weight} ${fs}px M`;while(g.measureText(text).width>cw*(bg?.84:.9)&&fs>20){fs-=6;g.font=`${weight} ${fs}px M`}
  g.textAlign='center';g.textBaseline='middle';g.lineJoin='round';
  if(stroke){g.lineWidth=sw;g.strokeStyle=stroke;g.strokeText(text,cw/2,ch/2+fs*.04)}g.fillStyle=fg;g.fillText(text,cw/2,ch/2+fs*.04);
  const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;t.anisotropy=8;
  const m=new THREE.Mesh(new THREE.PlaneGeometry(w,w*ch/cw),new THREE.MeshBasicMaterial({map:t,transparent:true,depthWrite:false}));m.renderOrder=5;p.add(m);return m}
function dynTex(cw,ch,draw){const c=document.createElement('canvas');c.width=cw;c.height=ch;const g=c.getContext('2d');const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;t.anisotropy=8;let last=null;
  return{t,set:(v)=>{if(v===last)return;last=v;g.clearRect(0,0,cw,ch);draw(g,cw,ch,v);t.needsUpdate=true}}}
const pop=(m,t0,t,dur=.28,base=1)=>{const k=t<t0?0:back((t-t0)/dur);m.visible=k>0.001;m.scale.setScalar(Math.max(.001,k*base))};
const BB=new Set();const face2cam=(m)=>BB.add(m);
let shakeT=-9;const shake=(t,amt=.05)=>{const d=t-shakeT;if(d<0||d>.22)return[0,0];const k=(1-d/.22)*amt;return[Math.sin(d*90)*k,Math.cos(d*77)*k]};
function camS(fov,pos,look,t,hitTimes=[],amt=.05){let dx=0,dy=0;for(const h of hitTimes){const d=t-h;if(d>=0&&d<.22){const k=(1-d/.22)*amt;dx+=Math.sin(d*90)*k;dy+=Math.cos(d*77)*k}}
  cam(fov,[pos[0]+dx,pos[1]+dy,pos[2]],[look[0]+dx,look[1]+dy,look[2]])}

// dark studio with coloured rim lights (the "clean explainer" look)
function studio2(top,bot,{floor=true,key=2.4,rimA=0x5fb2ff,rimB=0xff6fae,hemi=0.9,fogNear=9}={}){
  const s=new THREE.Scene();s.background=gradTex(top,bot);s.fog=new THREE.Fog(new THREE.Color(bot),fogNear,fogNear+10);
  s.add(new THREE.HemisphereLight(0xcfdcff,0x20141c,hemi));
  const k=new THREE.DirectionalLight(0xfff0e0,key);k.position.set(3,6,6);k.castShadow=true;k.shadow.mapSize.set(1024,1024);const c=k.shadow.camera;c.left=c.bottom=-5;c.right=c.top=5;k.shadow.bias=-.0008;k.shadow.normalBias=.03;k.shadow.radius=5;s.add(k);
  const r1=new THREE.DirectionalLight(rimA,2.2);r1.position.set(-5,3,-4);s.add(r1);const r2=new THREE.DirectionalLight(rimB,1.4);r2.position.set(5,2,-5);s.add(r2);
  if(floor){const f=new THREE.Mesh(new THREE.PlaneGeometry(60,60),new THREE.MeshStandardMaterial({color:new THREE.Color(bot).multiplyScalar(1.6),roughness:.9}));f.rotation.x=-Math.PI/2;f.receiveShadow=true;s.add(f);
    const spot=new THREE.Mesh(new THREE.CircleGeometry(1.9,48),new THREE.MeshBasicMaterial({map:GLOW,color:new THREE.Color(top).multiplyScalar(1.4),transparent:true,opacity:.55,depthWrite:false,blending:THREE.AdditiveBlending}));spot.rotation.x=-Math.PI/2;spot.position.y=.005;s.add(spot)}
  return s}

// ---------- the boy (rounded, expressive, x-ray capable) ----------
function brain(p){const g=grp(p);const geo=new THREE.IcosahedronGeometry(1,5);const pa=geo.attributes.position;
  for(let i=0;i<pa.count;i++){const x=pa.getX(i),y=pa.getY(i),z=pa.getZ(i);
    const n=Math.sin(x*7+y*2.3)*Math.sin(y*9.1+z*1.7)*Math.sin(z*8.3+x*3.1)+.55*Math.sin(x*17+z*13)*Math.sin(y*15+x*3);const f=1+.075*n;pa.setXYZ(i,x*f,y*f,z*f)}
  geo.computeVertexNormals();
  const M=new THREE.MeshStandardMaterial({color:0xf3a6b8,roughness:.45,emissive:0xff4f86,emissiveIntensity:.35});g.userData.M=M;
  for(const s of[-1,1]){const h=new THREE.Mesh(geo,M);h.scale.set(.48,.72,1);h.position.x=s*.5;h.castShadow=true;g.add(h)}
  const cb=SPH(g,.42,M,0,-.5,-.62,16);cb.scale.set(1.3,.7,1);const st=cyl(g,.16,.12,.7,M,0,-.85,-.35,10);st.rotation.x=.3;
  g.scale.setScalar(.2);return g}
function brainPt(seedV){const d=V(Math.sin(seedV*12.9)*.7,Math.sin(seedV*78.2)*.9,Math.cos(seedV*37.7)).normalize();const s=Math.sin(seedV*91.3)>0?1:-1;
  return V(s*.5+d.x*.48*1.05,d.y*.72*1.05,d.z*1.05)}
function kid(p,{tee=0x2f7fd8,pants=0x34405e,skin=0xe9b48c,hair=0x3b2414}={}){
  const R={};const S=sm(skin,.55);const HS=sm(skin,.55);R.HS=HS;const root=grp(p);R.root=root;R.legs=[];
  for(const s of[-1,1]){const lg=grp(root,s*.13,0,0);RB(lg,.23,.86,.25,.1,sm(pants,.85),0,-.43,0);RB(lg,.26,.15,.4,.07,sm(0xf4f4f4,.5),0,-.88,.07);R.legs.push(lg)}
  const torso=grp(root);R.torso=torso;RB(torso,.62,.76,.38,.17,sm(tee,.75),0,.39,0);RB(torso,.2,.1,.2,.06,S,0,.79,0);
  const head=grp(torso,0,.84,0);R.head=head;R.skull=RB(head,.58,.62,.54,.24,HS,0,.31,0);
  const HM=sm(hair,.85);R.hairG=grp(head);
  [[0,.62,-.02,.2],[-.16,.6,.05,.15],[.16,.6,.04,.16],[-.22,.5,-.12,.15],[.22,.5,-.12,.15],[0,.52,-.22,.2],[.05,.66,.12,.12],[-.09,.64,.16,.1],[.24,.42,-.2,.12],[-.24,.42,-.2,.12],[.13,.66,-.12,.13]]
    .forEach(([x,y,z,r])=>{const h=SPH(R.hairG,r,HM,x,y,z,14);h.scale.y=.75});
  for(const s of[-1,1])SPH(head,.075,HS,s*.29,.29,0,12);
  R.ewM=sm(0xffffff,.25);R.bagM=new THREE.MeshStandardMaterial({color:0x6a3a5a,roughness:.8,transparent:true,opacity:0});
  R.lids=[];R.pupils=[];R.eyes=[];
  for(const s of[-1,1]){const eg=grp(head,s*.125,.34,.245);R.eyes.push(eg);
    const w=SPH(eg,.085,R.ewM,0,0,0,18);w.scale.set(1,1.12,.6);
    const pg=grp(eg);R.pupils.push(pg);const ir=SPH(pg,.052,sm(0x3f7fb5,.3),0,0,.04,14);ir.scale.set(1,1.12,.45);
    const pu=SPH(pg,.03,sm(0x0c0c10,.2),0,0,.056,12);pu.scale.z=.4;SPH(pg,.012,sm(0xffffff,.1),.02,.025,.066,8);
    const lg=grp(eg);lg.scale.set(1.1,1.22,.68);const lid=new THREE.Mesh(new THREE.SphereGeometry(.085,18,10,0,Math.PI*2,0,Math.PI/2),HS);lg.add(lid);R.lids.push(lg);
    const bag=SPH(head,.07,R.bagM,s*.125,.255,.236,12);bag.scale.set(1.25,.42,.35)}
  R.brows=[];for(const s of[-1,1]){const b=RB(head,.13,.032,.035,.014,HM,s*.125,.47,.25);b.userData.s=s;R.brows.push(b)}
  RB(head,.075,.1,.07,.033,HS,0,.25,.27);
  const blk=sm(0x3a1414,.4);
  R.smile=new THREE.Mesh(new THREE.TorusGeometry(.075,.016,8,20,Math.PI),blk);R.smile.rotation.z=Math.PI;R.smile.position.set(0,.16,.255);head.add(R.smile);
  R.frown=new THREE.Mesh(new THREE.TorusGeometry(.065,.016,8,20,Math.PI),blk);R.frown.position.set(0,.1,.25);head.add(R.frown);
  R.flat=RB(head,.11,.022,.02,.01,blk,0,.13,.258);
  R.oM=SPH(head,.045,sm(0x5a1a1a,.5),0,.12,.252,12);R.oM.scale.set(1,1.3,.4);
  R.face=(f)=>{R.smile.visible=f==='happy';R.frown.visible=f==='sad';R.flat.visible=f==='neutral'||f==='tired';R.oM.visible=f==='shock';
    R.brows.forEach(b=>{const s=b.userData.s;b.rotation.z=f==='sad'||f==='tired'?-s*.28:f==='angry'?s*.3:0;b.position.y=f==='shock'?.5:f==='tired'?.455:.47})};
  R.lid=(c)=>R.lids.forEach(l=>l.rotation.x=lerp(-.8,1.55,c));
  R.tired=(k)=>{R.bagM.opacity=k*.85;R.ewM.color.setRGB(1,1-.22*k,1-.25*k)};
  R.look=(x,y)=>R.pupils.forEach(pg=>pg.position.set(x*.028,y*.028,0));
  R.arms=[];for(const s of[1,-1]){const sh=grp(torso,s*.38,.68,0);RB(sh,.17,.4,.18,.08,sm(tee,.75),0,-.17,0);const el=grp(sh,0,-.36,0);RB(el,.14,.32,.15,.065,S,0,-.15,0);SPH(el,.085,S,0,-.34,0,14);R.arms.push({sh,el,s})}
  R.arms.forEach(a=>{a.sh.rotation.z=a.s*.12});
  R.brain=brain(head);R.brain.position.set(0,.36,-.01);R.brain.visible=false;
  R.xray=(on,op=.16)=>{HS.transparent=on;HS.opacity=on?op:1;HS.depthWrite=!on;HS.needsUpdate=true;R.hairG.visible=!on;R.brain.visible=on;R.eyes.forEach(e=>e.visible=!on);R.brows.forEach(b=>b.visible=!on);[R.oM,R.flat,R.smile,R.frown].forEach(m=>m.visible=false)};
  R.face('neutral');R.lid(0);R.tired(0);return R}
const HEADY=.95+.84; // head-group world height for a standing boy (root at .95)

// ---------- night bedroom ----------
function clockTex(){return dynTex(512,512,(g,w,h,v)=>{g.fillStyle='#f7f3ea';g.beginPath();g.arc(256,256,240,0,7);g.fill();g.lineWidth=22;g.strokeStyle='#22283a';g.stroke();
  g.fillStyle='#22283a';for(let i=0;i<12;i++){const a=i/12*Math.PI*2;g.save();g.translate(256+Math.sin(a)*195,256-Math.cos(a)*195);g.rotate(a);g.fillRect(-7,-22,14,i%3?30:44);g.restore()}})}
function wallClock(p,r=.45){const g=grp(p);const ct=clockTex();ct.set(1);const face=new THREE.Mesh(new THREE.CircleGeometry(r,48),new THREE.MeshStandardMaterial({map:ct.t,roughness:.6}));g.add(face);
  const rim=new THREE.Mesh(new THREE.TorusGeometry(r,.035,10,48),sm(0x22283a,.4));g.add(rim);
  const hh=grp(g,0,0,.02),mh=grp(g,0,0,.03);RB(hh,.05,r*.55,.02,.01,sm(0x1b1f2c),0,r*.25,0);RB(mh,.035,r*.8,.02,.01,sm(0x1b1f2c),0,r*.38,0);
  const sh=grp(g,0,0,.04);RB(sh,.015,r*.85,.01,.005,sm(0xd8423a),0,r*.35,0);SPH(g,.03,sm(0xd8423a),0,0,.05,10);g.userData={hh,mh,sh};
  g.setTime=(hours)=>{hh.rotation.z=-hours/12*Math.PI*2;mh.rotation.z=-hours*Math.PI*2;sh.rotation.z=-hours*60*Math.PI*2};return g}
function bedroom(){const s=new THREE.Scene();s.background=new THREE.Color(0x0b1122);s.fog=new THREE.Fog(0x0b1122,9,18);
  const wallM=new THREE.MeshStandardMaterial({map:paintTex('#43547a',512,512,500,10,3),roughness:.95});
  const bw=new THREE.Mesh(new THREE.PlaneGeometry(14,8),wallM);bw.position.set(0,4,-3);bw.receiveShadow=true;s.add(bw);
  const lw=new THREE.Mesh(new THREE.PlaneGeometry(10,8),wallM);lw.rotation.y=Math.PI/2;lw.position.set(-3.4,4,1);lw.receiveShadow=true;s.add(lw);
  const fl=new THREE.Mesh(new THREE.PlaneGeometry(14,12),new THREE.MeshStandardMaterial({map:paintTex('#6b4a34',512,512,600,12,6,[40,140]),roughness:.85}));fl.rotation.x=-Math.PI/2;fl.receiveShadow=true;s.add(fl);
  const rug=RB(s,2.2,.02,1.5,.01,sm(0x8a3a4a,.95),-.2,.01,.2);rug.receiveShadow=true;
  // window with moon
  const win=grp(s,-1.5,2.7,-2.97);RB(win,1.5,1.3,.08,.03,sm(0xe8e8ee,.5));const gl=new THREE.Mesh(new THREE.PlaneGeometry(1.32,1.12),new THREE.MeshBasicMaterial({color:0x1b2f66}));gl.position.z=.05;win.add(gl);
  RB(win,.05,1.15,.06,.02,sm(0xe8e8ee,.5),0,0,.07);RB(win,1.32,.05,.06,.02,sm(0xe8e8ee,.5),0,0,.07);
  const moon=new THREE.Mesh(new THREE.CircleGeometry(.16,24),new THREE.MeshBasicMaterial({color:0xfff2c6}));moon.position.set(.3,.25,.06);win.add(moon);const mg=glow(win,0x9fb8ff,1.1,.6);mg.position.set(.3,.25,.08);
  for(let i=0;i<14;i++){const st=new THREE.Mesh(new THREE.CircleGeometry(.012,6),new THREE.MeshBasicMaterial({color:0xffffff}));st.position.set(-.6+((i*37)%120)/100,-.5+((i*53)%100)/100,.055);win.add(st)}
  // bed
  const bed=grp(s,1.25,0,-1.55);RB(bed,1.7,.36,2.7,.06,sm(0x8a5a3a,.6),0,.2,0);RB(bed,1.6,.24,2.6,.1,sm(0xf1efe8,.8),0,.5,0);RB(bed,1.72,1.1,.12,.05,sm(0x8a5a3a,.6),0,.55,-1.38);
  RB(bed,.85,.18,.45,.09,sm(0xffffff,.8),0,.69,-1.0);const blanket=RB(bed,1.66,.1,1.6,.05,sm(0x3a6fd0,.8),0,.65,.45);
  // nightstand + lamp (warm key light)
  const ns=grp(s,2.55,0,-2.5);RB(ns,.6,.6,.5,.05,sm(0x8a5a3a,.6),0,.3,0);cyl(ns,.05,.05,.35,sm(0x333333),0,.78,0,8);
  const shade=cyl(ns,.12,.22,.26,new THREE.MeshBasicMaterial({color:0xffd27a}),0,1.02,0,16);const lg=glow(ns,0xffb050,1.4,.7);lg.position.y=1.0;
  const pl=new THREE.PointLight(0xffb060,9,7,1.4);pl.position.set(2.45,1.2,-2.2);s.add(pl);
  // poster + clock
  const post=grp(s,.4,2.8,-2.97);RB(post,.75,1.0,.03,.01,sm(0xf2b33a,.7));const pc=SPH(post,.2,sm(0xd8423a,.6),0,.1,.03,16);pc.scale.z=.1;
  const clk=wallClock(s,.36);clk.position.set(1.25,2.55,-2.94);clk.setTime(3.2);
  s.add(new THREE.HemisphereLight(0x7088cc,0x1a1420,1.1));
  const mo=new THREE.DirectionalLight(0xa8c0ff,1.6);mo.position.set(-3,5,3);mo.castShadow=true;mo.shadow.mapSize.set(1024,1024);const c=mo.shadow.camera;c.left=c.bottom=-5;c.right=c.top=5;mo.shadow.bias=-.0008;mo.shadow.normalBias=.03;mo.shadow.radius=5;s.add(mo);
  const rim=new THREE.DirectionalLight(0x6fa8ff,1.2);rim.position.set(-2,3,-4);s.add(rim);
  return{s,clk,bed,blanket}}


// ---------- shared x-ray brain shot ----------
function xrayScene(mode){const s=studio2(mode==='toxic'?'#1d3a2c':'#13284a',mode==='toxic'?'#040a07':'#03060d',{floor:false,rimA:mode==='toxic'?0x7dff9a:0x5fb2ff});
  const k=kid(s);k.root.position.set(0,.95,0);k.xray(true);const B=k.brain,M=B.userData.M;
  // neural signals: glowing dots travelling between points on the brain surface
  const pulses=[];for(let i=0;i<34;i++){const a=brainPt(i*1.37+.3),b=brainPt(i*2.11+.9);const sp=glow(B,0x9fe8ff,.55,.95);pulses.push({sp,a,b,ph:(i*.137)%1})}
  // toxic waste particles
  const tox=[];if(mode==='toxic'){const tm=new THREE.MeshBasicMaterial({color:0x7dff3a});for(let i=0;i<150;i++){const p=brainPt(i*3.71+.11).multiplyScalar(1.02+((i*7)%10)/60);
    const m=SPH(B,.07+((i*13)%7)/90,tm,p.x,p.y,p.z,8);m.castShadow=false;const g=glow(B,0x7dff3a,.45,.8);g.position.copy(p);tox.push({m,g,at:i/150})}}
  return{s,k,B,M,pulses,tox}}
function updPulses(P,t,speed,on=1){for(const q of P){const u=(q.ph+t*speed)%1;q.sp.position.lerpVectors(q.a,q.b,u).multiplyScalar(1+.12*Math.sin(u*Math.PI));q.sp.material.opacity=on*Math.sin(u*Math.PI)}}

// ---------- coffee props ----------
const COF=0x3a1f0e;
function mug(p,{col=0xf4efe6,h=.9,r=.42,fill=.82}={}){const g=grp(p);const M=sm(col,.35);M.side=THREE.DoubleSide;
  const body=new THREE.Mesh(new THREE.CylinderGeometry(r,r*.9,h,40,1,true),M);body.position.y=h/2;body.castShadow=true;g.add(body);
  const bot=new THREE.Mesh(new THREE.CircleGeometry(r*.9,40),M);bot.rotation.x=-Math.PI/2;bot.position.y=.01;g.add(bot);
  const rim=new THREE.Mesh(new THREE.TorusGeometry(r,.03,8,40),M);rim.rotation.x=Math.PI/2;rim.position.y=h;g.add(rim);
  const cof=new THREE.Mesh(new THREE.CircleGeometry(r*.97,40),sm(COF,.15));cof.rotation.x=-Math.PI/2;g.add(cof);
  const hd=new THREE.Mesh(new THREE.TorusGeometry(r*.4,r*.1,10,24),M);hd.position.set(r*1.08,h*.52,0);g.add(hd);
  g.setFill=(f)=>{cof.position.y=Math.max(.02,h*f);cof.scale.setScalar(lerp(.9,1,f))};g.setFill(fill);g.userData={cof,h};return g}
function steam(p,n=6,col=0xffffff){const out=[];for(let i=0;i<n;i++){out.push({s:glow(p,col,.6,.3),ph:i/n})}
  return(t)=>out.forEach((q,i)=>{const u=(t*.6+q.ph)%1;q.s.position.set(Math.sin(u*6+i)*.12,u*1.1,0);q.s.material.opacity=.32*Math.sin(u*Math.PI);q.s.scale.setScalar(.4+u*.6)})}
function ecgDraw(g,w,h,key){const [tt,bpm]=key.split(':').map(Number);const t=tt/30;
  g.fillStyle='#04140c';g.fillRect(0,0,w,h);g.strokeStyle='rgba(60,255,140,.12)';g.lineWidth=2;for(let x=0;x<w;x+=40){g.beginPath();g.moveTo(x,0);g.lineTo(x,h);g.stroke()}for(let y=0;y<h;y+=40){g.beginPath();g.moveTo(0,y);g.lineTo(w,y);g.stroke()}
  const col=bpm>140?'#ff4a3a':bpm>100?'#ffd23a':'#3dff8c';g.strokeStyle=col;g.lineWidth=7;g.lineJoin='round';g.beginPath();const base=h*.62;
  for(let x=0;x<=w;x+=3){const ti=t-(1-x/w)*2.6;const ph=((ti*bpm/60)%1+1)%1;let y=0;
    if(ph>.10&&ph<.13)y=-(ph-.10)/.03*h*.42;else if(ph>=.13&&ph<.16)y=-h*.42+(ph-.13)/.03*h*.55;else if(ph>=.16&&ph<.19)y=h*.13-(ph-.16)/.03*h*.13;else if(ph>.3&&ph<.42)y=-Math.sin((ph-.3)/.12*Math.PI)*h*.06;
    x?g.lineTo(x,base+y):g.moveTo(x,base+y)}g.stroke();
  g.fillStyle=col;g.font='900 96px M';g.textAlign='right';g.fillText(bpm+' BPM',w-30,100);g.font='800 40px M';g.textAlign='left';g.fillText('HEART RATE',30,70)}
function monitor(p,wd=1.7){const g=grp(p);RB(g,wd,wd*.64,.2,.07,sm(0x252a33,.4));const sc=dynTex(800,480,ecgDraw);
  const scr=new THREE.Mesh(new THREE.PlaneGeometry(wd*.9,wd*.54),new THREE.MeshBasicMaterial({map:sc.t}));scr.position.z=.11;g.add(scr);
  const gl=glow(g,0x3dff8c,wd*1.6,.18);gl.position.z=-.2;g.setECG=(t,bpm)=>sc.set(Math.round(t*30)+':'+Math.round(bpm));return g}
function molecule(p,col,r=.2){const g=grp(p);const M=sm(col,.3);SPH(g,r,M,0,0,0,16);for(let i=0;i<4;i++){const a=i*1.57+.4,b=i%2?.6:-.5;SPH(g,r*.5,M,Math.cos(a)*r*1.2,b*r*1.3,Math.sin(a)*r*1.2,12)}
  const gl=glow(g,col,r*4,.35);return g}
function heart(p){const g=grp(p);const M=new THREE.MeshStandardMaterial({color:0xe0283a,roughness:.35,emissive:0xff1a2a,emissiveIntensity:.25});
  for(const s of[-1,1])SPH(g,.5,M,s*.3,.22,0,24);const c=new THREE.Mesh(new THREE.ConeGeometry(.74,1.05,32),M);c.rotation.z=Math.PI;c.position.y=-.42;c.castShadow=true;g.add(c);
  const ao=cyl(g,.12,.14,.5,sm(0xc0202e,.4),-.1,.82,0,12);ao.rotation.z=.25;const ao2=cyl(g,.1,.1,.4,sm(0x3a6fd0,.4),.25,.78,-.05,12);ao2.rotation.z=-.3;g.userData.M=M;return g}
function stomach(p){const g=grp(p);const M=new THREE.MeshStandardMaterial({color:0xf09aa8,roughness:.35,transparent:true,opacity:.42,depthWrite:false,side:THREE.DoubleSide,emissive:0xff2030,emissiveIntensity:0});
  const pts=[[-.55,.8,.34],[-.48,.5,.44],[-.3,.18,.54],[.05,-.02,.6],[.42,.02,.54],[.68,.22,.42],[.82,.46,.3]];pts.forEach(([x,y,r])=>SPH(g,r,M,x,y,0,24));
  cyl(g,.16,.18,.8,M,-.6,1.25,0,16);const du=cyl(g,.14,.14,.5,M,.95,.72,0,16);du.rotation.z=-.6;
  const CM=new THREE.MeshStandardMaterial({color:COF,roughness:.2,transparent:true,opacity:.92});pts.slice(1,6).forEach(([x,y,r])=>{const c=SPH(g,r*.8,CM,x,y-.06,0,20);c.scale.y=.75});
  const bub=[];for(let i=0;i<22;i++){const s=glow(g,0xd8ff3a,.22,.8);bub.push({s,x:-.4+((i*37)%100)/100*1.0,ph:(i*.137)%1})}
  g.userData={M,bub};return g}
function hand(p,s){const g=grp(p);const S=sm(0xe9b48c,.55);RB(g,.26,.9,.28,.12,sm(0x2f7fd8,.75),0,-.55,0);RB(g,.3,.32,.24,.1,S,0,0,0);
  for(let i=0;i<4;i++)RB(g,.065,.2,.08,.03,S,-s*.04+(i-1.5)*.07*s*-1,.12,.13).rotation.x=-.9;RB(g,.08,.18,.08,.035,S,s*.17,.0,.06).rotation.z=s*.6;return g}
function shadowMan(p){const g=grp(p);const M=sm(0x07060c,.9);RB(g,.7,1.5,.4,.3,M,0,.75,0);SPH(g,.32,M,0,1.75,0,16);
  const eyes=[];for(const x of[-.11,.11]){const e=SPH(g,.045,new THREE.MeshBasicMaterial({color:0xff3a3a}),x,1.8,.29,8);eyes.push(e);const gl=glow(g,0xff2a2a,.35,.8);gl.position.set(x,1.8,.32)}return g}
function kitchen(top='#6b3f22',bot='#1a0d06'){return studio2(top,bot,{rimA:0xffc07a,rimB:0xff8a5a,hemi:1.1})}

// ================= SHOTS =================
// 0. HOOK — black coffee pouring, title on frame 0
shot(0,()=>{const s=kitchen('#7a4526','#160a04');const tb=RB(s,4,.12,2.2,.04,sm(0x6b4a34,.7),0,1.0,0);
  const m=mug(s,{h:1.0,r:.5,fill:.2});m.position.set(0,1.06,.1);const st=steam(m);
  const pot=grp(s,-.72,3.0,.1);pot.rotation.z=-1.95;const gm=new THREE.MeshStandardMaterial({color:0xcfe6f2,roughness:.05,transparent:true,opacity:.35,depthWrite:false});
  cyl(pot,.32,.38,.75,gm,0,0,0,24);const pc=cyl(pot,.3,.36,.45,sm(COF,.2),0,-.12,0,24);cyl(pot,.2,.32,.2,sm(0x222222,.4),0,.47,0,24);
  const stream=cyl(s,.06,.07,1,sm(COF,.15),0,0,0,10);
  const h1=hud('ONLY COFFEE',{yf:.86,wf:.8,fg:'#ffffff'});const h2=hud('FOR 72 HOURS?',{yf:.79,wf:.74,fg:'#ffd23a'});
  return{s,u(t){const f=lerp(.25,.85,clamp(t/2.6));m.setFill(f);const top=1.06+1.0*f;const sx=-.72+.47*Math.sin(1.95),sy=3.0+.47*Math.cos(1.95);const dx=.0-sx,dy=top-sy;
    stream.position.set((sx)/2+Math.sin(t*20)*.008,(sy+top)/2,.1);stream.scale.y=Math.hypot(dx,dy);stream.rotation.z=Math.atan2(dx,-dy);st(t);
    hpop(h1,.0,t,.25);hpop(h2,.25,t,.25);
    const e=ease(t/2.7);cam(40,[lerp(.3,.2,e),lerp(2.0,1.95,e),lerp(5.4,5.0,e)],[0,1.75,0])}}});

// 1. "…three days straight, here's what happens inside your body." — heart monitor spiking as he drinks
shot(wordT(0,'three')-.05,()=>{const st0=wordT(0,'three')-.05;const s=studio2('#173049','#04080f');
  const k=kid(s);k.root.position.set(-.45,.95,0);k.root.rotation.y=.35;k.face('happy');const m=mug(k.arms[0].el,{h:.42,r:.2});m.position.set(0,-.55,.08);
  const mon=monitor(s,1.25);mon.position.set(.55,2.05,-.4);mon.rotation.y=-.25;
  return{s,u(t){const a=k.arms[0];const q=sstep(t/.5);a.sh.rotation.x=lerp(0,-1.9,q);a.sh.rotation.z=.25;a.el.rotation.x=lerp(0,-1.2,q);
    mon.setECG(t,lerp(72,128,sstep(t/2.6)));
    const e=ease(t/3);cam(40,[lerp(.25,.15,e),1.75,lerp(5.4,5.0,e)],[.05,1.55,0])}}});

// 2-3. receptor close-up: caffeine plugs the receptors, adenosine (sleep signal) bounces off
function receptorScene(mode,st){const s=studio2('#2a1f55','#07051a',{floor:false,rimA:0x9a7aff,rimB:0x5fd0ff});
  const mem=RB(s,3.4,.5,2.0,.25,sm(0x7a4fc0,.6),0,0,0);const xs=[-.9,0,.9];const cups=xs.map(x=>{const c=grp(s,x,.25,.2);cyl(c,.26,.2,.3,sm(0x3fd0a0,.4),0,.12,0,24);const r=new THREE.Mesh(new THREE.TorusGeometry(.27,.05,10,28),sm(0x6fffd0,.3));r.rotation.x=Math.PI/2;r.position.y=.28;c.add(r);return c});
  const caf=xs.map(x=>{const m=molecule(s,0x8a4a1c,.18);return m});const ado=xs.map(x=>molecule(s,0x3a8fff,.18));
  const cafT=wordT(1,'blocks')-st;
  return{s,u(t){xs.forEach((x,i)=>{const c=caf[i];if(mode==='block'){const q=sstep((t-cafT+.35+i*.12)/.45);c.position.set(x,lerp(2.6,.62,q),.2);c.rotation.y=t*2+i}
      else{c.position.set(x,.62,.2);c.rotation.y=t*2+i}
      const a=ado[i];if(mode==='bounce'){const u=((t*.9+i*.33)%1);const y=u<.5?lerp(2.4,.98,u/.5):lerp(.98,2.4,(u-.5)/.5);a.position.set(x+(u>.5?(u-.5)*1.4*(i-1||1):0),y,.2);a.visible=true}else a.visible=false});
    const e=ease(t/2);cam(40,[lerp(.3,.2,e),lerp(2.4,2.3,e),lerp(7.0,6.6,e)],[0,1.05,0])}}}
shot(L(1)-.1,()=>{const st=L(1)-.1;const R=receptorScene('block',st);const h=hud('CAFFEINE BLOCKS',{yf:.86,wf:.78,fg:'#ffffff'});const h2=hud('ADENOSINE',{yf:.79,wf:.56,fg:'#6fb8ff'});
  return{s:R.s,u(t){R.u(t);hpop(h,.05,t);hpop(h2,wordT(1,'adenosine')-st,t)}}});
shot(wordT(1,'the')-.05,()=>{const st=wordT(1,'the')-.05;const R=receptorScene('bounce',st);const h=hud('SLEEP SIGNAL: BLOCKED',{yf:.85,wf:.84,fg:'#ffffff',bg:'#d8423a',stroke:null,size:130});
  return{s:R.s,u(t){R.u(t);hpop(h,.15,t)}}});

// 4. "Your dopamine spikes, focus sharpens…" — x-ray brain firing fast
shot(L(2)-.1,()=>{const st=L(2)-.1;const X=xrayScene('normal');const sp=[];for(let i=0;i<30;i++){const g=glow(X.B,0xffd23a,.5,.9);g.position.copy(brainPt(i*4.3+.7)).multiplyScalar(1.15);sp.push(g)}
  const h1=hud('DOPAMINE SPIKE',{yf:.86,wf:.78,fg:'#ffd23a'});const h2=hud('FOCUS SHARPENS',{yf:.79,wf:.7,fg:'#ffffff'});
  return{s:X.s,u(t){updPulses(X.pulses,t,2.6);X.M.emissiveIntensity=.5+.3*Math.sin(t*20);sp.forEach((g,i)=>{g.material.opacity=Math.max(0,Math.sin(t*9+i*1.7))*.9});
    hpop(h1,wordT(2,'dopamine')-st,t);hpop(h2,wordT(2,'focus')-st,t);
    const e=ease(t/2.5);cam(30,[lerp(1.2,1.0,e),2.2,lerp(3.5,3.2,e)],[0,2.05,0])}}});

// 5. "…and you feel INVINCIBLE." — hero pose, golden aura
shot(wordT(2,'feel')-.12,()=>{const st=wordT(2,'feel')-.12;const s=studio2('#7a5410','#120a02',{rimA:0xffe27a,rimB:0xffa040,key:2.8});
  const k=kid(s);k.root.position.set(0,.95,0);k.face('happy');k.look(0,.3);const aura=glow(s,0xffd23a,3.6,.7);aura.position.set(0,1.6,-.4);
  const bolts=[];for(let i=0;i<8;i++){const b=RB(s,.06,.7,.06,.02,new THREE.MeshBasicMaterial({color:0xfff2a0}),0,0,0);const a=i/8*Math.PI*2;b.position.set(Math.cos(a)*1.25,1.5+Math.sin(a)*1.25,-.2);b.rotation.z=a+Math.PI/2;bolts.push(b)}
  const h=hud('INVINCIBLE',{yf:.84,wf:.84,fg:'#ffd23a'});const tI=wordT(2,'invincible')-st;
  return{s,u(t){const q=sstep((t-tI+.2)/.3);k.arms.forEach(a=>{a.sh.rotation.z=a.s*lerp(.12,1.55,q);a.el.rotation.z=a.s*lerp(0,1.6,q)});k.root.position.y=.95+q*.08*Math.abs(Math.sin(t*8));
    bolts.forEach((b,i)=>{b.visible=t>tI&&Math.sin(t*25+i*2)>0});aura.material.opacity=.4+.4*q;hpop(h,tI,t,.25);
    camS(40,[0,1.6,lerp(5.4,5.0,ease(t/1.5))],[0,1.45,0],t,[tI],.06)}}});

// 6. "By day two, the diuretic effect…" — clock racing, water draining
shot(L(3)-.1,()=>{const st=L(3)-.1;const s=studio2('#22355f','#060a16');const k=kid(s);k.root.position.set(-.35,.95,0);k.root.rotation.y=.25;k.face('neutral');k.tired(.3);
  const clk=wallClock(s,.34);clk.position.set(.72,2.5,-.2);
  const gauge=grp(s,.72,0,0);RB(gauge,.42,1.7,.3,.18,new THREE.MeshStandardMaterial({color:0xffffff,transparent:true,opacity:.25,roughness:.1}),0,.95,0);const wat=RB(gauge,.34,1.6,.22,.14,sm(0x3aa0ff,.2),0,.95,0);
  const h=hud('DAY 2',{yf:.86,wf:.5,fg:'#ffd23a'});const h2=hud('WATER LOSS',{yf:.79,wf:.6,fg:'#6fb8ff'});const tD=wordT(3,'diuretic')-st;
  return{s,u(t){clk.setTime(24+t*8);const lv=1-.6*sstep((t-tD)/1.4);wat.scale.y=lv;wat.position.y=.15+.8*lv;hpop(h,.05,t);hpop(h2,tD,t);
    const e=ease(t/2);cam(40,[lerp(.25,.15,e),1.85,lerp(6.0,5.6,e)],[0,1.7,0])}}});

// 7. "…and pure acidity kick in." — x-ray stomach, acid bubbles
function stomachShot(st,mode){const s=studio2(mode==='irr'?'#4a1420':'#1d2a3a',mode==='irr'?'#0a0204':'#04070c',{floor:false,rimA:mode==='irr'?0xff6a5a:0x7affc0});
  const g=stomach(s);g.position.set(-.1,1.5,0);g.scale.setScalar(.9);const {M,bub}=g.userData;
  return{s,g,u(t){bub.forEach(q=>{const u=(t*.8+q.ph)%1;q.s.position.set(q.x,lerp(-.15,.42,u),.15);q.s.material.opacity=Math.sin(u*Math.PI)*.85});
    if(mode==='irr'){const p=.5+.5*Math.sin(t*9);M.color.setRGB(1,.35+.2*p,.4);M.emissiveIntensity=.25+.35*p}g.rotation.y=Math.sin(t*1.2)*.15;
    const e=ease(t/1.8);cam(40,[lerp(.3,.2,e),1.9,lerp(6.8,6.4,e)],[.1,1.55,0])}}}
shot(wordT(3,'pure')-.1,()=>{const st=wordT(3,'pure')-.1;const S=stomachShot(st,'acid');const h=hud('PURE ACID',{yf:.85,wf:.62,fg:'#d8ff3a'});
  return{s:S.s,u(t){S.u(t);hpop(h,wordT(3,'acidity')-st,t)}}});
// 8. "Your stomach lining gets irritated,"
shot(L(4)-.1,()=>{const st=L(4)-.1;const S=stomachShot(st,'irr');const h=hud('IRRITATED LINING',{yf:.85,wf:.8,fg:'#ffffff',bg:'#d8423a',stroke:null,size:130});
  return{s:S.s,u(t){S.u(t);hpop(h,wordT(4,'irritated')-st-.1,t)}}});
// 9. "hand tremors start," — shaking hands, sloshing mug
shot(wordT(4,'hand')-.1,()=>{const st=wordT(4,'hand')-.1;const s=kitchen('#5a3a2a','#120804');const G=grp(s,0,1.5,0);const m=mug(G,{h:.8,r:.4,fill:.75});m.position.set(0,-.35,0);
  const hl=hand(G,1);hl.position.set(-.5,0,.05);hl.rotation.z=-.25;const hr=hand(G,-1);hr.position.set(.5,0,.05);hr.rotation.z=.25;
  const drops=[];for(let i=0;i<10;i++)drops.push({m:SPH(s,.05,sm(COF,.2),0,0,0,8),ph:i/10,x:(i-5)*.08});
  const h=hud('TREMORS',{yf:.85,wf:.62,fg:'#ffffff'});
  return{s,u(t){G.position.set(Math.sin(t*47)*.035,1.5+Math.sin(t*39)*.03,0);G.rotation.z=Math.sin(t*31)*.04;m.userData.cof.rotation.y=t;
    drops.forEach(d=>{const u=(t*1.4+d.ph)%1;d.m.position.set(G.position.x+d.x*(1+u*2),1.95+u*.8-u*u*2.2,.1);d.m.visible=u<.9});hpop(h,.12,t);
    cam(40,[0,1.6,lerp(4.6,4.3,ease(t/1.2))],[0,1.45,0])}}});
// 10. "…and your heart rate enters sustained overdrive." — pounding heart + ECG
shot(wordT(4,'heart')-.15,()=>{const st=wordT(4,'heart')-.15;const s=studio2('#3a0d16','#080104',{rimA:0xff5a5a,rimB:0xff9a6a});
  const hr=heart(s);hr.position.set(0,1.35,0);hr.scale.setScalar(.85);const mon=monitor(s,1.55);mon.position.set(0,2.75,-.3);
  const h=hud('OVERDRIVE',{yf:.88,wf:.66,fg:'#ff4a3a'});
  return{s,u(t){const bpm=lerp(120,175,sstep(t/1.8));const ph=(t*bpm/60)%1;const k=1+.13*Math.exp(-ph*9)-.03*Math.exp(-((ph-.3)**2)*80);hr.scale.setScalar(.85*k);hr.userData.M.emissiveIntensity=.2+.5*Math.exp(-ph*7);
    mon.setECG(t,bpm);hpop(h,wordT(4,'overdrive')-st,t);
    camS(40,[.2,2.0,lerp(5.9,5.5,ease(t/2))],[0,1.95,0],t,[],0)}}});

// 11. "By day three, massive caffeine overload…" — surrounded by empty mugs
shot(L(5)-.1,()=>{const st=L(5)-.1;const B=bedroom();const k=kid(B.s);k.root.position.set(-.1,.95,.2);k.tired(1);k.face('tired');k.lid(.15);k.look(.3,-.2);
  const mugs=[];setSeed(17);for(let i=0;i<26;i++){const a=rnd()*Math.PI*2,r=.75+rnd()*1.1;const m=mug(B.s,{h:.3,r:.13,fill:.2,col:[0xf4efe6,0xd8423a,0x3a6fd0,0xf2b33a][i%4]});m.position.set(-.1+Math.cos(a)*r,0,.2+Math.sin(a)*r*.6);m.rotation.y=rnd()*6;mugs.push({m,at:i/26})}
  const h=hud('DAY 3',{yf:.86,wf:.5,fg:'#ffd23a'});const h2=hud('CAFFEINE OVERLOAD',{yf:.79,wf:.8,fg:'#ffffff',bg:'#d8423a',stroke:null,size:130});
  return{s:B.s,u(t){mugs.forEach(q=>{const k2=clamp((t*1.6-q.at*1.4)/.25);q.m.visible=k2>0;q.m.scale.setScalar(Math.max(.001,back(k2)))});
    k.head.rotation.z=Math.sin(t*14)*.03;hpop(h,.05,t);hpop(h2,wordT(5,'massive')-st,t);
    const e=ease(t/2.2);cam(40,[lerp(.6,.45,e),lerp(2.6,2.5,e),lerp(5.8,5.4,e)],[-.05,1.75,0])}}});
// 12. "…combined with zero deep sleep" — wide awake in bed at 4 AM
shot(wordT(5,'combined')-.1,()=>{const st=wordT(5,'combined')-.1;const B=bedroom();const k=kid(B.s);k.root.rotation.x=-Math.PI/2;k.root.position.set(1.25,.82,-1.25);k.lid(-.1);k.face('shock');k.tired(1);
  B.blanket.scale.y=5;B.blanket.position.set(0,.82,.42);const clk=wallClock(B.s,.32);clk.position.set(.35,1.6,-2.3);
  const h=hud('0 HOURS DEEP SLEEP',{yf:.85,wf:.84,fg:'#ffffff'});
  return{s:B.s,u(t){clk.setTime(4+t*.8);clk.lookAt(camera.position);k.look(Math.sin(t*3)*.8,0);hpop(h,wordT(5,'zero')-st,t);
    const e=ease(t/2);cam(42,[lerp(2.6,2.5,e),lerp(3.9,3.7,e),lerp(.6,.4,e)],[.95,1.0,-1.9])}}});
// 13. "…can trigger hallucinations" — warped room, floating mugs
shot(wordT(5,'hallucinations')-.1,()=>{const st=wordT(5,'hallucinations')-.1;const B=bedroom();const k=kid(B.s);k.root.position.set(-.1,.95,.1);k.tired(1);k.face('shock');k.lid(-.15);
  const fl=[];for(let i=0;i<7;i++){const m=mug(B.s,{h:.36,r:.16,col:[0xf2b33a,0xd8423a,0x3fd0a0,0xb06aff][i%4]});faceEyes(m,.17,.07,.05);fl.push(m)}
  const hemi=B.s.children.find(o=>o.isHemisphereLight);const h=hud('HALLUCINATIONS',{yf:.85,wf:.82,fg:'#d89aff'});
  return{s:B.s,u(t){fl.forEach((m,i)=>{const a=t*1.4+i/7*Math.PI*2;m.position.set(-.1+Math.cos(a)*1.0,1.9+Math.sin(a*2)*.35,.1+Math.sin(a)*.6);m.rotation.set(Math.sin(t+i),t*2,Math.cos(t*1.3+i)*.5);m.scale.setScalar(1+.25*Math.sin(t*5+i))});
    hemi.color.setHSL((t*.35)%1,.8,.6);k.head.rotation.z=Math.sin(t*3)*.12;hpop(h,.12,t);
    cam(40,[Math.sin(t*1.7)*.25,2.1,5.4+Math.sin(t*2.3)*.2],[-.1,1.55,0]);camera.rotateZ(Math.sin(t*2.1)*.07)}}});
// 14. "…and extreme paranoia." — shadow figures with red eyes
shot(wordT(5,'paranoia')-.12,()=>{const st=wordT(5,'paranoia')-.12;const s=studio2('#1a1024','#020104',{hemi:.5,key:1.4,rimA:0xff3a3a,rimB:0x6a3aff});
  const k=kid(s);k.root.position.set(0,.95,.3);k.tired(1);k.face('shock');k.lid(-.15);
  const sh=[[-1.25,-.6],[1.25,-.6],[-.65,-1.4],[.65,-1.4]].map(([x,z])=>{const m=shadowMan(s);m.position.set(x,0,z);m.lookAt(0,0,.3);return m});
  const h=hud('PARANOIA',{yf:.85,wf:.66,fg:'#ff4a3a'});
  return{s,u(t){sh.forEach((m,i)=>{m.position.x*=1;m.position.y=Math.sin(t*2+i)*.04;m.scale.setScalar(.9+.1*sstep(t/1.2))});k.look(Math.sin(t*6)>0?.9:-.9,0);k.head.rotation.y=Math.sin(t*6)>0?.3:-.3;
    hpop(h,.12,t);camS(40,[0,2.1,lerp(5.6,5.2,ease(t/1.2))],[0,1.4,-.3],t,[.12],.05)}}});

// 15. "Your brain completely overloads." — red x-ray brain, sparks, glitch
shot(L(6)-.1,()=>{const st=L(6)-.1;const X=xrayScene('normal');X.M.color.setHex(0xff6a6a);X.M.emissive.setHex(0xff1a1a);const sp=[];for(let i=0;i<40;i++){const g=glow(X.B,i%2?0xff3a2a:0xffd23a,.7,1);g.position.copy(brainPt(i*2.9+.2)).multiplyScalar(1.2);sp.push(g)}
  const h=hud('OVERLOAD',{yf:.85,wf:.7,fg:'#ffffff',bg:'#d8423a',stroke:null,size:150});const tO=wordT(6,'overloads')-st;
  return{s:X.s,u(t){updPulses(X.pulses,t,4.5);X.M.emissiveIntensity=.6+.5*Math.abs(Math.sin(t*14));sp.forEach((g,i)=>{g.material.opacity=Math.random()<.5?1:0});X.B.rotation.z=Math.sin(t*30)*.04*sstep((t-tO)/.2);
    hpop(h,tO,t,.2);m0(t)}};function m0(t){camS(30,[1.05,2.2,lerp(3.5,3.25,ease(t/1.8))],[0,2.05,0],t,[tO],.05)}});

// 16. "How many cups of coffee do you drink a day? Let me know below." — cup counter spinning out of control
shot(L(7)-.1,()=>{const st=L(7)-.1;const s=kitchen('#6b3f22','#140904');RB(s,4,.12,2.2,.04,sm(0x6b4a34,.7),0,.9,0);
  const cups=[];for(let i=0;i<15;i++){const row=i<5?0:i<9?1:i<12?2:i<14?3:4;const idx=[0,5,9,12,14][row];const n=[5,4,3,2,1][row];const j=i-idx;
    const m=mug(s,{h:.34,r:.15,col:[0xf4efe6,0xd8423a,0x3a6fd0,0xf2b33a][i%4]});m.position.set((j-(n-1)/2)*.36,.96+row*.36,0);cups.push({m,at:i/15})}
  const cnt=dynTex(1024,256,(g,w,h,v)=>{g.font='900 150px M';g.textAlign='center';g.textBaseline='middle';g.lineJoin='round';g.lineWidth=24;g.strokeStyle='#0b0f1a';const s1=v+' CUPS?';g.strokeText(s1,w/2,h/2);g.fillStyle='#ffd23a';g.fillText(s1,w/2,h/2)});
  const hm=new THREE.Mesh(new THREE.PlaneGeometry(1,.25),new THREE.MeshBasicMaterial({map:cnt.t,transparent:true,depthTest:false,depthWrite:false,fog:false}));hm.renderOrder=30;hm.userData.hud={yf:.85,wf:.74};hm.userData.k=0;CURH.push(hm);
  return{s,u(t){cups.forEach(q=>{const k2=clamp((t*1.3-q.at*1.6)/.25);q.m.visible=k2>0;q.m.scale.setScalar(Math.max(.001,back(k2)))});
    cnt.set(Math.min(99,Math.floor(Math.pow(t*2.6,2.2))+1));hm.userData.k=back(t/.25);
    const e=ease(t/2.4);cam(40,[lerp(.3,.2,e),lerp(2.0,1.9,e),lerp(5.3,4.9,e)],[0,1.6,0])}}});

run(shots,END);
