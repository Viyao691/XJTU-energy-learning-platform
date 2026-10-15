import type { Metadata } from "next";
import "./globals.css";
import { WorkspaceShell } from "@/components/workspace/WorkspaceShell";
import { AuthProvider } from "@/components/auth/AuthProvider";
export const dynamic = "force-dynamic";
export const metadata: Metadata = { title: "储能科研学习平台", description: "储能科研学习平台 · Viyao", icons: { icon: [{ url: "/brand/energy-ring-light.svg", type: "image/svg+xml", media: "(prefers-color-scheme: light)" }, { url: "/brand/energy-ring-dark.svg", type: "image/svg+xml", media: "(prefers-color-scheme: dark)" }], apple: "/brand/apple-touch-icon.png" } };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) { return <html lang="zh-CN"><body><AuthProvider webMode={process.env.ENERGY_WEB_MODE === "true"}><WorkspaceShell>{children}</WorkspaceShell></AuthProvider></body></html>; }
