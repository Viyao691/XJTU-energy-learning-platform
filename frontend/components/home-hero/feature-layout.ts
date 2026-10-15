import type {Subject} from './interactions';
export type FeatureId='search'|'subscription'|'daily'|'library'|'learning'|'compare'|'qa'|'upload';
export type AnchorMap=Partial<Record<FeatureId,[number,number]>>;
export const featureLayout:{id:FeatureId;title:string;detail:string;href:string;model:Subject;x:number;y:number;preferred:[number,number];icon:string;side:'right'|'bottom'|'top'}[]=[
 {id:'search',title:'论文搜索',detail:'精准检索 · 快速定位',href:'/search',model:'city',x:748,y:214,preferred:[1106,394],icon:'search',side:'right'},
 {id:'subscription',title:'研究订阅',detail:'追踪主题 · 实时更新',href:'/subscriptions',model:'city',x:1060,y:139,preferred:[1198,263],icon:'bell',side:'bottom'},
 {id:'daily',title:'科研日报',detail:'每日研究线索 · 智能摘要',href:'/research-daily',model:'city',x:1340,y:139,preferred:[1451,284],icon:'daily',side:'bottom'},
 {id:'library',title:'论文库',detail:'管理 · 收藏 · 分享',href:'/library',model:'storage',x:742,y:393,preferred:[997,513],icon:'folder',side:'right'},
 {id:'learning',title:'学习中心',detail:'课程与资料库',href:'/learning',model:'wind',x:1632,y:162,preferred:[1785,398],icon:'cap',side:'bottom'},
 {id:'compare',title:'多篇比较',detail:'多维度 · 批量对比',href:'/compare',model:'solar',x:1605,y:844,preferred:[1743,795],icon:'scale',side:'top'},
 {id:'qa',title:'论文库问答',detail:'深度解析 · 循证洞见',href:'/knowledge',model:'orb',x:1090,y:825,preferred:[1355,870],icon:'chat',side:'right'},
 {id:'upload',title:'上传论文',detail:'从一篇研究开始',href:'/upload',model:'paper',x:243.2,y:684.7,preferred:[523,787],icon:'upload',side:'right'},
];
// Each route keeps its long segment in the free space between its card and model.
export function connectorPath(id:FeatureId,[x,y]:[number,number],top=featureLayout.find(c=>c.id===id)!.y){
 const middle=top+39,bottom=top+78;
 switch(id){
  case 'search':return `M960 ${middle} H990 Q1002 ${middle} 1002 ${middle+12} V${y-20} Q1002 ${y-8} 1014 ${y-8} H${x-10} Q${x} ${y-8} ${x} ${y}`;
  case 'subscription':return `M1166 ${bottom} V${y-23} Q1166 ${y-11} 1178 ${y-11} H${x-8} Q${x} ${y-11} ${x} ${y}`;
  case 'daily':return `M1446 ${bottom} V${y-14} Q1446 ${y-5} ${x} ${y}`;
  case 'library':return `M954 ${middle} H972 Q984 ${middle} 984 ${middle+12} V${y-12} Q984 ${y} ${x} ${y}`;
  case 'learning':return `M1738 ${bottom} V${y-37} Q1738 ${y-25} 1750 ${y-25} H${x-12} Q${x} ${y-25} ${x} ${y-13} V${y}`;
  case 'compare':return `M1711 ${top} V${y+25} Q1711 ${y+13} 1723 ${y+13} H${x-8} Q${x} ${y+13} ${x} ${y}`;
  case 'qa':return `M1302 ${middle} H${x-18} Q${x-8} ${middle} ${x} ${y}`;
  case 'upload':return `M455.2 ${middle} H470 Q482 ${middle} 482 ${middle+12} V${y-18} Q482 ${y-6} 494 ${y-6} H${x-8} Q${x} ${y-6} ${x} ${y}`;
 }
}

export type PhotographicFeatureId = 'library' | 'qa' | 'learning' | 'contests' | 'chronicle' | 'city';
export const photographicFeatureLayout: { id: PhotographicFeatureId; title: string; detail: string; href: string; icon: string; x: number; y: number; path: string; target: [number, number] }[] = [
 { id: 'library', title: '论文库', detail: '管理 · 收藏 · 阅读', href: '/library', icon: 'folder', x: 720, y: 350, path: 'M938 391h35q12 0 12 12v70', target: [985, 473] },
 { id: 'qa', title: '论文库问答', detail: '循证问答 · 页码引用', href: '/knowledge', icon: 'chat', x: 1080, y: 750, path: 'M1190 750v-48q0-15 15-15h130', target: [1335, 687] },
 { id: 'learning', title: '学习中心', detail: '课程 · 卡片 · 自测', href: '/learning', icon: 'cap', x: 1525, y: 515, path: 'M1634 515v-75q0-18 18-18h80', target: [1732, 422] },
 { id: 'contests', title: '科研创新竞赛', detail: '科研挑战 · 赛事实践', href: '/contests', icon: 'trophy', x: 1460, y: 345, path: 'M1678 386h19q18 0 18 18v151', target: [1715, 555] },
 { id: 'chronicle', title: '储能编年史', detail: '储能发展 · 历史脉络', href: '/research/chronicle', icon: 'calendar', x: 940, y: 125, path: 'M1049 207v55q0 20 20 20h81', target: [1150, 282] },
 { id: 'city', title: '储能城市应用', detail: '场景探索 · 城市能源', href: '/research/city-applications', icon: 'city', x: 1240, y: 125, path: 'M1349 207v101q0 22 22 22h19', target: [1390, 330] },
];
