<template>
  <div class="date-input-wrapper" @click="openPicker">
    <input
      ref="inputRef"
      :value="modelValue"
      @input="emit('update:modelValue', $event.target.value)"
      type="date"
      class="date-input"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  modelValue: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['update:modelValue'])

const inputRef = ref(null)

function openPicker() {
  if (!inputRef.value) return

  if (inputRef.value.showPicker) {
    inputRef.value.showPicker()
  } else {
    inputRef.value.focus()
  }
}
</script>

<style scoped>
.date-input-wrapper {
  position: relative;
  width: 100%;
  cursor: pointer;
}

.date-input::-webkit-calendar-picker-indicator {
  cursor: pointer;
}

.date-input {
  width: 100%;
  box-sizing: border-box;
  padding: 12px;
  font-size: 14px;
  border: 1px solid #ccc;
  font-family: "Inter";
  cursor: pointer;
}

.date-input:focus {
  outline: none;
  border-color: #000000;
}
</style>