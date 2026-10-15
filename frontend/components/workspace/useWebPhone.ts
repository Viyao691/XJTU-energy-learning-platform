"use client";

import { useEffect, useState } from "react";
import { useAuth } from "../auth/AuthProvider";

export function useWebPhone() {
  const { webMode } = useAuth();
  const [phone, setPhone] = useState<boolean | null>(null);
  useEffect(() => {
    if (!webMode) return;
    const media = window.matchMedia("(max-width: 620px)");
    const sync = () => setPhone(media.matches);
    sync();
    media.addEventListener?.("change", sync);
    return () => media.removeEventListener?.("change", sync);
  }, [webMode]);
  // Hold visual runtimes until the client viewport is known.
  return { phone: webMode && phone === true, motion: !webMode || phone === false };
}
