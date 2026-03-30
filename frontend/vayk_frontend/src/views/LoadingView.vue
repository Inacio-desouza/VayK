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
import mockPlaces from '../mock/places.json'

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

    const { destination, arrivalDate, departureDate, interests, preferences } = tripStore.tripForm

    const res = await fetch('http://localhost:8000/data_aquisition/itinerary/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        lat: destination.lat,
        lon: destination.lon,
        destination: destination.displayName,
        arrivalDate,
        departureDate,
        interests,
        preferences,
      }),
    })

    if (!res.ok) throw new Error('Server error')

    const places = await res.json()
    tripStore.setGeneratedItinerary(places)
    tripStore.setGenerating(false)
    router.push('/activities')
  } catch (error) {
    // Backend not running — use mock data so the UI flow can still be tested
    console.warn('Backend unavailable, falling back to mock data:', error)
    tripStore.setGeneratedItinerary(mockPlaces)
    tripStore.setGenerating(false)
    router.push('/activities')
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