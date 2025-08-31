import * as React from "react";
import { clsx } from "clsx";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, ...props }, ref) => (
    <button
      ref={ref}
      className={clsx(
        "inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-foreground hover:bg-primary/90 disabled:pointer-events-none disabled:opacity-50",
        className
      )}
      {...props}
    />
  )
);
Button.displayName = "Button";
