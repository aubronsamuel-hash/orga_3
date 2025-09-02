import type { Meta, StoryObj } from "@storybook/react";
import { AppLayout } from "../ui/AppLayout";

const meta = {
  title: "Layout/AppLayout",
  component: AppLayout,
  parameters: {
    layout: "fullscreen",
    chromatic: { disableSnapshot: true },
  },
} satisfies Meta<typeof AppLayout>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  play: async ({ canvasElement }) => {
    const header = canvasElement.querySelector("header");
    if (!header) throw new Error("Header not rendered");
  },
};
