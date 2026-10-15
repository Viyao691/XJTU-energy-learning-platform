"use client";
import {useEffect,useMemo} from 'react';
import * as T from 'three';
import {RoundedBoxGeometry} from 'three/examples/jsm/geometries/RoundedBoxGeometry.js';

function coverTexture(title:string,color:string){
 const canvas=document.createElement('canvas');canvas.width=1024;canvas.height=768;const c=canvas.getContext('2d')!;
 c.fillStyle=color;c.fillRect(0,0,1024,768);c.strokeStyle='#ae976c';c.lineWidth=2;c.strokeRect(58,54,908,660);
 c.fillStyle='#c5ab79';c.textAlign='center';c.font='28px Georgia';c.fillText('ENERGY RESEARCH / MONOGRAPHS',512,125);
 c.fillStyle=color==='#b9a283'?'#594b38':'#c5ab79';c.font='62px Georgia';title.split('|').forEach((line,i)=>c.fillText(line,512,290+i*84));
 c.font='23px Georgia';c.fillText('MATERIALS · SYSTEMS · TRANSITION',512,623);
 const tx=new T.CanvasTexture(canvas);tx.colorSpace=T.SRGBColorSpace;tx.anisotropy=16;return tx;
}
function mesh(g:T.BufferGeometry,m:T.Material,parent:T.Group,position:[number,number,number]){
 const o=new T.Mesh(g,m);o.position.set(...position);o.castShadow=o.receiveShadow=true;parent.add(o);return o;
}
function ceramicCup(dark:boolean){
 const root=new T.Group();root.name='coffee-solid';
 const ceramic=new T.MeshPhysicalMaterial({color:dark?'#afbbc4':'#e2d2b8',roughness:.25,metalness:0,clearcoat:.48,clearcoatRoughness:.18});
 // One closed lathed wall: foot, external taper, rounded lip, interior and inner floor.
 const profile=[[.0,.035],[.34,.035],[.39,.045],[.42,.075],[.435,.15],[.475,.93],[.50,1.03],[.501,1.065],[.49,1.08],[.469,1.077],[.455,1.058],[.451,1.02],[.423,.23],[.39,.18],[.0,.18]];
 mesh(new T.LatheGeometry(profile.map(p=>new T.Vector2(...p as [number,number])),96),ceramic,root,[0,.035,0]);
 const handle=mesh(new T.TorusGeometry(.30,.070,16,64),ceramic,root,[.57,.62,0]);handle.scale.set(.86,1.24,1);
 const liquid=new T.MeshPhysicalMaterial({color:'#28150b',roughness:.13,metalness:0,clearcoat:1,clearcoatRoughness:.10,envMapIntensity:1.1});
 mesh(new T.CylinderGeometry(.442,.442,.012,96),liquid,root,[0,1.015,0]);
 mesh(new T.LatheGeometry([new T.Vector2(.416,1.018),new T.Vector2(.437,1.021),new T.Vector2(.444,1.034)],96),liquid,root,[0,0,0]);
 const crema=new T.MeshStandardMaterial({color:'#9a6739',roughness:.45});
 for(let i=0;i<24;i++){const angle=i*2.39996,r=.36+.065*Math.sin(i*1.7);mesh(new T.SphereGeometry(.008+(i%3)*.003,8,4),crema,root,[Math.cos(angle)*r,1.024,Math.sin(angle)*r]).scale.y=.15;}
 mesh(new T.CylinderGeometry(.63,.635,.05,64),new T.MeshStandardMaterial({color:'#9d8055',roughness:.93}),root,[0,.025,0]);
 root.rotation.y=-.25;root.scale.setScalar(1.35);root.position.set(-4.118,0,7.985);return root;
}
function bookStack(dark:boolean){
 const root=new T.Group();root.name='books-solid';const paper=new T.MeshStandardMaterial({color:dark?'#a8b3bd':'#e3dac7',roughness:.91});
 const specs=[{w:2.85,d:1.85,h:.27,angle:.045,color:'#293c40',title:'Energy Storage|Systems'},{w:2.73,d:1.79,h:.23,angle:-.03,color:'#6d756b',title:'Sustainable|Energy'},{w:2.83,d:1.82,h:.20,angle:.07,color:dark?'#334c60':'#b9a283',title:'Materials|and Energy'}];
 let y=0;
 specs.forEach((s,index)=>{const book=new T.Group();book.position.set(index===1?.07:0,y,0);book.rotation.y=s.angle;root.add(book);
  const cloth=new T.MeshStandardMaterial({color:s.color,roughness:.78});const cover=new RoundedBoxGeometry(s.w,.045,s.d,2,.018);
  mesh(cover,cloth,book,[0,.0225,0]);mesh(cover,cloth,book,[0,s.h-.0225,0]);
  // Compressed signatures are actual thin volumes, separated by hairline recesses.
  const sheet=new RoundedBoxGeometry(s.w-.07,(s.h-.09)/15-.0015,s.d-.055,1,.004);
  const signatures=new T.InstancedMesh(sheet,paper,15),m=new T.Matrix4();
  for(let i=0;i<15;i++){m.makeTranslation(.018,.045+(i+.5)*(s.h-.09)/15,.006*Math.sin(i*.5));signatures.setMatrixAt(i,m);}
  signatures.castShadow=signatures.receiveShadow=true;book.add(signatures);
  mesh(new RoundedBoxGeometry(.075,s.h-.03,s.d,2,.027),cloth,book,[-s.w/2+.036,s.h/2,0]);
  if(index===2){const ink=new T.MeshStandardMaterial({map:coverTexture(s.title,s.color),roughness:.8});const front=mesh(new T.PlaneGeometry(s.w-.07,s.d-.05),ink,book,[0,s.h+.0005,0]);front.rotation.x=-Math.PI/2;}
  const label=document.createElement('canvas');label.width=1024;label.height=96;const ctx=label.getContext('2d')!;ctx.fillStyle=s.color;ctx.fillRect(0,0,1024,96);ctx.fillStyle=index===2?'#594b38':'#c5ab79';ctx.textAlign='center';ctx.font='39px Georgia';ctx.fillText(s.title.replace('|',' '),512,62);const labelMap=new T.CanvasTexture(label);labelMap.colorSpace=T.SRGBColorSpace;labelMap.anisotropy=16;
  mesh(new T.PlaneGeometry(s.w-.13,s.h-.075),new T.MeshStandardMaterial({map:labelMap,roughness:.8}),book,[0,s.h/2,s.d/2+.001]);
  y+=s.h+.004;
 });
 root.position.set(-2.222,0,9.78);root.rotation.y=.03;return root;
}
export function DeskObjects({dark=false}:{dark?:boolean}){
 const root=useMemo(()=>{const group=new T.Group();group.name='desk-solid-accessories';group.add(ceramicCup(dark),bookStack(dark));return group;},[dark]);
 useEffect(()=>()=>{const geometries=new Set<T.BufferGeometry>(),materials=new Set<T.Material>();root.traverse(o=>{if(o instanceof T.Mesh){geometries.add(o.geometry);(Array.isArray(o.material)?o.material:[o.material]).forEach(m=>materials.add(m));if(o instanceof T.InstancedMesh)o.dispose();}});geometries.forEach(g=>g.dispose());materials.forEach(m=>{if(m instanceof T.MeshStandardMaterial)m.map?.dispose();m.dispose();});},[root]);
 return <primitive object={root}/>;
}
