// Authentication API endpoints
import api from './client';

export const authApi = {
  // Register a new user
  async register(userData) {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },

  // Login user
  async login(username, password) {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    
    const response = await api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data;
  },

  // Get current user info
  async getCurrentUser() {
    const response = await api.get('/auth/me');
    return response.data;
  },

  // Get user profile
  async getUserProfile() {
    const response = await api.get('/users/profile');
    return response.data;
  },
};

