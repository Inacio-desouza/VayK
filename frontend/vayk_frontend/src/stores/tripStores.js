import { reactive } from 'vue'

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

  resetGenerationState() {
    this.generatedItinerary = null
    this.isGenerating = false
    this.generationError = ''
  },
})