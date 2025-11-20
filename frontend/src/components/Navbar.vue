<template>
  <header class="nav-wrapper">
    <div class="nav-inner">
      <div class="brand" @click="$router.push('/')">
        DermaSense
      </div>
      <nav>
        <router-link to="/about" class="link" active-class="active">
          About
        </router-link>
        <router-link to="/skin-self-exam" class="link" active-class="active">
          Self-Exam Guide
        </router-link>
        <router-link to="/upload" class="link" active-class="active">
          Upload Image
        </router-link>
        <router-link to="/results" class="link" active-class="active">
          Results
        </router-link>
      </nav>
    </div>
  </header>
</template>

<style scoped>
.nav-wrapper {
  background-color: var(--medical-white);
  border-bottom: 2px solid var(--medical-blue-light);
  box-shadow: 0 2px 8px rgba(0, 102, 204, 0.08);
}

.nav-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 16px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.brand {
  font-family: 'Inter', 'Roboto', sans-serif;
  font-size: 28px;
  font-weight: 700;
  color: var(--medical-blue);
  letter-spacing: -0.5px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.brand::before {
  content: "⚕";
  font-size: 32px;
  color: var(--medical-teal);
}

.brand:hover {
  cursor: pointer;
  color: var(--medical-blue-dark);
  transition: color 0.2s ease;
}

nav {
  display: flex;
  gap: 32px;
  align-items: center;
}

.link {
  text-decoration: none;
  color: var(--medical-gray-700);
  font-size: 15px;
  font-weight: 500;
  font-family: 'Inter', 'Roboto', system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
    sans-serif;
  padding: 8px 12px;
  border-radius: 6px;
  transition: all 0.2s ease;
  position: relative;
}

.link.active {
  color: var(--medical-blue);
  background-color: var(--medical-blue-light);
  font-weight: 600;
}

.link:hover {
  color: var(--medical-blue);
  background-color: var(--medical-gray-50);
}

@media (max-width: 768px) {
  .nav-inner {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }

  .brand {
    font-size: 24px;
  }

  .brand::before {
    font-size: 28px;
  }

  nav {
    gap: 16px;
    flex-wrap: wrap;
  }

  .link {
    font-size: 14px;
    padding: 6px 10px;
  }
}
</style>
