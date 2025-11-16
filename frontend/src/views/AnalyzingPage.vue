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
  min-height: 320px;
}

.card {
  background-color: #ffffff;
  border-radius: 18px;
  padding: 32px 40px;
  text-align: center;
  max-width: 480px;
  box-shadow: 0 14px 30px rgba(0, 0, 0, 0.06);
}

h2 {
  color: #262626;
  margin-bottom: 18px;
  font-size: 22px;
}

p {
  color: #4f4f4f;
  font-size: 15px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3ded0;
  border-top-color: #c48b62;
  border-radius: 50%;
  margin: 0 auto 16px;
  animation: spin 0.9s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
