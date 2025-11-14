<template>
  <section v-if="result" class="result">
    <h2>Result: {{ result.label }}</h2>
    <p class="confidence">Confidence Level: {{ result.confidence }}</p>

    <div class="content">
      <div class="desc">
        <p>{{ result.description }}</p>
        <p class="note">
          This output is for decision support only and does not replace clinical
          diagnosis. Please consult a certified dermatologist.
        </p>
      </div>

      <div class="images">
        <div class="img-card" v-if="imageSrc">
          <img :src="imageSrc" alt="Original lesion" />
          <p>Original Image</p>
        </div>
        <div class="img-card">
          <img :src="gradcamSrc" alt="Grad-CAM" />
          <p>Grad-CAM</p>
        </div>
      </div>
    </div>

    <div class="warning">
      ⚠️ This system is an aid tool, not a diagnostic system. Always consult a
      dermatologist for confirmation.
    </div>
  </section>

  <section v-else class="no-data">
    <p>No result available. Please upload an image first.</p>
    <router-link to="/upload">
      <button>Go to Upload</button>
    </router-link>
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";

const result = ref(null);
const error = ref(null);

onMounted(() => {
  const stored = localStorage.getItem("analysisResult");
  const storedError = localStorage.getItem("analysisError");

  if (storedError && !stored) {
    error.value = storedError;
  }

  if (stored) {
    result.value = JSON.parse(stored);
  }
});

const imageSrc = computed(() =>
  result.value?.image_url ? `http://127.0.0.1:8000${result.value.image_url}` : ""
);

// placeholder Grad-CAM until backend provides real gradcam_url
const gradcamSrc = computed(() =>
  result.value?.gradcam_url
    ? `http://127.0.0.1:8000${result.value.gradcam_url}`
    : "https://via.placeholder.com/200x200?text=Grad-CAM"
);
</script>

<style scoped>
.result h2 {
  color: #234a7c;
  margin-bottom: 4px;
}
.confidence {
  font-size: 13px;
  color: #4b5c73;
  margin-bottom: 18px;
}
.content {
  display: flex;
  gap: 30px;
  align-items: flex-start;
}
.desc p {
  font-size: 14px;
  color: #4b5c73;
  margin-bottom: 10px;
  max-width: 380px;
}
.note {
  font-size: 12px;
  color: #7c8ca3;
}
.images {
  display: flex;
  gap: 16px;
}
.img-card {
  background-color: #ffffff;
  padding: 10px;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}
.img-card img {
  width: 180px;
  height: 180px;
  object-fit: cover;
  border-radius: 8px;
}
.warning {
  margin-top: 18px;
  font-size: 11px;
  padding: 10px;
  border-radius: 6px;
  background-color: #fff9e6;
  color: #775a10;
}
.no-data {
  text-align: center;
}
.no-data button {
  margin-top: 10px;
  padding: 8px 16px;
  border-radius: 6px;
  border: none;
  background: #234a7c;
   cursor: pointer;
}
@media (max-width: 900px) {
  .content {
    flex-direction: column;
  }
  .images {
    justify-content: center;
  }
}
</style>
