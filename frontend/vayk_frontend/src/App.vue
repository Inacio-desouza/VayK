<script setup>
import DestinationInput from './components/form/DestinationInput.vue'
import StartDateInput from './components/form/StartDateInput.vue'
import EndDateInput from './components/form/EndDateInput.vue'
import ExperienceSelector from './components/form/ExperienceSelector.vue'
import PreferenceInput from './components/form/PreferenceInput.vue'
import GenerateItinerary from './components/form/GenerateItinerary.vue'
</script>

<template>
  <container style="display: flex; justify-content: center;">
    <div class="form-container">
      <h1 class="logo">VayK</h1>
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
  </container>
</template>

<style scoped>
.form-container {
  display: flex;
  flex-direction: column;
  width: 55%;
  margin-bottom: 8%;
}

.logo {
  font-family: 'Inter', sans-serif;
  font-weight: 300;
  font-size: 67px;
  margin-bottom: 0%;
  align-self: center;
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
