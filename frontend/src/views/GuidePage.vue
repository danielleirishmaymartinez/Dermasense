<template>
  <div class="guide-container fade-in">
    <div class="page-header">
      <h1>Skin Health Guide</h1>
      <p class="subtitle">Educational resources for skin health and self-examination</p>
    </div>

    <div class="guide-content">
      <!-- ABCDE Rule -->
      <section class="guide-section">
        <h2>🔍 The ABCDE Rule for Skin Lesions</h2>
        <p class="section-intro">
          The ABCDE rule is a helpful guide for identifying potentially concerning skin lesions. 
          Use this as a reference when examining your skin.
        </p>
        <div class="abcde-grid">
          <div class="abcde-item">
            <div class="abcde-letter">A</div>
            <h3>Asymmetry</h3>
            <p>One half of the lesion does not match the other half. Benign moles are typically symmetrical.</p>
          </div>
          <div class="abcde-item">
            <div class="abcde-letter">B</div>
            <h3>Border</h3>
            <p>Irregular, ragged, or blurred edges. Benign moles usually have smooth, even borders.</p>
          </div>
          <div class="abcde-item">
            <div class="abcde-letter">C</div>
            <h3>Color</h3>
            <p>Variation in color throughout the lesion, including shades of brown, black, red, white, or blue.</p>
          </div>
          <div class="abcde-item">
            <div class="abcde-letter">D</div>
            <h3>Diameter</h3>
            <p>Larger than 6mm (about the size of a pencil eraser), though smaller lesions can also be concerning.</p>
          </div>
          <div class="abcde-item">
            <div class="abcde-letter">E</div>
            <h3>Evolving</h3>
            <p>Changes in size, shape, color, or symptoms (itching, bleeding) over time.</p>
          </div>
        </div>
      </section>

      <!-- Photo-Taking Tips -->
      <section class="guide-section">
        <h2>📸 Photo-Taking Tips for Best Results</h2>
        <div class="tips-list">
          <div class="tip-item">
            <div class="tip-icon">1️⃣</div>
            <div class="tip-content">
              <h3>Good Lighting</h3>
              <p>Use natural daylight or bright, even lighting. Avoid shadows and harsh direct sunlight.</p>
            </div>
          </div>
          <div class="tip-item">
            <div class="tip-icon">2️⃣</div>
            <div class="tip-content">
              <h3>Close-Up Focus</h3>
              <p>Get close enough to clearly see the lesion details. The lesion should fill most of the frame.</p>
            </div>
          </div>
          <div class="tip-item">
            <div class="tip-icon">3️⃣</div>
            <div class="tip-content">
              <h3>Steady Camera</h3>
              <p>Hold the camera steady or use a tripod to avoid blurry images. Ensure the image is in focus.</p>
            </div>
          </div>
          <div class="tip-item">
            <div class="tip-icon">4️⃣</div>
            <div class="tip-content">
              <h3>Reference Object</h3>
              <p>Include a coin or ruler next to the lesion to provide scale and size reference.</p>
            </div>
          </div>
          <div class="tip-item">
            <div class="tip-icon">5️⃣</div>
            <div class="tip-content">
              <h3>Multiple Angles</h3>
              <p>Take photos from different angles if possible to capture all aspects of the lesion.</p>
            </div>
          </div>
          <div class="tip-item">
            <div class="tip-icon">6️⃣</div>
            <div class="tip-content">
              <h3>Clean Skin</h3>
              <p>Ensure the skin area is clean and free from lotions, makeup, or other substances.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- UV Protection -->
      <section class="guide-section">
        <h2>☀️ UV Protection Guidelines</h2>
        <div class="protection-grid">
          <div class="protection-card">
            <div class="protection-icon">🕶️</div>
            <h3>Sunscreen</h3>
            <p>Use broad-spectrum sunscreen with SPF 30 or higher. Reapply every 2 hours and after swimming or sweating.</p>
          </div>
          <div class="protection-card">
            <div class="protection-icon">👒</div>
            <h3>Protective Clothing</h3>
            <p>Wear long sleeves, pants, and wide-brimmed hats when spending time outdoors, especially during peak sun hours (10 AM - 4 PM).</p>
          </div>
          <div class="protection-card">
            <div class="protection-icon">🏖️</div>
            <h3>Seek Shade</h3>
            <p>Stay in the shade whenever possible, especially during midday when UV rays are strongest.</p>
          </div>
          <div class="protection-card">
            <div class="protection-icon">🚫</div>
            <h3>Avoid Tanning Beds</h3>
            <p>Tanning beds emit harmful UV radiation and increase skin cancer risk. Avoid them completely.</p>
          </div>
        </div>
      </section>

      <!-- Self-Examination -->
      <section class="guide-section">
        <h2>🔬 Regular Self-Examination</h2>
        <p class="section-intro">
          Perform regular self-examinations to monitor your skin health. Check your entire body monthly, 
          and use a mirror or ask a partner to help with hard-to-see areas.
        </p>
        <div class="examination-checklist">
          <div class="checklist-item">
            <span class="checkmark">✓</span>
            <span>Check your face, including nose, lips, and ears</span>
          </div>
          <div class="checklist-item">
            <span class="checkmark">✓</span>
            <span>Examine your scalp (use a comb to part hair)</span>
          </div>
          <div class="checklist-item">
            <span class="checkmark">✓</span>
            <span>Check your neck, chest, and torso</span>
          </div>
          <div class="checklist-item">
            <span class="checkmark">✓</span>
            <span>Examine your arms, including underarms and palms</span>
          </div>
          <div class="checklist-item">
            <span class="checkmark">✓</span>
            <span>Check your legs, including the back of your legs</span>
          </div>
          <div class="checklist-item">
            <span class="checkmark">✓</span>
            <span>Examine your feet, including soles and between toes</span>
          </div>
        </div>
      </section>

      <!-- When to See a Doctor -->
      <section class="guide-section warning-section">
        <h2>⚠️ When to Consult a Dermatologist</h2>
        <p class="section-intro">
          While self-examination is important, always consult a dermatologist if you notice:
        </p>
        <ul class="warning-list">
          <li>Any new or changing skin lesion</li>
          <li>A lesion that doesn't heal or continues to grow</li>
          <li>Bleeding, itching, or pain in a lesion</li>
          <li>Multiple atypical moles or a family history of skin cancer</li>
          <li>Any concern about a skin lesion, even if it seems minor</li>
        </ul>
        <div class="disclaimer-box">
          <strong>Remember:</strong> This guide is for educational purposes only. 
          It is not a substitute for professional medical advice, diagnosis, or treatment.
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
// No script needed for this static page
</script>

<style scoped>
.guide-container {
  width: 100%;
  padding: 0;
}

.page-header {
  margin-bottom: 40px;
}

.page-header h1 {
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

.guide-content {
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.guide-section {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: var(--radius-xl);
  padding: var(--spacing-2xl);
  box-shadow: 0 8px 32px rgba(0, 102, 204, 0.12);
  border: 1px solid rgba(0, 102, 204, 0.1);
  transition: all var(--transition-base);
  animation: fadeIn 0.6s ease-out both;
}

.guide-section:nth-child(1) { animation-delay: 0.1s; }
.guide-section:nth-child(2) { animation-delay: 0.2s; }
.guide-section:nth-child(3) { animation-delay: 0.3s; }
.guide-section:nth-child(4) { animation-delay: 0.4s; }
.guide-section:nth-child(5) { animation-delay: 0.5s; }

.guide-section:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 102, 204, 0.18);
}

.guide-section h2 {
  font-size: 28px;
  color: var(--medical-gray-900);
  margin-bottom: 16px;
  font-weight: 700;
}

.section-intro {
  font-size: 16px;
  color: var(--medical-gray-700);
  line-height: 1.7;
  margin-bottom: 24px;
}

.abcde-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 24px;
  margin-top: 24px;
}

.abcde-item {
  text-align: center;
  padding: 24px;
  background: var(--medical-gray-50);
  border-radius: 12px;
  border: 2px solid var(--medical-blue-light);
  transition: all 0.3s ease;
}

.abcde-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 102, 204, 0.15);
  border-color: var(--medical-blue);
}

.abcde-letter {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--medical-blue) 0%, var(--medical-teal) 100%);
  color: var(--medical-white);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  font-weight: 700;
  margin: 0 auto 16px;
}

.abcde-item h3 {
  font-size: 20px;
  color: var(--medical-gray-900);
  margin-bottom: 12px;
  font-weight: 600;
}

.abcde-item p {
  font-size: 14px;
  color: var(--medical-gray-700);
  line-height: 1.6;
  margin: 0;
}

.tips-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 24px;
}

.tip-item {
  display: flex;
  gap: 20px;
  padding: 20px;
  background: var(--medical-gray-50);
  border-radius: 12px;
  border-left: 4px solid var(--medical-blue);
}

.tip-icon {
  font-size: 32px;
  flex-shrink: 0;
}

.tip-content h3 {
  font-size: 18px;
  color: var(--medical-gray-900);
  margin-bottom: 8px;
  font-weight: 600;
}

.tip-content p {
  font-size: 15px;
  color: var(--medical-gray-700);
  line-height: 1.6;
  margin: 0;
}

.protection-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
  margin-top: 24px;
}

.protection-card {
  text-align: center;
  padding: 24px;
  background: linear-gradient(135deg, var(--medical-blue-light) 0%, var(--medical-teal-light) 100%);
  border-radius: 12px;
  border: 2px solid var(--medical-blue-light);
  transition: all 0.3s ease;
}

.protection-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 102, 204, 0.2);
  border-color: var(--medical-blue);
}

.protection-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.protection-card h3 {
  font-size: 20px;
  color: var(--medical-gray-900);
  margin-bottom: 12px;
  font-weight: 600;
}

.protection-card p {
  font-size: 14px;
  color: var(--medical-gray-700);
  line-height: 1.6;
  margin: 0;
}

.examination-checklist {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 24px;
}

.checklist-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: var(--medical-gray-50);
  border-radius: 8px;
  border-left: 4px solid #4caf50;
}

.checkmark {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #4caf50;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  flex-shrink: 0;
}

.checklist-item span:last-child {
  font-size: 15px;
  color: var(--medical-gray-700);
  line-height: 1.6;
}

.warning-section {
  background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
  border: 2px solid #ff9800;
}

.warning-list {
  list-style: none;
  padding: 0;
  margin: 24px 0;
}

.warning-list li {
  padding: 12px 0;
  padding-left: 32px;
  position: relative;
  font-size: 16px;
  color: var(--medical-gray-800);
  line-height: 1.7;
}

.warning-list li::before {
  content: "⚠️";
  position: absolute;
  left: 0;
  font-size: 20px;
}

.disclaimer-box {
  background: var(--medical-white);
  border-radius: 8px;
  padding: 16px;
  margin-top: 24px;
  border-left: 4px solid #ff9800;
}

.disclaimer-box strong {
  color: #e65100;
  display: block;
  margin-bottom: 8px;
}

.disclaimer-box {
  font-size: 14px;
  color: #e65100;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .abcde-grid,
  .protection-grid {
    grid-template-columns: 1fr;
  }

  .tip-item {
    flex-direction: column;
    text-align: center;
  }
}
</style>

