"use client";
import React, { useId, useRef } from "react";
import { useRouter } from "next/navigation";

export function GuestLoginButton() {
  const dialog = useRef<HTMLDialogElement>(null);
  const titleId = useId();
  const descriptionId = useId();
  const router = useRouter();
  return <>
    <button className="web-guest-trigger" type="button" onClick={() => dialog.current?.showModal()}>游客登录</button>
    <dialog className="web-guest-dialog" ref={dialog} aria-labelledby={titleId} aria-describedby={descriptionId}>
      <p className="web-login-eyebrow">PUBLIC KNOWLEDGE</p>
      <h2 id={titleId}>以游客身份浏览</h2>
      <p id={descriptionId}>游客可浏览公开储能知识、储能纪事与校园资讯。个人论文、科研分析与研究记录需要注册或登录账号后使用。</p>
      <div className="web-guest-actions">
        <button type="button" className="web-guest-close" onClick={() => dialog.current?.close()}>返回登录</button>
        <button type="button" autoFocus onClick={() => { dialog.current?.close(); router.replace("/dashboard"); router.refresh(); }}>进入游客模式</button>
      </div>
    </dialog>
  </>;
}
