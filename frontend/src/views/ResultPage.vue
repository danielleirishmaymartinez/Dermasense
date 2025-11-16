<template>
  <section class="result-page">
    <div v-if="result" class="result-card">
      <h1>Analysis Results</h1>

      <div class="result">
        <!-- IMAGE BLOCK -->
        <div class="image" v-if="imageUrl">
          <img :src="imageUrl" alt="Analyzed lesion image" />
        </div>

        <!-- TEXT BLOCK -->
        <div class="details">
          <h2 class="label">{{ result.label }}</h2>
          <p class="confidence">
            <strong>Confidence:</strong> {{ result.confidence_display }}
          </p>
          <p class="description">
            {{ result.description }}
          </p>
        </div>
      </div>

      <!-- TREATMENTS -->
      <div class="treatments" v-if="treatments.length">
        <h3>Possible Treatments</h3>
        <p class="treatment-note">
          These suggested treatments are based on the detected lesion type and are for
          educational purposes only. Always consult a dermatologist for an actual
          treatment plan and medical advice.
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

    <p v-else class="empty-message">
      No analysis result found. Please upload an image on the <strong>Upload Image</strong>
      page first.
    </p>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";

const result = ref(null);
const imageUrl = ref("");
const treatments = ref([]);

// 👇 adjust this if your backend URL is different
const BACKEND_BASE = "http://127.0.0.1:8000";

const treatmentOptions = {
  "No Skin Cancer (Benign)": [
    {
      name: "Skin Moisturization",
      description:
        "Use gentle moisturizers and sunscreen to keep the skin barrier healthy.",
    },
    {
      name: "Regular Skin Checks",
      description:
        "Monitor the lesion for changes and schedule routine skin examinations.",
    },
  ],
  "Basal Cell Carcinoma (BCC)": [
    {
      name: "Surgical Removal",
      description:
        "Minor surgery or excision is commonly used to remove BCC lesions.",
    },
    {
      name: "Cryotherapy",
      description:
        "Freezing the lesion with liquid nitrogen to destroy abnormal cells.",
    },
  ],
  "Squamous Cell Carcinoma (SCC)": [
    {
      name: "Surgical Excision",
      description:
        "Removal of the lesion with a margin of healthy tissue to reduce recurrence.",
    },
    {
      name: "Radiation Therapy",
      description:
        "Used in select SCC cases, especially in areas where surgery is difficult.",
    },
  ],
};

onMounted(() => {
  const stored = localStorage.getItem("analysisResult");
  if (!stored) return;

  result.value = JSON.parse(stored);

  // 🖼 Fix: build full URL so the image loads from FastAPI, not Vite
  if (result.value.image_url) {
    const url = result.value.image_url;
    imageUrl.value = url.startsWith("http")
      ? url
      : `${BACKEND_BASE}${url}`;
  }

  treatments.value = treatmentOptions[result.value.label] || [];
});
</script>

<style scoped>
.result-page {
  background-color: #f7efe7; /* nude */
  padding: 40px 16px 60px;
}

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

/* main layout: image + text */
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

/* Empty state */
.empty-message {
  max-width: 700px;
  margin: 40px auto;
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
