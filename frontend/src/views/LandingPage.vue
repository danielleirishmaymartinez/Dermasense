<template>
  <div>
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-card">
        <div class="hero-left">
          <div class="image-grid">
            <img src="@/assets/Land.jpg" alt="Skin Image" class="skin-image" />
          </div>
        </div>
        <div class="hero-right">
          <h1>Get the Best Skin Treatments</h1>
          <p>
            This system assists dermatologists and users by classifying skin lesions and
            recommending treatments.
          </p>
          <button class="cta" @click="$router.push('/upload')">View Services</button>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
// This section remains empty for now. We just need to display the layout.
</script>

<style scoped>
/* Hero section */
.hero {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 10px;     /* less space */
  background-color: #f4f1ec;
  padding: 20px 0 50px; /* tighter top, keep bottom padding */
}


.hero-card {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 40px;
  max-width: 1200px;
  background-color: #fff;
  padding: 60px;
  border-radius: 18px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.hero-left {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.hero-image {
  width: 90%;
  max-width: 500px;
  border-radius: 20px;

  /* Aesthetic shadow */
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);

  /* Smooth fade style for luxury look */
  mask-image: linear-gradient(
    to bottom right,
    rgba(0, 0, 0, 1) 60%,
    rgba(0, 0, 0, 0)
  );

  /* Soft border highlighting */
  border: 4px solid #f1e6dd;
  object-fit: cover;
}


/* Hero section right content */
.hero-right {
  flex: 1.5;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding-left: 40px;
}

.hero-right h1 {
  font-size: 48px; /* Larger font size for the heading */
  color: #2c3e50;
  margin-bottom: 20px;
  font-family: 'Poppins', sans-serif; /* Aesthetic font for the title */
}

.hero-right p {
  color: #2c3e50; /* Dark color for the text */
  font-size: 18px;
  margin-bottom: 30px;
  max-width: 500px; /* Limit the paragraph width */
}

.cta {
  background-color: #2c3e50; /* Dark color for the button */
  color: white;
  padding: 16px 30px;
  border: none;
  border-radius: 10px;
  font-size: 18px;
  cursor: pointer;
  font-weight: bold;
}

.cta:hover {
  background-color: #1a3d66;
}
</style>
