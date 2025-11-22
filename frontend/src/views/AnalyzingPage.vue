<template>
  <section class="analyzing">
    <div class="card">
      <h2>Analyzing Image…</h2>
      <div class="spinner"></div>
      <p>Please wait while the system processes the lesion image.</p>
    </div>
  </section>
</template>

<style scoped>
.analyzing {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
  padding: 40px 20px;
}

.card {
  position: relative;
  background-color: var(--medical-white);
  border-radius: 16px;
  padding: 48px 50px;
  text-align: center;
  max-width: 520px;
  box-shadow: 0 8px 32px rgba(0, 102, 204, 0.12);
  border: 1px solid var(--medical-gray-200);
}

h2 {
  color: var(--medical-gray-900);
  margin-bottom: 24px;
  font-size: 26px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

h2::before {
  content: "🔬";
  font-size: 32px;
}

p {
  color: var(--medical-gray-700);
  font-size: 16px;
  line-height: 1.6;
  margin-top: 8px;
}

.spinner {
  width: 56px;
  height: 56px;
  border: 4px solid var(--medical-blue-light);
  border-top-color: var(--medical-blue);
  border-right-color: var(--medical-teal);
  border-radius: 50%;
  margin: 0 auto 24px;
  animation: spin 1s linear infinite;
  position: relative;
}

.spinner::after {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 20px;
  height: 20px;
  background: var(--medical-teal-light);
  border-radius: 50%;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.card::before {
  content: "";
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: linear-gradient(135deg, var(--medical-blue), var(--medical-teal));
  border-radius: 16px;
  z-index: -1;
  opacity: 0.1;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 0.1;
  }
  50% {
    opacity: 0.2;
  }
}
</style>
