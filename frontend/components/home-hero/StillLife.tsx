"use client";
import {useEffect,useMemo} from 'react';
import {useThree} from '@react-three/fiber';
import {useTexture} from '@react-three/drei';
import * as T from 'three';

// Photographic accessories only. Core assets and their hover stay fully 3D.
const items=[{name:'plant',crop:[1040,75,1528,960],screen:[1820,157,198,359],foot:[1939,513],kind:'pot'}];
export function StillLife({dark=false}:{dark?:boolean}){
 const {camera}=useThree(),atlas=useTexture('/home-hero/still-life-atlas.png');
 const group=useMemo(()=>{
  const root=new T.Group();root.name='photographic-still-life';
  const ray=new T.Raycaster(),floor=new T.Plane(new T.Vector3(0,1,0),0),forward=new T.Vector3();camera.getWorldDirection(forward);
  for(const item of items){
   const [left,top,w,h]=item.screen,[sx,sy]=item.foot;
   ray.setFromCamera(new T.Vector2(sx/960-1,1-sy/540),camera);const contact=new T.Vector3();ray.ray.intersectPlane(floor,contact);
   const plane=new T.Plane().setFromNormalAndCoplanarPoint(forward,contact),vertices:number[]=[];
   for(const [x,y] of [[left,top+h],[left+w,top+h],[left,top],[left+w,top]]){
    ray.setFromCamera(new T.Vector2(x/960-1,1-y/540),camera);const p=new T.Vector3();ray.ray.intersectPlane(plane,p);vertices.push(...p.toArray());
   }
   const [x0,y0,x1,y1]=item.crop,geometry=new T.BufferGeometry();geometry.setAttribute('position',new T.Float32BufferAttribute(vertices,3));
   geometry.setAttribute('uv',new T.Float32BufferAttribute([x0/1536,1-y1/1024,x1/1536,1-y1/1024,x0/1536,1-y0/1024,x1/1536,1-y0/1024],2));geometry.setIndex([0,1,2,2,1,3]);geometry.computeVertexNormals();
   const texture=atlas.clone();texture.colorSpace=T.SRGBColorSpace;texture.anisotropy=8;texture.needsUpdate=true;
   const card=new T.Mesh(geometry,new T.MeshBasicMaterial({map:texture,color:dark?'#738ba2':'#ffffff',transparent:true,alphaTest:.045,depthWrite:false,side:T.DoubleSide,toneMapped:false}));card.renderOrder=2;card.name=item.name+'-photo-card';card.raycast=()=>{};root.add(card);
   // Invisible simple volumes provide shared window-light contact/cast shadows.
   const shape=item.kind==='books'?new T.BoxGeometry(2.7,.45,1.6):new T.CylinderGeometry(item.kind==='pot'?.45:.48,item.kind==='pot'?.38:.46,item.kind==='pot'?.8:.9,24);
   const proxy=new T.Mesh(shape,new T.MeshStandardMaterial({colorWrite:false,depthWrite:false}));proxy.position.copy(contact);proxy.position.y=item.kind==='books'?.225:item.kind==='pot'?.4:.45;proxy.castShadow=true;proxy.raycast=()=>{};proxy.name=item.name+'-shadow-volume';root.add(proxy);
  }
  return root;
 },[atlas,camera,dark]);
 useEffect(()=>()=>group.traverse(o=>{if(o instanceof T.Mesh){o.geometry.dispose();const m=o.material as T.MeshStandardMaterial;m.map?.dispose();m.dispose();}}),[group]);
 return <primitive object={group}/>;
}
