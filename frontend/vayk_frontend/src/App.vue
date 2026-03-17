<script setup>
import { reactive } from 'vue'

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

function handleSubmit() {
  console.log('Submitting trip form:', JSON.parse(JSON.stringify(tripForm)))
}
</script>

<template>
  <RouterView />
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