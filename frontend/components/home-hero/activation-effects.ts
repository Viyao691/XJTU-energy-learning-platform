import * as T from 'three';

// Local depth-tested energy paths. Storage's full primary frame is explicitly activated.
export function createActivation(group:T.Group,name:string,dark:boolean,uniforms:{uTime:{value:number};uHover:{value:number}}){
 const owned:T.Mesh[]=[],space=group.children[0],nodes:{mesh:T.Mesh;radius:number;phase:number}[]=[],indicators:T.MeshStandardMaterial[]=[];let outerEdges=0;
 const warm=new T.Color('#ffd78c'),cool=new T.Color(dark?'#c2eaff':'#a2d4eb');
 const currentRoutes:{start:T.Vector3;end:T.Vector3;phase:number}[]=[];let currentHeads:T.InstancedMesh|undefined;
 function pulse(parent:T.Object3D,points:T.Vector3[],radius:number,color:T.Color,phase=0){
  const curve=new T.CatmullRomCurve3(points,false,'centripetal');
  const mat=new T.ShaderMaterial({uniforms:{...uniforms,tint:{value:color},phase:{value:phase},uHalo:{value:0}},transparent:true,depthWrite:false,toneMapped:false,
   vertexShader:'varying vec2 vFlow;varying vec3 vNormal,vEye;void main(){vFlow=uv;vec4 p=modelViewMatrix*vec4(position,1.);vNormal=normalize(normalMatrix*normal);vEye=-p.xyz;gl_Position=projectionMatrix*p;}',
   fragmentShader:`varying vec2 vFlow;varying vec3 vNormal,vEye;uniform float uTime,uHover,phase,uHalo;uniform vec3 tint;
    void main(){float p=fract(vFlow.x*3.2-uTime*.78+phase);float head=exp(-pow((p-.72)/.10,2.));float tail=smoothstep(.05,.68,p)*(1.-smoothstep(.68,.86,p));
    float soft=pow(abs(dot(normalize(vNormal),normalize(vEye))),1.8);vec3 c=mix(tint*1.7,vec3(3.,2.75,2.1),head);
    float alpha=mix(.72+.35*tail+.7*head,soft*(.16+.35*tail+.75*head),uHalo);gl_FragColor=vec4(c,uHover*alpha);
    #include <colorspace_fragment>
    }`});
  const mesh=new T.Mesh(new T.TubeGeometry(curve,Math.max(32,points.length*2),radius,6,false),mat);mesh.name=name+'-activation-detail';mesh.raycast=()=>{};parent.add(mesh);owned.push(mesh);
  const halo=mat.clone();halo.uniforms={...mat.uniforms,uHalo:{value:1}};halo.blending=T.AdditiveBlending;
  const glow=new T.Mesh(new T.TubeGeometry(curve,Math.max(32,points.length*2),radius*2.8,8,false),halo);glow.raycast=()=>{};mesh.add(glow);owned.push(glow);
  return mesh;
 }
 const arc=(radius:number,start:number,end:number)=>Array.from({length:65},(_,i)=>{const a=T.MathUtils.lerp(start,end,i/64);return new T.Vector3(Math.cos(a)*radius,Math.sin(a)*radius,0);});
 if(name==='storage'){
  const X=2.407,Z=.938,bottom=.15,top=2.073;
  const rail=(a:number[],b:number[],phase:number)=>{const start=new T.Vector3(...a as [number,number,number]),end=new T.Vector3(...b as [number,number,number]);pulse(space,[start,end],dark?.020:.016,warm,phase);currentRoutes.push({start,end,phase});outerEdges++;};
  for(const y of [bottom,top]){
   for(const z of [-Z,Z])rail([-X,y,z],[X,y,z],z+y);
   for(const x of [-X,X])rail([x,y,-Z],[x,y,Z],x+y);
  }
  for(const x of [-X,X])for(const z of [-Z,Z])rail([x,bottom,z],[x,top,z],x-z);
  for(const x of [-.82,.23,1.3])pulse(space,[new T.Vector3(x,.34,Z-.035),new T.Vector3(x,1.92,Z-.035)],.006,cool,x);
  // Tapered, shallow die-cast badge: the bevel catches light instead of a flat yellow sticker.
  const bolt=new T.Shape();[[.055,.30],[-.105,-.012],[-.017,-.003],[-.070,-.285],[.117,.055],[.023,.036]].forEach(([x,y],i)=>{i?bolt.lineTo(x,y):bolt.moveTo(x,y);});bolt.closePath();
  const mat=new T.MeshPhysicalMaterial({color:'#c3ac77',metalness:.92,roughness:.28,clearcoat:.12,clearcoatRoughness:.3,emissive:'#f6d791',emissiveIntensity:.015});
  const badge=new T.ExtrudeGeometry(bolt,{depth:.007,bevelEnabled:true,bevelThickness:.003,bevelSize:.003,bevelSegments:3,steps:1,curveSegments:8});
  const mark=new T.Mesh(badge,mat);mark.position.set(.71,1.39,.899);mark.userData.idleVisible=true;mark.raycast=()=>{};space.add(mark);owned.push(mark);indicators.push(mat);
  currentHeads=new T.InstancedMesh(new T.SphereGeometry(.029,10,6),new T.MeshBasicMaterial({color:'#fff4d1',toneMapped:false,transparent:true}),currentRoutes.length);currentHeads.name='storage-traveling-current-heads';currentHeads.raycast=()=>{};currentHeads.frustumCulled=false;space.add(currentHeads);owned.push(currentHeads);
 }
 const rotor=group.getObjectByName('WindRotor');const rotorRest=rotor?.quaternion.clone();let rotorAngle=0;
 if(name==='wind'){
  const ring=pulse(space,arc(.34,0,Math.PI*2),.022,cool);ring.rotation.x=-Math.PI/2;ring.position.y=.019;
 }
 if(name==='solar'){
  // The glass node carries the existing panel tilt; local XZ is its front surface.
  let glass:T.Mesh|undefined;group.traverse(o=>{if(o instanceof T.Mesh&&!Array.isArray(o.material)&&o.material.name==='Solar clear cover')glass=o;});
  if(glass){
   glass.geometry.computeBoundingBox();const box=glass.geometry.boundingBox!,w=box.max.x-box.min.x,d=box.max.z-box.min.z;
   const mat=new T.ShaderMaterial({uniforms:{...uniforms,tint:{value:cool}},transparent:true,depthWrite:false,side:T.DoubleSide,toneMapped:false,
    vertexShader:'varying vec2 panel;void main(){panel=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0);}',
    fragmentShader:'varying vec2 panel;uniform float uTime,uHover;uniform vec3 tint;void main(){float x=panel.x+.10*panel.y;float sweep=fract(uTime*.20)*1.4-.15;float beam=exp(-pow((x-sweep)/.075,2.));vec2 cell=abs(fract(panel*vec2(12.,6.))-.5);float grid=max(smoothstep(.465,.5,cell.x),smoothstep(.47,.5,cell.y));float wave=.5+.5*sin(panel.x*30.-uTime*4.);float edge=smoothstep(0.,.012,panel.x)*smoothstep(0.,.012,1.-panel.x)*smoothstep(0.,.012,panel.y)*smoothstep(0.,.012,1.-panel.y);gl_FragColor=vec4(mix(tint*1.8,vec3(2.,1.95,1.8),beam),(beam*.95+grid*(.24+.65*wave))*uHover*edge);}'});
   const mesh=new T.Mesh(new T.PlaneGeometry(w,d),mat);mesh.rotation.x=-Math.PI/2;mesh.position.set((box.max.x+box.min.x)/2,box.max.y+.002,(box.max.z+box.min.z)/2);mesh.raycast=()=>{};glass.add(mesh);owned.push(mesh);
   const y=box.max.y+.003; pulse(glass,[new T.Vector3(box.min.x,y,box.min.z),new T.Vector3(0,y,box.min.z),new T.Vector3(box.max.x,y,box.min.z),new T.Vector3(box.max.x,y,box.max.z)],.010,cool);
  }
 }
 if(name==='orb'){
  for(let i=0;i<3;i++){const pivot=group.getObjectByName('orbit-phase-'+i);if(pivot){
   const radius=[.68,.76,.84][i];pulse(pivot,arc(radius,.2+i,5.3+i),.012,i?cool:warm,i*.4);
   const mat=new T.MeshStandardMaterial({color:i?cool:warm,metalness:.65,roughness:.27,emissive:i?cool:warm,emissiveIntensity:dark?2.5:1.7});
   const node=new T.Mesh(new T.SphereGeometry(.027,16,10),mat);node.raycast=()=>{};pivot.add(node);owned.push(node);nodes.push({mesh:node,radius,phase:i*2.1});
  }}
  const core=group.getObjectByName('core-spin');if(core){const ring=pulse(core,arc(.496,-.2,3.4),.0035,cool);ring.rotation.x=.75;}
 }
 const head=new T.Object3D(),up=new T.Vector3(0,1,0),direction=new T.Vector3();
 return {update(h:number,dt:number,reduced:boolean){if(rotor&&!reduced){rotorAngle+=dt*h*.78;rotor.quaternion.copy(rotorRest!).multiply(new T.Quaternion().setFromAxisAngle(new T.Vector3(0,0,1),rotorAngle));}for(const mesh of owned)mesh.visible=mesh.userData.idleVisible||h>.001;for(const m of indicators)m.emissiveIntensity=.015+h*(dark?2.6:1.7);for(const n of nodes){const a=uniforms.uTime.value*.45+n.phase;n.mesh.position.set(Math.cos(a)*n.radius,Math.sin(a)*n.radius,0);n.mesh.scale.setScalar(h);}
  if(currentHeads){for(let i=0;i<currentRoutes.length;i++){const r=currentRoutes[i],t=T.MathUtils.euclideanModulo(uniforms.uTime.value*.44+r.phase,1);head.position.lerpVectors(r.start,r.end,t);direction.subVectors(r.end,r.start).normalize();head.quaternion.setFromUnitVectors(up,direction);head.scale.set(1,3.2,1);head.updateMatrix();currentHeads.setMatrixAt(i,head.matrix);}currentHeads.instanceMatrix.needsUpdate=true;(currentHeads.material as T.MeshBasicMaterial).opacity=h;}
 },
  details:()=>({activationMeshes:owned.length,outerEdges,rotorAvailable:rotor?1:0,rotorAngle}),
  dispose(){if(rotor&&rotorRest)rotor.quaternion.copy(rotorRest);for(const mesh of owned){mesh.removeFromParent();if(mesh instanceof T.InstancedMesh)mesh.dispose();mesh.geometry.dispose();(mesh.material as T.Material).dispose();}}
 };
}
