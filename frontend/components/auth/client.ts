import { csrfHeaders } from "./session";
import type { ApiSchemas } from "../../lib/api.generated";

export type AuthUser = ApiSchemas["AuthUserResponse"];
export type AuthSession = ApiSchemas["AuthResponse"];
export type EmailCodeResponse = ApiSchemas["EmailCodeResponse"];

export async function authRequest<T>(path: string, payload?: object): Promise<T | null> {
  const method = payload ? "POST" : "GET";
  const response = await fetch(`/backend-api/api/v1/auth/${path}`, {
    method, credentials: "same-origin", cache: "no-store",
    headers: { "Content-Type": "application/json", ...csrfHeaders(method) },
    ...(payload ? { body: JSON.stringify(payload) } : {}),
  });
  if (path === "me" && response.status === 401) return null;
  const body = await response.json().catch(() => ({}));
  if (!response.ok) {
    const detail = body.detail;
    throw new Error(typeof detail === "string" ? detail : typeof detail?.message === "string" ? detail.message : `请求失败（${response.status}）`);
  }
  return body as T;
}
