// @vitest-environment jsdom
import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { LearningAnalyticsPanel } from "../components/LearningAnalyticsPanel";
import type { LearningAnalytics } from "../lib/api";

const auth = vi.hoisted(() => ({ webMode: false }));
vi.mock("../components/auth/AuthProvider", () => ({ useAuth: () => auth }));

const fixture: LearningAnalytics = {
  days: 7, from_date: "2026-09-18", to_date: "2026-09-24", history_start_date: "2026-09-18",
  daily: [{ date: "2026-09-18", reviews: 0, attempts: 0, completed_tasks: 0 }, { date: "2026-09-24", reviews: 4, attempts: 2, completed_tasks: 1 }],
  rating_distribution: { "不会": 1, "模糊": 2, "基本掌握": 1 }, correct_rate: null,
  mastery_distribution: { "未学习": 3, "学习中": 2, "已掌握": 1 }, due_review_count: 5,
  weaknesses: [{ concept: "层间滑移", score: 2.4, pack_count: 1, occurrence_count: 2, recurrence_count: 0 }],
};

describe("LearningAnalyticsPanel", () => {
  afterEach(() => { cleanup(); vi.restoreAllMocks(); vi.unstubAllGlobals(); auth.webMode = false; });

  it("fits all activity series and both endpoint dates inside a phone chart", () => {
    auth.webMode = true;
    vi.stubGlobal("matchMedia", () => ({ matches: true, addEventListener: vi.fn(), removeEventListener: vi.fn() }));
    vi.stubGlobal("ResizeObserver", class { observe() {} disconnect() {} });
    vi.spyOn(HTMLElement.prototype, "getBoundingClientRect").mockReturnValue({ width: 280, height: 240, x: 0, y: 0, top: 0, left: 0, right: 280, bottom: 240, toJSON: () => ({}) });
    const { container } = render(<LearningAnalyticsPanel data={fixture} days={7} onDays={vi.fn()} />);
    const chart = container.querySelector<SVGSVGElement>(".la-activity-svg")!;
    expect(Number(chart.getAttribute("viewBox")?.split(" ")[2])).toBeLessThanOrEqual(280);
    expect(Number(chart.getAttribute("viewBox")?.split(" ")[3])).toBe(180);
    expect(chart.querySelectorAll("rect")).toHaveLength(3);
    expect(chart.textContent).toContain("09-18");
    expect(chart.textContent).toContain("09-24");
  });

  it("keeps actual zero activity at zero height and shows missing accuracy as a dash", () => {
    const zero = { ...fixture, daily: [{ date: "2026-09-24", reviews: 0, attempts: 0, completed_tasks: 0 }] };
    const { container } = render(<LearningAnalyticsPanel data={zero} days={7} onDays={vi.fn()} />);
    expect(container.querySelectorAll(".la-activity-svg rect")).toHaveLength(0);
    expect(screen.getByText("—")).toBeTruthy();
  });

  it("distinguishes empty/loading/error states and gives empty mastery a neutral ring", () => {
    const { rerender, container } = render(<LearningAnalyticsPanel data={null} days={30} onDays={vi.fn()} loading />);
    expect(screen.getByRole("status").textContent).toContain("正在读取");
    rerender(<LearningAnalyticsPanel data={null} days={30} onDays={vi.fn()} error="读取失败" />);
    expect(screen.getByRole("alert").textContent).toBe("读取失败");
    rerender(<LearningAnalyticsPanel data={{ ...fixture, daily: [], mastery_distribution: {} }} days={30} onDays={vi.fn()} />);
    expect(screen.getByText("此范围暂无已记录活动。")).toBeTruthy();
    expect(screen.getByRole("img", { name: "知识掌握分布暂无卡片" })).toBeTruthy();
    expect(container.querySelector(".la-donut")?.getAttribute("style")).toBeNull();
  });

  it("renders the actual mastery and rating distributions and preserves range callbacks", async () => {
    const onDays = vi.fn();
    const { container } = render(<LearningAnalyticsPanel data={fixture} days={7} onDays={onDays} />);
    expect(screen.getByRole("img", { name: "知识掌握分布，共 6 张卡片" })).toBeTruthy();
    expect(screen.getByText("基本掌握")).toBeTruthy();
    expect(screen.getByText("层间滑移")).toBeTruthy();
    const ratingRows = container.querySelectorAll(".la-rating-list li");
    expect(ratingRows).toHaveLength(3);
    expect(container.querySelector(".la-rating-track i")?.getAttribute("style")).toContain("50%");
    await userEvent.click(screen.getByRole("button", { name: "90 天" }));
    expect(onDays).toHaveBeenCalledWith(90);
  });

  it("opens the daily activity table by keyboard from the compact disclosure", async () => {
    render(<LearningAnalyticsPanel data={fixture} days={7} onDays={vi.fn()} />);
    const disclosure = screen.getByText("查看每日活动明细（2 天）");
    disclosure.focus();
    await userEvent.keyboard("{Enter}");
    expect(screen.getByRole("table", { name: "7 天每日学习活动明细" })).toBeTruthy();
    expect(screen.getByRole("row", { name: /2026-09-24 4 2 1/ })).toBeTruthy();
  });
});
