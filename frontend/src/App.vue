<template>
  <div class="app-root">
    <NavBar />
    <main class="page">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import NavBar from "@/components/NavBar.vue";
</script>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
    sans-serif;
}

body {
  background-color: #f3f7fc;
}

.app-root {
  min-height: 100vh;
  background-color: #f3f7fc;
}

.page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 24px 64px;
}
</style>

