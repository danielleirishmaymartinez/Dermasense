<template>
  <div class="landing-container">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <!-- Left Content -->
        <div class="hero-text">
          <div class="hero-badge">
            <svg class="badge-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
            <span>AI-Powered Risk Assessment</span>
          </div>

          <h1 class="hero-title">
            <span class="gradient-text">DermaSense</span>
            <br />
            Skin Lesion Risk Assessment
          </h1>

          <p class="hero-description">
            Advanced machine learning technology combined with rule-based risk scoring 
            to provide accurate risk level assessments (Low / Medium / High) for skin lesions. 
            Monitor your skin health over time with comprehensive tracking and reporting.
          </p>

          <div class="hero-features">
            <div class="feature-item">
              <svg class="feature-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              <span>ML-Assisted</span>
            </div>
            <div class="feature-item">
              <svg class="feature-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              <span>Risk Scoring</span>
            </div>
            <div class="feature-item">
              <svg class="feature-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <span>Monitoring</span>
            </div>
          </div>

          <div class="cta-buttons">
            <button class="cta primary" @click="$router.push('/dashboard')">
              <span>Get Started</span>
              <svg class="arrow-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </button>
            <button class="cta secondary" @click="$router.push('/guide')">
              <span>Learn More</span>
            </button>
          </div>
        </div>

        <!-- Right Visual -->
        <div class="hero-visual">
          <div class="visual-card">
            <div class="card-glow"></div>
            <div class="card-content">
              <div class="visual-header">
                <span class="visual-title">Risk Assessment</span>
                <div class="visual-dots">
                  <span></span><span></span><span></span>
                </div>
              </div>
              <div class="visual-body">
                <div class="risk-display">
                  <div class="risk-circle high">
                    <span class="risk-percentage">68%</span>
                    <span class="risk-label">High Risk</span>
                  </div>
                </div>
                <div class="visual-stats">
                  <div class="stat blue">
                    <span class="stat-label">Image Risk</span>
                    <span class="stat-value">72%</span>
                  </div>
                  <div class="stat teal">
                    <span class="stat-label">Support Risk</span>
                    <span class="stat-value">40%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Disclaimer Section -->
    <section class="disclaimer-section">
      <div class="disclaimer-card">
        <svg class="disclaimer-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <div class="disclaimer-content">
          <h3>Important Disclaimer</h3>
          <p>
            This system is for <strong>risk assessment only</strong> and <strong>not a medical diagnosis</strong>. 
            It does not classify lesion types or provide medical diagnosis. 
            Always consult a dermatologist for professional evaluation.
          </p>
        </div>
      </div>
    </section>

    <!-- Features Grid -->
    <section class="features-section">
      <h2 class="section-title">Key Features</h2>
      <div class="features-grid">
        <div class="feature-card" v-for="(feature, index) in features" :key="index" :style="{ animationDelay: `${index * 0.1}s` }">
          <div class="feature-card-icon" :class="feature.colorClass">
            <div class="icon-inner"></div>
          </div>
          <h3>{{ feature.title }}</h3>
          <p>{{ feature.description }}</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from "vue";

const features = ref([
  {
    title: "AI-Powered Analysis",
    description: "Advanced DenseNet201 and Random Forest models for accurate risk probability estimation",
    colorClass: "blue-gradient"
  },
  {
    title: "Rule-Based Scoring",
    description: "Combines ML predictions with user inputs for comprehensive risk assessment",
    colorClass: "cyan-gradient"
  },
  {
    title: "Risk Level Classification",
    description: "Clear Low / Medium / High risk categorization for easy understanding",
    colorClass: "teal-gradient"
  },
  {
    title: "Monitoring & Tracking",
    description: "Track your skin health over time with detailed history and trend analysis",
    colorClass: "green-gradient"
  },
  {
    title: "Comprehensive Reports",
    description: "Generate and download detailed assessment reports with explanations",
    colorClass: "emerald-gradient"
  },
  {
    title: "Educational Resources",
    description: "Learn about skin health, ABCDE rule, and self-examination techniques",
    colorClass: "indigo-gradient"
  }
]);
</script>

<style scoped>
.landing-container {
  width: 100%;
  min-height: 100vh;
}

/* Hero Section */
.hero {
  padding: 5rem 1.5rem;
  max-width: 1400px;
  margin: 0 auto;
}

.hero-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
}

.hero-text {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: #eff6ff;
  border: 1px solid #3b82f6;
  border-radius: 50px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #1d4ed8;
  width: fit-content;
}

.badge-icon {
  width: 1rem;
  height: 1rem;
  stroke: currentColor;
}

.hero-title {
  font-size: clamp(2.5rem, 5vw, 3.75rem);
  font-weight: 800;
  line-height: 1.1;
  color: #1e293b;
  letter-spacing: -1px;
}

.gradient-text {
  background: linear-gradient(135deg, #2563eb 0%, #06b6d4 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-description {
  font-size: 1.125rem;
  line-height: 1.75;
  color: #475569;
}

.hero-features {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: white;
  border-radius: 0.75rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #334155;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  width: 1.25rem;
  height: 1.25rem;
  stroke: #2563eb;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  padding-top: 1rem;
}

.cta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  border: none;
  border-radius: 0.75rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cta.primary {
  background: linear-gradient(135deg, #2563eb 0%, #06b6d4 100%);
  color: white;
  box-shadow: 0 4px 20px rgba(37, 99, 235, 0.3);
}

.cta.primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 30px rgba(37, 99, 235, 0.4);
}

.cta.secondary {
  background: white;
  color: #334155;
  border: 2px solid #e2e8f0;
}

.cta.secondary:hover {
  background: #f8fafc;
  border-color: #3b82f6;
}

.arrow-icon {
  width: 1.25rem;
  height: 1.25rem;
  transition: transform 0.3s ease;
}

.cta.primary:hover .arrow-icon {
  transform: translateX(4px);
}

/* Hero Visual */
.hero-visual {
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.visual-card {
  position: relative;
  width: 100%;
  max-width: 450px;
  background: white;
  border-radius: 1.5rem;
  padding: 2rem;
  box-shadow: 0 20px 60px rgba(37, 99, 235, 0.15);
  border: 1px solid #e2e8f0;
  animation: fadeInUp 0.8s ease-out;
}

.card-glow {
  position: absolute;
  inset: -2px;
  background: linear-gradient(135deg, #3b82f6, #06b6d4);
  border-radius: 1.5rem;
  opacity: 0.3;
  filter: blur(20px);
  z-index: -1;
  animation: pulse 3s ease-in-out infinite;
}

.visual-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.visual-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #475569;
}

.visual-dots {
  display: flex;
  gap: 0.375rem;
}

.visual-dots span {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  background: #cbd5e1;
}

.visual-body {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.risk-display {
  display: flex;
  justify-content: center;
}

.risk-circle {
  width: 12rem;
  height: 12rem;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: inset 0 4px 20px rgba(0, 0, 0, 0.1);
}

.risk-circle.high {
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  border: 4px solid #ef4444;
}

.risk-percentage {
  font-size: 2.5rem;
  font-weight: 700;
  color: #dc2626;
  line-height: 1;
}

.risk-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #dc2626;
  margin-top: 0.5rem;
}

.visual-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.stat {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding: 1rem;
  border-radius: 0.75rem;
  border: 1px solid;
}

.stat.blue {
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  border-color: #3b82f6;
}

.stat.teal {
  background: linear-gradient(135deg, #f0fdfa 0%, #ccfbf1 100%);
  border-color: #14b8a6;
}

.stat-label {
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 500;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
}

.stat.blue .stat-value {
  color: #2563eb;
}

.stat.teal .stat-value {
  color: #0d9488;
}

/* Disclaimer Section */
.disclaimer-section {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 1.5rem 3rem;
}

.disclaimer-card {
  display: flex;
  gap: 1.5rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #fff7ed 0%, #fed7aa 100%);
  border-radius: 1rem;
  border-left: 4px solid #f59e0b;
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.15);
  animation: fadeInUp 0.8s ease-out 0.2s both;
}

.disclaimer-icon {
  width: 2rem;
  height: 2rem;
  flex-shrink: 0;
  stroke: #d97706;
  margin-top: 0.25rem;
}

.disclaimer-content h3 {
  font-size: 1.125rem;
  color: #92400e;
  margin-bottom: 0.5rem;
  font-weight: 700;
}

.disclaimer-content p {
  font-size: 0.9375rem;
  color: #92400e;
  line-height: 1.7;
}

/* Features Section */
.features-section {
  max-width: 1400px;
  margin: 0 auto;
  padding: 3rem 1.5rem 5rem;
}

.section-title {
  font-size: 2.25rem;
  font-weight: 700;
  text-align: center;
  margin-bottom: 3rem;
  background: linear-gradient(135deg, #2563eb 0%, #06b6d4 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
  animation: fadeInUp 0.8s ease-out both;
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12);
  border-color: #3b82f6;
}

.feature-card-icon {
  width: 3rem;
  height: 3rem;
  border-radius: 0.75rem;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.feature-card:hover .feature-card-icon {
  transform: scale(1.1);
}

.icon-inner {
  width: 1.5rem;
  height: 1.5rem;
  background: white;
  border-radius: 0.375rem;
}

.blue-gradient {
  background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%);
}

.cyan-gradient {
  background: linear-gradient(135deg, #06b6d4 0%, #14b8a6 100%);
}

.teal-gradient {
  background: linear-gradient(135deg, #14b8a6 0%, #10b981 100%);
}

.green-gradient {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.emerald-gradient {
  background: linear-gradient(135deg, #059669 0%, #3b82f6 100%);
}

.indigo-gradient {
  background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
}

.feature-card h3 {
  font-size: 1.25rem;
  color: #1e293b;
  margin-bottom: 0.75rem;
  font-weight: 700;
}

.feature-card p {
  font-size: 0.9375rem;
  color: #475569;
  line-height: 1.7;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 0.3;
  }
  50% {
    opacity: 0.5;
  }
}

@media (max-width: 1024px) {
  .hero-content {
    grid-template-columns: 1fr;
    gap: 3rem;
  }

  .hero-visual {
    order: -1;
  }
}

@media (max-width: 768px) {
  .hero {
    padding: 3rem 1rem;
  }

  .hero-title {
    font-size: 2rem;
  }

  .hero-description {
    font-size: 1rem;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .disclaimer-card {
    flex-direction: column;
    text-align: center;
    align-items: center;
  }
}
</style>