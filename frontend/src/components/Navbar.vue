<template>
  <header class="nav-wrapper">
    <div class="nav-inner">
      <div class="brand" @click="$router.push('/')">
        <div class="logo-container">
          <img src="/logo.png" alt="DermaSense Logo" class="logo-image" />
        </div>
        <div class="brand-text">
          <span class="brand-name">DermaSense</span>
          <span class="brand-tagline">Risk Assessment</span>
        </div>
      </div>
      
      <!-- Navigation Menu - Only show if NOT on landing page -->
      <nav v-if="!isLandingPage" class="nav-menu">
        <router-link to="/dashboard" class="nav-link" active-class="active">
          <span class="nav-text">Dashboard</span>
        </router-link>
        <router-link to="/upload" class="nav-link" active-class="active">
          <span class="nav-text">New Assessment</span>
        </router-link>
        <router-link to="/monitoring" class="nav-link" active-class="active">
          <span class="nav-text">Monitoring</span>
        </router-link>
        <router-link to="/reports" class="nav-link" active-class="active">
          <span class="nav-text">Reports</span>
        </router-link>
        <router-link to="/guide" class="nav-link" active-class="active">
          <span class="nav-text">Guide</span>
        </router-link>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

// Check if current page is landing page
const isLandingPage = computed(() => {
  return route.path === '/' || route.path === '';
});
</script>

<style scoped>
.nav-wrapper {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  position: sticky;
  top: 0;
  z-index: 1000;
  transition: all 0.3s ease;
}

.nav-wrapper:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.nav-inner {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.brand:hover {
  transform: translateY(-2px);
}

.logo-container {
  width: 3rem;
  height: 3rem;
  background: white;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15);
  transition: all 0.3s ease;
  padding: 0.25rem;
}

.brand:hover .logo-container {
  transform: rotate(5deg) scale(1.05);
  box-shadow: 0 6px 16px rgba(37, 99, 235, 0.25);
}

.logo-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
}

.brand-text {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.brand-name {
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #2563eb 0%, #06b6d4 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.5px;
  line-height: 1;
}

.brand-tagline {
  font-size: 0.6875rem;
  color: #64748b;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.nav-menu {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  flex-wrap: wrap;
}

.nav-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: #475569;
  font-size: 0.875rem;
  font-weight: 500;
  padding: 0.625rem 1rem;
  border-radius: 0.75rem;
  transition: all 0.3s ease;
  position: relative;
  white-space: nowrap;
}

.nav-link::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, #2563eb 0%, #06b6d4 100%);
  transition: width 0.3s ease;
  border-radius: 2px;
}

.nav-link:hover {
  color: #2563eb;
  background: #eff6ff;
  transform: translateY(-2px);
}

.nav-link.active {
  color: #2563eb;
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(37, 99, 235, 0.15);
}

.nav-link.active::before {
  width: 80%;
}

.nav-text {
  font-weight: inherit;
}

@media (max-width: 1024px) {
  .nav-inner {
    flex-direction: column;
    gap: 1rem;
  }

  .nav-menu {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 768px) {
  .brand-tagline {
    display: none;
  }

  .nav-menu {
    gap: 0.25rem;
    overflow-x: auto;
    padding-bottom: 0.5rem;
    -webkit-overflow-scrolling: touch;
  }

  .nav-link {
    padding: 0.5rem 0.75rem;
    font-size: 0.8125rem;
  }
}
</style>