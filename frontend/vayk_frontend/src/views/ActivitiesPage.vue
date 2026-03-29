<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { tripStore } from '../stores/tripStores'

const router = useRouter()

const itineraryTitle = computed(() => {
  return tripStore.generatedItinerary?.title || 'Your Itinerary'
})

function goHome() {
  router.push('/')
}
</script>

<template>
  <div class="activities-page">
    <div class="content">
      <h1>{{ itineraryTitle }}</h1>

      <div v-if="tripStore.generatedItinerary">
        <h2>Suggested Activities</h2>
        <ul>
          <li v-for="activity in tripStore.generatedItinerary.activities" :key="activity">
            {{ activity }}
          </li>
        </ul>
      </div>

      <div v-else>
        <p>No itinerary data found.</p>
      </div>

      <button class="card home-card" @click="goHome">
        <span class="label">Return to Home</span>
      </button>
    </div>
  </div>
</template>


<style scoped>
.activities-page {
  min-height: 100vh;
  background: #f8fafc;
  padding: 2rem;
}

.content {
  max-width: 800px;
  margin: 0 auto;
  background: white;
  padding: 2rem;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
}

h1 {
  color: #172554;
  margin-bottom: 1rem;
}

h2 {
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  color: #1e293b;
}

ul {
  padding-left: 1.25rem;
}

li {
  margin-bottom: 0.75rem;
  color: #334155;
}

/* copied/adapted from ExperienceSelector */
.card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 18px 20px;
  background: #fff;
  border: 1.5px solid #dcdcdc;
  border-radius: 0px;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s ease;
  min-height: 60px;
  width: 100%;
  box-sizing: border-box;
}

.card:hover {
  border-color: #9ca3af;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
  transform: translateY(-2px) scale(1.01);
}

.card:active {
  transform: scale(0.98);
}

.label {
  font-family: 'Inter', sans-serif;
  font-size: 15px;
  font-weight: 300;
  color: #000000;
}

.home-card {
  justify-content: center;
  margin-top: 24px;
  max-width: 300px;
  margin-left: auto;
  margin-right: auto;
}
</style>