let webMode = false;
let csrfToken: string | null = null;

export function configureWebSession(enabled: boolean, token: string | null) {
  webMode = enabled;
  csrfToken = token;
}

export function csrfHeaders(method = "GET"): Record<string, string> {
  return webMode && csrfToken && /^(POST|PUT|PATCH|DELETE)$/i.test(method) ? { "X-CSRF-Token": csrfToken } : {};
}
