import { NextRequest, NextResponse } from "next/server";
import { isPublicPage, safeReturnTo } from "./components/auth/routes";

export function middleware(request: NextRequest) {
  if (process.env.ENERGY_WEB_MODE !== "true") return NextResponse.next();
  const pathname = request.nextUrl.pathname;
  if (isPublicPage(pathname) || /^\/(?:backend-api|_next|chronicle|home-hero|workspace|images|fonts)(?:\/|$)/.test(pathname) || pathname === "/favicon.ico" || pathname === "/sidebar-research-scene.png") return NextResponse.next();
  if (request.cookies.get("__Host-energy-session")?.value) return NextResponse.next();
  const login = new URL("/login", request.url);
  login.searchParams.set("returnTo", safeReturnTo(`${pathname}${request.nextUrl.search}`));
  return NextResponse.redirect(login);
}

export const config = { matcher: ["/((?!_next/static|_next/image).*)"] };
