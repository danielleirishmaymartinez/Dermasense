<template>
  <div>
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-card">
        <div class="hero-left">
          <div class="image-grid">
            <img src="@/assets/Land.jpg" alt="Skin Image" class="skin-image" />
          </div>
        </div>
        <div class="hero-right">
          <h1>Get the Best Skin Treatments</h1>
          <p>
            This system assists dermatologists and users by classifying skin lesions and
            recommending treatments.
          </p>
          <button class="cta" @click="$router.push('/upload')">View Services</button>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
// This section remains empty for now. We just need to display the layout.
</script>

<style scoped>
/* Hero section */
.hero {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
  background: linear-gradient(135deg, var(--medical-blue-light) 0%, var(--medical-teal-light) 100%);
  padding: 40px 0 60px;
  border-radius: 12px;
}

.hero-card {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 50px;
  max-width: 1200px;
  background-color: var(--medical-white);
  padding: 50px 60px;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 102, 204, 0.12);
  border: 1px solid var(--medical-gray-200);
}

.hero-left {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.image-grid {
  position: relative;
}

.skin-image {
  width: 100%;
  max-width: 450px;
  border-radius: 12px;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
  border: 3px solid var(--medical-blue-light);
  object-fit: cover;
  transition: transform 0.3s ease;
}

.skin-image:hover {
  transform: scale(1.02);
}

/* Hero section right content */
.hero-right {
  flex: 1.2;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding-left: 40px;
}

.hero-right h1 {
  font-size: 42px;
  color: var(--medical-gray-900);
  margin-bottom: 20px;
  font-family: 'Inter', 'Roboto', sans-serif;
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -0.5px;
}

.hero-right h1::before {
  content: "🔬 ";
  color: var(--medical-blue);
}

.hero-right p {
  color: var(--medical-gray-700);
  font-size: 17px;
  margin-bottom: 32px;
  max-width: 520px;
  line-height: 1.7;
}

.cta {
  background: linear-gradient(135deg, var(--medical-blue) 0%, var(--medical-blue-dark) 100%);
  color: rgb(9, 9, 9);
  padding: 16px 36px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
  align-self: flex-start;
}

.cta:hover {
  background: linear-gradient(135deg, var(--medical-blue-dark) 0%, var(--medical-blue) 100%);
  box-shadow: 0 6px 20px rgba(0, 102, 204, 0.4);
  transform: translateY(-2px);
}

.cta:active {
  transform: translateY(0);
}

@media (max-width: 900px) {
  .hero-card {
    flex-direction: column;
    padding: 40px 30px;
    gap: 30px;
  }

  .hero-right {
    padding-left: 0;
    text-align: center;
  }

  .hero-right h1 {
    font-size: 32px;
  }

  .hero-right p {
    max-width: 100%;
  }

  .cta {
    align-self: center;
  }
}
</style>
