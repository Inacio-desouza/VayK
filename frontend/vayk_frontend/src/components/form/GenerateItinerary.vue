<template>
  <button
    class="generate-button"
    type="button"
    @click="emit('submit')"
    :disabled="disabled"
  >
    Generate My Itinerary
  </button>
</template>

<script setup>
const emit = defineEmits(['submit'])
const props = defineProps({ disabled: Boolean })
</script>

<style scoped>
.generate-button:disabled {
  cursor: not-allowed;
  opacity: 0.55;
}
.generate-button {
  background-color: #1e3a8a;
  color: #FFFFFF;
  font-family: "Inter", sans-serif;
  font-size: 20px;

  padding: 18px 30px;
  border: none;
  cursor: pointer;

  width: 100%;
  margin-top: 32px;

  transition: all 0.2s ease;
}
.generate-button:hover {
  background-color: #172554;
}

.generate-button:active {
  transform: scale(0.98);
}
</style>