import * as T from 'three';
// Frozen from orb-reference-silver; no hover behavior in this integration.
export function createOrb(dark) {
const s = new T.Group();
function material(color,metal,rough,emit=0){return new T.MeshStandardMaterial({color,metalness:metal,roughness:rough,emissive:color,emissiveIntensity:emit})}
const shell=material(dark?'#2e455f':'#aab7c1',dark?.78:.94,dark?.43:.42),silver=material(dark?'#819aae':'#bac3c7',.96,dark?.34:.37),gold=material('#aa9875',.92,.43),baseMat=material(dark?'#233346':'#9a9e9c',.88,.40),black=material('#18232d',.3,.56),light=material(dark?'#a2cef7':'#d9bf8c',.3,.3,dark?.28:.10);
// Seeded low-amplitude surface variation, no colour dirt or decorative geometry.
function finishMap(){const size=256,data=new Uint8Array(size*size*4);let seed=173;for(let y=0;y<size;y++)for(let x=0;x<size;x++){seed=(1664525*seed+1013904223)>>>0;const v=224+Math.floor((seed/4294967296)*12)+Math.round(3*Math.sin(y*.65));const k=(y*size+x)*4;data[k]=data[k+1]=data[k+2]=v;data[k+3]=255}let t=new T.DataTexture(data,size,size);t.wrapS=t.wrapT=T.RepeatWrapping;t.repeat.set(5,3);t.needsUpdate=true;return t}
const micro=finishMap();shell.roughnessMap=micro;shell.bumpMap=micro;shell.bumpScale=.0005;silver.roughnessMap=micro;gold.roughnessMap=micro;baseMat.roughnessMap=micro;
// User correction: smooth sphere and silver metal across the whole instrument.
shell.color.set('#424642');shell.metalness=1;shell.roughness=dark?.19:.17;shell.bumpMap=null;shell.roughnessMap=null;shell.envMapIntensity=dark?1.4:1;
silver.color.set('#b9b8ad');silver.metalness=.96;silver.roughness=.28;
gold.color.set('#b9b8ad');gold.metalness=.96;gold.roughness=.32;
baseMat.color.set('#a5a599');baseMat.metalness=.92;baseMat.roughness=.36;
light.color.set('#d4e2ea');light.emissive.set('#d4e2ea');light.emissiveIntensity=.06;
black.color.set('#626e78');black.metalness=.8;
const baseSide=baseMat.clone();baseSide.color.set('#898f88');baseSide.metalness=.95;baseSide.roughness=.27;
function add(g,m,p=[0,0,0],parent=s){let o=new T.Mesh(g,m);o.position.set(...p);o.castShadow=true;o.receiveShadow=true;parent.add(o);return o}
function rounded(w,h,d,rad){let sh=new T.Shape(),x=-w/2,y=-d/2;sh.moveTo(x+rad,y);sh.lineTo(x+w-rad,y);sh.quadraticCurveTo(x+w,y,x+w,y+rad);sh.lineTo(x+w,y+d-rad);sh.quadraticCurveTo(x+w,y+d,x+w-rad,y+d);sh.lineTo(x+rad,y+d);sh.quadraticCurveTo(x,y+d,x,y+d-rad);sh.lineTo(x,y+rad);sh.quadraticCurveTo(x,y,x+rad,y);let g=new T.ExtrudeGeometry(sh,{depth:h-.014,bevelEnabled:true,bevelThickness:.007,bevelSize:.007,bevelSegments:3,steps:1,curveSegments:8});g.rotateX(-Math.PI/2);g.translate(0,.007,0);return g}
add(rounded(1.35,.045,.92,.12),[baseMat,baseSide],[0,.016,0]);add(rounded(1.27,.016,.84,.10),black,[0,.004,0]);add(new T.BoxGeometry(.16,.004,.005),light,[.38,.038,.466]);
add(new T.CylinderGeometry(.055,.065,.025,32),baseMat,[0,.073,.34]);
// A tapered rear instrument column carries the core spindle and fixed outer bearing.
add(new T.CylinderGeometry(.024,.038,.86,32),silver,[0,.49,.34]);
let spindle=add(new T.CylinderGeometry(.020,.020,.36,24),silver,[0,.90,.17]);spindle.rotation.x=Math.PI/2;
const core=new T.Group();core.name='core-spin';core.position.set(0,1.12,0);s.add(core);add(new T.SphereGeometry(.49,64,40),shell,[0,0,0],core);
const configs=[[.68,[.65,.12,.30],gold],[.76,[-.55,.52,-.28],silver],[.84,[.08,-.35,.06],silver]];
for(let i=0;i<3;i++){let [rad,rot,mat]=configs[i];let pivot=new T.Group();pivot.name='orbit-phase-'+i;pivot.position.set(0,1.12,0);pivot.rotation.set(...rot);s.add(pivot);add(new T.TorusGeometry(rad,i===2?.010:(i===0?.0045:.0038),8,128),mat,[0,0,0],pivot);if(i<2){let a=i*2.2+.7;add(new T.SphereGeometry(.013,16,10),light,[Math.cos(a)*rad,Math.sin(a)*rad,0],pivot)} }
// Grounded outer support: two straight precision struts meet the outer ring lower quadrants.
function rod(a,b){a=new T.Vector3(...a);b=new T.Vector3(...b);let o=add(new T.CylinderGeometry(.010,.014,a.distanceTo(b),20),silver,a.clone().add(b).multiplyScalar(.5).toArray());o.quaternion.setFromUnitVectors(new T.Vector3(0,1,0),b.sub(a).normalize())}
for(const side of [-1,1]){const angle=side<0?4.22:5.20;const end=new T.Vector3(.84*Math.cos(angle),.84*Math.sin(angle),0).applyEuler(new T.Euler(.08,-.35,.06)).add(new T.Vector3(0,1.12,0));const mount=[side*.40,.070,.28];add(new T.CylinderGeometry(.027,.033,.012,24),baseMat,[mount[0],.067,mount[2]]);rod(mount,end.toArray());add(new T.SphereGeometry(.020,16,10),silver,end.toArray())}

return s;
}
