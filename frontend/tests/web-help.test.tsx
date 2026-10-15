// @vitest-environment jsdom
import React from "react";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, expect, it, vi } from "vitest";
vi.mock("../components/auth/AuthProvider", () => ({ useAuth: () => ({ webMode: true }) }));
vi.mock("../components/workspace/MaterialHero", () => ({ default: () => null }));
vi.mock("../components/workspace/TitleMotion", () => ({ default: ({ text }: { text: string }) => <span>{text}</span> }));
import HelpPage from "../app/help/page";
afterEach(cleanup);

it("explains actual Web login, enforced budgets, feedback and embedding limits", () => {
  render(<HelpPage />);
  expect(screen.getAllByText(/忘记密码/).length).toBeGreaterThan(0);
  expect(screen.getByText(/平台每日20元、每月100元/)).toBeTruthy();
  expect(screen.queryByText(/不会按金额自动停止调用/)).toBeNull();
  expect(screen.getByText(/状态检查不会调用嵌入服务/)).toBeTruthy();
  expect(screen.getByText(/手机采用静态背景/)).toBeTruthy();
  expect(screen.queryByText(/在项目目录运行/)).toBeNull();
});

it("searches new feedback guidance and opens its matched entry", () => {
  render(<HelpPage />);
  fireEvent.change(screen.getByRole("searchbox"), { target: { value: "怎样提交意见反馈" } });
  expect(screen.getByText("怎样提交意见反馈？")).toBeTruthy();
  expect(screen.getByText(/最多1000字/)).toBeTruthy();
  expect(screen.queryByText("费用与预算")).toBeNull();
});
