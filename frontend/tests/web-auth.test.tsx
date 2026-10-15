// @vitest-environment jsdom
import React from "react";
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { NextRequest } from "next/server";
const navigation = vi.hoisted(() => ({ pathname: "/library", replace: vi.fn(), refresh: vi.fn() }));
vi.mock("next/navigation", () => ({ usePathname: () => navigation.pathname, useRouter: () => navigation }));
import { middleware } from "../middleware";
import { safeReturnTo } from "../components/auth/routes";
import { AuthProvider } from "../components/auth/AuthProvider";
import { LoginForm } from "../components/auth/LoginForm";
import { AccountMenu } from "../components/auth/AccountMenu";
import { configureWebSession } from "../components/auth/session";
import { api } from "../lib/api";

const user = { id: 1, email: "research@example.org", is_admin: false };
const reply = (body: unknown, status = 200) => new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });
afterEach(() => { cleanup(); vi.unstubAllGlobals(); vi.unstubAllEnvs(); configureWebSession(false, null); });
beforeEach(() => {
  vi.clearAllMocks(); navigation.pathname = "/library";
  HTMLDialogElement.prototype.showModal = vi.fn(function (this: HTMLDialogElement) { this.open = true; });
  HTMLDialogElement.prototype.close = vi.fn(function (this: HTMLDialogElement) { this.open = false; });
});

describe("web authentication boundary", () => {
  it("keeps desktop routes open without session cookies", () => {
    vi.stubEnv("ENERGY_WEB_MODE", "false");
    expect(middleware(new NextRequest("https://energy.example/library")).headers.get("location")).toBeNull();
  });
  it("allows only explicit public pages and redirects private routes with a return address", () => {
    vi.stubEnv("ENERGY_WEB_MODE", "true");
    for (const path of ["/dashboard", "/research/chronicle", "/research/city-applications", "/help", "/campus", "/login", "/chronicle/photo.webp", "/brand/energy-ring-light.svg", "/brand/energy-ring-dark.svg", "/brand/apple-touch-icon.png", "/backend-api/api/v1/auth/me"]) {
      expect(middleware(new NextRequest(`https://energy.example${path}`)).headers.get("location")).toBeNull();
    }
    const location = middleware(new NextRequest("https://energy.example/library?page=2")).headers.get("location");
    expect(new URL(location!).searchParams.get("returnTo")).toBe("/library?page=2");
    expect(middleware(new NextRequest("https://energy.example/research/private")).headers.get("location")).toContain("/login?");
  });
  it("allows cookie-bearing navigation while the API remains the authentication authority", () => {
    vi.stubEnv("ENERGY_WEB_MODE", "true");
    expect(middleware(new NextRequest("https://energy.example/library", { headers: { cookie: "__Host-energy-session=session" } })).headers.get("location")).toBeNull();
  });
  it.each(["https://evil.example", "//evil.example", "/\\evil.example", "/%2f%2fevil.example", "/login", "/backend-api/api/v1/auth/logout", "/library\n"]) ("rejects unsafe return address %s", value => {
    expect(safeReturnTo(value)).toBe("/library");
  });
  it("keeps safe workspace return addresses", () => expect(safeReturnTo("/papers/7?tab=notes")).toBe("/papers/7?tab=notes"));
  it("does not mount private contents before session validation and redirects a guest", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(reply({ detail: "请先登录" }, 401)));
    render(<AuthProvider webMode><div>private papers</div></AuthProvider>);
    expect(screen.queryByText("private papers")).toBeNull();
    await waitFor(() => expect(navigation.replace).toHaveBeenCalledWith(expect.stringContaining("/login?returnTo=")));
    expect(screen.queryByText("private papers")).toBeNull();
  });
  it("preserves desktop rendering without any authentication request", () => {
    const fetchMock = vi.fn(); vi.stubGlobal("fetch", fetchMock);
    render(<AuthProvider webMode={false}><div>desktop papers</div></AuthProvider>);
    expect(screen.getByText("desktop papers")).toBeTruthy();
    expect(fetchMock).not.toHaveBeenCalled();
  });
  it("blocks non-admin settings before their controls mount", async () => {
    navigation.pathname = "/settings";
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(reply({ user, csrf_token: "csrf" })));
    render(<AuthProvider webMode><div>global model key controls</div></AuthProvider>);
    await screen.findByText("此页面仅供管理员使用");
    expect(screen.queryByText("global model key controls")).toBeNull();
  });
  it("adds CSRF only to mutations in web mode", async () => {
    const fetchMock = vi.fn().mockImplementation(async () => reply({})); vi.stubGlobal("fetch", fetchMock);
    configureWebSession(true, "csrf-value");
    await api.saveSettings({});
    expect(new Headers(fetchMock.mock.calls[0][1].headers).get("X-CSRF-Token")).toBe("csrf-value");
    await api.settings();
    expect(new Headers(fetchMock.mock.calls[1][1].headers).has("X-CSRF-Token")).toBe(false);
    configureWebSession(false, null);
    await api.saveSettings({});
    expect(new Headers(fetchMock.mock.calls[2][1].headers).has("X-CSRF-Token")).toBe(false);
  });
  it("shows send errors and a resend cooldown, then logs in with the entered code", async () => {
    navigation.pathname = "/login";
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(reply({ detail: "请先登录" }, 401))
      .mockResolvedValueOnce(reply({ detail: "邮件发送暂不可用" }, 503))
      .mockResolvedValueOnce(reply({ message: "已发送", retry_after_seconds: 45 }))
      .mockResolvedValueOnce(reply({ user, csrf_token: "csrf-login" }));
    vi.stubGlobal("fetch", fetchMock);
    render(<AuthProvider webMode><LoginForm returnTo="/papers/7" /></AuthProvider>);
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(1));
    fireEvent.change(screen.getByLabelText("邮箱"), { target: { value: user.email } });
    fireEvent.click(screen.getByRole("button", { name: "忘记密码" }));
    fireEvent.click(screen.getByRole("button", { name: "发送验证码" }));
    await screen.findByText("邮件发送暂不可用");
    fireEvent.click(screen.getByRole("button", { name: "发送验证码" }));
    const resend = await screen.findByRole("button", { name: /45 秒后重发/ });
    expect((resend as HTMLButtonElement).disabled).toBe(true);
    fireEvent.change(screen.getByLabelText("验证码"), { target: { value: "123456" } });
    fireEvent.click(screen.getByRole("button", { name: "登录" }));
    await waitFor(() => expect(navigation.replace).toHaveBeenCalledWith("/papers/7"));
    expect(JSON.parse(fetchMock.mock.calls[2][1].body)).toEqual({ email: user.email, intent: "login" });
    expect(JSON.parse(fetchMock.mock.calls[3][1].body)).toEqual({ email: user.email, code: "123456" });
  });
  it("logs out with CSRF, removes private content, and returns to public knowledge", async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(reply({ user, csrf_token: "csrf-logout" })).mockResolvedValueOnce(reply({ message: "已退出" }));
    vi.stubGlobal("fetch", fetchMock);
    render(<AuthProvider webMode><AccountMenu /><p>private content</p></AuthProvider>);
    fireEvent.click(await screen.findByRole("button", { name: "退出登录" }));
    await waitFor(() => expect(navigation.replace).toHaveBeenCalledWith("/dashboard"));
    expect(new Headers(fetchMock.mock.calls[1][1].headers).get("X-CSRF-Token")).toBe("csrf-logout");
    expect(screen.queryByText("private content")).toBeNull();
    expect(navigation.replace).not.toHaveBeenCalledWith(expect.stringContaining("/login?"));
  });
  it("registers explicitly with the email code, then returns to the requested workspace", async () => {
    navigation.pathname = "/login";
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(reply({ detail: "请先登录" }, 401))
      .mockResolvedValueOnce(reply({ retry_after_seconds: 60 }))
      .mockResolvedValueOnce(reply({ user, csrf_token: "csrf-register" }));
    vi.stubGlobal("fetch", fetchMock);
    render(<AuthProvider webMode><LoginForm returnTo="/papers/7" /></AuthProvider>);
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(1));
    fireEvent.click(screen.getByRole("button", { name: "注册账号" }));
    fireEvent.change(screen.getByLabelText("邮箱"), { target: { value: user.email } });
    fireEvent.click(screen.getByRole("button", { name: "发送验证码" }));
    await screen.findByText(/验证码已发送/);
    expect(JSON.parse(fetchMock.mock.calls[1][1].body)).toEqual({ email: user.email, intent: "register" });
    fireEvent.change(screen.getByLabelText("验证码"), { target: { value: "123456" } });
    fireEvent.change(screen.getByLabelText("设置密码"), { target: { value: "research-password" } });
    fireEvent.change(screen.getByLabelText("确认密码"), { target: { value: "research-password" } });
    fireEvent.click(screen.getByRole("button", { name: "注册并登录" }));
    await waitFor(() => expect(navigation.replace).toHaveBeenCalledWith("/papers/7"));
    expect(fetchMock.mock.calls[2][0]).toBe("/backend-api/api/v1/auth/register");
    expect(JSON.parse(fetchMock.mock.calls[2][1].body)).toEqual({ email: user.email, code: "123456", password: "research-password" });
  });
  it("defaults to password login without requesting an email code", async () => {
    navigation.pathname = "/login";
    const fetchMock = vi.fn().mockResolvedValueOnce(reply({ detail: "请先登录" }, 401)).mockResolvedValueOnce(reply({ user, csrf_token: "csrf" }));
    vi.stubGlobal("fetch", fetchMock);
    render(<AuthProvider webMode><LoginForm returnTo="/library" /></AuthProvider>);
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(1));
    expect(screen.queryByLabelText("验证码")).toBeNull();
    fireEvent.change(screen.getByLabelText("邮箱"), { target: { value: user.email } });
    fireEvent.change(screen.getByLabelText("密码"), { target: { value: "my-secret-password" } });
    fireEvent.click(screen.getByRole("button", { name: "登录" }));
    await waitFor(() => expect(navigation.replace).toHaveBeenCalledWith("/library"));
    expect(JSON.parse(fetchMock.mock.calls[1][1].body)).toEqual({ email: user.email, password: "my-secret-password" });
    expect(fetchMock.mock.calls[1][0]).toBe("/backend-api/api/v1/auth/login");
  });
  it("switches forgotten-password login back to password login without losing the email", async () => {
    navigation.pathname = "/login";
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(reply({ detail: "请先登录" }, 401)));
    render(<AuthProvider webMode><LoginForm /></AuthProvider>);
    fireEvent.change(screen.getByLabelText("邮箱"), { target: { value: user.email } });
    fireEvent.click(screen.getByRole("button", { name: "忘记密码" }));
    expect(screen.queryByLabelText("密码")).toBeNull();
    expect(screen.getByLabelText("验证码")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "返回密码登录" }));
    expect((screen.getByLabelText("邮箱") as HTMLInputElement).value).toBe(user.email);
    expect(screen.getByLabelText("密码")).toBeTruthy();
    expect(screen.queryByLabelText("验证码")).toBeNull();
  });
  it("rejects mismatched registration passwords before submitting", async () => {
    navigation.pathname = "/login";
    const fetchMock = vi.fn().mockResolvedValue(reply({ detail: "请先登录" }, 401));
    vi.stubGlobal("fetch", fetchMock);
    render(<AuthProvider webMode><LoginForm initialMode="register" /></AuthProvider>);
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(1));
    fireEvent.change(screen.getByLabelText("邮箱"), { target: { value: user.email } });
    fireEvent.change(screen.getByLabelText("验证码"), { target: { value: "123456" } });
    fireEvent.change(screen.getByLabelText("设置密码"), { target: { value: "research-password" } });
    fireEvent.change(screen.getByLabelText("确认密码"), { target: { value: "different-password" } });
    fireEvent.submit(screen.getByRole("button", { name: "注册并登录" }).closest("form")!);
    expect(await screen.findByRole("alert")).toHaveProperty("textContent", "两次输入的密码不一致");
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });
  it("shows and closes the guest dialog, and enters public content without an auth mutation", async () => {
    navigation.pathname = "/login";
    const fetchMock = vi.fn().mockResolvedValue(reply({ detail: "请先登录" }, 401));
    vi.stubGlobal("fetch", fetchMock);
    const showModal = HTMLDialogElement.prototype.showModal;
    const close = HTMLDialogElement.prototype.close;
    render(<AuthProvider webMode><LoginForm /></AuthProvider>);
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(1));
    fireEvent.click(screen.getByRole("button", { name: "游客登录" }));
    const dialog = screen.getByRole("dialog", { name: "以游客身份浏览" });
    expect(showModal).toHaveBeenCalledOnce();
    expect(dialog.textContent).toContain("公开储能知识、储能纪事与校园资讯");
    fireEvent.click(screen.getByRole("button", { name: "返回登录" }));
    expect(close).toHaveBeenCalledOnce();
    expect(screen.queryByRole("dialog")).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "游客登录" }));
    fireEvent.click(screen.getByRole("button", { name: "进入游客模式" }));
    expect(navigation.replace).toHaveBeenCalledWith("/dashboard");
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });
  it("shows guest identity and separate styled login and registration entries", async () => {
    navigation.pathname = "/dashboard";
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(reply({ detail: "请先登录" }, 401)));
    render(<AuthProvider webMode><AccountMenu /></AuthProvider>);
    await screen.findByText("游客");
    expect(screen.getByRole("link", { name: "登录" }).getAttribute("href")).toBe("/login");
    expect(screen.getByRole("link", { name: "注册" }).getAttribute("href")).toBe("/login?mode=register");
  });
  it("shows the full account email in its title and the administrator role", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(reply({ user: { ...user, is_admin: true }, csrf_token: "csrf" })));
    render(<AuthProvider webMode><AccountMenu /></AuthProvider>);
    expect((await screen.findByText(user.email)).getAttribute("title")).toBe(user.email);
    expect(screen.getByText("管理员")).toBeTruthy();
  });
});
