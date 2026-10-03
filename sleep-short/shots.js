// "11 days without sleep" — clean Zack-D-style knowledge short (rounded characters, x-ray cutaways, glow, dark studios)
import {THREE,camera,cam,loadTiming,run,clamp,ease,eout,back,lerp,V,grp,RB,SPH,sm,cyl,paintTex,setSeed,rnd,carSimple,lamp} from './engine.js';
const T=await loadTiming(); const T0=0.15;
const L=i=>T[i].start+T0, E=i=>T[i].end+T0;
const wordT=(i,w)=>{const x=T[i].words.find(q=>q.w.toLowerCase().replace(/[^a-z0-9]/g,'').startsWith(w));return (x?x.start:T[i].start)+T0};
const shots=[];const shot=(start,build)=>shots.push({start,build:()=>{const i=build();const u=i.u;i.u=(t)=>{BB.clear();u(t);BB.forEach(m=>m.quaternion.copy(camera.quaternion))};return i}});
const END=E(T.length-1)+0.06;

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

// ================= SHOTS =================
const P0={fov:30,pos:[.3,2.08,2.8],look:[0,1.95,-.2]};
function boyScene(){const B=bedroom();const k=kid(B.s);k.root.position.set(-.15,.95,-.2);k.root.rotation.y=.1;k.tired(1);k.face('tired');k.look(.15,-.35);return{B,k}}
const boyPose=(k,nod,lids)=>{k.head.rotation.x=nod;k.torso.rotation.x=nod*.3;k.lid(lids)};

// 0. HOOK — exhausted boy nodding off, snaps awake (frame 0 already moving)
shot(0,()=>{const {B,k}=boyScene();const day=txt(B.s,'DAY 11',{w:.5,fg:'#ffd23a'});day.position.set(.02,2.5,.45);
  const tE=wordT(0,'eleven');
  return{s:B.s,u(t){const snap=1.0;
    if(t<snap){const p=t/snap;boyPose(k,lerp(.12,.34,p*p),lerp(.5,.93,p));k.face('tired')}
    else{const q=clamp((t-snap)/.12);const tw=Math.pow(Math.max(0,Math.sin(t*8.5)),10)*.35;boyPose(k,lerp(.34,-.07,eout(q))+Math.sin(t*3)*.015,lerp(.93,.08,eout(q))+tw);k.face(t<snap+.35?'shock':'tired')}
    pop(day,tE,t,.3);face2cam(day);
    const e=ease(t/2.2);camS(P0.fov,[lerp(P0.pos[0],.24,e),lerp(P0.pos[1],2.1,e),lerp(P0.pos[2],2.55,e)],[0,lerp(P0.look[1],2.0,e),-.2],t,[snap],.035)}}});

// 1. "Back in 1964, Randy Gardner…" — retro calendar, name tag
shot(L(1)-.1,()=>{const s=studio2('#f6c978','#6e3818',{rimA:0xffe2a8,rimB:0xff8a5a,hemi:1.3});
  const k=kid(s);k.root.position.set(-.5,.95,.2);k.root.rotation.y=.3;k.face('happy');
  const cal=grp(s,.62,1.7,-.3);cal.rotation.y=-.22;RB(cal,1.25,1.65,.08,.04,sm(0xfbf8ef,.7));RB(cal,1.25,.42,.12,.04,sm(0xd8423a,.6),0,.62,0);
  const yr=txt(cal,'1964',{w:1.05,fg:'#ffffff',stroke:'#7a1a10',sw:14});yr.position.set(0,.62,.07);
  for(const x of[-.35,.35]){const r=new THREE.Mesh(new THREE.TorusGeometry(.06,.018,8,16),sm(0x666666,.3));r.position.set(x,.84,.05);cal.add(r)}
  const pages=[];for(let i=0;i<6;i++){const pv=grp(cal,0,.38,.07+.006*(6-i));const pg=txt(pv,'DAY '+(i+1),{w:1.12,cw:1024,ch:880,fg:'#22283a',stroke:null,bg:'#fdfbf4',radius:20,size:230});pg.position.y=-.5;pg.material.depthWrite=true;pages.push(pv)}
  const tag=txt(s,'RANDY GARDNER, 17',{w:1.5,bg:'#d8423a',fg:'#ffffff',stroke:null,size:120});tag.position.set(-.45,2.72,.4);
  const tR=wordT(1,'randy')-(L(1)-.1);
  return{s,u(t){pages.forEach((pv,i)=>{const t0=.25+i*.32,q=clamp((t-t0)/.35);pv.rotation.x=-q*2.6;pv.position.y=.38+q*.5;pv.visible=q<.98});
    const a=k.arms[0];a.sh.rotation.z=2.5+Math.sin(t*7)*.12;a.el.rotation.z=.9;k.root.position.y=.95+Math.abs(Math.sin(t*5))*.04;
    pop(tag,tR,t,.3);face2cam(tag);
    const e=ease(t/2.6);cam(40,[lerp(.55,.45,e),lerp(1.7,1.65,e),lerp(5.3,4.8,e)],[.12,1.35,0])}}});

// 2. "…stayed awake for 264 hours" — giant clock, hour counter racing up
shot(wordT(1,'stayed')-.08,()=>{const s=studio2('#22355f','#060a16');const st=wordT(1,'stayed')-.08;
  const k=kid(s);k.root.position.set(0,.95,.4);k.face('neutral');k.look(0,.6);
  const clk=wallClock(s,.5);clk.position.set(0,3.05,-.3);const hal=glow(s,0x5fb2ff,2.4,.55);hal.position.set(0,3.05,-.45);
  const cnt=dynTex(1024,256,(g,w,h,v)=>{g.font='900 150px M';g.textAlign='center';g.textBaseline='middle';g.lineJoin='round';g.lineWidth=24;g.strokeStyle='#0b0f1a';
    const s1=v+' HOURS';g.strokeText(s1,w/2,h/2);g.fillStyle=v>=264?'#ffd23a':'#ffffff';g.fillText(s1,w/2,h/2)});
  const cm=new THREE.Mesh(new THREE.PlaneGeometry(1.45,.36),new THREE.MeshBasicMaterial({map:cnt.t,transparent:true,depthWrite:false}));cm.position.set(0,3.78,-.2);s.add(cm);
  const tH=wordT(1,'hours')-st;
  return{s,u(t){const p=clamp(t/tH);const hrs=Math.round(264*(1-Math.pow(1-p,2)));cnt.set(hrs);clk.setTime(hrs);
    k.tired(p*.8);k.lid(p*.35);k.face(p>.6?'tired':'neutral');pop(cm,0,t,.25);
    const e=ease(t/2.4);cam(40,[.25,lerp(2.45,2.55,e),lerp(4.1,3.7,e)],[0,2.55,0])}}});

// 3. "After just one day, his brain worked like…" — x-ray: brain slowing down
shot(L(2)-.1,()=>{const X=xrayScene('normal');const st=L(2)-.1;const lab=txt(X.s,'24 HOURS AWAKE',{w:.42,fg:'#ffd23a'});lab.position.set(.28,2.48,.45);
  const tD=wordT(2,'worked')-st;
  return{s:X.s,u(t){const slow=sstep((t-tD)/.8);updPulses(X.pulses,t,lerp(1.4,.35,slow));X.B.rotation.z=Math.sin(t*2.2)*.12*slow;X.M.emissiveIntensity=lerp(.45,.2,slow);
    X.k.head.rotation.z=Math.sin(t*2.2)*.08*slow;pop(lab,wordT(2,'one')-st,t,.3);face2cam(lab);
    const e=ease(t/2.4);cam(30,[lerp(1.25,1.0,e),2.2,lerp(2.3,2.0,e)],[0,2.0,0])}}});

// 4. "…a drunk driver's" — swerving car
shot(wordT(2,'like')-.05,()=>{const st=wordT(2,'like')-.05;const s=new THREE.Scene();s.background=gradTex('#ff9a5a','#3a2a6a','#c76a8a');s.fog=new THREE.Fog(0x5a3a6a,14,40);
  s.add(new THREE.HemisphereLight(0xffd0b0,0x302040,1.4));const d=new THREE.DirectionalLight(0xffd8b0,2.2);d.position.set(4,8,6);d.castShadow=true;d.shadow.mapSize.set(1024,1024);
  const c=d.shadow.camera;c.left=c.bottom=-6;c.right=c.top=6;d.shadow.bias=-.0008;d.shadow.normalBias=.03;s.add(d);
  const gr=new THREE.Mesh(new THREE.PlaneGeometry(80,120),new THREE.MeshStandardMaterial({color:0x6a8a4a,roughness:1}));gr.rotation.x=-Math.PI/2;gr.receiveShadow=true;s.add(gr);
  const rd=new THREE.Mesh(new THREE.PlaneGeometry(5,120),new THREE.MeshStandardMaterial({color:0x2c2e36,roughness:.9}));rd.rotation.x=-Math.PI/2;rd.position.y=.01;rd.receiveShadow=true;s.add(rd);
  const dash=[];for(let i=0;i<24;i++){const m=RB(s,.12,.02,1.2,.01,sm(0xffe27a,.6),0,.02,0);dash.push(m)}
  const posts=[];for(let i=0;i<14;i++)for(const x of[-3.4,3.4]){const p=grp(s,x,0,0);cyl(p,.06,.06,1.1,sm(0xeeeeee),0,.55,0,6);RB(p,.14,.12,.04,.02,sm(0xd8423a),0,1.0,.04);posts.push({p,i})}
  const car=carSimple(s,0xd8423a);car.rotation.y=Math.PI;const head=SPH(car,.22,sm(0xe9b48c,.55),.35,1.25,-.1,14);
  const lab=txt(s,'= DRUNK DRIVER',{w:2.1,fg:'#ffffff',bg:'#d8423a',stroke:null,size:120});
  return{s,u(t){const v=14;dash.forEach((m,i)=>{m.position.z=-40+((i*3.3+t*v)%79)});posts.forEach(({p,i})=>{p.position.z=-40+((i*5.6+t*v)%79)});
    const x=Math.sin(t*2.6)*1.1,yaw=Math.cos(t*2.6)*.35;car.position.set(x,0,0);car.rotation.y=Math.PI-yaw;car.rotation.z=Math.sin(t*2.6)*.05;
    lab.position.set(1.25,3.0,2.2);pop(lab,wordT(2,'drunk')-st,t,.3);face2cam(lab);
    cam(42,[lerp(2.4,2.0,ease(t/2)),3.4,7.2],[x*.4,1.3,-.5]);camera.rotateZ(Math.sin(t*2.6+1)*.05)}}});

// 5. "Then it started shutting off for seconds…" — x-ray: brain blacking out
shot(L(3)-.1,()=>{const X=xrayScene('normal');const st=L(3)-.1;
  const off=txt(X.s,'OFF',{w:.42,fg:'#ffffff',bg:'#d8423a',stroke:null,size:170});off.position.set(.0,2.5,.45);
  const offs=[[wordT(3,'shutting')-st,.55],[wordT(3,'seconds')-st,.45]];
  return{s:X.s,u(t){let dark=0;for(const[a,d]of offs)if(t>=a&&t<a+d)dark=1;
    updPulses(X.pulses,t,dark?0:1.1,dark?0:1);X.M.emissiveIntensity=dark?0:.4;X.M.color.setHex(dark?0x4a3a44:0xf3a6b8);off.visible=!!dark;off.scale.setScalar(dark?1:0.001);face2cam(off);
    const e=ease(t/2);cam(30,[lerp(-1.1,-.85,e),2.25,lerp(2.2,1.95,e)],[0,2.02,0])}}});

// 6. "…with his eyes still open." — extreme close-up, micro-blackouts
shot(wordT(3,'with')-.05,()=>{const {B,k}=boyScene();const st=wordT(3,'with')-.05;k.root.rotation.y=0;k.face('neutral');k.lid(-.12);k.tired(.9);k.look(0,0);
  k.pupils.forEach(p=>p.scale.setScalar(.8));
  const lab=txt(B.s,'MICROSLEEP',{w:.34,fg:'#ffffff',bg:'#d8423a',stroke:null,size:150});
  const blk=new THREE.Mesh(new THREE.PlaneGeometry(4,4),new THREE.MeshBasicMaterial({color:0x000000,transparent:true,opacity:0,depthTest:false}));blk.renderOrder=10;B.s.add(blk);
  const flashes=[.35,1.05,1.75];
  return{s:B.s,u(t){const e=ease(t/2);cam(30,[0,2.14,lerp(2.2,1.95,e)],[-.15,2.05,-.2]);
    let o=0;for(const f of flashes){const d=t-f;if(d>=0&&d<.32)o=Math.max(o,d<.05?d/.05:d<.22?1:1-(d-.22)/.1)}
    blk.material.opacity=o*.92;blk.position.copy(camera.position).add(V(0,0,-.3).applyQuaternion(camera.quaternion));blk.quaternion.copy(camera.quaternion);
    lab.position.set(-.15,2.36,.4);pop(lab,flashes[0]+.1,t,.3);face2cam(lab)}}});

// 7. "By day four, he thought a street sign was a person." — hallucination
shot(L(4)-.1,()=>{const st=L(4)-.1;const s=new THREE.Scene();s.background=gradTex('#2c2458','#0a0c1c');s.fog=new THREE.Fog(0x0a0c1c,9,24);
  s.add(new THREE.HemisphereLight(0x7a80d0,0x18141c,1.2));const mo=new THREE.DirectionalLight(0xb0c0ff,1.5);mo.position.set(-3,6,5);mo.castShadow=true;mo.shadow.mapSize.set(1024,1024);
  const c=mo.shadow.camera;c.left=c.bottom=-5;c.right=c.top=5;mo.shadow.bias=-.0008;mo.shadow.normalBias=.03;s.add(mo);
  const gr=new THREE.Mesh(new THREE.PlaneGeometry(60,60),new THREE.MeshStandardMaterial({color:0x272a35,roughness:.95}));gr.rotation.x=-Math.PI/2;gr.receiveShadow=true;s.add(gr);
  const sw=RB(s,30,.12,2.2,.03,sm(0x8d8f99,.9),0,.06,-1.1);sw.receiveShadow=true;
  for(let i=0;i<8;i++)RB(s,1.1,.02,.14,.01,sm(0xe8e8e8,.7),-7+i*2,.01,1.6);
  lamp(s,-2.1,-1.6);
  const sign=grp(s,.75,0,-.7);cyl(sign,.05,.05,2.5,sm(0x9aa0a8,.4),0,1.25,0,10);const plate=grp(sign,0,2.45,0);RB(plate,1.05,.34,.06,.03,sm(0x1f8a4c,.6));
  const nm=txt(plate,'MAPLE ST',{w:.9,fg:'#ffffff',stroke:null,size:150});nm.position.z=.04;
  const fc=grp(plate,0,0,.05);for(const x of[-.16,.16]){const w=SPH(fc,.085,sm(0xffffff,.3),x,.02,0,14);w.scale.z=.5;SPH(fc,.04,sm(0x111111,.3),x+.01,.0,.04,10)}
  const sml=new THREE.Mesh(new THREE.TorusGeometry(.09,.02,8,16,Math.PI),sm(0x111111));sml.rotation.z=Math.PI;sml.position.set(0,-.06,.03);fc.add(sml);
  const arms=[];for(const sx of[-1,1]){const a=grp(sign,sx*.05,1.75,0);RB(a,.12,.6,.12,.05,sm(0x1f8a4c,.6),0,-.3,0);SPH(a,.08,sm(0xffffff,.4),0,-.62,0,10);arms.push({a,sx})}
  const aura=glow(s,0xb06aff,2.6,.0);aura.position.set(.75,2.1,-.8);
  const k=kid(s);k.root.position.set(-.6,.95,.1);k.root.rotation.y=.75;k.tired(.8);k.face('happy');k.look(.6,.3);
  const bub=txt(s,'HEY BUDDY!',{w:.9,fg:'#111',bg:'#ffffff',stroke:null,size:130});
  const tP=wordT(4,'person')-st,tT=wordT(4,'thought')-st;
  return{s,u(t){const m=sstep((t-tT)/.5);aura.material.opacity=.75*m*(.8+.2*Math.sin(t*6));nm.material.opacity=1-sstep((t-tP+.15)/.2);
    const fo=t<tP-.15?0:back((t-tP+.15)/.3);fc.scale.setScalar(Math.max(.001,fo));fc.visible=fo>.01;
    arms.forEach(({a,sx})=>{const q=t<tP?0:back((t-tP)/.3);a.scale.setScalar(Math.max(.001,q));a.visible=q>.01;a.rotation.z=sx*(.6+(sx>0?Math.sin(t*12)*.45+1.4:0))});
    sign.rotation.z=Math.sin(t*3)*.04*m;
    const ra=k.arms[0];ra.sh.rotation.z=lerp(.12,2.6,sstep((t-tP)/.25));ra.el.rotation.z=Math.sin(t*12)*.4*sstep((t-tP)/.25);
    bub.position.set(-.55,2.78,.2);pop(bub,tP+.15,t,.3);face2cam(bub);
    const e=ease(t/2.8);cam(44,[lerp(.3,.2,e),lerp(1.75,1.65,e),lerp(6.2,5.7,e)],[.1,1.5,-.3])}}});

// 8a. "Without sleep, his brain couldn't…" — toxic waste builds up
shot(L(5)-.1,()=>{const X=xrayScene('toxic');const st=L(5)-.1;const T1=(L(6)-.1)-st;
  return{s:X.s,u(t){updPulses(X.pulses,t,.7,.7);const p=clamp(t/T1);X.tox.forEach(q=>{const k=clamp((p*1.05-q.at)/.08);q.m.visible=q.g.visible=k>0;q.m.scale.setScalar(Math.max(.001,back(k)))});
    X.M.color.setRGB(lerp(.95,.62,p),lerp(.65,.66,p),lerp(.72,.45,p));
    const e=ease(t/1.9);cam(30,[lerp(1.2,.95,e),lerp(2.35,2.25,e),lerp(2.3,2.05,e)],[0,2.03,0])}}});
// 8b. "…flush out its toxic waste." — closer, label
shot(wordT(5,'flush')-.05,()=>{const X=xrayScene('toxic');const st=wordT(5,'flush')-.05;const st0=L(5)-.1,T1=(L(6)-.1)-st0;
  const lab=txt(X.s,'TOXIC WASTE',{w:.4,fg:'#111',bg:'#7dff3a',stroke:null,size:150});lab.position.set(-.2,2.47,.45);
  return{s:X.s,u(t){updPulses(X.pulses,t,.5,.5);const p=clamp((t+st-st0)/T1);X.tox.forEach(q=>{const k=clamp((p*1.05-q.at)/.08);q.m.visible=q.g.visible=k>0;q.m.scale.setScalar(Math.max(.001,k))});
    X.M.color.setRGB(lerp(.95,.62,p),lerp(.65,.66,p),lerp(.72,.45,p));X.B.rotation.y=Math.sin(t*1.5)*.08;
    pop(lab,wordT(5,'toxic')-st,t,.3);face2cam(lab);
    const e=ease(t/1.6);cam(30,[lerp(-.9,-.75,e),2.25,lerp(1.9,1.7,e)],[0,2.07,0])}}});

// 9. "When he finally crashed…" — face-plant onto the bed
shot(L(6)-.1,()=>{const st=L(6)-.1;const B=bedroom();const k=kid(B.s);k.tired(1);k.face('tired');k.lid(.8);
  const hip=grp(B.s,1.25,0,.25);hip.rotation.y=Math.PI;k.root.position.set(0,.95,0);hip.add(k.root);
  const tC=wordT(6,'crashed')-st;
  return{s:B.s,u(t){const q=clamp((t-tC)/.32),f=q*q;const bo=t>tC+.32?Math.sin((t-tC-.32)*22)*Math.exp(-(t-tC-.32)*9)*.05:0;
    k.root.position.set(0,lerp(.95,.8,f)+bo,lerp(0,.35,f));k.torso.rotation.x=lerp(Math.sin(t*2.5)*.05,Math.PI/2,f);k.legs.forEach(l=>l.rotation.x=lerp(0,.5,f));
    k.arms.forEach(a=>{a.sh.rotation.x=lerp(0,-2.6,f);a.sh.rotation.z=a.s*lerp(.12,.5,f)});k.lid(lerp(.8,1,f));
    camS(40,[lerp(8.6,8.2,ease(t/1.5)),lerp(1.9,1.75,ease(t/1.5)),-.45],[1.25,1.0,-.45],t,[tC+.3],.06)}}});

// 10. "…he slept fourteen hours straight." — top view, Zzz, clock racing
shot(wordT(6,'slept')-.05,()=>{const st=wordT(6,'slept')-.05;const B=bedroom();const k=kid(B.s);k.root.rotation.x=-Math.PI/2;k.root.position.set(1.25,.82,-1.25);k.lid(1);k.face('happy');
  k.arms.forEach(a=>{a.sh.rotation.z=a.s*.05});B.blanket.scale.y=5;B.blanket.position.set(0,.82,.42);
  const clk=wallClock(B.s,.38);clk.position.set(.45,1.55,-2.2);
  const cnt=txt(B.s,'14 HOURS',{w:.8,fg:'#ffd23a'});cnt.position.set(1.45,1.75,-1.4);
  const zs=[];for(let i=0;i<3;i++){const z=txt(B.s,'Z',{w:.35+i*.06,fg:'#bfe0ff',stroke:'#1b2a55',sw:22,size:200});zs.push(z)}
  return{s:B.s,u(t){clk.setTime(t*5.5);clk.lookAt(camera.position);
    zs.forEach((z,i)=>{const u=((t*.7+i/3)%1);z.position.set(1.4+u*.5+Math.sin(u*6+i)*.1,1.05+u*1.1,-2.35);z.material.opacity=Math.sin(u*Math.PI);face2cam(z)});
    pop(cnt,wordT(6,'fourteen')-st,t,.3);face2cam(cnt);B.blanket.position.y=.82+Math.sin(t*2.4)*.012;
    const e=ease(t/1.8);cam(40,[lerp(2.45,2.3,e),lerp(3.5,3.3,e),lerp(-.05,-.25,e)],[1.0,1.05,-2.05])}}});

// 11. "Guinness won't even accept this record anymore," — record book + stamp
shot(L(7)-.1,()=>{const st=L(7)-.1;const s=studio2('#3a2a5a','#0a0614',{rimA:0xffd27a,rimB:0xb06aff,key:2.6});
  const ped=cyl(s,.75,.85,1.0,sm(0x2b2440,.5),0,.5,0,32);const top=cyl(s,.82,.82,.06,sm(0xd9b04a,.3),0,1.03,0,32);
  const bk=grp(s,0,1.12,0);bk.rotation.x=.18;RB(bk,1.62,.06,1.02,.03,sm(0x8a1f2a,.5),0,0,0);
  const lp=grp(bk,-.4,.05,0);lp.rotation.z=.06;RB(lp,.78,.04,.94,.02,sm(0xfbf8ef,.8));const rp=grp(bk,.4,.05,0);rp.rotation.z=-.06;RB(rp,.78,.04,.94,.02,sm(0xfbf8ef,.8));
  const t1=txt(lp,'WORLD',{w:.62,fg:'#8a1f2a',stroke:null,size:190});t1.rotation.x=-Math.PI/2;t1.position.set(0,.03,-.22);
  const t2=txt(lp,'RECORDS',{w:.62,fg:'#8a1f2a',stroke:null,size:170});t2.rotation.x=-Math.PI/2;t2.position.set(0,.03,-.02);
  const t3=txt(rp,'NO SLEEP',{w:.62,fg:'#22283a',stroke:null,size:170});t3.rotation.x=-Math.PI/2;t3.position.set(0,.03,-.24);
  const t4=txt(rp,'264 HRS',{w:.55,fg:'#22283a',stroke:null,size:170});t4.rotation.x=-Math.PI/2;t4.position.set(0,.03,-.05);
  const stamp=txt(rp,'NOT ACCEPTED',{w:.74,fg:'#e02a2a',stroke:'#fbf8ef',sw:10,size:150,cw:1024,ch:300});stamp.rotation.set(-Math.PI/2,0,.22);stamp.position.set(-.02,.04,.2);
  const sb=grp(s,.4,2.6,.3);RB(sb,.36,.14,.24,.04,sm(0xd8423a,.5),0,0,0);RB(sb,.08,.4,.08,.03,sm(0x3a2a1a,.6),0,.27,0);SPH(sb,.1,sm(0x3a2a1a,.6),0,.5,0,12);
  const halo=glow(s,0xffd27a,3.4,.5);halo.position.set(0,1.6,-1.2);
  const tA=wordT(7,'accept')-st;
  return{s,u(t){const dn=sstep((t-(tA-.3))/.25),up=sstep((t-(tA+.08))/.3);sb.position.y=lerp(2.6,1.32,dn)+up*1.4;sb.visible=t<tA+.6;
    pop(stamp,tA,t,.2,1);bk.rotation.y=Math.sin(t*.8)*.05;
    camS(40,[lerp(0,.06,ease(t/2)),lerp(3.0,2.85,ease(t/2)),lerp(4.0,3.75,ease(t/2))],[0,1.22,0],t,[tA],.05)}}});

// 12. "…because nobody should end up like…" — pull back to the boy, land EXACTLY on frame 0 (loop)
shot(wordT(7,'because')-.05,()=>{const st=wordT(7,'because')-.05;const D=END-st;const {B,k}=boyScene();
  return{s:B.s,u(t){const p=clamp(t/D),e=ease(p);boyPose(k,lerp(-.02,.12,sstep(p)),lerp(.2,.5,sstep(p)));
    cam(lerp(36,P0.fov,e),[lerp(1.3,P0.pos[0],e),lerp(2.3,P0.pos[1],e),lerp(5.0,P0.pos[2],e)],[lerp(.4,P0.look[0],e),lerp(1.65,P0.look[1],e),lerp(-.6,P0.look[2],e)])}}});

run(shots,END);
