// @vitest-environment jsdom
import React from "react";
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, expect, it, vi } from "vitest";
import { FeedbackButton } from "../components/feedback/FeedbackButton";

beforeEach(() => {
  HTMLDialogElement.prototype.showModal = function () { this.setAttribute("open", ""); };
  HTMLDialogElement.prototype.close = function () { this.removeAttribute("open"); };
});
afterEach(() => { cleanup(); vi.unstubAllGlobals(); });

it("opens a labeled dialog, blocks blank input, and closes", () => {
  render(<FeedbackButton />);
  fireEvent.click(screen.getByRole("button", { name: "意见反馈" }));
  expect(screen.getByRole("dialog", { name: "意见反馈" })).toBeTruthy();
  expect((screen.getByRole("button", { name: "提交反馈" }) as HTMLButtonElement).disabled).toBe(true);
  expect(screen.getByLabelText("反馈内容").getAttribute("maxlength")).toBe("1000");
  fireEvent.click(screen.getByRole("button", { name: "关闭意见反馈" }));
  expect(screen.queryByRole("dialog")).toBeNull();
});

it("sends trimmed content once and displays the server delivery result", async () => {
  let finish!: (value: unknown) => void;
  const request = vi.fn((_url: string, _options: RequestInit) => new Promise(resolve => { finish = resolve; }));
  vi.stubGlobal("fetch", request);
  render(<FeedbackButton />);
  fireEvent.click(screen.getByRole("button", { name: "意见反馈" }));
  fireEvent.change(screen.getByLabelText("反馈内容"), { target: { value: "  手机菜单需要优化  " } });
  fireEvent.change(screen.getByLabelText("联系方式（选填）"), { target: { value: " test@example.test " } });
  fireEvent.click(screen.getByRole("button", { name: "提交反馈" }));
  expect((screen.getByRole("button", { name: "正在提交…" }) as HTMLButtonElement).disabled).toBe(true);
  expect(request).toHaveBeenCalledTimes(1);
  expect(JSON.parse(request.mock.calls[0][1].body as string)).toEqual({ message: "手机菜单需要优化", contact: "test@example.test" });
  finish({ ok: true, json: async () => ({ message: "反馈已保存，管理员通知暂时延迟" }) });
  await waitFor(() => expect(screen.getByRole("status").textContent).toContain("通知暂时延迟"));
  expect((screen.getByLabelText("反馈内容") as HTMLTextAreaElement).value).toBe("");
});

it("keeps the draft on a rejected request and allows retry", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: false, json: async () => ({ detail: "提交过于频繁，请稍后再试" }) }));
  render(<FeedbackButton />);
  fireEvent.click(screen.getByRole("button", { name: "意见反馈" }));
  fireEvent.change(screen.getByLabelText("反馈内容"), { target: { value: "保留这份反馈" } });
  fireEvent.click(screen.getByRole("button", { name: "提交反馈" }));
  await waitFor(() => expect(screen.getByRole("alert").textContent).toContain("提交过于频繁"));
  expect((screen.getByLabelText("反馈内容") as HTMLTextAreaElement).value).toBe("保留这份反馈");
  expect((screen.getByRole("button", { name: "提交反馈" }) as HTMLButtonElement).disabled).toBe(false);
});
