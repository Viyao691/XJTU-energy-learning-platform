"use client";
import {useEffect,useMemo} from 'react';
import {useThree} from '@react-three/fiber';
import {useTexture} from '@react-three/drei';
import * as T from 'three';
import {Reflector} from 'three/examples/jsm/objects/Reflector.js';

// A small, deterministic material tile, not a photograph with baked lighting.
function limestone(){
 const n=512,base=new Uint8Array(n*n*4),rough=new Uint8Array(n*n*4),height=new Uint8Array(n*n*4);
 const hash=(x:number,y:number)=>{const v=Math.sin(x*127.1+y*311.7)*43758.5453;return v-Math.floor(v);};
 const noise=(x:number,y:number)=>{const ix=Math.floor(x),iy=Math.floor(y);let a=x-ix,b=y-iy;a=a*a*(3-2*a);b=b*b*(3-2*b);return T.MathUtils.lerp(T.MathUtils.lerp(hash(ix,iy),hash(ix+1,iy),a),T.MathUtils.lerp(hash(ix,iy+1),hash(ix+1,iy+1),a),b);};
 for(let y=0;y<n;y++)for(let x=0;x<n;x++){
  const i=(y*n+x)*4,cloud=noise(x/70,y/90)*.55+noise(x/21,y/27)*.3+noise(x/7,y/9)*.15;
  const grain=hash(x,y)-.5,fleck=grain>.475?-.8:0,v=(cloud-.5)*8+grain*.7+fleck*.2;
  base.set([239+v,234+v,222+v,255],i);const r=177+(cloud-.5)*12+grain*2;rough.set([r,r,r,255],i);
  const h=126+(cloud-.5)*8+grain*2;height.set([h,h,h,255],i);
 }
 const texture=(data:Uint8Array,color=false)=>{const tx=new T.DataTexture(data,n,n);tx.wrapS=tx.wrapT=T.RepeatWrapping;tx.minFilter=T.LinearMipmapLinearFilter;tx.magFilter=T.LinearFilter;tx.generateMipmaps=true;tx.anisotropy=8;tx.repeat.set(3.5,3.5);if(color)tx.colorSpace=T.SRGBColorSpace;tx.needsUpdate=true;return tx;};
 return {map:texture(base,true),roughnessMap:texture(rough),bumpMap:texture(height)};
}

export function LightDesk({dark=false}:{dark?:boolean}){
 const {camera}=useThree(),albedo=useTexture('/home-hero/ivory-mineral-albedo.png');
 const resources=useMemo(()=>{
  const ray=new T.Raycaster(),v:number[]=[],uv:number[]=[],index:number[]=[];
  const xs=[0,1040,1645,1920],ys=[533,438,392,463];
  for(let j=0;j<2;j++)for(let i=0;i<4;i++){
   ray.setFromCamera(new T.Vector2(xs[i]/960-1,1-(j?1450:ys[i])/540),camera);
   const p=new T.Vector3();ray.ray.intersectPlane(new T.Plane(new T.Vector3(0,1,0),0),p);
   v.push(p.x,-.009,p.z);uv.push(.5+p.x/26,.5+p.z/26);
  }
  for(let i=0;i<3;i++)index.push(i,i+4,i+1,i+1,i+4,i+5);
  const geometry=new T.BufferGeometry();geometry.setAttribute('position',new T.Float32BufferAttribute(v,3));geometry.setAttribute('uv',new T.Float32BufferAttribute(uv,2));geometry.setIndex(index);geometry.computeVertexNormals();
  const textures:{map:T.Texture;roughnessMap:T.Texture;bumpMap:T.Texture}=limestone();textures.map.dispose();textures.map=albedo.clone();textures.map.colorSpace=T.SRGBColorSpace;textures.map.wrapS=textures.map.wrapT=T.ClampToEdgeWrapping;textures.map.repeat.set(1,1);textures.map.anisotropy=16;textures.map.needsUpdate=true;
  const material=new T.MeshPhysicalMaterial({...textures,color:dark?'#3e4855':'#f6f0e7',roughness:dark?.64:.78,metalness:dark?.18:0,bumpScale:.0012,clearcoat:.12,clearcoatRoughness:.48,envMapIntensity:dark?1.15:.8,side:T.DoubleSide});
  const mirrorGeometry=geometry.clone();mirrorGeometry.translate(0,.0095,0);
  const reflector=new Reflector(mirrorGeometry,{textureWidth:1536,textureHeight:1024,multisample:0,clipBias:0});
  // Reflector assumes a local +Z plane; geometry itself lies in XZ.
  mirrorGeometry.rotateX(Math.PI/2);reflector.rotation.x=-Math.PI/2;
  const rm=reflector.material as T.ShaderMaterial;rm.transparent=true;rm.depthWrite=false;
  rm.fragmentShader=`uniform sampler2D tDiffuse;varying vec4 vUv;
   void main(){vec2 p=vUv.xy/vUv.w;vec4 c=vec4(0.);float sum=0.;
   for(int x=-3;x<=3;x++)for(int y=-3;y<=3;y++){float w=exp(-float(x*x+y*y)*.22);c+=texture2D(tDiffuse,p+vec2(float(x),float(y))*.0023)*w;sum+=w;}
   vec4 sampleColor=c/sum;gl_FragColor=vec4(sampleColor.rgb,${dark?'.16':'.085'}*sampleColor.a);
   #include <tonemapping_fragment>
   #include <colorspace_fragment>
   }`;
  reflector.renderOrder=1;
  return {geometry,material,reflector,textures};
 },[camera,albedo,dark]);
 useEffect(()=>()=>{resources.geometry.dispose();resources.material.dispose();resources.reflector.geometry.dispose();resources.reflector.dispose();Object.values(resources.textures).forEach(t=>t.dispose());},[resources]);
 return <><mesh position={[7,7,-10]} rotation={[Math.PI/2,0,0]}>
   <planeGeometry args={[7,10]}/><meshBasicMaterial color={dark?'#b4d3ee':'#fff3db'} side={T.DoubleSide}/>
  </mesh><mesh receiveShadow geometry={resources.geometry} material={resources.material}/><primitive object={resources.reflector}/></>;
}


// A projected window illuminates the desk and every physical asset together.
export function WindowSun(){
 const resources=useMemo(()=>{
  const n=256,data=new Uint8Array(n*n*4);
  for(let y=0;y<n;y++)for(let x=0;x<n;x++){
   const u=x/(n-1),v=y/(n-1);
   const pane=Math.max(...[.21,.43,.65].map(c=>Math.exp(-Math.pow(Math.abs((u-c)/.092),8))));
   const edge=T.MathUtils.smoothstep(v,.02,.10)*(1-T.MathUtils.smoothstep(v,.88,.98));
   const light=Math.round(255*(.06+.94*pane*edge));data.set([light,light,light,255],(y*n+x)*4);
  }
  const map=new T.DataTexture(data,n,n);map.minFilter=map.magFilter=T.LinearFilter;map.needsUpdate=true;
  const target=new T.Object3D();target.position.set(0,0,3);
  return {map,target};
 },[]);
 useEffect(()=>()=>resources.map.dispose(),[resources]);
 return <><primitive object={resources.target}/><spotLight position={[4.9,8,-10.3]} target={resources.target} color="#ffe5ba" intensity={7.5} decay={0} angle={.83} penumbra={.6} map={resources.map} castShadow shadow-mapSize={[4096,4096]} shadow-normalBias={.012} shadow-bias={-.000015} shadow-radius={6} shadow-intensity={.72}/></>;
}

