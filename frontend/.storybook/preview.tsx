import "../src/index.css";
import type { Preview } from "@storybook/react";
import React from "react";
import { MemoryRouter } from "react-router-dom";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "../src/lib/queryClient";

const preview: Preview = {
  decorators: [
    (Story) => (
      <MemoryRouter basename="/">
        <QueryClientProvider client={queryClient}>
          <Story />
        </QueryClientProvider>
      </MemoryRouter>
    ),
  ],
  parameters: {
    // stability pour test-runner
    controls: { expanded: true },
    layout: "fullscreen",
  },
};

export default preview;
