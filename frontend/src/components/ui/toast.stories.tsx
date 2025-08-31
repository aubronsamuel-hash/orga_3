import type { Meta, StoryObj } from "@storybook/react";
import { useState } from "react";
import { Button } from "./button";
import { Toast } from "./toast";

const meta: Meta<typeof Toast> = {
  title: "UI/Toast",
  component: Toast,
};

export default meta;

function ToastDemo() {
  const [open, setOpen] = useState(false);
  return (
    <div>
      <Button onClick={() => setOpen(true)}>Show</Button>
      <Toast open={open} message="Saved" />
    </div>
  );
}

export const Basic: StoryObj<typeof Toast> = {
  render: () => <ToastDemo />,
};
