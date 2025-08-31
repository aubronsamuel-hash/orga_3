import * as React from "react";
import { clsx } from "clsx";

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, ...props }, ref) => (
    <input
      ref={ref}
      className={clsx(
        "w-full rounded-md border border-foreground/20 bg-background px-3 py-2 text-sm text-foreground placeholder-foreground/60 disabled:pointer-events-none disabled:opacity-50",
        className
      )}
      {...props}
    />
  )
);
Input.displayName = "Input";
