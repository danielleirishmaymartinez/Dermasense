// frontend/src/api/client.js
import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000", // FastAPI backend
  timeout: 30000,
});

export default api;
