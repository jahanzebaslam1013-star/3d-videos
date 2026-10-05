// zkit engine: low-poly flat-shaded 3D (Zack-D-like) scenes rendered with three.js
import * as THREE from './node_modules/three/build/three.module.js';
import {RoundedBoxGeometry} from './node_modules/three/examples/jsm/geometries/RoundedBoxGeometry.js';
export {THREE};
export const W=1080,H=1920;
export const renderer=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});
renderer.setPixelRatio(1);renderer.setSize(W,H);
renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFShadowMap;
document.body.appendChild(renderer.domElement);
export const camera=new THREE.PerspectiveCamera(40,W/H,0.05,500);
export const cam=(fov,pos,look)=>{camera.fov=fov;camera.position.set(...pos);camera.lookAt(...look)};

// ---------- helpers ----------
const clamp=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
const ease=x=>{x=clamp(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2};
const eout=x=>{x=clamp(x);return 1-Math.pow(1-x,3)};
const back=x=>{x=clamp(x);const c1=1.9,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)};
const lerp=(a,b,t)=>a+(b-a)*t;
const V=(x,y,z)=>new THREE.Vector3(x,y,z);
export let seed=7;export const setSeed=n=>{seed=n};const rnd=()=>{seed=(seed*16807)%2147483647;return seed/2147483647};
const mat=(c,o={})=>new THREE.MeshLambertMaterial({color:c,flatShading:true,...o});
function add(p,m){p.add(m);return m}
function box(p,w,h,d,c,x=0,y=0,z=0){const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),c.isMaterial?c:mat(c));m.position.set(x,y,z);m.castShadow=m.receiveShadow=true;p.add(m);return m}
function cyl(p,rt,rb,h,c,x=0,y=0,z=0,seg=10){const m=new THREE.Mesh(new THREE.CylinderGeometry(rt,rb,h,seg),c.isMaterial?c:mat(c));m.position.set(x,y,z);m.castShadow=m.receiveShadow=true;p.add(m);return m}
function grp(p,x=0,y=0,z=0){const g=new THREE.Group();g.position.set(x,y,z);p.add(g);return g}

function paintTex(base,w=512,h=512,n=900,var_=14,rep=1,stroke=[20,90]){
  const c=document.createElement('canvas');c.width=w;c.height=h;const g=c.getContext('2d');
  g.fillStyle=base;g.fillRect(0,0,w,h);const col=new THREE.Color(base);
  for(let i=0;i<n;i++){const d=(rnd()-.5)*var_/255;
    g.fillStyle=`rgba(${(col.r+d)*255|0},${(col.g+d)*255|0},${(col.b+d)*255|0},${.25+rnd()*.35})`;
    g.save();g.translate(rnd()*w,rnd()*h);g.rotate(-.5+rnd()*.3);
    const L=stroke[0]+rnd()*(stroke[1]-stroke[0]);g.beginPath();g.ellipse(0,0,L,L*.22,0,0,7);g.fill();g.restore();}
  const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;t.wrapS=t.wrapT=THREE.RepeatWrapping;t.repeat.set(rep,rep);return t;
}
function textTex(txt,{w=512,h=128,bg='#1b2330',fg='#fff',font='800 72px M',border=null}={}){
  const c=document.createElement('canvas');c.width=w;c.height=h;const g=c.getContext('2d');
  if(bg){g.fillStyle=bg;g.fillRect(0,0,w,h)}
  if(border){g.strokeStyle=border;g.lineWidth=8;g.strokeRect(4,4,w-8,h-8)}
  g.fillStyle=fg;g.font=font;g.textAlign='center';g.textBaseline='middle';g.fillText(txt,w/2,h/2+4);
  const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;t.anisotropy=8;return t;
}
// flat cartoon sun with orange outlined flame spikes
function sunTex(spikes=true){
  const S=1024,c=document.createElement('canvas');c.width=c.height=S;const g=c.getContext('2d');const cx=S/2,R=S*0.36;
  if(spikes){g.strokeStyle='#f08a1c';g.lineWidth=9;g.lineJoin='round';
    const n=26;for(let i=0;i<n;i++){const a=i/n*Math.PI*2+ (i%2)*.05;const len=R*(0.2+0.12*((i*7)%3)/2);
      const w=0.075;g.beginPath();
      g.moveTo(cx+Math.cos(a-w)*R*.95,cy(a-w));g.lineTo(cx+Math.cos(a+0.03)*(R+len),cx+Math.sin(a+0.03)*(R+len));g.lineTo(cx+Math.cos(a+w)*R*.95,cy(a+w));g.stroke();}
    function cy(a){return cx+Math.sin(a)*R*.95}}
  g.fillStyle='#ffd52e';g.beginPath();g.arc(cx,cx,R,0,7);g.fill();
  // subtle painterly speckle
  for(let i=0;i<500;i++){g.fillStyle=`rgba(255,${200+rnd()*40|0},40,${.15+rnd()*.2})`;const a=rnd()*7,r=Math.sqrt(rnd())*R*.97;g.beginPath();g.ellipse(cx+Math.cos(a)*r,cx+Math.sin(a)*r,14+rnd()*20,4,rnd()*3,0,7);g.fill()}
  const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;return t;
}
const SUNTEX=sunTex(true),SUNPLAIN=sunTex(false);
function sunDisc(p,size,spk=true){const m=new THREE.Mesh(new THREE.PlaneGeometry(size,size),new THREE.MeshBasicMaterial({map:spk?SUNTEX:SUNPLAIN,transparent:true,depthWrite:false}));p.add(m);return m}

function lights(scene,{sky=0xdff2ea,ground=0x9c8660,hemi=1.6,dir=2.2,pos=[6,12,8],target=[0,0,0],sh=12,col=0xfff3dd}={}){
  scene.add(new THREE.HemisphereLight(sky,ground,hemi));
  const d=new THREE.DirectionalLight(col,dir);d.position.set(...pos);d.target.position.set(...target);scene.add(d.target);
  d.castShadow=true;d.shadow.mapSize.set(2048,2048);const c=d.shadow.camera;c.left=c.bottom=-sh;c.right=c.top=sh;c.near=.5;c.far=80;d.shadow.bias=-0.0015;d.shadow.normalBias=0.03;d.shadow.radius=4;
  scene.add(d);return d;
}

// ---------- colors ----------
const C={sky:'#a9dcc6',sea:0x2c8a8c,foam:0xe8efe0,sand:'#cda45d',suit:0x1c2640,lapel:0x2b3a5c,shirt:0xf3f0e6,tie:0xc2272c,
 skin:0xd7a07a,burn:0xd2442a,hair:0x1a1310,chair:0x3e8c85,frame:0xe9ecea,umb:0xd9d0b6,palmT:0x8b6a3c,leaf:0x4c7a3a};

// ---------- character ----------
function makeMan(p,{suit=C.suit,cop=false}={}){
  const skinM=mat(C.skin);const R={skinM};
  const root=grp(p);R.root=root;
  const legs=grp(root);R.legs=legs;
  for(const s of[-1,1]){box(legs,.21,.21,.95,suit,s*.13,0,.47);box(legs,.22,.24,.32,0x111111,s*.13,.02,1.02)}
  const torso=grp(root);R.torso=torso;
  box(torso,.58,.72,.32,suit,0,.38,0);
  if(!cop){box(torso,.22,.46,.02,C.shirt,0,.5,.162);box(torso,.075,.42,.02,C.tie,0,.47,.175);box(torso,.1,.07,.03,C.tie,0,.69,.175);
    for(const s of[-1,1]){const l=box(torso,.1,.45,.03,C.lapel,s*.14,.5,.17);l.rotation.z=s*.28}
    box(torso,.05,.07,.02,C.shirt,.2,.62,.17);}
  else{box(torso,.06,.5,.02,0x0e1424,0,.45,.165);box(torso,.12,.1,.02,0xe0b33a,.14,.6,.166);box(torso,.6,.08,.34,0x0b0f1a,0,.08,0)}
  box(torso,.15,.12,.15,skinM,0,.78,0);
  const head=grp(torso,0,.8,0);R.head=head;
  box(head,.29,.42,.3,skinM,0,.22,0);
  box(head,.31,.1,.33,C.hair,0,.45,-.005);box(head,.31,.28,.06,C.hair,0,.3,-.15);
  R.brows=[];for(const s of[-1,1]){box(head,.05,.1,.08,skinM,s*.16,.22,0);box(head,.055,.028,.01,0x1b1511,s*.07,.28,.152);const b=box(head,.08,.02,.01,0x2a1d15,s*.07,.33,.152);b.userData.s=s;R.brows.push(b)}
  box(head,.05,.1,.07,skinM,0,.2,.17);R.mouth=box(head,.1,.018,.01,0x5a2a20,0,.1,.152);
  R.smile=box(head,.13,.05,.012,0xffffff,0,.1,.153);R.oMouth=box(head,.07,.08,.012,0x3a1510,0,.09,.153);
  R.face=(f)=>{R.mouth.visible=f==='neutral'||f==='angry'||f==='sad';R.smile.visible=f==='happy';R.oMouth.visible=f==='scared';
    for(const b of R.brows){const s=b.userData.s;b.rotation.z=f==='angry'?s*.4:f==='sad'||f==='scared'?-s*.35:0;b.position.y=f==='scared'?.35:.33}};R.face('neutral');
  if(cop){box(head,.34,.08,.36,0x0e1424,0,.47,.02);box(head,.3,.03,.14,0x0e1424,0,.44,.2);box(head,.07,.06,.01,0xe0b33a,0,.5,.2)}
  R.arms=[];
  for(const s of[1,-1]){
    const sh=grp(torso,s*.36,.67,0);box(sh,.15,.34,.17,suit,0,-.17,0);
    const el=grp(sh,0,-.34,0);box(el,.14,.3,.16,suit,0,-.15,0);box(el,.145,.05,.165,C.shirt,0,-.3,0);box(el,.12,.14,.1,skinM,0,-.39,0);
    R.arms.push({sh,el,s});
  }
  return R;
}

// ---------- props ----------
function umbrella(p,x,z,s=1){const g=grp(p,x,0,z);g.scale.setScalar(s);cyl(g,.035,.035,2.2,0xd8d2c0,0,1.1,0,6);const c=cyl(g,.02,1.15,.32,C.umb,0,2.25,0,9);box(g,.35,.06,.35,0xb3322b,0,.03,0);return g}
function palm(p,x,z,s=1,lean=.25){const g=grp(p,x,0,z);g.scale.setScalar(s);let y=0,xx=0;
  for(let i=0;i<7;i++){const seg=cyl(g,.11-i*.008,.14-i*.008,.8,C.palmT,xx,y+.4,0,7);seg.rotation.z=-lean*.5;y+=.76;xx+=lean*.35*(i/6)}
  const top=grp(g,xx,y,0);for(let i=0;i<9;i++){const f=grp(top);f.rotation.y=i/9*Math.PI*2;const lf=box(f,.36,.04,1.7,C.leaf,0,0,.8);lf.rotation.x=.45+ (i%2)*.2;
    const tip=box(f,.26,.04,.8,0x5c8a44,0,-.62,1.95);tip.rotation.x=.9}return g}
function lounger(p,x,z,rot=0){const g=grp(p,x,0,z);g.rotation.y=rot;
  box(g,.8,.08,1.5,C.chair,0,.4,.55);for(let i=0;i<5;i++)box(g,.82,.02,.12,0x5aa79e,0,.45,-.1+i*.3);
  const bk=grp(g,0,.42,-.2);box(bk,.8,.08,1.0,C.chair,0,0,-.5);bk.rotation.x=0.45;
  for(const s of[-1,1])for(const zz of[-.1,1.2]){box(g,.05,.4,.05,C.frame,s*.38,.2,zz)}box(g,.86,.05,.05,C.frame,0,.36,1.3);
  g.userData.back=bk;return g}
function policeCar(p){const g=grp(p);
  const blk=0x14171d,wht=0xf2f2ee;box(g,1.9,.55,4.3,blk,0,.62,0);box(g,1.95,.5,2.1,wht,0,.64,0);
  box(g,1.7,.55,2.2,wht,0,1.15,-.2);box(g,1.72,.36,1.6,0x1f2a36,0,1.2,-.2);box(g,1.5,.36,2.22,0x1f2a36,0,1.2,-.2);
  const txt=new THREE.MeshBasicMaterial({map:textTex('POLICE',{bg:null,fg:'#10151d',font:'800 90px M'}),transparent:true});
  for(const s of[-1,1]){const pl=new THREE.Mesh(new THREE.PlaneGeometry(1.8,.45),txt);pl.position.set(s*.98,.62,0);pl.rotation.y=s*Math.PI/2;g.add(pl)}
  const red=new THREE.MeshBasicMaterial({color:0xff2a2a}),blu=new THREE.MeshBasicMaterial({color:0x2a6bff});
  const lr=box(g,.55,.16,.34,red,-.3,1.5,-.2),lb=box(g,.55,.16,.34,blu,.3,1.5,-.2);
  box(g,1.8,.18,.12,0xbfc3c6,0,.45,2.18);box(g,1.8,.18,.12,0xbfc3c6,0,.45,-2.18);
  box(g,.4,.14,.04,0xfff6c8,-.6,.7,2.16);box(g,.4,.14,.04,0xfff6c8,.6,.7,2.16);
  const wheels=[];for(const s of[-1,1])for(const zz of[-1.35,1.35]){const w=cyl(g,.4,.4,.3,0x0d0d0d,s*.92,.4,zz,14);w.rotation.z=Math.PI/2;wheels.push(w);cyl(w,.2,.2,.32,0x9aa0a4,0,0,0,10)}
  g.userData={lr,lb,red,blu,wheels};return g}
function flash(car,t){const on=Math.floor(t*6)%2;car.userData.red.color.setHex(on?0xff2a2a:0x551010);car.userData.blu.color.setHex(on?0x1e2f55:0x3a7bff)}
function magnifier(p){const g=grp(p);const ring=new THREE.Mesh(new THREE.TorusGeometry(.6,.085,10,40),mat(0x1b2431));ring.castShadow=true;g.add(ring);
  const lens=new THREE.Mesh(new THREE.CircleGeometry(.56,40),new THREE.MeshBasicMaterial({color:0xdff6ff,transparent:true,opacity:.18,side:THREE.DoubleSide}));g.add(lens);
  const gl=box(g,.09,.32,.02,0xe8ecea,-.33,.28,.06);gl.rotation.z=.6;
  const hb=grp(g,0,-.66,0);cyl(hb,.08,.08,.18,0x1b2431,0,0,0,10);cyl(hb,.075,.09,.95,0x8a5a2b,0,-.55,0,10);return g}

// ---------- world builders ----------
function beachWorld(){const s=new THREE.Scene();s.background=paintTex(C.sky,512,1024,1400,16,1,[40,140]);
  s.fog=new THREE.Fog(0xa9dcc6,40,140);
  const sand=new THREE.Mesh(new THREE.PlaneGeometry(200,200),new THREE.MeshLambertMaterial({map:paintTex(C.sand,512,512,900,9,10,[10,50])}));
  sand.rotation.x=-Math.PI/2;sand.position.z=60;sand.receiveShadow=true;s.add(sand);
  const sea=new THREE.Mesh(new THREE.PlaneGeometry(400,200),new THREE.MeshLambertMaterial({color:C.sea}));sea.rotation.x=-Math.PI/2;sea.position.set(0,.03,-108);s.add(sea);
  const foam=new THREE.Mesh(new THREE.PlaneGeometry(400,.35),new THREE.MeshLambertMaterial({color:C.foam}));foam.rotation.x=-Math.PI/2;foam.position.set(0,.04,-8.1);s.add(foam);s.userData.foam=foam;
  const wet=new THREE.Mesh(new THREE.PlaneGeometry(400,1.6),new THREE.MeshLambertMaterial({color:0xb48d4c}));wet.rotation.x=-Math.PI/2;wet.position.set(0,.02,-7.2);s.add(wet);
  seed=11;for(let i=0;i<14;i++){const x=-22+i*3.4+rnd()*1.5;if(Math.abs(x)>2.2)umbrella(s,x,-4-rnd()*2.5,1)}
  for(let i=0;i<8;i++)umbrella(s,-18+i*5+rnd()*2,3-rnd()*3,1);
  palm(s,7,-2,1.4,.3);palm(s,-8,-3,1.3,-.25);palm(s,13,1,1.5,.2);
  return s}


// ---------- extra props & worlds ----------
function stars(s,n,R){seed=3;const g=new THREE.BufferGeometry();const p=[];for(let i=0;i<n;i++){const v=V(rnd()-.5,rnd()-.5,rnd()-.5).normalize().multiplyScalar(R);p.push(v.x,v.y,v.z)}
  g.setAttribute('position',new THREE.Float32BufferAttribute(p,3));const pts=new THREE.Points(g,new THREE.PointsMaterial({color:0xffffff,size:2.2,sizeAttenuation:false}));s.add(pts);return pts}
function cloud(p,x,y,z,s=1){const g=grp(p,x,y,z);g.scale.setScalar(s);seed=(x*100+z*7|0)+999;const m=mat(0xffffff);
  for(let i=0;i<5;i++){const c=new THREE.Mesh(new THREE.IcosahedronGeometry(.8+rnd()*.6,1),m);c.position.set((i-2)*.9+rnd()*.3,rnd()*.4,rnd()*.4);c.scale.y=.7;g.add(c)}return g}
function skyScene(col='#8fd0f0'){const s=new THREE.Scene();s.background=paintTex(col,512,1024,1400,14,1,[40,140]);return s}
function carSimple(p,col){const g=grp(p);box(g,1.8,.55,3.8,col,0,.62,0);box(g,1.6,.55,2,col,0,1.15,-.15);
  box(g,1.62,.36,1.5,0x1f2a36,0,1.18,-.15);box(g,1.4,.36,2.02,0x1f2a36,0,1.18,-.15);
  box(g,1.7,.16,.12,0xbfc3c6,0,.45,1.93);box(g,1.7,.16,.12,0xbfc3c6,0,.45,-1.93);box(g,.35,.14,.04,0xfff6c8,-.6,.7,1.91);box(g,.35,.14,.04,0xfff6c8,.6,.7,1.91);
  for(const s of[-1,1])for(const zz of[-1.2,1.2]){const w=cyl(g,.38,.38,.28,0x0d0d0d,s*.88,.38,zz,14);w.rotation.z=Math.PI/2;cyl(w,.18,.18,.3,0x9aa0a4,0,0,0,10)}return g}
function cow(p){const g=grp(p);const W=0xf4f1ea,B=0x1c1a18;box(g,1.5,.8,.75,W,0,1.1,0);
  box(g,.5,.45,.02,B,-.2,1.2,.38);box(g,.4,.35,.02,B,.4,1.0,-.38);box(g,.35,.3,.02,B,-.45,1.0,-.38);box(g,.3,.02,.3,B,.2,1.51,0);
  const h=grp(g,.85,1.35,0);box(h,.45,.48,.52,W,.1,0,0);box(h,.1,.26,.42,0xe8a0a0,.36,-.1,0);box(h,.02,.05,.05,B,.42,-.08,.1);box(h,.02,.05,.05,B,.42,-.08,-.1);
  for(const s of[-1,1]){box(h,.06,.06,.02,B,.2,.1,s*.265);box(h,.06,.14,.06,0xe8e0c8,0,.3,s*.18);box(h,.08,.06,.2,W,-.05,.15,s*.33)}
  const legs=[];for(const x of[-.55,.55])for(const z of[-.25,.25]){const lg=grp(g,x,.75,z);box(lg,.18,.6,.18,W,0,-.3,0);box(lg,.19,.12,.19,B,0,-.62,0);legs.push(lg)}
  box(g,.05,.5,.05,W,-.78,1.0,0).rotation.z=-.3;box(g,.1,.12,.1,B,-.86,.76,0);g.userData={legs,h};return g}
function house(p,x,z,col,roof=0x9a4a3a){const g=grp(p,x,0,z);box(g,3,2.2,3,col,0,1.1,0);const r=new THREE.Mesh(new THREE.ConeGeometry(2.35,1.3,4),mat(roof));r.rotation.y=Math.PI/4;r.position.y=2.85;r.castShadow=true;g.add(r);
  box(g,.6,1.1,.05,0x6b4a2e,0,.55,1.52);for(const s of[-1,1])box(g,.6,.55,.05,0x9fd3ea,s*.9,1.35,1.52);return g}
function tree(p,x,z,s=1){const g=grp(p,x,0,z);g.scale.setScalar(s);cyl(g,.12,.16,1.4,0x7a5530,0,.7,0,7);const c=new THREE.Mesh(new THREE.IcosahedronGeometry(.85,0),mat(0x5a9a45));c.position.y=1.8;c.castShadow=true;g.add(c);return g}
function earth(p,R=4){const geo=new THREE.IcosahedronGeometry(R,4);const pa=geo.attributes.position;const cols=[];
  for(let i=0;i<pa.count;i++){const x=pa.getX(i)/R,y=pa.getY(i)/R,z=pa.getZ(i)/R;const n=Math.sin(x*4.1+1)*Math.cos(y*3.3)+Math.sin(z*5.2+y*2)*.7;
    const c=Math.abs(y)>.85?new THREE.Color(0xf2f6f8):n>.35?new THREE.Color(0x5aa24a):new THREE.Color(0x2f7fcf);cols.push(c.r,c.g,c.b)}
  geo.setAttribute('color',new THREE.Float32BufferAttribute(cols,3));const m=new THREE.Mesh(geo,new THREE.MeshLambertMaterial({vertexColors:true,flatShading:true}));p.add(m);return m}
function paperTex(lines,{w=400,h=520,title='#111'}={}){const c=document.createElement('canvas');c.width=w;c.height=h;const g=c.getContext('2d');g.fillStyle='#fbf8ef';g.fillRect(0,0,w,h);
  g.textAlign='center';lines.forEach((l,i)=>{g.fillStyle=l.c||'#222';g.font=l.f||'800 44px M';g.fillText(l.t,w/2,l.y)});
  g.strokeStyle='rgba(0,0,0,.25)';g.lineWidth=4;for(let y=300;y<h-30;y+=40){g.beginPath();g.moveTo(50,y);g.lineTo(w-50-(y*7%90),y);g.stroke()}
  const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;t.anisotropy=8;return t}
function flail(m,t,amp=1){for(const a of m.arms){a.sh.rotation.z=a.s*(1.7+Math.sin(t*19+a.s)*.7*amp);a.sh.rotation.x=Math.sin(t*15+a.s*2)*.5*amp;a.el.rotation.x=-.5+Math.sin(t*21)*.4}
  m.legs.rotation.x=Math.PI/2+Math.sin(t*17)*.35*amp}
function stairY(x){return x<0?3:x>=4?0:3-(Math.floor(x/.4)+1)*.3}
function stairsWorld(){const s=new THREE.Scene();s.background=new THREE.Color(0xe9dcbf);
  const wall=new THREE.Mesh(new THREE.PlaneGeometry(30,14),new THREE.MeshLambertMaterial({map:paintTex('#e6d6b4',512,512,900,12,3)}));wall.position.set(2,5,-1);wall.receiveShadow=true;s.add(wall);
  const wood=0x9a6a3c;const fl=new THREE.Mesh(new THREE.PlaneGeometry(30,20),new THREE.MeshLambertMaterial({map:paintTex('#a8764a',512,512,900,16,6,[30,120])}));fl.rotation.x=-Math.PI/2;fl.receiveShadow=true;s.add(fl);
  box(s,4,3,1.8,0xd9c9a4,-2,1.5,0);box(s,4,.08,1.84,wood,-2,3.02,0);
  for(let i=0;i<10;i++){const top=3-(i+1)*.3;box(s,.4,top,1.6,0xd9c9a4,i*.4+.2,top/2,0);box(s,.44,.07,1.64,wood,i*.4+.2,top+.01,0)}
  box(s,.1,.4,1.8,0xc9b58f,-.02,3.2,0);
  // rail at back
  for(let i=0;i<11;i++){const x=i*.4,y=stairY(x-.01);cyl(s,.03,.03,1,0xf2eee4,x,y+.5,-.7,6)}
  const rail=box(s,4.4*1.25,.08,.08,wood,2,2.25,-.7);rail.rotation.z=-Math.atan2(3,4);
  // frames on wall
  const fr=(x,y,w,h,c)=>{box(s,w+.12,h+.12,.05,0x5b3b22,x,y,-.97);box(s,w,h,.06,c,x,y,-.96)};fr(-1.2,5.2,1,1.3,0x7fb6c9);fr(3.6,4.4,1.2,.9,0xd98f6a);fr(5.8,2.4,.8,1,0x9cc48a);
  lights(s,{sky:0xfff6e4,ground:0x8a6a4a,hemi:1.5,dir:1.8,pos:[4,10,8],target:[2,1,0],sh:8});return s}
function galaxyTex(){const S=512,c=document.createElement('canvas');c.width=c.height=S;const g=c.getContext('2d');
  for(let i=0;i<4000;i++){const arm=i%3;const r=Math.pow(rnd(),.7)*230;const a=arm*2.09+r*.022+(rnd()-.5)*.5;const x=256+Math.cos(a)*r,y=256+Math.sin(a)*r;
    g.fillStyle=`rgba(${190+rnd()*65|0},${140+rnd()*80|0},255,${.08+.25*(1-r/230)})`;g.beginPath();g.arc(x,y,1+rnd()*3,0,7);g.fill()}
  const rg=g.createRadialGradient(256,256,0,256,256,70);rg.addColorStop(0,'rgba(255,240,220,.9)');rg.addColorStop(1,'rgba(255,200,255,0)');g.fillStyle=rg;g.fillRect(0,0,S,S);
  const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;return t}
function skyWithClouds(col,n=10,spread=16){const s=skyScene(col);lights(s,{sky:0xffffff,ground:0x9fc3d8,pos:[5,10,8],sh:6});const cl=[];seed=21;
  for(let i=0;i<n;i++)cl.push(cloud(s,(rnd()-.5)*spread,(rnd()-.5)*spread*1.4,-6-rnd()*14,.8+rnd()*1.2));return{s,cl}}
function prison(){const s=new THREE.Scene();s.background=new THREE.Color(0xb9bbb0);
  const fl=new THREE.Mesh(new THREE.PlaneGeometry(30,30),new THREE.MeshLambertMaterial({map:paintTex('#c7c7bb',512,512,900,14,4)}));fl.rotation.x=-Math.PI/2;fl.receiveShadow=true;s.add(fl);
  const bt=brickTex();const wm=new THREE.MeshLambertMaterial({map:bt});
  const bw=new THREE.Mesh(new THREE.PlaneGeometry(8,5),wm);bw.position.set(0,2.5,-2.2);bw.receiveShadow=true;s.add(bw);
  for(const sx of[-1,1]){const sw=new THREE.Mesh(new THREE.PlaneGeometry(4.4,5),wm);sw.rotation.y=-sx*Math.PI/2;sw.position.set(sx*2.4,2.5,0);sw.receiveShadow=true;s.add(sw)}
  box(s,5,1.2,.4,0xa9ab9f,0,3.6,1.55);box(s,.5,5,.4,0xa9ab9f,-2.5,2.5,1.55);box(s,.5,5,.4,0xa9ab9f,2.5,2.5,1.55);
  const plaque=new THREE.Mesh(new THREE.PlaneGeometry(.7,.3),new THREE.MeshBasicMaterial({map:textTex('20',{w:256,h:110,bg:'#e8e8e2',fg:'#333',font:'700 70px M'})}));plaque.position.set(.8,3.25,1.76);s.add(plaque);
  const bars=[];const bm=mat(0x7e8f86);for(let i=0;i<12;i++){const x=-2.1+i*.38;const b=cyl(s,.055,.055,3,bm,x,1.5,1.6,8);bars.push(b)}
  box(s,4.5,.1,.1,bm,0,2.95,1.6);box(s,4.5,.1,.1,bm,0,.08,1.6);
  box(s,1.8,.1,.6,0x2b3036,-1.2,.55,-1.7);box(s,.08,.5,.08,0x2b3036,-1.9,.3,-1.5);box(s,.08,.5,.08,0x2b3036,-.5,.3,-1.5);
  box(s,.45,.5,.5,0xe6e6e0,1.8,.25,-1.8);
  lights(s,{sky:0xf4f2e6,ground:0x8a8a80,hemi:1.5,dir:1.4,pos:[3,9,9],target:[0,1,0],sh:6});
  const sun=sunDisc(s,3.6);sun.position.set(0,1.7,.2);
  const gl=new THREE.PointLight(0xffcc55,6,6,1.2);gl.position.set(0,1.7,.8);s.add(gl);
  s.userData={bars,sun,bm};return s}
function brickTex(){const c=document.createElement('canvas');c.width=c.height=512;const g=c.getContext('2d');g.fillStyle='#b9bbae';g.fillRect(0,0,512,512);
  g.strokeStyle='rgba(90,92,80,.35)';g.lineWidth=3;for(let r=0;r<16;r++){const y=r*32;g.beginPath();g.moveTo(0,y);g.lineTo(512,y);g.stroke();for(let x=(r%2)*48;x<512;x+=96){g.beginPath();g.moveTo(x,y);g.lineTo(x,y+32);g.stroke()}}
  const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;t.wrapS=t.wrapT=THREE.RepeatWrapping;t.repeat.set(2,1.4);return t}


// ---------- gravity cube character ----------
function gravFace(mood){const S=512,c=document.createElement('canvas');c.width=c.height=S;const g=c.getContext('2d');
  g.fillStyle='#3d3690';g.fillRect(0,0,S,S);for(let i=0;i<300;i++){g.fillStyle=`rgba(${70+rnd()*30|0},${60+rnd()*25|0},${150+rnd()*30|0},.3)`;g.beginPath();g.ellipse(rnd()*S,rnd()*S,20+rnd()*30,5,rnd()*3,0,7);g.fill()}
  // arrow
  g.fillStyle=mood==='glow'?'#fff6b0':'#f4f1ff';g.beginPath();g.moveTo(206,250);g.lineTo(306,250);g.lineTo(306,360);g.lineTo(356,360);g.lineTo(256,460);g.lineTo(156,360);g.lineTo(206,360);g.closePath();g.fill();
  // eyes
  for(const s of[-1,1]){const ex=256+s*85,ey=140;
    if(mood==='happy'||mood==='glow'){g.strokeStyle='#fff';g.lineWidth=16;g.lineCap='round';g.beginPath();g.arc(ex,ey+15,36,Math.PI*1.1,Math.PI*1.9);g.stroke()}
    else{g.fillStyle='#fff';g.beginPath();g.ellipse(ex,ey,40,48,0,0,7);g.fill();g.fillStyle='#111';g.beginPath();g.arc(ex+(mood==='side'?-16:0),ey+(mood==='sad'?14:6),20,0,7);g.fill();
      if(mood==='sad'){g.strokeStyle='#fff';g.lineWidth=12;g.lineCap='round';g.beginPath();g.moveTo(ex-s*40,ey-78);g.lineTo(ex+s*30,ey-58);g.stroke()}}}
  if(mood==='sad'){g.fillStyle='#8fd8ff';g.beginPath();g.ellipse(256+95,215,10,16,0,0,7);g.fill()}
  const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;return t}
const GF={};for(const m of['normal','happy','sad','side','glow'])GF[m]=gravFace(m);
function gravity(p){const side=mat(0x3a338a);const front=new THREE.MeshLambertMaterial({map:GF.normal});
  const m=new THREE.Mesh(new THREE.BoxGeometry(2,2,2),[side,side,side,side,front,side]);m.castShadow=true;const g=grp(p);g.add(m);g.userData={front,body:m};
  g.setMood=(k)=>{front.map=GF[k];front.needsUpdate=true};return g}

// ---------- moon / night ----------
function moonChar(p){const g=grp(p);seed=5;const geo=new THREE.IcosahedronGeometry(1,2);const pa=geo.attributes.position;
  for(let i=0;i<pa.count;i++){const v=V(pa.getX(i),pa.getY(i),pa.getZ(i));v.multiplyScalar(1+(rnd()-.5)*.045);pa.setXYZ(i,v.x,v.y,v.z)}geo.computeVertexNormals();
  const bodyM=mat(0xe6e3d3);const body=new THREE.Mesh(geo,bodyM);body.castShadow=true;g.add(body);
  const cm=mat(0xc2bfae);
  for(const [x,y,z,r] of [[.72,.5,.48,.17],[-.78,-.2,.58,.14],[.35,-.78,.52,.12],[-.42,.76,.5,.13],[.93,-.3,.2,.12],[-.92,.3,-.2,.18],[.5,.3,-.8,.2],[-.3,-.5,-.8,.15],[.1,.95,-.2,.1]]){
    const n=V(x,y,z).normalize();const c=new THREE.Mesh(new THREE.CylinderGeometry(r,r*.8,.06,9),cm);c.position.copy(n.clone().multiplyScalar(.99));c.quaternion.setFromUnitVectors(V(0,1,0),n);g.add(c)}
  const F=grp(g);const blk=mat(0x1d1b22);const eyes=[],lids=[],brows=[];
  for(const s of[-1,1]){const e=new THREE.Mesh(new THREE.SphereGeometry(.09,12,10),blk);e.position.set(s*.3,.2,.93);F.add(e);eyes.push(e);
    const l=box(F,.24,.13,.08,bodyM,s*.3,.33,.95);lids.push(l);const b=box(F,.22,.045,.04,0x5a5850,s*.3,.38,.93);b.userData.s=s;brows.push(b)}
  const smile=new THREE.Mesh(new THREE.TorusGeometry(.2,.035,6,16,Math.PI),blk);smile.position.set(0,-.12,.97);smile.rotation.z=Math.PI;F.add(smile);
  const frown=new THREE.Mesh(new THREE.TorusGeometry(.18,.035,6,16,Math.PI),blk);frown.position.set(0,-.3,.95);F.add(frown);
  const flat=box(F,.26,.04,.04,0x1d1b22,0,-.22,.96);
  const o=new THREE.Mesh(new THREE.SphereGeometry(.11,12,10),blk);o.scale.set(1,1.25,.4);o.position.set(0,-.25,.95);F.add(o);
  const blush=[];for(const s of[-1,1]){const b=box(F,.16,.07,.03,0xf0a0a0,s*.48,-.02,.87);blush.push(b)}
  const mask=box(F,1.0,.22,.12,0x4a3a78,0,.22,.9);
  const sweat=new THREE.Mesh(new THREE.SphereGeometry(.07,8,6),new THREE.MeshBasicMaterial({color:0x8fd8ff}));sweat.scale.y=1.5;sweat.position.set(.62,.45,.8);g.add(sweat);
  g.mood=(m)=>{smile.visible=m==='happy';frown.visible=m==='sad'||m==='angry';flat.visible=m==='tired'||m==='think'||m==='neutral';o.visible=m==='yawn'||m==='shock';
    blush.forEach(b=>b.visible=m==='happy');mask.visible=m==='sleep';eyes.forEach(e=>{e.visible=m!=='sleep';e.scale.setScalar(m==='shock'?1.3:1);e.position.y=m==='think'?.24:.2});
    lids.forEach(l=>{l.visible=m==='tired'||m==='yawn';l.position.y=m==='yawn'?.24:.27});sweat.visible=m==='tired'||m==='yawn';
    brows.forEach(b=>{const s=b.userData.s;b.rotation.z=m==='angry'?s*.45:m==='sad'||m==='tired'?-s*.3:0;b.position.y=m==='angry'?.33:m==='think'?.45:.38})};
  g.mood('neutral');g.userData={bodyM,cm,F};return g}
function picket(p,txt,col='#d23a2a'){const g=grp(p);cyl(g,.04,.04,1.8,0x8a5a2b,0,-.6,0,6);box(g,1.35,.72,.05,0xf6f1e4,0,.55,0);
  const t=new THREE.Mesh(new THREE.PlaneGeometry(1.25,.62),new THREE.MeshBasicMaterial({map:textTex(txt,{w:512,h:256,bg:null,fg:col,font:'900 92px M'}),transparent:true}));t.position.set(0,.55,.03);g.add(t);return g}
function faceEyes(p,z,sp=.35,r=.2){for(const s of[-1,1]){const w=new THREE.Mesh(new THREE.SphereGeometry(r,12,10),mat(0xffffff));w.position.set(s*sp,.25,z);w.scale.z=.5;p.add(w);
  const pu=new THREE.Mesh(new THREE.SphereGeometry(r*.5,10,8),mat(0x111111));pu.position.set(s*sp+.04,.23,z+r*.45);p.add(pu)}}
function nightSky(col='#1a2346'){const s=new THREE.Scene();s.background=paintTex(col,512,1024,1200,10,1,[40,140]);stars(s,700,70);return s}
function lamp(p,x,z,on=true){const g=grp(p,x,0,z);cyl(g,.06,.08,3.2,0x2b2f38,0,1.6,0,8);box(g,.5,.08,.12,0x2b2f38,.22,3.2,0);
  const b=box(g,.22,.14,.22,on?new THREE.MeshBasicMaterial({color:0xffe6a0}):0x3a3e48,.42,3.1,0);if(on){const l=new THREE.PointLight(0xffd890,8,7,1.3);l.position.set(.42,2.9,0);g.add(l)}return g}
function nightGround(s,col='#2b3350'){const gr=new THREE.Mesh(new THREE.PlaneGeometry(200,200),new THREE.MeshLambertMaterial({map:paintTex(col,512,512,900,10,12,[10,50])}));gr.rotation.x=-Math.PI/2;gr.receiveShadow=true;s.add(gr);return gr}
function litWindows(g){g.traverse(o=>{if(o.isMesh&&o.material.color&&o.material.color.getHex()===0x9fd3ea){o.material=new THREE.MeshBasicMaterial({color:0xffd66b})}})}
function pauseTex(){const c=document.createElement('canvas');c.width=c.height=256;const g=c.getContext('2d');g.fillStyle='rgba(20,24,40,.85)';g.beginPath();g.arc(128,128,120,0,7);g.fill();
  g.fillStyle='#fff';g.fillRect(80,70,34,116);g.fillRect(142,70,34,116);const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;return t}
function calTex(){const c=document.createElement('canvas');c.width=c.height=512;const g=c.getContext('2d');const tex=new THREE.CanvasTexture(c);tex.colorSpace=THREE.SRGBColorSpace;let last=-1;
  const draw=(p)=>{if(Math.abs(p-last)<.01)return;last=p;g.fillStyle='#fbf8ef';g.fillRect(0,0,512,512);g.fillStyle='#d23a2a';g.fillRect(0,0,512,92);
    g.fillStyle='#fff';g.font='900 56px M';g.textAlign='center';g.fillText('MOON SHIFTS',256,66);g.font='700 30px M';g.fillStyle='#333';
    for(let i=0;i<30;i++){const x=36+(i%7)*66,y=140+Math.floor(i/7)*78;g.strokeStyle='#bbb';g.lineWidth=2;g.strokeRect(x-26,y-30,60,70);g.fillText(i===14?'OFF':'✓'.replace('✓','•'),x+4,y+14)}
    if(p>0){const x=36+0*66+4,y=140+2*78+4;g.strokeStyle='#d23a2a';g.lineWidth=9;g.beginPath();g.ellipse(x,y,44,40,0,-Math.PI/2,-Math.PI/2+p*Math.PI*2);g.stroke()}
    tex.needsUpdate=true};draw(0);return{tex,draw}}

// ---------- earth / space ----------
function spiralTex(){const c=document.createElement('canvas');c.width=c.height=256;const g=c.getContext('2d');g.fillStyle='#fff';g.beginPath();g.arc(128,128,124,0,7);g.fill();
  g.strokeStyle='#111';g.lineWidth=12;g.beginPath();for(let a=0;a<Math.PI*7;a+=.05){const r=4+a*5;const x=128+Math.cos(a)*r,y=128+Math.sin(a)*r;a?g.lineTo(x,y):g.moveTo(x,y)}g.stroke();
  const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;return t}
const SPIRAL=spiralTex();
function earthChar(p,R=1.4){const g=grp(p);const ball=earth(g,R);const F=grp(g);const blk=mat(0x111111);
  const whites=[],pupils=[],spir=[],happy=[];
  for(const s of[-1,1]){const w=new THREE.Mesh(new THREE.SphereGeometry(R*.17,14,10),mat(0xffffff));w.position.set(s*R*.3,R*.22,R*.93);w.scale.z=.5;F.add(w);whites.push(w);
    const pu=new THREE.Mesh(new THREE.SphereGeometry(R*.085,10,8),blk);pu.position.set(s*R*.3,R*.2,R*1.0);F.add(pu);pupils.push(pu);
    const sp=new THREE.Mesh(new THREE.CircleGeometry(R*.17,24),new THREE.MeshBasicMaterial({map:SPIRAL}));sp.position.set(s*R*.3,R*.22,R*1.02);F.add(sp);spir.push(sp);
    const h=new THREE.Mesh(new THREE.TorusGeometry(R*.12,R*.025,6,14,Math.PI),blk);h.position.set(s*R*.3,R*.18,R*1.0);F.add(h);happy.push(h)}
  const smile=new THREE.Mesh(new THREE.TorusGeometry(R*.2,R*.03,6,16,Math.PI),blk);smile.rotation.z=Math.PI;smile.position.set(0,-R*.1,R*.99);F.add(smile);
  const oM=new THREE.Mesh(new THREE.SphereGeometry(R*.1,12,10),blk);oM.scale.set(1,1.3,.4);oM.position.set(0,-R*.25,R*.97);F.add(oM);
  const wob=new THREE.Mesh(new THREE.TorusGeometry(R*.16,R*.025,6,16,Math.PI),blk);wob.position.set(0,-R*.32,R*.95);F.add(wob);
  g.mood=(m)=>{const sp=m==='dizzy';spir.forEach(x=>x.visible=sp);whites.forEach(x=>{x.visible=m!=='happy'&&!sp;x.scale.setScalar(m==='shock'?1.35:1);x.scale.z=.5});
    pupils.forEach(x=>{x.visible=m!=='happy'&&!sp;x.scale.setScalar(m==='shock'?.8:1)});happy.forEach(x=>x.visible=m==='happy');
    smile.visible=m==='happy'||m==='neutral';oM.visible=m==='shock';wob.visible=sp||m==='sad'};
  g.mood('happy');g.userData={ball,F,spir};return g}
function sunFace(p,size=4){const g=grp(p);const d=sunDisc(g,size);const k=size/4;const blk=new THREE.MeshBasicMaterial({color:0x2a1608});
  const parts=[];for(const s of[-1,1]){const e=new THREE.Mesh(new THREE.CircleGeometry(.16*k,16),blk);e.position.set(s*.42*k,.2*k,.02);g.add(e);
    const b=new THREE.Mesh(new THREE.PlaneGeometry(.52*k,.11*k),blk);b.position.set(s*.42*k,.5*k,.02);b.rotation.z=s*.42;g.add(b)}
  const fr=new THREE.Mesh(new THREE.TorusGeometry(.32*k,.05*k,6,16,Math.PI),blk);fr.position.set(0,-.48*k,.02);g.add(fr);return g}
function giantHand(p){const g=grp(p);const sk=mat(0xe0ab84);box(g,2.0,2.1,.6,sk,0,0,0);
  const fingers=[];[-.72,-.24,.24,.72].forEach((x,i)=>{const f=grp(g,x,1.05,0);const len=[1.1,1.35,1.3,1.0][i];box(f,.4,len,.46,sk,0,len/2,0);box(f,.3,.08,.1,0xf2d0b8,0,len-.12,.24);fingers.push(f)});
  const th=grp(g,-1.05,.1,.1);box(th,.42,1.0,.46,sk,0,.45,0);th.rotation.z=.9;box(g,1.3,.9,.62,0xd99c74,0,-1.4,0);g.userData={fingers,th};return g}
function speedLines(s,n=30,spreadY=8,z=-2,col=0xffffff){const lm=new THREE.MeshBasicMaterial({color:col,transparent:true,opacity:.75});const out=[];seed=77;
  for(let i=0;i<n;i++){const l=new THREE.Mesh(new THREE.BoxGeometry(2.2+rnd()*2,.035,.035),lm);s.add(l);out.push({l,y:(rnd()-.5)*spreadY,z:z-rnd()*3,ph:rnd()*20})}
  return(t,speed=30)=>out.forEach(q=>q.l.position.set(10-((q.ph+t*speed)%20),q.y,q.z))}
function pajamaMan(p){const m=makeMan(p,{suit:0x7fa8dc});const st=mat(0xeaf2ff);
  for(const y of[.15,.35,.55])box(m.torso,.6,.05,.34,st,0,y,0);for(const s of[-1,1])for(const z of[.25,.6])box(m.legs,.23,.23,.06,st,s*.13,0,z);
  const cap=new THREE.Mesh(new THREE.ConeGeometry(.17,.42,8),mat(0x5a7fd0));cap.position.set(0,.6,-.02);cap.rotation.z=-.5;m.head.add(cap);
  const pom=new THREE.Mesh(new THREE.SphereGeometry(.05,8,6),mat(0xffffff));pom.position.set(.2,.78,-.02);m.head.add(pom);
  const pillow=box(m.arms[0].el,.4,.25,.55,0xffffff,0,-.45,.15);return m}
function bubble(p,txt,w=1.6,h=.8){const c=document.createElement('canvas');c.width=512;c.height=300;const g=c.getContext('2d');g.fillStyle='#fff';
  g.beginPath();g.roundRect(10,10,492,220,60);g.fill();g.beginPath();g.moveTo(120,220);g.lineTo(90,290);g.lineTo(190,220);g.fill();
  g.fillStyle='#111';g.font='900 86px M';g.textAlign='center';g.textBaseline='middle';g.fillText(txt,256,124);
  const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;const m=new THREE.Mesh(new THREE.PlaneGeometry(w,w*300/512),new THREE.MeshBasicMaterial({map:t,transparent:true}));p.add(m);return m}
function label(p,txt,w,h,opt){const m=new THREE.Mesh(new THREE.PlaneGeometry(w,h),new THREE.MeshBasicMaterial({map:textTex(txt,opt),transparent:true}));p.add(m);return m}
function spaceScene(){const s=nightSky('#0f1430');lights(s,{sky:0xd0d8ff,ground:0x1a1d33,hemi:1.2,dir:2.2,pos:[-4,3,8],sh:8});return s}

// ---------- clouds / weather ----------
function cloudChar(p,{storm=false,shades=false,bag=false}={}){const g=grp(p);const m=mat(storm?0x5d6474:0xffffff);seed=31;
  const puffs=[[0,0,0,1],[-.85,-.15,.05,.75],[.85,-.12,.05,.8],[-.4,.45,-.05,.7],[.45,.42,-.05,.72],[0,-.35,.25,.7]];
  for(const [x,y,z,r] of puffs){const c=new THREE.Mesh(new THREE.IcosahedronGeometry(r,1),m);c.position.set(x,y,z);c.castShadow=true;g.add(c)}
  const blk=mat(0x1d1b22);const F=grp(g,0,0,0);const eyes=[];
  for(const s of[-1,1]){const e=new THREE.Mesh(new THREE.SphereGeometry(.1,12,10),blk);e.position.set(s*.3,.1,.98);F.add(e);eyes.push(e)}
  const smile=new THREE.Mesh(new THREE.TorusGeometry(.18,.035,6,16,Math.PI),blk);smile.rotation.z=Math.PI;smile.position.set(0,-.12,1.0);F.add(smile);
  const frown=new THREE.Mesh(new THREE.TorusGeometry(.16,.035,6,16,Math.PI),blk);frown.position.set(0,-.3,.98);F.add(frown);
  const brows=[];for(const s of[-1,1]){const b=box(F,.2,.04,.04,0x1d1b22,s*.3,.3,.97);b.userData.s=s;brows.push(b)}
  const sh=grp(F);for(const s of[-1,1])box(sh,.3,.16,.05,0x15151a,s*.3,.12,1.04);box(sh,.2,.04,.04,0x15151a,0,.16,1.04);sh.visible=shades;
  let suit=null;if(bag){suit=grp(g,.6,-1.05,.3);box(suit,.6,.45,.22,0xc0503a,0,0,0);box(suit,.22,.06,.05,0x5a2a1a,0,.27,0);box(suit,.62,.06,.24,0xe8c070,0,-.05,0)}
  g.mood=(m)=>{smile.visible=m==='happy';frown.visible=m==='angry'||m==='sad';brows.forEach(b=>{const s=b.userData.s;b.rotation.z=m==='angry'?s*.45:m==='sad'?-s*.3:0;b.visible=m!=='happy'||!shades})};
  g.mood('happy');g.userData={sh,suit,mat:m};return g}
function sunHappy(p,size=4){const g=grp(p);sunDisc(g,size);const k=size/4;const blk=new THREE.MeshBasicMaterial({color:0x2a1608});
  for(const s of[-1,1]){const e=new THREE.Mesh(new THREE.TorusGeometry(.15*k,.04*k,6,14,Math.PI),blk);e.position.set(s*.42*k,.18*k,.02);g.add(e)}
  const sm=new THREE.Mesh(new THREE.TorusGeometry(.4*k,.05*k,6,18,Math.PI),blk);sm.rotation.z=Math.PI;sm.position.set(0,-.12*k,.02);g.add(sm);return g}
function poolGuy(p){const m=makeMan(p,{suit:0x1c2640});const ring=new THREE.Mesh(new THREE.TorusGeometry(.42,.13,10,20),mat(0xf0a020));ring.rotation.x=Math.PI/2;ring.position.y=.28;m.torso.add(ring);
  const sg=grp(m.head);for(const s of[-1,1])box(sg,.12,.07,.02,0x111111,s*.07,.28,.16);box(sg,.06,.02,.02,0x111111,0,.29,.16);m.shades=sg;return m}
function yard(s,{lawn='#7fb65a',water=true}={}){const gr=new THREE.Mesh(new THREE.PlaneGeometry(200,200),new THREE.MeshLambertMaterial({map:paintTex(lawn,512,512,900,14,20,[10,40])}));gr.rotation.x=-Math.PI/2;gr.receiveShadow=true;s.add(gr);
  const rim=mat(0xe8e4da);box(s,4.4,.12,.3,rim,0,.06,-1.85);box(s,4.4,.12,.3,rim,0,.06,1.85);box(s,.3,.12,4,rim,-2.05,.06,0);box(s,.3,.12,4,rim,2.05,.06,0);
  const hole=new THREE.Mesh(new THREE.PlaneGeometry(3.8,3.4),mat(0x9fb8c0));hole.rotation.x=-Math.PI/2;hole.position.y=.005;s.add(hole);
  const wat=new THREE.Mesh(new THREE.PlaneGeometry(3.8,3.4),new THREE.MeshLambertMaterial({color:0x3aa8d8,transparent:true,opacity:.92}));wat.rotation.x=-Math.PI/2;wat.position.y=.03;s.add(wat);wat.visible=water;
  return{gr,wat,hole}}
function rainLines(s,n=160,area=10){const lm=new THREE.MeshBasicMaterial({color:0xbfd8ff,transparent:true,opacity:.6});const out=[];seed=88;
  for(let i=0;i<n;i++){const l=new THREE.Mesh(new THREE.BoxGeometry(.015,.5,.015),lm);l.rotation.z=.15;s.add(l);out.push({l,x:(rnd()-.5)*area,z:(rnd()-.5)*area*.6,ph:rnd()*10})}
  return t=>out.forEach(q=>q.l.position.set(q.x+((q.ph+t*14)%8)*-.08,8-((q.ph+t*14)%8)*1.2,q.z))}
function weatherTex(){const c=document.createElement('canvas');c.width=720;c.height=440;const g=c.getContext('2d');g.fillStyle='#3a8fd0';g.fillRect(0,0,720,440);
  g.fillStyle='#fff';g.font='900 52px M';g.textAlign='center';g.fillText('7-DAY FORECAST',360,70);
  for(let i=0;i<7;i++){const x=60+i*100;g.fillStyle='#ffd52e';g.beginPath();g.arc(x,190,32,0,7);g.fill();g.fillStyle='#fff';g.font='700 26px M';g.fillText(['M','T','W','T','F','S','S'][i],x,135)}
  g.fillStyle='#d23a2a';g.fillRect(150,280,420,110);g.fillStyle='#fff';g.font='900 70px M';g.fillText('0% RAIN',360,358);
  const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;return t}
function postTex(){const c=document.createElement('canvas');c.width=650;c.height=425;const g=c.getContext('2d');g.fillStyle='#fbf3df';g.fillRect(0,0,650,425);
  g.strokeStyle='#d23a2a';g.lineWidth=10;g.strokeRect(10,10,630,405);g.fillStyle='#ffd52e';g.fillRect(510,30,110,120);g.fillStyle='#d23a2a';g.font='900 26px M';g.textAlign='center';g.fillText('☀',565,100);
  g.fillStyle='#222';g.font='900 54px M';g.textAlign='left';g.fillText('Please',40,110);g.fillText('come back.',40,180);g.font='700 38px M';g.fillText('Everyone misses you ♥',40,270);
  g.font='700 30px M';g.fillStyle='#666';g.fillText('— the Sun',40,350);const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;return t}

// ---------- clean rounded style (gig-video characters) ----------
const sm=(c,r=.75)=>new THREE.MeshStandardMaterial({color:c,roughness:r,metalness:0});
const RB=(p,w,h,d,r,m,x=0,y=0,z=0)=>{const o=new THREE.Mesh(new RoundedBoxGeometry(w,h,d,4,Math.min(r,w/2-.001,h/2-.001,d/2-.001)),m.isMaterial?m:sm(m));o.position.set(x,y,z);o.castShadow=o.receiveShadow=true;p.add(o);return o};
const SPH=(p,r,m,x=0,y=0,z=0,seg=20)=>{const o=new THREE.Mesh(new THREE.SphereGeometry(r,seg,seg*3/4|0),m.isMaterial?m:sm(m));o.position.set(x,y,z);o.castShadow=true;p.add(o);return o};
function cleanMan(p,{suit=0x24345e,shirt=0xf6f4ee,tie=0xd8423a,skin=0xf0c09a,hair=0x2a1c14,pants=null}={}){
  const R={};const S=sm(skin,.6),SU=sm(suit,.7),PA=sm(pants??suit,.7),blk=sm(0x15151a,.4),wh=sm(0xffffff,.3);R.skinM=S;
  const root=grp(p);R.root=root;
  R.legs=[];for(const s of[-1,1]){const lg=grp(root,s*.13,0,0);RB(lg,.22,.88,.24,.09,PA,0,-.44,0);RB(lg,.24,.14,.38,.07,sm(0x2b2b30,.5),0,-.9,.07);R.legs.push(lg)}
  const torso=grp(root);R.torso=torso;RB(torso,.64,.78,.38,.15,SU,0,.4,0);
  RB(torso,.2,.4,.04,.02,sm(shirt),0,.55,.185);RB(torso,.08,.34,.03,.015,sm(tie,.5),0,.5,.205);RB(torso,.11,.07,.035,.02,sm(tie,.5),0,.7,.205);
  for(const s of[-1,1]){const l=RB(torso,.11,.42,.035,.03,SU,s*.12,.55,.19);l.rotation.z=s*.32}
  RB(torso,.17,.12,.17,.06,S,0,.82,0);
  const head=grp(torso,0,.86,0);R.head=head;RB(head,.5,.54,.46,.18,S,0,.27,0);
  RB(head,.53,.17,.49,.08,sm(hair,.8),0,.54,-.01);RB(head,.53,.36,.12,.06,sm(hair,.8),0,.38,-.2);RB(head,.18,.12,.08,.04,sm(hair,.8),-.14,.5,.2);
  for(const s of[-1,1])SPH(head,.07,S,s*.26,.26,0,12);
  R.eyes=[];R.pupils=[];R.brows=[];
  for(const s of[-1,1]){const e=SPH(head,.075,wh,s*.11,.31,.22,16);e.scale.set(1,1.15,.55);R.eyes.push(e);
    const pu=SPH(head,.045,blk,s*.11,.3,.258,14);pu.scale.set(1,1.15,.5);R.pupils.push(pu);SPH(head,.013,wh,s*.11+.015,.325,.272,8);
    const b=RB(head,.12,.03,.03,.012,sm(hair,.6),s*.11,.41,.225);b.userData.s=s;R.brows.push(b)}
  RB(head,.07,.09,.06,.03,S,0,.22,.24);
  R.smile=new THREE.Mesh(new THREE.TorusGeometry(.08,.016,8,20,Math.PI),blk);R.smile.rotation.z=Math.PI;R.smile.position.set(0,.13,.23);head.add(R.smile);
  R.frown=new THREE.Mesh(new THREE.TorusGeometry(.07,.016,8,20,Math.PI),blk);R.frown.position.set(0,.06,.225);head.add(R.frown);
  R.oM=SPH(head,.045,sm(0x5a1a1a,.5),0,.11,.225,12);R.oM.scale.set(1,1.25,.4);
  R.face=(f)=>{R.smile.visible=f==='happy'||f==='neutral';R.smile.scale.setScalar(f==='neutral'?.6:1);R.frown.visible=f==='sad';R.oM.visible=f==='shock';
    R.brows.forEach(b=>{const s=b.userData.s;b.rotation.z=f==='sad'?-s*.3:f==='angry'?s*.35:0;b.position.y=f==='shock'?.44:.41});
    R.eyes.forEach(e=>e.scale.set(f==='shock'?1.2:1,f==='shock'?1.35:1.15,.55))};R.face('neutral');
  R.arms=[];for(const s of[1,-1]){const sh=grp(torso,s*.38,.7,0);RB(sh,.17,.4,.18,.08,SU,0,-.18,0);const el=grp(sh,0,-.38,0);RB(el,.16,.34,.17,.07,SU,0,-.16,0);
    RB(el,.165,.05,.175,.02,sm(shirt),0,-.33,0);SPH(el,.085,S,0,-.41,0,14);R.arms.push({sh,el,s})}
  R.sit=()=>{R.legs.forEach(l=>l.rotation.x=-Math.PI/2+.05)};return R}
function canvasTex(w,h,draw){const c=document.createElement('canvas');c.width=w;c.height=h;const g=c.getContext('2d');const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;t.anisotropy=8;
  return{tex:t,draw:(...a)=>{draw(g,w,h,...a);t.needsUpdate=true}}}
function laptop(p,draw){const g=grp(p);RB(g,1.1,.05,.75,.02,sm(0x9aa0aa,.4),0,.025,0);const lid=grp(g,0,.05,-.36);RB(lid,1.1,.72,.04,.02,sm(0x9aa0aa,.4),0,.36,0);
  const sc=canvasTex(640,400,draw);const s=new THREE.Mesh(new THREE.PlaneGeometry(1.0,.62),new THREE.MeshBasicMaterial({map:sc.tex}));s.position.set(0,.36,.022);lid.add(s);lid.rotation.x=-.18;g.userData={sc,lid};return g}
function room(){const s=new THREE.Scene();s.background=new THREE.Color(0xe9dfd0);
  const wall=new THREE.Mesh(new THREE.PlaneGeometry(30,14),new THREE.MeshStandardMaterial({map:paintTex('#eadfce',512,512,500,8,3),roughness:.9}));wall.position.set(0,5,-3.2);wall.receiveShadow=true;s.add(wall);
  const fl=new THREE.Mesh(new THREE.PlaneGeometry(30,20),new THREE.MeshStandardMaterial({map:paintTex('#b88a5e',512,512,600,12,6,[40,140]),roughness:.8}));fl.rotation.x=-Math.PI/2;fl.receiveShadow=true;s.add(fl);
  const win=grp(s,-1.7,2.9,-3.15);RB(win,2.0,1.5,.08,.04,sm(0xffffff,.5));const sky=new THREE.Mesh(new THREE.PlaneGeometry(1.8,1.3),new THREE.MeshBasicMaterial({color:0x9fd6f2}));sky.position.z=.05;win.add(sky);
  RB(win,.06,1.3,.06,.02,sm(0xffffff,.5),0,0,.07);RB(win,1.8,.06,.06,.02,sm(0xffffff,.5),0,0,.07);
  const plant=grp(s,2.6,0,-2.4);RB(plant,.5,.6,.5,.12,sm(0xd8734a,.6),0,.3,0);for(let i=0;i<6;i++){const l=SPH(plant,.28,sm(0x5aa05a,.7),Math.cos(i)*.18,.85+(i%3)*.15,Math.sin(i)*.18,12);l.scale.set(1,1.3,1)}
  const shelf=grp(s,1.4,3.0,-3.05);RB(shelf,1.6,.08,.35,.02,sm(0xa8784e,.6));['#d8423a','#3a7bd5','#f2b33a'].forEach((c,i)=>RB(shelf,.16,.45,.3,.03,sm(c),-.5+i*.2,.27,0));
  const hemi=new THREE.HemisphereLight(0xfff6ea,0x8a7258,1.6);s.add(hemi);const d=new THREE.DirectionalLight(0xfff0dd,2.2);d.position.set(3,8,6);d.castShadow=true;d.shadow.mapSize.set(2048,2048);
  const c=d.shadow.camera;c.left=c.bottom=-6;c.right=c.top=6;d.shadow.bias=-.0008;d.shadow.normalBias=.03;d.shadow.radius=6;s.add(d);s.userData={sky,win};return s}
function deskSet(s,draw){const desk=grp(s,0,0,0);RB(desk,2.6,.1,1.2,.04,sm(0xc49a6c,.6),0,1.0,0);for(const x of[-1.2,1.2])for(const z of[-.5,.5])RB(desk,.08,1.0,.08,.03,sm(0x7a5a3a,.6),x,.5,z);
  const lt=laptop(s,draw);lt.position.set(0,1.05,.05);lt.rotation.y=Math.PI;const chair=grp(s,0,0,-1.05);chair.rotation.y=Math.PI;RB(chair,.7,.1,.7,.04,sm(0x2b3240,.5),0,.62,0);RB(chair,.7,.8,.1,.05,sm(0x2b3240,.5),0,1.05,.32);cyl(chair,.04,.04,.6,0x555555,0,.3,0,8);
  return{desk,lt,chair}}
function studio(col){const s=new THREE.Scene();s.background=new THREE.Color(col);const h=new THREE.HemisphereLight(0xffffff,0x606070,1.8);s.add(h);
  const d=new THREE.DirectionalLight(0xffffff,2);d.position.set(3,6,8);d.castShadow=true;s.add(d);return s}
function confetti(s,n=80){const out=[];seed=12;const cols=[0xff5a2a,0x2f86d8,0x5cc06a,0xf2b33a,0x9b59b6];for(let i=0;i<n;i++){const m=new THREE.Mesh(new THREE.PlaneGeometry(.08,.14),new THREE.MeshBasicMaterial({color:cols[i%5],side:THREE.DoubleSide}));s.add(m);
  out.push({m,x:(rnd()-.5)*8,z:(rnd()-.5)*3,ph:rnd()*4,sp:.8+rnd()})}return t=>out.forEach(q=>{const y=4.5-((q.ph+t*q.sp)%5);q.m.position.set(q.x+Math.sin(t*2+q.ph)*.2,y,q.z);q.m.rotation.set(t*3+q.ph,t*2,q.ph)})}

// ---------- runtime ----------
export async function loadTiming(){return await (await fetch('timing.json')).json()}
// shots: [{start:sec, build:()=>({s:Scene, u:(localT)=>void})}], END: total seconds
export function run(shots,END){shots.sort((a,b)=>a.start-b.start);
  const renderAt=(t)=>{let si=0;for(let i=0;i<shots.length;i++)if(t>=shots[i].start)si=i;const sh=shots[si];
    if(!sh.inst){for(const o of shots)if(o!==sh&&o.inst){o.inst.s.traverse(x=>{x.geometry&&x.geometry.dispose();if(x.material){(Array.isArray(x.material)?x.material:[x.material]).forEach(m=>{m.dispose()})}});o.inst=null}sh.inst=sh.build()}
    sh.inst.u(t-sh.start);camera.aspect=W/H;camera.updateProjectionMatrix();renderer.render(sh.inst.s,camera);return si};
  window.renderAt=renderAt;window.frameJPEG=(t,q=0.93)=>{renderAt(t);return renderer.domElement.toDataURL('image/jpeg',q)};
  window.END=END;window.SHOTS=shots.map(s=>s.start);window.READY=true;}
export {C,GF,RB,RoundedBoxGeometry,SPH,SPIRAL,SUNTEX,V,add,back,beachWorld,box,brickTex,bubble,calTex,canvasTex,carSimple,clamp,cleanMan,cloud,cloudChar,confetti,cow,cyl,deskSet,earth,earthChar,ease,eout,faceEyes,flail,flash,galaxyTex,giantHand,gravFace,gravity,grp,house,label,lamp,laptop,lerp,lights,litWindows,lounger,magnifier,makeMan,mat,moonChar,nightGround,nightSky,paintTex,pajamaMan,palm,paperTex,pauseTex,picket,policeCar,poolGuy,postTex,prison,rainLines,rnd,room,skyScene,skyWithClouds,sm,spaceScene,speedLines,spiralTex,stairY,stairsWorld,stars,studio,sunDisc,sunFace,sunHappy,sunTex,textTex,tree,umbrella,weatherTex,yard};
