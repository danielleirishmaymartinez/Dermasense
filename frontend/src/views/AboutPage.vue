<template>
  <section class="about">
    <h2>About DermaSense</h2>

    <p>
      DermaSense is a research prototype that supports early assessment of suspicious
      skin lesions. It analyzes images and optional metadata (age, sex, lesion site)
      to provide a predicted class and confidence score.
    </p>

    <p>
      The system focuses on three classes: Benign, Basal Cell Carcinoma (BCC), and
      Squamous Cell Carcinoma (SCC).
    </p>

    <h3>How to use</h3>
    <ul>
      <li>Go to <strong>Upload Image</strong> and choose a lesion image.</li>
      <li>Optionally enter age, sex, and lesion site.</li>
      <li>Wait for the system to analyze the image.</li>
      <li>View the result and explanation on the Results page.</li>
    </ul>

    <p class="disclaimer">
      Disclaimer: This tool is for research and educational purposes only and is not a
      substitute for professional medical diagnosis.
    </p>
  </section>
</template>

<style scoped>
.about {
  max-width: 800px;
}
h2 {
  color: #234a7c;
  margin-bottom: 14px;
}
h3 {
  color: #234a7c;
  margin: 18px 0 8px;
}
p {
  font-size: 14px;
  color: #4b5c73;
  margin-bottom: 10px;
}
ul {
  margin-left: 18px;
  margin-bottom: 16px;
  font-size: 14px;
  color: #4b5c73;
}
.disclaimer {
  font-size: 12px;
  background-color: #fff9e6;
  padding: 10px 12px;
  border-radius: 6px;
}
</style>
