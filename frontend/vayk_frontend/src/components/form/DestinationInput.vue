<template>
  <div class="destination-input-wrapper">
    <input
      v-model="searchText"
      type="text"
      placeholder="Enter destination"
      class="destination-input"
      @focus="handleFocus"
      @blur="handleBlur"
    />

    <div v-if="showDropdown && suggestions.length" class="dropdown">
      <button
        v-for="place in suggestions"
        :key="place.id || `${place.name}-${place.country}-${place.lat}-${place.lon}`"
        type="button"
        class="dropdown-item"
        @mousedown.prevent="selectDestination(place)"
      >
        <div class="place-name">{{ place.name }}</div>
        <div class="place-meta">
          {{ [place.admin1, place.country].filter(Boolean).join(', ') }}
        </div>
      </button>
    </div>

    <div v-if="showDropdown && searchText.trim().length >= 2 && !loading && !suggestions.length" class="dropdown empty-state">
      No matching destinations found
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['update:modelValue'])


const searchText = ref('')
const suggestions = ref([])
const loading = ref(false)
const showDropdown = ref(false)


let debounceTimeout = null

watch(
  () => props.modelValue,
  (newValue) => {
    if (!newValue) {
      searchText.value = ''
      return
    }

    searchText.value = newValue.displayName || newValue.name || ''
  },
  { immediate: true }
)

watch(searchText, (newValue) => {
  showDropdown.value = true

  if (props.modelValue && newValue !== (props.modelValue.displayName || props.modelValue.name || '')) {
    emit('update:modelValue', null)
  }

  clearTimeout(debounceTimeout)

  if (!newValue.trim() || newValue.trim().length < 2) {
    suggestions.value = []
    return
  }

  debounceTimeout = setTimeout(() => {
    fetchSuggestions(newValue.trim())
  }, 300)
})


async function fetchSuggestions(query) {
  loading.value = true

  try {
    const url = `https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(query)}&count=7&language=en&format=json`

    const response = await fetch(url)
    const data = await response.json()

    if (data && data.results) {
      suggestions.value = data.results.map((place) => ({
        id: `${place.id ?? place.latitude}-${place.longitude}`,
        name: place.name || '',
        country: place.country || '',
        admin1: place.admin1 || '',
        lat: place.latitude ?? null,
        lon: place.longitude ?? null,
        countryCode: place.country_code || '',
        timezone: place.timezone || '',
        displayName: [
          place.name,
          place.admin1,
          place.country
        ].filter(Boolean).join(', ')
      }))
    } else {
      suggestions.value = []
    }
  } catch (error) {
    console.error('Error fetching destination suggestions:', error)
    suggestions.value = []
  } finally {
    loading.value = false
  }
}

function selectDestination(place) {
  emit('update:modelValue', place)
  searchText.value = place.displayName || place.name
  suggestions.value = []
  showDropdown.value = false
}

function handleFocus() {
  if (suggestions.value.length) {
    showDropdown.value = true
  }
}

function handleBlur() {
  setTimeout(() => {
    showDropdown.value = false
  }, 150)
}
</script>

<style scoped>
.destination-input-wrapper {
  position: relative;
  width: 100%;
}

.destination-input {
  width: 100%;
  padding: 12px;
  font-size: 14px;
  border: 1px solid #ccc;
  font-family: "Inter";
}

.destination-input:focus {
  outline: none;
  border-color: #000000;
}

.dropdown {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  width: 100%;
  background: white;
  border: 1px solid #dcdcdc;
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.08);
  z-index: 20;
}

.dropdown-item {
  width: 100%;
  border: none;
  background: white;
  text-align: left;
  padding: 12px;
  cursor: pointer;
  border-bottom: 1px solid #efefef;
}

.dropdown-item:last-child {
  border-bottom: none;
}

.dropdown-item:hover {
  background: #f7f7f7;
}

.place-name {
  font-size: 14px;
  font-weight: 500;
  color: #111;
}

.place-meta {
  font-size: 12px;
  color: #666;
  margin-top: 2px;
}

.empty-state {
  padding: 12px;
  font-size: 13px;
  color: #666;
}
</style>