<template>
  <div class="register-container fade-in">
    <div class="register-card">
      <div class="register-header">
        <div class="logo-container">
          <div class="logo-icon">🔬</div>
        </div>
        <h1>Create Account</h1>
        <p class="subtitle">Join DermaSense to start monitoring your skin health</p>
      </div>

      <form @submit.prevent="handleRegister" class="register-form">
        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <div class="form-group">
          <label for="fullName">Full Name (Optional)</label>
          <input
            id="fullName"
            v-model="fullName"
            type="text"
            placeholder="Enter your full name"
            :disabled="loading"
          />
        </div>

        <div class="form-group">
          <label for="email">Email *</label>
          <input
            id="email"
            v-model="email"
            type="email"
            required
            placeholder="Enter your email"
            :disabled="loading"
          />
        </div>

        <div class="form-group">
          <label for="username">Username *</label>
          <input
            id="username"
            v-model="username"
            type="text"
            required
            placeholder="Choose a username"
            :disabled="loading"
          />
        </div>

        <div class="form-group">
          <label for="password">Password *</label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            placeholder="Create a password"
            :disabled="loading"
            minlength="6"
          />
          <small class="form-hint">Password must be at least 6 characters</small>
        </div>

        <div class="form-group">
          <label for="confirmPassword">Confirm Password *</label>
          <input
            id="confirmPassword"
            v-model="confirmPassword"
            type="password"
            required
            placeholder="Confirm your password"
            :disabled="loading"
          />
        </div>

        <button type="submit" class="register-button" :disabled="loading || !isFormValid">
          <span v-if="!loading">Create Account</span>
          <span v-else>Creating Account...</span>
        </button>
      </form>

      <div class="register-footer">
        <p>
          Already have an account?
          <router-link to="/login" class="link">Sign in here</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { authApi } from '@/api/auth';
import { authService } from '@/services/auth';

const router = useRouter();
const fullName = ref('');
const email = ref('');
const username = ref('');
const password = ref('');
const confirmPassword = ref('');
const loading = ref(false);
const error = ref('');

const isFormValid = computed(() => {
  return email.value && 
         username.value && 
         password.value && 
         password.value === confirmPassword.value &&
         password.value.length >= 6;
});

const handleRegister = async () => {
  error.value = '';

  // Validate passwords match
  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match';
    return;
  }

  if (password.value.length < 6) {
    error.value = 'Password must be at least 6 characters';
    return;
  }

  loading.value = true;

  try {
    const userData = {
      email: email.value,
      username: username.value,
      password: password.value,
      full_name: fullName.value || null,
    };

    const user = await authApi.register(userData);
    
    // After registration, automatically log in
    const loginResponse = await authApi.login(username.value, password.value);
    authService.setAuth(loginResponse.access_token, loginResponse.user);
    
    // Redirect to dashboard
    router.push('/dashboard');
  } catch (err) {
    error.value = err.response?.data?.detail || 'Registration failed. Please try again.';
    console.error('Registration error:', err);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.register-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 200px);
  padding: var(--spacing-xl);
}

.register-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: var(--radius-xl);
  padding: var(--spacing-2xl);
  box-shadow: 0 8px 32px rgba(0, 102, 204, 0.12);
  border: 1px solid rgba(0, 102, 204, 0.1);
  width: 100%;
  max-width: 480px;
}

.register-header {
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

.register-header h1 {
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

.register-form {
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

.form-hint {
  font-size: 12px;
  color: var(--medical-gray-500);
  margin-top: -4px;
}

.register-button {
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

.register-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 102, 204, 0.3);
}

.register-button:active:not(:disabled) {
  transform: translateY(0);
}

.register-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.register-footer {
  margin-top: var(--spacing-xl);
  text-align: center;
  padding-top: var(--spacing-xl);
  border-top: 1px solid var(--medical-gray-200);
}

.register-footer p {
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
  .register-card {
    padding: var(--spacing-xl);
  }
  
  .register-header h1 {
    font-size: 28px;
  }
}
</style>

