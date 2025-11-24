import { createRouter, createWebHistory } from "vue-router";
import LandingPage from "@/views/LandingPage.vue";
import AboutPage from "@/views/AboutPage.vue";
import UploadPage from "@/views/UploadPage.vue";
import AnalyzingPage from "@/views/AnalyzingPage.vue";
import ResultPage from "@/views/ResultPage.vue";
import SkinSelfExamPage from "@/views/SkinSelfExamPage.vue";

const routes = [
  { path: "/", name: "Landing", component: LandingPage },
  { path: "/about", name: "About", component: AboutPage },
  { path: "/skin-self-exam", name: "SkinSelfExam", component: SkinSelfExamPage },
  { path: "/upload", name: "Upload", component: UploadPage },
  { path: "/analyzing", name: "Analyzing", component: AnalyzingPage },
  { path: "/results", name: "Results", component: ResultPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
