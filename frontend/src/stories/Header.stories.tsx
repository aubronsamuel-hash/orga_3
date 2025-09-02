import type { Meta, StoryObj } from "@storybook/react";
import React from "react";
import { MemoryRouter } from "react-router-dom";
import { AppLayout } from "../ui/AppLayout";

const meta: Meta<typeof AppLayout> = {
  title: "Layout/AppLayout",
  component: AppLayout,
  // Garde-fou si une story consomme le Router (basename/useLocation) avant le decorateur global
  decorators: [
    (Story) => (
      <MemoryRouter basename="/" initialEntries={["/"]}>
        <Story />
      </MemoryRouter>
    ),
  ],
};
export default meta;

type Story = StoryObj<typeof AppLayout>;
export const Default: Story = {
  args: {},
};
