<template>
  <div class="preference-input-wrapper" style="width: 100%;">
    <textarea
      :value="modelValue"
      @input="emit('update:modelValue', $event.target.value)"
      placeholder="e.g., I prefer local experiences over tourist spots, I'm vegetarian, I want to avoid crowds..."
      class="preference-input"
      rows="6"
      maxlength="500"
    ></textarea>

    <div class="character-counter">
      {{ modelValue.length }}/500
    </div>
  </div>
</template>

<script setup>
defineProps({
  modelValue: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['update:modelValue'])
</script>

<style scoped>
.preference-input-wrapper {
  position: relative;
  width: 100%;
}

.preference-input {
  width: 96%;
  padding: 12px;
  font-size: 14px;
  border: 1px solid #ccc;
  font-family: "Inter";
}

.preference-input:focus {
  outline: none;
  border-color: #000000;
}

.character-counter {
  font-family: "Inter";
  font-size: 12px;
  color: #666;
  text-align: right;
  margin-top: 4px;
  padding-right: 12px;
  align-self: flex-end;
}
</style>