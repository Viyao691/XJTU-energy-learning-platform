import * as T from 'three';
import {createOrb} from './orb-baseline';

import {earthTextures} from './earth-textures';

export function createLiveOrb(dark:boolean):T.Group{
 const group=createOrb(dark) as T.Group,core=group.getObjectByName('core-spin')!;
 const sphere=core.children[0] as T.Mesh<T.BufferGeometry,T.MeshStandardMaterial>;
 const metals=new Set<T.MeshStandardMaterial>();group.traverse(o=>{if(o instanceof T.Mesh&&o!==sphere)for(const m of Array.isArray(o.material)?o.material:[o.material])if(m instanceof T.MeshStandardMaterial&&m.metalness>.6)metals.add(m);});
 for(const m of metals){m.color.set(dark?'#b5c4ce':'#d9dfe0');m.metalness=.90;m.roughness=dark?.25:.27;m.envMapIntensity=1.35;}
 const {map,glow,roughness}=earthTextures();sphere.material.dispose();
 sphere.material=new T.MeshPhysicalMaterial({color:'#ffffff',map,roughnessMap:roughness,metalness:.72,roughness:dark?.48:.50,clearcoat:.24,clearcoatRoughness:.29,envMapIntensity:1.1,emissiveMap:glow,emissive:dark?'#c2dfef':'#d8b77e',emissiveIntensity:dark?.13:.055});
 sphere.material.userData.earthCore=true;core.rotation.y=-.65;
 return group;
}
