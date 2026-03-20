import { createBrowserRouter } from "react-router";
import { Layout } from "./components/Layout";
import { Home } from "./pages/Home";
import { Insights } from "./pages/Insights";
import { Assessment } from "./pages/Assessment";
import { Results } from "./pages/Results";
import { FullReport } from "./pages/FullReport";
import { ParentsGuidance } from "./pages/ParentsGuidance";
import { TeacherDashboard } from "./pages/TeacherDashboard";
import { About } from "./pages/About";

export const router = createBrowserRouter([
  {
    path: "/",
    Component: Layout,
    children: [
      { index: true, Component: Home },
      { path: "insights", Component: Insights },
      { path: "assessment", Component: Assessment },
      { path: "results", Component: Results },
      { path: "report", Component: FullReport },
      { path: "parents", Component: ParentsGuidance },
      { path: "teachers", Component: TeacherDashboard },
      { path: "about", Component: About },
    ],
  },
]);
