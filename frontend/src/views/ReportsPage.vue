<template>
  <div class="reports-container fade-in">
    <div class="page-header">
      <h1>Reports</h1>
      <p class="subtitle">Download and manage your assessment reports</p>
    </div>

    <div v-if="assessments.length === 0" class="empty-state">
      <div class="empty-icon">📄</div>
      <h2>No assessments available</h2>
      <p>Create a risk assessment to generate reports.</p>
      <button class="primary-button" @click="$router.push('/upload')">
        New Assessment
      </button>
    </div>

    <div v-else>
      <div class="reports-list">
        <div 
          v-for="assessment in sortedAssessments" 
          :key="assessment.id"
          class="report-card"
        >
          <div class="report-header">
            <div class="report-info">
              <div class="report-date">{{ formatDate(assessment.timestamp) }}</div>
              <div class="report-risk" :class="`risk-${assessment.risk_level.toLowerCase()}`">
                {{ assessment.risk_level }} Risk - {{ assessment.final_risk_percentage }}
              </div>
            </div>
            <button 
              class="download-button" 
              @click="generatePDF(assessment)"
              :disabled="generating === assessment.id"
            >
              {{ generating === assessment.id ? 'Generating...' : '📥 Download PDF' }}
            </button>
          </div>
          <div class="report-summary">
            <div class="summary-item">
              <span class="label">Image Risk:</span>
              <span class="value">{{ assessment.image_risk_percentage }}</span>
            </div>
            <div class="summary-item">
              <span class="label">Support Risk:</span>
              <span class="value">{{ assessment.support_risk_percentage }}</span>
            </div>
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
const generating = ref(null);

const sortedAssessments = computed(() => {
  return [...assessments.value].sort((a, b) => 
    new Date(b.timestamp) - new Date(a.timestamp)
  );
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

const generatePDF = async (assessment) => {
  generating.value = assessment.id;
  
  try {
    // Create PDF content
    const pdfContent = createPDFContent(assessment);
    
    // Create blob and download
    const blob = new Blob([pdfContent], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `DermaSense_Report_${assessment.id.substring(0, 8)}.html`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    
    // Alternative: Open in new window for printing
    setTimeout(() => {
      const printWindow = window.open();
      printWindow.document.write(pdfContent);
      printWindow.document.close();
      printWindow.print();
    }, 500);
    
  } catch (error) {
    console.error("Failed to generate PDF:", error);
    alert("Failed to generate report. Please try again.");
  } finally {
    generating.value = null;
  }
};

const createPDFContent = (assessment) => {
  const riskColor = assessment.risk_level === 'HIGH' ? '#d32f2f' : 
                   assessment.risk_level === 'MEDIUM' ? '#f57c00' : '#388e3c';
  
  return `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>DermaSense Risk Assessment Report</title>
  <style>
    body {
      font-family: 'Arial', sans-serif;
      max-width: 800px;
      margin: 40px auto;
      padding: 20px;
      color: #333;
    }
    .header {
      text-align: center;
      border-bottom: 3px solid #0066cc;
      padding-bottom: 20px;
      margin-bottom: 30px;
    }
    .header h1 {
      color: #0066cc;
      margin: 0;
    }
    .risk-badge {
      display: inline-block;
      padding: 12px 24px;
      border-radius: 8px;
      font-size: 24px;
      font-weight: 700;
      margin: 20px 0;
      color: white;
      background-color: ${riskColor};
    }
    .section {
      margin: 30px 0;
      padding: 20px;
      background: #f5f5f5;
      border-radius: 8px;
    }
    .section h2 {
      color: #0066cc;
      margin-top: 0;
    }
    .info-row {
      display: flex;
      justify-content: space-between;
      padding: 10px 0;
      border-bottom: 1px solid #ddd;
    }
    .info-row:last-child {
      border-bottom: none;
    }
    .label {
      font-weight: 600;
      color: #666;
    }
    .value {
      color: #333;
    }
    .disclaimer {
      background: #fff3cd;
      border-left: 4px solid #ff9800;
      padding: 15px;
      margin: 30px 0;
      border-radius: 4px;
    }
    .disclaimer strong {
      color: #e65100;
    }
    ul {
      padding-left: 20px;
    }
    li {
      margin: 8px 0;
    }
    @media print {
      body {
        margin: 0;
        padding: 20px;
      }
    }
  </style>
</head>
<body>
  <div class="header">
    <h1>DermaSense Risk Assessment Report</h1>
    <p>Machine Learning-Assisted Skin Lesion Risk Assessment System</p>
  </div>

  <div style="text-align: center;">
    <div class="risk-badge">${assessment.risk_level} Risk</div>
    <p style="font-size: 20px; margin: 10px 0;">Final Risk Score: ${assessment.final_risk_percentage}</p>
  </div>

  <div class="section">
    <h2>Assessment Details</h2>
    <div class="info-row">
      <span class="label">Assessment Date:</span>
      <span class="value">${formatDate(assessment.timestamp)}</span>
    </div>
    <div class="info-row">
      <span class="label">Assessment ID:</span>
      <span class="value">${assessment.id}</span>
    </div>
  </div>

  <div class="section">
    <h2>Risk Breakdown</h2>
    <div class="info-row">
      <span class="label">Image-Based Risk:</span>
      <span class="value">${assessment.image_risk_percentage}</span>
    </div>
    <div class="info-row">
      <span class="label">Support Risk (User Inputs):</span>
      <span class="value">${assessment.support_risk_percentage}</span>
    </div>
    <div class="info-row" style="border-top: 2px solid #0066cc; margin-top: 10px; padding-top: 15px;">
      <span class="label" style="font-size: 18px;">Final Risk Score:</span>
      <span class="value" style="font-size: 18px; font-weight: 700; color: #0066cc;">${assessment.final_risk_percentage}</span>
    </div>
  </div>

  <div class="section">
    <h2>Assessment Explanations</h2>
    <ul>
      ${assessment.explanations.map(exp => `<li>${exp}</li>`).join('')}
    </ul>
  </div>

  <div class="section">
    <h2>Recommendations</h2>
    <p>${assessment.recommendation}</p>
  </div>

  ${assessment.user_inputs && Object.keys(assessment.user_inputs).some(k => assessment.user_inputs[k]) ? `
  <div class="section">
    <h2>User Inputs</h2>
    ${assessment.user_inputs.duration ? `<div class="info-row"><span class="label">Duration:</span><span class="value">${assessment.user_inputs.duration}</span></div>` : ''}
    ${assessment.user_inputs.location ? `<div class="info-row"><span class="label">Location:</span><span class="value">${assessment.user_inputs.location}</span></div>` : ''}
    ${assessment.user_inputs.sun_exposure ? `<div class="info-row"><span class="label">Sun Exposure:</span><span class="value">${assessment.user_inputs.sun_exposure}</span></div>` : ''}
    ${assessment.user_inputs.itching || assessment.user_inputs.bleeding || assessment.user_inputs.pain ? `
    <div class="info-row">
      <span class="label">Symptoms:</span>
      <span class="value">
        ${[assessment.user_inputs.itching && 'Itching', assessment.user_inputs.bleeding && 'Bleeding', assessment.user_inputs.pain && 'Pain'].filter(Boolean).join(', ') || 'None'}
      </span>
    </div>
    ` : ''}
  </div>
  ` : ''}

  <div class="disclaimer">
    <strong>⚠️ Important Disclaimer:</strong>
    <p>This system is for risk assessment only and not a medical diagnosis. 
    DermaSense is a machine learning-assisted system that estimates skin lesion risk levels 
    and supports long-term monitoring. It does not provide medical diagnosis. 
    Always consult a dermatologist for professional evaluation.</p>
  </div>

  <div style="text-align: center; margin-top: 40px; color: #666; font-size: 12px;">
    <p>Generated by DermaSense Risk Assessment System</p>
    <p>Report ID: ${assessment.id}</p>
  </div>
</body>
</html>
  `;
};

const loadAssessments = async () => {
  try {
    const response = await api.get("/assessments");
    if (response.data && response.data.success) {
      assessments.value = response.data.assessments || [];
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
.reports-container {
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

.reports-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.report-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: var(--radius-lg);
  padding: var(--spacing-xl);
  box-shadow: 0 4px 20px rgba(0, 102, 204, 0.1);
  border: 1px solid rgba(0, 102, 204, 0.1);
  transition: all var(--transition-base);
  position: relative;
  overflow: hidden;
}

.report-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(180deg, var(--medical-blue) 0%, var(--medical-teal) 100%);
  opacity: 0;
  transition: opacity var(--transition-base);
}

.report-card:hover::before {
  opacity: 1;
}

.report-card:hover {
  box-shadow: 0 8px 24px rgba(0, 102, 204, 0.15);
  transform: translateY(-2px);
}

.report-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 16px;
}

.report-info {
  flex: 1;
}

.report-date {
  font-size: 14px;
  color: var(--medical-gray-600);
  margin-bottom: 8px;
}

.report-risk {
  font-size: 18px;
  font-weight: 600;
  padding: 6px 12px;
  border-radius: 6px;
  display: inline-block;
}

.report-risk.risk-high {
  background: #ffebee;
  color: var(--medical-red);
}

.report-risk.risk-medium {
  background: #fff3e0;
  color: #f57c00;
}

.report-risk.risk-low {
  background: #e8f5e9;
  color: #388e3c;
}

.download-button {
  padding: 10px 20px;
  background: linear-gradient(135deg, var(--medical-blue) 0%, var(--medical-teal) 100%);
  color: var(--medical-white);
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.download-button:hover:not(:disabled) {
  background: linear-gradient(135deg, var(--medical-blue-dark) 0%, var(--medical-teal-dark) 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
}

.download-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.report-summary {
  display: flex;
  gap: 24px;
  padding-top: 16px;
  border-top: 1px solid var(--medical-gray-200);
}

.summary-item {
  display: flex;
  gap: 8px;
}

.summary-item .label {
  font-size: 14px;
  color: var(--medical-gray-600);
}

.summary-item .value {
  font-size: 14px;
  color: var(--medical-gray-900);
  font-weight: 600;
}

@media (max-width: 768px) {
  .report-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .download-button {
    width: 100%;
  }

  .report-summary {
    flex-direction: column;
    gap: 12px;
  }
}
</style>

