<template>
  <section class="landing">
    <div class="hero-card">
      <div class="left">
        <div class="illustration">
          <!-- Replace this with real illustration later -->
          👩‍⚕️
        </div>
      </div>
      <div class="right">
        <h1>Empowering Early Detection<br />Through AI Assistance</h1>
        <p>
          DermaSense assists dermatologists and users by classifying skin lesion
          images using AI and metadata, helping support early detection decisions.
        </p>
        <button class="cta" @click="$router.push('/upload')">
          Try it now
        </button>
      </div>
    </div>
  </section>
</template>

<style scoped>
.landing {
  display: flex;
  justify-content: center;
  padding-top: 10px;
}

.hero-card {
  width: 100%;
  max-width: 960px;
  background-color: #e3edf8;
  border-radius: 16px;
  padding: 32px 40px;
  display: flex;
  gap: 32px;
}

.left {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.illustration {
  width: 220px;
  height: 220px;
  background-color: #ffffff;
  border-radius: 18px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 64px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

.right {
  flex: 1.4;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.right h1 {
  font-size: 28px;
  color: #234a7c;
  margin-bottom: 12px;
}

.right p {
  color: #4b5c73;
  font-size: 14px;
  max-width: 420px;
  margin-bottom: 20px;
}

.cta {
  padding: 10px 24px;
  border-radius: 6px;
  border: none;
  background-color: #234a7c;
  color: #ffffff;
  font-size: 14px;
  cursor: pointer;
}

@media (max-width: 768px) {
  .hero-card {
    flex-direction: column;
    text-align: center;
    padding: 24px;
  }
  .right p {
    margin: 0 auto 20px;
  }
}
</style>
