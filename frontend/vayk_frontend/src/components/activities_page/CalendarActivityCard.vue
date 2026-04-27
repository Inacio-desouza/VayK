<script setup>
import { ref } from 'vue'
import { tripStore } from '../../stores/tripStores'

const props = defineProps({
  activity: {
    type: Object,
    required: true,
  },
  dayId: String,
})

const emit = defineEmits(['edit-time', 'open-detail', 'remove'])

const nativeTimeInput = ref(null)

function titleFor(activity) {
  return tripStore.getActivityTitle(activity)
}

function formatTime(timeString) {
  if (!timeString) return ''
  const match = timeString.match(/(\d{1,2}:\d{2}\s*[AP]M)/i)
  return match ? match[1] : timeString
}

function timeToInputValue(timeString) {
  if (!timeString) return ''

  const match = formatTime(timeString).match(/(\d{1,2}):(\d{2})\s*(AM|PM)/i)
  if (!match) return ''

  let hour = Number(match[1])
  const minute = match[2]
  const period = match[3].toUpperCase()

  if (period === 'PM' && hour !== 12) hour += 12
  if (period === 'AM' && hour === 12) hour = 0

  return `${String(hour).padStart(2, '0')}:${minute}`
}

function inputValueToTime(value) {
  if (!value) return undefined

  const [hourString, minute] = value.split(':')
  let hour = Number(hourString)
  const period = hour >= 12 ? 'PM' : 'AM'

  hour = hour % 12
  if (hour === 0) hour = 12

  return `${hour}:${minute} ${period}`
}

function openTimePicker() {
  if (!nativeTimeInput.value) return

  nativeTimeInput.value.value = timeToInputValue(props.activity.time)

  if (nativeTimeInput.value.showPicker) {
    nativeTimeInput.value.showPicker()
  } else {
    nativeTimeInput.value.click()
    nativeTimeInput.value.focus()
  }
}

function handleTimeChange(event) {
  emit('edit-time', inputValueToTime(event.target.value))
}

function handleOpenDetail() {
  emit('open-detail')
}

function handleRemove() {
  emit('remove', props.dayId)
}
</script>

<template>
  <div class="calendar-activity-card" :class="{ 'timed-card': !!activity.time }">
    <div class="calendar-card-top">
      <div class="calendar-card-title-wrap">
        <span v-if="activity.time" class="mini-lock" aria-hidden="true">
          <span class="lock-icon">
            <svg viewBox="0 0 20 20" fill="none">
              <rect x="4" y="9" width="12" height="8" rx="2.5" stroke="currentColor" stroke-width="1.8" />
              <path
                d="M6.5 9V6.8C6.5 4.7 8.07 3 10 3C11.93 3 13.5 4.7 13.5 6.8V9"
                stroke="currentColor"
                stroke-width="1.8"
                stroke-linecap="round"
              />
            </svg>
          </span>
        </span>

        <span v-else class="mini-lock drag-handle" aria-hidden="true">
          <span class="grip-icon">
            <svg viewBox="0 0 20 20" fill="currentColor">
              <circle cx="7" cy="5" r="1.2" />
              <circle cx="13" cy="5" r="1.2" />
              <circle cx="7" cy="10" r="1.2" />
              <circle cx="13" cy="10" r="1.2" />
              <circle cx="7" cy="15" r="1.2" />
              <circle cx="13" cy="15" r="1.2" />
            </svg>
          </span>
        </span>

        <h4 class="calendar-card-title">{{ titleFor(activity) }}</h4>
      </div>

      <div v-if="activity.url" class="calendar-url">
        <a :href="activity.url" target="_blank" rel="noopener noreferrer">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="16" height="16">
            <path d="M19 19H5V5h7V3H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2v-7h-2v7zM14 3v2h3.59l-9.83 9.83 1.41 1.41L19 6.41V10h2V3h-7z"/>
          </svg>
        </a>
      </div>

      <div class="calendar-card-right">
        <div class="time-picker-wrap">
          <button
            class="time-pill"
            :class="activity.time ? 'time-pill-filled visible' : 'time-pill-ghost hover-only'"
            type="button"
            @click.stop="openTimePicker"
          >
            {{ activity.time ? formatTime(activity.time) : 'Add time' }}
          </button>

          <input
            ref="nativeTimeInput"
            class="native-time-input"
            type="time"
            step="300"
            @change="handleTimeChange"
            @click.stop
          />
        </div>

        <button class="info-btn" type="button" @click="handleOpenDetail">
          <span class="info-icon">
            <svg viewBox="0 0 20 20" fill="none">
              <circle cx="10" cy="10" r="7.2" stroke="currentColor" stroke-width="1.6" />
              <path d="M10 8.8V12.8" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
              <circle cx="10" cy="6.6" r="0.9" fill="currentColor" />
            </svg>
          </span>
        </button>

        <button class="icon-btn remove" type="button" @click="handleRemove">×</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.calendar-activity-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 20px;
  padding: 16px 18px;
  box-shadow: 0 1px 6px rgba(15, 23, 42, 0.04);
}

.calendar-activity-card.timed-card {
  border-left: 4px solid #d5dbe6;
}

.calendar-card-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 14px;
}

.calendar-card-title-wrap {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  min-width: 0;
  flex: 1;
}

.mini-lock {
  color: #d1d5db;
  flex-shrink: 0;
  line-height: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding-top: 2px;
  width: 28px;
  min-width: 28px;
}

.drag-handle {
  cursor: grab;
}

.drag-handle:active {
  cursor: grabbing;
}

.lock-icon,
.grip-icon {
  width: 18px;
  height: 18px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #d1d5db;
  flex-shrink: 0;
}

.lock-icon svg,
.grip-icon svg {
  width: 100%;
  height: 100%;
  display: block;
}

.calendar-card-title {
  margin: 0;
  font-size: 17px;
  font-weight: 600;
  line-height: 1.25;
  letter-spacing: -0.01em;
  color: #0f172a;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.calendar-card-right {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  flex-shrink: 0;
  margin-left: auto;
}

.time-picker-wrap {
  position: relative;
  display: inline-flex;
  flex-shrink: 0;
}

.native-time-input {
  position: absolute;
  inset: 0;
  width: 1px;
  height: 1px;
  opacity: 0;
  pointer-events: none;
}

.time-pill {
  border: none;
  padding: 7px 12px;
  border-radius: 11px;
  font-size: 13px;
  line-height: 1;
  cursor: pointer;
  white-space: nowrap;
  transition:
    opacity 0.15s ease,
    background 0.15s ease,
    color 0.15s ease;
  letter-spacing: -0.01em;
  flex-shrink: 0;
}

.time-pill-filled {
  background: #e7eefc;
  color: #2b3f75;
  font-weight: 600;
}

.time-pill-filled:hover {
  background: #dfe8fb;
}

.time-pill-ghost {
  background: #f3f4f6;
  color: #9ca3af;
  font-weight: 500;
}

.time-pill-ghost:hover {
  background: #e5e7eb;
  color: #6b7280;
}

.visible {
  opacity: 1;
}

.hover-only {
  opacity: 0;
  pointer-events: none;
}

.calendar-activity-card:hover .hover-only {
  opacity: 1;
  pointer-events: auto;
}

.icon-btn {
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 18px;
  color: #94a3b8;
  padding: 4px;
  border-radius: 10px;
}

.icon-btn:hover {
  background: #f8fafc;
}

.icon-btn.remove:hover {
  color: #dc2626;
}

.info-btn {
  width: 26px;
  height: 26px;
  border-radius: 8px;
  background: transparent;
  border: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  padding: 0;
  transition: background 0.15s ease;
}

.info-icon {
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
}

.info-icon svg {
  width: 100%;
  height: 100%;
}

.info-btn:hover {
  background: #f3f4f6;
}

.info-btn:hover .info-icon {
  color: #475569;
}

.calendar-url {
  flex-shrink: 0;
}

.calendar-url a {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  border-radius: 8px;
  color: #94a3b8;
  transition: background 0.15s ease, color 0.15s ease;
}

.calendar-url a:hover {
  background: #f3f4f6;
  color: #2563eb;
}

.calendar-url svg {
  width: 14px;
  height: 14px;
}
</style>