<template>
  <section class="analyzing">
    <div class="card">
      <div class="spinner-wrapper">
        <div class="spinner"></div>
        <svg class="check-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <h2>Analyzing Image</h2>
      <p>Please wait while the system processes the lesion image using machine learning models.</p>
      <div class="progress-steps">
        <div class="step active">
          <div class="step-dot"></div>
          <span>Uploading</span>
        </div>
        <div class="step-line"></div>
        <div class="step">
          <div class="step-dot"></div>
          <span>Processing</span>
        </div>
        <div class="step-line"></div>
        <div class="step">
          <div class="step-dot"></div>
          <span>Analyzing</span>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.analyzing {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
  padding: 2.5rem 1.25rem;
}

.card {
  position: relative;
  background: white;
  border-radius: 1.25rem;
  padding: 3rem 3.5rem;
  text-align: center;
  max-width: 540px;
  width: 100%;
  box-shadow: 0 8px 32px rgba(37, 99, 235, 0.12);
  border: 1px solid #e2e8f0;
  animation: fadeIn 0.6s ease-out;
}

.spinner-wrapper {
  position: relative;
  width: 80px;
  height: 80px;
  margin: 0 auto 2rem;
}

.spinner {
  width: 80px;
  height: 80px;
  border: 4px solid #dbeafe;
  border-top-color: #2563eb;
  border-right-color: #06b6d4;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
}

.check-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 36px;
  height: 36px;
  stroke: #2563eb;
  stroke-width: 2.5;
  opacity: 0.3;
}

h2 {
  color: #1e293b;
  margin-bottom: 0.75rem;
  font-size: 1.75rem;
  font-weight: 700;
}

p {
  color: #64748b;
  font-size: 1rem;
  line-height: 1.6;
  margin-bottom: 2rem;
}

.progress-steps {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0;
  margin-top: 2rem;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  position: relative;
}

.step-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #cbd5e1;
  transition: all 0.3s ease;
}

.step.active .step-dot {
  background: linear-gradient(135deg, #2563eb, #06b6d4);
  box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.2);
  animation: pulse 2s ease-in-out infinite;
}

.step span {
  font-size: 0.75rem;
  color: #94a3b8;
  font-weight: 500;
}

.step.active span {
  color: #2563eb;
  font-weight: 600;
}

.step-line {
  width: 60px;
  height: 2px;
  background: #e2e8f0;
  margin: 0 0.5rem;
  margin-bottom: 1.5rem;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes pulse {
  0%, 100% {
    box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.2);
  }
  50% {
    box-shadow: 0 0 0 8px rgba(37, 99, 235, 0.1);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.card::before {
  content: "";
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: linear-gradient(135deg, #2563eb, #06b6d4);
  border-radius: 1.25rem;
  z-index: -1;
  opacity: 0.1;
  animation: bgPulse 2s ease-in-out infinite;
}

@keyframes bgPulse {
  0%, 100% {
    opacity: 0.1;
  }
  50% {
    opacity: 0.2;
  }
}

@media (max-width: 768px) {
  .card {
    padding: 2rem 1.5rem;
  }

  .progress-steps {
    flex-direction: column;
    gap: 1rem;
  }

  .step-line {
    width: 2px;
    height: 30px;
    margin: 0;
  }
}
</style>