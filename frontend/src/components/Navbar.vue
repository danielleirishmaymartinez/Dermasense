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
  background-color: #d2e2f8;
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
  font-family: "Playfair Display", serif;
  font-size: 48px;
  font-weight: 700;
  font-style: italic;
  color: #2b2b2b;
}
.brand:hover{
  cursor: pointer;
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
  border-bottom: 2px solid #0c0c0c;
  padding-bottom: 3px;
}

.link:hover {
  color: #9da5f4;
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
