<template>
  <div class="grid">
      <button
        v-for="option in options"
        :key="option.id"
        class="card"
        :class="{ selected: selected.includes(option.id) }"
        @click="toggle(option.id)"
      >
        <component :is="option.icon" :size="20" :stroke-width="1.5" class="icon" />
        <span class="label">{{ option.label }}</span>
      </button>
</div>
</template>

<script setup>
import { ref } from 'vue'
import { GlassWater, Landmark, UtensilsCrossed, Mountain, Users, DollarSign } from 'lucide-vue-next'

const options = [
  { id: 'nightlife', icon: GlassWater,     label: 'Nightlife' },
  { id: 'museums',  icon: Landmark,        label: 'Museums' },
  { id: 'food',     icon: UtensilsCrossed, label: 'Food & Dining' },
  { id: 'outdoor',  icon: Mountain,        label: 'Outdoor Adventures' },
  { id: 'family',   icon: Users,           label: 'Family-Friendly' },
  { id: 'budget',   icon: DollarSign,      label: 'Budget-Focused' },
]

const selected = ref([])

function toggle(id) {
  const idx = selected.value.indexOf(id)
  if (idx === -1) {
    selected.value.push(id)
  } else {
    selected.value.splice(idx, 1)
  }
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
  border: 1.5px solid #dcdcdc;
  border-radius: 0px;
  background: #fff;
  cursor: pointer;
  transition: border-color 0.15s, background 0.15s, box-shadow 0.15s;
  text-align: left;
}

.card:hover {
  border-color: #b3b3b3;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.card.selected {
  border-color: #3b82f6;
  background: #eff6ff;
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