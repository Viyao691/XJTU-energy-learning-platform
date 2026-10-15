"use client";
import { Suspense, useEffect, useLayoutEffect, useMemo, useRef, memo, type ComponentRef, type Ref } from 'react';
import { Canvas, useThree, useFrame } from '@react-three/fiber';
import { AccumulativeShadows, RandomizedLight, Environment, Lightformer, ContactShadows, useTexture, useGLTF } from '@react-three/drei';
import * as T from 'three';
import { createLiveOrb } from './orb-live';
import { makeInteraction, SUBJECTS, type Subject } from './interactions';
import layout from '../../public/home-hero/scene-layout.json';
import {campusInteraction} from './campus';
import cityThemes from '../../public/home-hero/city-theme.json';
import {LightDesk,WindowSun} from './LightDesk';
import {StillLife} from './StillLife';
import {DeskObjects} from './DeskObjects';
import {featureLayout,type AnchorMap} from './feature-layout';
export type Theme = 'light' | 'dark';
const ROOT='/home-hero/models/';
const GROUND_Y=0;
type SceneProps={theme:Theme;onReady:()=>void;hovered:Subject|null;onHover:(name:Subject|null)=>void;overview?:boolean;environmentOnly?:boolean;onAnchors?:(anchors:AnchorMap)=>void};
type Placement={x:number;y:number;width?:number;height?:number;angle:number};
const C=new T.Matrix4().set(1,0,0,0,0,0,1,0,0,-1,0,0,0,0,0,1);
function calibrated(group:T.Group,key:string){
 const entry=(layout.subjects as Record<string,{matrix:number[][]}>)[key.toUpperCase()];
 const content=new T.Group();content.add(...group.children.slice());group.add(content);
 if(key==='orb'){const box=new T.Box3().setFromObject(content);content.position.y-=box.min.y;}
 const rows=entry.matrix;const matrix=new T.Matrix4().set(...rows.flat() as [number,number,number,number,number,number,number,number,number,number,number,number,number,number,number,number]);
 group.applyMatrix4(C.clone().multiply(matrix).multiply(C.clone().invert()));group.updateMatrixWorld(true);
}
// Diagnostic hulls allow the browser check to compare silhouettes, rather than overlapping boxes.
function silhouette(points:number[][]){
 const p=points.sort((a,b)=>a[0]-b[0]||a[1]-b[1]),cross=(a:number[],b:number[],c:number[])=>(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]);
 const half=(a:number[][])=>{const h:number[][]=[];for(const v of a){while(h.length>1&&cross(h[h.length-2],h[h.length-1],v)<=0)h.pop();h.push(v);}return h.slice(0,-1);};
 return [...half(p),...half([...p].reverse())];
}
function cloneAsset(source:T.Group,name:string,theme:Theme){
 const clone=source.clone(true),materials=new Map<T.Material,T.Material>();
 clone.traverse(o=>{if(!(o instanceof T.Mesh))return;o.castShadow=true;o.receiveShadow=true;
 const src=o.material as T.MeshStandardMaterial;let material=materials.get(src) as T.MeshStandardMaterial;
 if(!material){material=src.clone();materials.set(src,material);material.name=material.name.replace(/^CITY V4 \| /,'');
  if(name==='city'){
   const preset=(cityThemes[theme] as Record<string,{baseColor:number[];metalness:number;roughness:number;emissiveIntensity:number}>)[material.name];
   if(preset){material.color.fromArray(preset.baseColor);material.metalness=preset.metalness;material.roughness=preset.roughness;material.emissiveIntensity=preset.emissiveIntensity;}
   if(material.name.startsWith('15')){material.emissiveIntensity=0;material.color.set(theme==='dark'?'#354452':'#aaa99e');}
   if(material.name.startsWith('07'))material.emissiveIntensity=theme==='dark'?2:.12;
   if(theme==='dark'&&/^(01|02)/.test(material.name)){material.color.set('#7e8d9e');material.roughness=.48;}
   if(theme==='dark'&&material.name.startsWith('05'))material.color.set('#344f68');
   if(theme==='dark'&&material.name.startsWith('16'))material.emissiveIntensity=1.5;
   material.envMapIntensity=material.name.startsWith('05')?1.3:.75;
   if(material.name.startsWith('05')){material.roughness=.22;material.metalness=.48;}
  }else{material.envMapIntensity=theme==='dark'?1.05:.85;
   if(name==='storage'&&material.name.startsWith('01')){material.color.set(theme==='dark'?'#b2bdc7':'#d9ceba');material.metalness=.38;material.roughness=material.roughnessMap?.94:.38;}
   if(name==='storage'&&material.name.startsWith('02')){material.color.set('#7a8589');material.metalness=.88;material.roughness=.26;}
   if(name==='storage'&&material.name.startsWith('05')){material.color.set('#273b43');material.metalness=.54;material.roughness=.38;}
   if(material.name.startsWith('03')){material.metalness=.95;material.roughness=.23;}
   if(name==='storage'&&theme==='dark'&&material.name.startsWith('08')){material.emissive.set('#ffd49a');material.emissiveIntensity=1.2;}
   if(name==='wind'&&material.name.startsWith('01')){material.color.set('#c7cbc9');material.roughness=.34;material.metalness=.32;}
   if(name==='solar'&&material.name.includes('silicon')){material.color.set('#10283e');material.roughness=.26;material.metalness=.36;}
   if(name==='solar'&&material.name==='Solar clear cover'){
    const glass=material as T.MeshPhysicalMaterial;glass.transmission=0;glass.transparent=true;glass.opacity=.055;glass.depthWrite=false;glass.roughness=.20;glass.metalness=.05;glass.envMapIntensity=1.1;
   }
   if(name==='solar'&&material.name.includes('aluminium')){material.color.set('#a9b5b9');material.metalness=.9;material.roughness=.24;}
   if(name==='paper'){material.roughness=.96;material.metalness=0;material.envMapIntensity=.08;if(material.map)material.map.anisotropy=16;}
  }
 }o.material=material;
 });
 // The modular city keeps shared geometry; repeated primitives are batched in world space once.
 if(['city','coffee','books','plant','pen'].includes(name)){
  clone.updateMatrixWorld(true);const batches=new Map<string,T.Mesh[]>();
  clone.traverse(o=>{if(o instanceof T.Mesh){const k=o.geometry.uuid+':'+(o.material as T.Material).uuid;const list=batches.get(k)||[];list.push(o);batches.set(k,list);}});
  for(const parts of batches.values())if(parts.length>1){const inst=new T.InstancedMesh(parts[0].geometry,parts[0].material,parts.length);parts.forEach((o,i)=>{inst.setMatrixAt(i,o.matrixWorld);o.removeFromParent();});inst.castShadow=true;inst.receiveShadow=true;inst.instanceMatrix.needsUpdate=true;clone.add(inst);}
 }
 
 if(name==='paper'){clone.userData.blenderAsset=true;if(theme==='light')clone.traverse(o=>{const layer=Number(o.name.match(/PaperLeaf_(\d)/)?.[1]);if(Number.isFinite(layer))o.position.y+=layer*.0035;});}
 return clone;
}
const GroundShadows=memo(function GroundShadows({theme,shadowRef}:{theme:Theme;shadowRef:Ref<ComponentRef<typeof AccumulativeShadows>>}){
 return <AccumulativeShadows ref={shadowRef} frames={Infinity} blend={48} limit={0} color={theme==='dark'?'#020a12':'#685c4b'} colorBlend={1.5} opacity={theme==='dark'?.50:.25} alphaTest={.84} scale={32} position={[0,.001,0]} resolution={4096}>
  <RandomizedLight amount={6} radius={theme==='light'?2.6:3.4} ambient={.42} intensity={Math.PI} position={[4.9,8,-10.3]} size={18} near={.1} far={70} mapSize={2048}/>
 </AccumulativeShadows>;
});
function Assets({theme,onReady,hovered,onHover,overview=false,onAnchors}:SceneProps){
 const {camera,invalidate,scene:renderScene,gl,size}=useThree();
 const hoverRef=useRef(hovered);hoverRef.current=hovered;const overviewRef=useRef(overview);overviewRef.current=overview;
 const reduced=useRef(false);
 const shadow=useRef<ComponentRef<typeof AccumulativeShadows>>(null);
 const city=useGLTF('/home-hero/models/city.glb'),storage=useGLTF(ROOT+'storage.glb'),wind=useGLTF('/home-hero/models/wind.glb'),solar=useGLTF(ROOT+'solar.glb');
 const paper=useGLTF('/home-hero/models/paper.glb');
 const pen=useGLTF('/home-hero/models/pen.glb');
 const props=useMemo(()=>{const g=cloneAsset(pen.scene,'pen',theme);calibrated(g,'pen');g.position.z+=.65;return [g];},[pen.scene,theme]);
 const models=useMemo(()=>{
  const m:Record<Subject,T.Group>={city:cloneAsset(city.scene,'city',theme),storage:cloneAsset(storage.scene,'storage',theme),wind:cloneAsset(wind.scene,'wind',theme),solar:cloneAsset(solar.scene,'solar',theme),orb:createLiveOrb(theme==='dark'),paper:cloneAsset(paper.scene,'paper',theme)};
  for(const [name,group] of Object.entries(m)){group.name='hero-'+name;calibrated(group,name);if(name==='solar')group.position.x-=.42;}return m;
 },[city.scene,storage.scene,wind.scene,solar.scene,paper.scene,theme,camera,size.width,size.height]);
 useEffect(()=>{
  const ray=new T.Raycaster(),point=new T.Vector2(),anchors:AnchorMap={},evidence:Record<string,unknown>={};
  renderScene.updateMatrixWorld(true);const roots=Object.values(models);
  for(const feature of featureLayout){let found=false;
   for(const radius of [0,4,9,16,25,38,56,80]){if(found)break;
    for(let a=0;a<(radius?24:1);a++){const angle=a*Math.PI/12,x=feature.preferred[0]+radius*Math.cos(angle),y=feature.preferred[1]+radius*Math.sin(angle);point.set(x/960-1,1-y/540);ray.setFromCamera(point,camera);
     const hit=ray.intersectObjects(roots,true).find(h=>h.object instanceof T.Mesh&&h.object.material instanceof T.MeshStandardMaterial);if(!hit)continue;
     let parent:T.Object3D|null=hit.object;while(parent&&parent!==models[feature.model])parent=parent.parent;if(!parent)continue;
     anchors[feature.id]=[x,y];evidence[feature.id]={model:feature.model,world:hit.point.toArray(),screen:[x,y]};found=true;break;
    }
   }
  }
  onAnchors?.(anchors);Object.assign(window,{heroAnchors:evidence});
 },[models,camera,renderScene,size.width,size.height,onAnchors]);
 const controllers=useMemo(()=>Object.fromEntries(SUBJECTS.map(name=>[name,{baseScale:models[name].scale.x,blend:0}])) as Record<Subject,{effect?:ReturnType<typeof makeInteraction>;baseScale:number;blend:number}>,[models]);
 useEffect(()=>{
  // Own shader/ribbon lifetimes in an effect, including React's development replay.
  for(const name of SUBJECTS)controllers[name].effect=name==='city'?campusInteraction(models[name],theme==='dark'):makeInteraction(models[name],name,theme==='dark');
  return()=>{for(const name of SUBJECTS){controllers[name].effect?.dispose();controllers[name].effect=undefined;}};
 },[models,controllers,theme]);
 useEffect(()=>{
  const preference=matchMedia('(prefers-reduced-motion: reduce)');const update=()=>{reduced.current=preference.matches;invalidate();};update();preference.addEventListener('change',update);
  const timer=setInterval(()=>{if(!document.hidden&&(!reduced.current||hoverRef.current||SUBJECTS.some(n=>controllers[n].blend>.001)))invalidate();},33);
  return()=>{clearInterval(timer);preference.removeEventListener('change',update);};
 },[invalidate,controllers]);
 useFrame((_,delta)=>{
  const dt=Math.min(delta,.05);
  for(const name of SUBJECTS){const entry=controllers[name];entry.blend=T.MathUtils.damp(entry.blend,overviewRef.current||hoverRef.current===name?1:0,8,dt);entry.effect?.update(entry.blend,dt,reduced.current);
   models[name].scale.setScalar(entry.baseScale*(1+(reduced.current?0:entry.blend)*(name==='storage'?.018:name==='city'?.006:name==='wind'?.008:0)));
  }
 });
 useEffect(()=>{
  const ray=new T.Raycaster(),all=Object.values(models);const point=new T.Vector2();
  const hitPoint=(name:Subject)=>{
   const bounds=new T.Box3().setFromObject(models[name]),lo=new T.Vector2(Infinity,Infinity),hi=new T.Vector2(-Infinity,-Infinity);
   for(const x of [bounds.min.x,bounds.max.x])for(const y of [bounds.min.y,bounds.max.y])for(const z of [bounds.min.z,bounds.max.z]){const v=new T.Vector3(x,y,z).project(camera);lo.min(new T.Vector2(v.x,v.y));hi.max(new T.Vector2(v.x,v.y));}
   for(const fy of [.55,.4,.7,.25,.85])for(const fx of [.5,.35,.65,.2,.8]){point.set(T.MathUtils.lerp(lo.x,hi.x,fx),T.MathUtils.lerp(lo.y,hi.y,fy));ray.setFromCamera(point,camera);const hit=ray.intersectObjects(all,true)[0];if(!hit)continue;let o:T.Object3D|null=hit.object;while(o&&o!==models[name])o=o.parent;if(o)return{x:(point.x+1)*size.width/2,y:(1-point.y)*size.height/2};}
   return null;
  };
  const spatial=()=>Object.fromEntries(['paper','storage'].map(n=>{const points:number[][]=[],bounds=new T.Box3(),v=new T.Vector3(),lo=new T.Vector2(Infinity,Infinity),hi=new T.Vector2(-Infinity,-Infinity);models[n as Subject].traverse(o=>{if(o instanceof T.Mesh&&o.material instanceof T.MeshStandardMaterial){for(let i=0;i<o.geometry.getAttribute('position').count;i++){o.getVertexPosition(i,v);v.applyMatrix4(o.matrixWorld);bounds.expandByPoint(v);v.project(camera);const p=new T.Vector2((v.x+1)*size.width/2,(1-v.y)*size.height/2);lo.min(p);hi.max(p);points.push([p.x,p.y]);}}});return[n,{minY:bounds.min.y,hull:silhouette(points),rect:[lo.x,lo.y,hi.x,hi.y]}];}));
  const snapshot=()=>({models:SUBJECTS,sceneRaster:false,groundY:GROUND_Y,spatial:spatial(),overview:overviewRef.current,hover:hoverRef.current,blend:Math.max(...SUBJECTS.map(n=>controllers[n].blend)),reducedMotion:reduced.current,renderer:{calls:gl.info.render.calls,triangles:gl.info.render.triangles},effects:Object.fromEntries(SUBJECTS.map(n=>[n,controllers[n].effect?.details()]))});
  const modelAt=(x:number,y:number)=>{const rect=gl.domElement.getBoundingClientRect();point.set((x-rect.left)/rect.width*2-1,1-(y-rect.top)/rect.height*2);ray.setFromCamera(point,camera);const hit=ray.intersectObjects(all,true).find(h=>h.object instanceof T.Mesh&&h.object.material instanceof T.MeshStandardMaterial);if(!hit)return null;let o:T.Object3D|null=hit.object;while(o&&!SUBJECTS.some(n=>o===models[n]))o=o.parent;return SUBJECTS.find(n=>o===models[n])||null;};
  Object.assign(window,{heroInteraction:{hitPoint,snapshot,modelAt}});
  return()=>{Object.assign(window,{heroInteraction:undefined});};
 },[models,controllers,camera,gl,size]);
 useEffect(()=>{
  // Bake only direct visibility: r185 Lambert IBL otherwise fills shadow texels above alphaTest.
  const environment=renderScene.environment;const mirrors:T.Object3D[]=[];
  renderScene.traverse(o=>{if('isReflector' in o && o.visible){mirrors.push(o);o.visible=false;}});
  renderScene.environment=null;shadow.current?.reset();shadow.current?.update(48);
  renderScene.environment=environment;mirrors.forEach(o=>o.visible=true);invalidate();onReady();
  renderScene.updateMatrixWorld(true);
  const contact=Object.fromEntries([...Object.values(models),...['coffee-solid','books-solid'].map(n=>renderScene.getObjectByName(n)).filter((o):o is T.Object3D=>!!o)].map(o=>[o.name,{minY:new T.Box3().setFromObject(o,true).min.y,worldPosition:o.getWorldPosition(new T.Vector3()).toArray()}]));
  Object.assign(window,{heroEvidence:{models:Object.keys(models),shadowFrames:48,camera:{position:camera.position.toArray(),fov:(camera as T.PerspectiveCamera).fov},groundY:0,contact}});
  return()=>{
  const mats=new Set<T.Material>();for(const group of Object.values(models))group.traverse(o=>{if(o instanceof T.Mesh){const mm=Array.isArray(o.material)?o.material:[o.material];mm.forEach(m=>mats.add(m));if(o.customDepthMaterial)mats.add(o.customDepthMaterial);}});mats.forEach(m=>m.dispose());
  for(const name of ['orb'] as const){const geometries=new Set<T.BufferGeometry>();const textures=new Set<T.Texture>();models[name].traverse(o=>{if(o instanceof T.Mesh){geometries.add(o.geometry);for(const m of (Array.isArray(o.material)?o.material:[o.material]))for(const value of Object.values(m))if(value instanceof T.Texture)textures.add(value);}});geometries.forEach(g=>g.dispose());textures.forEach(tx=>tx.dispose());}
  models.city.traverse(o=>{if(o instanceof T.InstancedMesh)o.dispose();});
 };},[models,onReady,invalidate]);

 return <><StillLife dark={theme==='dark'}/><DeskObjects dark={theme==='dark'}/>{props.map((object,i)=><primitive key={'prop-'+i} object={object}/>)}{SUBJECTS.map(name=><primitive key={name} object={models[name]} onPointerOver={(e:{stopPropagation:()=>void})=>{e.stopPropagation();onHover(name);}} onPointerOut={()=>onHover(null)}/>)}<GroundShadows key={theme} theme={theme} shadowRef={shadow}/>{theme==='light'&&<><ContactShadows position={[0,.003,0]} opacity={.24} scale={32} blur={1.6} far={1.1} resolution={1024} frames={1} color="#655847"/><ContactShadows position={[0,.004,6]} opacity={.30} scale={[17,10]} blur={.75} far={.55} resolution={2048} frames={1} color="#76634b"/></>}</>;
}
function Rig({theme}:{theme:Theme}){
 const {gl,invalidate}=useThree();const dark=theme==='dark';
 useLayoutEffect(()=>{gl.toneMappingExposure=dark?1.10:1.08;invalidate();},[gl,dark,invalidate]);
 return <>

  <hemisphereLight args={[dark?'#9fb8d0':'#f3eee4',dark?'#273442':'#b8a98b',dark?.52:.32]}/>
  <directionalLight position={[4.9,8,-10.3]} color={dark?'#c9dce9':'#ffebc9'} intensity={dark?3.8:.6} castShadow shadow-mapSize={[4096,4096]} shadow-radius={4} shadow-camera-left={-18} shadow-camera-right={18} shadow-camera-top={16} shadow-camera-bottom={-16} shadow-camera-far={80} shadow-normalBias={.018} shadow-bias={-.00002}/>
  <directionalLight position={[-5,6,6]} color={dark?'#d2dbe3':'#eee8da'} intensity={dark?1.1:1.4}/>
  <Environment key={'calibrated-'+theme} frames={1} resolution={512} environmentIntensity={dark?1.05:.72}>
   <mesh><sphereGeometry args={[45,16,16]}/><meshBasicMaterial side={T.BackSide} color={dark?'#303e4b':'#887a68'}/></mesh>
   <Lightformer position={[5,8,-10]} rotation={[Math.PI/4,0,0]} scale={[7,9,1]} color={dark?'#b8d4ec':'#fff0d4'} intensity={5}/>
   <Lightformer position={[-6,5,4]} rotation={[0,Math.PI/2,0]} scale={[6,8,1]} color={dark?'#a6bfd6':'#eee9df'} intensity={1.5}/>
   {!dark&&<Lightformer position={[-7,7,-14]} rotation={[.4,.4,0]} scale={[4,7,1]} color="#fff2df" intensity={3}/> }
   <Lightformer position={[7,6,2]} rotation={[0,-Math.PI/2,0]} scale={[2,6,1]} color={dark?'#f2d3a1':'#fff6e7'} intensity={3}/>
  </Environment>
  {dark?<directionalLight position={[8,5,6]} color="#e2ba7d" intensity={1.15}/>:<WindowSun/>}
  <Suspense fallback={null}><LightDesk dark={dark}/></Suspense>
 </>;
}
function EnvironmentReady({onReady}:{onReady:()=>void}){useTexture('/home-hero/ivory-mineral-albedo.png');useEffect(()=>{onReady();},[onReady]);return null;}
function Scene(props:SceneProps){
 return <Canvas frameloop="demand" shadows dpr={1} camera={{position:[layout.camera[0],layout.camera[2],-layout.camera[1]],fov:2*Math.atan(36/(2*70*(1920/1080)))*180/Math.PI,near:.1,far:180}} gl={{alpha:true,antialias:true,powerPreference:'high-performance'}} onCreated={({gl,camera})=>{camera.lookAt(0,0,0);camera.updateMatrixWorld(true);gl.setClearColor(0,0);gl.outputColorSpace=T.SRGBColorSpace;gl.toneMapping=T.ACESFilmicToneMapping;}}>
  <Rig theme={props.theme}/><Suspense fallback={null}>{props.environmentOnly?<EnvironmentReady onReady={props.onReady}/>:<Assets {...props}/>}</Suspense>
 </Canvas>;
}

export default memo(Scene);


