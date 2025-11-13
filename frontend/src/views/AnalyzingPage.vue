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
}
.card {
  background-color: #e3edf8;
  border-radius: 16px;
  padding: 32px 40px;
  text-align: center;
  max-width: 480px;
}
h2 {
  color: #234a7c;
  margin-bottom: 18px;
}
p {
  color: #4b5c73;
  font-size: 14px;
}
.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #c4d4ea;
  border-top-color: #234a7c;
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
