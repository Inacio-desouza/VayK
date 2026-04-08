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

.actions {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-top: 14px;
}
</style>