import type { Meta, StoryObj } from "@storybook/react";
import { MemoryRouter } from "react-router-dom";
import { AppLayout } from "../ui/AppLayout";

const meta = {
  title: "Layout/AppLayout",
  component: AppLayout,
  decorators: [
    (Story) => (
      <MemoryRouter initialEntries={["/"]} basename="/">
        <Story />
      </MemoryRouter>
    ),
  ],
} satisfies Meta<typeof AppLayout>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {};
