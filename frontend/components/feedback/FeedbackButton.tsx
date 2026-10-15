"use client";

import React, { useRef, useState } from "react";
import { csrfHeaders } from "../auth/session";
import type { ApiSchemas } from "../../lib/api.generated";
import "./feedback.css";

export function FeedbackButton() {
  const dialog = useRef<HTMLDialogElement>(null);
  const [message, setMessage] = useState("");
  const [contact, setContact] = useState("");
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState("");
  const [error, setError] = useState("");

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    if (busy || !message.trim()) return;
    setBusy(true); setError(""); setResult("");
    try {
      const response = await fetch("/backend-api/api/v1/feedback", {
        method: "POST", credentials: "same-origin",
        headers: { "Content-Type": "application/json", ...csrfHeaders("POST") },
        body: JSON.stringify({ message: message.trim(), contact: contact.trim() || null }),
      });
      const body = await response.json();
      if (!response.ok) throw new Error(typeof body.detail === "string" ? body.detail : "提交失败，请稍后重试");
      setResult((body as ApiSchemas["FeedbackResponse"]).message);
      setMessage(""); setContact("");
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "网络异常，请稍后重试");
    } finally { setBusy(false); }
  }

  return <>
    <button className="feedback-trigger" type="button" onClick={() => dialog.current?.showModal()} aria-label="意见反馈">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" aria-hidden="true"><path d="M5 4h14a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H9l-6 4V6a2 2 0 0 1 2-2Z"/><path d="M7 9h10M7 13h7"/></svg><span>意见反馈</span>
    </button>
    <dialog className="feedback-dialog" ref={dialog} aria-labelledby="feedback-title" onClick={event => { if (event.target === event.currentTarget) dialog.current?.close(); }}>
      <div className="feedback-heading"><h2 id="feedback-title">意见反馈</h2><button type="button" aria-label="关闭意见反馈" onClick={() => dialog.current?.close()}>关闭</button></div>
      <p className="feedback-note">反馈会保存并通知网站负责人，请勿填写密码或论文敏感内容。</p>
      <form onSubmit={submit}>
        <label htmlFor="feedback-message">反馈内容</label>
        <textarea id="feedback-message" required maxLength={1000} rows={5} value={message} onChange={event => setMessage(event.target.value)} />
        <small className="feedback-count">{message.length}/1000 字</small>
        <label htmlFor="feedback-contact">联系方式（选填）</label>
        <input id="feedback-contact" maxLength={200} value={contact} onChange={event => setContact(event.target.value)} placeholder="邮箱或其他联系方式" />
        {error && <p role="alert">{error}</p>}
        {result && <p className="feedback-result" role="status">{result}</p>}
        <button className="feedback-submit" disabled={busy || !message.trim()} type="submit">{busy ? "正在提交…" : "提交反馈"}</button>
      </form>
    </dialog>
  </>;
}
