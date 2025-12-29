import { createRouter, createWebHistory } from "vue-router";
import LandingPage from "@/views/LandingPage.vue";
import AboutPage from "@/views/AboutPage.vue";
import DashboardPage from "@/views/DashboardPage.vue";
import UploadPage from "@/views/UploadPage.vue";
import AnalyzingPage from "@/views/AnalyzingPage.vue";
import ResultPage from "@/views/ResultPage.vue";
import MonitoringPage from "@/views/MonitoringPage.vue";
import ReportsPage from "@/views/ReportsPage.vue";
import GuidePage from "@/views/GuidePage.vue";
import SkinSelfExamPage from "@/views/SkinSelfExamPage.vue";

const routes = [
  { path: "/", name: "Landing", component: LandingPage },
  { path: "/dashboard", name: "Dashboard", component: DashboardPage },
  { path: "/about", name: "About", component: AboutPage },
  { path: "/skin-self-exam", name: "SkinSelfExam", component: SkinSelfExamPage },
  { path: "/upload", name: "Upload", component: UploadPage },
  { path: "/analyzing", name: "Analyzing", component: AnalyzingPage },
  { path: "/results", name: "Results", component: ResultPage },
  { path: "/monitoring", name: "Monitoring", component: MonitoringPage },
  { path: "/reports", name: "Reports", component: ReportsPage },
  { path: "/guide", name: "Guide", component: GuidePage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
