<template>
  <section class="landing">
    <div class="hero-card">
      <div class="left">
        <div class="illustration">
          👩‍⚕️
        </div>
      </div>
      <div class="right">
        <h1>
          Empowering Early Detection<br />
          Through AI Assistance
        </h1>
        <p>
          This system assists dermatologists and users by classifying skin lesion
          images using AI and basic clinical details.
        </p>
        <button class="cta" @click="$router.push('/upload')">Try it now</button>
      </div>
    </div>
  </section>
</template>

<style scoped>
.landing {
  min-height: calc(100vh - 70px); /* minus navbar height */
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-card {
  width: 100%;
  max-width: 1000px;
  background-color: #e3edf8;
  border-radius: 18px;
  padding: 32px 40px;
  display: flex;
  align-items: center;
  gap: 32px;
}

.left {
  flex: 1;
  display: flex;
  justify-content: center;
}

.right {
  flex: 1.3;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.illustration {
  width: 230px;
  height: 230px;
  background-color: #ffffff;
  border-radius: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 64px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

.right h1 {
  font-size: 28px;
  color: #234a7c;
  margin-bottom: 12px;
  line-height: 1.25;
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

.cta:hover {
  opacity: 0.9;
}

@media (max-width: 900px) {
  .landing {
    padding-top: 16px;
  }
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
