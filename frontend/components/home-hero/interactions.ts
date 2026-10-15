import * as T from 'three';
import {createActivation} from './activation-effects';
import {createOrbNetwork} from './orb-network';

export type Subject='storage'|'city'|'wind'|'solar'|'orb'|'paper';
export const SUBJECTS:Subject[]=['storage','city','wind','solar','orb','paper'];
export type Interaction={update:(hover:number,dt:number,reduced:boolean)=>void;dispose:()=>void;details:()=>Record<string,number>};
export function makeInteraction(group:T.Group,name:Subject,dark:boolean):Interaction{
 const materials=new Set<T.MeshStandardMaterial>();
 group.traverse(o=>{if(o instanceof T.Mesh)for(const m of Array.isArray(o.material)?o.material:[o.material])if(m instanceof T.MeshStandardMaterial)materials.add(m);});
 const initial=new Map([...materials].map(m=>[m,{emission:m.emissiveIntensity,env:m.envMapIntensity}]));
 const uniforms={uTime:{value:0},uHover:{value:0}};
 const owned:T.Mesh[]=[];let routeCount=0;
 if(name==='city'){
  const roads:T.Mesh[]=[];group.traverse(o=>{if(o instanceof T.Mesh&&!Array.isArray(o.material)&&o.material.name.startsWith('15'))roads.push(o);});
  for(const road of roads){
   const pos=road.geometry.getAttribute('position'),uv=road.geometry.getAttribute('uv');if(!uv)continue;
   const stations=new Map<number,{p:T.Vector3;n:number}>();
   for(let i=0;i<pos.count;i++){const k=Math.round(uv.getX(i)*10000);const q=stations.get(k)||{p:new T.Vector3(),n:0};q.p.add(new T.Vector3().fromBufferAttribute(pos,i));q.n++;stations.set(k,q);}
   const center=[...stations].sort((a,b)=>a[0]-b[0]).map(([,q])=>q.p.divideScalar(q.n));
   function lane(points:T.Vector3[],offset:number,phase:number){
    const v:number[]=[],tex:number[]=[],idx:number[]=[];let length=0;
    for(let i=0;i<points.length;i++){if(i)length+=points[i].distanceTo(points[i-1]);const tangent=points[Math.min(i+1,points.length-1)].clone().sub(points[Math.max(0,i-1)]).normalize();const side=new T.Vector3(-tangent.z,0,tangent.x);const p=points[i].clone().addScaledVector(side,offset);p.y+=.011;v.push(...p.clone().addScaledVector(side,.036).toArray(),...p.clone().addScaledVector(side,-.036).toArray());tex.push(length,0,length,1);if(i){let a=(i-1)*2;idx.push(a,a+1,a+2,a+1,a+3,a+2);}}
    const geometry=new T.BufferGeometry();geometry.setAttribute('position',new T.Float32BufferAttribute(v,3));geometry.setAttribute('uv',new T.Float32BufferAttribute(tex,2));geometry.setIndex(idx);
    const material=new T.ShaderMaterial({uniforms:{...uniforms,uPhase:{value:phase},uHalo:{value:0}},transparent:true,depthWrite:false,side:T.DoubleSide,blending:T.AdditiveBlending,toneMapped:false,
     vertexShader:'varying vec2 flow;void main(){flow=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0);}',
     fragmentShader:`varying vec2 flow;uniform float uTime,uHover,uPhase,uHalo;void main(){
      float p=fract((flow.x-uTime*1.85+uPhase)/1.35);float head=exp(-pow((p-.67)/.11,2.));float tail=smoothstep(.03,.65,p)*(1.-smoothstep(.65,.86,p));
      float edge=pow(max(0.,1.-abs(flow.y-.5)*2.),mix(.8,2.,uHalo));vec3 c=mix(vec3(1.7,.91,.32),vec3(3.,2.6,1.8),head);
      gl_FragColor=vec4(c,edge*uHover*mix(.7+tail*1.2+head*1.8,.05+tail*.12+head*.28,uHalo));
      #include <colorspace_fragment>
     }`});
    const mesh=new T.Mesh(geometry,material);mesh.name='hero-hover-energy-'+routeCount++;mesh.raycast=()=>{};road.add(mesh);owned.push(mesh);
    const glowGeometry=geometry.clone(),gp=glowGeometry.getAttribute('position');
    for(let i=0;i<gp.count;i+=2){const a=new T.Vector3().fromBufferAttribute(gp,i),b=new T.Vector3().fromBufferAttribute(gp,i+1),mid=a.clone().add(b).multiplyScalar(.5);a.sub(mid).multiplyScalar(2.1).add(mid);b.sub(mid).multiplyScalar(2.1).add(mid);gp.setXYZ(i,a.x,a.y+.001,a.z);gp.setXYZ(i+1,b.x,b.y+.001,b.z);}
    const glowMaterial=material.clone();glowMaterial.uniforms={...material.uniforms,uHalo:{value:1}};
    const glow=new T.Mesh(glowGeometry,glowMaterial);glow.name='hero-road-local-glow';glow.raycast=()=>{};road.add(glow);owned.push(glow);
   }
   if(center.length>2)for(const [offset,phase] of [[0,0],[-.10,.6],[-.20,1.2]])lane(center,offset,phase);
   const H=.166;
   const branches=[ [[-1.18,H,.44],[-1.04,H,.81],[-.91,H,1.21],[-.98,H,1.65],[-1.10,H,2.02]], [[1.57,H,-.40],[1.23,H,-.05],[1.10,H,.48],[1.13,H,1.04],[1.27,H,1.48]], [[-.43,H,.04],[-.51,H,-.10],[-.54,H,-.28]], [[1.12,H,1.04],[.79,H,1.76],[.48,H,2.03],[.44,H,2.61],[.19,H,2.89]] ];
   branches.forEach((p,i)=>lane(new T.CatmullRomCurve3(p.map(v=>new T.Vector3(...v as [number,number,number]))).getSpacedPoints(40),0,i*.4));
  }
  for(const m of materials)if(m.name.startsWith('05')||m.name.startsWith('20')){
   m.onBeforeCompile=shader=>{
    Object.assign(shader.uniforms,uniforms);
    shader.vertexShader=shader.vertexShader.replace('#include <common>','#include <common>\nvarying vec3 windowPoint;varying vec3 windowNormal;').replace('#include <begin_vertex>','#include <begin_vertex>\nwindowPoint=position;windowNormal=normal;');
    shader.fragmentShader=shader.fragmentShader.replace('#include <common>','#include <common>\nvarying vec3 windowPoint;varying vec3 windowNormal;uniform float uHover;').replace('#include <emissivemap_fragment>',`#include <emissivemap_fragment>
    vec2 cell=vec2(windowPoint.x/.19,(windowPoint.y-.1)/.205);vec2 g=fract(cell);
    float occupied=step(.76,fract(sin(dot(floor(cell),vec2(12.9898,78.233)))*43758.5453));
    float pane=smoothstep(.14,.20,g.x)*(1.-smoothstep(.80,.86,g.x))*smoothstep(.24,.28,g.y)*(1.-smoothstep(.72,.76,g.y));
    totalEmissiveRadiance+=vec3(1.,.48,.17)*occupied*pane*step(.85,abs(normalize(windowNormal).z))*uHover*${dark?'1.6':'.8'};`);
   };m.customProgramCacheKey=()=> 'hero-city-window-'+dark;m.needsUpdate=true;
  }
 }
 const activation=createActivation(group,name,dark,uniforms);
 const core=group.getObjectByName('core-spin'),rings=[0,1,2].map(i=>group.getObjectByName('orbit-phase-'+i));
 const network=name==='orb'&&core?createOrbNetwork(core,dark,uniforms):undefined;
 const leaves:T.Mesh[]=[];if(name==='paper')group.traverse(o=>{if(o instanceof T.Mesh&&o.morphTargetInfluences?.length)leaves.push(o);});
 const sphere=core?.children.find(o=>o instanceof T.Mesh) as T.Mesh<T.BufferGeometry,T.MeshStandardMaterial>|undefined;
 const shell=sphere?.material,coreRoughness=shell?.roughness??.2,coreEnvironment=shell?.envMapIntensity??1;
 const ringRest=rings.map(r=>r?.quaternion.clone()),ringPositions=rings.map(r=>r?.position.clone());const coreRest=core?.rotation.clone();
 const bearingA=new T.Vector3(.84*Math.cos(4.22),.84*Math.sin(4.22),0),bearingB=new T.Vector3(.84*Math.cos(5.20),.84*Math.sin(5.20),0),bearingAxis=bearingB.clone().sub(bearingA).normalize();
 const tilt=new T.Quaternion(),offset=new T.Vector3();let tiltTime=0;
 let hover=0;
 return {update(h,dt,reduced){hover=h;const energy=dark&&['storage','orb','solar'].includes(name)?.045+h*.65:h;uniforms.uHover.value=energy;if(!reduced)uniforms.uTime.value+=dt;
  activation.update(energy,dt,reduced);
  network?.update(energy);
  for(const leaf of leaves){const root=leaf.parent?.name.startsWith('PaperLeaf_')?leaf.parent:leaf;const layer=Number(root.name.match(/PaperLeaf_(\d)/)?.[1]??0);const strength=T.MathUtils.smoothstep(h,.10+layer*.12,.70+layer*.12);leaf.morphTargetInfluences![0]=Math.min(1,(dark?0:.025+layer*.022)+strength*(reduced?.10:.86+.12*Math.sin(uniforms.uTime.value*1.65-layer*.65)));}
  for(const m of materials){const base=initial.get(m)!;
   if(name==='storage'){if(m.name.startsWith('08'))m.emissiveIntensity=base.emission+h*(dark?4:2.8);if(m.name.startsWith('05')){m.emissive.set('#6793a4');m.emissiveIntensity=h*(dark?.22:.14);}if(m.name.startsWith('03'))m.envMapIntensity=base.env+h*.45;}
   if(name==='city'&&m.name.startsWith('07'))m.emissiveIntensity=base.emission+h*(dark?2.0:1.2);
   if(name==='wind')m.envMapIntensity=base.env+h*.35;
   if(name==='orb'&&m.emissive.getHex()===0xd4e2ea)m.emissiveIntensity=.06+h*(dark?3.2:1.9);
   if(name==='paper'&&m.userData.pageHover){m.userData.pageHover.value=reduced?h*.18:h;m.userData.pageTime.value=uniforms.uTime.value;}
  }
  if(name==='orb'){if(shell){shell.roughness=coreRoughness-h*.045;shell.envMapIntensity=coreEnvironment+h*.45;if(shell.userData.earthCore)shell.emissiveIntensity=(dark?.13:.055)+h*(dark?.95:.82);}
   if(!reduced){tiltTime+=dt;if(core)core.rotation.y+=dt*(.018+h*.09);}
   rings.forEach((ring,i)=>{if(!ring)return;const strength=reduced?0:h;
    if(i<2){tilt.setFromAxisAngle(i===0?new T.Vector3(1,0,0):new T.Vector3(0,1,0),Math.sin(tiltTime*(i?.82:1.05)+i*.7)*strength*(i?.70:.80));ring.quaternion.copy(ringRest[i]!).multiply(tilt);}
    else{tilt.setFromAxisAngle(bearingAxis,Math.sin(tiltTime*.68)*strength*.24);ring.quaternion.copy(ringRest[i]!).multiply(tilt);offset.copy(bearingA).sub(bearingA.clone().applyQuaternion(tilt)).applyQuaternion(ringRest[i]!);ring.position.copy(ringPositions[i]!).add(offset);}
   });}
 },dispose(){activation.dispose();network?.dispose();leaves.forEach(p=>p.morphTargetInfluences![0]=0);if(core&&coreRest)core.rotation.copy(coreRest);rings.forEach((r,i)=>{if(r&&ringRest[i]){r.quaternion.copy(ringRest[i]!);r.position.copy(ringPositions[i]!);}});for(const mesh of owned){mesh.removeFromParent();mesh.geometry.dispose();(mesh.material as T.Material).dispose();}},details(){return{hover,flowRoutes:routeCount,attachedRoutes:owned.filter(m=>m.parent).length,time:uniforms.uTime.value,pageLift:leaves.length?Math.max(...leaves.map(p=>p.morphTargetInfluences![0])):0,blenderAsset:group.userData.blenderAsset?1:0,morphLeaves:leaves.length,networkSegments:network?.segments??0,movingRings:rings.filter(Boolean).length,earthEmission:shell?.userData.earthCore?shell.emissiveIntensity:0,ring0:rings[0]?.quaternion.x??0,ring1:rings[1]?.quaternion.y??0,ring2:rings[2]?.quaternion.x??0,...activation.details()};}};
}
