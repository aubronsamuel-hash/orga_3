import "../src/index.css";
import type { Preview } from "@storybook/react";
import React from "react";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "../src/lib/queryClient";
import { MemoryRouter } from "react-router-dom";

const withProviders = (Story: React.ComponentType) => (
  <MemoryRouter basename="/" initialEntries={["/"]}>
    <QueryClientProvider client={queryClient}>
      <Story />
    </QueryClientProvider>
  </MemoryRouter>
);

const preview: Preview = {
  decorators: [withProviders],
  parameters: {
    actions: { argTypesRegex: "^on[A-Z].*" },
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
  },
};

export default preview;
