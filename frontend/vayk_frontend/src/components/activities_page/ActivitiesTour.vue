<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import { tripStore } from '../../stores/tripStores'

const steps = [
  {
    title: 'Switch views',
    text: 'Use these buttons to switch between list view and calendar view.',
    target: '[data-tour="view-toggle"]',
    before: () => tripStore.setActiveView('list'),
  },
  {
    title: 'Export your itinerary',
    text: 'Download your trip as a PDF or export it to your calendar.',
    target: '[data-tour="export-actions"]',
  },
  {
    title: 'Add alternate activities',
    text: 'Open the alternates tab, then drag activities into your itinerary. You can also drag activities back here to remove them from the main plan.',
    target: '[data-tour="alternates"]',
    before: () => {
      if (!tripStore.isAlternatesOpen) tripStore.toggleAlternates()
    },
  },
  {
    title: 'See more details',
    text: 'Click the “i” button to view more information about an activity.',
    target: '[data-tour="info-button"]',
    before: () => {
      tripStore.setActiveView('list')
      if (tripStore.isAlternatesOpen) tripStore.toggleAlternates()
    },
  },
  {
    title: 'Change the time',
    text: 'Click the time pill to update when an activity happens.',
    target: '[data-tour="time-button"]',
  },
  {
    title: 'Delete an activity',
    text: 'Click the × button to remove an activity from your itinerary.',
    target: '[data-tour="remove-button"]',
  },
]

const isOpen = ref(false)
const currentIndex = ref(0)
const targetRect = ref(null)
let activeTarget = null

const currentStep = computed(() => steps[currentIndex.value])
const isLastStep = computed(() => currentIndex.value === steps.length - 1)

function clearHighlight() {
  if (activeTarget) {
    activeTarget.classList.remove('tour-highlight')
    activeTarget = null
  }
}

async function updateTarget() {
  clearHighlight()

  const step = currentStep.value
  if (!step) return

  if (step.before) {
    step.before()
    await nextTick()
  }

  const target = document.querySelector(step.target)

  if (!target) {
    targetRect.value = null
    return
  }

  target.scrollIntoView({
    behavior: 'smooth',
    block: 'center',
  })

  setTimeout(() => {
    const rect = target.getBoundingClientRect()
    targetRect.value = rect
    target.classList.add('tour-highlight')
    activeTarget = target
  }, 250)
}

function startTour() {
  isOpen.value = true
  currentIndex.value = 0
  updateTarget()
}

function closeTour() {
  isOpen.value = false
  clearHighlight()
}

function nextStep() {
  if (isLastStep.value) {
    closeTour()
    return
  }

  currentIndex.value += 1
  updateTarget()
}

function previousStep() {
  if (currentIndex.value === 0) return
  currentIndex.value -= 1
  updateTarget()
}

function handleReposition() {
  if (!isOpen.value || !activeTarget) return
  targetRect.value = activeTarget.getBoundingClientRect()
}

/* 🔥 FIXED POSITIONING LOGIC */
const tooltipStyle = computed(() => {
  if (!targetRect.value) {
    return {
      top: '50%',
      left: '50%',
      transform: 'translate(-50%, -50%)',
    }
  }

  const rect = targetRect.value
  const tooltipWidth = 340
  const padding = 18

  let top = rect.top + rect.height / 2 - 100
  let left

  const isRightSide = rect.left > window.innerWidth / 2

  if (isRightSide) {
    left = rect.left - tooltipWidth - 16
  } else {
    left = rect.right + 16
  }

  if (left < padding) left = padding

  if (left + tooltipWidth > window.innerWidth - padding) {
    left = window.innerWidth - tooltipWidth - padding
  }

  if (top < padding) top = padding
  if (top + 220 > window.innerHeight) {
    top = window.innerHeight - 220 - padding
  }

  return {
    top: `${top}px`,
    left: `${left}px`,
  }
})

onMounted(() => {
  window.addEventListener('resize', handleReposition)
  window.addEventListener('scroll', handleReposition, true)
})

onBeforeUnmount(() => {
  clearHighlight()
  window.removeEventListener('resize', handleReposition)
  window.removeEventListener('scroll', handleReposition, true)
})
</script>

<template>
  <button class="tour-start-btn" type="button" @click="startTour">
    How to use this page
  </button>

  <teleport to="body">
    <div v-if="isOpen" class="tour-layer">
      <div class="tour-backdrop" />

      <div class="tour-card" :style="tooltipStyle">
        <div class="tour-card-header">
          <p class="tour-step">Step {{ currentIndex + 1 }} of {{ steps.length }}</p>
          <button class="tour-close" type="button" @click="closeTour">×</button>
        </div>

        <h2>{{ currentStep.title }}</h2>
        <p>{{ currentStep.text }}</p>

        <div class="tour-actions">
          <button class="tour-secondary" type="button" @click="closeTour">
            Skip
          </button>

          <div class="tour-right-actions">
            <button
              v-if="currentIndex > 0"
              class="tour-secondary"
              type="button"
              @click="previousStep"
            >
              Back
            </button>

            <button class="tour-primary" type="button" @click="nextStep">
              {{ isLastStep ? 'Done' : 'Next' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </teleport>
</template>

<style scoped>
.tour-start-btn {
  position: fixed;
  right: 24px;
  bottom: 24px;
  z-index: 50;
  border: none;
  background: #182655;
  color: white;
  padding: 12px 16px;
  border-radius: 999px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 12px 26px rgba(24, 38, 85, 0.24);
}

.tour-layer {
  position: fixed;
  inset: 0;
  z-index: 99999;
  pointer-events: none;
}

.tour-backdrop {
  position: absolute;
  inset: 0;
  background: rgba(15, 23, 42, 0.36);
}

.tour-card {
  position: fixed;
  width: min(340px, calc(100vw - 36px));
  background: white;
  border-radius: 22px;
  padding: 18px;
  box-shadow: 0 22px 60px rgba(15, 23, 42, 0.28);
  pointer-events: auto;
  transition: all 0.25s ease;
}

.tour-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tour-step {
  font-size: 13px;
  font-weight: 700;
  color: #64748b;
}

.tour-close {
  border: none;
  background: #f1f5f9;
  border-radius: 999px;
  width: 28px;
  height: 28px;
  cursor: pointer;
}

.tour-card h2 {
  margin: 12px 0 6px;
}

.tour-actions {
  margin-top: 18px;
  display: flex;
  justify-content: space-between;
}

.tour-right-actions {
  display: flex;
  gap: 8px;
}

.tour-primary {
  background: #182655;
  color: white;
  border-radius: 12px;
  padding: 10px 14px;
  cursor: pointer;
}

.tour-secondary {
  background: #f1f5f9;
  border-radius: 12px;
  padding: 10px 14px;
  cursor: pointer;
}

:global(.tour-highlight) {
  position: relative;
  z-index: 100000 !important;
  outline: 4px solid rgba(147, 197, 253, 0.9);
  border-radius: 18px;
}
</style>