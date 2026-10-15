import { LoginForm } from "../../components/auth/LoginForm";
export default async function LoginPage({ searchParams }: { searchParams: Promise<{ returnTo?: string | string[]; mode?: string | string[] }> }) {
  const params = await searchParams;
  const mode = params.mode === "register" ? "register" : "login";
  return <LoginForm key={mode} initialMode={mode} returnTo={typeof params.returnTo === "string" ? params.returnTo : undefined} />;
}
