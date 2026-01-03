// frontend/src/api/client.js
import axios from "axios";
import { authService } from "@/services/auth";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  timeout: 60000, // 60 seconds for ML inference
});

// Add request interceptor for authentication and logging
api.interceptors.request.use(
  (config) => {
    // Add authentication token if available
    const token = authService.getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.code === 'ECONNABORTED') {
      console.error('Request timeout - the server took too long to respond');
    } else if (error.response) {
      // Server responded with error status
      const status = error.response.status;
      console.error('API Error:', status, error.response.data);
      
      // Handle 401 Unauthorized - clear auth and redirect to login
      if (status === 401) {
        authService.clearAuth();
        // Only redirect if not already on login/register page
        const currentPath = window.location.pathname;
        if (!currentPath.includes('/login') && !currentPath.includes('/register')) {
          window.location.href = '/login';
        }
      }
    } else if (error.request) {
      // Request made but no response received
      console.error('Network Error - Is the backend server running?', error.request);
    } else {
      // Something else happened
      console.error('Error:', error.message);
    }
    return Promise.reject(error);
  }
);

export default api;
