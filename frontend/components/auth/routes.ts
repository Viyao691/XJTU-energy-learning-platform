const publicPages = new Set(["/", "/dashboard", "/research", "/research/chronicle", "/research/city-applications", "/help", "/campus", "/login"]);
const adminPages = new Set(["/settings", "/diagnostics", "/maintenance", "/onboarding"]);
export const isPublicPage = (pathname: string) => publicPages.has(pathname);
export const isAdminPage = (pathname: string) => adminPages.has(pathname);

export function safeReturnTo(value: string | null | undefined): string {
  if (!value || !value.startsWith("/") || value.startsWith("//") || /[\\\x00-\x20]|%(?:2f|5c|0[0-9a-f]|1[0-9a-f]|20|25)/i.test(value)) return "/library";
  const url = new URL(value, "https://energy.invalid");
  if (url.origin !== "https://energy.invalid" || /^\/(?:login|backend-api|_next)(?:\/|$)/.test(url.pathname)) return "/library";
  return `${url.pathname}${url.search}${url.hash}`;
}
