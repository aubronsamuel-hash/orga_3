import type { Meta, StoryObj } from "@storybook/react";
import Legend from "./Legend";

const meta: Meta<typeof Legend> = {
  title: "Calendar/Legend",
  component: Legend,
};
export default meta;
export const Basic: StoryObj<typeof Legend> = { args: {} };
