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
        :key="place.xid || `${place.name}-${place.country}-${place.lat}-${place.lon}`"
        type="button"
        class="dropdown-item"
        @mousedown.prevent="selectDestination(place)"
      >
        <div class="place-name">{{ place.name }}</div>
        <div class="place-meta">
          {{ place.country || 'Unknown country' }}
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

const API_KEY = '5ae2e3f221c38a28845f05b606078b51fd1f6bb18e7bc9e7685b8007'

const searchText = ref('')
const suggestions = ref([])
const loading = ref(false)
const showDropdown = ref(false)

// Reduce random results
const blockedKinds = [
  'street',
  'building',
  'cafe',
  'restaurant',
  'shop',
  'supermarket',
  'accomodations',
  'hotel',
  'hostels',
  'apartments',
  'banks',
  'atm',
  'fuel',
  'car_rental',
  'car_wash',
  'airport',
  'railway',
  'bus_station',
]
const blockedNamePatterns = [
  /\bstreet\b/i,
  /\broad\b/i,
  /\bavenue\b/i,
  /\bave\b/i,
  /\bblvd\b/i,
  /\bboulevard\b/i,
  /\bdrive\b/i,
  /\bdr\b/i,
  /\blane\b/i,
  /\bln\b/i,
  /\bcafe\b/i,
  /\brestaurant\b/i,
  /\bhotel\b/i,
  /\bapartment\b/i,
  /\bmuseum\b/i,
  /\bmall\b/i,
  /\bplaza\b/i,
  /\bbuilding\b/i,
]

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

function scoreFeature(feature, query) {
  const name = feature.properties?.name || ''
  const lowerName = name.toLowerCase()
  const lowerQuery = query.toLowerCase()
  const kinds = (feature.properties?.kinds || '').toLowerCase()

  let score = 0

  // Strong preference for close text matches
  if (lowerName === lowerQuery) score += 100
  else if (lowerName.startsWith(lowerQuery)) score += 60
  else if (lowerName.includes(lowerQuery)) score += 30

  // Prefer cleaner, simpler names
  if (!/\d/.test(name)) score += 10
  if (name.length <= 30) score += 8
  if ((name.match(/,/g) || []).length <= 1) score += 6

  // Penalize obvious non-destination types
  if (blockedKinds.some(kind => kinds.includes(kind))) score -= 100
  if (blockedNamePatterns.some(pattern => pattern.test(name))) score -= 100

  return score
}

async function fetchSuggestions(query) {
  loading.value = true

  try {
    const url = `https://api.opentripmap.com/0.1/en/places/autosuggest?name=${encodeURIComponent(query)}&radius=5000000&lon=0&lat=20&limit=25&apikey=${API_KEY}`

    const response = await fetch(url)
    const data = await response.json()

    if (data && data.features) {
      suggestions.value = data.features
        .filter((feature) => {
          const name = feature.properties?.name || ''
          return !!name
        })
        .map((feature) => {
          const score = scoreFeature(feature, query)

          return {
            xid: feature.properties?.xid || '',
            name: feature.properties?.name || '',
            highlightedName: feature.properties?.highlighted_name || '',
            kinds: feature.properties?.kinds || '',
            country: '',
            lon: feature.geometry?.coordinates?.[0] ?? null,
            lat: feature.geometry?.coordinates?.[1] ?? null,
            displayName: feature.properties?.name || '',
            score,
          }
        })
        .filter((place) => place.score > 0)
        .sort((a, b) => b.score - a.score)
        .slice(0, 7)
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