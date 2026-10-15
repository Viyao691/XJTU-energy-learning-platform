import * as T from 'three';
import type {Interaction} from './interactions';

export function campusInteraction(group:T.Group,dark:boolean):Interaction{
 const time={value:0},hover={value:0},owned:T.Mesh[]=[],mats=new Set<T.MeshStandardMaterial>();
 group.traverse(o=>{if(o instanceof T.Mesh)for(const m of Array.isArray(o.material)?o.material:[o.material])if(m instanceof T.MeshStandardMaterial)mats.add(m);});
 const windows=[...mats].filter(m=>/^(07)|occupied|interior pane/.test(m.name));
 const original=windows.map(m=>({m,color:m.emissive.clone(),strength:m.emissiveIntensity}));
 for(const m of mats)if(m.name.startsWith('05')){
  m.onBeforeCompile=shader=>{
   shader.uniforms.campusHover=hover;
   shader.vertexShader=shader.vertexShader.replace('#include <common>','#include <common>\nvarying vec3 facadePoint,facadeNormal;').replace('#include <begin_vertex>','#include <begin_vertex>\nfacadePoint=position;facadeNormal=normal;');
   shader.fragmentShader=shader.fragmentShader.replace('#include <common>','#include <common>\nvarying vec3 facadePoint,facadeNormal;uniform float campusHover;').replace('#include <emissivemap_fragment>',`#include <emissivemap_fragment>
   vec2 cell=vec2((abs(facadeNormal.z)>.6?facadePoint.x:facadePoint.z)/.14,facadePoint.y/.225);vec2 g=fract(cell);
   float occupied=step(.58,fract(sin(dot(floor(cell),vec2(12.9898,78.233)))*43758.5453));
   float pane=smoothstep(.15,.22,g.x)*(1.-smoothstep(.78,.85,g.x))*smoothstep(.17,.23,g.y)*(1.-smoothstep(.77,.83,g.y));
   totalEmissiveRadiance+=vec3(1.,.53,.22)*pane*occupied*step(.65,max(abs(facadeNormal.x),abs(facadeNormal.z)))*${dark?'(.15+campusHover*.85)':'campusHover'}*${dark?'2.0':'2.3'};`);
  };m.customProgramCacheKey=()=> 'calibrated-campus-windows-'+dark;m.needsUpdate=true;
 }
 const lines:T.Vector3[][]=[];
 for(const z of [1.48,-.15,-1.76])lines.push([new T.Vector3(-4.5,.19,z),new T.Vector3(4.5,.19,z)]);
 for(const x of [-3.42,.95,3.65])lines.push([new T.Vector3(x,.19,-2.65),new T.Vector3(x,.19,2.65)]);
 for(let i=0;i<lines.length;i++){
  const curve=new T.CatmullRomCurve3(lines[i]);
  for(const halo of [false,true]){
   const material=new T.ShaderMaterial({uniforms:{time,hover,phase:{value:i*.23},halo:{value:halo?1:0}},transparent:true,depthWrite:false,blending:T.AdditiveBlending,toneMapped:false,
    vertexShader:'varying vec2 flow;void main(){flow=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',
    fragmentShader:`varying vec2 flow;uniform float time,hover,phase,halo;void main(){float p=fract(flow.x*5.-time*.85+phase);float head=exp(-pow((p-.77)/.08,2.));float tail=smoothstep(.10,.72,p)*(1.-smoothstep(.72,.88,p));vec3 color=mix(vec3(1.7,.91,.30),vec3(2.5,2.2,1.55),head);gl_FragColor=vec4(color,hover*(.24+tail*.8+head)*mix(.9,.15,halo));
    #include <colorspace_fragment>
    }`});
   const mesh=new T.Mesh(new T.TubeGeometry(curve,48,halo?.055:.014,6,false),material);mesh.raycast=()=>{};group.add(mesh);owned.push(mesh);
  }
 }
 return {update(h,dt,reduced){hover.value=dark?.035+h*.965:h;if(!reduced)time.value+=dt;for(const mesh of owned)mesh.visible=dark||h>.005;for(const {m,strength} of original){m.emissive.set('#ffbc67');m.emissiveIntensity=strength+h*(dark?2.8:3.3);}},details:()=>({hover:hover.value,time:time.value,flowRoutes:lines.length,windowMaterials:windows.length,windowEmission:Math.max(0,...windows.map(m=>m.emissiveIntensity))}),dispose(){for(const o of owned){o.removeFromParent();o.geometry.dispose();(o.material as T.Material).dispose();}for(const {m,color,strength} of original){m.emissive.copy(color);m.emissiveIntensity=strength;}}};
}
