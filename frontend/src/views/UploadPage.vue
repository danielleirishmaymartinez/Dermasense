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
          <p v-if="!previewUrl">Upload skin lesion image here</p>
          <img v-else :src="previewUrl" alt="Preview" />
        </div>
      </div>

      <div class="right">
        <h3>Optional</h3>
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

  // go to analyzing page immediately
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
  background-color: #e3edf8;
  border-radius: 16px;
  padding: 24px 28px;
}
h2 {
  color: #234a7c;
  margin-bottom: 18px;
}
.layout {
  display: flex;
  gap: 26px;
  align-items: flex-start;
}
.left {
  flex: 1;
}
.right {
  flex: 1;
}
.dropzone {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 26px;
  text-align: center;
  border: 1px dashed #b3c6e2;
  cursor: pointer;
}
.dropzone p {
  color: #7c8ca3;
  font-size: 13px;
}
.dropzone img {
  max-width: 240px;
  max-height: 240px;
  object-fit: cover;
}
h3 {
  font-size: 14px;
  color: #6a7c96;
  margin-bottom: 10px;
}
.grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  margin-bottom: 14px;
}
.field label {
  font-size: 12px;
  color: #6a7c96;
  margin-bottom: 4px;
  display: block;
}
.field input,
.field select {
  width: 100%;
  padding: 8px;
  border-radius: 6px;
  border: 1px solid #c4d4ea;
  font-size: 13px;
}
.analyze {
  margin-top: 6px;
  padding: 10px 18px;
  border: none;
  border-radius: 8px;
  background-color: #234a7c;
  color: #ffffff;
  font-size: 14px;
  cursor: pointer;
}
.analyze:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.error {
  margin-top: 8px;
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
