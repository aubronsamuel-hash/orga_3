import type { Meta, StoryObj } from "@storybook/react";
import React from "react";
import { MemoryRouter, useLocation } from "react-router-dom";
import { AppLayout } from "../ui/AppLayout";
import { useSafeBasename } from "../lib/routerSafe";

const meta: Meta<typeof AppLayout> = {
  title: "Layout/AppLayout",
  component: AppLayout,
  decorators: [
    // Garde-fou local: si jamais le decorateur global n'est pas applique
    (Story) => (
      <MemoryRouter basename="/">
        <Story />
      </MemoryRouter>
    ),
  ],
};
export default meta;

type Story = StoryObj<typeof AppLayout>;

export const Default: Story = {
  render: () => {
    const basename = useSafeBasename("/");
    const loc = (() => {
      try {
        return useLocation();
      } catch {
        return {
          pathname: "/",
          search: "",
          hash: "",
          state: null,
          key: "init",
        } as ReturnType<typeof useLocation>;
      }
    })();

    return (
      <div data-basename={basename} data-path={loc.pathname}>
        <AppLayout />
      </div>
    );
  },
};

