import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { AppLayout } from "./ui/AppLayout";

it("renders brand in header", () => {
  render(
    <MemoryRouter>
      <AppLayout />
    </MemoryRouter>
  );
  expect(screen.getByText("Coulisses Crew")).toBeInTheDocument();
});
