import { createBrowserRouter } from "react-router-dom";
import { AppLayout } from "./ui/AppLayout";
import { Home } from "./pages/Home";
import { Login } from "./pages/Login";
import { NotFound } from "./pages/NotFound";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <AppLayout />,
    children: [
      { index: true, element: <Home /> },
      { path: "login", element: <Login /> },
      { path: "*", element: <NotFound /> }
    ]
  }
]);
