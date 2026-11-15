"use client";

import Link from 'next/link';
import { useEffect, useState, type ReactNode } from 'react';
import Features from './Features';
import HomeDock from './HomeDock';
import Particles from './Particles';
import type { PhotographicFeatureId } from './feature-layout';
import ThemePillSwitch from '../react-bits/ThemePillSwitch';
import { BrandMark } from '../BrandMark';
import { FeedbackButton } from '../feedback/FeedbackButton';
import './hero.css';

type Theme = 'light' | 'dark';
type IconName = 'bell';
type Props = { theme: Theme; onTheme: (theme: Theme) => void; papers?: number | null; subscriptions?: number | null; model?: string; unread?: number | null; previewHoverAll?: boolean; calibrated?: boolean; sceneOnly?: boolean; environmentOnly?: boolean };

function Icon({ name }: { name: IconName }) {
 const shapes: Record<IconName, ReactNode> = {
  bell: <><path d="M18 8a6 6 0 0 0-12 0c0 6-2 8-3 10h18c-1-2-3-4-3-10M10 21h4"/></>,
 };
 return <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">{shapes[name]}</svg>;
}

export default function Hero({ theme, onTheme, papers, subscriptions, model, unread, sceneOnly = false, environmentOnly = false }: Props) {
 const [hovered, setHovered] = useState<PhotographicFeatureId | null>(null);
 const [mobile, setMobile] = useState<boolean | null>(null);
 useEffect(() => {
  const viewport = window.matchMedia?.('(max-width: 900px)');
  const update = () => setMobile(viewport?.matches ?? false);
  update();
  viewport?.addEventListener('change', update);
  return () => viewport?.removeEventListener('change', update);
 }, []);
 useEffect(() => { setHovered(null); }, [theme]);
 return <section className={`integrated-hero hi-photo hi-${theme}${sceneOnly || environmentOnly ? ' hi-photo-scene-only' : ''}`} data-theme={theme} aria-label="储能科研工作台">
  <div className="hi-photo-frame">
   <img className="hi-photo-scene" src={`/home-hero/scene-${theme}.webp`} alt="" aria-hidden="true" width="1672" height="941" fetchPriority="high"/>
   {mobile === false && <Particles theme={theme}/>}
   <header className="hi-photo-header">
    <Link href="/dashboard" className="hi-photo-brand" aria-label="储能科研学习智慧平台 首页"><BrandMark /><span>Energy Storage<br/>Research &amp; Learning<br/>Smart Platform<small>储能科研学习智慧平台</small></span></Link>
    <div className="hi-photo-account"><FeedbackButton /><Link href="/research-daily" aria-label="科研通知" className="hi-photo-notice"><Icon name="bell"/>{typeof unread === 'number' && unread > 0 && <i/>}</Link><div className="hi-photo-theme"><ThemePillSwitch theme={theme} onChange={onTheme}/><a className="hi-photo-github" href="https://github.com/Viyao691/XJTU-energy-learning-platform" target="_blank" rel="noopener noreferrer" aria-label="GitHub 储能平台仓库（新窗口打开）" title="GitHub 仓库"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 .75a11.25 11.25 0 0 0-3.558 21.924c.563.104.77-.244.77-.542 0-.267-.01-.975-.015-1.914-3.13.68-3.79-1.51-3.79-1.51-.512-1.3-1.25-1.646-1.25-1.646-1.023-.7.078-.686.078-.686 1.13.08 1.725 1.16 1.725 1.16 1.006 1.724 2.64 1.226 3.283.938.102-.729.394-1.226.716-1.508-2.498-.284-5.124-1.25-5.124-5.565 0-1.23.44-2.234 1.16-3.022-.117-.285-.503-1.43.11-2.98 0 0 .945-.303 3.095 1.155a10.78 10.78 0 0 1 5.636 0c2.15-1.458 3.093-1.155 3.093-1.155.615 1.55.229 2.695.113 2.98.722.788 1.158 1.792 1.158 3.022 0 4.327-2.63 5.278-5.136 5.556.404.35.764 1.043.764 2.1 0 1.516-.014 2.738-.014 3.11 0 .3.203.652.774.541A11.25 11.25 0 0 0 12 .75Z"/></svg><small>点亮star</small></a></div><Link href="/settings" className="hi-photo-avatar" aria-label="个人设置">席</Link></div>
   </header>
   <div className="hi-photo-copy"><h1><img src={`/home-hero/title-${theme}.svg`} alt="储能科研，洞见未来" width="610" height="291"/></h1><p className="hi-photo-description">整合论文、检索、订阅、日报与智能工具，<br/>打造专注高效的一站式储能科研工作空间，<br/>助力每一次洞见与突破。</p><p className="hi-photo-motto">更清洁的能源 · 更美好的未来</p></div>
   <Features hovered={hovered} onHover={setHovered} mobile={mobile === true}/>
   <HomeDock papers={papers} subscriptions={subscriptions} model={model} unread={unread}/>
  </div>
 </section>;
}
