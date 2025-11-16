<template>
  <section class="upload-card">
    <h2>Upload Skin Lesion Image</h2>

    <div class="layout">
      <div class="left">
        <div class="dropzone" @click="triggerFile">
          <input
            ref="fileInput"
            type="file"
            accept="image/*"
            hidden
            @change="onFileChange"
          />
          <p v-if="!previewUrl">Click to upload a skin lesion image</p>
          <img v-else :src="previewUrl" alt="Preview" />
        </div>
      </div>

      <div class="right">
        <h3>Optional Clinical Details</h3>
        <div class="grid">
          <div class="field">
            <label>Age</label>
            <input v-model="age" type="number" placeholder="e.g., 45" />
          </div>
          <div class="field">
            <label>Sex</label>
            <select v-model="sex">
              <option value="">Select</option>
              <option>Male</option>
              <option>Female</option>
            </select>
          </div>
          <div class="field">
            <label>Lesion Site</label>
            <select v-model="site">
              <option value="">Select</option>
              <option>Head / neck</option>
              <option>Trunk</option>
              <option>Upper extremity</option>
              <option>Lower extremity</option>
            </select>
          </div>
        </div>

        <button class="analyze" :disabled="!file" @click="submit">
          Analyze Image
        </button>

        <p v-if="error" class="error">{{ error }}</p>
      </div>
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
const age = ref("");
const sex = ref("");
const site = ref("");
const error = ref("");

const triggerFile = () => fileInput.value?.click();

const onFileChange = (e) => {
  const f = e.target.files?.[0];
  if (!f) return;
  file.value = f;
  previewUrl.value = URL.createObjectURL(f);
};

const submit = async () => {
  if (!file.value) return;
  error.value = "";

  router.push("/analyzing");

  try {
    const form = new FormData();
    form.append("file", file.value);
    form.append("age", age.value);
    form.append("sex", sex.value);
    form.append("site", site.value);

    const { data } = await api.post("/analyze", form);
    localStorage.setItem("analysisResult", JSON.stringify(data));
    router.push("/results");
  } catch (err) {
    console.error(err);
    localStorage.removeItem("analysisResult");
    localStorage.setItem("analysisError", "Failed to analyze image.");
    router.push("/results");
  }
};
</script>

<style scoped>
.upload-card {
  background-color: #ffffff;
  border-radius: 20px;
  padding: 32px 36px;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.05);
}

h2 {
  font-size: 28px;
  color: #262626;
  margin-bottom: 20px;
}

.layout {
  display: flex;
  gap: 32px;
  align-items: flex-start;
}

.left,
.right {
  flex: 1;
}

.dropzone {
  background-color: #fdf7f1;
  border-radius: 16px;
  padding: 32px;
  text-align: center;
  border: 2px dashed #d0b39a;
  cursor: pointer;
}

.dropzone p {
  color: #7a644f;
  font-size: 15px;
}

.dropzone img {
  max-width: 260px;
  max-height: 260px;
  object-fit: cover;
  border-radius: 14px;
}

h3 {
  font-size: 18px;
  color: #3f3f3f;
  margin-bottom: 14px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
  margin-bottom: 18px;
}

.field label {
  font-size: 13px;
  color: #5f5f5f;
  margin-bottom: 4px;
  display: block;
}

.field input,
.field select {
  width: 100%;
  padding: 9px 10px;
  border-radius: 8px;
  border: 1px solid #d7c3b2;
  font-size: 14px;
  background-color: #fff;
}

.analyze {
  margin-top: 10px;
  padding: 12px 24px;
  border: none;
  border-radius: 999px;
  background-color: #2f3a4c;
  color: #ffffff;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
}

.analyze:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.error {
  margin-top: 10px;
  color: #c53030;
  font-size: 13px;
}

@media (max-width: 900px) {
  .layout {
    flex-direction: column;
  }

  .grid {
    grid-template-columns: 1fr;
  }
}
</style>
