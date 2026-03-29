<template>
  <div class="experience-selector">
    <div class="grid-wrapper">
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
    </div>

    <div class="actions">
      <button
        type="button"
        class="text-button"
        @click="unselectAll"
        :disabled="!modelValue.length"
      >
        Unselect All
      </button>
    </div>
  </div>
</template>

<script setup>
import {
  GlassWater,
  Landmark,
  UtensilsCrossed,
  Mountain,
  Users,
  DollarSign,
  Music,
  Trees,
  ShoppingBag,
  Dumbbell,
  Camera,
  Wine,
  Waves,
  Building2,
  Bus,
  Theater,
  Bike,
  Sun,
  Plane,
  Coffee,
  Tent,
  FerrisWheel,
  BookOpen,
  ShipWheel,
  Trophy,
  Palette,
} from 'lucide-vue-next'

const props = defineProps({
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
  { id: 'live-music', icon: Music, label: 'Live Music' },
  { id: 'parks', icon: Trees, label: 'Parks & Nature' },
  { id: 'shopping', icon: ShoppingBag, label: 'Shopping' },
  { id: 'fitness', icon: Dumbbell, label: 'Fitness & Wellness' },
  { id: 'photography', icon: Camera, label: 'Scenic Views' },
  { id: 'wine', icon: Wine, label: 'Wine & Tasting' },
  { id: 'beaches', icon: Waves, label: 'Beaches & Water' },
  { id: 'history', icon: Building2, label: 'History & Landmarks' },
  { id: 'day-trips', icon: Bus, label: 'Day Trips' },
  { id: 'arts', icon: Theater, label: 'Arts & Theater' },
  { id: 'biking', icon: Bike, label: 'Biking' },
  { id: 'relaxation', icon: Sun, label: 'Relaxation' },
  { id: 'travel', icon: Plane, label: 'Travel Hotspots' },
  { id: 'cafes', icon: Coffee, label: 'Cafés & Brunch' },
  { id: 'camping', icon: Tent, label: 'Camping' },
  { id: 'theme-parks', icon: FerrisWheel, label: 'Theme Parks' },
  { id: 'reading', icon: BookOpen, label: 'Bookstores & Reading' },
  { id: 'boating', icon: ShipWheel, label: 'Boating & Cruises' },
  { id: 'sports', icon: Trophy, label: 'Sports & Recreation' },
  { id: 'creative', icon: Palette, label: 'Creative Experiences' },
]

function toggle(id) {
  const updated = [...props.modelValue]
  const idx = updated.indexOf(id)

  if (idx === -1) {
    updated.push(id)
  } else {
    updated.splice(idx, 1)
  }

  emit('update:modelValue', updated)
}

function unselectAll() {
  emit('update:modelValue', [])
}
</script>

<style scoped>
.experience-selector {
  font-family: 'Inter', sans-serif;
  width: 100%;
}

.grid-wrapper {
  position: relative;
  max-height: 372px;
  overflow-y: auto;
  overflow-x: hidden;
}


.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  padding: 12px;
  padding-bottom: 28px;
  width: 100%;
  box-sizing: border-box;
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
  min-height: 60px;
  width: 100%;
  box-sizing: border-box;
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
  background: #172554;
  border-color: #0c1630;
}

.card.selected .label,
.card.selected .icon {
  color: #ffffff;
}

.icon {
  color: #000000;
  flex-shrink: 0;
}

.label {
  font-family: 'Inter', sans-serif;
  font-size: 15px;
  font-weight: 300;
  color: #000000;
}

.actions {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-top: 14px;
}

.text-button {
  background: none;
  border: none;
  padding: 0;
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  color: #172554;
  cursor: pointer;
  text-decoration: underline;
}

.text-button:disabled {
  color: #9ca3af;
  cursor: not-allowed;
  text-decoration: none;
}
</style>