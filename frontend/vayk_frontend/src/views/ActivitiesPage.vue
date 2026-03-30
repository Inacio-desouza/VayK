<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { tripStore } from '../stores/tripStores'
import mockPlaces from '../mock/places.json'

const router = useRouter()

const allPlaces = tripStore.generatedItinerary ?? mockPlaces

// Split into itinerary (first 4) and the rest go into the swap pool
const itinerary = ref(allPlaces.slice(0, 4))
const pool = ref(allPlaces.slice(4))

// --- Drag and drop state ---
// We track where a drag started so we know which list to remove from on drop
const dragSource = ref(null)  // 'itinerary' or 'pool'
const dragIndex = ref(null)

function onDragStart(source, index) {
  dragSource.value = source
  dragIndex.value = index
}

function onDropIntoItinerary() {
  if (dragSource.value === 'pool') {
    const [moved] = pool.value.splice(dragIndex.value, 1)
    itinerary.value.push(moved)
  }
}

function onDropIntoPool() {
  if (dragSource.value === 'itinerary') {
    const [moved] = itinerary.value.splice(dragIndex.value, 1)
    pool.value.push(moved)
  }
}

function goHome() {
  router.push('/')
}
</script>

<template>
  <div class="page">
    <div class="header">
      <h2 class="title">{{ tripStore.tripForm.destination?.displayName || 'Your Itinerary' }}</h2>
      <button class="back-btn" @click="goHome">← Plan another trip</button>
    </div>

    <div class="panels">

      <!-- Left: current itinerary -->
      <div
        class="panel"
        @dragover.prevent
        @drop="onDropIntoItinerary"
      >
        <h3 class="panel-title">Your Itinerary</h3>
        <p class="panel-hint">Drag activities here to add them</p>

        <p v-if="!itinerary.length" class="empty">
          Drag activities from the right to build your itinerary.
        </p>

        <div
          v-for="(place, index) in itinerary"
          :key="place.name"
          class="card"
          draggable="true"
          @dragstart="onDragStart('itinerary', index)"
        >
          <img v-if="place.icon" :src="place.icon" alt="" class="icon" />
          <div class="info">
            <p class="name">{{ place.name }}</p>
            <p class="address">{{ place.address }}</p>
            <p class="meta">⭐ {{ place.rating }} · {{ place.reviews.toLocaleString() }} reviews</p>
          </div>
          <span class="drag-handle">⠿</span>
        </div>
      </div>

      <!-- Right: swap pool -->
      <div
        class="panel pool"
        @dragover.prevent
        @drop="onDropIntoPool"
      >
        <h3 class="panel-title">More Options</h3>
        <p class="panel-hint">Drag activities left to add, right to remove</p>

        <p v-if="!pool.length" class="empty">
          No more options — drag something back from your itinerary.
        </p>

        <div
          v-for="(place, index) in pool"
          :key="place.name"
          class="card"
          draggable="true"
          @dragstart="onDragStart('pool', index)"
        >
          <img v-if="place.icon" :src="place.icon" alt="" class="icon" />
          <div class="info">
            <p class="name">{{ place.name }}</p>
            <p class="address">{{ place.address }}</p>
            <p class="meta">⭐ {{ place.rating }} · {{ place.reviews.toLocaleString() }} reviews</p>
          </div>
          <span class="drag-handle">⠿</span>
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
.page {
  min-height: 100vh;
  width: 100%;
  padding: 32px 24px;
  box-sizing: border-box;
  background: white;
}

.header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 24px;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
}

.title {
  font-family: 'Inter', sans-serif;
  font-weight: 300;
  font-size: 28px;
  margin: 0;
}

.back-btn {
  background: none;
  border: none;
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  color: #555;
  cursor: pointer;
  padding: 0;
}

.back-btn:hover {
  color: #000;
}

.panels {
  display: flex;
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto;
  align-items: flex-start;
}

.panel {
  flex: 1;
  min-height: 400px;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 20px;
}

/* Subtle background difference to distinguish the two panels */
.pool {
  background: #fafafa;
}

.panel-title {
  font-family: 'Inter', sans-serif;
  font-weight: 500;
  font-size: 16px;
  margin: 0 0 4px 0;
}

.panel-hint {
  font-family: 'Inter', sans-serif;
  font-size: 12px;
  color: #aaa;
  margin: 0 0 16px 0;
}

.empty {
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  color: #aaa;
  text-align: center;
  margin-top: 40px;
}

.card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  margin-bottom: 8px;
  background: white;
  border: 1px solid #efefef;
  border-radius: 8px;
  cursor: grab;
}

.card:active {
  cursor: grabbing;
}

.icon {
  width: 36px;
  height: 36px;
  object-fit: contain;
  flex-shrink: 0;
}

.info {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
}

.name {
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  font-weight: 500;
  margin: 0;
}

.address {
  font-family: 'Inter', sans-serif;
  font-size: 12px;
  color: #555;
  margin: 0;
}

.meta {
  font-family: 'Inter', sans-serif;
  font-size: 12px;
  color: #888;
  margin: 0;
}

.drag-handle {
  font-size: 18px;
  color: #ccc;
  flex-shrink: 0;
  user-select: none;
}

@media (max-width: 700px) {
  .panels {
    flex-direction: column;
  }
}
</style>
