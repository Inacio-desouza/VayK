<template>
  <div class="experience-selector">
    <div class="grid-wrapper-container">
      <div
        ref="gridWrapper"
        class="grid-wrapper"
        @scroll="handleScroll"
      >
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

      <div v-if="showFade" class="bottom-fade"></div>
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
import { ref, onMounted, nextTick } from 'vue'
import {
  GlassWater,
  Landmark,
  UtensilsCrossed,
  Users,
  DollarSign,
  Music,
  Trees,
  ShoppingBag,
  Dumbbell,
  Wine,
  Waves,
  Building2,
  Theater,
  Trophy,
} from 'lucide-vue-next'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['update:modelValue'])

const gridWrapper = ref(null)
const showFade = ref(false)

const options = [
  { id: 'nightlife', icon: GlassWater, label: 'Nightlife' },
  { id: 'museums', icon: Landmark, label: 'Museums' },
  { id: 'food', icon: UtensilsCrossed, label: 'Food & Dining' },
  { id: 'family', icon: Users, label: 'Family-Friendly' },
  { id: 'budget', icon: DollarSign, label: 'Budget-Focused' },
  { id: 'live-music', icon: Music, label: 'Live Music' },
  { id: 'parks', icon: Trees, label: 'Parks & Nature' },
  { id: 'shopping', icon: ShoppingBag, label: 'Shopping' },
  { id: 'fitness', icon: Dumbbell, label: 'Fitness & Wellness' },
  { id: 'wine', icon: Wine, label: 'Wine & Tasting' },
  { id: 'beaches', icon: Waves, label: 'Beaches & Water' },
  { id: 'history', icon: Building2, label: 'History & Landmarks' },
  { id: 'arts', icon: Theater, label: 'Arts & Theater' },
  { id: 'sports', icon: Trophy, label: 'Sports Events' },
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

function handleScroll() {
  const el = gridWrapper.value
  if (!el) return

  const isScrollable = el.scrollHeight > el.clientHeight
  const isAtBottom = el.scrollTop + el.clientHeight >= el.scrollHeight - 4

  showFade.value = isScrollable && !isAtBottom
}

onMounted(async () => {
  await nextTick()
  handleScroll()
})
</script>

<style scoped>
.experience-selector {
  font-family: 'Inter', sans-serif;
  width: 100%;
}

.grid-wrapper-container {
  position: relative;
}

.grid-wrapper {
  max-height: 340px;
  overflow-y: auto;
  overflow-x: hidden;
}

.bottom-fade {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 56px;
  pointer-events: none;
  background: linear-gradient(to bottom, rgba(255, 255, 255, 0), #ffffff);
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