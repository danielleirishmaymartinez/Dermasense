<template>
  <header class="nav-wrapper">
    <div class="nav-inner">
      <div class="brand" @click="$router.push('/')">
        <div class="logo-container">
          <div class="logo-icon">🔬</div>
        </div>
        <div class="brand-text">
          <span class="brand-name">DermaSense</span>
          <span class="brand-tagline">Risk Assessment</span>
        </div>
      </div>
      <nav class="nav-menu">
        <router-link to="/dashboard" class="nav-link" active-class="active">
          <span class="nav-icon">📊</span>
          <span class="nav-text">Dashboard</span>
        </router-link>
        <router-link to="/upload" class="nav-link" active-class="active">
          <span class="nav-icon">📸</span>
          <span class="nav-text">New Assessment</span>
        </router-link>
        <router-link to="/monitoring" class="nav-link" active-class="active">
          <span class="nav-icon">📈</span>
          <span class="nav-text">Monitoring</span>
        </router-link>
        <router-link to="/reports" class="nav-link" active-class="active">
          <span class="nav-icon">📄</span>
          <span class="nav-text">Reports</span>
        </router-link>
        <router-link to="/guide" class="nav-link" active-class="active">
          <span class="nav-icon">📖</span>
          <span class="nav-text">Guide</span>
        </router-link>
      </nav>
    </div>
  </header>
</template>

<script setup>
// No authentication needed
</script>

<style scoped>
.nav-wrapper {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(0, 102, 204, 0.1);
  box-shadow: 0 2px 20px rgba(0, 102, 204, 0.08);
  position: sticky;
  top: 0;
  z-index: 1000;
  transition: all var(--transition-base);
}

.nav-wrapper:hover {
  box-shadow: 0 4px 30px rgba(0, 102, 204, 0.12);
}

.nav-inner {
  max-width: 1400px;
  margin: 0 auto;
  padding: var(--spacing-md) var(--spacing-lg);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--spacing-xl);
}

.brand {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  cursor: pointer;
  transition: transform var(--transition-base);
  padding: var(--spacing-xs);
  border-radius: var(--radius-md);
}

.brand:hover {
  transform: translateY(-2px);
}

.logo-container {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, var(--medical-blue) 0%, var(--medical-teal) 100%);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-colored);
  transition: all var(--transition-base);
}

.brand:hover .logo-container {
  transform: rotate(5deg) scale(1.05);
  box-shadow: 0 8px 24px rgba(0, 102, 204, 0.25);
}

.logo-icon {
  font-size: 24px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
}

.brand-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.brand-name {
  font-size: 24px;
  font-weight: 700;
  background: linear-gradient(135deg, var(--medical-blue) 0%, var(--medical-teal) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.5px;
  line-height: 1;
}

.brand-tagline {
  font-size: 11px;
  color: var(--medical-gray-600);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.nav-menu {
  display: flex;
  gap: var(--spacing-sm);
  align-items: center;
  flex-wrap: wrap;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  text-decoration: none;
  color: var(--medical-gray-700);
  font-size: 14px;
  font-weight: 500;
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-md);
  transition: all var(--transition-base);
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
  background: linear-gradient(90deg, var(--medical-blue) 0%, var(--medical-teal) 100%);
  transition: width var(--transition-base);
  border-radius: 2px;
}

.nav-link:hover {
  color: var(--medical-blue);
  background: var(--medical-blue-lighter);
  transform: translateY(-2px);
}

.nav-link.active {
  color: var(--medical-blue);
  background: linear-gradient(135deg, var(--medical-blue-light) 0%, var(--medical-teal-light) 100%);
  font-weight: 600;
  box-shadow: var(--shadow-sm);
}

.nav-link.active::before {
  width: 80%;
}

.nav-icon {
  font-size: 18px;
  transition: transform var(--transition-base);
}

.nav-link:hover .nav-icon {
  transform: scale(1.2);
}

.nav-text {
  font-weight: inherit;
}

@media (max-width: 1024px) {
  .nav-inner {
    flex-direction: column;
    gap: var(--spacing-md);
  }

  .nav-menu {
    width: 100%;
    justify-content: center;
  }

  .brand-tagline {
    display: none;
  }
}

@media (max-width: 768px) {
  .nav-menu {
    gap: var(--spacing-xs);
    overflow-x: auto;
    padding-bottom: var(--spacing-xs);
    -webkit-overflow-scrolling: touch;
  }

  .nav-link {
    padding: var(--spacing-xs) var(--spacing-sm);
    font-size: 13px;
  }

  .nav-text {
    display: none;
  }

  .nav-link {
    min-width: 44px;
    justify-content: center;
  }
}
</style>
