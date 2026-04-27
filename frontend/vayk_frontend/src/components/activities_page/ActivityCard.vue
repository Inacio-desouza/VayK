<script setup>
import { tripStore } from '../../stores/tripStores'

const props = defineProps({
  activity: {
    type: Object,
    required: true,
  },
  dayId: String,
})

const emit = defineEmits(['edit-time', 'open-detail', 'remove'])

function titleFor(activity) {
  return tripStore.getActivityTitle(activity)
}

function formatTime(timeString) {
  if (!timeString) return ''
  // If timeString contains a date portion (e.g., "2026-05-04 02:00 PM"), extract just the time
  const match = timeString.match(/(\d{1,2}:\d{2}\s*[AP]M)/i)
  return match ? match[1] : timeString
}

function subtitleFor(activity) {
  if (activity.address) return activity.address
  if (activity.venue) return activity.venue
  if (activity.location) return activity.location
  return ''
}

function handleEditTime() {
  const current = props.activity.time || ''
  const next = window.prompt('Enter time (example: 9:00 AM). Leave empty to remove.', current)

  if (next === null) return
  emit('edit-time', next.trim() || undefined)
}

function handleOpenDetail() {
  emit('open-detail')
}

function handleRemove() {
  emit('remove', props.dayId)
}
</script>

<template>
  <div class="activity-card" :class="{ 'timed-card': !!activity.time }">
    <div class="activity-left">
      <div
        class="drag-indicator"
        :class="{ 'drag-handle': !activity.time }"
        aria-hidden="true"
      >
        <span v-if="activity.time" class="lock-icon">
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

        <span v-else class="grip-icon">
          <svg viewBox="0 0 20 20" fill="currentColor">
            <circle cx="7" cy="5" r="1.2" />
            <circle cx="13" cy="5" r="1.2" />
            <circle cx="7" cy="10" r="1.2" />
            <circle cx="13" cy="10" r="1.2" />
            <circle cx="7" cy="15" r="1.2" />
            <circle cx="13" cy="15" r="1.2" />
          </svg>
        </span>
      </div>

      <div class="activity-info">
        <div class="activity-top-row">
          <h3 class="activity-title">{{ titleFor(activity) }}</h3>

          <button
            v-if="activity.time"
            class="time-pill time-pill-filled visible"
            @click="handleEditTime"
          >
            {{ formatTime(activity.time) }}
          </button>

          <button
            v-else
            class="time-pill time-pill-ghost hover-only"
            @click="handleEditTime"
          >
            Add time
          </button>
        </div>

        <p v-if="subtitleFor(activity)" class="activity-subtitle">
          <span class="meta-icon" aria-hidden="true">
            <svg viewBox="0 0 20 20" fill="none">
              <path
                d="M10 17C10 17 15 12.4 15 8.5C15 5.46 12.76 3 10 3C7.24 3 5 5.46 5 8.5C5 12.4 10 17 10 17Z"
                stroke="currentColor"
                stroke-width="1.8"
              />
              <circle cx="10" cy="8.3" r="2.1" stroke="currentColor" stroke-width="1.8" />
            </svg>
          </span>
          <span class="subtitle-text">{{ subtitleFor(activity) }}</span>
        </p>

        <p v-if="activity.rating" class="activity-meta">
          <span class="star">★</span>
          {{ activity.rating }}
          <span v-if="activity.reviewCount">
            ({{ activity.reviewCount.toLocaleString() }})
          </span>
        </p>

        <p v-if="activity.url" class="activity-url">
          <a :href="activity.url" target="_blank" rel="noopener noreferrer">
            View on website
            <svg viewBox="0 0 16 16" fill="none">
              <path d="M12.5 8.5H3.5M12.5 8.5V3.5M12.5 8.5V13.5M3.5 8.5H13.5M3.5 8.5V3.5M3.5 8.5V13.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </a>
        </p>
      </div>
    </div>

    <div class="activity-actions">
      <button class="info-btn" @click="handleOpenDetail">
        <span class="info-icon">
          <svg viewBox="0 0 20 20" fill="none">
            <circle cx="10" cy="10" r="7.2" stroke="currentColor" stroke-width="1.6" />
            <path d="M10 8.8V12.8" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
            <circle cx="10" cy="6.6" r="0.9" fill="currentColor" />
          </svg>
        </span>
      </button>

      <button class="icon-btn remove" @click="handleRemove">×</button>
    </div>
  </div>
</template>

<style scoped>
.activity-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 20px;
  padding: 16px 18px;
  display: flex;
  justify-content: space-between;
  gap: 14px;
  box-shadow: 0 1px 6px rgba(15, 23, 42, 0.04);
}

.activity-card.timed-card {
  border-left: 4px solid #d5dbe6;
}

.activity-left {
  display: flex;
  gap: 14px;
  flex: 1;
  min-width: 0;
}

.drag-indicator {
  color: #d1d5db;
  flex-shrink: 0;
  line-height: 1;
  padding-top: 2px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
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

.activity-info {
  flex: 1;
  min-width: 0;
}

.activity-top-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
}

.activity-title {
  margin: 0;
  font-size: 17px;
  font-weight: 600;
  line-height: 1.28;
  letter-spacing: -0.01em;
  color: #0f172a;
}

.activity-subtitle {
  margin: 6px 0 0;
  font-size: 14px;
  color: #667085;
  display: flex;
  align-items: center;
  min-width: 0;
}

.subtitle-text {
  display: inline-block;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.meta-icon {
  width: 15px;
  height: 15px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #667085;
  margin-right: 6px;
  flex-shrink: 0;
}

.meta-icon svg {
  width: 100%;
  height: 100%;
  display: block;
}

.activity-meta {
  margin: 6px 0 0;
  font-size: 14px;
  color: #6b7280;
}

.star {
  color: #eab308;
}

.activity-url {
  margin: 6px 0 0;
  font-size: 14px;
}

.activity-url a {
  color: #2563eb;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.activity-url a:hover {
  text-decoration: underline;
}

.activity-url svg {
  width: 14px;
  height: 14px;
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

.activity-card:hover .hover-only {
  opacity: 1;
  pointer-events: auto;
}

.activity-actions {
  display: flex;
  gap: 8px;
  align-items: flex-start;
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
</style>