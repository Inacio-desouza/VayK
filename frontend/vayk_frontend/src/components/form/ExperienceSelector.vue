<template>
  <div class="grid">
    <button
      v-for="option in options"
      :key="option.id"
      type="button"
      class="card"
      :class="{ selected: modelValue.includes(option.id) }"
      @click="toggle(option.id)"
    >
      <component :is="option.icon" :size="20" :stroke-width="1.5" class="icon" />
      <span class="label">{{ option.label }}</span>
    </button>
  </div>
</template>

<script setup>
import { GlassWater, Landmark, UtensilsCrossed, Mountain, Users, DollarSign } from 'lucide-vue-next'

const { modelValue } = defineProps({
  modelValue: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['update:modelValue'])

const options = [
  { id: 'nightlife', icon: GlassWater, label: 'Nightlife' },
  { id: 'museums', icon: Landmark, label: 'Museums' },
  { id: 'food', icon: UtensilsCrossed, label: 'Food & Dining' },
  { id: 'outdoor', icon: Mountain, label: 'Outdoor Adventures' },
  { id: 'family', icon: Users, label: 'Family-Friendly' },
  { id: 'budget', icon: DollarSign, label: 'Budget-Focused' },
]

function toggle(id) {
  const updated = [...modelValue]
  const idx = updated.indexOf(id)

  if (idx === -1) {
    updated.push(id)
  } else {
    updated.splice(idx, 1)
  }

  emit('update:modelValue', updated)
}
</script>

<style scoped>
.experience-selector {
  font-family: 'Inter', sans-serif;
  max-width: 800px;
  padding: 24px;
}

.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-top: 10px;
  width: 100%;
  margin-bottom: 10px;
}

.card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 18px 20px;
  background: #fff;
  border: 1.5px solid #dcdcdc;
  border-radius: 0px;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s ease;
}

.card:hover:not(.selected) {
  border-color: #9ca3af;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
  transform: translateY(-2px) scale(1.01);
}

.card:active {
  transform: scale(0.98);
}

.card.selected {
  background: #1e3a8a;
  border-color: #1e3a8a;
}

.card.selected .label,
.card.selected .icon {
  color: white;
}

.icon {
  color: #000000;
  flex-shrink: 0;
}

.label {
  font-family: "Inter", sans-serif;
  font-size: 15px;
  font-weight: 300;
  color: #000000;
}
</style>