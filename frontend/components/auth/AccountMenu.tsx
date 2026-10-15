"use client";
import React, { useState } from "react";
import Link from "next/link";
import { useAuth } from "./AuthProvider";

export function AccountMenu() {
  const { user, loading, logout } = useAuth();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const signOut = async () => {
    setBusy(true); setError("");
    try { await logout(); }
    catch (reason) { setError(reason instanceof Error ? reason.message : "退出失败，请重试"); }
    finally { setBusy(false); }
  };
  return <div className="web-auth-account" aria-label="账户信息">
    <div className="web-account-identity">
      <span className="web-account-avatar" aria-hidden="true">{user ? user.email.charAt(0).toUpperCase() : <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6"><circle cx="12" cy="8" r="3.5" /><path d="M5 21v-2a7 7 0 0 1 14 0v2" /></svg>}</span>
      <div className="web-account-copy">
        <strong className="web-account-name">{loading ? "正在确认账户" : user ? "科研工作空间" : "游客"}</strong>
        <span className="web-account-detail" title={user?.email}>{loading ? <span role="status">请稍候…</span> : user ? user.email : "浏览公开储能知识"}</span>
        {!loading && <div className="web-account-status"><span aria-hidden="true" />{user ? (user.is_admin ? "管理员" : "科研用户") : "公开浏览模式"}</div>}
      </div>
    </div>
    {!loading && <div className="web-account-actions">{user ? <button type="button" disabled={busy} onClick={signOut}>{busy ? "正在退出…" : "退出登录"}</button> : <><Link className="web-account-login" href="/login">登录</Link><Link href="/login?mode=register">注册</Link></>}</div>}
    {error && <span className="web-account-error" role="alert">{error}</span>}
  </div>;
}
