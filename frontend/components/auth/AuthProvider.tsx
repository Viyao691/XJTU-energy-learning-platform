"use client";
import React, { createContext, useContext, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { authRequest, type AuthSession, type AuthUser } from "./client";
import { configureWebSession } from "./session";
import { isAdminPage, isPublicPage, safeReturnTo } from "./routes";
import "./auth.css";

type AuthContextValue = { webMode: boolean; user: AuthUser | null; loading: boolean; setSession: (session: AuthSession | null) => void; logout: () => Promise<void> };
const AuthContext = createContext<AuthContextValue>({ webMode: false, user: null, loading: false, setSession: () => {}, logout: async () => {} });
export const useAuth = () => useContext(AuthContext);

export function AuthProvider({ webMode, children }: { webMode: boolean; children: React.ReactNode }) {
  const pathname = usePathname() || "/";
  const router = useRouter();
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(webMode);
  const [error, setError] = useState("");
  const [attempt, setAttempt] = useState(0);
  const leavingWorkspace = useRef(false);
  const setSession = (session: AuthSession | null) => {
    configureWebSession(webMode, session?.csrf_token ?? null);
    setUser(session?.user ?? null);
    setLoading(false);
  };
  useEffect(() => {
    configureWebSession(webMode, null);
    if (!webMode) return;
    let active = true;
    setLoading(true);
    setError("");
    authRequest<AuthSession>("me").then(session => { if (active) setSession(session); }).catch(reason => {
      if (active) { setError(reason instanceof Error ? reason.message : "登录状态暂时无法获取"); setLoading(false); }
    });
    return () => { active = false; };
  }, [webMode, attempt]); // Session initialization does not follow every page navigation.

  const publicPage = isPublicPage(pathname);
  useEffect(() => {
    if (publicPage) leavingWorkspace.current = false;
    if (webMode && !publicPage && !loading && !user && !error && !leavingWorkspace.current) {
      router.replace(`/login?returnTo=${encodeURIComponent(safeReturnTo(`${pathname}${window.location.search}`))}`);
    }
  }, [webMode, publicPage, loading, user, error, pathname, router]);

  const logout = async () => {
    await authRequest("logout", {});
    leavingWorkspace.current = true;
    setSession(null);
    router.replace("/dashboard");
    router.refresh();
  };
  let content = children;
  if (webMode && !publicPage) {
    if (loading) content = <main className="web-auth-state" role="status">正在确认登录状态…</main>;
    else if (error) content = <main className="web-auth-state"><p role="alert">{error}</p><button type="button" onClick={() => setAttempt(value => value + 1)}>重新连接</button><Link href="/dashboard">浏览公开知识</Link></main>;
    else if (!user) content = <main className="web-auth-state" role="status">{leavingWorkspace.current ? "正在退出工作空间…" : "正在前往登录…"}</main>;
    else if (isAdminPage(pathname) && !user.is_admin) content = <main className="web-auth-state"><h1>此页面仅供管理员使用</h1><Link href="/library">返回个人论文库</Link><Link href="/dashboard">浏览公开知识</Link></main>;
  }
  return <AuthContext.Provider value={{ webMode, user, loading, setSession, logout }}>{content}</AuthContext.Provider>;
}
