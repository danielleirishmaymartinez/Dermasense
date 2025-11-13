<template>
  <header class="nav-wrapper">
    <div class="nav-inner">
      <div class="brand" @click="$router.push('/')">
        DermaSense
      </div>
      <nav>
        <router-link to="/about" class="link" active-class="active">About</router-link>
        <router-link to="/upload" class="link" active-class="active">Upload Image</router-link>
        <router-link to="/results" class="link" active-class="active">Results</router-link>
      </nav>
    </div>
  </header>
</template>

<style scoped>
.nav-wrapper {
  background-color: #e3edf8;
  border-bottom: 1px solid #c7d5eb;
}
.nav-inner {
  max-width: 1100px;
  margin: 0 auto;
  padding: 14px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.brand {
  font-weight: 700;
  font-size: 22px;
  color: #234a7c;
  cursor: pointer;
}
nav {
  display: flex;
  gap: 24px;
}
.link {
  text-decoration: none;
  color: #234a7c;
  font-size: 14px;
}
.link.active {
  font-weight: 600;
  border-bottom: 2px solid #234a7c;
}
</style>
