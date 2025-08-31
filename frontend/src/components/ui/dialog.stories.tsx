import type { Meta, StoryObj } from "@storybook/react";
import { useState } from "react";
import { Dialog } from "./dialog";
import { Button } from "./button";

const meta: Meta<typeof Dialog> = {
  title: "UI/Dialog",
  component: Dialog,
};

export default meta;

function DialogDemo() {
  const [open, setOpen] = useState(false);
  return (
    <div>
      <Button onClick={() => setOpen(true)}>Open</Button>
      <Dialog open={open} onClose={() => setOpen(false)}>
        <p>Simple dialog content.</p>
      </Dialog>
    </div>
  );
}

export const Basic: StoryObj<typeof Dialog> = {
  render: () => <DialogDemo />,
};
