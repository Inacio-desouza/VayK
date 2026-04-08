<template>
  <div class="preference-input-wrapper">
    <Transition name="fade" mode="out-in">
      <div
        v-if="!modelValue && !isFocused"
        class="placeholder-overlay"
        :key="groupKey"
      >
        e.g., {{ visibleSuggestions }}...
      </div>
    </Transition>

    <textarea
      :value="modelValue"
      @input="handleInput"
      @focus="isFocused = true"
      @blur="isFocused = false"
      placeholder=""
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
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { preferenceSuggestions } from '@/data/preferenceSuggestions'

const props = defineProps({
  modelValue: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['update:modelValue'])

const suggestions = preferenceSuggestions
const currentStartIndex = ref(0)
const isFocused = ref(false)
const groupSize = 3
let intervalId = null

function handleInput(event) {
  emit('update:modelValue', event.target.value)
}

const visibleSuggestions = computed(() => {
  const items = []

  for (let i = 0; i < groupSize; i++) {
    const index = (currentStartIndex.value + i) % suggestions.length
    items.push(suggestions[index])
  }

  return items.join(', ')
})

const groupKey = computed(() => {
  return `${currentStartIndex.value}-${visibleSuggestions.value}`
})

function rotateSuggestionGroup() {
  if (suggestions.length <= groupSize) return

  const minJump = 2
  const maxJump = 7
  const jump = Math.floor(Math.random() * (maxJump - minJump + 1)) + minJump

  currentStartIndex.value =
    (currentStartIndex.value + jump) % suggestions.length
}

onMounted(() => {
  intervalId = setInterval(() => {
    if (!props.modelValue && !isFocused.value) {
      rotateSuggestionGroup()
    }
  }, 4000)
})

onBeforeUnmount(() => {
  if (intervalId) clearInterval(intervalId)
})
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
  resize: vertical;
  background: transparent;
  position: relative;
  z-index: 2;
}

.preference-input:focus {
  outline: none;
  border-color: #000000;
}

.placeholder-overlay {
  position: absolute;
  top: 12px;
  left: 12px;
  right: 24px;
  font-size: 14px;
  font-family: "Inter";
  color: #777;
  pointer-events: none;
  z-index: 1;
  line-height: 1.5;
  white-space: normal;
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

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.35s ease, transform 0.35s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(4px);
}

.fade-enter-to {
  opacity: 1;
  transform: translateY(0);
}

.fade-leave-from {
  opacity: 1;
  transform: translateY(0);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>