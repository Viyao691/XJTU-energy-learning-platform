import * as T from 'three';
import land from './earth-land.json';

// Natural Earth 1:110m land (public domain). Local data; no network request at runtime.
export function earthTextures(){
 const color=document.createElement('canvas'),emission=document.createElement('canvas'),rough=document.createElement('canvas');
 for(const canvas of [color,emission,rough]){canvas.width=2048;canvas.height=1024;}
 const c=color.getContext('2d')!,e=emission.getContext('2d')!,r=rough.getContext('2d')!;
 const ocean=c.createLinearGradient(0,0,0,1024);ocean.addColorStop(0,'#18374d');ocean.addColorStop(.5,'#102b42');ocean.addColorStop(1,'#20394a');
 c.fillStyle=ocean;c.fillRect(0,0,2048,1024);e.fillStyle='#000';e.fillRect(0,0,2048,1024);r.fillStyle='#a0a0a0';r.fillRect(0,0,2048,1024);
 const xy=(lon:number,lat:number)=>[(lon+180)/360*2048,(90-lat)/180*1024];
 for(const poly of land){
  for(const ctx of [c,e,r]){
   ctx.beginPath();for(const ring of poly){ring.forEach(([lon,lat],i)=>{const [x,y]=xy(lon,lat);if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);});ctx.closePath();}
   ctx.fillStyle=ctx===c?'#978760':ctx===e?'#454234':'#d1d1d1';ctx.fill('evenodd');
   if(ctx!==r){ctx.strokeStyle=ctx===c?'#d2c19a':'#b9ac83';ctx.lineWidth=ctx===c?1.35:1.8;ctx.stroke();}
  }
 }
 // Fine engraved graticule: geographically legible at rest, light circuitry only on hover.
 for(const ctx of [c,e]){ctx.strokeStyle=ctx===c?'#8c8b75':'#484d47';ctx.lineWidth=.85;
  for(let lon=-180;lon<=180;lon+=20){const x=xy(lon,0)[0];ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,1024);ctx.stroke();}
  for(let lat=-60;lat<=60;lat+=20){const y=xy(0,lat)[1];ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(2048,y);ctx.stroke();}
 }
 for(const [lon,lat] of [[-122,38],[-74,41],[-46,-24],[2,49],[13,52],[31,30],[77,29],[116,40],[139,36],[151,-34]]){const [x,y]=xy(lon,lat);e.fillStyle='#e9ddbf';e.beginPath();e.arc(x,y,2.8,0,Math.PI*2);e.fill();}
 const map=new T.CanvasTexture(color),glow=new T.CanvasTexture(emission),roughness=new T.CanvasTexture(rough);
 map.colorSpace=glow.colorSpace=T.SRGBColorSpace;for(const tex of [map,glow,roughness])tex.anisotropy=8;
 return {map,glow,roughness};
}
