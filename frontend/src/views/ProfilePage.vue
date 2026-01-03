<template>
  <div class="profile-container fade-in">
    <div class="profile-header">
      <h1>User Profile</h1>
      <p class="subtitle">Manage your account information</p>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>Loading profile...</p>
    </div>

    <div v-else-if="error" class="error-state">
      <div class="error-icon">⚠️</div>
      <p>{{ error }}</p>
      <button @click="loadProfile" class="retry-button">Retry</button>
    </div>

    <div v-else class="profile-content">
      <!-- Profile Info Card -->
      <div class="profile-card">
        <div class="card-header">
          <div class="profile-avatar">
            <span class="avatar-icon">👤</span>
          </div>
          <h2>Account Information</h2>
        </div>
        
        <div class="card-body">
          <div class="info-item">
            <label>Username</label>
            <div class="info-value">{{ profile.username }}</div>
          </div>
          
          <div class="info-item">
            <label>Email</label>
            <div class="info-value">{{ profile.email }}</div>
          </div>
          
          <div class="info-item" v-if="profile.full_name">
            <label>Full Name</label>
            <div class="info-value">{{ profile.full_name }}</div>
          </div>
          
          <div class="info-item">
            <label>Member Since</label>
            <div class="info-value">{{ formatDate(profile.created_at) }}</div>
          </div>
          
          <div class="info-item">
            <label>Total Assessments</label>
            <div class="info-value highlight">{{ profile.total_assessments }}</div>
          </div>
        </div>
      </div>

      <!-- Statistics Card -->
      <div class="stats-card">
        <div class="card-header">
          <h2>Your Statistics</h2>
        </div>
        
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-icon">📊</div>
            <div class="stat-content">
              <div class="stat-value">{{ profile.total_assessments }}</div>
              <div class="stat-label">Total Assessments</div>
            </div>
          </div>
          
          <div class="stat-item">
            <div class="stat-icon">📅</div>
            <div class="stat-content">
              <div class="stat-value">{{ getDaysSinceJoin() }}</div>
              <div class="stat-label">Days Active</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Actions Card -->
      <div class="actions-card">
        <div class="card-header">
          <h2>Quick Actions</h2>
        </div>
        
        <div class="actions-list">
          <button @click="$router.push('/dashboard')" class="action-button">
            <span class="action-icon">📊</span>
            <span class="action-text">Go to Dashboard</span>
            <span class="action-arrow">→</span>
          </button>
          
          <button @click="$router.push('/upload')" class="action-button">
            <span class="action-icon">📸</span>
            <span class="action-text">New Assessment</span>
            <span class="action-arrow">→</span>
          </button>
          
          <button @click="$router.push('/monitoring')" class="action-button">
            <span class="action-icon">📈</span>
            <span class="action-text">View History</span>
            <span class="action-arrow">→</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { authApi } from '@/api/auth';

const profile = ref(null);
const loading = ref(true);
const error = ref('');

const loadProfile = async () => {
  loading.value = true;
  error.value = '';
  
  try {
    profile.value = await authApi.getUserProfile();
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to load profile. Please try again.';
    console.error('Profile load error:', err);
  } finally {
    loading.value = false;
  }
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

const getDaysSinceJoin = () => {
  if (!profile.value) return 0;
  const joinDate = new Date(profile.value.created_at);
  const today = new Date();
  const diffTime = Math.abs(today - joinDate);
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  return diffDays;
};

onMounted(() => {
  loadProfile();
});
</script>

<style scoped>
.profile-container {
  width: 100%;
  padding: 0;
}

.profile-header {
  margin-bottom: var(--spacing-2xl);
}

.profile-header h1 {
  font-size: 42px;
  color: var(--medical-gray-900);
  margin-bottom: var(--spacing-sm);
  font-weight: 800;
  background: linear-gradient(135deg, var(--medical-blue) 0%, var(--medical-teal) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -1px;
}

.subtitle {
  font-size: 18px;
  color: var(--medical-gray-600);
}

.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-4xl);
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: var(--radius-xl);
  box-shadow: 0 8px 32px rgba(0, 102, 204, 0.12);
  border: 1px solid rgba(0, 102, 204, 0.1);
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid var(--medical-gray-200);
  border-top-color: var(--medical-blue);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: var(--spacing-md);
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-icon {
  font-size: 48px;
  margin-bottom: var(--spacing-md);
}

.retry-button {
  padding: var(--spacing-md) var(--spacing-xl);
  background: var(--medical-blue);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-weight: 600;
  cursor: pointer;
  margin-top: var(--spacing-md);
  transition: all var(--transition-base);
}

.retry-button:hover {
  background: var(--medical-teal);
  transform: translateY(-2px);
}

.profile-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-xl);
}

.profile-card,
.stats-card,
.actions-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: var(--radius-xl);
  padding: var(--spacing-2xl);
  box-shadow: 0 8px 32px rgba(0, 102, 204, 0.12);
  border: 1px solid rgba(0, 102, 204, 0.1);
  transition: all var(--transition-base);
  animation: fadeIn 0.6s ease-out both;
}

.profile-card {
  grid-column: 1 / -1;
}

.profile-card:hover,
.stats-card:hover,
.actions-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 102, 204, 0.18);
}

.card-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-xl);
  padding-bottom: var(--spacing-md);
  border-bottom: 2px solid var(--medical-gray-200);
}

.profile-avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--medical-blue) 0%, var(--medical-teal) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-colored);
}

.avatar-icon {
  font-size: 32px;
}

.card-header h2 {
  font-size: 24px;
  color: var(--medical-gray-900);
  font-weight: 700;
  margin: 0;
}

.card-body {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.info-item label {
  font-size: 14px;
  font-weight: 600;
  color: var(--medical-gray-600);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-value {
  font-size: 18px;
  color: var(--medical-gray-900);
  font-weight: 500;
}

.info-value.highlight {
  color: var(--medical-blue);
  font-weight: 700;
  font-size: 24px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: var(--spacing-lg);
}

.stat-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-lg);
  background: var(--medical-gray-50);
  border-radius: var(--radius-md);
  border: 2px solid var(--medical-gray-200);
  transition: all var(--transition-base);
}

.stat-item:hover {
  border-color: var(--medical-blue);
  transform: translateY(-2px);
}

.stat-icon {
  font-size: 32px;
}

.stat-content {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--medical-blue);
  line-height: 1;
}

.stat-label {
  font-size: 14px;
  color: var(--medical-gray-600);
  margin-top: var(--spacing-xs);
}

.actions-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.action-button {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md) var(--spacing-lg);
  background: var(--medical-gray-50);
  border: 2px solid var(--medical-gray-200);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-base);
  text-align: left;
}

.action-button:hover {
  background: var(--medical-blue-light);
  border-color: var(--medical-blue);
  transform: translateX(4px);
}

.action-icon {
  font-size: 24px;
}

.action-text {
  flex: 1;
  font-size: 16px;
  font-weight: 600;
  color: var(--medical-gray-900);
}

.action-arrow {
  font-size: 20px;
  color: var(--medical-blue);
  font-weight: 700;
}

@media (max-width: 768px) {
  .profile-content {
    grid-template-columns: 1fr;
  }
  
  .profile-card {
    grid-column: 1;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>

