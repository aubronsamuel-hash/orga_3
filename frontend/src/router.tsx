import { createBrowserRouter, type RouteObject } from "react-router-dom";
import { lazy } from "react";
import { AppLayout } from "./ui/AppLayout";
import { Home } from "./pages/Home";
import { Login } from "./pages/Login";
import { NotFound } from "./pages/NotFound";
import { Protected } from "./components/Protected";
import { Dashboard } from "./pages/Dashboard";
import { AuthProvider } from "./auth";
import MyMissions from "./pages/MyMissions";
import InviteLanding from "./pages/Invite";
const CalendarPage = lazy(() => import("./features/calendar/CalendarPage"));
import ConflictsPage from "./pages/ConflictsPage";

function WithAuth({ element }: { element: JSX.Element }) {
  return <AuthProvider>{element}</AuthProvider>;
}

const routes: RouteObject[] = [
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
        ),
      },
      { path: "calendar", element: <CalendarPage /> },
      {
        path: "my-missions",
        element: (
          <Protected>
            <MyMissions />
          </Protected>
        ),
      },
      { path: "conflicts", element: <ConflictsPage /> },
      { path: "invite", element: <InviteLanding /> },
      { path: "*", element: <NotFound /> },
    ],
  },
];

if (import.meta.env.MODE !== "production") {
  const RetryProbe = lazy(() => import("./pages/dev/RetryProbe"));
  routes.push({ path: "/dev/retry", element: <RetryProbe /> });
}

export const router = createBrowserRouter(routes);
