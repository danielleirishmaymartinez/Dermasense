<template>
  <div class="landing-container">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-card">
        <div class="hero-left">
          <div class="image-grid">
            <img src="@/assets/Land.jpg" alt="Skin Image" class="skin-image" />
          </div>
        </div>
        <div class="hero-right">
          <h1>AI-Assisted Skin Lesion Check</h1>
          <p>
            DermaSense uses AI to help dermatologists and users review photos of 
            suspicious skin lesions. It provides quick classifications, confidence scores, 
            and general information about possible treatment options to support early consultation with 
            a dermatologist. It does not give a medical diagnosis or replace professional care.
          </p>
          <div class="cta-buttons">
            <button class="cta primary" @click="$router.push('/upload')">Start Analysis</button>
            <button class="cta secondary" @click="$router.push('/about')">Learn More</button>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
// This section remains empty for now. We just need to display the layout.
</script>

<style scoped>
.landing-container {
  width: 100%;
}

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

.cta-buttons {
  display: flex;
  gap: 16px;
  align-items: center;
}

.cta {
  padding: 16px 36px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  align-self: flex-start;
}

.cta.primary {
  background: linear-gradient(135deg, var(--medical-blue) 0%, var(--medical-blue-dark) 100%);
  color: var(--medical-white);
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
}

.cta.primary:hover {
  background: linear-gradient(135deg, var(--medical-blue-dark) 0%, var(--medical-blue) 100%);
  box-shadow: 0 6px 20px rgba(0, 102, 204, 0.4);
  transform: translateY(-2px);
}

.cta.secondary {
  background: var(--medical-white);
  color: var(--medical-blue);
  border: 2px solid var(--medical-blue);
  box-shadow: 0 2px 8px rgba(0, 102, 204, 0.1);
}

.cta.secondary:hover {
  background: var(--medical-blue-light);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.2);
}

.cta:active {
  transform: translateY(0);
}

/* Statistics Section */
.stats-section {
  margin: 60px 0;
  padding: 40px 0;
  background: linear-gradient(135deg, var(--medical-white) 0%, var(--medical-gray-50) 100%);
  border-radius: 12px;
}

.stats-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.stat-card {
  background: linear-gradient(135deg, var(--medical-blue-light) 0%, var(--medical-teal-light) 100%);
  padding: 32px 24px;
  border-radius: 16px;
  text-align: center;
  box-shadow: 0 4px 16px rgba(0, 102, 204, 0.1);
  border: 2px solid var(--medical-blue-light);
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 102, 204, 0.2);
  border-color: var(--medical-blue);
}

.stat-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.stat-number {
  font-size: 36px;
  font-weight: 700;
  color: var(--medical-blue-dark);
  margin-bottom: 8px;
}

.stat-label {
  font-size: 16px;
  color: var(--medical-gray-700);
  font-weight: 500;
}

/* Features Section */
.features-section {
  margin: 60px 0;
  padding: 50px 0;
  background: linear-gradient(135deg, var(--medical-gray-50) 0%, var(--medical-blue-light) 100%);
  border-radius: 12px;
}

.section-header {
  text-align: center;
  max-width: 1200px;
  margin: 0 auto 48px;
  padding: 0 20px;
}

.section-header h2 {
  font-size: 38px;
  color: var(--medical-gray-900);
  margin-bottom: 16px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.section-header h2::before {
  content: "✨";
  font-size: 42px;
}

.section-header p {
  font-size: 18px;
  color: var(--medical-gray-700);
  max-width: 600px;
  margin: 0 auto;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.feature-card {
  background: var(--medical-white);
  padding: 32px 28px;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 102, 204, 0.1);
  border: 2px solid var(--medical-gray-200);
  transition: all 0.3s ease;
  text-align: center;
}

.feature-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 8px 24px rgba(0, 102, 204, 0.2);
  border-color: var(--medical-blue);
}

.feature-icon {
  font-size: 56px;
  margin-bottom: 20px;
}

.feature-card h3 {
  font-size: 22px;
  color: var(--medical-gray-900);
  margin-bottom: 12px;
  font-weight: 700;
}

.feature-card p {
  font-size: 15px;
  color: var(--medical-gray-700);
  line-height: 1.7;
}

/* Responsive Design */
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

  .cta-buttons {
    flex-direction: column;
    width: 100%;
  }

  .cta {
    width: 100%;
    align-self: center;
  }

  .stats-container {
    grid-template-columns: repeat(2, 1fr);
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .steps-container {
    flex-direction: column;
  }

  .step-arrow {
    transform: rotate(90deg);
    margin: 8px 0;
  }

  .section-header h2 {
    font-size: 28px;
  }

  .cta-card {
    padding: 40px 24px;
  }

  .cta-card h2 {
    font-size: 28px;
  }
}

@media (max-width: 600px) {
  .stats-container {
    grid-template-columns: 1fr;
  }
}
</style>
