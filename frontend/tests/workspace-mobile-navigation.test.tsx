// @vitest-environment jsdom
import React from "react";
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, expect, it, vi } from "vitest";

const state = vi.hoisted(() => ({ pathname: "/search", mobile: true }));
vi.mock("next/navigation", () => ({ usePathname: () => state.pathname }));
vi.mock("../components/auth/AuthProvider", () => ({ useAuth: () => ({ webMode: true, user: { is_admin: true } }) }));
vi.mock("../components/auth/AccountMenu", () => ({ AccountMenu: () => <span>账户</span> }));
vi.mock("../components/workspace/FullMaterialBackdrop", () => ({ FullMaterialBackdrop: () => <div data-testid="gpu-background" /> }));
vi.mock("../components/workspace/EnergyHeaderBackdrop", () => ({ EnergyHeaderBackdrop: () => <div data-testid="header-particles" /> }));
vi.mock("../components/react-bits/SpecularInteractions", () => ({ SpecularInteractions: () => <span data-testid="specular-runtime" /> }));
import { WorkspaceShell } from "../components/workspace/WorkspaceShell";

beforeEach(() => {
  state.pathname = "/search";
  state.mobile = true;
  vi.stubGlobal("matchMedia", () => ({ matches: state.mobile, addEventListener: vi.fn(), removeEventListener: vi.fn() }));
});
afterEach(() => { cleanup(); vi.unstubAllGlobals(); localStorage.clear(); });

it("closes from the outside button and restores keyboard focus", () => {
  render(<WorkspaceShell><p>正文</p></WorkspaceShell>);
  const menu = screen.getByRole("button", { name: "打开导航" });
  fireEvent.click(menu);
  fireEvent.click(screen.getByRole("button", { name: "收起导航菜单" }));
  expect(menu.getAttribute("aria-expanded")).toBe("false");
  expect(document.activeElement).toBe(menu);
});

it("closes only on a deliberate horizontal left swipe and keeps normal link taps", () => {
  const { container } = render(<WorkspaceShell><p>正文</p></WorkspaceShell>);
  const menu = screen.getByRole("button", { name: "打开导航" });
  const sidebar = container.querySelector("aside")!;
  fireEvent.click(menu);
  fireEvent.touchStart(sidebar, { touches: [{ clientX: 150, clientY: 160 }] });
  fireEvent.touchEnd(sidebar, { changedTouches: [{ clientX: 130, clientY: 260 }] });
  expect(menu.getAttribute("aria-expanded")).toBe("true");
  fireEvent.touchStart(sidebar, { touches: [{ clientX: 150, clientY: 160 }] });
  fireEvent.touchEnd(sidebar, { changedTouches: [{ clientX: 75, clientY: 170 }] });
  expect(menu.getAttribute("aria-expanded")).toBe("false");
  fireEvent.click(menu);
  const link = container.querySelector<HTMLAnchorElement>('.branched-menu a[href="/library"]')!;
  fireEvent.touchStart(link, { touches: [{ clientX: 100, clientY: 180 }] });
  fireEvent.touchEnd(link, { changedTouches: [{ clientX: 99, clientY: 181 }] });
  expect(fireEvent.click(link)).toBe(true);
  expect(link.getAttribute("href")).toBe("/library");
  expect(menu.getAttribute("aria-expanded")).toBe("false");
});

it("retains ESC dismissal and focus recovery", async () => {
  render(<WorkspaceShell><p>正文</p></WorkspaceShell>);
  const menu = screen.getByRole("button", { name: "打开导航" });
  fireEvent.click(menu);
  await waitFor(() => expect(document.activeElement?.getAttribute("href")).toBe("/dashboard"));
  fireEvent.keyDown(document, { key: "Escape" });
  expect(menu.getAttribute("aria-expanded")).toBe("false");
  expect(document.activeElement).toBe(menu);
});

it("uses static phone materials without mounting GPU effects and retains desktop effects", () => {
  const view = render(<WorkspaceShell><p>正文</p></WorkspaceShell>);
  expect(view.container.querySelector(".workspace-mobile-backdrop")).toBeTruthy();
  expect(screen.queryByTestId("gpu-background")).toBeNull();
  expect(screen.queryByTestId("specular-runtime")).toBeNull();
  expect(screen.getByText("储能科研学习智慧平台")).toBeTruthy();
  state.mobile = false;
  view.unmount();
  render(<WorkspaceShell><p>正文</p></WorkspaceShell>);
  expect(screen.getByTestId("gpu-background")).toBeTruthy();
  expect(screen.getByTestId("specular-runtime")).toBeTruthy();
  expect(screen.getByText(/研究工作台/)).toBeTruthy();
});
