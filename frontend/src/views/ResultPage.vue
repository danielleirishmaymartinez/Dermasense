<template>
  <section class="result-page fade-in">
    <div v-if="errorMessage" class="error-card">
      <svg class="error-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <h2>Assessment Error</h2>
      <p class="error-message">{{ errorMessage }}</p>
      <div class="error-actions">
        <button class="retry-button primary" @click="$router.push('/upload')">
          <svg class="btn-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Try Again
        </button>
        <button class="retry-button secondary" @click="$router.push('/dashboard')">
          <svg class="btn-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
          </svg>
          Go to Dashboard
        </button>
      </div>
    </div>

    <div v-else-if="!result" class="empty-message">
      <svg class="empty-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      <p>No analysis result found. Please start a new assessment.</p>
      <button class="retry-button primary" @click="$router.push('/upload')">
        <svg class="btn-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        New Assessment
      </button>
    </div>

    <div v-else class="result-card">
      <h1>Risk Assessment Results</h1>

      <div class="result-content">
        <!-- Left Side: Image and Risk Badge -->
        <div class="image-section" v-if="imageUrl">
          <img :src="imageUrl" alt="Assessed Image" class="result-image" />
          <div class="image-label">Analyzed Image</div>
          
          <!-- Risk Badge Below Image -->
          <div class="risk-badge-container">
            <div class="risk-badge-large" :class="`risk-${result.risk_level?.toLowerCase()}`">
              <div class="risk-icon-circle" :class="`risk-${result.risk_level?.toLowerCase()}`">
                <svg v-if="result.risk_level === 'HIGH'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                <svg v-else-if="result.risk_level === 'MEDIUM'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                <svg v-else fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="risk-info">
                <div class="risk-level-text">{{ result.risk_level }} Risk</div>
                <div class="risk-percentage">{{ result.final_risk_percentage }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Side: Details -->
        <div class="details-section">
          <!-- Risk Breakdown -->
          <div class="risk-breakdown">
            <div class="breakdown-header">
              <svg class="section-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              <h3>Risk Breakdown</h3>
            </div>
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
            <div class="breakdown-header">
              <svg class="section-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <h3>Assessment Explanations</h3>
            </div>
            <ul class="explanations-list">
              <li v-for="(explanation, index) in result.explanations" :key="index">
                {{ explanation }}
              </li>
            </ul>
          </div>

          <!-- Recommendations -->
          <div class="recommendations-section">
            <div class="breakdown-header">
              <svg class="section-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
              </svg>
              <h3>Recommendations</h3>
            </div>
            <p class="recommendation-text">{{ result.recommendation }}</p>
          </div>

          <!-- Disclaimer -->
          <div class="disclaimer-box">
            <svg class="disclaimer-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <div>
              <strong>Important Disclaimer</strong>
              <p>{{ result.disclaimer || "This system is for risk assessment only and not a medical diagnosis. Always consult a dermatologist for professional evaluation." }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="action-buttons">
        <button class="action-btn secondary" @click="$router.push('/monitoring')">
          <svg class="btn-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          View History
        </button>
        <button class="action-btn secondary" @click="$router.push('/reports')">
          <svg class="btn-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          Generate Report
        </button>
        <button class="action-btn primary" @click="$router.push('/upload')">
          <svg class="btn-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
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
  background: white;
  border-radius: 1.25rem;
  padding: 2.5rem;
  box-shadow: 0 12px 40px rgba(37, 99, 235, 0.12);
  border: 1px solid #e2e8f0;
  animation: slideIn 0.6s ease-out;
}

.result-card h1 {
  font-size: 2.75rem;
  margin-bottom: 2.5rem;
  color: #1e293b;
  font-weight: 800;
  text-align: center;
  border-bottom: 3px solid #2563eb;
  padding-bottom: 1.25rem;
  background: linear-gradient(135deg, #2563eb 0%, #06b6d4 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -1px;
}

.result-content {
  display: flex;
  gap: 2.5rem;
  margin-bottom: 2rem;
  align-items: flex-start;
}

.image-section {
  flex: 1;
  max-width: 420px;
  display: flex;
  flex-direction: column;
}

.result-image {
  width: 100%;
  border-radius: 0.75rem;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  background-color: #f8fafc;
  object-fit: cover;
  border: 3px solid #dbeafe;
  margin-bottom: 0.75rem;
}

.image-label {
  text-align: center;
  margin-bottom: 1.5rem;
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 500;
}

.risk-badge-container {
  margin-top: 1rem;
}

.risk-badge-large {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  padding: 1.5rem;
  border-radius: 1rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
  position: relative;
  overflow: hidden;
  animation: fadeIn 0.8s ease-out 0.3s both;
}

.risk-badge-large::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.3) 0%, transparent 70%);
  pointer-events: none;
}

.risk-badge-large.risk-high {
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  border: 3px solid #dc2626;
}

.risk-badge-large.risk-medium {
  background: linear-gradient(135deg, #ffedd5 0%, #fed7aa 100%);
  border: 3px solid #f97316;
}

.risk-badge-large.risk-low {
  background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
  border: 3px solid #22c55e;
}

.risk-icon-circle {
  width: 3.5rem;
  height: 3.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  flex-shrink: 0;
}

.risk-icon-circle.risk-high {
  background: linear-gradient(135deg, #fee2e2, #fca5a5);
  border: 3px solid #dc2626;
}

.risk-icon-circle.risk-medium {
  background: linear-gradient(135deg, #ffedd5, #fdba74);
  border: 3px solid #f97316;
}

.risk-icon-circle.risk-low {
  background: linear-gradient(135deg, #dcfce7, #86efac);
  border: 3px solid #22c55e;
}

.risk-icon-circle svg {
  width: 2rem;
  height: 2rem;
  stroke-width: 2;
}

.risk-icon-circle.risk-high svg {
  stroke: #dc2626;
}

.risk-icon-circle.risk-medium svg {
  stroke: #f97316;
}

.risk-icon-circle.risk-low svg {
  stroke: #22c55e;
}

.risk-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.risk-level-text {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  line-height: 1;
}

.risk-percentage {
  font-size: 1.25rem;
  color: #475569;
  font-weight: 600;
}

.details-section {
  flex: 1.5;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.risk-breakdown,
.explanations-section,
.recommendations-section {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, #f8fafc 100%);
  border-radius: 0.75rem;
  padding: 1.5rem;
  border-left: 4px solid #2563eb;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.risk-breakdown:hover,
.explanations-section:hover,
.recommendations-section:hover {
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.breakdown-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.section-icon {
  width: 1.5rem;
  height: 1.5rem;
  stroke: #2563eb;
  stroke-width: 2;
}

.breakdown-header h3,
.explanations-section h3,
.recommendations-section h3 {
  font-size: 1.25rem;
  color: #1e293b;
  font-weight: 600;
  margin: 0;
}

.breakdown-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.875rem 0;
  border-bottom: 1px solid #e2e8f0;
}

.breakdown-item:last-child {
  border-bottom: none;
}

.breakdown-item.final {
  margin-top: 0.5rem;
  padding-top: 1rem;
  border-top: 2px solid #2563eb;
  border-bottom: none;
}

.breakdown-item .label {
  font-size: 0.9375rem;
  color: #475569;
}

.breakdown-item .value {
  font-size: 1.125rem;
  color: #1e293b;
  font-weight: 600;
}

.breakdown-item .value.final-value {
  font-size: 1.5rem;
  color: #2563eb;
  font-weight: 700;
}

.explanations-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.explanations-list li {
  padding: 0.875rem 0;
  padding-left: 1.75rem;
  position: relative;
  font-size: 0.9375rem;
  color: #475569;
  line-height: 1.6;
  border-bottom: 1px solid #f1f5f9;
}

.explanations-list li:last-child {
  border-bottom: none;
}

.explanations-list li::before {
  content: "";
  position: absolute;
  left: 0;
  top: 1.125rem;
  width: 0.5rem;
  height: 0.5rem;
  background: #2563eb;
  border-radius: 50%;
}

.recommendation-text {
  font-size: 1rem;
  color: #475569;
  line-height: 1.8;
  margin: 0;
}

.disclaimer-box {
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  border-radius: 0.75rem;
  padding: 1.25rem;
  border-left: 4px solid #dc2626;
  margin-top: 0.5rem;
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.disclaimer-icon {
  width: 1.5rem;
  height: 1.5rem;
  flex-shrink: 0;
  stroke: #dc2626;
  stroke-width: 2;
  margin-top: 0.125rem;
}

.disclaimer-box strong {
  font-size: 1rem;
  color: #991b1b;
  display: block;
  margin-bottom: 0.5rem;
}

.disclaimer-box p {
  font-size: 0.875rem;
  color: #991b1b;
  line-height: 1.7;
  margin: 0;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
  flex-wrap: wrap;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 2rem;
  border: none;
  border-radius: 0.75rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn.primary {
  background: linear-gradient(135deg, #2563eb 0%, #06b6d4 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

.action-btn.primary:hover {
  background: linear-gradient(135deg, #1d4ed8 0%, #0891b2 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
}

.action-btn.secondary {
  background: white;
  color: #2563eb;
  border: 2px solid #2563eb;
}

.action-btn.secondary:hover {
  background: #eff6ff;
  transform: translateY(-2px);
}

.btn-icon {
  width: 1.25rem;
  height: 1.25rem;
  stroke-width: 2.5;
}

.error-card,
.empty-message {
  width: 100%;
  max-width: 700px;
  margin: 2.5rem auto;
  text-align: center;
  padding: 3rem 2.5rem;
  background-color: white;
  border-radius: 1.25rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  border: 1px solid #e2e8f0;
}

.error-icon,
.empty-icon {
  width: 5rem;
  height: 5rem;
  margin: 0 auto 1.5rem;
  stroke: #ef4444;
  stroke-width: 1.5;
}

.empty-icon {
  stroke: #94a3b8;
}

.error-card h2 {
  font-size: 1.5rem;
  color: #1e293b;
  margin-bottom: 1rem;
}

.error-card .error-message,
.empty-message p {
  font-size: 1rem;
  color: #475569;
  margin-bottom: 1.5rem;
  line-height: 1.6;
  word-wrap: break-word;
}

.error-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: center;
  flex-wrap: wrap;
}

.retry-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 2rem;
  border: none;
  border-radius: 0.75rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.retry-button.primary {
  background: linear-gradient(135deg, #2563eb 0%, #06b6d4 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

.retry-button.secondary {
  background: #f1f5f9;
  color: #1e293b;
}

.retry-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(37, 99, 235, 0.3);
}

.retry-button.secondary:hover {
  background: #e2e8f0;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@media (max-width: 900px) {
  .result-card {
    padding: 2rem 1.5rem;
  }

  .result-content {
    flex-direction: column;
    gap: 2rem;
  }

  .image-section {
    max-width: 100%;
  }

  .action-buttons {
    flex-direction: column;
  }

  .result-card h1 {
    font-size: 2rem;
  }
}
</style>