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
  error.value = "";
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

    const { data } = await api.post("/predict", form);

    // Save backend result and image preview for ResultPage
    localStorage.setItem("analysisResult", JSON.stringify(data));
    if (previewUrl.value) {
      localStorage.setItem("analysisImage", previewUrl.value);
    } else {
      localStorage.removeItem("analysisImage");
    }
    localStorage.removeItem("analysisError");

    router.push("/results");
  } catch (err) {
    console.error(err);

    localStorage.removeItem("analysisResult");

    const detail =
      err?.response?.data?.detail ||
      "Failed to analyze image. Please try again.";
    localStorage.setItem("analysisError", detail);

    router.push("/results");
  }
};
</script>


<style scoped>
.upload-card {
  background-color: var(--medical-white);
  border-radius: 16px;
  padding: 40px 44px;
  box-shadow: 0 8px 24px rgba(0, 102, 204, 0.1);
  border: 1px solid var(--medical-gray-200);
}

h2 {
  font-size: 32px;
  color: var(--medical-gray-900);
  margin-bottom: 32px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 12px;
}

h2::before {
  content: "📤";
  font-size: 36px;
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

.dropzone {
  background: linear-gradient(135deg, var(--medical-blue-light) 0%, var(--medical-teal-light) 100%);
  border-radius: 12px;
  padding: 40px;
  text-align: center;
  border: 2px dashed var(--medical-blue);
  cursor: pointer;
  transition: all 0.3s ease;
  min-height: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
}

.dropzone:hover {
  border-color: var(--medical-blue-dark);
  background: linear-gradient(135deg, var(--medical-teal-light) 0%, var(--medical-blue-light) 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 102, 204, 0.15);
}

.dropzone p {
  color: var(--medical-blue-dark);
  font-size: 16px;
  font-weight: 500;
  margin-top: 12px;
}

.dropzone p::before {
  font-size: 48px;
  display: block;
  margin-bottom: 8px;
}

.dropzone img {
  max-width: 100%;
  max-height: 280px;
  object-fit: cover;
  border-radius: 10px;
  border: 2px solid var(--medical-white);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  z-index: 1;
}

h3 {
  font-size: 20px;
  color: var(--medical-gray-900);
  margin-bottom: 20px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}

h3::before {
  content: "📋";
  font-size: 24px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.field label {
  font-size: 14px;
  color: var(--medical-gray-700);
  margin-bottom: 8px;
  display: block;
  font-weight: 500;
}

.field input,
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

.field input:focus,
.field select:focus {
  outline: none;
  border-color: var(--medical-blue);
  box-shadow: 0 0 0 3px var(--medical-blue-light);
}

.analyze {
  margin-top: 8px;
  padding: 14px 32px;
  border: none;
  border-radius: 8px;
  background: linear-gradient(135deg, var(--medical-blue) 0%, var(--medical-teal) 100%);
  color: var(--medical-white);
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
  width: 100%;
}

.analyze:hover:not(:disabled) {
  background: linear-gradient(135deg, var(--medical-blue-dark) 0%, var(--medical-teal-dark) 100%);
  box-shadow: 0 6px 20px rgba(0, 102, 204, 0.4);
  transform: translateY(-2px);
}

.analyze:active:not(:disabled) {
  transform: translateY(0);
}

.analyze:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
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

@media (max-width: 900px) {
  .upload-card {
    padding: 30px 24px;
  }

  .layout {
    flex-direction: column;
    gap: 30px;
  }

  .grid {
    grid-template-columns: 1fr;
  }

  .dropzone {
    min-height: 250px;
  }
}
</style>
