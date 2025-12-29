<template>
  <div class="monitoring-container fade-in">
    <div class="page-header">
      <h1>Monitoring & History</h1>
      <p class="subtitle">Track your skin lesion assessments over time</p>
    </div>

    <div v-if="assessments.length === 0" class="empty-state">
      <div class="empty-icon">📋</div>
      <h2>No assessments yet</h2>
      <p>Start by creating a new risk assessment to track your skin health.</p>
      <button class="primary-button" @click="$router.push('/upload')">
        New Assessment
      </button>
    </div>

    <div v-else>
      <!-- Timeline View -->
      <div class="timeline-section">
        <h2>Assessment Timeline</h2>
        <div class="timeline">
          <div 
            v-for="(assessment, index) in sortedAssessments" 
            :key="assessment.id"
            class="timeline-item"
            @click="selectAssessment(assessment)"
          >
            <div class="timeline-marker" :class="`risk-${assessment.risk_level.toLowerCase()}`"></div>
            <div class="timeline-content">
              <div class="timeline-header">
                <span class="risk-badge-small" :class="`risk-${assessment.risk_level.toLowerCase()}`">
                  {{ assessment.risk_level }} Risk
                </span>
                <span class="timeline-date">{{ formatDate(assessment.timestamp) }}</span>
              </div>
              <div class="timeline-details">
                <div class="detail-item">
                  <span class="label">Final Risk:</span>
                  <span class="value">{{ assessment.final_risk_percentage }}</span>
                </div>
                <div class="detail-item">
                  <span class="label">Image Risk:</span>
                  <span class="value">{{ assessment.image_risk_percentage }}</span>
                </div>
                <div class="detail-item">
                  <span class="label">Support Risk:</span>
                  <span class="value">{{ assessment.support_risk_percentage }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Comparison View -->
      <div class="comparison-section" v-if="selectedAssessment && previousAssessment">
        <h2>Comparison View</h2>
        <div class="comparison-grid">
          <div class="comparison-card">
            <h3>Previous Assessment</h3>
            <div class="comparison-date">{{ formatDate(previousAssessment.timestamp) }}</div>
            <div class="comparison-risk" :class="`risk-${previousAssessment.risk_level.toLowerCase()}`">
              {{ previousAssessment.risk_level }} Risk
            </div>
            <div class="comparison-score">{{ previousAssessment.final_risk_percentage }}</div>
          </div>

          <div class="comparison-arrow">→</div>

          <div class="comparison-card">
            <h3>Current Assessment</h3>
            <div class="comparison-date">{{ formatDate(selectedAssessment.timestamp) }}</div>
            <div class="comparison-risk" :class="`risk-${selectedAssessment.risk_level.toLowerCase()}`">
              {{ selectedAssessment.risk_level }} Risk
            </div>
            <div class="comparison-score">{{ selectedAssessment.final_risk_percentage }}</div>
          </div>
        </div>

        <div class="trend-indicator">
          <span class="trend-icon">{{ getTrendIcon() }}</span>
          <span class="trend-text">{{ getTrendText() }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import api from "@/api/client";

const assessments = ref([]);
const selectedAssessment = ref(null);

const sortedAssessments = computed(() => {
  return [...assessments.value].sort((a, b) => 
    new Date(b.timestamp) - new Date(a.timestamp)
  );
});

const previousAssessment = computed(() => {
  if (!selectedAssessment.value) return null;
  const currentIndex = sortedAssessments.value.findIndex(
    a => a.id === selectedAssessment.value.id
  );
  if (currentIndex < sortedAssessments.value.length - 1) {
    return sortedAssessments.value[currentIndex + 1];
  }
  return null;
});

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString("en-US", { 
    year: "numeric",
    month: "long", 
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit"
  });
};

const selectAssessment = (assessment) => {
  selectedAssessment.value = assessment;
};

const getTrendIcon = () => {
  if (!selectedAssessment.value || !previousAssessment.value) return "➡️";
  const current = selectedAssessment.value.final_risk_score;
  const previous = previousAssessment.value.final_risk_score;
  if (current > previous) return "📈";
  if (current < previous) return "📉";
  return "➡️";
};

const getTrendText = () => {
  if (!selectedAssessment.value || !previousAssessment.value) return "No comparison available";
  const current = selectedAssessment.value.final_risk_score;
  const previous = previousAssessment.value.final_risk_score;
  const diff = Math.abs(current - previous).toFixed(1);
  if (current > previous) return `Risk increased by ${diff}%`;
  if (current < previous) return `Risk decreased by ${diff}%`;
  return "Risk level unchanged";
};

const loadAssessments = async () => {
  try {
    const response = await api.get("/assessments");
    if (response.data && response.data.success) {
      assessments.value = response.data.assessments || [];
      if (assessments.value.length > 0) {
        selectedAssessment.value = sortedAssessments.value[0];
      }
    }
  } catch (error) {
    console.error("Failed to load assessments:", error);
  }
};

onMounted(() => {
  loadAssessments();
});
</script>

<style scoped>
.monitoring-container {
  width: 100%;
  padding: 0;
}

.page-header {
  margin-bottom: 40px;
}

.page-header h1 {
  font-size: 42px;
  color: var(--medical-gray-900);
  margin-bottom: var(--spacing-sm);
  font-weight: 800;
  background: linear-gradient(135deg, var(--medical-blue) 0%, var(--medical-teal) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -1px;
}

.subtitle {
  font-size: 18px;
  color: var(--medical-gray-600);
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
  background: var(--medical-white);
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 102, 204, 0.1);
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 24px;
}

.empty-state h2 {
  font-size: 24px;
  color: var(--medical-gray-900);
  margin-bottom: 12px;
}

.empty-state p {
  font-size: 16px;
  color: var(--medical-gray-600);
  margin-bottom: 32px;
}

.primary-button {
  padding: 14px 32px;
  background: linear-gradient(135deg, var(--medical-blue) 0%, var(--medical-teal) 100%);
  color: var(--medical-white);
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.primary-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 102, 204, 0.3);
}

.timeline-section {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: var(--radius-xl);
  padding: var(--spacing-2xl);
  margin-bottom: var(--spacing-2xl);
  box-shadow: 0 8px 32px rgba(0, 102, 204, 0.12);
  border: 1px solid rgba(0, 102, 204, 0.1);
  animation: slideIn 0.6s ease-out;
}

.timeline-section h2 {
  font-size: 24px;
  color: var(--medical-gray-900);
  margin-bottom: 24px;
  font-weight: 700;
}

.timeline {
  position: relative;
  padding-left: 32px;
}

.timeline::before {
  content: "";
  position: absolute;
  left: 11px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: var(--medical-gray-300);
}

.timeline-item {
  position: relative;
  margin-bottom: 24px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.timeline-item:hover {
  transform: translateX(4px);
}

.timeline-marker {
  position: absolute;
  left: -21px;
  top: 8px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 3px solid var(--medical-white);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.timeline-marker.risk-high {
  background: var(--medical-red);
}

.timeline-marker.risk-medium {
  background: #ff9800;
}

.timeline-marker.risk-low {
  background: #4caf50;
}

.timeline-content {
  background: var(--medical-gray-50);
  border-radius: 12px;
  padding: 20px;
  border-left: 4px solid var(--medical-gray-300);
}

.timeline-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.risk-badge-small {
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

.risk-badge-small.risk-high {
  background: #ffebee;
  color: var(--medical-red);
}

.risk-badge-small.risk-medium {
  background: #fff3e0;
  color: #f57c00;
}

.risk-badge-small.risk-low {
  background: #e8f5e9;
  color: #388e3c;
}

.timeline-date {
  font-size: 14px;
  color: var(--medical-gray-600);
}

.timeline-details {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
}

.detail-item {
  display: flex;
  gap: 8px;
}

.detail-item .label {
  font-size: 14px;
  color: var(--medical-gray-600);
}

.detail-item .value {
  font-size: 14px;
  color: var(--medical-gray-900);
  font-weight: 600;
}

.comparison-section {
  background: var(--medical-white);
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 4px 16px rgba(0, 102, 204, 0.1);
}

.comparison-section h2 {
  font-size: 24px;
  color: var(--medical-gray-900);
  margin-bottom: 24px;
  font-weight: 700;
}

.comparison-grid {
  display: flex;
  align-items: center;
  gap: 24px;
  margin-bottom: 24px;
}

.comparison-card {
  flex: 1;
  background: var(--medical-gray-50);
  border-radius: 12px;
  padding: 24px;
  text-align: center;
}

.comparison-card h3 {
  font-size: 18px;
  color: var(--medical-gray-700);
  margin-bottom: 8px;
  font-weight: 600;
}

.comparison-date {
  font-size: 14px;
  color: var(--medical-gray-600);
  margin-bottom: 16px;
}

.comparison-risk {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 8px;
  padding: 8px 16px;
  border-radius: 8px;
  display: inline-block;
}

.comparison-risk.risk-high {
  background: #ffebee;
  color: var(--medical-red);
}

.comparison-risk.risk-medium {
  background: #fff3e0;
  color: #f57c00;
}

.comparison-risk.risk-low {
  background: #e8f5e9;
  color: #388e3c;
}

.comparison-score {
  font-size: 24px;
  color: var(--medical-gray-900);
  font-weight: 700;
}

.comparison-arrow {
  font-size: 32px;
  color: var(--medical-blue);
}

.trend-indicator {
  text-align: center;
  padding: 16px;
  background: var(--medical-gray-50);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.trend-icon {
  font-size: 24px;
}

.trend-text {
  font-size: 16px;
  color: var(--medical-gray-700);
  font-weight: 600;
}

@media (max-width: 768px) {
  .comparison-grid {
    flex-direction: column;
  }

  .comparison-arrow {
    transform: rotate(90deg);
  }
}
</style>

