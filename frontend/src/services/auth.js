// Authentication service for managing user authentication state
const AUTH_TOKEN_KEY = 'dermasense_auth_token';
const AUTH_USER_KEY = 'dermasense_auth_user';

export const authService = {
  // Get token from localStorage
  getToken() {
    return localStorage.getItem(AUTH_TOKEN_KEY);
  },

  // Get user from localStorage
  getUser() {
    const userStr = localStorage.getItem(AUTH_USER_KEY);
    return userStr ? JSON.parse(userStr) : null;
  },

  // Save token and user to localStorage
  setAuth(token, user) {
    localStorage.setItem(AUTH_TOKEN_KEY, token);
    localStorage.setItem(AUTH_USER_KEY, JSON.stringify(user));
  },

  // Clear authentication data
  clearAuth() {
    localStorage.removeItem(AUTH_TOKEN_KEY);
    localStorage.removeItem(AUTH_USER_KEY);
  },

  // Check if user is authenticated
  isAuthenticated() {
    return !!this.getToken();
  },

  // Get authorization header
  getAuthHeader() {
    const token = this.getToken();
    return token ? { Authorization: `Bearer ${token}` } : {};
  }
};

