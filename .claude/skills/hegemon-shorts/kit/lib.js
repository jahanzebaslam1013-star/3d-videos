// Hegemon Shorts helper library: clean rounded 3D explainer look (boy, x-ray brain, studios, props) + screen-pinned HUD titles.
// Usage in shots.js:  import * as K from "./lib.js"; await K.initTimeline(); const {shot,hud,hpop,L,E,wordT,...}=K;  ...  K.go();
import {faceEyes,W,H,THREE,camera,cam,loadTiming,run,clamp,ease,eout,back,lerp,V,grp,RB,SPH,sm,cyl,paintTex,setSeed,rnd,carSimple,lamp} from './engine.js';
export let T=null,T0=0.15,END=0;
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
export async function initTimeline({t0=0.15,tail=0.25}={}){T=await loadTiming();T0=t0;END=E(T.length-1)+tail;return{T,END}}
export const go=()=>run(shots,END);
export function hudMesh(m,{yf=.8,wf=.76}={}){m.material.depthTest=false;m.material.fog=false;m.renderOrder=30;m.userData.hud={yf,wf};m.userData.k=0;CURH.push(m);return m}

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

export {E,face2cam,BB,COF,GLOW,HEADY,L,bedroom,brain,brainPt,camS,clockTex,dynTex,ecgDraw,glow,gradTex,hand,heart,hpop,hud,kid,kitchen,molecule,monitor,mug,pop,shadowMan,shakeT,shot,shots,sstep,steam,stomach,studio2,txt,updPulses,wallClock,wordT,xrayScene};
