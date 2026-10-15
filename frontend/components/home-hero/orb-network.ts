import * as T from 'three';

// A depth-tested geodesic shield sits just above the core, so rear links stay occluded.
export function createOrbNetwork(core:T.Object3D,dark:boolean,uniforms:{uTime:{value:number};uHover:{value:number}}){
 const lattice=new T.IcosahedronGeometry(.505,3),geometry=new T.WireframeGeometry(lattice);lattice.dispose();
 const tint=new T.Color(dark?'#b4dce9':'#a98343');
 const material=new T.ShaderMaterial({uniforms:{...uniforms,tint:{value:tint}},transparent:true,depthWrite:false,toneMapped:false,
  vertexShader:'varying vec3 spherePoint;void main(){spherePoint=normalize(position);gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',
  fragmentShader:`varying vec3 spherePoint;uniform float uTime,uHover;uniform vec3 tint;
  void main(){float phase=fract(atan(spherePoint.z,spherePoint.x)/6.28318+uTime*.115+spherePoint.y*.27);
   float sweep=exp(-pow((phase-.5)/.12,2.));float grid=.42+.9*sweep;
   gl_FragColor=vec4(mix(tint,vec3(1.,.94,.76),sweep)*${dark?'2.2':'1.8'},uHover*grid);}`});
 const links=new T.LineSegments(geometry,material);links.name='orb-geodesic-shield';links.raycast=()=>{};core.add(links);
 const positions:number[]=[],seeds:number[]=[];
 for(let i=0;i<34;i++){const y=1-2*(i+.5)/34,r=Math.sqrt(1-y*y),a=i*2.399963;positions.push(Math.cos(a)*r*.509,y*.509,Math.sin(a)*r*.509);seeds.push(i/34);}
 const points=new T.BufferGeometry();points.setAttribute('position',new T.Float32BufferAttribute(positions,3));points.setAttribute('phase',new T.Float32BufferAttribute(seeds,1));
 const dots=new T.ShaderMaterial({uniforms:{...uniforms,tint:{value:tint}},transparent:true,depthWrite:false,toneMapped:false,
  vertexShader:'attribute float phase;varying float nodePhase;void main(){nodePhase=phase;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);gl_PointSize=6.;}',
  fragmentShader:'varying float nodePhase;uniform float uTime,uHover;uniform vec3 tint;void main(){float r=length(gl_PointCoord-.5)*2.;float p=.28+.72*pow(.5+.5*sin(nodePhase*19.-uTime*2.4),6.);gl_FragColor=vec4(mix(tint,vec3(1.,.97,.87),p),uHover*(1.-smoothstep(.1,1.,r))*p);}' });
 const nodes=new T.Points(points,dots);nodes.name='orb-network-nodes';nodes.raycast=()=>{};core.add(nodes);
 return {segments:geometry.getAttribute('position').count/2,update(h:number){links.visible=nodes.visible=h>.001;},dispose(){links.removeFromParent();nodes.removeFromParent();geometry.dispose();material.dispose();points.dispose();dots.dispose();}};
}
