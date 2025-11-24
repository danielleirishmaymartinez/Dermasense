// frontend/src/api/dermasenseApi.js

const BASE_URL = "http://127.0.0.1:8000"; // FastAPI backend

/**
 * Send an image file to the backend /predict endpoint.
 * Returns: { filename, predicted_label, confidence, probabilities }
 */
export async function classifyLesion(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${BASE_URL}/predict`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Backend error (${response.status}): ${text}`);
  }

  return await response.json();
}
