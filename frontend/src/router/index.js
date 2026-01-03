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
import LoginPage from "@/views/LoginPage.vue";
import RegisterPage from "@/views/RegisterPage.vue";
import ProfilePage from "@/views/ProfilePage.vue";
import { authService } from "@/services/auth";

const routes = [
  { path: "/", name: "Landing", component: LandingPage },
  { path: "/login", name: "Login", component: LoginPage },
  { path: "/register", name: "Register", component: RegisterPage },
  { 
    path: "/dashboard", 
    name: "Dashboard", 
    component: DashboardPage,
    meta: { requiresAuth: true }
  },
  { path: "/about", name: "About", component: AboutPage },
  { path: "/skin-self-exam", name: "SkinSelfExam", component: SkinSelfExamPage },
  { 
    path: "/upload", 
    name: "Upload", 
    component: UploadPage,
    meta: { requiresAuth: true }
  },
  { 
    path: "/analyzing", 
    name: "Analyzing", 
    component: AnalyzingPage,
    meta: { requiresAuth: true }
  },
  { 
    path: "/results", 
    name: "Results", 
    component: ResultPage,
    meta: { requiresAuth: true }
  },
  { 
    path: "/monitoring", 
    name: "Monitoring", 
    component: MonitoringPage,
    meta: { requiresAuth: true }
  },
  { 
    path: "/reports", 
    name: "Reports", 
    component: ReportsPage,
    meta: { requiresAuth: true }
  },
  { path: "/guide", name: "Guide", component: GuidePage },
  { 
    path: "/profile", 
    name: "Profile", 
    component: ProfilePage,
    meta: { requiresAuth: true }
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation guard for authentication
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const isAuthenticated = authService.isAuthenticated();

  if (requiresAuth && !isAuthenticated) {
    // Redirect to login if route requires auth and user is not authenticated
    next({ name: "Login", query: { redirect: to.fullPath } });
  } else if ((to.name === "Login" || to.name === "Register") && isAuthenticated) {
    // Redirect to dashboard if user is already logged in
    next({ name: "Dashboard" });
  } else {
    next();
  }
});

export default router;
