<template>
  <section class="result-page">
    <!-- ERROR STATE FROM BACKEND -->
    <div v-if="errorMessage" class="empty-message">
      {{ errorMessage }}
      <br />
      Please try uploading another image on the
      <strong>Upload Image</strong> page.
    </div>

    <!-- NO RESULT YET -->
    <div v-else-if="!result" class="empty-message">
      No analysis result found. Please upload an image on the
      <strong>Upload Image</strong> page first.
    </div>

    <!-- WE HAVE A RESULT -->
    <div v-else class="result-card">
      <h1>Analysis Results</h1>

      <div class="result">
        <!-- IMAGE -->
        <div class="image" v-if="imageUrl">
          <img :src="imageUrl" alt="Analyzed Image" />
        </div>

        <!-- TEXT DETAILS -->
        <div class="details">
          <h2 class="label">{{ result.label }}</h2>

          <p class="confidence">
            <strong>Confidence:</strong> {{ confidenceDisplay }}
          </p>

          <p class="description">
            {{ result.description }}
          </p>

          <p class="doctor-note">
            <strong>⚠️Reminder:</strong> This result is for educational and
            decision-support purposes only. It is always best to consult a
            board-certified dermatologist for a full evaluation and treatment
            plan.
          </p>
        </div>
      </div>

      <!-- TREATMENTS -->
      <div class="treatments" v-if="treatments.length">
        <h3>Possible Treatments</h3>
        <p class="treatment-note">
          These treatments are common options based on the detected lesion type.
          They do not replace professional medical advice.
        </p>

        <div class="treatment-cards">
          <div
            v-for="(treatment, index) in treatments"
            :key="index"
            class="treatment-card"
          >
            <h4>{{ treatment.name }}</h4>
            <p>{{ treatment.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";

const result = ref(null);
const imageUrl = ref("");
const treatments = ref([]);
const errorMessage = ref("");

// confidence_display from backend OR numeric confidence (0–1)
const confidenceDisplay = computed(() => {
  if (!result.value) return "";
  if (result.value.confidence_display) return result.value.confidence_display;
  if (typeof result.value.confidence === "number") {
    return `${(result.value.confidence * 100).toFixed(1)}%`;
  }
  return "";
});

const treatmentOptions = {
  "No Skin Cancer (Benign)": [
    {
      name: "Skin Moisturization",
      description:
        "Use gentle moisturizers and daily sunscreen to keep the skin barrier healthy.",
    },
    {
      name: "Regular Skin Checks",
      description:
        "Monitor the area for changes in size, color, or shape and schedule routine skin examinations.",
    },
  ],
  "Basal Cell Carcinoma (BCC)": [
    {
      name: "Surgical Removal",
      description:
        "Minor surgery or excision is commonly used to remove BCC lesions with clear margins.",
    },
    {
      name: "Cryotherapy",
      description:
        "Freezing the lesion with liquid nitrogen to destroy abnormal cells in small or superficial BCCs.",
    },
  ],
  "Squamous Cell Carcinoma (SCC)": [
    {
      name: "Surgical Excision",
      description:
        "Removal of the lesion with a margin of healthy tissue to reduce the risk of recurrence.",
    },
    {
      name: "Radiation Therapy",
      description:
        "Sometimes used for SCC in locations where surgery is difficult or for certain high-risk lesions.",
    },
  ],
};

onMounted(() => {
  // error from backend (if any)
  const storedError = localStorage.getItem("analysisError");
  if (storedError) {
    errorMessage.value = storedError;
  }

  const stored = localStorage.getItem("analysisResult");
  if (!stored) return;

  try {
    const parsed = JSON.parse(stored);
    console.log("Loaded analysisResult from localStorage:", parsed);
    result.value = parsed;
  } catch (e) {
    console.error("Failed to parse analysisResult:", e);
    errorMessage.value = "Could not read saved analysis result.";
    return;
  }

  // Load preview image from UploadPage
  imageUrl.value = localStorage.getItem("analysisImage") || "";

  // Pick treatments based on label returned by backend
  if (result.value.label) {
    treatments.value = treatmentOptions[result.value.label] || [];
  }
});
</script>


<style scoped>
.result-page {
  background: linear-gradient(135deg, var(--medical-gray-50) 0%, var(--medical-blue-light) 100%);
  padding: 40px 16px 60px;
  min-height: calc(100vh - 200px);
}

/* Main white card */
.result-card {
  max-width: 1150px;
  margin: 0 auto;
  background-color: var(--medical-white);
  border-radius: 16px;
  padding: 40px 44px 48px;
  box-shadow: 0 12px 40px rgba(0, 102, 204, 0.15);
  border: 1px solid var(--medical-gray-200);
}

.result-card h1 {
  font-size: 36px;
  margin-bottom: 32px;
  color: var(--medical-gray-900);
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 3px solid var(--medical-blue);
  padding-bottom: 16px;
}

.result-card h1::before {
  content: "📊";
  font-size: 40px;
}

/* Layout: image + text */
.result {
  display: flex;
  gap: 40px;
  margin-bottom: 40px;
  align-items: flex-start;
}

/* IMAGE */
.image {
  flex: 1;
  max-width: 420px;
}

.image img {
  width: 100%;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  background-color: var(--medical-gray-50);
  object-fit: cover;
  border: 3px solid var(--medical-blue-light);
}

/* TEXT */
.details {
  flex: 1.6;
}

.label {
  font-size: 28px;
  margin-bottom: 16px;
  color: var(--medical-gray-900);
  font-weight: 700;
  padding: 12px 20px;
  background: linear-gradient(135deg, var(--medical-blue-light) 0%, var(--medical-teal-light) 100%);
  border-radius: 8px;
  border-left: 4px solid var(--medical-blue);
  display: inline-block;
}

.confidence {
  margin-bottom: 16px;
  color: var(--medical-gray-800);
  font-size: 17px;
  font-weight: 600;
  padding: 10px 16px;
  background-color: var(--medical-gray-50);
  border-radius: 8px;
  display: inline-block;
}

.confidence strong {
  color: var(--medical-blue);
}

.description {
  font-size: 16px;
  line-height: 1.8;
  color: var(--medical-gray-700);
  margin-bottom: 20px;
  padding: 16px;
  background-color: var(--medical-gray-50);
  border-radius: 8px;
  border-left: 4px solid var(--medical-teal);
}

.doctor-note {
  font-size: 14px;
  line-height: 1.7;
  color: var(--medical-gray-800);
  background: linear-gradient(135deg, var(--medical-red-light) 0%, #FFE5E5 100%);
  padding: 16px 20px;
  border-radius: 10px;
  border-left: 4px solid var(--medical-red);
  font-weight: 500;
  box-shadow: 0 2px 8px rgba(220, 53, 69, 0.1);
}

.doctor-note strong {
  color: var(--medical-red);
}

/* TREATMENTS */
.treatments {
  margin-top: 32px;
  padding-top: 32px;
  border-top: 2px solid var(--medical-gray-200);
}

.treatments h3 {
  font-size: 24px;
  margin-bottom: 12px;
  color: var(--medical-gray-900);
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 10px;
}

.treatments h3::before {
  content: "💊";
  font-size: 28px;
}

.treatment-note {
  font-size: 15px;
  color: var(--medical-gray-600);
  margin-bottom: 24px;
  max-width: 780px;
  line-height: 1.6;
}

.treatment-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.treatment-card {
  background: linear-gradient(135deg, var(--medical-white) 0%, var(--medical-blue-light) 100%);
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 16px rgba(0, 102, 204, 0.1);
  border: 1.5px solid var(--medical-blue-light);
  transition: all 0.3s ease;
}

.treatment-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 102, 204, 0.2);
  border-color: var(--medical-blue);
}

.treatment-card h4 {
  font-size: 18px;
  margin-bottom: 12px;
  color: var(--medical-blue-dark);
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 8px;
}

.treatment-card h4::before {
  content: "✓";
  color: var(--medical-teal);
  font-size: 20px;
}

.treatment-card p {
  font-size: 15px;
  color: var(--medical-gray-700);
  line-height: 1.7;
}

/* Empty state / error state */
.empty-message {
  max-width: 700px;
  margin: 80px auto;
  font-size: 17px;
  text-align: center;
  color: var(--medical-gray-700);
  padding: 40px;
  background-color: var(--medical-white);
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  border: 1px solid var(--medical-gray-200);
}

.empty-message strong {
  color: var(--medical-blue);
  font-weight: 600;
}

/* Responsive */
@media (max-width: 900px) {
  .result-card {
    padding: 30px 24px 36px;
  }

  .result-card h1 {
    font-size: 28px;
  }

  .result {
    flex-direction: column;
    gap: 30px;
  }

  .image {
    max-width: 100%;
  }

  .treatment-cards {
    grid-template-columns: 1fr;
  }
}
</style>
