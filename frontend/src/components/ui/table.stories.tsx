import type { Meta, StoryObj } from "@storybook/react";
import { Table, TableHeader, TableRow, TableHead, TableBody, TableCell } from "./table";

const meta: Meta<typeof Table> = {
  title: "UI/Table",
  component: Table,
};

export default meta;

export const Basic: StoryObj<typeof Table> = {
  render: () => (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Company</TableHead>
          <TableHead>Contact</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        <TableRow>
          <TableCell>ACME</TableCell>
          <TableCell>john@acme.io</TableCell>
        </TableRow>
      </TableBody>
    </Table>
  ),
};
