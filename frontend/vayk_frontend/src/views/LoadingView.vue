<template>
  <div class="loading-view">
    <div class="loading-card">
      <h1>Creating your itinerary...</h1>

      <p class="loading-message">
        <Transition name="fade-up" mode="out-in">
          <span :key="loadingMessage">{{ loadingMessage }}</span>
        </Transition>
      </p>

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
  }, 3500)
}

function buildDateLabel(dateString, dayNumber) {
  if (!dateString) return `Day ${dayNumber}`

  const date = new Date(`${dateString}T00:00:00`)
  if (Number.isNaN(date.getTime())) return `Day ${dayNumber}`

  return date.toLocaleDateString('en-US', {
    weekday: 'long',
    month: 'long',
    day: 'numeric',
  })
}

function formatHourMinute(hour, minute = 0) {
  if (typeof hour !== 'number') return ''

  const normalizedMinute = typeof minute === 'number' ? minute : 0
  const suffix = hour >= 12 ? 'PM' : 'AM'
  const hour12 = hour % 12 === 0 ? 12 : hour % 12
  const minuteText = String(normalizedMinute).padStart(2, '0')

  return `${hour12}:${minuteText} ${suffix}`
}

function formatBackendTime(dateTime) {
  if (!dateTime) return undefined

  if (typeof dateTime === 'string') {
    const looksLikeDate = /^[A-Za-z]{3,}\s\d{1,2}$/.test(dateTime)

    if (looksLikeDate) return undefined

    return dateTime
  }

  if (Array.isArray(dateTime)) {
    if (dateTime.length === 0) return undefined

    const firstValue = dateTime[0]

    if (typeof firstValue === 'string') {
      // If it's just a date like "Apr 23", ignore it
      const looksLikeDate = /^[A-Za-z]{3,}\s\d{1,2}$/.test(firstValue)

      if (looksLikeDate) return undefined

      return firstValue
    }

    if (firstValue?.open || firstValue?.close) {
      const openText = firstValue.open
        ? formatHourMinute(firstValue.open.hour, firstValue.open.minute)
        : ''
      const closeText = firstValue.close
        ? formatHourMinute(firstValue.close.hour, firstValue.close.minute)
        : ''

      if (openText && closeText) return `${openText} - ${closeText}`
      return openText || closeText || undefined
    }

    return undefined
  }

  if (dateTime.open || dateTime.close) {
    const openText = dateTime.open
      ? formatHourMinute(dateTime.open.hour, dateTime.open.minute)
      : ''
    const closeText = dateTime.close
      ? formatHourMinute(dateTime.close.hour, dateTime.close.minute)
      : ''

    if (openText && closeText) return `${openText} - ${closeText}`
    return openText || closeText || undefined
  }

  return undefined
}

function formatActivity(activity, index, prefix = 'act') {
  return {
    id: `${prefix}-${index}`,
    title: activity.name,
    name: activity.name,
    time: formatBackendTime(activity.date_time),
    address: activity.address,
    description: activity.description,
    rating: activity.rating,
  }
}

function buildFormattedItinerary(places) {
  const { destination, arrivalDate, departureDate } = tripStore.tripForm

  const startDate = new Date(`${arrivalDate}T00:00:00`)
  const endDate = new Date(`${departureDate}T00:00:00`)

  const tripLength =
    !Number.isNaN(startDate.getTime()) && !Number.isNaN(endDate.getTime())
      ? Math.max(
          1,
          Math.ceil((endDate - startDate) / (1000 * 60 * 60 * 24)) + 1
        )
      : Math.max(1, (places.itinerary || []).length)

  const dayBuckets = Array.from({ length: tripLength }, (_, index) => {
    const currentDate = new Date(startDate)
    currentDate.setDate(startDate.getDate() + index)

    const isoDate = !Number.isNaN(currentDate.getTime())
      ? currentDate.toISOString().split('T')[0]
      : null

    return {
      id: `day-${index + 1}`,
      dayNumber: index + 1,
      dateLabel: buildDateLabel(isoDate, index + 1),
      activities: [],
    }
  })

  ;(places.itinerary || []).forEach((activity, index) => {
    const dayIndex = index % dayBuckets.length
    dayBuckets[dayIndex].activities.push(formatActivity(activity, index, 'act'))
  })

  return {
    tripTitle: destination?.displayName || 'Your Itinerary',
    tripDates: `${arrivalDate} - ${departureDate}`,
    days: dayBuckets,
    alternates: (places.alternates || []).map((activity, index) =>
      formatActivity(activity, index, 'alt')
    ),
  }
}

async function generateItinerary() {
  try {
    tripStore.setGenerating(true)
    tripStore.setGenerationError('')

    const { destination, arrivalDate, departureDate, interests, preferences } = tripStore.tripForm

    const requestBody = {
      lat: destination.lat,
      lon: destination.lon,
      destination: destination.displayName,
      arrivalDate,
      departureDate,
      interests,
      preferences,
    }

    console.log('TRIP FORM FROM STORE:', JSON.parse(JSON.stringify(tripStore.tripForm)))
    console.log('REQUEST BODY SENT TO BACKEND:', requestBody)

    const res = await fetch(`${import.meta.env.VITE_API_URL}/itinerary/get_itinerary/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(requestBody),
    })

    console.log('RESPONSE STATUS:', res.status)

    if (!res.ok) throw new Error('Server error')

    const places = await res.json()

    console.log('RAW BACKEND RESPONSE:', places)
    console.log('FIRST ITINERARY ITEM:', places.itinerary?.[0])
    console.log('BACKEND RESPONSE itinerary:', places.itinerary)
    console.log('BACKEND RESPONSE alternates:', places.alternates)

    const formattedItinerary = buildFormattedItinerary(places)

    console.log('FORMATTED ITINERARY:', formattedItinerary)

    tripStore.setGeneratedItinerary(formattedItinerary)
    tripStore.initializeItineraryState(formattedItinerary)

    console.log('STORE DAYS AFTER INIT:', JSON.parse(JSON.stringify(tripStore.days)))
    console.log('STORE ALTERNATES AFTER INIT:', JSON.parse(JSON.stringify(tripStore.alternates)))

    tripStore.setGenerating(false)
    router.push('/activities')
  } catch (error) {
    console.warn('Backend unavailable, falling back to mock data:', error)
    tripStore.setGeneratedItinerary(mockPlaces)
    tripStore.initializeItineraryState(mockPlaces)
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

.loading-message {
  font-size: 1rem;
  color: #475569;
  margin-bottom: 1.5rem;
  min-height: 1.5em;
}

.loading-message span {
  display: inline-block;
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

.fade-up-enter-active,
.fade-up-leave-active {
  transition:
    opacity 0.45s ease,
    transform 0.45s ease;
}

.fade-up-enter-from {
  opacity: 0;
  transform: translateY(8px);
}

.fade-up-enter-to {
  opacity: 1;
  transform: translateY(0);
}

.fade-up-leave-from {
  opacity: 1;
  transform: translateY(0);
}

.fade-up-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>