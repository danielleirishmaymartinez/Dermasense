<template>
  <div class="about-container">
    <!-- Main About Section -->
    <section class="about-section">
      <div class="about-hero">
        <h1>About DermaSense</h1>
        <p class="hero-subtitle">
          Supporting early checking of skin lesions with AI assisted image analysis
        </p>
      </div>

      <div class="about-content-wrapper">
        <div class="about-main-content">
          <div class="intro-card">
            <h2>What is DermaSense?</h2>
            <p>
              DermaSense is a decision-support tool that helps users and dermatologists in the early checking of
               suspicious skin lesions. The system analyzes uploaded images together with optional details 
               such as age, sex, and lesion site to highlight patterns that may need further medical attention.
            </p> <br></br>
            <p>
              DermaSense does not provide a medical diagnosis and should always be used as an 
              aid only, together with a consultation from a licensed health professional.
            </p>
          </div>

          <div class="features-grid">
            <div class="feature-box">
              <div class="feature-number">01</div>
              <h3>Image Screening</h3>
              <p>AI assisted review of dermoscopic and clinical images to flag skin lesions that 
                may require closer examination or follow up.</p>
            </div>
            <div class="feature-box">
              <div class="feature-number">02</div>
              <h3>Clinical Context</h3>
              <p>Optional entry of patient age, sex, and lesion location to give more 
                tailored risk hints and support clinical judgment.</p>
            </div>
            <div class="feature-box">
              <div class="feature-number">03</div>
              <h3>Results and Guidance</h3>
              <p>Clear summaries and simple next-step suggestions (such as “monitor” or “seek a dermatologist”) 
                to support early detection and informed decision-making, without replacing professional medical advice.</p>
            </div> 
          </div>

        </div>
      </div>
    </section>

    <!-- How It Works Section -->
    <section class="how-it-works-section">
      <div class="section-header">
        <h2>How It Works</h2>
        <p>Simple steps to get your skin lesion analyzed</p>
      </div>
      <div class="steps-container">
        <div class="step-card">
          <div class="step-number">1</div>
          <div class="step-content">
            <h3>Upload Image</h3>
            <p>Upload a dermoscopic or clinical photo of the skin lesion you want to check.</p>
            <em>“The system only helps you review the image. It does not give a final diagnosis.”</em>
          </div>
        </div>
        <div class="step-arrow">→</div>
        <div class="step-card">
          <div class="step-number">2</div>
          <div class="step-content">
            <h3>Add Details (Optional)</h3>
            <p>You can optionally add age, sex, and lesion location to give more context and
               help the system highlight patterns more clearly.</p>
          </div>
        </div>
        <div class="step-arrow">→</div>
        <div class="step-card">
          <div class="step-number">3</div>
          <div class="step-content">
            <h3>View AI-Assisted Results</h3>
            <p>View AI-assisted results and simple next-step 
              suggestions; results are informational only and do not replace a licensed healthcare professional.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Mission & Vision Section -->
    <section class="mission-section">
      <div class="mission-grid">
        <div class="mission-card">
          <img src="@/assets/mission.png" alt="Mission" class="mission-icon" />
          <h3>Our Mission</h3>
          <p>
            To make AI-assisted skin lesion checking more accessible, 
            supporting both healthcare professionals and individuals with tools that 
            encourage early consultation and awareness, not self-diagnosis.
          </p>
        </div>
        <div class="mission-card">
          <img src="@/assets/shared-vision.png" alt="Vision" class="mission-icon" />
          <h3>Our Vision</h3>
          <p>
            To be a trusted support tool in dermatology decision-making, 
            combining advanced technology with medical expertise to help people and 
            clinicians make more informed choices about skin health.
          </p>
        </div>
      </div>
    </section>


    <!-- Classification Types Section -->
    <section class="classification-section">
      <div class="class-header">
        <h2>Classification Types</h2>
        <p>Understanding the main skin lesion categories used in DermaSense.</p>
      </div>
      <div class="class-grid">
        <div class="class-card benign">
          <img src="@/assets/breast.png" alt="Vision" class="mission-icon" />
          <h3>Benign</h3>
          <p>
            Non-cancerous growths such as moles and freckles that are usually harmless and do not need urgent treatment.
          </p>
        </div>
        <div class="class-card bcc">
          <img src="@/assets/basal-cell-carcinoma.png" alt="Vision" class="mission-icon" />
          <h3>Basal Cell Carcinoma (BCC)</h3>
          <p>
            A common skin cancer that grows slowly and rarely spreads; early check-up helps achieve better treatment outcomes.
          </p>
        </div>
        <div class="class-card scc">
          <img src="@/assets/squamous-cell-carcinoma.png" alt="Vision" class="mission-icon" />
          <h3>Squamous Cell Carcinoma (SCC)</h3>
          <p>
            Another common skin cancer that may grow and spread faster than BCC, so early detection and treatment are essential.
          </p>
        </div>
      </div>
    </section>

              <!-- DISCLAIMER -->
              <div class="disclaimer-box">
            <div class="disclaimer-icon">⚠️</div>
            <div class="disclaimer-content">
              <strong>Important Disclaimer:</strong>
              <p>
                DermaSense is not a diagnostic tool. Only a licensed dermatologist can make a 
                final diagnosis. This system is for educational and decision-support use only.
              </p>
            </div>
          </div>
  </div>
</template>

<style scoped>
.about-container {
  width: 100%;
}

/* Section background */
.about-section {
  padding: 40px 0 60px;
  background: linear-gradient(
    135deg,
    var(--medical-gray-50) 0%,
    var(--medical-teal-light) 100%
  );
}

/* Hero Section */
.about-hero {
  text-align: center;
  max-width: 1150px;
  margin: 0 auto 60px;
  padding: 0 20px;
}

.about-hero h1 {
  font-size: 38px; /* Adjusted the size */
  font-weight: 700;
  color: var(--medical-gray-900);
  margin-bottom: 16px;
  font-family: 'Inter', 'Roboto', sans-serif;
  letter-spacing: -0.5px;
}

.hero-subtitle {
  font-size: 20px;
  color: var(--medical-gray-700);
  max-width: 700px;
  margin: 0 auto;
  line-height: 1.6;
}

/* Main Content Wrapper */
.about-content-wrapper {
  max-width: 1150px;
  margin: 0 auto;
  padding: 0 20px;
}

.about-main-content {
  display: flex;
  flex-direction: column;
  gap: 40px;
}

/* Intro Card */
.intro-card {
  background: var(--medical-white);
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 102, 204, 0.1);
  border: 1px solid var(--medical-gray-200);
}

.intro-card h2 {
  font-size: 28px; /* Adjusted the size */
  font-weight: 700;
  color: var(--medical-gray-900);
  margin-bottom: 20px;
  border-bottom: 3px solid var(--medical-blue);
  padding-bottom: 12px;
}

.intro-card p {
  font-size: 17px;
  line-height: 1.8;
  color: var(--medical-gray-700);
}

/* Features Grid */
.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}

.feature-box {
  background: var(--medical-white);
  padding: 32px 28px;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 102, 204, 0.1);
  border: 2px solid var(--medical-gray-200);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.feature-box::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(135deg, var(--medical-blue) 0%, var(--medical-teal) 100%);
  transform: scaleY(0);
  transition: transform 0.3s ease;
}

.feature-box:hover::before {
  transform: scaleY(1);
}

.feature-box:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 102, 204, 0.2);
  border-color: var(--medical-blue);
}

.feature-number {
  font-size: 48px;
  font-weight: 700;
  color: var(--medical-blue-light);
  line-height: 1;
  margin-bottom: 16px;
  font-family: 'Inter', 'Roboto', sans-serif;
}

.feature-box h3 {
  font-size: 22px;
  font-weight: 700;
  color: var(--medical-gray-900);
  margin-bottom: 12px;
}

.feature-box p {
  font-size: 15px;
  line-height: 1.7;
  color: var(--medical-gray-700);
}

/* Classification Section Inline */
.classification-section-inline {
  background: var(--medical-white);
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 102, 204, 0.1);
  border: 1px solid var(--medical-gray-200);
}

.classification-section-inline h2 {
  font-size: 32px;
  font-weight: 700;
  color: var(--medical-gray-900);
  margin-bottom: 12px;
  border-bottom: 3px solid var(--medical-blue);
  padding-bottom: 12px;
}

.section-description {
  font-size: 16px;
  color: var(--medical-gray-700);
  margin-bottom: 28px;
  line-height: 1.7;
}

.classification-cards {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.class-item {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px;
  background: var(--medical-gray-50);
  border-radius: 12px;
  border-left: 4px solid transparent;
  transition: all 0.3s ease;
}

.class-item:hover {
  background: var(--medical-blue-light);
  transform: translateX(4px);
}

.class-indicator {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  flex-shrink: 0;
}

.benign-indicator {
  background: var(--medical-green);
}

.bcc-indicator {
  background: var(--medical-teal);
}

.scc-indicator {
  background: var(--medical-red);
}

.class-info h4 {
  font-size: 18px;
  font-weight: 700;
  color: var(--medical-gray-900);
  margin-bottom: 4px;
}

.class-info p {
  font-size: 14px;
  color: var(--medical-gray-700);
  line-height: 1.6;
}

/* Value Proposition */
.value-proposition {
  background: linear-gradient(135deg, var(--medical-blue) 0%, var(--medical-teal) 100%);
  padding: 48px 40px;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 102, 204, 0.2);
}

.value-content h2 {
  font-size: 32px;
  font-weight: 700;
  color: var(--medical-white);
  margin-bottom: 20px;
}

.value-content p {
  font-size: 17px;
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.95);
}

/* Disclaimer Box */
.disclaimer-box {
  background: linear-gradient(135deg, var(--medical-red-light) 0%, #FFE5E5 100%);
  border-left: 4px solid var(--medical-red);
  padding: 24px;
  border-radius: 12px;
  display: flex;
  gap: 16px;
  align-items: flex-start;
  box-shadow: 0 4px 12px rgba(220, 53, 69, 0.15);
}

.disclaimer-icon {
  font-size: 32px;
  flex-shrink: 0;
}

.disclaimer-content {
  flex: 1;
}

.disclaimer-content strong {
  display: block;
  font-size: 16px;
  color: #d32f2f;
  font-weight: 700;
  margin-bottom: 8px;
}

.disclaimer-content p {
  font-size: 14px;
  line-height: 1.7;
  color: #d32f2f;
  margin: 0;
}

/* How It Works Section */
.how-it-works-section {
  margin: 60px 0;
  padding: 50px 0;
  background: linear-gradient(135deg, var(--medical-white) 0%, var(--medical-teal-light) 100%);
  border-radius: 12px;
}

.section-header {
  text-align: center;
  max-width: 1150px;
  margin: 0 auto 48px;
  padding: 0 20px;
}

.section-header h2 {
  font-size: 36px;
  color: var(--medical-gray-900);
  margin-bottom: 16px;
  font-weight: 700;
}

.section-header p {
  font-size: 18px;
  color: var(--medical-gray-700);
  max-width: 600px;
  margin: 0 auto;
}

.steps-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 24px;
  max-width: 1150px;
  margin: 0 auto;
  padding: 0 20px;
  flex-wrap: wrap;
}

.step-card {
  flex: 1;
  min-width: 250px;
  background: var(--medical-white);
  padding: 32px 28px;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 102, 204, 0.1);
  border: 2px solid var(--medical-blue-light);
  text-align: center;
  transition: all 0.3s ease;
  position: relative;
}

.step-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 102, 204, 0.2);
  border-color: var(--medical-blue);
}

.step-number {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, var(--medical-blue) 0%, var(--medical-teal) 100%);
  color: var(--medical-white);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  font-weight: 700;
  margin: 0 auto 20px;
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
}

.step-content h3 {
  font-size: 20px;
  color: var(--medical-gray-900);
  margin-bottom: 12px;
  font-weight: 700;
}

.step-content p {
  font-size: 15px;
  color: var(--medical-gray-700);
  line-height: 1.7;
}

.step-arrow {
  font-size: 32px;
  color: var(--medical-blue);
  font-weight: 700;
}

/* Mission Section */
.mission-section {
  margin: 60px 0;
  padding: 0;
}

.mission-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
  max-width: 1150px;
  margin: 0 auto;
}

.mission-card {
  background: linear-gradient(135deg, var(--medical-white) 0%, var(--medical-blue-light) 100%);
  padding: 40px 32px;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 102, 204, 0.12);
  border: 2px solid var(--medical-blue-light);
  text-align: center;
  transition: all 0.3s ease;
}

.mission-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 32px rgba(0, 102, 204, 0.2);
  border-color: var(--medical-blue);
}

.mission-icon {
  width: 80px;
  height: 80px;
  object-fit: contain;
  margin-bottom: 20px;
  display: block;
  margin-left: auto;
  margin-right: auto;
}

.mission-card h3 {
  font-size: 24px;
  color: var(--medical-gray-900);
  margin-bottom: 16px;
  font-weight: 700;
}

.mission-card p {
  font-size: 16px;
  color: var(--medical-gray-700);
  line-height: 1.8;
}

/* Technology Section */
.technology-section {
  margin: 60px 0;
  padding: 50px 0;
  background: linear-gradient(135deg, var(--medical-gray-50) 0%, var(--medical-teal-light) 100%);
  border-radius: 12px;
}

.tech-header {
  text-align: center;
  max-width: 1150px;
  margin: 0 auto 48px;
  padding: 0 20px;
}

.tech-header h2 {
  font-size: 36px;
  color: var(--medical-gray-900);
  margin-bottom: 16px;
  font-weight: 700;
}

.tech-header p {
  font-size: 18px;
  color: var(--medical-gray-700);
  max-width: 600px;
  margin: 0 auto;
}

.tech-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
  max-width: 1150px;
  margin: 0 auto;
  padding: 0 20px;
}

.tech-card {
  background: var(--medical-white);
  padding: 32px 24px;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 102, 204, 0.1);
  border: 2px solid var(--medical-gray-200);
  text-align: center;
  transition: all 0.3s ease;
}

.tech-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 102, 204, 0.2);
  border-color: var(--medical-blue);
}

.tech-card h4 {
  font-size: 20px;
  color: var(--medical-gray-900);
  margin-bottom: 12px;
  font-weight: 700;
}

.tech-card p {
  font-size: 14px;
  color: var(--medical-gray-700);
  line-height: 1.6;
}

/* Classification Section */
.classification-section {
  margin: 60px 0;
  padding: 50px 0;
  background: linear-gradient(135deg, var(--medical-white) 0%, var(--medical-blue-light) 100%);
  border-radius: 12px;
}

.class-header {
  text-align: center;
  max-width: 1150px;
  margin: 0 auto 48px;
  padding: 0 20px;
}

.class-header h2 {
  font-size: 36px;
  color: var(--medical-gray-900);
  margin-bottom: 16px;
  font-weight: 700;
}

.class-header p {
  font-size: 18px;
  color: var(--medical-gray-700);
  max-width: 600px;
  margin: 0 auto;
}

.class-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
  max-width: 1150px;
  margin: 0 auto;
  padding: 0 20px;
}

.class-card {
  background: var(--medical-white);
  padding: 32px 28px;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 102, 204, 0.1);
  border: 2px solid var(--medical-gray-200);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.class-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--medical-blue);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.class-card.benign::before {
  background: var(--medical-green);
}

.class-card.bcc::before {
  background: var(--medical-teal);
}

.class-card.scc::before {
  background: var(--medical-red);
}

.class-card:hover::before {
  transform: scaleX(1);
}

.class-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 102, 204, 0.2);
}

.class-card h3 {
  font-size: 22px;
  color: var(--medical-gray-900);
  margin-bottom: 16px;
  font-weight: 700;
  text-align: center;
}

.class-card p {
  font-size: 15px;
  color: var(--medical-gray-700);
  line-height: 1.7;
  text-align: center;
}

/* Responsive for mobile */
@media (max-width: 900px) {
  .about-hero h1 {
    font-size: 36px;
  }

  .hero-subtitle {
    font-size: 18px;
  }

  .intro-card,
  .classification-section-inline,
  .value-proposition {
    padding: 32px 24px;
  }

  .intro-card h2,
  .classification-section-inline h2,
  .value-content h2 {
    font-size: 28px;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .mission-grid,
  .class-grid {
    grid-template-columns: 1fr;
  }

  .class-header h2,
  .section-header h2 {
    font-size: 28px;
  }

  .steps-container {
    flex-direction: column;
  }

  .step-arrow {
    transform: rotate(90deg);
    margin: 8px 0;
  }

  .disclaimer-box {
    flex-direction: column;
    text-align: center;
  }

  .disclaimer-icon {
    margin: 0 auto;
  }
}
</style>
