<template>
  <section class="about-section">
    <div class="about-card">
      
      <!-- LEFT SIDE — IMAGE -->
      <div class="about-image-wrapper">
        <img src="@/assets/About.jpg" class="about-image" alt="About-image" />
      </div>

      <!-- RIGHT SIDE — TEXT -->
      <div class="about-content">
        <h2>About DermaSense</h2>

        <p>
          DermaSense is a decision-support tool designed to assist dermatologists and users 
          in the early assessment of suspicious skin lesions. It analyzes uploaded images 
          together with optional details such as age, sex, and lesion site.
        </p>

        <p>
          The system classifies lesions into:
          <strong>Benign</strong>, <strong>Basal Cell Carcinoma (BCC)</strong>, and 
          <strong>Squamous Cell Carcinoma (SCC)</strong>.
          It provides insights to support learning and clinical evaluation.
        </p>

        <h3>How it Works</h3>
        <ul>
          <li>Upload a dermoscopic or clinical image of a lesion.</li>
          <li>Optionally enter age, sex, and lesion location.</li>
          <li>Receive classification, confidence score, and explanation.</li>
        </ul>

        <p class="disclaimer">
          <strong>Disclaimer:</strong> DermaSense is a research prototype and not a diagnostic tool. 
          Final evaluation must be performed by a licensed dermatologist.
        </p>
      </div>

    </div>
  </section>
</template>

<style scoped>
/* Section background */
.about-section {
  display: flex;
  justify-content: center;
  padding: 40px 0;
  background-color: #f7efe7; /* nude background */
}

/* Main card */
.about-card {
  display: flex;
  gap: 40px;
  background: #ffffff;
  border-radius: 24px;
  padding: 40px;
  max-width: 1150px;
  width: 100%;
  box-shadow: 0 12px 35px rgba(0, 0, 0, 0.08);
}

/* LEFT image block */
.about-image-wrapper {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.about-image {
  width: 100%;
  max-width: 420px;
  border-radius: 18px;
  object-fit: cover;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

/* RIGHT text block */
.about-content {
  flex: 1.3;
}

.about-content h2 {
  font-size: 36px;
  font-weight: 700;
  color: #2c2c2c;
  margin-bottom: 14px;
  font-family: "Poppins", sans-serif;
}

.about-content h3 {
  margin-top: 20px;
  font-size: 20px;
  font-weight: 600;
  color: #2c2c2c;
}

.about-content p {
  font-size: 16px;
  line-height: 1.55;
  color: #3a3a3a;
  margin-bottom: 12px;
}

ul {
  margin: 10px 0 20px 20px;
  color: #3a3a3a;
  font-size: 15px;
}

.disclaimer {
  background: #fff4d9;
  padding: 12px 16px;
  border-radius: 10px;
  font-size: 14px;
  color: #6b4e2d;
}

/* Responsive for mobile */
@media (max-width: 900px) {
  .about-card {
    flex-direction: column;
    padding: 25px;
  }

  .about-image {
    max-width: 100%;
  }
}
</style>
