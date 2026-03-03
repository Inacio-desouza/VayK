<script setup>
import DestinationInput from './components/form/DestinationInput.vue'
import StartDateInput from './components/form/StartDateInput.vue'
import EndDateInput from './components/form/EndDateInput.vue'
import ExperienceSelector from './components/form/ExperienceSelector.vue'
import PreferenceInput from './components/form/PreferenceInput.vue'
import GenerateItinerary from './components/form/GenerateItinerary.vue'

import logoUrl from './assets/transparent_logo.png'
</script>

<template>
  <div class="page">
    <div class="form-container">
      <!-- Replace text logo with image -->
      <img class="logo-img" :src="logoUrl" alt="VayK logo" />
      <h2 class="subheader">Build your trip around experiences, not logistics</h2>
      <div style="width: 100%">
        <h3 class="form-question">Where do you want to go?</h3>
        <DestinationInput />
        <h3 class="form-question">When are you traveling?</h3>

        <div style="display: flex; gap: 40px">
          <div style="display: flex; flex-direction: column; width: 50%">
            <StartDateInput />
            <h4 class="form-question" style="font-size: 12px; margin-top: 6px">Arrival Date</h4>
          </div>
          <div style="display: flex; flex-direction: column; width: 50%">
            <EndDateInput />
            <h4 class="form-question" style="font-size: 12px; margin-top: 6px">Departure Date</h4>
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
        <ExperienceSelector />
      </div>
      <div class="line"></div>

      <div style="width: 100%">
        <h3 class="form-question" style="font-size: 18px; margin-top: 10px">
          Add additional preferences below
        </h3>
        <h4 class="form-question" style="font-size: 12px; margin-top: 0px">
          Tell us more about yourself and your interests
        </h4>
        <PreferenceInput />
      </div>
      <GenerateItinerary />

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
  color: white;

  /* gradient */
  background: linear-gradient(180deg, #0828a8 0%, #1c62ff 45%, #2aa6ff 100%);
}


.form-container {
  display: flex;
  flex-direction: column;
  width: 55%;
  margin-bottom: 8%;
}

.logo-img {
  height: 200px;
  width: auto;
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
  margin-top: 30px;
  margin-bottom: 30px;
  width: 104%;
}
</style>
