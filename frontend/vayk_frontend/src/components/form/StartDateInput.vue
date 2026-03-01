<template>
  <div class="date-input-wrapper">
    <!-- Main text input field for user to type destination -->
    <input
      type="text"
      placeholder="MM/DD/YYYY"
      class="date-input"
    />
  </div>
</template>

<script setup>

</script>

<style scoped>
/* Wrapper container - positioned relative so dropdown can be positioned absolute */
.date-input-wrapper {
  position: relative;
  width: 100%;
}

/* Main input field styling */
.date-input {
  width: 100%;
  padding: 12px;
  font-size: 14px;
  border: 1px solid #ccc;
  font-family: "Inter";
}

/* Styling when input field is focused (active) */
.date-input:focus {
  outline: none;
  border-color: #000000;
}
</style>