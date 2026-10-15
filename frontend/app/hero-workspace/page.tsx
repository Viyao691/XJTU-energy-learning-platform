"use client";
import {useEffect,useState} from 'react';
import Hero from '../../components/home-hero/Hero';
export default function HeroWorkspace(){
 const [theme,setTheme]=useState<'light'|'dark'>('light'),[overview,setOverview]=useState(false),[sceneOnly,setSceneOnly]=useState(false),[environmentOnly,setEnvironmentOnly]=useState(false);
 useEffect(()=>{const p=new URLSearchParams(location.search);setTheme(p.get('theme')==='dark'?'dark':'light');setOverview(p.get('pose')==='hover-all');setSceneOnly(['only','environment'].includes(p.get('scene')||''));setEnvironmentOnly(p.get('scene')==='environment');},[]);
 return <div className="hi-preview"><Hero theme={theme} onTheme={setTheme} previewHoverAll={overview} sceneOnly={sceneOnly} environmentOnly={environmentOnly} calibrated/></div>;
}
