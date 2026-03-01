<template>
  <div class="preference-input-wrapper" style="width: 100%;">
    <!-- Main text input field for user to type destination -->
    <textarea
      placeholder="e.g., I prefer local experiences over tourist spots, I'm vegetarian, I want to avoid crowds..."
      class="preference-input"
      rows="6"
    />
  </div>
</template>

<script setup>

</script>

<style scoped>
/* Wrapper container - positioned relative so dropdown can be positioned absolute */
.preference-input-wrapper {
  position: relative;
  width: 100%;
}

/* Main input field styling */
.preference-input {
  width: 100%;
  padding: 12px;
  font-size: 14px;
  border: 1px solid #ccc;
  font-family: "Inter";
}

/* Styling when input field is focused (active) */
.preference-input:focus {
  outline: none;
  border-color: #000000;
}
</style>