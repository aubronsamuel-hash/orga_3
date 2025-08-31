import type { Meta, StoryObj } from "@storybook/react";
import { Button } from "./button";

const meta: Meta<typeof Button> = {
  title: "UI/Button",
  component: Button,
};

export default meta;

export const Primary: StoryObj<typeof Button> = {
  render: () => <Button>Button</Button>,
};
