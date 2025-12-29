<template>
  <div class="landing-container fade-in">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-background">
        <div class="gradient-orb orb-1"></div>
        <div class="gradient-orb orb-2"></div>
        <div class="gradient-orb orb-3"></div>
      </div>
      <div class="hero-content">
        <div class="hero-text">
          <div class="hero-badge">
            <span class="badge-icon">🤖</span>
            <span>AI-Powered Risk Assessment</span>
          </div>
          <h1 class="hero-title">
            <span class="gradient-text">DermaSense</span>
            <br />
            Skin Lesion Risk Assessment System
          </h1>
          <p class="hero-description">
            Advanced machine learning technology combined with rule-based risk scoring 
            to provide accurate risk level assessments (Low / Medium / High) for skin lesions. 
            Monitor your skin health over time with comprehensive tracking and reporting.
          </p>
          <div class="hero-features">
            <div class="feature-item">
              <div class="feature-icon">🔬</div>
              <span>ML-Assisted Analysis</span>
            </div>
            <div class="feature-item">
              <div class="feature-icon">📊</div>
              <span>Risk Level Assessment</span>
            </div>
            <div class="feature-item">
              <div class="feature-icon">📈</div>
              <span>Long-term Monitoring</span>
            </div>
          </div>
          <div class="cta-buttons">
            <button class="cta primary" @click="$router.push('/dashboard')">
              <span>Get Started</span>
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M7.5 15L12.5 10L7.5 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
            <button class="cta secondary" @click="$router.push('/guide')">
              <span>Learn More</span>
            </button>
          </div>
        </div>
        <div class="hero-visual">
          <div class="visual-card">
            <div class="card-glow"></div>
            <div class="card-content">
              <div class="visual-header">
                <div class="visual-dots">
                  <span></span><span></span><span></span>
                </div>
                <span class="visual-title">Risk Assessment</span>
              </div>
              <div class="visual-body">
                <div class="risk-display">
                  <div class="risk-circle high">
                    <span class="risk-percentage">68%</span>
                    <span class="risk-label">High Risk</span>
                  </div>
                </div>
                <div class="visual-stats">
                  <div class="stat">
                    <span class="stat-value">Image Risk</span>
                    <span class="stat-label">72%</span>
                  </div>
                  <div class="stat">
                    <span class="stat-value">Support Risk</span>
                    <span class="stat-label">40%</span>
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
        <div class="disclaimer-icon">⚠️</div>
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
        <div class="feature-card" v-for="(feature, index) in features" :key="index">
          <div class="feature-card-icon">{{ feature.icon }}</div>
          <h3>{{ feature.title }}</h3>
          <p>{{ feature.description }}</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const handleGetStarted = () => {
  router.push("/dashboard");
};

const features = ref([
  {
    icon: "🧠",
    title: "AI-Powered Analysis",
    description: "Advanced DenseNet201 and Random Forest models for accurate risk probability estimation"
  },
  {
    icon: "📋",
    title: "Rule-Based Scoring",
    description: "Combines ML predictions with user inputs for comprehensive risk assessment"
  },
  {
    icon: "📊",
    title: "Risk Level Classification",
    description: "Clear Low / Medium / High risk categorization for easy understanding"
  },
  {
    icon: "📈",
    title: "Monitoring & Tracking",
    description: "Track your skin health over time with detailed history and trend analysis"
  },
  {
    icon: "📄",
    title: "Comprehensive Reports",
    description: "Generate and download detailed assessment reports with explanations"
  },
  {
    icon: "📖",
    title: "Educational Resources",
    description: "Learn about skin health, ABCDE rule, and self-examination techniques"
  }
]);
</script>

<style scoped>
.landing-container {
  width: 100%;
  animation: fadeIn 0.8s ease-out;
}

/* Hero Section */
.hero {
  position: relative;
  padding: var(--spacing-3xl) var(--spacing-lg);
  margin: calc(var(--spacing-xl) * -1) calc(var(--spacing-lg) * -1) var(--spacing-3xl);
  border-radius: var(--radius-xl);
  overflow: hidden;
  min-height: 600px;
  display: flex;
  align-items: center;
}

.hero-background {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, 
    rgba(0, 102, 204, 0.08) 0%, 
    rgba(0, 168, 150, 0.08) 50%,
    rgba(0, 102, 204, 0.05) 100%);
  z-index: 0;
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.6;
  animation: float 20s ease-in-out infinite;
}

.orb-1 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(0, 102, 204, 0.3) 0%, transparent 70%);
  top: -200px;
  left: -200px;
  animation-delay: 0s;
}

.orb-2 {
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(0, 168, 150, 0.3) 0%, transparent 70%);
  bottom: -150px;
  right: -150px;
  animation-delay: 7s;
}

.orb-3 {
  width: 250px;
  height: 250px;
  background: radial-gradient(circle, rgba(0, 102, 204, 0.2) 0%, transparent 70%);
  top: 50%;
  right: 10%;
  animation-delay: 14s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(30px, -30px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
}

.hero-content {
  position: relative;
  z-index: 1;
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-3xl);
  align-items: center;
  width: 100%;
}

.hero-text {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-md);
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 50px;
  font-size: 13px;
  font-weight: 600;
  color: var(--medical-blue);
  width: fit-content;
  box-shadow: var(--shadow-sm);
  border: 1px solid rgba(0, 102, 204, 0.1);
}

.badge-icon {
  font-size: 16px;
}

.hero-title {
  font-size: clamp(32px, 5vw, 56px);
  font-weight: 800;
  line-height: 1.1;
  color: var(--medical-gray-900);
  letter-spacing: -1px;
}

.gradient-text {
  background: linear-gradient(135deg, var(--medical-blue) 0%, var(--medical-teal) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-description {
  font-size: 18px;
  line-height: 1.7;
  color: var(--medical-gray-700);
  max-width: 600px;
}

.hero-features {
  display: flex;
  gap: var(--spacing-md);
  flex-wrap: wrap;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-md);
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 500;
  color: var(--medical-gray-700);
  border: 1px solid rgba(0, 102, 204, 0.1);
}

.feature-icon {
  font-size: 18px;
}

.cta-buttons {
  display: flex;
  gap: var(--spacing-md);
  flex-wrap: wrap;
}

.cta {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: 16px 32px;
  border: none;
  border-radius: var(--radius-md);
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-base);
  position: relative;
  overflow: hidden;
}

.cta.primary {
  background: linear-gradient(135deg, var(--medical-blue) 0%, var(--medical-teal) 100%);
  color: var(--medical-white);
  box-shadow: 0 4px 20px rgba(0, 102, 204, 0.3);
}

.cta.primary::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, var(--medical-blue-dark) 0%, var(--medical-teal-dark) 100%);
  opacity: 0;
  transition: opacity var(--transition-base);
}

.cta.primary:hover::before {
  opacity: 1;
}

.cta.primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 30px rgba(0, 102, 204, 0.4);
}

.cta.primary span,
.cta.primary svg {
  position: relative;
  z-index: 1;
}

.cta.secondary {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  color: var(--medical-blue);
  border: 2px solid var(--medical-blue);
  box-shadow: var(--shadow-sm);
}

.cta.secondary:hover {
  background: var(--medical-blue-light);
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
}

/* Hero Visual */
.hero-visual {
  display: flex;
  justify-content: center;
  align-items: center;
}

.visual-card {
  position: relative;
  width: 100%;
  max-width: 450px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: var(--radius-xl);
  padding: var(--spacing-xl);
  box-shadow: 0 20px 60px rgba(0, 102, 204, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.5);
  animation: slideIn 0.8s ease-out 0.2s both;
}

.card-glow {
  position: absolute;
  inset: -2px;
  background: linear-gradient(135deg, var(--medical-blue), var(--medical-teal));
  border-radius: var(--radius-xl);
  opacity: 0.3;
  filter: blur(20px);
  z-index: -1;
  animation: pulse 3s ease-in-out infinite;
}

.visual-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--spacing-lg);
  padding-bottom: var(--spacing-md);
  border-bottom: 1px solid var(--medical-gray-200);
}

.visual-dots {
  display: flex;
  gap: 6px;
}

.visual-dots span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--medical-gray-400);
}

.visual-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--medical-gray-700);
}

.visual-body {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.risk-display {
  display: flex;
  justify-content: center;
}

.risk-circle {
  width: 180px;
  height: 180px;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  box-shadow: inset 0 4px 20px rgba(0, 0, 0, 0.1);
}

.risk-circle.high {
  background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
  border: 4px solid var(--medical-red);
}

.risk-percentage {
  font-size: 36px;
  font-weight: 700;
  color: var(--medical-red);
}

.risk-label {
  font-size: 14px;
  font-weight: 600;
  color: var(--medical-red);
  margin-top: 4px;
}

.visual-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-md);
}

.stat {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: var(--spacing-md);
  background: var(--medical-gray-50);
  border-radius: var(--radius-md);
}

.stat-value {
  font-size: 12px;
  color: var(--medical-gray-600);
  font-weight: 500;
}

.stat-label {
  font-size: 20px;
  font-weight: 700;
  color: var(--medical-blue);
}

/* Disclaimer Section */
.disclaimer-section {
  margin: var(--spacing-3xl) 0;
}

.disclaimer-card {
  display: flex;
  gap: var(--spacing-lg);
  padding: var(--spacing-xl);
  background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
  border-radius: var(--radius-lg);
  border-left: 4px solid var(--medical-orange);
  box-shadow: var(--shadow-md);
  animation: fadeIn 0.8s ease-out 0.4s both;
}

.disclaimer-icon {
  font-size: 32px;
  flex-shrink: 0;
}

.disclaimer-content h3 {
  font-size: 18px;
  color: #e65100;
  margin-bottom: var(--spacing-sm);
  font-weight: 700;
}

.disclaimer-content p {
  font-size: 15px;
  color: #e65100;
  line-height: 1.7;
}

.disclaimer-content strong {
  font-weight: 700;
}

/* Features Section */
.features-section {
  margin: var(--spacing-3xl) 0;
}

.section-title {
  font-size: 36px;
  font-weight: 700;
  text-align: center;
  margin-bottom: var(--spacing-2xl);
  color: var(--medical-gray-900);
  background: linear-gradient(135deg, var(--medical-blue) 0%, var(--medical-teal) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-xl);
}

.feature-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  padding: var(--spacing-xl);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  border: 1px solid rgba(0, 102, 204, 0.1);
  transition: all var(--transition-base);
  animation: fadeIn 0.8s ease-out both;
}

.feature-card:nth-child(1) { animation-delay: 0.1s; }
.feature-card:nth-child(2) { animation-delay: 0.2s; }
.feature-card:nth-child(3) { animation-delay: 0.3s; }
.feature-card:nth-child(4) { animation-delay: 0.4s; }
.feature-card:nth-child(5) { animation-delay: 0.5s; }
.feature-card:nth-child(6) { animation-delay: 0.6s; }

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-xl);
  border-color: var(--medical-blue);
}

.feature-card-icon {
  font-size: 48px;
  margin-bottom: var(--spacing-md);
  display: block;
}

.feature-card h3 {
  font-size: 20px;
  color: var(--medical-gray-900);
  margin-bottom: var(--spacing-sm);
  font-weight: 700;
}

.feature-card p {
  font-size: 15px;
  color: var(--medical-gray-700);
  line-height: 1.7;
}

@media (max-width: 1024px) {
  .hero-content {
    grid-template-columns: 1fr;
    gap: var(--spacing-2xl);
  }

  .hero-visual {
    order: -1;
  }
}

@media (max-width: 768px) {
  .hero {
    padding: var(--spacing-xl) var(--spacing-md);
    min-height: auto;
  }

  .hero-title {
    font-size: 32px;
  }

  .hero-description {
    font-size: 16px;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .disclaimer-card {
    flex-direction: column;
    text-align: center;
  }
}
</style>
