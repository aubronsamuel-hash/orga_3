import { createBrowserRouter } from "react-router-dom";
import { lazy } from "react";
import { AppLayout } from "./ui/AppLayout";
import { Home } from "./pages/Home";
import { Login } from "./pages/Login";
import { NotFound } from "./pages/NotFound";
import { Protected } from "./components/Protected";
import { Dashboard } from "./pages/Dashboard";
import { AuthProvider } from "./auth";

function WithAuth({ element }: { element: JSX.Element }) {
  return <AuthProvider>{element}</AuthProvider>;
}

const routes: any[] = [
  {
    path: "/",
    element: <WithAuth element={<AppLayout />} />,
    children: [
      { index: true, element: <Home /> },
      { path: "login", element: <Login /> },
      {
        path: "app",
        element: (
          <Protected>
            <Dashboard />
          </Protected>
        )
      },
      { path: "*", element: <NotFound /> }
    ]
  }
];

if (import.meta.env.MODE !== "production") {
  const RetryProbe = lazy(() => import("./pages/dev/RetryProbe"));
  routes.push({ path: "/dev/retry", element: <RetryProbe /> });
}

export const router = createBrowserRouter(routes);
