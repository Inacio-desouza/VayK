import { reactive } from 'vue'

function parseTimeToMinutes(time) {
  if (!time) return null

  const trimmed = String(time).trim().toUpperCase()
  const match = trimmed.match(/^(\d{1,2}):(\d{2})\s*(AM|PM)$/)

  if (!match) return null

  let hours = Number(match[1])
  const minutes = Number(match[2])
  const meridiem = match[3]

  if (meridiem === 'AM' && hours === 12) hours = 0
  if (meridiem === 'PM' && hours !== 12) hours += 12

  return hours * 60 + minutes
}

function sortActivitiesForDay(activities) {
  const timed = activities
    .filter((activity) => activity.time)
    .sort((a, b) => {
      const aTime = parseTimeToMinutes(a.time) ?? 0
      const bTime = parseTimeToMinutes(b.time) ?? 0
      return aTime - bTime
    })

  const untimed = activities.filter((activity) => !activity.time)

  return [
    ...timed.map((activity) => ({
      ...activity,
      locked: true,
    })),
    ...untimed.map((activity) => ({
      ...activity,
      locked: false,
    })),
  ]
}

export const tripStore = reactive({
  tripForm: {
    destination: null,
    arrivalDate: '',
    departureDate: '',
    interests: [],
    preferences: '',
  },

  generatedItinerary: null,
  isGenerating: false,
  generationError: '',

  tripTitle: '',
  tripDates: '',
  days: [],
  alternates: [],
  activeView: 'list',
  selectedActivity: null,
  isAlternatesOpen: false,

  setTripForm(formData) {
    this.tripForm = {
      destination: formData.destination,
      arrivalDate: formData.arrivalDate,
      departureDate: formData.departureDate,
      interests: [...formData.interests],
      preferences: formData.preferences,
    }
  },

  setGeneratedItinerary(itinerary) {
    this.generatedItinerary = itinerary
  },

  setGenerating(value) {
    this.isGenerating = value
  },

  setGenerationError(message) {
    this.generationError = message
  },

  initializeItineraryState(payload) {
    this.tripTitle =
      payload.tripTitle ||
      this.tripForm.destination?.displayName ||
      'Your Itinerary'

    this.tripDates = payload.tripDates || ''

    this.days = (payload.days || []).map((day) => ({
      ...day,
      activities: sortActivitiesForDay(
        (day.activities || []).map((activity) => ({
          ...activity,
          dayId: day.id,
          locked: Boolean(activity.time),
        }))
      ),
    }))

    this.alternates = (payload.alternates || []).map((activity) => ({
      ...activity,
      dayId: null,
      time: undefined,
      locked: false,
    }))

    this.activeView = 'list'
    this.selectedActivity = null
    this.isAlternatesOpen = false
  },

  getActivityTitle(activity) {
    return activity.name || activity.title || 'Untitled activity'
  },

  getDay(dayId) {
    return this.days.find((day) => day.id === dayId)
  },

  normalizeDay(dayId) {
    const day = this.getDay(dayId)
    if (!day) return
    day.activities = sortActivitiesForDay([...day.activities])
  },

  removeActivityFromCurrentLocation(activityId) {
    for (const day of this.days) {
      const index = day.activities.findIndex((activity) => activity.id === activityId)
      if (index !== -1) {
        return day.activities.splice(index, 1)[0]
      }
    }

    const alternateIndex = this.alternates.findIndex((activity) => activity.id === activityId)
    if (alternateIndex !== -1) {
      return this.alternates.splice(alternateIndex, 1)[0]
    }

    return null
  },

  moveActivityToDay(dayId, activity, insertIndex = null) {
    const moved = this.removeActivityFromCurrentLocation(activity.id)
    if (!moved) return

    const day = this.getDay(dayId)
    if (!day) return

    const nextActivity = {
      ...moved,
      dayId,
      locked: Boolean(moved.time),
    }

    if (nextActivity.time) {
      day.activities.push(nextActivity)
    } else if (typeof insertIndex === 'number') {
      day.activities.splice(insertIndex, 0, nextActivity)
    } else {
      day.activities.push(nextActivity)
    }

    this.normalizeDay(dayId)
  },

  moveActivityToAlternates(activityId) {
    const moved = this.removeActivityFromCurrentLocation(activityId)
    if (!moved) return

    this.alternates.unshift({
      ...moved,
      dayId: null,
      time: undefined,
      locked: false,
    })
  },

  removeActivityFromDay(dayId, activityId) {
    const day = this.getDay(dayId)
    if (!day) return

    const index = day.activities.findIndex((activity) => activity.id === activityId)
    if (index === -1) return

    const [removed] = day.activities.splice(index, 1)

    this.alternates.unshift({
      ...removed,
      dayId: null,
      time: undefined,
      locked: false,
    })
  },

  updateActivityTime(activityId, time) {
    for (const day of this.days) {
      const activity = day.activities.find((item) => item.id === activityId)
      if (!activity) continue

      activity.time = time || undefined
      activity.locked = Boolean(activity.time)
      this.normalizeDay(day.id)
      return
    }
  },

  openActivityDetail(activity) {
    this.selectedActivity = activity
  },

  closeActivityDetail() {
    this.selectedActivity = null
  },

  toggleAlternates() {
    this.isAlternatesOpen = !this.isAlternatesOpen
  },

  setActiveView(view) {
    this.activeView = view
  },

  resetGenerationState() {
    this.generatedItinerary = null
    this.isGenerating = false
    this.generationError = ''

    this.tripTitle = ''
    this.tripDates = ''
    this.days = []
    this.alternates = []
    this.activeView = 'list'
    this.selectedActivity = null
    this.isAlternatesOpen = false
  },
})