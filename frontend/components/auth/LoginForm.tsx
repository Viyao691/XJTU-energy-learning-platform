"use client";
import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "./AuthProvider";
import { authRequest, type AuthSession, type EmailCodeResponse } from "./client";
import { safeReturnTo } from "./routes";
import { GuestLoginButton } from "./GuestLoginButton";

export function LoginForm({ returnTo, initialMode = "login" }: { returnTo?: string; initialMode?: "login" | "register" }) {
  const auth = useAuth();
  const router = useRouter();
  const destination = safeReturnTo(returnTo);
  const [mode, setMode] = useState(initialMode);
  const [email, setEmail] = useState("");
  const [code, setCode] = useState("");
  const [loginMethod, setLoginMethod] = useState<"password" | "code">("password");
  const [password, setPassword] = useState("");
  const [confirmation, setConfirmation] = useState("");
  const [busy, setBusy] = useState<"send" | "submit" | null>(null);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [cooldown, setCooldown] = useState(0);
  useEffect(() => { if (auth.webMode && auth.user) { router.replace(destination); router.refresh(); } }, [auth.webMode, auth.user, destination, router]);
  useEffect(() => {
    if (!cooldown) return;
    const timer = window.setTimeout(() => setCooldown(value => value - 1), 1000);
    return () => window.clearTimeout(timer);
  }, [cooldown]);
  const useCode = mode === "register" || loginMethod === "code";
  const changeMode = (next: "login" | "register", method: "password" | "code" = "password") => {
    setMode(next); setLoginMethod(method); setCode(""); setPassword(""); setConfirmation(""); setError(""); setNotice("");
  };

  const sendCode = async () => {
    setBusy("send"); setError(""); setNotice("");
    try {
      const result = await authRequest<EmailCodeResponse>("email-code", { email: email.trim(), intent: mode });
      setCooldown(result?.retry_after_seconds ?? 60);
      setNotice("验证码已发送，未收到请检查垃圾邮件。");
    } catch (reason) { setError(reason instanceof Error ? reason.message : "验证码发送失败"); }
    finally { setBusy(null); }
  };
  const submit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault(); setError("");
    if (mode === "register" && password !== confirmation) { setError("两次输入的密码不一致"); return; }
    if ((!useCode || mode === "register") && (password.length < 8 || password.length > 128)) { setError("密码需为 8–128 个字符"); return; }
    setBusy("submit");
    try {
      const credentials = mode === "register" ? { code: code.trim(), password } : useCode ? { code: code.trim() } : { password };
      const session = await authRequest<AuthSession>(mode, { email: email.trim(), ...credentials });
      setPassword(""); setConfirmation("");
      auth.setSession(session);
    } catch (reason) { setError(reason instanceof Error ? reason.message : `${mode === "register" ? "注册" : "登录"}失败，请重新尝试`); }
    finally { setBusy(null); }
  };
  if (!auth.webMode) return <section className="web-login"><h1>本地工作空间</h1><p>桌面模式无需登录。</p><Link href="/library">进入论文库</Link></section>;
  return <section className="web-login" aria-labelledby="login-title">
    <div className="web-login-story">
      <span className="web-login-story-label">ENERGY RESEARCH COPILOT</span>
      <h2>读懂论文。<br />连接储能新知。</h2>
      <p>让分散的文献成为有据可循的知识，<br />让每一次研读推进你的研究。</p>
      <svg className="web-login-art" viewBox="0 0 400 240" fill="none" aria-hidden="true">
        <path d="M20 199H380M40 220H360M68 36V204M130 36V204M192 36V204M254 36V204M316 36V204M36 68H364M36 130H364" stroke="currentColor" opacity=".13" />
        <path d="M37 151C66 151 66 103 96 103S127 173 156 173 186 78 216 78 245 126 276 126 307 52 365 52" stroke="currentColor" strokeWidth="2" opacity=".5" />
        <rect x="113" y="71" width="166" height="132" rx="16" fill="var(--auth-story)" stroke="currentColor" strokeWidth="1.5" />
        <path d="M146 71V55H246V71M130 184H262M150 101V164M196 101V164M242 101V164" stroke="currentColor" strokeWidth="1.5" opacity=".6" />
        <rect x="141" y="130" width="18" height="44" rx="4" fill="currentColor" opacity=".22" />
        <rect x="187" y="112" width="18" height="62" rx="4" fill="currentColor" opacity=".4" />
        <rect x="233" y="94" width="18" height="80" rx="4" fill="currentColor" opacity=".65" />
        <circle cx="326" cy="52" r="23" fill="var(--auth-story)" stroke="currentColor" opacity=".7" />
        <path d="M329 39L318 54H328L323 66L335 50H326L329 39Z" fill="currentColor" />
        <circle cx="71" cy="160" r="5" fill="currentColor" opacity=".5" />
        <path d="M20 198L81 172M298 184L375 148" stroke="currentColor" opacity=".3" />
      </svg>
      <div className="web-login-story-topics"><span>论文研读</span><span>知识积累</span><span>科研实践</span></div>
      <small>从证据出发，让研究更进一步。</small>
    </div>
    <div className="web-login-panel">
    <header className="web-login-heading"><h1 id="login-title">{mode === "register" ? "创建科研账号" : useCode ? "验证码登录" : "欢迎回来"}</h1>
    <p>{mode === "register" ? "验证邮箱，设置你的登录密码。" : useCode ? "通过邮箱验证身份，无需输入密码。" : "登录你的个人科研空间。"}</p></header>
    <div className="web-login-modes" role="group" aria-label="账号入口">
      <button type="button" aria-pressed={mode === "login"} disabled={busy !== null} onClick={() => changeMode("login")}>密码登录</button>
      <button type="button" aria-pressed={mode === "register"} disabled={busy !== null} onClick={() => changeMode("register")}>注册账号</button>
    </div>
    <form onSubmit={submit} aria-busy={busy !== null}>
      <div className="web-login-field"><label htmlFor="web-login-email">邮箱</label>
      <input id="web-login-email" type="email" autoComplete={mode === "register" ? "email" : "username"} placeholder="name@example.com" required value={email} disabled={busy !== null} onChange={event => setEmail(event.target.value)} aria-describedby={error ? "web-login-error" : undefined} /></div>
      {useCode && <div className="web-login-field"><label htmlFor="web-login-code">验证码</label>
      <div className="web-login-code-row"><input id="web-login-code" type="text" inputMode="numeric" autoComplete="one-time-code" placeholder="6 位验证码" pattern="[0-9]{6}" maxLength={6} required value={code} disabled={busy !== null} onChange={event => setCode(event.target.value.replace(/\D/g, "").slice(0, 6))} aria-describedby={error ? "web-login-error" : undefined} />
      <button className="web-login-send" type="button" disabled={auth.loading || busy !== null || cooldown > 0 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())} onClick={sendCode}>{busy === "send" ? "正在发送…" : cooldown > 0 ? `${cooldown} 秒后重发` : "发送验证码"}</button></div></div>}
      {(!useCode || mode === "register") && <div className={mode === "register" ? "web-login-passwords" : undefined}>
        <div className="web-login-field"><label htmlFor="web-login-password">{mode === "register" ? "设置密码" : "密码"}</label>
        <input id="web-login-password" type="password" autoComplete={mode === "register" ? "new-password" : "current-password"} placeholder={mode === "register" ? "至少 8 个字符" : "请输入密码"} minLength={8} maxLength={128} required value={password} disabled={busy !== null} onChange={event => setPassword(event.target.value)} aria-describedby={error ? "web-login-error" : undefined} /></div>
        {mode === "register" && <div className="web-login-field"><label htmlFor="web-login-confirmation">确认密码</label><input id="web-login-confirmation" type="password" autoComplete="new-password" placeholder="再次输入密码" minLength={8} maxLength={128} required value={confirmation} disabled={busy !== null} onChange={event => setConfirmation(event.target.value)} aria-describedby={error ? "web-login-error" : undefined} /></div>}
      </div>}
      {mode === "login" && <div className="web-login-options"><button className="web-login-method" type="button" disabled={busy !== null} onClick={() => changeMode("login", useCode ? "password" : "code")}>{useCode ? "返回密码登录" : "忘记密码"}</button></div>}
      {auth.loading && <small role="status">正在确认登录状态…</small>}
      {error && <p id="web-login-error" role="alert">{error}</p>}
      {notice && <p role="status">{notice}</p>}
      <button className="web-login-submit" type="submit" disabled={auth.loading || busy !== null || !email || (useCode && code.length !== 6) || ((!useCode || mode === "register") && password.length < 8) || (mode === "register" && !confirmation)}>{busy === "submit" ? (mode === "register" ? "正在注册…" : "正在登录…") : (mode === "register" ? "注册并登录" : "登录")}</button>
    </form>
    <div className="web-login-divider"><span>先了解平台</span></div>
    <GuestLoginButton />
    </div>
  </section>;
}
