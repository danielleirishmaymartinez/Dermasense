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

        <!-- HOW IT WORKS -->
        <h3>How it Works</h3>
        <ul class="how-list">
          <li>
            <span class="bullet-dot"></span>
            <span class="how-text">
              Upload a dermoscopic or clinical image of a lesion.
            </span>
          </li>
          <li>
            <span class="bullet-dot"></span>
            <span class="how-text">
              Optionally enter age, sex, and lesion location.
            </span>
          </li>
          <li>
            <span class="bullet-dot"></span>
            <span class="how-text">
              Receive classification, confidence score, and explanation.
            </span>
          </li>
        </ul>

        <!-- DISCLAIMER (plain text, red) -->
        <p class="disclaimer">
          <strong>Disclaimer:</strong>
          DermaSense is a research prototype and not a diagnostic tool. 
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
  background: linear-gradient(
    135deg,
    var(--medical-gray-50) 0%,
    var(--medical-teal-light) 100%
  );
}

/* Main card */
.about-card {
  display: flex;
  gap: 50px;
  background: var(--medical-white);
  border-radius: 16px;
  padding: 48px;
  max-width: 1150px;
  width: 100%;
  box-shadow: 0 12px 40px rgba(0, 102, 204, 0.12);
  border: 1px solid var(--medical-gray-200);
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
  border-radius: 12px;
  object-fit: cover;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  border: 3px solid var(--medical-blue-light);
  transition: transform 0.3s ease;
}

.about-image:hover {
  transform: scale(1.02);
}

/* RIGHT text block */
.about-content {
  flex: 1.3;
}

.about-content h2 {
  font-size: 38px;
  font-weight: 700;
  color: var(--medical-gray-900);
  margin-bottom: 20px;
  font-family: 'Inter', 'Roboto', sans-serif;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 3px solid var(--medical-blue);
  padding-bottom: 16px;
}

.about-content h2::before {
  content: "🏥";
  font-size: 42px;
}

/* HOW IT WORKS TITLE – a bit smaller */
.about-content h3 {
  margin-top: 28px;
  margin-bottom: 16px;
  font-size: 22px;              /* smaller now */
  font-weight: 700;
  color: var(--medical-blue-dark);
  letter-spacing: 0.02em;
  display: flex;
  align-items: center;
  gap: 10px;
}

.about-content h3::before {
  content: "⚙️";
  font-size: 26px;
}

.about-content p {
  font-size: 16px;
  line-height: 1.7;
  color: var(--medical-gray-700);
  margin-bottom: 16px;
}

.about-content p strong {
  color: var(--medical-blue-dark);
  font-weight: 600;
}

/* HOW IT WORKS – bullet cards with clearer shadow */
.how-list {
  list-style: none;
  margin: 0 0 24px 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.how-list li {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  background: #ffffff;
  border-radius: 12px;
  padding: 12px 14px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.10); /* stronger, more precise shadow */
  border: 1px solid var(--medical-gray-150, #e5ecf4);
}

.bullet-dot {
  width: 10px;
  height: 10px;
  border-radius: 999px;
  margin-top: 7px;
  background: var(--medical-teal);
}

.how-text {
  font-size: 15px;
  line-height: 1.7;
  color: var(--medical-gray-800);
}

.disclaimer {
  margin-top: 16px;
  font-size: 15px;
  line-height: 1.7;
  /* pure red text for the whole sentence */
  color: #d32f2f !important;
  font-weight: 500;
}

.disclaimer strong {
  /* keep the word “Disclaimer:” the same red */
  color: #d32f2f !important;
  font-weight: 700;
}


/* Responsive for mobile */
@media (max-width: 900px) {
  .about-card {
    flex-direction: column;
    padding: 32px 24px;
    gap: 30px;
  }

  .about-image {
    max-width: 100%;
  }

  .about-content h2 {
    font-size: 28px;
  }
}
</style>
