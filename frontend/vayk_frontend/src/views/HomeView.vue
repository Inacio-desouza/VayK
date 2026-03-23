<script setup>
import { reactive, computed } from 'vue'
import { useRouter } from 'vue-router'

import DestinationInput from '../components/form/DestinationInput.vue'
import StartDateInput from '../components/form/StartDateInput.vue'
import EndDateInput from '../components/form/EndDateInput.vue'
import ExperienceSelector from '../components/form/ExperienceSelector.vue'
import PreferenceInput from '../components/form/PreferenceInput.vue'
import GenerateItinerary from '../components/form/GenerateItinerary.vue'

import logoUrl from '../assets/transparent_logo.png'

const router = useRouter()

const tripForm = reactive({
  destination: '',
  arrivalDate: '',
  departureDate: '',
  interests: [],
  preferences: '',
})

const isFormValid = computed(() => {
  const destinationOk = !!tripForm.destination
  const arrival = new Date(tripForm.arrivalDate)
  const depart = new Date(tripForm.departureDate)
  const arrivalOk = tripForm.arrivalDate && !Number.isNaN(arrival.valueOf())
  const departOk = tripForm.departureDate && !Number.isNaN(depart.valueOf())
  const dateOrderOk = arrivalOk && departOk && depart > arrival
  return destinationOk && arrivalOk && departOk && dateOrderOk
})

function handleSubmit() {
  if (!isFormValid.value) return
  router.push('/activities')
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

      <GenerateItinerary :disabled="!isFormValid" @submit="handleSubmit" />
      <p v-if="!isFormValid" class="warning">
        Please complete destination and choose valid arrival/departure dates (departure after
        arrival).
      </p>
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
  width: 70%;
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

.warning {
  color: #ffb5b5;
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  margin-top: 16px;
  text-align: center;
}
</style>
