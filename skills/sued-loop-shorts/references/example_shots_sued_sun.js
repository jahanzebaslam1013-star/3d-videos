// "He Sued the Sun" — loop short. Last frame of the final shot == first frame of shot 0.
// Every sign/label goes through face() -> fitToFrame(): it is kept fully inside the frame AND above the subtitle band.
import {THREE,renderer,W,H,camera,cam,loadTiming,run,clamp,ease,eout,back,lerp,V,box,cyl,grp,mat,lights,makeMan,flail,paintTex,textTex,
  canvasTex,label,skyScene,cloud,setSeed,rnd,RB,SPH,sm,sunDisc,sunFace,earthChar,stars,nightSky,beachWorld,lounger,poolGuy,umbrella,fitToFrame} from './engine.js';
const T=await loadTiming(); const T0=0;
const L=i=>T[i].start+T0, E=i=>T[i].end+T0;
const wordT=(i,w)=>{const x=T[i].words.find(q=>q.w.toLowerCase().replace(/[^a-z0-9]/g,'').startsWith(w));if(!x)throw new Error('word '+w);return x.start+T0};
const END=32.64;const PI=Math.PI;
const CAP_Y=-0.27;   // NDC y of the top of the subtitle band: signs must stay above this
const LOOK=[];const face=(o,rz=0)=>LOOK.push([o,rz]);
const shots=[];
const shot=(start,build)=>shots.push({start,build:()=>{const I=build();const u=I.u;I.u=t=>{LOOK.length=0;
  renderer.setScissorTest(false);renderer.setViewport(0,0,W,H);
  u(t);camera.aspect=W/H;camera.updateProjectionMatrix();
  for(const [o,rz] of LOOK){o.lookAt(camera.position);if(rz)o.rotateZ(rz);fitToFrame(o,.07,camera,CAP_Y)}};return I}});
const shake=(t,t0,a=.12,d=.3)=>{const k=t-t0;if(k<0||k>d)return 0;return Math.sin(k*90)*a*(1-k/d)};
const pop=(t,t0,d=.25)=>t<t0?0:back((t-t0)/d);
const PAPER='#fbf8ef';

// ---------- text props ----------
function canvasTexOnce(w,h,draw){const c=canvasTex(w,h,draw);c.draw();return c.tex}
function fitFont(g,txt,max,w,wt=900){g.font=`${wt} ${max}px M`;const k=Math.min(1,w/g.measureText(txt).width);const fs=Math.floor(max*k);g.font=`${wt} ${fs}px M`;return fs}
function folder(p,w=1.15,h=.85,t=.2){const g=grp(p);box(g,w,h,t,0xd9a94e,0,0,0);box(g,w-.08,h-.1,t+.02,0xfbf8ef,0,-.03,0);box(g,w*.3,.1,t+.04,0xd9a94e,-w*.3,h/2+.03,0);
  const lb=label(g,'',w*.9,h*.62,{});lb.material.map=canvasTexOnce(512,350,(c,W,H)=>{c.fillStyle='#d9a94e';c.fillRect(0,0,W,H);c.fillStyle='#fff7e0';c.fillRect(18,18,W-36,H-36);
    c.textAlign='center';c.fillStyle='#d23a2a';c.font='900 92px M';c.fillText('LAWSUIT',W/2,140);c.fillStyle='#1b2330';fitFont(c,'ME vs. THE SUN',66,W-70);c.fillText('ME vs. THE SUN',W/2,250)});
  lb.position.z=t/2+.025;return g}
function stamp(p,txt,w=1.2,col='#d23a2a'){const m=label(p,'',w,w*.38,{});m.material.map=canvasTexOnce(512,196,(g,W,H)=>{g.strokeStyle=col;g.lineWidth=16;g.strokeRect(10,10,W-20,H-20);
  g.fillStyle=col;fitFont(g,txt,116,W-70);g.textAlign='center';g.textBaseline='middle';g.fillText(txt,W/2,H/2+6)});return m}
function sign(p,txt,w,col='#d23a2a',fg='#fff',fs=110){const m=label(p,'',w,w*.36,{});m.material.map=canvasTexOnce(560,200,(g,W,H)=>{g.fillStyle=col;g.beginPath();g.roundRect(6,6,W-12,H-12,36);g.fill();
  g.strokeStyle='#fff';g.lineWidth=8;g.beginPath();g.roundRect(16,16,W-32,H-32,28);g.stroke();g.fillStyle=fg;fitFont(g,txt,fs,W-70);g.textAlign='center';g.textBaseline='middle';g.fillText(txt,W/2,H/2+6)});return m}
function bub(p,lines,w=2,fs=84){const m=label(p,'',w,w*.62,{});m.material.map=canvasTexOnce(560,348,(g,W,H)=>{g.fillStyle='#fff';g.strokeStyle='#111';g.lineWidth=8;
  g.beginPath();g.roundRect(10,10,W-20,H-90,60);g.fill();g.stroke();g.beginPath();g.moveTo(150,H-84);g.lineTo(110,H-12);g.lineTo(230,H-84);g.closePath();g.fill();g.stroke();
  g.fillStyle='#fff';g.fillRect(150,H-92,80,14);g.fillStyle='#111';g.textAlign='center';g.textBaseline='middle';
  lines.forEach((l,i)=>{fitFont(g,l,fs,W-80);g.fillText(l,W/2,(H-80)/2+(i-(lines.length-1)/2)*fs*1.05+4)})});return m}
function hookText(p){const m=label(p,'',1.6,.8,{});m.material.map=canvasTexOnce(1024,512,(g,W,H)=>{g.textAlign='center';g.textBaseline='middle';g.lineJoin='round';
  for(const [txt,y,col] of [['HE SUED',150,'#ffffff'],['THE SUN?!',360,'#ffd52e']]){fitFont(g,txt,190,W-80);g.lineWidth=30;g.strokeStyle='#111';g.strokeText(txt,W/2,y);g.fillStyle=col;g.fillText(txt,W/2,y)}});
  m.material.depthTest=false;m.renderOrder=10;return m}

// ---------- characters ----------
const BURN=0xd8442e,SKIN=0xd7a07a,ICE=0x9fd0ea;
function sunburnt(m){m.skinM.color.setHex(BURN);m.skinM.emissive=new THREE.Color(0x000000);return m}
function judgeMan(p){const m=makeMan(p,{suit:0x15161c});const w=0xf2f0ea;
  box(m.head,.36,.14,.36,w,0,.48,-.01);for(const s of[-1,1])for(const y of[.38,.26,.14])box(m.head,.09,.1,.3,w,s*.19,y,-.03);box(m.head,.3,.36,.1,w,0,.22,-.2);
  box(m.torso,.62,.74,.34,0x0c0d12,0,.37,0);box(m.torso,.12,.1,.02,0xffffff,0,.7,.175);
  const gv=grp(m.arms[0].el,0,-.42,0);cyl(gv,.035,.035,.55,0x5a3418,0,0,-.22,8).rotation.x=PI/2;const hd=cyl(gv,.09,.09,.3,0x4a2a12,0,0,-.5,12);hd.rotation.z=PI/2;
  m.face('neutral');m.gavel=gv;m.gHead=hd;return m}
function shades(m){const g=grp(m.head);for(const s of[-1,1])box(g,.12,.07,.02,0x111111,s*.07,.28,.16);box(g,.06,.02,.02,0x111111,0,.29,.16);return g}
function sunChar(p,size=2.4){const g=sunFace(p,size);const glow=new THREE.PointLight(0xffb040,14,9,1.3);glow.position.set(0,0,1.2);g.add(glow);return g}

// ---------- courtroom ----------
function court({judge=false,man=true,sun=false,jury=false,steno=false}={}){const s=new THREE.Scene();s.background=new THREE.Color(0x5e3f26);setSeed(9);
  const fl=new THREE.Mesh(new THREE.PlaneGeometry(30,30),new THREE.MeshLambertMaterial({map:paintTex('#8a5a36',512,512,900,14,6,[30,120])}));fl.rotation.x=-PI/2;fl.receiveShadow=true;s.add(fl);
  const rug=new THREE.Mesh(new THREE.PlaneGeometry(2.4,9),mat(0x8e2a2a));rug.rotation.x=-PI/2;rug.position.set(0,.01,-2.5);rug.receiveShadow=true;s.add(rug);
  const bw=new THREE.Mesh(new THREE.PlaneGeometry(20,10),new THREE.MeshLambertMaterial({map:paintTex('#7a5232',512,512,900,12,3)}));bw.position.set(0,5,7);bw.rotation.y=PI;bw.receiveShadow=true;s.add(bw);
  for(let i=-4;i<=4;i++)box(s,.12,4.2,.1,0x5a3a20,i*1.3,2.1,6.92);box(s,14,.18,.14,0x4a2e16,0,4.25,6.9);
  const fw=new THREE.Mesh(new THREE.PlaneGeometry(20,10),new THREE.MeshLambertMaterial({map:paintTex('#b49a78',512,512,900,12,3)}));fw.position.set(0,5,-7);fw.receiveShadow=true;s.add(fw);
  const doors=[];for(const sx of[-1,1]){const d=grp(s,sx*1.33,0,-6.9);const leaf=grp(d,0,0,0);box(leaf,1.3,2.9,.12,0x5b3b22,-sx*.65,1.45,0);box(leaf,.5,.7,.13,0xbfd8e8,-sx*.65,2.0,.01);doors.push({leaf,sx})}
  box(s,2.8,.2,.15,0x4a2e16,0,2.98,-6.9);
  for(const sx of[-1,1]){const sw=new THREE.Mesh(new THREE.PlaneGeometry(14,10),new THREE.MeshLambertMaterial({map:paintTex('#a88a66',512,512,700,12,3)}));sw.position.set(sx*6,5,0);sw.rotation.y=-sx*PI/2;s.add(sw)}
  for(const z of[-2.3,-3.6,-4.9])for(const sx of[-1,1]){box(s,3.2,.12,.6,0x6e4426,sx*2.9,.5,z);box(s,3.2,.7,.1,0x6e4426,sx*2.9,.85,z-.3)}
  const bench=grp(s,0,0,3.6);box(bench,4.4,1.7,1.2,0x6e4426,0,.85,0);box(bench,4.6,.1,1.4,0x4f2f18,0,1.75,0);for(const x of[-1.5,0,1.5])box(bench,1.2,1.1,.04,0x83532f,x,.85,-.61);
  box(s,3,.5,1.6,0x5a3418,0,.25,4.6);
  const stand=grp(s,-3.1,0,2.4);stand.rotation.y=.5;box(stand,1.5,1.15,1.3,0x6e4426,0,.575,0);box(stand,1.6,.08,1.4,0x4f2f18,0,1.17,0);
  const plaque=label(stand,'',1.1,.26,{});plaque.material.map=canvasTexOnce(560,124,(g,W,H)=>{g.fillStyle='#d9b44a';g.fillRect(0,0,W,H);g.fillStyle='#2a1d12';fitFont(g,'WITNESS',64,W-40);g.textAlign='center';g.textBaseline='middle';g.fillText('WITNESS',W/2,H/2+4)});
  plaque.position.set(0,.85,-.665);plaque.rotation.y=PI;
  for(const sx of[-1,1]){const bn=grp(s,sx*3.4,0,6.85);box(bn,1.1,3.2,.05,0x24345e,0,3.0,0);box(bn,1.1,.14,.06,0xd9b44a,0,1.45,0)}
  const hemi=new THREE.HemisphereLight(0xfff1dc,0x6b4a30,1.5);s.add(hemi);
  const lamp=new THREE.PointLight(0xffe2b0,10,14,1.4);lamp.position.set(0,5,1);s.add(lamp);
  const d=new THREE.DirectionalLight(0xfff3dd,1.7);d.position.set(4,12,-3);d.target.position.set(0,1,2);s.add(d.target);d.castShadow=true;d.shadow.mapSize.set(2048,2048);
  const c=d.shadow.camera;c.left=c.bottom=-9;c.right=c.top=9;c.near=.5;c.far=80;d.shadow.bias=-.0015;d.shadow.normalBias=.03;s.add(d);
  const R={s,bench,stand,doors,hemi,lamp,dir:d};
  if(judge){const j=judgeMan(s);j.legs.rotation.x=PI/2;j.root.position.set(0,1.52,4.35);j.root.rotation.y=PI;R.judge=j}
  if(man){const m=sunburnt(makeMan(s));m.legs.rotation.x=PI/2;m.root.position.set(0,1.02,2.2);m.face('angry');R.man=m}
  if(sun){const su=sunChar(s,2.2);su.position.set(-3.1,2.5,2.4);R.sun=su}
  if(jury){const jb=grp(s,4.0,0,1.6);jb.rotation.y=PI+.55;box(jb,3.4,.9,.15,0x6e4426,0,.45,.75);R.jurors=[];const suits=[0x2f5d3a,0x6a3a7a,0x2b4a7a,0x7a4a2a,0x3a3a3a,0x8a2a2a];
    for(let i=0;i<6;i++){const r=Math.floor(i/3),cI=i%3;const m=makeMan(jb,{suit:suits[i]});m.legs.rotation.x=0;m.root.position.set(-1.05+cI*1.05,.47+r*.5,.1-r*.7);const sg=shades(m);sg.visible=false;R.jurors.push({m,sg})}}
  if(steno){const st=grp(s,2.2,0,1.6);st.rotation.y=PI-.4;box(st,.9,.08,.6,0x4f2f18,0,.8,.35);for(const x of[-.4,.4])box(st,.06,.8,.06,0x4f2f18,x,.4,.35);
    const mach=box(st,.4,.12,.3,0x2b2f38,0,.9,.35);const m=makeMan(st,{suit:0x3a6a8a});m.legs.rotation.x=0;m.root.position.set(0,.47,-.15);R.steno=m}
  return R}
function holdOverhead(m,f,a,{flat=0}={}){for(const ar of m.arms){ar.sh.rotation.x=a;ar.sh.rotation.z=ar.s*.18;ar.el.rotation.x=-.25}
  const Lr=.8,r=m.root.position;const y=r.y+.67-Lr*Math.cos(a),z=r.z-Lr*Math.sin(a);
  f.position.set(r.x,y+.25*(1-flat),z+.12+.15*flat);f.rotation.set(-flat*PI/2+(1-flat)*.15,0,0)}
const C0={fov:44,pos:[.25,2.9,6.1],look:[0,2.1,1.8]};
function snow(s,n=260,area=12){const m=new THREE.MeshBasicMaterial({color:0xffffff});const out=[];setSeed(55);
  for(let i=0;i<n;i++){const f=new THREE.Mesh(new THREE.BoxGeometry(.06,.06,.06),m);s.add(f);out.push({f,x:(rnd()-.5)*area,z:(rnd()-.5)*area*.7,ph:rnd()*9,sp:.6+rnd()*.6})}
  return (t,on=1)=>out.forEach(q=>{q.f.visible=on>0&&(q.ph/9)<on;const y=7-((q.ph+t*q.sp*1.4)%9);q.f.position.set(q.x+Math.sin(t+q.ph)*.25,y,q.z)})}

// ===== S0: slam + kinetic hook text (frame 0 == last frame of S9b)
const tSlam=0.15;
shot(0,()=>{const R=court();const {s,man}=R;const f=folder(s);const ht=hookText(s);
  return{s,u(t){const k=clamp(t/tSlam);const a=lerp(-2.7,-1.72,k*k);holdOverhead(man,f,a,{flat:k*k});
    if(t>=tSlam){f.position.set(0,1.9,3.1);f.rotation.set(-PI/2,0,0)}
    man.torso.rotation.x=lerp(0,.28,k*k);man.face('angry');
    ht.visible=t>=tSlam;ht.scale.setScalar(pop(t,tSlam,.22)*(1+Math.sin(t*14)*.025));ht.position.set(0,3.6,2.9);face(ht,Math.sin(t*9)*.04);
    const sk=shake(t,tSlam,.16,.45);const e=ease(t/2.2);
    cam(C0.fov,[C0.pos[0]+sk,C0.pos[1]-e*.15+sk*.7,C0.pos[2]-e*.5],[C0.look[0]+sk*.3,C0.look[1],C0.look[2]])}}});

// ===== S1: "His sunburn was so bad, his face glowed in the dark."
shot(L(1)-.06,()=>{const R=court();const {s,man,hemi,lamp,dir}=R;man.root.position.set(0,1.02,2.2);man.face('sad');
  const glow=new THREE.PointLight(0xff3a1a,0,4,1.5);glow.position.set(0,2.4,2.8);s.add(glow);
  const t0=L(1)-.06,tg=wordT(1,'glowed')-t0;const sg=sign(s,'SPF 0',.9,'#d23a2a');
  return{s,u(t){const dk=clamp((t-tg+.15)/.2);hemi.intensity=1.5*(1-dk*.93);lamp.intensity=10*(1-dk);dir.intensity=1.7*(1-dk);
    man.skinM.emissive.setHex(0xff2a10).multiplyScalar(dk*.45);glow.intensity=dk*6;man.head.rotation.z=Math.sin(t*2)*.04;
    sg.visible=t>.3&&t<tg;sg.scale.setScalar(pop(t,.3));sg.position.set(.55,3.0,2.4);face(sg,-.08);
    const e=ease(t/3.6);cam(40,[.15,2.75,lerp(5.0,4.4,e)],[0,2.55,2.2])}}});

// ===== S2: "long-range attack, from 93 million miles away." — space: Earth to the Sun
shot(L(2)-.06,()=>{const s=nightSky('#0d1230');s.add(new THREE.HemisphereLight(0xd0d8ff,0x1a1d33,1.0));const dl=new THREE.DirectionalLight(0xffe0a0,2.4);dl.position.set(-10,2,-6);s.add(dl);
  const e=earthChar(s,1.0);e.position.set(1.2,0,0);e.mood('shock');const su=sunChar(s,7);su.position.set(-9,1.5,-28);
  const ray=new THREE.Mesh(new THREE.CylinderGeometry(.06,.06,1,8),new THREE.MeshBasicMaterial({color:0xffd23a}));s.add(ray);
  const t0=L(2)-.06,ta=wordT(2,'longrange')-t0,tm=wordT(2,'93')-t0;const mi=sign(s,'93,000,000 MILES',2.4,'#1b2330','#ffd52e',90);
  const A=V(-9,1.5,-28),B=V(1.2,0,0);
  return{s,u(t){e.rotation.y=t*.3;const k=clamp((t-ta)/1.0);const P=A.clone().lerp(B,k);const Q=A.clone().lerp(B,Math.max(0,k-.15));
    ray.visible=k>0&&k<1;const mid=P.clone().add(Q).multiplyScalar(.5);ray.position.copy(mid);ray.scale.y=P.distanceTo(Q)+.01;ray.quaternion.setFromUnitVectors(V(0,1,0),P.clone().sub(Q).normalize());
    e.mood(t>ta+1?'shock':'neutral');e.position.x=1.2+(t>ta+1&&t<ta+1.3?Math.sin(t*60)*.05:0);
    su.lookAt(camera.position);
    mi.visible=t>tm;mi.scale.setScalar(pop(t,tm));mi.position.set(1.4,3.4,3.0);face(mi);
    const p=ease(t/4.9);cam(46,[lerp(4.6,5.2,p),lerp(1.2,2.8,p),lerp(7.0,11.0,p)],[lerp(.6,-3.0,p),lerp(.2,.8,p),lerp(0,-12,p)])}}});

// ===== S3: "The Sun showed up to court... and instantly melted the judge's gavel."
shot(L(3)-.06,()=>{const R=court({judge:true,man:false,sun:true});R.sun.scale.setScalar(.8);const {s,sun,judge}=R;const t0=L(3)-.06,ts=wordT(3,'showed')-t0,tm=wordT(3,'melted')-t0;
  const drips=[];for(let i=0;i<6;i++){const d=new THREE.Mesh(new THREE.SphereGeometry(.05,6,5),mat(0x4a2a12));s.add(d);d.visible=false;drips.push(d)}
  return{s,u(t){const k=eout(clamp((t-ts+.3)/.6));sun.position.set(-2.15,lerp(6.5,2.85,k)+Math.sin(t*2)*.06,2.4);sun.scale.setScalar(.8*(.5+.5*k));sun.lookAt(camera.position);
    const ar=judge.arms[0];ar.sh.rotation.x=-1.6;const m=eout(clamp((t-tm)/.6));judge.gHead.scale.set(1,1,1-m*.85);judge.gHead.position.y=-m*.1;
    judge.face(t>tm?'scared':'neutral');
    const gp=new THREE.Vector3();judge.gHead.getWorldPosition(gp);drips.forEach((d,i)=>{const dt=t-tm-i*.12;d.visible=dt>0&&dt<.6;d.position.set(gp.x+(i%3-1)*.06,gp.y-dt*dt*6,gp.z)});
    const sk=shake(t,tm,.05);const e=ease(t/4);cam(50,[lerp(-1.4,-1.6,e)+sk,3.0,lerp(-4.8,-4.2,e)],[-1.6,2.5,3.2])}}});

// ===== S4: "The jury needed sunglasses."
shot(L(4)-.06,()=>{const R=court({man:false,jury:true});const {s,jurors}=R;const sl=new THREE.PointLight(0xffb040,10,10,1.3);sl.position.set(1.5,3,0);s.add(sl);
  const t0=L(4)-.06,tg=wordT(4,'sunglasses')-t0;
  return{s,u(t){jurors.forEach(({m,sg},i)=>{sg.visible=t>tg+i*.04;m.face(t>tg?'happy':'scared');m.arms[0].sh.rotation.x=t>tg-.25&&t<tg+.15?-2.4:-.3;m.head.rotation.y=Math.sin(t*2+i)*.1})
    const e=ease(t/2);cam(44,[lerp(.6,.9,e),2.6,lerp(-3.6,-3.1,e)],[3.8,1.35,1.5])}}});

// ===== S5: "The stenographer got a tan."
shot(L(5)-.06,()=>{const R=court({man:false,steno:true});const {s,steno}=R;const t0=L(5)-.06,tt=wordT(5,'tan')-t0;const sg=sign(s,'TAN +100',1.0,'#c8781e');
  const c0=new THREE.Color(SKIN),c1=new THREE.Color(0x7a4424);
  return{s,u(t){const k=clamp((t-tt+.3)/.4);steno.skinM.color.copy(c0).lerp(c1,k);for(const a of steno.arms){a.sh.rotation.x=-1.0;a.el.rotation.x=-.6+Math.sin(t*30+a.s)*.15}
    steno.face(t>tt?'happy':'neutral');sg.visible=t>tt;sg.scale.setScalar(pop(t,tt));sg.position.set(2.2,2.75,1.4);face(sg,-.06);
    const e=ease(t/2);cam(40,[lerp(.6,.8,e),2.3,lerp(-2.4,-2.0,e)],[2.2,1.6,1.6])}}});

// ===== S6a: "So the judge ruled:" — gavel bang
shot(L(6)-.06,()=>{const R=court({judge:true,man:false});const {s,judge}=R;const t0=L(6)-.06,tr=wordT(6,'ruled')-t0;
  return{s,u(t){const ar=judge.arms[0];const up=clamp(t/Math.max(.05,tr-.15));const dn=clamp((t-tr+.05)/.05);ar.sh.rotation.x=lerp(-1.45,-2.6,up)*(1-dn)+(-1.45)*dn;judge.face('angry');
    const sk=shake(t,tr,.08);cam(42,[.55+sk,2.95,lerp(.9,1.4,ease(t/1.6))],[.45,2.75,4.3])}}});
// ===== S6b: "the Sun must stay twice as far away." — the sun shrinks away into the sky
shot(T[6].words[4].start-.06,()=>{const s=skyScene('#8fd0f0');lights(s,{sky:0xffffff,ground:0xcda45d,pos:[5,10,6],sh:8});
  const gr=new THREE.Mesh(new THREE.PlaneGeometry(200,200),new THREE.MeshLambertMaterial({map:paintTex('#cda45d',512,512,900,9,10,[10,50])}));gr.rotation.x=-PI/2;s.add(gr);
  const sea=new THREE.Mesh(new THREE.PlaneGeometry(400,200),mat(0x2c8a8c));sea.rotation.x=-PI/2;sea.position.set(0,.03,-108);s.add(sea);
  const su=sunChar(s,3.2);const t0=T[6].words[4].start-.06,tw=wordT(6,'twice')-t0;const st=stamp(s,'2X FARTHER',1.7);
  return{s,u(t){const k=eout(clamp((t-tw)/1.0));su.position.set(0,lerp(6.5,7.4,k),lerp(-8,-30,k));su.lookAt(camera.position);
    st.visible=t>tw+.2;const ks=clamp((t-tw-.2)/.12);st.scale.setScalar(lerp(1.7,1,ks));st.position.set(0,3.1,2.2);face(st,-.12);
    cam(46,[0,1.6,6],[0,4.2,-6])}}});

// ===== S7: "Problem solved... except now it's snowing in July." — frozen beach
shot(L(7)-.06,()=>{const s=beachWorld();lights(s,{sky:0xdfe8f2,ground:0x9c9a90,pos:[5,10,6],sh:8});const sn=snow(s);
  const su=sunDisc(s,1.0);su.position.set(-2.5,8,-30);const pg=poolGuy(s);pg.legs.rotation.x=PI/2;pg.root.position.set(0,1.02,0);
  const ice=new THREE.Mesh(new THREE.BoxGeometry(1.2,2.6,1.0),new THREE.MeshLambertMaterial({color:ICE,transparent:true,opacity:.55}));ice.position.set(0,1.3,0);s.add(ice);
  const cover=new THREE.Mesh(new THREE.PlaneGeometry(60,40),new THREE.MeshLambertMaterial({color:0xffffff,transparent:true,opacity:0}));cover.rotation.x=-PI/2;cover.position.set(0,.06,-5);s.add(cover);
  const t0=L(7)-.06,te=wordT(7,'except')-t0,tj=wordT(7,'july')-t0;const cal=label(s,'',1.0,1.15,{});
  cal.material.map=canvasTexOnce(400,460,(g,W,H)=>{g.fillStyle=PAPER;g.fillRect(0,0,W,H);g.fillStyle='#d23a2a';g.fillRect(0,0,W,120);g.fillStyle='#fff';g.font='900 80px M';g.textAlign='center';g.fillText('JULY',W/2,90);
    g.fillStyle='#1b2330';g.font='900 190px M';g.fillText('4',W/2,340);g.font='700 44px M';g.fillText('-30°F',W/2,420)});
  const ok=sign(s,'PROBLEM SOLVED',1.6,'#1f8a3a');
  return{s,u(t){const sk=clamp((t-te)/1.2);sn(t,sk);cover.material.opacity=sk*.85;ice.visible=t>te+.6;ice.scale.setScalar(t>te+.6?back((t-te-.6)/.3):1);
    pg.face(t>te+.6?'scared':'happy');for(const a of pg.arms){a.sh.rotation.z=a.s*(t>te+.6?.25:.4+Math.sin(t*3)*.1)}pg.skinM.color.setHex(t>te+.6?0x8fb8d8:SKIN);
    ok.visible=t>.2&&t<te;ok.scale.setScalar(pop(t,.2));ok.position.set(0,3.4,0);face(ok);
    cal.visible=t>tj;cal.scale.setScalar(pop(t,tj));cal.position.set(.95,2.9,.3);face(cal,-.08);
    const e=ease(t/3.9);cam(44,[.3,2.4,lerp(6.4,5.6,e)],[0,2.0,0])}}});

// ===== S8: "Would you take that deal? Yes or no?" — shivering in the snow
shot(L(8)-.06,()=>{const s=beachWorld();lights(s,{sky:0xdfe8f2,ground:0x9c9a90,pos:[5,10,6],sh:8});const sn=snow(s);
  const cover=new THREE.Mesh(new THREE.PlaneGeometry(60,40),new THREE.MeshLambertMaterial({color:0xffffff,transparent:true,opacity:.85}));cover.rotation.x=-PI/2;cover.position.set(0,.06,-5);s.add(cover);
  const m=sunburnt(makeMan(s));m.legs.rotation.x=PI/2;m.root.position.set(0,1.02,0);m.skinM.color.setHex(0x8fb8d8);
  const t0=L(8)-.06,td=wordT(8,'deal')-t0,ty=wordT(8,'yes')-t0,tn=T[8].words.find(w=>w.w==='no?').start-t0;
  const q=bub(s,['DEAL?'],1.0,100),yes=sign(s,'YES',.75,'#1f8a3a'),no=sign(s,'NO',.75,'#d23a2a');
  return{s,u(t){sn(t,1);m.root.position.x=Math.sin(t*45)*.015;m.face('scared');for(const a of m.arms){a.sh.rotation.x=-1.1;a.sh.rotation.z=-a.s*.4;a.el.rotation.x=-1.6}
    q.visible=t>td&&t<ty;q.scale.setScalar(pop(t,td));q.position.set(.75,3.0,.2);face(q);
    yes.visible=t>ty;yes.scale.setScalar(pop(t,ty));yes.position.set(-.5,3.05,.3);face(yes,.1);
    no.visible=t>tn;no.scale.setScalar(pop(t,tn));no.position.set(.55,3.05,.3);face(no,-.1);
    cam(42,[.1,2.5,lerp(4.8,4.4,ease(t/2.6))],[0,2.25,0])}}});

// ===== S9a: "He got frostbite..." — frozen solid, then smashes out
shot(L(9)-.06,()=>{const s=beachWorld();lights(s,{sky:0xdfe8f2,ground:0x9c9a90,pos:[5,10,6],sh:8});const sn=snow(s);
  const cover=new THREE.Mesh(new THREE.PlaneGeometry(60,40),new THREE.MeshLambertMaterial({color:0xffffff,transparent:true,opacity:.85}));cover.rotation.x=-PI/2;cover.position.set(0,.06,-5);s.add(cover);
  const m=sunburnt(makeMan(s));m.legs.rotation.x=PI/2;m.root.position.set(0,1.02,0);m.skinM.color.setHex(0x8fb8d8);m.face('scared');
  const ice=new THREE.Mesh(new THREE.BoxGeometry(1.2,2.6,1.0),new THREE.MeshLambertMaterial({color:ICE,transparent:true,opacity:.55}));ice.position.set(0,1.3,0);s.add(ice);
  setSeed(66);const sh=[];for(let i=0;i<18;i++){const q=new THREE.Mesh(new THREE.TetrahedronGeometry(.14+rnd()*.12),new THREE.MeshLambertMaterial({color:ICE,transparent:true,opacity:.8}));s.add(q);sh.push({q,v:V((rnd()-.5)*5,2+rnd()*3,(rnd()-.2)*3),r:rnd()*6})}
  const t0=L(9)-.06,tf=wordT(9,'frostbite')-t0,tb=tf+.9;const fb=stamp(s,'FROSTBITE',1.4,'#2a6bd8');
  return{s,u(t){sn(t,1);const k=back(clamp((t-tf+.1)/.25));ice.visible=t<tb;ice.scale.setScalar(Math.max(.01,k));
    fb.visible=t>tf+.15;const kf=clamp((t-tf-.15)/.12);fb.scale.setScalar(lerp(1.7,1,kf));fb.position.set(0,3.25,.5);face(fb,-.12);
    const pt=t-tb;for(const p of sh){p.q.visible=pt>0;p.q.position.set(p.v.x*pt,1.3+p.v.y*pt-5*pt*pt,p.v.z*pt);p.q.rotation.set(p.r+pt*8,pt*6,p.r)}
    if(t>tb){m.face('angry');flail(m,t,.8);m.legs.rotation.x=PI/2}else{for(const a of m.arms){a.sh.rotation.x=0;a.sh.rotation.z=a.s*.15}}
    const sk=shake(t,tb,.12);cam(42,[.1+sk,2.4,lerp(5.0,4.6,ease(t/1.7))],[0,2.0,0])}}});

// ===== S9b: "...which is exactly why..." — storms into court with a fresh lawsuit; ends on S0's first frame
shot(wordT(9,'which')-.1,()=>{const R=court();const {s,man,doors}=R;const f=folder(s);const t0=wordT(9,'which')-.1;const D=END-t0;
  return{s,u(t){const p=clamp(t/(D-.1));for(const d of doors)d.leaf.rotation.y=d.sx*-1.3*(1-clamp(t/.6))*Math.min(1,t*8);
    const z=lerp(-3.4,2.2,eout(p));man.root.position.set(0,1.02+(p<1?Math.abs(Math.sin(t*12))*.07*(1-p):0),z);man.root.rotation.z=p<1?Math.sin(t*12)*.05*(1-p):0;
    man.face('angry');man.torso.rotation.x=0;holdOverhead(man,f,lerp(-1.2,-2.7,eout(clamp(t/(D*.75)))));
    const e=eout(p);cam(C0.fov,[lerp(.6,C0.pos[0],e),lerp(3.2,C0.pos[1],e),lerp(6.6,C0.pos[2],e)],[C0.look[0],lerp(1.8,C0.look[1],e),lerp(-1.2,C0.look[2],e)])}}});

run(shots,END);
