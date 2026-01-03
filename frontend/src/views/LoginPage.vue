<template>
  <div class="login-container fade-in">
    <div class="login-card">
      <div class="login-header">
        <div class="logo-container">
          <div class="logo-icon">🔬</div>
        </div>
        <h1>Welcome Back</h1>
        <p class="subtitle">Sign in to your DermaSense account</p>
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <div class="form-group">
          <label for="username">Username or Email</label>
          <input
            id="username"
            v-model="username"
            type="text"
            required
            placeholder="Enter your username or email"
            :disabled="loading"
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            placeholder="Enter your password"
            :disabled="loading"
          />
        </div>

        <button type="submit" class="login-button" :disabled="loading">
          <span v-if="!loading">Sign In</span>
          <span v-else>Signing In...</span>
        </button>
      </form>

      <div class="login-footer">
        <p>
          Don't have an account?
          <router-link to="/register" class="link">Sign up here</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { authApi } from '@/api/auth';
import { authService } from '@/services/auth';

const router = useRouter();
const username = ref('');
const password = ref('');
const loading = ref(false);
const error = ref('');

const handleLogin = async () => {
  error.value = '';
  loading.value = true;

  try {
    const response = await authApi.login(username.value, password.value);
    
    // Save token and user
    authService.setAuth(response.access_token, response.user);
    
    // Redirect to dashboard
    router.push('/dashboard');
  } catch (err) {
    error.value = err.response?.data?.detail || 'Login failed. Please check your credentials.';
    console.error('Login error:', err);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 200px);
  padding: var(--spacing-xl);
}

.login-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: var(--radius-xl);
  padding: var(--spacing-2xl);
  box-shadow: 0 8px 32px rgba(0, 102, 204, 0.12);
  border: 1px solid rgba(0, 102, 204, 0.1);
  width: 100%;
  max-width: 440px;
}

.login-header {
  text-align: center;
  margin-bottom: var(--spacing-2xl);
}

.logo-container {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, var(--medical-blue) 0%, var(--medical-teal) 100%);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto var(--spacing-md);
  box-shadow: var(--shadow-colored);
}

.logo-icon {
  font-size: 32px;
}

.login-header h1 {
  font-size: 32px;
  color: var(--medical-gray-900);
  margin-bottom: var(--spacing-sm);
  font-weight: 700;
  background: linear-gradient(135deg, var(--medical-blue) 0%, var(--medical-teal) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  font-size: 16px;
  color: var(--medical-gray-600);
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.error-message {
  background: #fee;
  color: #c33;
  padding: var(--spacing-md);
  border-radius: var(--radius-md);
  border: 1px solid #fcc;
  font-size: 14px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.form-group label {
  font-size: 14px;
  font-weight: 600;
  color: var(--medical-gray-700);
}

.form-group input {
  padding: var(--spacing-md);
  border: 2px solid var(--medical-gray-200);
  border-radius: var(--radius-md);
  font-size: 15px;
  transition: all var(--transition-base);
  background: white;
}

.form-group input:focus {
  outline: none;
  border-color: var(--medical-blue);
  box-shadow: 0 0 0 3px var(--medical-blue-light);
}

.form-group input:disabled {
  background: var(--medical-gray-100);
  cursor: not-allowed;
}

.login-button {
  padding: var(--spacing-md) var(--spacing-xl);
  background: linear-gradient(135deg, var(--medical-blue) 0%, var(--medical-teal) 100%);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-base);
  margin-top: var(--spacing-sm);
}

.login-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 102, 204, 0.3);
}

.login-button:active:not(:disabled) {
  transform: translateY(0);
}

.login-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.login-footer {
  margin-top: var(--spacing-xl);
  text-align: center;
  padding-top: var(--spacing-xl);
  border-top: 1px solid var(--medical-gray-200);
}

.login-footer p {
  font-size: 14px;
  color: var(--medical-gray-600);
}

.link {
  color: var(--medical-blue);
  text-decoration: none;
  font-weight: 600;
  transition: color var(--transition-base);
}

.link:hover {
  color: var(--medical-teal);
  text-decoration: underline;
}

@media (max-width: 480px) {
  .login-card {
    padding: var(--spacing-xl);
  }
  
  .login-header h1 {
    font-size: 28px;
  }
}
</style>

