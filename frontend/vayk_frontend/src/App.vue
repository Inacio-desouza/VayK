<script setup>
import DestinationInput from './components/form/DestinationInput.vue'
import StartDateInput from './components/form/StartDateInput.vue'
import EndDateInput from './components/form/EndDateInput.vue'
</script>

<template>
  <container style="display: flex; justify-content: center; height: 100vh;">
    <div class="form-container">
      <h1 class="logo">VayK</h1>
      <h2 class="subheader">Build your trip around experiences, not logistics</h2>
      <h3 class="form-question">Where do you want to go?</h3>
      <DestinationInput />
      <h3 class="form-question">When are you traveling?</h3>
      
      <div style="display: flex; gap: 40px;">
        <div style="display: flex; flex-direction: column; width: 50%;">
        <StartDateInput />
        <h4 class="form-question" style="font-size: 12px; margin-top: 6px;">Arrival Date</h4>
        </div>
        <div style="display: flex; flex-direction: column; width: 50%;">
        <EndDateInput />
        <h4 class="form-question" style="font-size: 12px; margin-top: 6px;">Departure Date</h4>
        </div>
      </div>

    </div>
  </container>
</template>

<style scoped>

.form-container {
  display: flex;
  flex-direction: column;
  width: 55%;
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
</style>
