<template>
  <div class="dashboard-container fade-in">
    <div class="dashboard-header">
      <div class="header-content">
        <h1>Dashboard</h1>
        <p class="subtitle">Welcome to DermaSense Risk Assessment System</p>
      </div>
      <div class="header-actions">
        <button class="action-button primary" @click="$router.push('/upload')">
          <span>+</span>
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
        <div class="risk-icon-large">{{ getRiskIcon(latestAssessment.risk_level) }}</div>
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
          View Details →
        </button>
      </div>
    </div>

    <!-- Empty State -->
    <div class="empty-state-card" v-else>
      <div class="empty-icon">📊</div>
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
        <div class="card-glow"></div>
        <div class="card-content">
          <div class="card-icon-wrapper primary">
            <span class="card-icon">📸</span>
          </div>
          <h3>New Risk Assessment</h3>
          <p>Upload a skin lesion image for comprehensive risk analysis using AI and rule-based scoring</p>
          <div class="card-arrow">→</div>
        </div>
      </div>

      <div class="action-card" @click="$router.push('/monitoring')">
        <div class="card-glow"></div>
        <div class="card-content">
          <div class="card-icon-wrapper secondary">
            <span class="card-icon">📊</span>
          </div>
          <h3>Monitoring History</h3>
          <p>View your complete assessment timeline, track trends, and compare results over time</p>
          <div class="card-arrow">→</div>
        </div>
      </div>

      <div class="action-card" @click="$router.push('/reports')">
        <div class="card-glow"></div>
        <div class="card-content">
          <div class="card-icon-wrapper accent">
            <span class="card-icon">📄</span>
          </div>
          <h3>Reports</h3>
          <p>Generate and download detailed assessment reports with comprehensive risk analysis</p>
          <div class="card-arrow">→</div>
        </div>
      </div>

      <div class="action-card" @click="$router.push('/guide')">
        <div class="card-glow"></div>
        <div class="card-content">
          <div class="card-icon-wrapper info">
            <span class="card-icon">📖</span>
          </div>
          <h3>Skin Health Guide</h3>
          <p>Learn about skin health, ABCDE rule, self-examination techniques, and UV protection</p>
          <div class="card-arrow">→</div>
        </div>
      </div>
    </div>

    <!-- Risk Trends (if multiple assessments) -->
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

const getRiskIcon = (level) => {
  if (level === "HIGH") return "🔴";
  if (level === "MEDIUM") return "🟡";
  return "🟢";
};

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
  margin-bottom: var(--spacing-2xl);
  gap: var(--spacing-lg);
  flex-wrap: wrap;
}

.header-content h1 {
  font-size: 42px;
  font-weight: 800;
  color: var(--medical-gray-900);
  margin-bottom: var(--spacing-xs);
  background: linear-gradient(135deg, var(--medical-blue) 0%, var(--medical-teal) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -1px;
}

.subtitle {
  font-size: 18px;
  color: var(--medical-gray-600);
  font-weight: 500;
}

.header-actions {
  display: flex;
  gap: var(--spacing-md);
}

.action-button {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: 12px 24px;
  border: none;
  border-radius: var(--radius-md);
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-base);
}

.action-button.primary {
  background: linear-gradient(135deg, var(--medical-blue) 0%, var(--medical-teal) 100%);
  color: var(--medical-white);
  box-shadow: 0 4px 16px rgba(0, 102, 204, 0.3);
}

.action-button.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(0, 102, 204, 0.4);
}

/* Status Card */
.status-card {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.9) 100%);
  backdrop-filter: blur(20px);
  border-radius: var(--radius-xl);
  padding: var(--spacing-2xl);
  margin-bottom: var(--spacing-2xl);
  box-shadow: 0 8px 32px rgba(0, 102, 204, 0.12);
  border: 1px solid rgba(0, 102, 204, 0.1);
  animation: slideIn 0.6s ease-out;
}

.status-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xl);
}

.status-header h2 {
  font-size: 24px;
  color: var(--medical-gray-900);
  font-weight: 700;
}

.status-badge {
  padding: 6px 12px;
  background: var(--medical-green-light);
  color: var(--medical-green-dark);
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.risk-display {
  display: flex;
  align-items: center;
  gap: var(--spacing-xl);
  padding: var(--spacing-xl);
  border-radius: var(--radius-lg);
  margin-bottom: var(--spacing-xl);
  transition: all var(--transition-base);
}

.risk-display.risk-high {
  background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
  border: 2px solid var(--medical-red);
}

.risk-display.risk-medium {
  background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
  border: 2px solid var(--medical-orange);
}

.risk-display.risk-low {
  background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
  border: 2px solid var(--medical-green);
}

.risk-icon-large {
  font-size: 64px;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.1));
}

.risk-info {
  flex: 1;
}

.risk-level-text {
  font-size: 28px;
  font-weight: 700;
  color: var(--medical-gray-900);
  margin-bottom: var(--spacing-xs);
}

.risk-score-large {
  font-size: 48px;
  font-weight: 800;
  color: var(--medical-gray-900);
  margin-bottom: var(--spacing-sm);
  line-height: 1;
}

.risk-breakdown {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: 14px;
  color: var(--medical-gray-600);
  font-weight: 500;
}

.status-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: var(--spacing-lg);
  border-top: 1px solid var(--medical-gray-200);
  flex-wrap: wrap;
  gap: var(--spacing-md);
}

.footer-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.footer-label {
  font-size: 12px;
  color: var(--medical-gray-600);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.footer-value {
  font-size: 15px;
  color: var(--medical-gray-900);
  font-weight: 600;
}

.view-details-btn {
  padding: 10px 20px;
  background: transparent;
  border: 2px solid var(--medical-blue);
  color: var(--medical-blue);
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-base);
}

.view-details-btn:hover {
  background: var(--medical-blue);
  color: var(--medical-white);
  transform: translateX(4px);
}

/* Empty State */
.empty-state-card {
  text-align: center;
  padding: var(--spacing-3xl);
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-md);
  margin-bottom: var(--spacing-2xl);
  border: 2px dashed var(--medical-gray-300);
}

.empty-icon {
  font-size: 80px;
  margin-bottom: var(--spacing-lg);
  opacity: 0.6;
}

.empty-state-card h3 {
  font-size: 24px;
  color: var(--medical-gray-900);
  margin-bottom: var(--spacing-sm);
  font-weight: 700;
}

.empty-state-card p {
  font-size: 16px;
  color: var(--medical-gray-600);
  margin-bottom: var(--spacing-xl);
}

/* Section Header */
.section-header {
  margin-bottom: var(--spacing-xl);
}

.section-header h2 {
  font-size: 28px;
  color: var(--medical-gray-900);
  margin-bottom: var(--spacing-xs);
  font-weight: 700;
}

.section-header p {
  font-size: 15px;
  color: var(--medical-gray-600);
}

/* Action Cards */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--spacing-xl);
  margin-bottom: var(--spacing-3xl);
}

.action-card {
  position: relative;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: var(--radius-lg);
  padding: var(--spacing-xl);
  box-shadow: var(--shadow-md);
  border: 1px solid rgba(0, 102, 204, 0.1);
  cursor: pointer;
  transition: all var(--transition-base);
  overflow: hidden;
  animation: fadeIn 0.6s ease-out both;
}

.action-card:nth-child(1) { animation-delay: 0.1s; }
.action-card:nth-child(2) { animation-delay: 0.2s; }
.action-card:nth-child(3) { animation-delay: 0.3s; }
.action-card:nth-child(4) { animation-delay: 0.4s; }

.card-glow {
  position: absolute;
  inset: 0;
  opacity: 0;
  transition: opacity var(--transition-base);
  background: linear-gradient(135deg, var(--medical-blue), var(--medical-teal));
  border-radius: var(--radius-lg);
  filter: blur(20px);
  z-index: 0;
}

.action-card:hover .card-glow {
  opacity: 0.3;
}

.action-card:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-xl);
  border-color: var(--medical-blue);
}

.card-content {
  position: relative;
  z-index: 1;
}

.card-icon-wrapper {
  width: 64px;
  height: 64px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: var(--spacing-lg);
  transition: transform var(--transition-base);
}

.card-icon-wrapper.primary {
  background: linear-gradient(135deg, var(--medical-blue-light) 0%, var(--medical-teal-light) 100%);
}

.card-icon-wrapper.secondary {
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
}

.card-icon-wrapper.accent {
  background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
}

.card-icon-wrapper.info {
  background: linear-gradient(135deg, #e0f2f1 0%, #b2dfdb 100%);
}

.action-card:hover .card-icon-wrapper {
  transform: scale(1.1) rotate(5deg);
}

.card-icon {
  font-size: 32px;
}

.action-card h3 {
  font-size: 20px;
  color: var(--medical-gray-900);
  margin-bottom: var(--spacing-sm);
  font-weight: 700;
}

.action-card p {
  font-size: 14px;
  color: var(--medical-gray-700);
  line-height: 1.6;
  margin-bottom: var(--spacing-md);
}

.card-arrow {
  font-size: 24px;
  color: var(--medical-blue);
  transition: transform var(--transition-base);
}

.action-card:hover .card-arrow {
  transform: translateX(8px);
}

/* Trends Section */
.trends-section {
  margin-top: var(--spacing-3xl);
}

.trends-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: var(--radius-xl);
  padding: var(--spacing-2xl);
  box-shadow: var(--shadow-md);
  border: 1px solid rgba(0, 102, 204, 0.1);
}

.trend-chart {
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  gap: var(--spacing-md);
  height: 300px;
  padding: var(--spacing-lg) 0;
  margin-bottom: var(--spacing-xl);
}

.trend-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-md);
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
  border-radius: var(--radius-md) var(--radius-md) 0 0;
  position: relative;
  transition: all var(--transition-base);
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: var(--spacing-sm);
  box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.1);
}

.trend-bar:hover {
  transform: scaleY(1.05);
  box-shadow: 0 -6px 16px rgba(0, 0, 0, 0.15);
}

.trend-bar.risk-high {
  background: linear-gradient(180deg, var(--medical-red) 0%, #d32f2f 100%);
}

.trend-bar.risk-medium {
  background: linear-gradient(180deg, var(--medical-orange) 0%, #f57c00 100%);
}

.trend-bar.risk-low {
  background: linear-gradient(180deg, var(--medical-green) 0%, #388e3c 100%);
}

.trend-value {
  color: var(--medical-white);
  font-size: 12px;
  font-weight: 700;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.trend-label {
  font-size: 12px;
  color: var(--medical-gray-600);
  font-weight: 500;
  text-align: center;
}

.trend-legend {
  display: flex;
  justify-content: center;
  gap: var(--spacing-xl);
  padding-top: var(--spacing-lg);
  border-top: 1px solid var(--medical-gray-200);
  flex-wrap: wrap;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: 14px;
  color: var(--medical-gray-700);
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: 4px;
}

.legend-color.risk-high {
  background: var(--medical-red);
}

.legend-color.risk-medium {
  background: var(--medical-orange);
}

.legend-color.risk-low {
  background: var(--medical-green);
}

@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
  }

  .header-content h1 {
    font-size: 32px;
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
