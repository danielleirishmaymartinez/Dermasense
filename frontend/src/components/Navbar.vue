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
  background-color: #f5e8dd; /* nude */
  border-bottom: 1px solid #e1cdbd;
}

.nav-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 18px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.brand {
  font-weight: 800;
  font-size: 40px; /* bigger logo text */
  letter-spacing: 0.04em;
  color: #2b2b2b;
  cursor: pointer;
  font-family: "Poppins", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
    sans-serif;
}

nav {
  display: flex;
  gap: 30px;
}

.link {
  text-decoration: none;
  color: #3b3b3b;
  font-size: 18px; /* bigger nav text */
  font-weight: 600;
  font-family: "Poppins", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
    sans-serif;
}

.link.active {
  border-bottom: 2px solid #c48b62;
  padding-bottom: 3px;
}

.link:hover {
  color: #c0794f;
}

@media (max-width: 768px) {
  .nav-inner {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }

  .brand {
    font-size: 32px;
  }

  nav {
    gap: 18px;
  }
}
</style>
