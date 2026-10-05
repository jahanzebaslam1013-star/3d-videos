// "He Sued Sleep" — loop short (no music, no subtitles). Last frame of the final shot == first frame of shot 0.
import {THREE,renderer,W,H,camera,cam,loadTiming,run,clamp,ease,eout,back,lerp,V,box,cyl,grp,mat,lights,makeMan,flail,paintTex,textTex,
  canvasTex,label,skyScene,cloud,room,pajamaMan,setSeed,rnd,RB,SPH,sm,tree,nightSky,speedLines} from './engine.js';
const T=await loadTiming(); const T0=0;
const L=i=>T[i].start+T0, E=i=>T[i].end+T0;
const wordT=(i,w)=>{const x=T[i].words.find(q=>q.w.toLowerCase().replace(/[^a-z0-9]/g,'').startsWith(w));if(!x)throw new Error('word '+w);return x.start+T0};
const END=31.5;const PI=Math.PI;
const LOOK=[];const face=(o,rz=0)=>LOOK.push([o,rz]);
const shots=[];
const shot=(start,build)=>shots.push({start,build:()=>{const I=build();const u=I.u;I.u=t=>{LOOK.length=0;
  renderer.setScissorTest(false);renderer.setViewport(0,0,W,H);renderer.autoClear=true;renderer.setClearColor(0x000000,1);
  u(t);for(const [o,rz] of LOOK){o.lookAt(camera.position);if(rz)o.rotateZ(rz)}};return I}});
const shake=(t,t0,a=.12,d=.3)=>{const k=t-t0;if(k<0||k>d)return 0;return Math.sin(k*90)*a*(1-k/d)};
const pop=(t,t0,d=.25)=>t<t0?0:back((t-t0)/d);
const PAPER='#fbf8ef';

// ---------- textures / props ----------
function canvasTexOnce(w,h,draw){const c=canvasTex(w,h,draw);c.draw();return c.tex}
function fitFont(g,txt,max,w,wt=900){g.font=`${wt} ${max}px M`;const k=Math.min(1,w/g.measureText(txt).width);const fs=Math.floor(max*k);g.font=`${wt} ${fs}px M`;return fs}
function folder(p,w=1.15,h=.85,t=.2){const g=grp(p);box(g,w,h,t,0xd9a94e,0,0,0);box(g,w-.08,h-.1,t+.02,0xfbf8ef,0,-.03,0);box(g,w*.3,.1,t+.04,0xd9a94e,-w*.3,h/2+.03,0);
  const lb=label(g,'',w*.9,h*.62,{});lb.material.map=canvasTexOnce(512,350,(c,W,H)=>{c.fillStyle='#d9a94e';c.fillRect(0,0,W,H);c.fillStyle='#fff7e0';c.fillRect(18,18,W-36,H-36);
    c.textAlign='center';c.fillStyle='#d23a2a';c.font='900 92px M';c.fillText('LAWSUIT',W/2,140);c.fillStyle='#1b2330';fitFont(c,'ME vs. SLEEP',66,W-70);c.fillText('ME vs. SLEEP',W/2,250)});
  lb.position.z=t/2+.025;return g}
function stamp(p,txt,w=1.2,col='#d23a2a'){const m=label(p,'',w,w*.38,{});m.material.map=canvasTexOnce(512,196,(g,W,H)=>{g.strokeStyle=col;g.lineWidth=16;g.strokeRect(10,10,W-20,H-20);
  g.fillStyle=col;fitFont(g,txt,116,W-70);g.textAlign='center';g.textBaseline='middle';g.fillText(txt,W/2,H/2+6)});return m}
function sign(p,txt,w,col='#d23a2a',fg='#fff',fs=110){const m=label(p,'',w,w*.36,{});m.material.map=canvasTexOnce(560,200,(g,W,H)=>{g.fillStyle=col;g.beginPath();g.roundRect(6,6,W-12,H-12,36);g.fill();
  g.strokeStyle='#fff';g.lineWidth=8;g.beginPath();g.roundRect(16,16,W-32,H-32,28);g.stroke();g.fillStyle=fg;fitFont(g,txt,fs,W-70);g.textAlign='center';g.textBaseline='middle';g.fillText(txt,W/2,H/2+6)});return m}
function bub(p,lines,w=2,fs=84){const m=label(p,'',w,w*.62,{});m.material.map=canvasTexOnce(560,348,(g,W,H)=>{g.fillStyle='#fff';g.strokeStyle='#111';g.lineWidth=8;
  g.beginPath();g.roundRect(10,10,W-20,H-90,60);g.fill();g.stroke();g.beginPath();g.moveTo(150,H-84);g.lineTo(110,H-12);g.lineTo(230,H-84);g.closePath();g.fill();g.stroke();
  g.fillStyle='#fff';g.fillRect(150,H-92,80,14);g.fillStyle='#111';g.textAlign='center';g.textBaseline='middle';
  lines.forEach((l,i)=>{fitFont(g,l,fs,W-80);g.fillText(l,W/2,(H-80)/2+(i-(lines.length-1)/2)*fs*1.05+4)})});return m}
// giant kinetic hook text
function hookText(p){const m=label(p,'',1.55,.775,{});m.material.map=canvasTexOnce(1024,512,(g,W,H)=>{g.textAlign='center';g.textBaseline='middle';g.lineJoin='round';
  for(const [txt,y,col] of [['SUING',150,'#ffffff'],['SLEEP?!',360,'#ffd52e']]){fitFont(g,txt,190,W-80);g.lineWidth=30;g.strokeStyle='#111';g.strokeText(txt,W/2,y);g.fillStyle=col;g.fillText(txt,W/2,y)}});
  m.material.depthTest=false;m.renderOrder=10;return m}
function clockSign(p,txt,col='#1b2330',w=1.3){const m=label(p,'',w,w*.42,{});m.material.map=canvasTexOnce(520,220,(g,W,H)=>{g.fillStyle=col;g.beginPath();g.roundRect(6,6,W-12,H-12,30);g.fill();
  g.fillStyle='#ff4a3a';g.shadowColor='#ff4a3a';g.shadowBlur=20;fitFont(g,txt,130,W-60);g.textAlign='center';g.textBaseline='middle';g.fillText(txt,W/2,H/2+6)});return m}
function zzz(p,n=3){const out=[];for(let i=0;i<n;i++){const m=label(p,'',.5,.5,{});m.material.map=canvasTexOnce(128,128,(g,W,H)=>{g.font='900 110px M';g.textAlign='center';g.textBaseline='middle';g.lineWidth=12;g.strokeStyle='#1b2330';g.strokeText('Z',64,68);g.fillStyle='#fff';g.fillText('Z',64,68)});out.push(m)}
  return (t,x,y,z,s=1)=>out.forEach((m,i)=>{const k=((t*.7+i/n)%1);m.position.set(x+k*.6*s+Math.sin(k*6)*.08,y+k*1.2*s,z);m.scale.setScalar((.4+k*.8)*s);m.material.opacity=k<.8?1:1-(k-.8)/.2;m.material.transparent=true;face(m)})}

// ---------- characters ----------
// sleep-deprived look: dark eye bags, messy hair, red-tinted eyes
function tired(m){const bag=mat(0x6a4a7a);for(const s of[-1,1]){box(m.head,.08,.035,.01,bag,s*.07,.245,.153)}
  for(const [x,z,r] of [[-.1,.05,.4],[.05,-.05,-.3],[.12,.08,.2]]){const sp=box(m.head,.06,.14,.06,0x1a1310,x,.53,z);sp.rotation.z=r}
  const whites=[];for(const s of[-1,1]){const w=box(m.head,.065,.04,.012,0xffffff,s*.07,.28,.155);w.visible=false;whites.push(w)}
  m.rollEyes=on=>whites.forEach(w=>w.visible=on);return m}
function judgeMan(p){const m=makeMan(p,{suit:0x15161c});const w=0xf2f0ea;
  box(m.head,.36,.14,.36,w,0,.48,-.01);for(const s of[-1,1])for(const y of[.38,.26,.14])box(m.head,.09,.1,.3,w,s*.19,y,-.03);box(m.head,.3,.36,.1,w,0,.22,-.2);
  box(m.torso,.62,.74,.34,0x0c0d12,0,.37,0);box(m.torso,.12,.1,.02,0xffffff,0,.7,.175);
  const gv=grp(m.arms[0].el,0,-.42,0);cyl(gv,.035,.035,.55,0x5a3418,0,0,-.22,8).rotation.x=PI/2;const hd=cyl(gv,.09,.09,.3,0x4a2a12,0,0,-.5,12);hd.rotation.z=PI/2;
  m.face('neutral');return m}
// fluffy pillow defendant with sunglasses
function pillowChar(p){const g=grp(p);const wm=sm(0xf7f5f0,.9);const body=RB(g,1.5,.62,.95,.28,wm,0,0,0);
  setSeed(17);for(const [x,y] of [[-.72,.28],[.72,.28],[-.72,-.28],[.72,-.28]]){const c=SPH(g,.22,wm,x,y,0,14);c.scale.set(1,1,.8)}
  for(let i=0;i<6;i++){const c=SPH(g,.2,wm,-.55+i*.22,.3+rnd()*.04,.2,12);c.scale.set(1,.6,.8)}
  const blk=sm(0x111114,.3);const shades=grp(g,0,.06,.49);for(const s of[-1,1]){RB(shades,.42,.2,.05,.06,blk,s*.26,0,0)}RB(shades,.16,.05,.04,.02,blk,0,.05,0);
  const mouth=SPH(g,.1,sm(0x5a1a1a,.5),0,-.17,.47,12);mouth.scale.set(1.2,1,.4);
  const blush=[];for(const s of[-1,1]){const b=SPH(g,.07,sm(0xf2a0a0,.8),s*.5,-.1,.46,10);b.scale.z=.3;blush.push(b)}
  g.userData={body,mouth,shades};g.snore=t=>{const k=.5+.5*Math.sin(t*3.2);g.scale.set(1+k*.05,1+k*.08,1+k*.05);mouth.scale.set(1.2,.5+k*1.0,.4)};return g}

// ---------- worlds ----------
function court({judge=false,man=true,pillow=false}={}){const s=new THREE.Scene();s.background=new THREE.Color(0x5e3f26);setSeed(9);
  const fl=new THREE.Mesh(new THREE.PlaneGeometry(30,30),new THREE.MeshLambertMaterial({map:paintTex('#8a5a36',512,512,900,14,6,[30,120])}));fl.rotation.x=-PI/2;fl.receiveShadow=true;s.add(fl);
  const rug=new THREE.Mesh(new THREE.PlaneGeometry(2.4,9),mat(0x8e2a2a));rug.rotation.x=-PI/2;rug.position.set(0,.01,-2.5);rug.receiveShadow=true;s.add(rug);
  const panel=new THREE.MeshLambertMaterial({map:paintTex('#7a5232',512,512,900,12,3)});
  const bw=new THREE.Mesh(new THREE.PlaneGeometry(20,10),panel);bw.position.set(0,5,7);bw.rotation.y=PI;bw.receiveShadow=true;s.add(bw);
  for(let i=-4;i<=4;i++)box(s,.12,4.2,.1,0x5a3a20,i*1.3,2.1,6.92);box(s,14,.18,.14,0x4a2e16,0,4.25,6.9);
  const fw=new THREE.Mesh(new THREE.PlaneGeometry(20,10),new THREE.MeshLambertMaterial({map:paintTex('#b49a78',512,512,900,12,3)}));fw.position.set(0,5,-7);fw.receiveShadow=true;s.add(fw);
  const doors=[];for(const sx of[-1,1]){const d=grp(s,sx*1.33,0,-6.9);const leaf=grp(d,0,0,0);box(leaf,1.3,2.9,.12,0x5b3b22,-sx*.65,1.45,0);box(leaf,.5,.7,.13,0xbfd8e8,-sx*.65,2.0,0.01);doors.push({d,leaf,sx})}
  box(s,2.8,.2,.15,0x4a2e16,0,2.98,-6.9);
  for(const sx of[-1,1]){const sw=new THREE.Mesh(new THREE.PlaneGeometry(14,10),new THREE.MeshLambertMaterial({map:paintTex('#a88a66',512,512,700,12,3)}));sw.position.set(sx*6,5,0);sw.rotation.y=-sx*PI/2;s.add(sw)}
  for(const z of[-2.3,-3.6,-4.9])for(const sx of[-1,1]){box(s,3.2,.12,.6,0x6e4426,sx*2.9,.5,z);box(s,3.2,.7,.1,0x6e4426,sx*2.9,.85,z-.3)}
  const bench=grp(s,0,0,3.6);box(bench,4.4,1.7,1.2,0x6e4426,0,.85,0);box(bench,4.6,.1,1.4,0x4f2f18,0,1.75,0);for(const x of[-1.5,0,1.5])box(bench,1.2,1.1,.04,0x83532f,x,.85,-.61);
  box(s,3,.5,1.6,0x5a3418,0,.25,4.6);
  const stand=grp(s,-3.1,0,2.4);stand.rotation.y=.5;box(stand,1.5,1.15,1.3,0x6e4426,0,.575,0);box(stand,1.6,.08,1.4,0x4f2f18,0,1.17,0);
  const plaque=label(stand,'',1.2,.26,{});plaque.material.map=canvasTexOnce(560,124,(g,W,H)=>{g.fillStyle='#d9b44a';g.fillRect(0,0,W,H);g.fillStyle='#2a1d12';fitFont(g,'DEFENDANT',64,W-40);g.textAlign='center';g.textBaseline='middle';g.fillText('DEFENDANT',W/2,H/2+4)});
  plaque.position.set(0,.85,-.665);plaque.rotation.y=PI;
  for(const sx of[-1,1]){const bn=grp(s,sx*3.4,0,6.85);box(bn,1.1,3.2,.05,0x24345e,0,3.0,0);box(bn,1.1,.14,.06,0xd9b44a,0,1.45,0)}
  const ck=clockSign(s,'3:00 AM','#1b2330',1.6);ck.position.set(0,5.3,6.85);ck.rotation.y=PI;
  const lamp=new THREE.PointLight(0xffe2b0,10,14,1.4);lamp.position.set(0,5,1);s.add(lamp);
  lights(s,{sky:0xfff1dc,ground:0x6b4a30,hemi:1.5,dir:1.7,pos:[4,12,-3],target:[0,1,2],sh:9});
  const R={s,bench,stand,doors};
  if(judge){const j=judgeMan(s);j.legs.rotation.x=PI/2;j.root.position.set(0,1.52,4.35);j.root.rotation.y=PI;R.judge=j}
  if(man){const m=tired(makeMan(s));m.legs.rotation.x=PI/2;m.root.position.set(0,1.02,2.2);m.face('angry');R.man=m}
  if(pillow){const pw=pillowChar(s);pw.position.set(-3.1,1.75,2.4);pw.rotation.y=.5+PI;R.pillow=pw}
  return R}
function holdOverhead(m,f,a,{flat=0}={}){for(const ar of m.arms){ar.sh.rotation.x=a;ar.sh.rotation.z=ar.s*.18;ar.el.rotation.x=-.25}
  const Lr=.8,r=m.root.position;const y=r.y+.67-Lr*Math.cos(a),z=r.z-Lr*Math.sin(a);
  f.position.set(r.x,y+.25*(1-flat),z+.12+.15*flat);f.rotation.set(-flat*PI/2+(1-flat)*.15,0,0)}
const C0={fov:44,pos:[.25,2.9,6.1],look:[0,2.1,1.8]};

// open convertible with the man driving; road scrolls
function carScene(sky='#9fd6f0'){const s=skyScene(sky);lights(s,{sky:0xffffff,ground:0x8a8a80,hemi:1.5,dir:2.0,pos:[5,10,6],sh:8});
  const road=paintTex('#55585e',256,256,300,10,1,[10,40]);const rd=new THREE.Mesh(new THREE.PlaneGeometry(9,400),new THREE.MeshLambertMaterial({map:road}));rd.rotation.x=-PI/2;rd.position.z=-150;rd.receiveShadow=true;s.add(rd);
  const gr=new THREE.Mesh(new THREE.PlaneGeometry(400,400),new THREE.MeshLambertMaterial({map:paintTex('#7fb65a',512,512,900,14,30,[10,40])}));gr.rotation.x=-PI/2;gr.position.y=-.01;gr.receiveShadow=true;s.add(gr);
  const dashes=[];for(let i=0;i<30;i++)dashes.push(box(s,.15,.02,1.4,0xf4f1ea,0,.02,-i*4));
  setSeed(3);const trees=[];for(let i=0;i<24;i++){const sx=i%2?1:-1;trees.push(tree(s,sx*(6+rnd()*4),-i*6,1.4+rnd()*.6))}
  for(const [x,y,z] of [[-8,9,-40],[9,11,-55],[0,13,-70]])cloud(s,x,y,z,2.2);
  const car=grp(s);const red=0xd23a2a;box(car,2.0,.6,4.0,red,0,.65,0);box(car,1.9,.35,1.2,red,0,1.1,-1.3);box(car,1.9,.35,.9,red,0,1.1,1.5);
  for(const sx of[-1,1])box(car,.06,.7,.06,0x2b2f38,sx*.9,1.55,1.0);box(car,1.86,.06,.06,0x2b2f38,0,1.9,1.0);box(car,1.75,.5,.1,0x2b2f38,0,.95,-.2);
  const wheelS=grp(car,.35,1.25,.65);const sw=new THREE.Mesh(new THREE.TorusGeometry(.22,.04,8,20),mat(0x111111));wheelS.add(sw);wheelS.rotation.x=-.9;
  for(const sx of[-1,1])for(const zz of[-1.25,1.25]){const w=cyl(car,.4,.4,.3,0x0d0d0d,sx*1.0,.4,zz,14);w.rotation.z=PI/2}
  box(car,.4,.14,.04,0xfff6c8,-.6,.75,2.01);box(car,.4,.14,.04,0xfff6c8,.6,.75,2.01);
  const m=tired(makeMan(car));m.root.position.set(.35,.72,.0);m.legs.rotation.x=0;
  for(const a of m.arms){a.sh.rotation.x=-1.25;a.sh.rotation.z=a.s*-.12;a.el.rotation.x=-.2}
  return{s,car,m,dashes,trees,sw:wheelS,
    roll(t,speed=14){dashes.forEach((d,i)=>d.position.z=8-i*4-((t*speed)%4));trees.forEach((tr,i)=>tr.position.z=14-i*6-((t*speed)%6))}}}

// ===== S0: slam + giant kinetic text (first frame == last frame of the final shot)
const tSlam=0.15;
shot(0,()=>{const R=court();const {s,man}=R;const f=folder(s);const ht=hookText(s);
  return{s,u(t){const k=clamp(t/tSlam);const a=lerp(-2.7,-1.72,k*k);holdOverhead(man,f,a,{flat:k*k});
    if(t>=tSlam){f.position.set(0,1.9,3.1);f.rotation.set(-PI/2,0,0)}
    man.torso.rotation.x=lerp(0,.28,k*k);man.face('angry');
    ht.visible=t>=tSlam;const hp=pop(t,tSlam,.22);ht.scale.setScalar(hp*(1+Math.sin(t*14)*.025));ht.position.set(0,1.5,3.05);face(ht,Math.sin(t*9)*.04);
    const sk=shake(t,tSlam,.16,.45);const e=ease(t/2.0);
    cam(C0.fov,[C0.pos[0]+sk,C0.pos[1]-e*.15+sk*.7,C0.pos[2]-e*.5],[C0.look[0]+sk*.3,C0.look[1],C0.look[2]])}}});

// ===== S1: "a sleep-deprived guy" — twitchy close-up, 0 HOURS SLEPT
shot(wordT(0,'sleep')-.06,()=>{const R=court();const {s,man}=R;man.root.position.set(0,1.02,2.2);man.face('scared');
  const cup=grp(man.arms[1].el,0,-.44,.08);cyl(cup,.08,.07,.18,0xffffff,0,0,0,12);cyl(cup,.07,.07,.01,0x4a2a12,0,.085,0,12);
  const sg=sign(s,'0 HOURS SLEPT',.95,'#1b2330','#ffd52e',90);
  return{s,u(t){man.arms[1].sh.rotation.x=-1.2;man.arms[1].el.rotation.x=-1.2+Math.sin(t*40)*.05;man.head.rotation.z=Math.sin(t*23)*.03;man.root.position.x=Math.sin(t*31)*.01;
    sg.scale.setScalar(pop(t,.25));sg.position.set(.05,3.08,2.5);face(sg,-.05);
    const e=ease(t/1.4);cam(40,[.1,2.75,lerp(5.0,4.6,e)],[0,2.65,2.2])}}});

// ===== S2: "officially filed a lawsuit against Sleep." — FILED stamp
shot(wordT(0,'officially')-.06,()=>{const R=court();const {s,man}=R;const f=folder(s);f.position.set(0,1.9,3.1);f.rotation.x=-PI/2;
  for(const ar of man.arms){ar.sh.rotation.x=-1.72;ar.sh.rotation.z=ar.s*.18;ar.el.rotation.x=-.25}man.torso.rotation.x=.28;
  const t0=wordT(0,'officially')-.06;const st=stamp(s,'FILED',1.0);st.rotation.x=-PI/2;st.rotation.z=.25;const tf=wordT(0,'filed')-t0;
  const ts=wordT(0,'sleep',)-t0;const ts2=T[0].words.at(-1).start-t0;const vs=sign(s,'vs. SLEEP',1.15,'#3a2a78');
  return{s,u(t){st.visible=t>tf;const k=clamp((t-tf)/.12);st.position.set(.18,lerp(2.6,2.03,k),3.15);st.scale.setScalar(lerp(1.6,1,k));
    vs.visible=t>ts2;vs.scale.setScalar(pop(t,ts2));vs.position.set(.15,2.75,3.1);face(vs,.06);
    const sk=shake(t,tf,.06);const e=ease(t/2.4);cam(42,[.3+sk,lerp(4.0,3.8,e),lerp(5.6,5.2,e)],[.05,2.0,2.6])}}});

// ===== S3: "His charge? Breach of contract." — sleep contract rips, BREACHED stamp
shot(L(1)-.06,()=>{const s=new THREE.Scene();s.background=paintTex('#2a2f5a',512,1024,1200,12,1,[40,140]);
  s.add(new THREE.HemisphereLight(0xfff6ea,0x2a2f5a,2.4));
  const ct=canvasTex(600,780,(g,w,h)=>{g.fillStyle=PAPER;g.fillRect(0,0,w,h);g.fillStyle='#3a2a78';g.textAlign='center';fitFont(g,'SLEEP CONTRACT',66,w-60);g.fillText('SLEEP CONTRACT',w/2,100);
    g.fillStyle='#ccc';g.fillRect(50,130,w-100,4);g.fillStyle='#1b2330';g.font='900 52px M';g.fillText('8 HOURS',w/2,260);g.fillText('EVERY NIGHT',w/2,330);
    g.font='700 34px M';g.fillStyle='#666';g.fillText('guaranteed*',w/2,390);g.fillStyle='rgba(0,0,0,.18)';for(let y=460;y<620;y+=30)g.fillRect(60,y,w-120-(y*7%120),8);
    g.fillStyle='#3a2a78';g.font='italic 700 46px M';g.fillText('— Sleep',w/2,700)});ct.draw();
  const mk=o=>{const g=new THREE.PlaneGeometry(1.15,3.0);const uv=g.attributes.uv;for(let i=0;i<uv.count;i++)uv.setX(i,uv.getX(i)*.5+o);const m=new THREE.Mesh(g,new THREE.MeshBasicMaterial({map:ct.tex,side:THREE.DoubleSide}));s.add(m);return m};
  const hl=mk(0),hr=mk(.5);const t0=L(1)-.06,tb=wordT(1,'breach')-t0;const st=stamp(s,'BREACHED',1.3);
  setSeed(71);const P=[];const pm=new THREE.MeshBasicMaterial({color:0xfbf8ef,side:THREE.DoubleSide});for(let i=0;i<16;i++){const q=new THREE.Mesh(new THREE.PlaneGeometry(.12,.15),pm);s.add(q);P.push({q,v:V((rnd()-.5)*3,1+rnd()*2,rnd()),r:rnd()*6})}
  return{s,u(t){const k=eout(clamp((t-tb)/.3));hl.position.set(-.575-k*.5,.5-k*.25,0);hl.rotation.z=k*.35;hr.position.set(.575+k*.5,.5-k*.25,0);hr.rotation.z=-k*.35;
    const pt=t-tb;for(const p of P){p.q.visible=pt>0;p.q.position.set(p.v.x*pt,.5+p.v.y*pt-2.5*pt*pt,.3+p.v.z*pt);p.q.rotation.set(p.r+pt*6,pt*4,p.r)}
    const ts=wordT(1,'contract')-t0;st.visible=t>ts;const ks=clamp((t-ts)/.12);st.scale.setScalar(lerp(1.7,1,ks));st.position.set(0,.6,.6);st.rotation.z=-.2;
    const sk=shake(t,tb,.06)+shake(t,ts,.08);cam(40,[sk,.5+sk,lerp(6.2,5.6,ease(t/2.4))],[0,.45,0])}}});

// ===== S4: SPLIT SCREEN — top: 2:00 AM wide awake in bed / bottom: 7:00 AM face-plant into coffee
shot(L(2)-.06,()=>{const t0=L(2)-.06;const empty=new THREE.Scene();
  const camA=new THREE.PerspectiveCamera(42,W/(H/2),.05,200),camB=new THREE.PerspectiveCamera(42,W/(H/2),.05,200);
  // top: bedroom at night
  const A=nightSky('#1d2550');A.add(new THREE.HemisphereLight(0x9fb0ee,0x1a1d33,1.3));const dA=new THREE.DirectionalLight(0xbfcaff,1.3);dA.position.set(2,6,5);dA.castShadow=true;A.add(dA);
  const flA=new THREE.Mesh(new THREE.PlaneGeometry(30,30),mat(0x2b3350));flA.rotation.x=-PI/2;flA.receiveShadow=true;A.add(flA);
  const wall=new THREE.Mesh(new THREE.PlaneGeometry(30,12),mat(0x3a4470));wall.position.z=-2;A.add(wall);
  const win=grp(A,-2.4,2.6,-1.95);box(win,1.4,1.2,.05,0xdfe6ff,0,0,0);box(win,1.3,1.1,.06,0x0f1430,0,0,.01);const mn=new THREE.Mesh(new THREE.CircleGeometry(.25,20),new THREE.MeshBasicMaterial({color:0xfff6d0}));mn.position.set(.25,.2,.05);win.add(mn);
  box(A,2.4,.5,3.2,0x6b4a30,0,.25,0);box(A,2.2,.25,3.0,0xeef2ff,0,.62,0);box(A,1.6,.25,.6,0xffffff,0,.85,-1.1);box(A,2.25,.18,2.0,0x5a7fd0,0,.83,.55);
  const pm=tired(pajamaMan(A));pm.legs.rotation.x=0;pm.root.position.set(0,.98,-.6);pm.torso.rotation.x=-1.45;pm.face('scared');
  box(A,.6,.8,.6,0x6b4a30,1.5,.4,-1.3);const dc=clockSign(A,'2:00 AM','#111',.62);dc.position.set(.62,1.45,-.7);dc.material.depthTest=false;dc.renderOrder=5;
  // bottom: office meeting morning
  const B=room();const tbl=grp(B,0,0,0);box(tbl,3.4,.1,1.4,0x9a6a3c,0,.95,.2);for(const x of[-1.5,1.5])box(tbl,.1,.95,1.2,0x7a5230,x,.475,.2);
  const om=tired(makeMan(B));om.root.position.set(0,.47,-.75);om.legs.rotation.x=0;om.face('neutral');
  const cup=grp(B,0,1.0,.15);cyl(cup,.12,.1,.24,0xffffff,0,.12,0,14);const cof=cyl(cup,.11,.11,.01,0x4a2a12,0,.235,0,14);
  const brd=grp(B,1.9,1.5,-2.6);box(brd,1.6,1.1,.05,0xffffff,0,1.1,0);box(brd,.12,.4,.02,0x3a7bd5,-.4,.85,.03);box(brd,.12,.65,.02,0x3a7bd5,-.1,.98,.03);box(brd,.12,.9,.02,0xd23a2a,.2,1.1,.03);
  const dc2=clockSign(B,'7:00 AM','#1b2330',1.1);dc2.position.set(-.9,2.6,-1.2);
  const zz=zzz(B,3);setSeed(41);const sp=[];const sm2=mat(0x6a3f1e);for(let i=0;i<14;i++){const d=new THREE.Mesh(new THREE.SphereGeometry(.035,6,5),sm2);B.add(d);sp.push({d,v:V((rnd()-.5)*2,1+rnd()*1.5,(rnd()-.2)*1.2)})}
  const tBut=wordT(3,'but')-t0,tV=wordT(3,'violently')-t0;
  return{s:empty,u(t){
    // top half animation: eyes wide, tiny twitch, clock blink
    pm.head.rotation.x=Math.sin(t*1.5)*.03;pm.root.position.x=Math.sin(t*37)*.004;dc.visible=Math.floor(t*2)%2===0||t<.6;dc.scale.setScalar(pop(t,.1));
    camA.position.set(.35,2.7,lerp(.9,.6,ease(t/5)));camA.lookAt(.15,1.0,-1.15);
    // bottom half: nods, then face-plant on "violently"
    const plant=eout(clamp((t-tV)/.16));const nod=t>tBut&&t<tV?Math.sin((t-tBut)*14)*.08:0;om.torso.rotation.x=nod+plant*.85;om.head.rotation.x=plant*.3;
    om.face(t>tV?'neutral':'neutral');om.rollEyes(t>tBut);for(const a of om.arms){a.sh.rotation.x=-.9-plant*.4;a.el.rotation.x=-.4;a.sh.rotation.z=a.s*plant*.4}
    const pt=t-tV-.12;for(const q of sp){q.d.visible=pt>0&&pt<1.2;q.d.position.set(q.v.x*pt,1.25+q.v.y*pt-4*pt*pt,.15+q.v.z*pt)}
    cof.visible=pt<0;if(t>tV+.3)zz(t,.25,2.05,.1,.9);else zz(-9,0,-50,0);
    dc2.scale.setScalar(t>tBut-.3?pop(t,tBut-.3):0);face(dc2);
    const sk=shake(t,tV+.1,.08);camB.position.set(.15+sk,2.05,lerp(2.4,2.15,ease((t-tBut)/3)));camB.lookAt(0,1.6,-.6);
    face(dc);for(const [o,rz] of LOOK){o.lookAt((o===dc?camA:camB).position);if(rz)o.rotateZ(rz)}LOOK.length=0;
    // draw both halves ourselves, active half bright
    renderer.setScissorTest(true);renderer.autoClear=true;
    renderer.setViewport(0,H/2+6,W,H/2-6);renderer.setScissor(0,H/2+6,W,H/2-6);renderer.render(A,camA);
    renderer.setViewport(0,0,W,H/2-6);renderer.setScissor(0,0,W,H/2-6);renderer.render(B,camB);
    renderer.setClearColor(0xffffff,1);renderer.setScissor(0,H/2-6,W,12);renderer.clear();
    renderer.setClearColor(0x000000,1);renderer.setViewport(0,0,1,1);renderer.setScissor(0,0,1,1);
    cam(40,[0,0,5],[0,0,0])}}});

// ===== S5: "Sleep refused to testify, claiming exhaustion." — snoring pillow in the defendant box
shot(L(4)-.06,()=>{const R=court({man:false,pillow:true});const {s,pillow}=R;const zz=zzz(s,3);
  const t0=L(4)-.06,tr=wordT(4,'refused')-t0,tc=wordT(4,'claiming')-t0;const b1=bub(s,['NO COMMENT'],1.0,90),b2=bub(s,['TOO TIRED'],1.0,90);
  const ds=sign(s,'DEFENDANT: SLEEP',1.25,'#3a2a78','#fff',80);
  return{s,u(t){pillow.snore(t);pillow.position.y=1.75+Math.sin(t*2)*.08;zz(t,-2.75,2.35,2.1,1);
    ds.scale.setScalar(pop(t,.05));ds.position.set(-3.05,3.3,2.1);face(ds,.04);
    b1.visible=t>tr&&t<tc;b1.scale.setScalar(pop(t,tr));b1.position.set(-3.45,2.85,1.9);face(b1);
    b2.visible=t>tc;b2.scale.setScalar(pop(t,tc));b2.position.set(-3.45,2.85,1.9);face(b2);
    const e=ease(t/3);cam(42,[lerp(-1.6,-1.9,e),2.4,lerp(-2.4,-1.8,e)],[-3.2,2.1,2.4])}}});

// ===== S6: "So the judge ordered a legal compromise:" — gavel bang, pillow keeps snoring
shot(L(5)-.06,()=>{const R=court({judge:true,man:false,pillow:true});const {s,judge,pillow}=R;const zz=zzz(s,3);
  const t0=L(5)-.06,tb=wordT(5,'judge')-t0,tc=wordT(5,'compromise')-t0;const cs=sign(s,'COMPROMISE',2.1,'#1f8a3a');
  return{s,u(t){pillow.snore(t);pillow.position.y=1.75+Math.sin(t*2)*.08;zz(t,-2.75,2.35,2.1,1);
    const ar=judge.arms[0];const up=clamp(t/Math.max(.01,tb-.2));const dn=clamp((t-tb+.06)/.06);ar.sh.rotation.x=lerp(-1.45,-2.6,up)*(1-dn)+(-1.45)*dn;
    if(t>tc-.25){const k=clamp((t-tc+.25)/.2),k2=clamp((t-tc)/.06);ar.sh.rotation.x=lerp(-1.45,-2.6,k)*(1-k2)+(-1.45)*k2}judge.face('angry');
    cs.visible=t>tc;cs.scale.setScalar(pop(t,tc));cs.position.set(-1.6,3.7,2.0);face(cs,-.04);
    const sk=shake(t,tb,.09)+shake(t,tc,.09);const e=ease(t/2.6);cam(50,[lerp(-1.6,-1.8,e)+sk,2.8+sk,lerp(-5.6,-5.0,e)],[-1.85,2.3,3.2])}}});

// ===== S7: "12-hour naps are now mandatory," — new law, APPROVED stamp
shot(L(6)-.06,()=>{const s=new THREE.Scene();s.background=paintTex('#6e4426',512,1024,1200,14,1,[40,140]);s.add(new THREE.HemisphereLight(0xfff6ea,0x6b4a30,2.4));
  const pg=label(s,'',2.4,3.12,{});pg.material.map=canvasTexOnce(600,780,(g,w,h)=>{g.fillStyle=PAPER;g.fillRect(0,0,w,h);g.fillStyle='#1b2330';g.textAlign='center';fitFont(g,'NEW LAW',80,w-80);g.fillText('NEW LAW',w/2,110);
    g.fillStyle='#ccc';g.fillRect(50,140,w-100,4);g.fillStyle='#3a2a78';fitFont(g,'12-HOUR',120,w-70);g.fillText('12-HOUR',w/2,300);g.font='900 96px M';g.fillText('NAPS',w/2,400);
    g.fillStyle='#1b2330';fitFont(g,'MANDATORY',70,w-80);g.fillText('MANDATORY',w/2,520);g.fillStyle='rgba(0,0,0,.18)';for(let y=580;y<700;y+=28)g.fillRect(60,y,w-120-(y*7%120),8)});
  const st=stamp(s,'APPROVED',1.5,'#1f8a3a');const t0=L(6)-.06,tm=wordT(6,'mandatory')-t0;const pil=pillowChar(s);pil.scale.setScalar(.45);
  return{s,u(t){pg.position.set(0,.5,0);pg.rotation.z=-.03;st.visible=t>tm;const k=clamp((t-tm)/.12);st.scale.setScalar(lerp(1.7,1,k));st.position.set(.15,-.55,.05);st.rotation.z=.18;
    pil.snore(t);pil.position.set(-.85,-1.05,.35);pil.rotation.z=-.2;pil.visible=t>.3;pil.scale.setScalar(.45*pop(t,.3));
    const sk=shake(t,tm,.06);cam(40,[sk,.6+sk,lerp(6.0,5.3,ease(t/2.3))],[0,.55,0])}}});

// ===== S8: "but they only occur during your daily commute." — driving, falls asleep at the wheel
shot(L(7)-.06,()=>{const C=carScene();const {s,car,m}=C;const zz=zzz(s,3);const t0=L(7)-.06,tc=wordT(7,'commute')-t0,td=wordT(7,'daily')-t0;
  const ns=sign(s,'NAP TIME',1.3,'#3a2a78');
  return{s,u(t){C.roll(t,16);const sl=eout(clamp((t-td)/.4));m.head.rotation.x=sl*.5;m.torso.rotation.x=sl*.12;m.face('neutral');m.rollEyes(false);
    car.rotation.y=Math.sin(t*1.7)*.02+(t>tc?Math.sin((t-tc)*5)*.12:0);car.position.x=t>tc?Math.sin((t-tc)*4)*.5:0;car.position.y=Math.abs(Math.sin(t*13))*.02;
    if(t>td+.3)zz(t,car.position.x+.2,2.6,.4,1);else zz(-9,0,-50,0);
    ns.visible=t>tc;ns.scale.setScalar(pop(t,tc));ns.position.set(car.position.x,3.0,.3);face(ns,-.05);
    const e=ease(t/2.6);cam(44,[lerp(.8,.4,e),2.6,lerp(5.6,4.9,e)],[.3,1.7,0])}}});

// ===== S9: "Would you accept that deal? Drop a Yes or No below." — terrified, eyes rolling back
shot(L(8)-.06,()=>{const C=carScene('#f2b98a');const {s,car,m}=C;const t0=L(8)-.06,ty=wordT(8,'yes')-t0,tn=T[8].words.find(w=>w.w==='No').start-t0;
  const yes=sign(s,'YES',.75,'#1f8a3a'),no=sign(s,'NO',.75,'#d23a2a');const q=bub(s,['DEAL?'],1.05,100);const tq=wordT(8,'deal')-t0;
  return{s,u(t){C.roll(t,22);const roll=Math.floor(t*1.6)%2===1;m.face('scared');m.rollEyes(roll);m.head.rotation.x=roll?-.25:0;m.root.position.x=.35+Math.sin(t*30)*.01;
    for(const a of m.arms){a.sh.rotation.x=-1.25+Math.sin(t*25+a.s)*.06}
    car.rotation.y=Math.sin(t*3)*.1;car.position.x=Math.sin(t*2.2)*.6;
    q.visible=t>tq&&t<ty-.1;q.scale.setScalar(pop(t,tq));q.position.set(car.position.x+.75,2.8,.3);face(q);
    yes.visible=t>ty;yes.scale.setScalar(pop(t,ty));yes.position.set(car.position.x*.6-.1,2.9,.4);face(yes,.1);
    no.visible=t>tn;no.scale.setScalar(pop(t,tn));no.position.set(car.position.x*.6+.75,2.9,.4);face(no,-.1);
    cam(40,[car.position.x*.6+.3,2.45,4.2-t*.12],[car.position.x*.6+.3,1.95,0])}}});

// ===== S10: "He panicked so hard..." — panic in the car, grabs a fresh lawsuit
shot(L(9)-.06,()=>{const C=carScene('#f2b98a');const {s,car,m}=C;const f=folder(s,.8,.6,.14);const t0=L(9)-.06,tp=wordT(9,'panicked')-t0,tg=wordT(9,'so')-t0;
  const pn=sign(s,'PANIC!',1.0,'#d23a2a');
  return{s,u(t){C.roll(t,22);m.rollEyes(false);m.face('scared');car.rotation.y=Math.sin(t*4)*.12;car.position.x=Math.sin(t*3)*.4;
    if(t<tg){flail(m,t,1);m.legs.rotation.x=0}else{const k=eout(clamp((t-tg)/.3));const a=m.arms[1];a.sh.rotation.x=lerp(-1.2,-2.6,k);a.sh.rotation.z=-.2;a.el.rotation.x=-.2;m.arms[0].sh.rotation.x=-1.25}
    // folder: lies on passenger seat, then up in his hand
    const k=eout(clamp((t-tg)/.3));const seat=V(car.position.x-.35,1.2,.0);const hand=V(car.position.x+.05,2.75,-.1);f.position.lerpVectors(seat,hand,k);f.rotation.set(lerp(-PI/2,0,k),0,0);
    pn.visible=t>tp;pn.scale.setScalar(pop(t,tp));pn.position.set(car.position.x+.1,3.5,.3);face(pn,.08);
    cam(42,[car.position.x*.5+.2,2.6,lerp(4.6,5.0,t/2)],[car.position.x*.5+.1,2.0,0])}}});

// ===== S11: "...that precisely..." — storms back into court; ends on S0's first frame
shot(wordT(9,'that')-.12,()=>{const R=court();const {s,man,doors}=R;const f=folder(s);const t0=wordT(9,'that')-.12;const D=END-t0;
  return{s,u(t){const p=clamp(t/(D-.1));for(const d of doors)d.leaf.rotation.y=d.sx*-1.3*(1-clamp(t/.6))*Math.min(1,t*8);
    const z=lerp(-3.4,2.2,eout(p));man.root.position.set(0,1.02+(p<1?Math.abs(Math.sin(t*12))*.07*(1-p):0),z);man.root.rotation.z=p<1?Math.sin(t*12)*.05*(1-p):0;
    man.face('angry');man.torso.rotation.x=0;holdOverhead(man,f,lerp(-1.2,-2.7,eout(clamp(t/(D*.75)))));
    const e=eout(p);cam(C0.fov,[lerp(.6,C0.pos[0],e),lerp(3.2,C0.pos[1],e),lerp(6.6,C0.pos[2],e)],[C0.look[0],lerp(1.8,C0.look[1],e),lerp(-1.2,C0.look[2],e)])}}});

run(shots,END);
