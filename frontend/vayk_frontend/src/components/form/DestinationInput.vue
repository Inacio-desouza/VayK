<template>
  <div class="destination-input-wrapper">
    <!-- Main text input field for user to type destination -->
    <input
      type="text"
      placeholder="Enter destination"
      class="destination-input"
    />
  </div>
</template>

<script setup>

</script>

<style scoped>
/* Wrapper container - positioned relative so dropdown can be positioned absolute */
.destination-input-wrapper {
  position: relative;
  width: 100%;
}

/* Main input field styling */
.destination-input {
  width: 100%;
  padding: 12px;
  font-size: 14px;
  border: 1px solid #ccc;
  font-family: "Inter";
}

/* Styling when input field is focused (active) */
.destination-input:focus {
  outline: none;
  border-color: #000000;
}
</style>