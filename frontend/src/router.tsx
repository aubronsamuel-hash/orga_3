import { createBrowserRouter } from "react-router-dom";
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

export const router = createBrowserRouter([
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
]);
