<template>
  <section class="about">
    <h2>About DermaSense</h2>

    <p>
      DermaSense is a prototype decision-support tool for the early assessment of
      suspicious skin lesions. It analyzes uploaded lesion images together with
      optional clinical details such as age, sex, and lesion site.
    </p>

    <p>
      The system focuses on three target classes: <strong>Benign</strong>,
      <strong>Basal Cell Carcinoma (BCC)</strong>, and
      <strong>Squamous Cell Carcinoma (SCC)</strong>. The goal is to assist
      clinicians and learners, not to replace clinical judgment.
    </p>

    <h3>How it works</h3>
    <ul>
      <li>Upload a dermoscopic or clinical image of a skin lesion.</li>
      <li>Optionally provide age, sex, and lesion site for additional context.</li>
      <li>View the predicted class, confidence level, and explanation image.</li>
    </ul>

    <p class="disclaimer">
      <strong>Disclaimer:</strong> DermaSense is a research prototype and not a
      diagnostic tool. All outputs must be confirmed by a board-certified
      dermatologist.
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
