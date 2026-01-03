<template>
  <div class="dashboard-container fade-in">
    <div class="dashboard-header">
      <div class="header-content">
        <h1>Dashboard</h1>
        <p class="subtitle">Welcome to DermaSense Risk Assessment System</p>
      </div>
      <div class="header-actions">
        <button class="action-button primary" @click="$router.push('/upload')">
          <svg class="btn-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          <span>New Assessment</span>
        </button>
      </div>
    </div>

    <!-- Quick Status Card -->
    <div class="status-card" v-if="latestAssessment">
      <div class="status-header">
        <h2>Latest Risk Assessment</h2>
        <span class="status-badge">Recent</span>
      </div>
      <div class="risk-display" :class="`risk-${latestAssessment.risk_level.toLowerCase()}`">
        <div class="risk-icon-large">
          <div class="risk-circle-indicator" :class="`risk-${latestAssessment.risk_level.toLowerCase()}`"></div>
        </div>
        <div class="risk-info">
          <div class="risk-level-text">{{ latestAssessment.risk_level }} Risk</div>
          <div class="risk-score-large">{{ latestAssessment.final_risk_percentage }}</div>
          <div class="risk-breakdown">
            <span>Image: {{ latestAssessment.image_risk_percentage }}</span>
            <span>•</span>
            <span>Support: {{ latestAssessment.support_risk_percentage }}</span>
          </div>
        </div>
      </div>
      <div class="status-footer">
        <div class="footer-item">
          <span class="footer-label">Assessed on</span>
          <span class="footer-value">{{ formatDate(latestAssessment.timestamp) }}</span>
        </div>
        <button class="view-details-btn" @click="$router.push('/monitoring')">
          View Details
          <svg class="arrow-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Empty State -->
    <div class="empty-state-card" v-else>
      <svg class="empty-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
      </svg>
      <h3>No Assessments Yet</h3>
      <p>Start by creating your first risk assessment to track your skin health.</p>
      <button class="action-button primary" @click="$router.push('/upload')">
        Create First Assessment
      </button>
    </div>

    <!-- Action Cards Grid -->
    <div class="section-header">
      <h2>Quick Actions</h2>
      <p>Access key features and tools</p>
    </div>
    <div class="cards-grid">
      <div class="action-card" @click="$router.push('/upload')">
        <div class="card-icon-wrapper blue">
          <svg class="card-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        </div>
        <h3>New Risk Assessment</h3>
        <p>Upload a skin lesion image for comprehensive risk analysis using AI and rule-based scoring</p>
        <div class="card-arrow">
          <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
          </svg>
        </div>
      </div>

      <div class="action-card" @click="$router.push('/monitoring')">
        <div class="card-icon-wrapper cyan">
          <svg class="card-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        </div>
        <h3>Monitoring History</h3>
        <p>View your complete assessment timeline, track trends, and compare results over time</p>
        <div class="card-arrow">
          <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
          </svg>
        </div>
      </div>

      <div class="action-card" @click="$router.push('/reports')">
        <div class="card-icon-wrapper teal">
          <svg class="card-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <h3>Reports</h3>
        <p>Generate and download detailed assessment reports with comprehensive risk analysis</p>
        <div class="card-arrow">
          <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
          </svg>
        </div>
      </div>

      <div class="action-card" @click="$router.push('/guide')">
        <div class="card-icon-wrapper green">
          <svg class="card-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
          </svg>
        </div>
        <h3>Skin Health Guide</h3>
        <p>Learn about skin health, ABCDE rule, self-examination techniques, and UV protection</p>
        <div class="card-arrow">
          <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
          </svg>
        </div>
      </div>
    </div>

    <!-- Risk Trends -->
    <div class="trends-section" v-if="assessments.length > 1">
      <div class="section-header">
        <div>
          <h2>Risk Trends</h2>
          <p>Track your risk levels over time</p>
        </div>
      </div>
      <div class="trends-card">
        <div class="trend-chart">
          <div 
            v-for="(assessment, index) in recentAssessments" 
            :key="assessment.id"
            class="trend-item"
          >
            <div class="trend-bar-wrapper">
              <div 
                class="trend-bar" 
                :class="`risk-${assessment.risk_level.toLowerCase()}`" 
                :style="{ height: `${Math.min(assessment.final_risk_score, 100)}%` }"
                :title="`${assessment.final_risk_percentage} - ${formatShortDate(assessment.timestamp)}`"
              >
                <div class="trend-value">{{ Math.round(assessment.final_risk_score) }}%</div>
              </div>
            </div>
            <div class="trend-label">{{ formatShortDate(assessment.timestamp) }}</div>
          </div>
        </div>
        <div class="trend-legend">
          <div class="legend-item">
            <span class="legend-color risk-low"></span>
            <span>Low Risk (0-40%)</span>
          </div>
          <div class="legend-item">
            <span class="legend-color risk-medium"></span>
            <span>Medium Risk (41-65%)</span>
          </div>
          <div class="legend-item">
            <span class="legend-color risk-high"></span>
            <span>High Risk (66-100%)</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import api from "@/api/client";

const assessments = ref([]);
const latestAssessment = ref(null);

const recentAssessments = computed(() => {
  return assessments.value.slice(-5).reverse();
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

const formatShortDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString("en-US", { month: "short", day: "numeric" });
};

const loadAssessments = async () => {
  try {
    const response = await api.get("/assessments");
    if (response.data && response.data.success) {
      assessments.value = response.data.assessments || [];
      if (assessments.value.length > 0) {
        latestAssessment.value = assessments.value[assessments.value.length - 1];
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
.dashboard-container {
  width: 100%;
  margin: 0;
  padding: 0;
  animation: fadeIn 0.6s ease-out;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2.5rem;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.header-content h1 {
  font-size: 2.75rem;
  font-weight: 800;
  color: #1e293b;
  margin-bottom: 0.5rem;
  background: linear-gradient(135deg, #2563eb 0%, #06b6d4 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -1px;
}

.subtitle {
  font-size: 1.125rem;
  color: #64748b;
  font-weight: 500;
}

.action-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1.75rem;
  border: none;
  border-radius: 0.75rem;
  font-size: 0.9375rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-button.primary {
  background: linear-gradient(135deg, #2563eb 0%, #06b6d4 100%);
  color: white;
  box-shadow: 0 4px 16px rgba(37, 99, 235, 0.3);
}

.action-button.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(37, 99, 235, 0.4);
}

.btn-icon {
  width: 1.25rem;
  height: 1.25rem;
  stroke-width: 2.5;
}

/* Status Card */
.status-card {
  background: white;
  border-radius: 1.25rem;
  padding: 2rem;
  margin-bottom: 2.5rem;
  box-shadow: 0 4px 20px rgba(37, 99, 235, 0.08);
  border: 1px solid #e2e8f0;
  animation: slideIn 0.6s ease-out;
}

.status-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.status-header h2 {
  font-size: 1.5rem;
  color: #1e293b;
  font-weight: 700;
}

.status-badge {
  padding: 0.375rem 0.875rem;
  background: #dcfce7;
  color: #166534;
  border-radius: 50px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.risk-display {
  display: flex;
  align-items: center;
  gap: 2rem;
  padding: 1.5rem;
  border-radius: 0.75rem;
  margin-bottom: 1.5rem;
}

.risk-display.risk-high {
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  border: 2px solid #ef4444;
}

.risk-display.risk-medium {
  background: linear-gradient(135deg, #ffedd5 0%, #fed7aa 100%);
  border: 2px solid #f97316;
}

.risk-display.risk-low {
  background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
  border: 2px solid #22c55e;
}

.risk-icon-large {
  display: flex;
  align-items: center;
  justify-content: center;
}

.risk-circle-indicator {
  width: 4rem;
  height: 4rem;
  border-radius: 50%;
  border: 4px solid;
  position: relative;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.risk-circle-indicator.risk-high {
  background: linear-gradient(135deg, #fee2e2, #fca5a5);
  border-color: #ef4444;
}

.risk-circle-indicator.risk-medium {
  background: linear-gradient(135deg, #ffedd5, #fdba74);
  border-color: #f97316;
}

.risk-circle-indicator.risk-low {
  background: linear-gradient(135deg, #dcfce7, #86efac);
  border-color: #22c55e;
}

.risk-info {
  flex: 1;
}

.risk-level-text {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.25rem;
}

.risk-score-large {
  font-size: 3rem;
  font-weight: 800;
  color: #1e293b;
  line-height: 1;
  margin-bottom: 0.5rem;
}

.risk-breakdown {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 500;
}

.status-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1.25rem;
  border-top: 1px solid #e2e8f0;
  flex-wrap: wrap;
  gap: 1rem;
}

.footer-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.footer-label {
  font-size: 0.75rem;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.footer-value {
  font-size: 0.9375rem;
  color: #1e293b;
  font-weight: 600;
}

.view-details-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  background: transparent;
  border: 2px solid #2563eb;
  color: #2563eb;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.view-details-btn:hover {
  background: #2563eb;
  color: white;
  transform: translateX(4px);
}

.arrow-icon {
  width: 1rem;
  height: 1rem;
  stroke-width: 2.5;
  transition: transform 0.3s ease;
}

.view-details-btn:hover .arrow-icon {
  transform: translateX(4px);
}

/* Empty State */
.empty-state-card {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 1.25rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
  margin-bottom: 2.5rem;
  border: 2px dashed #cbd5e1;
}

.empty-icon {
  width: 5rem;
  height: 5rem;
  margin: 0 auto 1.5rem;
  stroke: #94a3b8;
  stroke-width: 1.5;
}

.empty-state-card h3 {
  font-size: 1.5rem;
  color: #1e293b;
  margin-bottom: 0.5rem;
  font-weight: 700;
}

.empty-state-card p {
  font-size: 1rem;
  color: #64748b;
  margin-bottom: 2rem;
}

/* Section Header */
.section-header {
  margin-bottom: 2rem;
}

.section-header h2 {
  font-size: 1.75rem;
  color: #1e293b;
  margin-bottom: 0.25rem;
  font-weight: 700;
}

.section-header p {
  font-size: 0.9375rem;
  color: #64748b;
}

/* Action Cards */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.action-card {
  position: relative;
  background: white;
  border-radius: 1rem;
  padding: 1.75rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  cursor: pointer;
  transition: all 0.3s ease;
  animation: fadeIn 0.6s ease-out both;
}

.action-card:nth-child(1) { animation-delay: 0.1s; }
.action-card:nth-child(2) { animation-delay: 0.2s; }
.action-card:nth-child(3) { animation-delay: 0.3s; }
.action-card:nth-child(4) { animation-delay: 0.4s; }

.action-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 32px rgba(37, 99, 235, 0.12);
  border-color: #3b82f6;
}

.card-icon-wrapper {
  width: 3.5rem;
  height: 3.5rem;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.25rem;
  transition: transform 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card-icon-wrapper.blue {
  background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%);
}

.card-icon-wrapper.cyan {
  background: linear-gradient(135deg, #06b6d4 0%, #14b8a6 100%);
}

.card-icon-wrapper.teal {
  background: linear-gradient(135deg, #14b8a6 0%, #10b981 100%);
}

.card-icon-wrapper.green {
  background: linear-gradient(135deg, #10b981 0%, #22c55e 100%);
}

.action-card:hover .card-icon-wrapper {
  transform: scale(1.1) rotate(5deg);
}

.card-icon {
  width: 1.75rem;
  height: 1.75rem;
  stroke: white;
  stroke-width: 2;
}

.action-card h3 {
  font-size: 1.25rem;
  color: #1e293b;
  margin-bottom: 0.5rem;
  font-weight: 700;
}

.action-card p {
  font-size: 0.875rem;
  color: #475569;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.card-arrow {
  display: flex;
  align-items: center;
  color: #2563eb;
  transition: transform 0.3s ease;
}

.card-arrow svg {
  width: 1.25rem;
  height: 1.25rem;
  stroke-width: 2.5;
}

.action-card:hover .card-arrow {
  transform: translateX(8px);
}

/* Trends Section */
.trends-section {
  margin-top: 3rem;
}

.trends-card {
  background: white;
  border-radius: 1.25rem;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(37, 99, 235, 0.08);
  border: 1px solid #e2e8f0;
}

.trend-chart {
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  gap: 1rem;
  height: 300px;
  padding: 1.25rem 0;
  margin-bottom: 1.5rem;
}

.trend-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  max-width: 120px;
}

.trend-bar-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: flex-end;
  justify-content: center;
}

.trend-bar {
  width: 100%;
  min-height: 40px;
  border-radius: 0.5rem 0.5rem 0 0;
  position: relative;
  transition: all 0.3s ease;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: 0.5rem;
  box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.1);
}

.trend-bar:hover {
  transform: scaleY(1.05);
  box-shadow: 0 -6px 16px rgba(0, 0, 0, 0.15);
}

.trend-bar.risk-high {
  background: linear-gradient(180deg, #ef4444 0%, #dc2626 100%);
}

.trend-bar.risk-medium {
  background: linear-gradient(180deg, #f97316 0%, #ea580c 100%);
}

.trend-bar.risk-low {
  background: linear-gradient(180deg, #22c55e 0%, #16a34a 100%);
}

.trend-value {
  color: white;
  font-size: 0.75rem;
  font-weight: 700;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.trend-label {
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 500;
  text-align: center;
}

.trend-legend {
  display: flex;
  justify-content: center;
  gap: 2rem;
  padding-top: 1.25rem;
  border-top: 1px solid #e2e8f0;
  flex-wrap: wrap;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #475569;
}

.legend-color {
  width: 1rem;
  height: 1rem;
  border-radius: 0.25rem;
}

.legend-color.risk-high {
  background: #ef4444;
}

.legend-color.risk-medium {
  background: #f97316;
}

.legend-color.risk-low {
  background: #22c55e;
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

@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
  }

  .header-content h1 {
    font-size: 2rem;
  }

  .cards-grid {
    grid-template-columns: 1fr;
  }

  .trend-chart {
    height: 200px;
  }

  .risk-display {
    flex-direction: column;
    text-align: center;
  }
}
</style>