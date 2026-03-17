<script setup>
import { reactive, watch } from 'vue'

import DestinationInput from './components/form/DestinationInput.vue'
import StartDateInput from './components/form/StartDateInput.vue'
import EndDateInput from './components/form/EndDateInput.vue'
import ExperienceSelector from './components/form/ExperienceSelector.vue'
import PreferenceInput from './components/form/PreferenceInput.vue'
import GenerateItinerary from './components/form/GenerateItinerary.vue'

import logoUrl from './assets/transparent_logo.png'

const tripForm = reactive({
  destination: null,
  arrivalDate: '',
  departureDate: '',
  interests: [],
  preferences: '',
})

const errors = reactive({
  destination: '',
  arrivalDate: '',
  departureDate: '',
})

const submitPopup = reactive({
  show: false,
  messages: [],
})

// --- Clear errors on input ---
watch(() => tripForm.destination, (newValue) => {
  if (newValue) {
    errors.destination = ''
  }
})

watch(() => tripForm.arrivalDate, (newValue) => {
  if (newValue) {
    errors.arrivalDate = ''
  }
})

// --- Real-time date validation ---
watch(() => tripForm.departureDate, (newValue) => {
  if (newValue && errors.departureDate === 'Please select a departure date.') {
    errors.departureDate = ''
  }
})

watch(
  () => [tripForm.arrivalDate, tripForm.departureDate],
  ([arrival, departure]) => {
    if (!arrival || !departure) {
      if (errors.departureDate === 'Departure date must be after arrival date.') {
        errors.departureDate = ''
      }
      return
    }

    if (departure <= arrival) {
      errors.departureDate = 'Departure date must be after arrival date.'
    } else {
      errors.departureDate = ''
    }
  }
)

// --- Validate form inputs ---
function validateForm() {
  errors.destination = ''
  errors.arrivalDate = ''
  errors.departureDate = ''

  let isValid = true
  const popupMessages = []

  if (!tripForm.destination) {
    errors.destination = 'Please select a destination from the dropdown.'
    popupMessages.push('Please select a destination from the dropdown.')
    isValid = false
  }

  if (!tripForm.arrivalDate) {
    errors.arrivalDate = 'Please select an arrival date.'
    popupMessages.push('Please select an arrival date.')
    isValid = false
  }

  if (!tripForm.departureDate) {
    errors.departureDate = 'Please select a departure date.'
    popupMessages.push('Please select a departure date.')
    isValid = false
  }

  if (tripForm.arrivalDate && tripForm.departureDate && tripForm.departureDate <= tripForm.arrivalDate) {
    errors.departureDate = 'Departure date must be after arrival date.'

    if (!popupMessages.includes('Departure date must be after arrival date.')) {
      popupMessages.push('Departure date must be after arrival date.')
    }

    isValid = false
  }

  return { isValid, popupMessages }
}

function closePopup() {
  submitPopup.show = false
  submitPopup.messages = []
}

function handleSubmit() {
  const { isValid, popupMessages } = validateForm()

  if (!isValid) {
    submitPopup.show = true
    submitPopup.messages = popupMessages
    return
  }

  closePopup()
  console.log('Submitting trip form:', JSON.parse(JSON.stringify(tripForm)))
}
</script>

<template>
  <div class="page">
    <div class="form-container">
      <img class="logo-img" :src="logoUrl" alt="VayK logo" />
      <h2 class="subheader">Build your trip around experiences, not logistics</h2>

      <div style="width: 100%">
        <h3 class="form-question">Where do you want to go?</h3>
        <DestinationInput v-model="tripForm.destination" />

        <h3 class="form-question">When are you traveling?</h3>

        <div class="date-row">
          <div>
            <StartDateInput v-model="tripForm.arrivalDate" />
            <h4 class="form-question small-label">Arrival Date</h4>
          </div>
          <div>
            <EndDateInput v-model="tripForm.departureDate" />
            <h4 class="form-question small-label">Departure Date</h4>
          </div>
        </div>
      </div>

      <div class="line"></div>

      <div style="width: 100%">
        <h3 class="form-question" style="font-size: 18px; margin-top: 1%">
          What are your interests?
        </h3>
        <h4 class="form-question" style="font-size: 12px; margin-top: 0px">
          Select all that interest you
        </h4>
        <ExperienceSelector v-model="tripForm.interests" />
      </div>

      <div class="line"></div>

      <div style="width: 100%">
        <h3 class="form-question" style="font-size: 18px; margin-top: 10px">
          Add additional preferences below
        </h3>
        <h4 class="form-question" style="font-size: 12px; margin-top: 0px">
          Tell us more about yourself and your interests
        </h4>
        <PreferenceInput v-model="tripForm.preferences" />
      </div>

      <GenerateItinerary @submit="handleSubmit" />
    </div>
  </div>
</template>

<style scoped>
.page {
  min-height: 100vh;
  width: 100%;
  display: flex;
  justify-content: center;
  padding: 48px 16px;
  box-sizing: border-box;
  color: white;
  background: linear-gradient(180deg, #0828a8 0%, #1c62ff 45%, #2aa6ff 100%);
}

.form-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 700px;
  margin: 0 auto 8%;
  box-sizing: border-box;
}

.logo-img {
  width: 100%;
  max-width: 650px;
  height: auto;
  align-self: center;
  margin-bottom: 8px;
  display: block;
}

.subheader {
  font-family: 'Inter', sans-serif;
  font-weight: 300;
  font-size: 22px;
  margin-top: 1%;
  align-self: center;
  text-align: center;
}

.form-question {
  font-family: 'Inter', sans-serif;
  font-weight: 300;
  font-size: 16px;
  margin-top: 30px;
  margin-bottom: 10px;
}

.line {
  border-bottom: 1px solid #939393;
  margin: 30px 0;
  width: 100%;
}

.date-row {
  display: flex;
  gap: 16px;
  width: 100%;
}

.date-row > div {
  display: flex;
  flex-direction: column;
  width: 50%;
  min-width: 0;
}

.small-label {
  font-size: 12px;
  margin-top: 6px;
}

.destination-input-shell,
.date-input-shell {
  position: relative;
  width: 100%;
  border-radius: 0;
}

.input-shell-error {
  border: 2px solid #ef4444;
  background: #fff7f7;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.12);
}

.field-error-box {
  display: flex;
  align-items: center;
  gap: 8px;
  width: fit-content;
  max-width: 100%;
  margin-top: 10px;
  padding: 8px 12px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-left: 4px solid #ef4444;
  border-radius: 8px;
  color: #991b1b;
  font-size: 14px;
  font-weight: 500;
  font-family: 'Inter', sans-serif;
  line-height: 1.4;
}

.field-error-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  border-radius: 999px;
  background: #ef4444;
  color: white;
  font-size: 12px;
  font-weight: 700;
  flex-shrink: 0;
}

.date-error-left {
  margin-top: 12px;
}

.error-popup {
  width: 100%;
  margin-top: 24px;
  padding: 16px 18px;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 10px;
  color: #991b1b;
  font-family: 'Inter', sans-serif;
}

.error-popup-text {
  font-size: 15px;
  font-weight: 500;
  line-height: 1.5;
}

.error-popup-text strong {
  display: block;
  margin-bottom: 6px;
}

.error-popup-text ul {
  margin: 0;
  padding-left: 18px;
}

.error-popup-text li + li {
  margin-top: 4px;
}

.error-popup-close {
  border: none;
  background: transparent;
  color: #991b1b;
  font-size: 22px;
  line-height: 1;
  cursor: pointer;
  padding: 0;
  flex-shrink: 0;
}

@media (max-width: 600px) {
  .page {
    padding: 24px 12px;
  }

  .date-row {
    flex-direction: column;
    gap: 12px;
  }

  .date-row > div {
    width: 100%;
  }

  .field-error-box {
    width: 100%;
  }
}
</style>

<style>
html,
body,
#app {
  margin: 0;
  padding: 0;
  width: 100%;
  min-height: 100%;
}

body {
  font-family: 'Inter', sans-serif;
  background: linear-gradient(180deg, #0828a8 0%, #1c62ff 45%, #2aa6ff 100%);
}

input,
textarea,
button {
  font-family: 'Inter', sans-serif;
}

::placeholder {
  font-family: 'Inter', sans-serif;
}

*,
*::before,
*::after {
  box-sizing: border-box;
}
</style>