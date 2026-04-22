import { reactive } from 'vue'

function getOrdinal(day) {
  if (day >= 11 && day <= 13) return `${day}th`

  const lastDigit = day % 10
  if (lastDigit === 1) return `${day}st`
  if (lastDigit === 2) return `${day}nd`
  if (lastDigit === 3) return `${day}rd`
  return `${day}th`
}

function formatSingleDate(dateString) {
  if (!dateString) return ''

  const date = new Date(`${dateString}T12:00:00`)
  if (Number.isNaN(date.getTime())) return dateString

  const weekday = date.toLocaleDateString('en-US', { weekday: 'short' })
  const month = date.toLocaleDateString('en-US', { month: 'long' })
  const day = getOrdinal(date.getDate())

  return `${weekday}, ${month} ${day}`
}

function formatTripDateRange(startDate, endDate) {
  if (!startDate || !endDate) return ''

  return `${formatSingleDate(startDate)} - ${formatSingleDate(endDate)}`
}

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

function normalizeActivity(activity, dayId = null) {
  return {
    ...activity,
    dayId,
    time: activity.time || undefined,
    locked: Boolean(activity.time),
  }
}

function sortInitialActivities(activities) {
  const timed = activities
    .filter((activity) => activity.time)
    .sort((a, b) => {
      const aTime = parseTimeToMinutes(a.time) ?? 0
      const bTime = parseTimeToMinutes(b.time) ?? 0
      return aTime - bTime
    })

  const untimed = activities.filter((activity) => !activity.time)

  return [...timed, ...untimed]
}

function findTimedInsertIndex(activities, activityMinutes, fallbackIndex = 0) {
  for (let i = 0; i < activities.length; i += 1) {
    const current = activities[i]
    if (!current.time) continue

    const currentMinutes = parseTimeToMinutes(current.time)
    if (currentMinutes !== null && currentMinutes > activityMinutes) {
      return i
    }
  }

  for (let i = activities.length - 1; i >= 0; i -= 1) {
    if (activities[i].time) {
      return i + 1
    }
  }

  return fallbackIndex
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
  isDraggingAlternate: false,

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

      this.tripDates =
      formatTripDateRange(this.tripForm.arrivalDate, this.tripForm.departureDate) ||
      payload.tripDates ||
      ''

    this.days = (payload.days || []).map((day) => ({
      ...day,
      activities: sortInitialActivities(
        (day.activities || []).map((activity) => normalizeActivity(activity, day.id))
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

  handleDayActivitiesChange(dayId) {
    const day = this.getDay(dayId)
    if (!day) return
  
    day.activities.forEach((activity) => {
      activity.dayId = dayId
      activity.locked = Boolean(activity.time)
    })
  },
  
  handleAlternatesChange() {
    this.alternates.forEach((activity) => {
      activity.dayId = null
      activity.time = undefined
      activity.locked = false
    })
  },

  removeActivityFromCurrentLocation(activityId) {
    for (const day of this.days) {
      const index = day.activities.findIndex((activity) => activity.id === activityId)
      if (index !== -1) {
        return {
          activity: day.activities.splice(index, 1)[0],
          from: 'day',
          dayId: day.id,
          index,
        }
      }
    }

    const alternateIndex = this.alternates.findIndex((activity) => activity.id === activityId)
    if (alternateIndex !== -1) {
      return {
        activity: this.alternates.splice(alternateIndex, 1)[0],
        from: 'alternates',
        dayId: null,
        index: alternateIndex,
      }
    }

    return null
  },

  moveActivityToAlternates(activityId) {
    const result = this.removeActivityFromCurrentLocation(activityId)
    if (!result) return

    this.alternates.unshift({
      ...result.activity,
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
    const normalizedTime = time || undefined

    for (const day of this.days) {
      const index = day.activities.findIndex((item) => item.id === activityId)
      if (index === -1) continue

      const [activity] = day.activities.splice(index, 1)

      const updatedActivity = {
        ...activity,
        time: normalizedTime,
        locked: Boolean(normalizedTime),
        dayId: day.id,
      }

      if (!normalizedTime) {
        day.activities.splice(index, 0, updatedActivity)
        return
      }

      const updatedMinutes = parseTimeToMinutes(normalizedTime)
      const insertIndex = findTimedInsertIndex(day.activities, updatedMinutes, index)

      day.activities.splice(insertIndex, 0, updatedActivity)
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