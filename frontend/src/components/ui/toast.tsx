import * as React from "react";
import { clsx } from "clsx";

export interface ToastProps {
  open: boolean;
  message: string;
}

export function Toast({ open, message }: ToastProps) {
  if (!open) return null;
  return (
    <div
      role="status"
      aria-live="polite"
      className={clsx(
        "fixed bottom-4 right-4 rounded-md bg-foreground px-4 py-2 text-background shadow"
      )}
    >
      {message}
    </div>
  );
}
