// EXAMPLE: "What Happens If You Drink ONLY Coffee for 3 Days?" (34 s, 17 shots). Copy the pattern, not the content.
import {faceEyes,W,H,THREE,camera,cam,clamp,ease,eout,back,lerp,V,grp,RB,SPH,sm,cyl,paintTex,setSeed,rnd,carSimple,lamp} from './engine.js';
import * as K from './lib.js';
await K.initTimeline({t0:0.15,tail:0.25});
const {BB,COF,GLOW,HEADY,L,bedroom,brain,brainPt,camS,clockTex,dynTex,ecgDraw,glow,gradTex,hand,heart,hpop,hud,kid,kitchen,molecule,monitor,mug,pop,shadowMan,shakeT,shot,shots,sstep,steam,stomach,studio2,txt,updPulses,wallClock,wordT,xrayScene}=K;
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
  const hm=new THREE.Mesh(new THREE.PlaneGeometry(1,.25),new THREE.MeshBasicMaterial({map:cnt.t,transparent:true,depthTest:false,depthWrite:false,fog:false}));hm.userData.hud={yf:.85,wf:.74};K.hudMesh(hm,hm.userData.hud);
  return{s,u(t){cups.forEach(q=>{const k2=clamp((t*1.3-q.at*1.6)/.25);q.m.visible=k2>0;q.m.scale.setScalar(Math.max(.001,back(k2)))});
    cnt.set(Math.min(99,Math.floor(Math.pow(t*2.6,2.2))+1));hm.userData.k=back(t/.25);
    const e=ease(t/2.4);cam(40,[lerp(.3,.2,e),lerp(2.0,1.9,e),lerp(5.3,4.9,e)],[0,1.6,0])}}});

K.go();
