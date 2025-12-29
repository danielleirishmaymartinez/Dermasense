<template>
  <section class="result-page fade-in">
    <div v-if="errorMessage" class="error-card">
      <div class="error-icon">⚠️</div>
      <h2>Assessment Error</h2>
      <p class="error-message">{{ errorMessage }}</p>
      <div class="error-actions">
        <button class="retry-button primary" @click="$router.push('/upload')">
          Try Again
        </button>
        <button class="retry-button secondary" @click="$router.push('/dashboard')">
          Go to Dashboard
        </button>
      </div>
    </div>

    <div v-else-if="!result" class="empty-message">
      No analysis result found. Please start a new assessment.
      <button class="retry-button" @click="$router.push('/upload')">
        New Assessment
      </button>
    </div>

    <div v-else class="result-card">
      <h1>Risk Assessment Results</h1>

      <!-- Risk Level Badge -->
      <div class="risk-header">
        <div class="risk-badge-large" :class="`risk-${result.risk_level?.toLowerCase()}`">
          <span class="risk-icon">{{ getRiskIcon(result.risk_level) }}</span>
          <div class="risk-info">
            <div class="risk-level-text">{{ result.risk_level }} Risk</div>
            <div class="risk-percentage">{{ result.final_risk_percentage }}</div>
          </div>
        </div>
      </div>

      <div class="result-content">
        <div class="image-section" v-if="imageUrl">
          <img :src="imageUrl" alt="Assessed Image" class="result-image" />
        </div>

        <div class="details-section">
          <!-- Risk Breakdown -->
          <div class="risk-breakdown">
            <h3>Risk Breakdown</h3>
            <div class="breakdown-item">
              <span class="label">Image-Based Risk:</span>
              <span class="value">{{ result.image_risk_percentage }}</span>
            </div>
            <div class="breakdown-item">
              <span class="label">Support Risk (User Inputs):</span>
              <span class="value">{{ result.support_risk_percentage }}</span>
            </div>
            <div class="breakdown-item final">
              <span class="label">Final Risk Score:</span>
              <span class="value final-value">{{ result.final_risk_percentage }}</span>
            </div>
          </div>

          <!-- Explanations -->
          <div class="explanations-section">
            <h3>Assessment Explanations</h3>
            <ul class="explanations-list">
              <li v-for="(explanation, index) in result.explanations" :key="index">
                {{ explanation }}
              </li>
            </ul>
          </div>

          <!-- Recommendations -->
          <div class="recommendations-section">
            <h3>Recommendations</h3>
            <p class="recommendation-text">{{ result.recommendation }}</p>
          </div>

          <!-- Disclaimer -->
          <div class="disclaimer-box">
            <strong>⚠️ Important Disclaimer:</strong>
            <p>{{ result.disclaimer || "This system is for risk assessment only and not a medical diagnosis. Always consult a dermatologist for professional evaluation." }}</p>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="action-buttons">
        <button class="action-btn secondary" @click="$router.push('/monitoring')">
          View History
        </button>
        <button class="action-btn secondary" @click="$router.push('/reports')">
          Generate Report
        </button>
        <button class="action-btn primary" @click="$router.push('/upload')">
          New Assessment
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";

const result = ref(null);
const imageUrl = ref("");
const errorMessage = ref("");

const getRiskIcon = (level) => {
  if (!level) return "❓";
  if (level === "HIGH") return "🔴";
  if (level === "MEDIUM") return "🟡";
  return "🟢";
};

onMounted(() => {
  const stored = localStorage.getItem("assessmentResult");
  const error = localStorage.getItem("assessmentError");
  
  if (error) {
    errorMessage.value = error;
    localStorage.removeItem("assessmentError");
    return;
  }

  if (!stored) {
    errorMessage.value = "No analysis result available. Please upload an image first.";
    return;
  }

  try {
    const parsed = JSON.parse(stored);
    
    // Check if it's a successful result
    if (parsed.success === false) {
      errorMessage.value = parsed.message || "Assessment failed. Please try again.";
      return;
    }
    
    result.value = parsed;
    imageUrl.value = localStorage.getItem("assessmentImage") || "";
    
    console.log("Result loaded:", result.value);
  } catch (e) {
    errorMessage.value = "Failed to parse assessment result.";
    console.error("Parse error:", e);
  }
});
</script>

<style scoped>
.result-page {
  width: 100%;
  padding: 0;
  min-height: calc(100vh - 200px);
}

.result-card {
  width: 100%;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: var(--radius-xl);
  padding: var(--spacing-2xl);
  box-shadow: 0 12px 40px rgba(0, 102, 204, 0.15);
  border: 1px solid rgba(0, 102, 204, 0.1);
  animation: slideIn 0.6s ease-out;
}

.result-card h1 {
  font-size: 42px;
  margin-bottom: var(--spacing-2xl);
  color: var(--medical-gray-900);
  font-weight: 800;
  text-align: center;
  border-bottom: 3px solid var(--medical-blue);
  padding-bottom: var(--spacing-lg);
  background: linear-gradient(135deg, var(--medical-blue) 0%, var(--medical-teal) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -1px;
}

.risk-header {
  display: flex;
  justify-content: center;
  margin-bottom: 40px;
}

.risk-badge-large {
  display: flex;
  align-items: center;
  gap: var(--spacing-xl);
  padding: var(--spacing-2xl) var(--spacing-3xl);
  border-radius: var(--radius-xl);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
  position: relative;
  overflow: hidden;
}

.risk-badge-large::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.3) 0%, transparent 70%);
  pointer-events: none;
}

.risk-badge-large.risk-high {
  background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
  border: 3px solid var(--medical-red);
}

.risk-badge-large.risk-medium {
  background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
  border: 3px solid #ff9800;
}

.risk-badge-large.risk-low {
  background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
  border: 3px solid #4caf50;
}

.risk-icon {
  font-size: 72px;
  filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.15));
  animation: pulse 2s ease-in-out infinite;
}

.risk-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.risk-level-text {
  font-size: 32px;
  font-weight: 700;
  color: var(--medical-gray-900);
}

.risk-percentage {
  font-size: 24px;
  color: var(--medical-gray-700);
  font-weight: 600;
}

.result-content {
  display: flex;
  gap: 40px;
  margin-bottom: 32px;
  align-items: flex-start;
}

.image-section {
  flex: 1;
  max-width: 400px;
}

.result-image {
  width: 100%;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  background-color: var(--medical-gray-50);
  object-fit: cover;
  border: 3px solid var(--medical-blue-light);
}

.details-section {
  flex: 1.5;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.risk-breakdown,
.explanations-section,
.recommendations-section {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, var(--medical-gray-50) 100%);
  backdrop-filter: blur(10px);
  border-radius: var(--radius-lg);
  padding: var(--spacing-xl);
  border-left: 4px solid var(--medical-blue);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-base);
}

.risk-breakdown:hover,
.explanations-section:hover,
.recommendations-section:hover {
  transform: translateX(4px);
  box-shadow: var(--shadow-md);
}

.risk-breakdown h3,
.explanations-section h3,
.recommendations-section h3 {
  font-size: 20px;
  color: var(--medical-gray-900);
  margin-bottom: 16px;
  font-weight: 600;
}

.breakdown-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid var(--medical-gray-200);
}

.breakdown-item:last-child {
  border-bottom: none;
}

.breakdown-item.final {
  margin-top: 8px;
  padding-top: 16px;
  border-top: 2px solid var(--medical-blue);
  border-bottom: none;
}

.breakdown-item .label {
  font-size: 15px;
  color: var(--medical-gray-700);
}

.breakdown-item .value {
  font-size: 18px;
  color: var(--medical-gray-900);
  font-weight: 600;
}

.breakdown-item .value.final-value {
  font-size: 24px;
  color: var(--medical-blue);
  font-weight: 700;
}

.explanations-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.explanations-list li {
  padding: 12px 0;
  padding-left: 24px;
  position: relative;
  font-size: 15px;
  color: var(--medical-gray-700);
  line-height: 1.6;
}

.explanations-list li::before {
  content: "✓";
  position: absolute;
  left: 0;
  color: var(--medical-blue);
  font-weight: 700;
}

.recommendation-text {
  font-size: 16px;
  color: var(--medical-gray-700);
  line-height: 1.8;
  margin: 0;
}

.disclaimer-box {
  background: linear-gradient(135deg, var(--medical-red-light) 0%, #FFE5E5 100%);
  border-radius: 12px;
  padding: 20px;
  border-left: 4px solid var(--medical-red);
  margin-top: 8px;
}

.disclaimer-box strong {
  font-size: 16px;
  color: var(--medical-red);
  display: block;
  margin-bottom: 8px;
}

.disclaimer-box p {
  font-size: 14px;
  color: #c62828;
  line-height: 1.7;
  margin: 0;
}

.action-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-top: 32px;
}

.action-btn {
  padding: 14px 32px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn.primary {
  background: linear-gradient(135deg, var(--medical-blue) 0%, var(--medical-teal) 100%);
  color: var(--medical-white);
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
}

.action-btn.primary:hover {
  background: linear-gradient(135deg, var(--medical-blue-dark) 0%, var(--medical-teal-dark) 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 102, 204, 0.4);
}

.action-btn.secondary {
  background: var(--medical-white);
  color: var(--medical-blue);
  border: 2px solid var(--medical-blue);
}

.action-btn.secondary:hover {
  background: var(--medical-blue-light);
  transform: translateY(-2px);
}

.error-card,
.empty-message {
  width: 100%;
  max-width: 700px;
  margin: 40px auto;
  text-align: center;
  padding: 40px;
  background-color: var(--medical-white);
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  border: 1px solid var(--medical-gray-200);
}

.error-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.error-card h2 {
  font-size: 24px;
  color: var(--medical-gray-900);
  margin-bottom: 16px;
}

.error-card .error-message,
.empty-message {
  font-size: 16px;
  color: var(--medical-gray-700);
  margin-bottom: 24px;
  line-height: 1.6;
  word-wrap: break-word;
}

.error-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}

.retry-button {
  padding: 12px 32px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.retry-button.primary {
  background: linear-gradient(135deg, var(--medical-blue) 0%, var(--medical-teal) 100%);
  color: var(--medical-white);
}

.retry-button.secondary {
  background: var(--medical-gray-200);
  color: var(--medical-gray-900);
}

.retry-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 102, 204, 0.3);
}

.retry-button.secondary:hover {
  background: var(--medical-gray-300);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

@media (max-width: 900px) {
  .result-card {
    padding: 30px 24px 36px;
  }

  .result-content {
    flex-direction: column;
    gap: 30px;
  }

  .image-section {
    max-width: 100%;
  }

  .risk-badge-large {
    flex-direction: column;
    padding: 24px;
    text-align: center;
  }

  .action-buttons {
    flex-direction: column;
  }
}
</style>
