<template>
  <section class="upload-card fade-in">
    <div class="upload-header">
      <h2>New Risk Assessment</h2>
      <p class="header-subtitle">Complete the 3-step process to get your risk assessment</p>
    </div>

    <div class="steps-indicator">
      <div class="step" :class="{ active: currentStep >= 1, completed: currentStep > 1 }">
        <span class="step-number">1</span>
        <span class="step-label">Image Upload</span>
      </div>
      <div class="step-connector" :class="{ completed: currentStep > 1 }"></div>
      <div class="step" :class="{ active: currentStep >= 2, completed: currentStep > 2 }">
        <span class="step-number">2</span>
        <span class="step-label">Image Analysis</span>
      </div>
      <div class="step-connector" :class="{ completed: currentStep > 2 }"></div>
      <div class="step" :class="{ active: currentStep >= 3 }">
        <span class="step-number">3</span>
        <span class="step-label">Optional Inputs</span>
      </div>
    </div>

    <div class="layout">
      <div class="left">
        <div class="step-content" v-if="currentStep === 1">
          <h3>Step 1: Upload Skin Lesion Image</h3>
          <div class="dropzone" @click="triggerFile">
            <input
              ref="fileInput"
              type="file"
              accept="image/*"
              hidden
              @change="onFileChange"
            />
            <div v-if="!previewUrl" class="dropzone-empty">
              <svg class="upload-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              <p>Click to upload a skin lesion image</p>
              <p class="hint">Supported formats: JPG, PNG</p>
            </div>
            <img v-else :src="previewUrl" alt="Preview" class="preview-image" />
          </div>
          <button 
            class="next-button" 
            :disabled="!file" 
            @click="currentStep = 2"
          >
            Next: Image Analysis
            <svg class="btn-arrow" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </button>
        </div>

        <div class="step-content" v-if="currentStep === 2">
          <h3>Step 2: Image Analysis</h3>
          <div class="analysis-info">
            <p>The image will be analyzed using our machine learning model to estimate risk probability.</p>
            <div class="analysis-placeholder">
              <div class="spinner" v-if="analyzing"></div>
              <svg v-else class="ready-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p v-if="!analyzing">Ready to analyze</p>
            </div>
          </div>
          <button 
            class="next-button" 
            :disabled="analyzing" 
            @click="currentStep = 3"
          >
            Next: Optional Inputs
            <svg class="btn-arrow" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </button>
        </div>

        <div class="step-content" v-if="currentStep === 3">
          <h3>Step 3: Optional User Inputs</h3>
          <p class="step-description">
            Provide additional information to improve risk assessment accuracy.
            All fields are optional.
          </p>
        </div>
      </div>

      <div class="right" v-if="currentStep === 3">
        <div class="form-section">
          <div class="field">
            <label>Lesion Duration</label>
            <select v-model="duration">
              <option value="">Select duration</option>
              <option value="Less than 1 month">Less than 1 month</option>
              <option value="1-3 months">1-3 months</option>
              <option value="3-6 months">3-6 months</option>
              <option value="More than 6 months">More than 6 months</option>
            </select>
          </div>

          <div class="field">
            <label>Lesion Location</label>
            <select v-model="location">
              <option value="">Select location</option>
              <option value="Face / Neck">Face / Neck</option>
              <option value="Trunk / Chest / Back">Trunk / Chest / Back</option>
              <option value="Upper Extremity">Upper Extremity</option>
              <option value="Lower Extremity">Lower Extremity</option>
              <option value="Other">Other</option>
            </select>
          </div>

          <div class="field">
            <label>Sun Exposure Level</label>
            <select v-model="sunExposure">
              <option value="">Select level</option>
              <option value="Low">Low</option>
              <option value="Medium">Medium</option>
              <option value="High">High</option>
            </select>
          </div>

          <div class="symptoms-section">
            <label class="symptoms-label">Symptoms (check all that apply)</label>
            <div class="checkbox-group">
              <label class="checkbox-label">
                <input type="checkbox" v-model="itching" />
                <span>Itching</span>
              </label>
              <label class="checkbox-label">
                <input type="checkbox" v-model="bleeding" />
                <span>Bleeding</span>
              </label>
              <label class="checkbox-label">
                <input type="checkbox" v-model="pain" />
                <span>Pain</span>
              </label>
            </div>
          </div>

          <button class="analyze" :disabled="!file" @click="submit">
            <svg class="btn-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
            </svg>
            Analyze Risk
          </button>

          <p v-if="error" class="error">{{ error }}</p>
        </div>
      </div>
    </div>

    <!-- Disclaimer Note -->
    <div class="info-note-full">
      <svg class="note-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
      </svg>
      <p>
        <strong>Disclaimer:</strong> This system is for risk assessment only and not a medical diagnosis. 
        Always consult a dermatologist for professional evaluation.
      </p>
    </div>
  </section>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "@/api/client";

const router = useRouter();

const fileInput = ref(null);
const file = ref(null);
const previewUrl = ref(null);
const currentStep = ref(1);
const analyzing = ref(false);

// Step 3 inputs
const duration = ref("");
const location = ref("");
const sunExposure = ref("");
const itching = ref(false);
const bleeding = ref(false);
const pain = ref(false);

const error = ref("");

const triggerFile = () => fileInput.value?.click();

const onFileChange = (e) => {
  const f = e.target.files?.[0];
  if (!f) return;
  file.value = f;
  previewUrl.value = URL.createObjectURL(f);
  error.value = "";
};

const submit = async () => {
  if (!file.value) return;
  error.value = "";
  analyzing.value = true;

  router.push("/analyzing");

  try {
    const form = new FormData();
    form.append("file", file.value);
    form.append("duration", duration.value || "");
    form.append("location", location.value || "");
    form.append("sun_exposure", sunExposure.value || "");
    form.append("itching", itching.value ? "true" : "false");
    form.append("bleeding", bleeding.value ? "true" : "false");
    form.append("pain", pain.value ? "true" : "false");

    console.log("Submitting assessment request...");
    
    const { data } = await api.post("/assess-risk", form, {
      timeout: 60000,
    });

    console.log("Assessment response:", data);

    if (!data || data.success === false) {
      localStorage.removeItem("assessmentResult");
      const errorMsg = data?.message || data?.detail || "Assessment failed. Please try again.";
      localStorage.setItem("assessmentError", errorMsg);
      router.push("/results");
      return;
    }

    localStorage.setItem("assessmentResult", JSON.stringify(data));
    if (previewUrl.value) {
      localStorage.setItem("assessmentImage", previewUrl.value);
    } else {
      localStorage.removeItem("assessmentImage");
    }
    localStorage.removeItem("assessmentError");

    router.push("/results");
  } catch (err) {
    console.error("Assessment error:", err);

    localStorage.removeItem("assessmentResult");

    let errorMessage = "Failed to analyze image. Please try again.";
    
    if (err?.code === 'ECONNABORTED') {
      errorMessage = "Request timeout. The analysis took too long. Please try again with a smaller image or check your connection.";
    } else if (err?.code === 'ERR_NETWORK' || err?.message?.includes('Network Error')) {
      errorMessage = "Cannot connect to the server. Please make sure the backend server is running on http://127.0.0.1:8000";
    } else if (err?.response?.data) {
      errorMessage = err.response.data.detail || err.response.data.message || errorMessage;
    } else if (err?.message) {
      errorMessage = err.message;
    }
    
    localStorage.setItem("assessmentError", errorMessage);
    router.push("/results");
  } finally {
    analyzing.value = false;
  }
};
</script>

<style scoped>
.upload-card {
  background: white;
  border-radius: 1.25rem;
  padding: 2.5rem;
  box-shadow: 0 8px 32px rgba(37, 99, 235, 0.12);
  border: 1px solid #e2e8f0;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  animation: fadeIn 0.6s ease-out;
}

.upload-header {
  margin-bottom: 2.5rem;
  text-align: center;
}

.upload-header h2 {
  font-size: 2.25rem;
  color: #1e293b;
  margin-bottom: 0.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #2563eb 0%, #06b6d4 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.header-subtitle {
  font-size: 1rem;
  color: #64748b;
  font-weight: 500;
}

.steps-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 2.5rem;
  gap: 0.5rem;
  padding: 1.5rem;
  background: #f8fafc;
  border-radius: 0.75rem;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.step-number {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background: #cbd5e1;
  color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  transition: all 0.3s ease;
}

.step.active .step-number {
  background: linear-gradient(135deg, #2563eb, #06b6d4);
  color: white;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

.step.completed .step-number {
  background: #22c55e;
  color: white;
}

.step-label {
  font-size: 0.75rem;
  color: #94a3b8;
  text-align: center;
}

.step.active .step-label {
  color: #2563eb;
  font-weight: 600;
}

.step-connector {
  width: 60px;
  height: 2px;
  background: #e2e8f0;
  margin: 0 0.5rem;
  margin-bottom: 1.5rem;
  transition: all 0.3s ease;
}

.step-connector.completed {
  background: #22c55e;
}

.layout {
  display: flex;
  gap: 2.5rem;
  align-items: flex-start;
}

.left,
.right {
  flex: 1;
}

.step-content h3 {
  font-size: 1.25rem;
  color: #1e293b;
  margin-bottom: 1.25rem;
  font-weight: 600;
}

.step-description {
  font-size: 0.875rem;
  color: #64748b;
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.dropzone {
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  border-radius: 0.75rem;
  padding: 2.5rem;
  text-align: center;
  border: 3px dashed #3b82f6;
  cursor: pointer;
  transition: all 0.3s ease;
  min-height: 350px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
}

.dropzone:hover {
  border-color: #2563eb;
  background: linear-gradient(135deg, #dbeafe 0%, #eff6ff 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(37, 99, 235, 0.15);
}

.dropzone-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.upload-icon {
  width: 4rem;
  height: 4rem;
  stroke: #3b82f6;
  stroke-width: 2;
  margin-bottom: 0.5rem;
}

.dropzone p {
  color: #1e40af;
  font-size: 1rem;
  font-weight: 500;
  margin: 0;
}

.hint {
  font-size: 0.875rem;
  color: #64748b;
}

.preview-image {
  max-width: 100%;
  max-height: 400px;
  object-fit: cover;
  border-radius: 0.625rem;
  border: 2px solid white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.analysis-info {
  background: #f8fafc;
  border-radius: 0.75rem;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.analysis-info p {
  color: #475569;
  margin-bottom: 1rem;
  line-height: 1.6;
}

.analysis-placeholder {
  text-align: center;
  padding: 2.5rem;
}

.spinner {
  width: 2.5rem;
  height: 2.5rem;
  border: 4px solid #e2e8f0;
  border-top-color: #2563eb;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

.ready-icon {
  width: 4rem;
  height: 4rem;
  stroke: #22c55e;
  stroke-width: 2;
  margin: 0 auto 0.5rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.next-button,
.analyze {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 1.5rem;
  padding: 1rem 2rem;
  border: none;
  border-radius: 0.75rem;
  background: linear-gradient(135deg, #2563eb 0%, #06b6d4 100%);
  color: white;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  width: 100%;
  box-shadow: 0 4px 16px rgba(37, 99, 235, 0.3);
}

.next-button:hover:not(:disabled),
.analyze:hover:not(:disabled) {
  background: linear-gradient(135deg, #1d4ed8 0%, #0891b2 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
}

.next-button:disabled,
.analyze:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-arrow,
.btn-icon {
  width: 1.25rem;
  height: 1.25rem;
  stroke-width: 2.5;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.field label {
  font-size: 0.875rem;
  color: #475569;
  margin-bottom: 0.5rem;
  display: block;
  font-weight: 500;
}

.field select {
  width: 100%;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  border: 1.5px solid #cbd5e1;
  font-size: 0.9375rem;
  background-color: white;
  color: #1e293b;
  transition: all 0.2s ease;
}

.field select:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.symptoms-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.symptoms-label {
  font-size: 0.875rem;
  color: #475569;
  font-weight: 500;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  padding: 0.875rem;
  border-radius: 0.5rem;
  border: 1.5px solid #e2e8f0;
  transition: all 0.2s ease;
}

.checkbox-label:hover {
  background: #f8fafc;
  border-color: #3b82f6;
}

.checkbox-label input[type="checkbox"] {
  width: 1.25rem;
  height: 1.25rem;
  cursor: pointer;
  accent-color: #2563eb;
}

.checkbox-label span {
  font-size: 0.9375rem;
  color: #475569;
}

.error {
  margin-top: 1rem;
  color: #dc2626;
  font-size: 0.875rem;
  padding: 0.875rem 1rem;
  background-color: #fee2e2;
  border-radius: 0.5rem;
  border-left: 4px solid #dc2626;
  font-weight: 500;
}

.info-note-full {
  margin-top: 2rem;
  padding: 1rem 1.25rem;
  background: linear-gradient(135deg, #ffedd5 0%, #fed7aa 100%);
  border-left: 4px solid #f97316;
  border-radius: 0.75rem;
  display: flex;
  align-items: flex-start;
  gap: 0.875rem;
}

.info-note-full .note-icon {
  width: 1.5rem;
  height: 1.5rem;
  flex-shrink: 0;
  color: #ea580c;
  margin-top: 0.125rem;
  stroke-width: 2;
}

.info-note-full p {
  margin: 0;
  font-size: 0.875rem;
  line-height: 1.6;
  color: #9a3412;
}

.info-note-full strong {
  font-weight: 600;
  color: #7c2d12;
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

@media (max-width: 900px) {
  .upload-card {
    padding: 2rem 1.5rem;
  }

  .layout {
    flex-direction: column;
    gap: 2rem;
  }

  .steps-indicator {
    flex-wrap: wrap;
  }

  .step-connector {
    display: none;
  }
}
</style>