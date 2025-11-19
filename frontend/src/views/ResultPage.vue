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
            <strong>Reminder:</strong> This result is for educational and
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

// In case backend returns "confidence_display" OR plain "confidence"
const confidenceDisplay = computed(() => {
  if (!result.value) return "";
  if (result.value.confidence_display) return result.value.confidence_display;
  if (typeof result.value.confidence === "number") {
    // format numeric confidence like "92.3%"
    return `${(result.value.confidence * 100).toFixed(1)}%`;
  }
  return result.value.confidence || "";
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
  // Check if backend stored an error
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

  imageUrl.value = result.value.image_url || "";
  treatments.value = treatmentOptions[result.value.label] || [];
});
</script>

<style scoped>
.result-page {
  background-color: #f7efe7; /* nude */
  padding: 40px 16px 60px;
}

/* Main white card */
.result-card {
  max-width: 1150px;
  margin: 0 auto;
  background-color: #ffffff;
  border-radius: 24px;
  padding: 32px 36px 40px;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.08);
}

.result-card h1 {
  font-size: 32px;
  margin-bottom: 24px;
  color: #222222;
  font-weight: 700;
}

/* Layout: image + text */
.result {
  display: flex;
  gap: 32px;
  margin-bottom: 32px;
  align-items: flex-start;
}

/* IMAGE */
.image {
  flex: 1;
  max-width: 420px;
}

.image img {
  width: 100%;
  border-radius: 18px;
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.15);
  background-color: #fdf7f1;
  object-fit: cover;
}

/* TEXT */
.details {
  flex: 1.6;
}

.label {
  font-size: 26px;
  margin-bottom: 10px;
  color: #222222;
  font-weight: 700;
}

.confidence {
  margin-bottom: 12px;
  color: #333333;
  font-size: 16px;
}

.description {
  font-size: 16px;
  line-height: 1.7;
  color: #3f3f3f;
  margin-bottom: 14px;
}

.doctor-note {
  font-size: 14px;
  line-height: 1.6;
  color: #6a4d34;
  background-color: #fff4d9;
  padding: 10px 14px;
  border-radius: 10px;
}

/* TREATMENTS */
.treatments {
  margin-top: 10px;
}

.treatments h3 {
  font-size: 22px;
  margin-bottom: 8px;
  color: #222222;
}

.treatment-note {
  font-size: 14px;
  color: #5e5e5e;
  margin-bottom: 18px;
  max-width: 780px;
}

.treatment-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 18px;
}

.treatment-card {
  background-color: #ffffff;
  border-radius: 16px;
  padding: 18px 20px;
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.04);
  border: 1px solid #f0e0d3;
}

.treatment-card h4 {
  font-size: 17px;
  margin-bottom: 8px;
  color: #222222;
}

.treatment-card p {
  font-size: 14px;
  color: #444444;
  line-height: 1.6;
}

/* Empty state / error state */
.empty-message {
  max-width: 700px;
  margin: 60px auto;
  font-size: 16px;
  text-align: center;
  color: #444444;
}

/* Responsive */
@media (max-width: 900px) {
  .result-card {
    padding: 24px 18px 28px;
  }

  .result {
    flex-direction: column;
  }

  .image {
    max-width: 100%;
  }
}
</style>
