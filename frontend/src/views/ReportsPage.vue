<template>
  <div class="reports-container fade-in">
    <div class="page-header">
      <h1>Reports</h1>
      <p class="subtitle">Download and manage your assessment reports</p>
    </div>

    <div v-if="assessments.length === 0" class="empty-state">
      <svg class="empty-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      <h2>No assessments available</h2>
      <p>Create a risk assessment to generate reports.</p>
      <button class="primary-button" @click="$router.push('/upload')">
        <svg class="btn-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
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
              <svg class="btn-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10" />
              </svg>
              {{ generating === assessment.id ? 'Generating...' : 'Download PDF' }}
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
    const pdfContent = createPDFContent(assessment);
    
    const blob = new Blob([pdfContent], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `DermaSense_Report_${assessment.id.substring(0, 8)}.html`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    
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
  const riskColor = assessment.risk_level === 'HIGH' ? '#dc2626' : 
                   assessment.risk_level === 'MEDIUM' ? '#ea580c' : '#16a34a';
  
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
      color: #1e293b;
    }
    .header {
      text-align: center;
      border-bottom: 3px solid #2563eb;
      padding-bottom: 20px;
      margin-bottom: 30px;
    }
    .header h1 {
      color: #2563eb;
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
      background: #f8fafc;
      border-radius: 8px;
    }
    .section h2 {
      color: #2563eb;
      margin-top: 0;
    }
    .info-row {
      display: flex;
      justify-content: space-between;
      padding: 10px 0;
      border-bottom: 1px solid #e2e8f0;
    }
    .info-row:last-child {
      border-bottom: none;
    }
    .label {
      font-weight: 600;
      color: #64748b;
    }
    .value {
      color: #1e293b;
    }
    .disclaimer {
      background: #ffedd5;
      border-left: 4px solid #f97316;
      padding: 15px;
      margin: 30px 0;
      border-radius: 4px;
    }
    .disclaimer strong {
      color: #9a3412;
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
    <div class="info-row" style="border-top: 2px solid #2563eb; margin-top: 10px; padding-top: 15px;">
      <span class="label" style="font-size: 18px;">Final Risk Score:</span>
      <span class="value" style="font-size: 18px; font-weight: 700; color: #2563eb;">${assessment.final_risk_percentage}</span>
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

  <div style="text-align: center; margin-top: 40px; color: #64748b; font-size: 12px;">
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

.reports-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.report-card {
  background: white;
  border-radius: 1rem;
  padding: 1.75rem;
  box-shadow: 0 4px 20px rgba(37, 99, 235, 0.08);
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
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
  background: linear-gradient(180deg, #2563eb 0%, #06b6d4 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.report-card:hover::before {
  opacity: 1;
}

.report-card:hover {
  box-shadow: 0 8px 24px rgba(37, 99, 235, 0.12);
  transform: translateY(-2px);
}

.report-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.report-info {
  flex: 1;
}

.report-date {
  font-size: 0.875rem;
  color: #64748b;
  margin-bottom: 0.5rem;
}

.report-risk {
  font-size: 1.125rem;
  font-weight: 600;
  padding: 0.375rem 0.875rem;
  border-radius: 0.375rem;
  display: inline-block;
}

.report-risk.risk-high {
  background: #fee2e2;
  color: #dc2626;
}

.report-risk.risk-medium {
  background: #ffedd5;
  color: #ea580c;
}

.report-risk.risk-low {
  background: #dcfce7;
  color: #16a34a;
}

.download-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #2563eb 0%, #06b6d4 100%);
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(37, 99, 235, 0.2);
}

.download-button:hover:not(:disabled) {
  background: linear-gradient(135deg, #1d4ed8 0%, #0891b2 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

.download-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.report-summary {
  display: flex;
  gap: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.summary-item {
  display: flex;
  gap: 0.5rem;
}

.summary-item .label {
  font-size: 0.875rem;
  color: #64748b;
}

.summary-item .value {
  font-size: 0.875rem;
  color: #1e293b;
  font-weight: 600;
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
  .report-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .download-button {
    width: 100%;
    justify-content: center;
  }

  .report-summary {
    flex-direction: column;
    gap: 0.75rem;
  }
}
</style>