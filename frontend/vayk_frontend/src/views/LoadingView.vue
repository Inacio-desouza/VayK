<template>
  <div class="loading-view">
    <div class="loading-card">
      <h1>Creating your itinerary...</h1>
      <p>{{ loadingMessage }}</p>

      <div class="spinner"></div>

      <p v-if="tripStore.generationError" class="error-message">
        {{ tripStore.generationError }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { tripStore } from '../stores/tripStores'

const router = useRouter()

const loadingMessages = [
  'Finding local experiences...',
  'Checking your trip details...',
  'Personalizing your itinerary...',
]

const loadingMessage = ref(loadingMessages[0])

let messageInterval = null

function rotateMessages() {
  let index = 0
  messageInterval = setInterval(() => {
    index = (index + 1) % loadingMessages.length
    loadingMessage.value = loadingMessages[index]
  }, 1800)
}

async function generateItinerary() {
  try {
    tripStore.setGenerating(true)
    tripStore.setGenerationError('')

    // TEMPORARY: simulate backend delay
    // Later, replace this with a real fetch call
    await new Promise((resolve) => setTimeout(resolve, 2500)) 

    // TEMPORARY: fake itinerary data
    tripStore.setGeneratedItinerary({
      title: `Trip to ${tripStore.tripForm.destination?.displayName || 'your destination'}`,
      activities: [
        'Morning walking tour',
        'Lunch at a local restaurant',
        'Afternoon museum visit',
        'Evening live event',
      ],
    })

    tripStore.setGenerating(false)
    router.push('/activities')
  } catch (error) {
    tripStore.setGenerating(false)
    tripStore.setGenerationError('Something went wrong while generating your itinerary.')
    setTimeout(() => {
      router.push('/')
    }, 2000)
  }
}

onMounted(() => {
  if (!tripStore.tripForm.destination || !tripStore.tripForm.arrivalDate || !tripStore.tripForm.departureDate) {
    router.push('/')
    return
  }

  rotateMessages()
  generateItinerary()
})

onUnmounted(() => {
  if (messageInterval) clearInterval(messageInterval)
})
</script>

<style scoped>
.loading-view {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8fafc;
  padding: 2rem;
}

.loading-card {
  background: white;
  padding: 2.5rem 2rem;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  text-align: center;
  width: 100%;
  max-width: 480px;
}

.loading-card h1 {
  font-size: 1.8rem;
  margin-bottom: 0.75rem;
  color: #172554;
}

.loading-card p {
  font-size: 1rem;
  color: #475569;
  margin-bottom: 1.5rem;
}

.spinner {
  width: 52px;
  height: 52px;
  margin: 0 auto 1.5rem;
  border: 5px solid #dbeafe;
  border-top: 5px solid #172554;
  border-radius: 50%;
  animation: spin 0.9s linear infinite;
}

.error-message {
  color: #b91c1c;
  font-weight: 600;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>