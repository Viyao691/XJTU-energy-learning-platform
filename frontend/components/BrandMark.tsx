import React from "react";
import "./brand-mark.css";

/** The user's final A logo; the small-size originals stay legible in navigation. */
export function BrandMark() {
  return <span className="energy-brand-icon" aria-hidden="true">
    <img className="energy-brand-light" src="/brand/energy-ring-light.svg" alt="" width="36" height="36" />
    <img className="energy-brand-dark" src="/brand/energy-ring-dark.svg" alt="" width="36" height="36" />
  </span>;
}
