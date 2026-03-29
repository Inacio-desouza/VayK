<script setup>
defineProps({
  modelValue: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['update:modelValue'])
</script>

<template>
  <div class="date-input-wrapper">
    <input
      :value="modelValue"
      @input="emit('update:modelValue', $event.target.value)"
      type="date"
      class="date-input"
    />
  </div>
</template>

<style scoped>
.date-input-wrapper {
  position: relative;
  width: 100%;
}

.date-input {
  width: 94%;
  padding: 12px;
  font-size: 14px;
  border: 1px solid #ccc;
  font-family: "Inter";
}

.date-input:focus {
  outline: none;
  border-color: #000000;
}
</style>