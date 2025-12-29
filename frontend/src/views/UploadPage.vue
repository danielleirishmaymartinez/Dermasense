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
      <div class="step-connector"></div>
      <div class="step" :class="{ active: currentStep >= 2, completed: currentStep > 2 }">
        <span class="step-number">2</span>
        <span class="step-label">Image Analysis</span>
      </div>
      <div class="step-connector"></div>
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
              <div class="upload-icon">📸</div>
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
          </button>
        </div>

        <div class="step-content" v-if="currentStep === 2">
          <h3>Step 2: Image Analysis</h3>
          <div class="analysis-info">
            <p>The image will be analyzed using our machine learning model to estimate risk probability.</p>
            <div class="analysis-placeholder">
              <div class="spinner" v-if="analyzing"></div>
              <p v-else>Ready to analyze</p>
            </div>
          </div>
          <button 
            class="next-button" 
            :disabled="analyzing" 
            @click="currentStep = 3"
          >
            Next: Optional Inputs
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
            Analyze Risk
          </button>

          <p v-if="error" class="error">{{ error }}</p>
        </div>
      </div>
    </div>

    <!-- Disclaimer Note -->
    <div class="info-note-full">
      <svg class="note-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
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
    
    // Don't set Content-Type header - let axios set it automatically for FormData
    const { data } = await api.post("/assess-risk", form, {
      timeout: 60000, // 60 second timeout for ML inference
    });

    console.log("Assessment response:", data);

    // Check if assessment was successful
    if (!data || data.success === false) {
      // Handle error response from backend
      localStorage.removeItem("assessmentResult");
      const errorMsg = data?.message || data?.detail || "Assessment failed. Please try again.";
      localStorage.setItem("assessmentError", errorMsg);
      router.push("/results");
      return;
    }

    // Save result for ResultPage
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
    console.error("Error details:", {
      message: err?.message,
      code: err?.code,
      response: err?.response?.data,
      status: err?.response?.status,
    });

    localStorage.removeItem("assessmentResult");

    // Better error message handling
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
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: var(--radius-xl);
  padding: var(--spacing-2xl);
  box-shadow: 0 8px 32px rgba(0, 102, 204, 0.12);
  border: 1px solid rgba(0, 102, 204, 0.1);
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  animation: fadeIn 0.6s ease-out;
}

.upload-header {
  margin-bottom: var(--spacing-2xl);
  text-align: center;
}

.upload-header h2 {
  font-size: 36px;
  color: var(--medical-gray-900);
  margin-bottom: var(--spacing-sm);
  font-weight: 800;
  background: linear-gradient(135deg, var(--medical-blue) 0%, var(--medical-teal) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.header-subtitle {
  font-size: 16px;
  color: var(--medical-gray-600);
  font-weight: 500;
}

.steps-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: var(--spacing-2xl);
  gap: var(--spacing-sm);
  padding: var(--spacing-lg);
  background: var(--medical-gray-50);
  border-radius: var(--radius-lg);
  position: relative;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.step-number {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--medical-gray-200);
  color: var(--medical-gray-600);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  transition: all 0.3s ease;
}

.step.active .step-number {
  background: var(--medical-blue);
  color: var(--medical-white);
}

.step.completed .step-number {
  background: #4caf50;
  color: var(--medical-white);
}

.step-label {
  font-size: 12px;
  color: var(--medical-gray-600);
  text-align: center;
}

.step.active .step-label {
  color: var(--medical-blue);
  font-weight: 600;
}

.step-connector {
  width: 60px;
  height: 2px;
  background: var(--medical-gray-300);
  margin: 0 8px;
}

.layout {
  display: flex;
  gap: 40px;
  align-items: flex-start;
}

.left,
.right {
  flex: 1;
}

.step-content h3 {
  font-size: 20px;
  color: var(--medical-gray-900);
  margin-bottom: 20px;
  font-weight: 600;
}

.step-description {
  font-size: 14px;
  color: var(--medical-gray-600);
  margin-bottom: 24px;
  line-height: 1.6;
}

.dropzone {
  background: linear-gradient(135deg, var(--medical-blue-light) 0%, var(--medical-teal-light) 100%);
  border-radius: var(--radius-lg);
  padding: var(--spacing-2xl);
  text-align: center;
  border: 3px dashed var(--medical-blue);
  cursor: pointer;
  transition: all var(--transition-base);
  min-height: 350px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.dropzone::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, var(--medical-blue) 0%, var(--medical-teal) 100%);
  opacity: 0;
  transition: opacity var(--transition-base);
}

.dropzone:hover::before {
  opacity: 0.05;
}

.dropzone:hover {
  border-color: var(--medical-blue-dark);
  background: linear-gradient(135deg, var(--medical-teal-light) 0%, var(--medical-blue-light) 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 102, 204, 0.15);
}

.dropzone-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.upload-icon {
  font-size: 64px;
}

.dropzone p {
  color: var(--medical-blue-dark);
  font-size: 16px;
  font-weight: 500;
  margin: 0;
}

.hint {
  font-size: 14px;
  color: var(--medical-gray-600);
}

.preview-image {
  max-width: 100%;
  max-height: 400px;
  object-fit: cover;
  border-radius: 10px;
  border: 2px solid var(--medical-white);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.analysis-info {
  background: var(--medical-gray-50);
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
}

.analysis-info p {
  color: var(--medical-gray-700);
  margin-bottom: 16px;
  line-height: 1.6;
}

.analysis-placeholder {
  text-align: center;
  padding: 40px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--medical-gray-200);
  border-top-color: var(--medical-blue);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.next-button {
  margin-top: 24px;
  padding: 14px 32px;
  border: none;
  border-radius: 8px;
  background: linear-gradient(135deg, var(--medical-blue) 0%, var(--medical-teal) 100%);
  color: var(--medical-white);
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  width: 100%;
}

.next-button:hover:not(:disabled) {
  background: linear-gradient(135deg, var(--medical-blue-dark) 0%, var(--medical-teal-dark) 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 102, 204, 0.4);
}

.next-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.field label {
  font-size: 14px;
  color: var(--medical-gray-700);
  margin-bottom: 8px;
  display: block;
  font-weight: 500;
}

.field select {
  width: 100%;
  padding: 12px 14px;
  border-radius: 8px;
  border: 1.5px solid var(--medical-gray-300);
  font-size: 15px;
  background-color: var(--medical-white);
  color: var(--medical-gray-900);
  transition: all 0.2s ease;
  font-family: 'Inter', 'Roboto', sans-serif;
}

.field select:focus {
  outline: none;
  border-color: var(--medical-blue);
  box-shadow: 0 0 0 3px var(--medical-blue-light);
}

.symptoms-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.symptoms-label {
  font-size: 14px;
  color: var(--medical-gray-700);
  font-weight: 500;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  padding: 12px;
  border-radius: 8px;
  border: 1.5px solid var(--medical-gray-200);
  transition: all 0.2s ease;
}

.checkbox-label:hover {
  background: var(--medical-gray-50);
  border-color: var(--medical-blue);
}

.checkbox-label input[type="checkbox"] {
  width: 20px;
  height: 20px;
  cursor: pointer;
}

.checkbox-label span {
  font-size: 15px;
  color: var(--medical-gray-700);
}

.analyze {
  margin-top: var(--spacing-md);
  padding: 16px 32px;
  border: none;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, var(--medical-blue) 0%, var(--medical-teal) 100%);
  color: var(--medical-white);
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-base);
  box-shadow: 0 4px 20px rgba(0, 102, 204, 0.3);
  width: 100%;
  position: relative;
  overflow: hidden;
}

.analyze::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, var(--medical-blue-dark) 0%, var(--medical-teal-dark) 100%);
  opacity: 0;
  transition: opacity var(--transition-base);
}

.analyze:hover::before {
  opacity: 1;
}

.analyze span {
  position: relative;
  z-index: 1;
}

.analyze:hover:not(:disabled) {
  background: linear-gradient(135deg, var(--medical-blue-dark) 0%, var(--medical-teal-dark) 100%);
  box-shadow: 0 6px 20px rgba(0, 102, 204, 0.4);
  transform: translateY(-2px);
}

.analyze:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.error {
  margin-top: 16px;
  color: var(--medical-red);
  font-size: 14px;
  padding: 12px 16px;
  background-color: var(--medical-red-light);
  border-radius: 8px;
  border-left: 4px solid var(--medical-red);
  font-weight: 500;
}

.info-note-full {
  margin-top: 24px;
  padding: 14px 18px;
  background-color: #FFF4E6;
  border-left: 4px solid #FF9800;
  border-radius: 8px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.info-note-full .note-icon {
  width: 22px;
  height: 22px;
  flex-shrink: 0;
  color: #F57C00;
  margin-top: 2px;
}

.info-note-full p {
  margin: 0;
  font-size: 14px;
  line-height: 1.6;
  color: #E65100;
}

.info-note-full strong {
  font-weight: 600;
  color: #BF360C;
}

@media (max-width: 900px) {
  .upload-card {
    padding: 30px 24px;
  }

  .layout {
    flex-direction: column;
    gap: 30px;
  }

  .steps-indicator {
    flex-wrap: wrap;
  }

  .step-connector {
    display: none;
  }
}
</style>
