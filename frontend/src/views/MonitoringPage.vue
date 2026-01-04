<template>
  <div class="monitoring-container fade-in">
    <div class="page-header">
      <h1>Monitoring & History</h1>
      <p class="subtitle">Track your skin lesion assessments over time</p>
    </div>

    <div v-if="assessments.length === 0" class="empty-state">
      <svg class="empty-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
      </svg>
      <h2>No assessments yet</h2>
      <p>Start by creating a new risk assessment to track your skin health.</p>
      <button class="primary-button" @click="$router.push('/upload')">
        <svg class="btn-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
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

          <div class="comparison-arrow">
            <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </div>

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
          <svg class="trend-icon" :class="getTrendClass()" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="getTrendIconPath()" />
          </svg>
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

const getTrendClass = () => {
  if (!selectedAssessment.value || !previousAssessment.value) return "trend-neutral";
  const current = selectedAssessment.value.final_risk_score;
  const previous = previousAssessment.value.final_risk_score;
  if (current > previous) return "trend-up";
  if (current < previous) return "trend-down";
  return "trend-neutral";
};

const getTrendIconPath = () => {
  if (!selectedAssessment.value || !previousAssessment.value) return "M13 7h8m0 0v8m0-8l-8 8-4-4-6 6";
  const current = selectedAssessment.value.final_risk_score;
  const previous = previousAssessment.value.final_risk_score;
  if (current > previous) return "M13 17h8m0 0V9m0 8l-8-8-4 4-6-6";
  if (current < previous) return "M13 7h8m0 0v8m0-8l-8 8-4-4-6 6";
  return "M13 7h8m0 0v8m0-8l-8 8-4-4-6 6";
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
  margin-bottom: 2.5rem;
}

.page-header h1 {
  font-size: 2.75rem;
  color: #1e293b;
  margin-bottom: 0.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #2563eb 0%, #06b6d4 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -1px;
}

.subtitle {
  font-size: 1.125rem;
  color: #64748b;
}

.empty-state {
  text-align: center;
  padding: 5rem 1.25rem;
  background: white;
  border-radius: 1.25rem;
  box-shadow: 0 4px 16px rgba(37, 99, 235, 0.08);
}

.empty-icon {
  width: 5rem;
  height: 5rem;
  margin: 0 auto 1.5rem;
  stroke: #94a3b8;
  stroke-width: 1.5;
}

.empty-state h2 {
  font-size: 1.5rem;
  color: #1e293b;
  margin-bottom: 0.75rem;
}

.empty-state p {
  font-size: 1rem;
  color: #64748b;
  margin-bottom: 2rem;
}

.primary-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #2563eb 0%, #06b6d4 100%);
  color: white;
  border: none;
  border-radius: 0.75rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 16px rgba(37, 99, 235, 0.3);
}

.primary-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
}

.btn-icon {
  width: 1.25rem;
  height: 1.25rem;
  stroke-width: 2.5;
}

.timeline-section {
  background: white;
  border-radius: 1.25rem;
  padding: 2rem;
  margin-bottom: 2.5rem;
  box-shadow: 0 4px 20px rgba(37, 99, 235, 0.08);
  border: 1px solid #e2e8f0;
  animation: slideIn 0.6s ease-out;
}

.timeline-section h2 {
  font-size: 1.5rem;
  color: #1e293b;
  margin-bottom: 1.5rem;
  font-weight: 700;
}

.timeline {
  position: relative;
  padding-left: 2rem;
}

.timeline::before {
  content: "";
  position: absolute;
  left: 0.6875rem;
  top: 0;
  bottom: 0;
  width: 2px;
  background: #e2e8f0;
}

.timeline-item {
  position: relative;
  margin-bottom: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.timeline-item:hover {
  transform: translateX(4px);
}

.timeline-marker {
  position: absolute;
  left: -1.3125rem;
  top: 0.5rem;
  width: 1.25rem;
  height: 1.25rem;
  border-radius: 50%;
  border: 3px solid white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.timeline-marker.risk-high {
  background: #ef4444;
}

.timeline-marker.risk-medium {
  background: #f97316;
}

.timeline-marker.risk-low {
  background: #22c55e;
}

.timeline-content {
  background: #f8fafc;
  border-radius: 0.75rem;
  padding: 1.25rem;
  border-left: 4px solid #cbd5e1;
}

.timeline-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.risk-badge-small {
  padding: 0.375rem 0.75rem;
  border-radius: 0.375rem;
  font-size: 0.75rem;
  font-weight: 600;
}

.risk-badge-small.risk-high {
  background: #fee2e2;
  color: #dc2626;
}

.risk-badge-small.risk-medium {
  background: #ffedd5;
  color: #ea580c;
}

.risk-badge-small.risk-low {
  background: #dcfce7;
  color: #16a34a;
}

.timeline-date {
  font-size: 0.875rem;
  color: #64748b;
}

.timeline-details {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.detail-item {
  display: flex;
  gap: 0.5rem;
}

.detail-item .label {
  font-size: 0.875rem;
  color: #64748b;
}

.detail-item .value {
  font-size: 0.875rem;
  color: #1e293b;
  font-weight: 600;
}

.comparison-section {
  background: white;
  border-radius: 1.25rem;
  padding: 2rem;
  box-shadow: 0 4px 16px rgba(37, 99, 235, 0.08);
}

.comparison-section h2 {
  font-size: 1.5rem;
  color: #1e293b;
  margin-bottom: 1.5rem;
  font-weight: 700;
}

.comparison-grid {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.comparison-card {
  flex: 1;
  background: #f8fafc;
  border-radius: 0.75rem;
  padding: 1.5rem;
  text-align: center;
}

.comparison-card h3 {
  font-size: 1.125rem;
  color: #475569;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.comparison-date {
  font-size: 0.875rem;
  color: #64748b;
  margin-bottom: 1rem;
}

.comparison-risk {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  display: inline-block;
}

.comparison-risk.risk-high {
  background: #fee2e2;
  color: #dc2626;
}

.comparison-risk.risk-medium {
  background: #ffedd5;
  color: #ea580c;
}

.comparison-risk.risk-low {
  background: #dcfce7;
  color: #16a34a;
}

.comparison-score {
  font-size: 1.5rem;
  color: #1e293b;
  font-weight: 700;
}

.comparison-arrow {
  display: flex;
  align-items: center;
  justify-content: center;
}

.comparison-arrow svg {
  width: 2rem;
  height: 2rem;
  stroke: #2563eb;
  stroke-width: 2.5;
}

.trend-indicator {
  text-align: center;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
}

.trend-icon {
  width: 1.5rem;
  height: 1.5rem;
  stroke-width: 2.5;
}

.trend-icon.trend-up {
  stroke: #dc2626;
}

.trend-icon.trend-down {
  stroke: #16a34a;
}

.trend-icon.trend-neutral {
  stroke: #64748b;
}

.trend-text {
  font-size: 1rem;
  color: #475569;
  font-weight: 600;
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

@media (max-width: 768px) {
  .comparison-grid {
    flex-direction: column;
  }

  .comparison-arrow {
    transform: rotate(90deg);
  }
}
</style>