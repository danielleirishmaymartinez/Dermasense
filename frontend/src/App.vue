<template>
  <div class="app-root">
    <NavBar />
    <main class="page">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import NavBar from "@/components/Navbar.vue";
</script>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  font-family: 'Inter', 'Roboto', system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

body {
  background: linear-gradient(135deg, #f8fafc 0%, #eff6ff 50%, #f0fdfa 100%);
  background-attachment: fixed;
  color: #1e293b;
}

.app-root {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.page {
  flex: 1;
  width: 100%;
  margin: 0 auto;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.page > * {
  width: 100%;
}

/* CSS Variables */
:root {
  /* Primary Colors */
  --color-primary-blue: #2563eb;
  --color-primary-cyan: #06b6d4;
  --color-primary-teal: #14b8a6;
  
  /* Secondary Colors */
  --color-green: #10b981;
  --color-emerald: #059669;
  --color-indigo: #6366f1;
  
  /* Status Colors */
  --color-red: #ef4444;
  --color-red-dark: #dc2626;
  --color-orange: #f59e0b;
  --color-amber: #d97706;
  
  /* Neutral Colors */
  --color-slate-50: #f8fafc;
  --color-slate-100: #f1f5f9;
  --color-slate-200: #e2e8f0;
  --color-slate-300: #cbd5e1;
  --color-slate-400: #94a3b8;
  --color-slate-500: #64748b;
  --color-slate-600: #475569;
  --color-slate-700: #334155;
  --color-slate-800: #1e293b;
  --color-slate-900: #0f172a;
  
  /* Background Colors */
  --color-bg-blue-50: #eff6ff;
  --color-bg-blue-100: #dbeafe;
  --color-bg-cyan-50: #ecfeff;
  --color-bg-cyan-100: #cffafe;
  --color-bg-teal-50: #f0fdfa;
  --color-bg-teal-100: #ccfbf1;
  --color-bg-red-50: #fee2e2;
  --color-bg-red-100: #fecaca;
  --color-bg-orange-50: #fff7ed;
  --color-bg-orange-100: #fed7aa;
  
  /* Spacing */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;
  --spacing-2xl: 3rem;
  --spacing-3xl: 4rem;
  
  /* Border Radius */
  --radius-sm: 0.375rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;
  --radius-xl: 1rem;
  --radius-2xl: 1.5rem;
  
  /* Shadows */
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.08);
  --shadow-lg: 0 10px 24px rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 20px 40px rgba(0, 0, 0, 0.12);
  --shadow-colored: 0 4px 20px rgba(37, 99, 235, 0.25);
  
  /* Transitions */
  --transition-fast: 0.15s ease;
  --transition-base: 0.3s ease;
  --transition-slow: 0.5s ease;
}

/* Global animations */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

.fade-in {
  animation: fadeIn 0.5s ease-out;
}

.slide-in {
  animation: slideIn 0.5s ease-out;
}

/* Scrollbar Styling */
::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}

::-webkit-scrollbar-track {
  background: var(--color-slate-100);
  border-radius: 10px;
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, var(--color-primary-blue), var(--color-primary-cyan));
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #1d4ed8, #0891b2);
}

/* Utility Classes */
.gradient-bg {
  background: linear-gradient(135deg, var(--color-primary-blue) 0%, var(--color-primary-cyan) 100%);
}

.gradient-text {
  background: linear-gradient(135deg, var(--color-primary-blue) 0%, var(--color-primary-cyan) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.card {
  background: white;
  border-radius: var(--radius-xl);
  padding: var(--spacing-xl);
  box-shadow: var(--shadow-md);
  border: 1px solid var(--color-slate-200);
  transition: all var(--transition-base);
}

.card:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: var(--radius-lg);
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all var(--transition-base);
  border: none;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-primary {
  background: linear-gradient(135deg, var(--color-primary-blue) 0%, var(--color-primary-cyan) 100%);
  color: white;
  box-shadow: var(--shadow-colored);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(37, 99, 235, 0.35);
}

.btn-secondary {
  background: white;
  color: var(--color-slate-700);
  border: 2px solid var(--color-slate-200);
}

.btn-secondary:hover {
  background: var(--color-slate-50);
  border-color: var(--color-primary-blue);
}

/* Responsive */
@media (max-width: 768px) {
  :root {
    --spacing-lg: 1rem;
    --spacing-xl: 1.5rem;
    --spacing-2xl: 2rem;
    --spacing-3xl: 3rem;
  }
}
</style>