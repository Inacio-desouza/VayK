<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { tripStore } from '../stores/tripStores'
import itineraryMock from '../mock/itineraryMock.json'

const router = useRouter()

onMounted(() => {
  if (!tripStore.days.length) {
    tripStore.initializeItineraryState(itineraryMock)
  }
})

function goHome() {
  router.push('/')
}

function editTime(activity) {
  const current = activity.time || ''
  const next = window.prompt('Enter time (example: 9:00 AM). Leave empty to remove.', current)

  if (next === null) return
  tripStore.updateActivityTime(activity.id, next.trim() || undefined)
}

function openDetail(activity) {
  tripStore.openActivityDetail(activity)
}

function closeDetail() {
  tripStore.closeActivityDetail()
}

function removeFromDay(dayId, activityId) {
  tripStore.removeActivityFromDay(dayId, activityId)
}

function titleFor(activity) {
  return tripStore.getActivityTitle(activity)
}

function subtitleFor(activity) {
  if (activity.address) return activity.address
  if (activity.venue) return activity.venue
  if (activity.location) return activity.location
  return ''
}

function splitDateLabel(label) {
  if (!label) return { weekday: '', date: '' }

  const parts = label.split(',')
  if (parts.length >= 2) {
    return {
      weekday: parts[0].trim(),
      date: parts.slice(1).join(',').trim(),
    }
  }

  return {
    weekday: '',
    date: label,
  }
}
</script>

<template>
  <div class="page">
    <header class="header">
      <div class="header-inner">
        <div>
          <h1 class="title">{{ tripStore.tripTitle }}</h1>
          <p class="date-range">{{ tripStore.tripDates }}</p>
        </div>

        <div class="header-right">
          <div class="view-toggle">
            <button
              class="toggle-btn"
              :class="{ active: tripStore.activeView === 'list' }"
              @click="tripStore.setActiveView('list')"
            >
              <span class="toggle-icon" aria-hidden="true">
                <svg viewBox="0 0 20 20" fill="none">
                  <path d="M7 5H17" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
                  <path d="M7 10H17" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
                  <path d="M7 15H17" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
                  <path d="M3 5H3.01" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" />
                  <path d="M3 10H3.01" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" />
                  <path d="M3 15H3.01" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" />
                </svg>
              </span>
              <span>List</span>
            </button>

            <button
              class="toggle-btn"
              :class="{ active: tripStore.activeView === 'calendar' }"
              @click="tripStore.setActiveView('calendar')"
            >
              <span class="toggle-icon" aria-hidden="true">
                <svg viewBox="0 0 20 20" fill="none">
                  <rect x="3" y="4.5" width="14" height="12" rx="2.5" stroke="currentColor" stroke-width="1.8" />
                  <path d="M6.5 2.8V6.2" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
                  <path d="M13.5 2.8V6.2" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
                  <path d="M3 8H17" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
                </svg>
              </span>
              <span>Calendar</span>
            </button>
          </div>

          <button class="back-btn" @click="goHome">← Plan another trip</button>
        </div>
      </div>
    </header>

    <main class="content">
      <div class="content-inner">
        <section v-if="tripStore.activeView === 'list'" class="list-view">
          <div v-for="day in tripStore.days" :key="day.id" class="day-card">
            <div class="day-header">
              <p class="day-number">Day {{ day.dayNumber }}</p>
              <p class="day-weekday">{{ splitDateLabel(day.dateLabel).weekday }}</p>
              <h2 class="day-date">{{ splitDateLabel(day.dateLabel).date }}</h2>
            </div>

            <div class="day-body">
              <div
                v-for="activity in day.activities"
                :key="activity.id"
                class="activity-card"
                :class="{ timed: !!activity.time }"
              >
                <div class="activity-left">
                  <div class="drag-indicator">
                    <span v-if="activity.time" class="lock-icon" aria-hidden="true">
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

                    <span v-else class="grip-icon" aria-hidden="true">
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
                        @click="editTime(activity)"
                      >
                        {{ activity.time }}
                      </button>

                      <button
                        v-else
                        class="time-pill time-pill-ghost hover-only"
                        @click="editTime(activity)"
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
                  </div>
                </div>

                <div class="activity-actions">
                  <button class="info-btn" @click="openDetail(activity)">
                    <span class="info-icon">
                      <svg viewBox="0 0 20 20" fill="none">
                        <circle cx="10" cy="10" r="7.2" stroke="currentColor" stroke-width="1.6" />
                        <path d="M10 8.8V12.8" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
                        <circle cx="10" cy="6.6" r="0.9" fill="currentColor" />
                      </svg>
                    </span>
                  </button>

                  <button class="icon-btn remove" @click="removeFromDay(day.id, activity.id)">×</button>
                </div>
              </div>

              <p v-if="!day.activities.length" class="empty">
                No activities added for this day yet.
              </p>
            </div>
          </div>
        </section>

        <section v-else class="calendar-view">
          <div class="calendar-header">
            <h2>Full Trip Calendar</h2>
            <p>Scroll horizontally to view all days</p>
          </div>

          <div class="calendar-scroll">
            <div class="calendar-row">
              <div v-for="day in tripStore.days" :key="day.id" class="calendar-day">
                <div class="calendar-day-header">
                  <p class="day-number">Day {{ day.dayNumber }}</p>
                  <p class="day-weekday">{{ splitDateLabel(day.dateLabel).weekday }}</p>
                  <h3 class="day-date">{{ splitDateLabel(day.dateLabel).date }}</h3>
                </div>

                <div class="calendar-day-body">
                  <div
                    v-for="activity in day.activities"
                    :key="activity.id"
                    class="calendar-activity-card"
                    :class="{ timed: !!activity.time }"
                  >
                    <div class="calendar-card-top">
                      <div class="calendar-card-title-wrap">
                        <span class="mini-lock">
                          <span v-if="activity.time" class="lock-icon" aria-hidden="true">
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

                          <span v-else class="grip-icon" aria-hidden="true">
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

                      <div class="calendar-card-right">
                        <button
                          v-if="activity.time"
                          class="time-pill time-pill-filled visible"
                          @click="editTime(activity)"
                        >
                          {{ activity.time }}
                        </button>

                        <button
                          v-else
                          class="time-pill time-pill-ghost hover-only"
                          @click="editTime(activity)"
                        >
                          Add time
                        </button>

                        <button class="info-btn" @click="openDetail(activity)">
                          <span class="info-icon">
                            <svg viewBox="0 0 20 20" fill="none">
                              <circle cx="10" cy="10" r="7.2" stroke="currentColor" stroke-width="1.6" />
                              <path d="M10 8.8V12.8" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
                              <circle cx="10" cy="6.6" r="0.9" fill="currentColor" />
                            </svg>
                          </span>
                        </button>

                        <button class="icon-btn remove" @click="removeFromDay(day.id, activity.id)">×</button>
                      </div>
                    </div>
                  </div>

                  <p v-if="!day.activities.length" class="empty">
                    No activities yet.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </main>

    <button
      v-if="!tripStore.isAlternatesOpen"
      class="alternates-tab"
      @click="tripStore.toggleAlternates()"
    >
      <span class="tab-arrow">‹</span>
      <span class="tab-text">Alternates {{ tripStore.alternates.length }}</span>
    </button>

    <aside class="alternates-sidebar" :class="{ open: tripStore.isAlternatesOpen }">
      <div class="alternates-header">
        <div>
          <h2>Alternate Activities</h2>
          <p>{{ tripStore.alternates.length }} available</p>
        </div>
        <button class="icon-btn" @click="tripStore.toggleAlternates()">›</button>
      </div>

      <div class="alternates-body">
        <div
          v-for="activity in tripStore.alternates"
          :key="activity.id"
          class="alternate-card"
        >
          <div class="activity-info">
            <h3 class="activity-title">{{ titleFor(activity) }}</h3>

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
          </div>

          <div class="activity-actions">
            <button class="info-btn" @click="openDetail(activity)">
              <span class="info-icon">
                <svg viewBox="0 0 20 20" fill="none">
                  <circle cx="10" cy="10" r="7.2" stroke="currentColor" stroke-width="1.6" />
                  <path d="M10 8.8V12.8" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
                  <circle cx="10" cy="6.6" r="0.9" fill="currentColor" />
                </svg>
              </span>
            </button>

            <button
              class="icon-btn"
              @click="tripStore.moveActivityToDay(tripStore.days[0]?.id, activity)"
            >
              +
            </button>
          </div>
        </div>

        <p v-if="!tripStore.alternates.length" class="empty">
          All alternate activities have been added.
        </p>
      </div>

      <div class="alternates-footer">
        Add from this panel first. Drag and drop can come after the layout is working.
      </div>
    </aside>

    <div
      v-if="tripStore.isAlternatesOpen"
      class="sidebar-backdrop"
      @click="tripStore.toggleAlternates()"
    />

    <div
      v-if="tripStore.selectedActivity"
      class="modal-backdrop"
      @click="closeDetail"
    >
      <div class="modal-card" @click.stop>
        <div class="modal-header">
          <h2>{{ titleFor(tripStore.selectedActivity) }}</h2>
          <button class="icon-btn" @click="closeDetail">×</button>
        </div>

        <div class="modal-body">
          <template v-if="tripStore.selectedActivity">
            <div
              v-if="tripStore.selectedActivity.address || tripStore.selectedActivity.location"
              class="modal-section modal-row"
            >
              <div class="modal-row-icon">
                <svg viewBox="0 0 20 20" fill="none">
                  <path
                    d="M10 17C10 17 15 12.4 15 8.5C15 5.46 12.76 3 10 3C7.24 3 5 5.46 5 8.5C5 12.4 10 17 10 17Z"
                    stroke="currentColor"
                    stroke-width="1.8"
                  />
                  <circle cx="10" cy="8.3" r="2.1" stroke="currentColor" stroke-width="1.8" />
                </svg>
              </div>

              <div class="modal-row-content">
                <p class="modal-label">
                  {{ tripStore.selectedActivity.address ? 'Address' : 'Location' }}
                </p>
                <p class="modal-value">
                  {{ tripStore.selectedActivity.address || tripStore.selectedActivity.location }}
                </p>
              </div>
            </div>

            <div
              v-if="tripStore.selectedActivity.rating"
              class="modal-section modal-row"
            >
              <div class="modal-row-icon">
                <svg viewBox="0 0 20 20" fill="none">
                  <path
                    d="M10 2.8L12.22 7.3L17.2 8.02L13.6 11.54L14.45 16.5L10 14.16L5.55 16.5L6.4 11.54L2.8 8.02L7.78 7.3L10 2.8Z"
                    stroke="currentColor"
                    stroke-width="1.6"
                    stroke-linejoin="round"
                  />
                </svg>
              </div>

              <div class="modal-row-content">
                <p class="modal-label">Rating</p>
                <p class="modal-value">
                  <span class="modal-rating-star">★</span>
                  {{ tripStore.selectedActivity.rating }}
                  <span v-if="tripStore.selectedActivity.reviewCount" class="modal-muted">
                    ({{ tripStore.selectedActivity.reviewCount.toLocaleString() }} reviews)
                  </span>
                </p>
              </div>
            </div>

            <div v-if="tripStore.selectedActivity.description" class="modal-section">
              <p class="modal-label">Description</p>
              <p class="modal-description">{{ tripStore.selectedActivity.description }}</p>
            </div>

            <a
              v-if="tripStore.selectedActivity.link"
              :href="tripStore.selectedActivity.link"
              target="_blank"
              rel="noopener noreferrer"
              class="visit-link"
            >
              Visit website
            </a>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page {
  min-height: 100vh;
  background: #fcfcfd;
  color: #111827;
  padding-bottom: 40px;
}

.header {
  border-bottom: 1px solid #e5e7eb;
  padding: 28px 24px 20px;
}

.header-inner,
.content-inner {
  max-width: 1360px;
  margin: 0 auto;
}

.header-inner {
  display: flex;
  justify-content: space-between;
  gap: 24px;
  align-items: flex-start;
}

.title {
  margin: 0;
  font-size: 34px;
  line-height: 1.08;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.date-range {
  margin: 8px 0 0;
  font-size: 16px;
  color: #6b7280;
}

.header-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 12px;
}

.view-toggle {
  display: flex;
  gap: 4px;
  background: #f3f4f6;
  padding: 4px;
  border-radius: 16px;
}

.toggle-btn {
  border: none;
  background: transparent;
  padding: 10px 14px;
  border-radius: 12px;
  cursor: pointer;
  font-size: 15px;
  color: #475569;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

.toggle-btn.active {
  background: white;
  color: #1f2f6b;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.14);
}

.toggle-icon {
  width: 18px;
  height: 18px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.toggle-icon svg,
.lock-icon svg,
.grip-icon svg,
.meta-icon svg {
  width: 100%;
  height: 100%;
  display: block;
}

.back-btn {
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 14px;
  color: #475569;
}

.content {
  padding: 28px 24px;
}

.list-view {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.day-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 24px;
  overflow: hidden;
}

.day-header {
  background: #f8fafc;
  padding: 20px 24px;
  border-bottom: 1px solid #e5e7eb;
}

.day-number {
  margin: 0 0 2px;
  font-size: 14px;
  color: #6b7280;
}

.day-weekday {
  margin: 0 0 4px;
  font-size: 14px;
  color: #6b7280;
}

.day-date {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.day-body {
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.activity-card,
.alternate-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 20px;
  padding: 16px 18px;
  display: flex;
  justify-content: space-between;
  gap: 14px;
  box-shadow: 0 1px 6px rgba(15, 23, 42, 0.04);
}
.calendar-activity-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 20px;
  padding: 16px 18px;
  box-shadow: 0 1px 6px rgba(15, 23, 42, 0.04);
}

.activity-card.timed,
.calendar-activity-card.timed {
  border-left: 4px solid #d5dbe6;
}

.activity-left {
  display: flex;
  gap: 14px;
  flex: 1;
  min-width: 0;
}

.drag-indicator,
.mini-lock {
  color: #d1d5db;
  flex-shrink: 0;
  line-height: 1;
  padding-top: 2px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
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

.calendar-card-top {
  display: flex;
  align-items: flex-start;
  gap: 14px;
}


.activity-title,
.calendar-card-title {
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

.activity-meta {
  margin: 6px 0 0;
  font-size: 14px;
  color: #6b7280;
}

.star {
  color: #eab308;
}

.time-btn,
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

.activity-card:hover .hover-only,
.calendar-activity-card:hover .hover-only {
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

.calendar-view {
  width: 100%;
}

.calendar-header h2 {
  margin: 0;
  font-size: 26px;
  letter-spacing: -0.02em;
}

.calendar-header p {
  margin: 6px 0 20px;
  color: #6b7280;
  font-size: 15px;
}

.calendar-scroll {
  overflow-x: auto;
  padding-bottom: 8px;
}

.calendar-row {
  display: grid;
  grid-auto-flow: column;
  grid-auto-columns: calc((1360px - 48px) / 3);
  gap: 24px;
  min-width: max-content;
}

.calendar-day {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 24px;
  overflow: hidden;
}

.calendar-day-header {
  background: #f8fafc;
  padding: 18px 20px;
  border-bottom: 1px solid #e5e7eb;
}

.calendar-day-body {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-height: 520px;
}

.calendar-activity-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 20px;
  padding: 16px 18px;
  box-shadow: 0 1px 6px rgba(15, 23, 42, 0.04);
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
.calendar-card-right {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  flex-shrink: 0;
  margin-left: auto;
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

.alternates-tab {
  position: fixed;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  border: 1px solid #e5e7eb;
  border-right: none;
  background: white;
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
  border-radius: 18px 0 0 18px;
  padding: 16px 10px;
  z-index: 40;
  cursor: pointer;
}

.tab-arrow {
  display: block;
  font-size: 18px;
  color: #64748b;
  margin-bottom: 8px;
}

.tab-text {
  writing-mode: vertical-rl;
  text-orientation: mixed;
  font-size: 13px;
  color: #334155;
  font-weight: 600;
}

.alternates-sidebar {
  position: fixed;
  top: 0;
  right: 0;
  width: 360px;
  height: 100vh;
  background: white;
  border-left: 1px solid #e5e7eb;
  box-shadow: -8px 0 30px rgba(15, 23, 42, 0.08);
  transform: translateX(100%);
  transition: transform 0.28s ease;
  z-index: 50;
  display: flex;
  flex-direction: column;
}

.alternates-sidebar.open {
  transform: translateX(0);
}

.alternates-header {
  padding: 22px 20px 18px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  gap: 12px;
}

.alternates-header h2 {
  margin: 0;
  font-size: 24px;
  letter-spacing: -0.02em;
}

.alternates-header p {
  margin: 6px 0 0;
  color: #6b7280;
  font-size: 14px;
}

.alternates-body {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.alternates-footer {
  border-top: 1px solid #e5e7eb;
  background: #f8fafc;
  padding: 14px 16px;
  font-size: 12px;
  color: #475569;
}

.sidebar-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.08);
  z-index: 45;
}

.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.24);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  z-index: 70;
}

.modal-card {
  width: 100%;
  max-width: 760px;
  background: white;
  border-radius: 28px;
  overflow: hidden;
  box-shadow: 0 24px 60px rgba(15, 23, 42, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: center;
  padding: 24px 28px 18px;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h2 {
  margin: 0;
  font-size: 26px;
  letter-spacing: -0.02em;
}

.modal-body {
  padding: 28px;
}

.modal-section + .modal-section {
  margin-top: 24px;
}

.modal-row {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.modal-row-icon {
  width: 28px;
  height: 28px;
  color: #98a2b3;
  flex-shrink: 0;
  margin-top: 2px;
}

.modal-row-icon svg {
  width: 100%;
  height: 100%;
  display: block;
}

.modal-row-content {
  flex: 1;
}

.modal-label {
  margin: 0 0 8px;
  color: #6b7280;
  font-size: 14px;
  font-weight: 500;
}

.modal-value {
  margin: 0;
  color: #0f172a;
  font-size: 16px;
  line-height: 1.5;
}

.modal-description {
  margin: 0;
  color: #334155;
  font-size: 16px;
  line-height: 1.65;
  max-width: 52ch;
}

.modal-rating-star {
  color: #eab308;
  margin-right: 4px;
}

.modal-muted {
  color: #6b7280;
}

.visit-link {
  display: inline-block;
  margin-top: 24px;
  background: #27429b;
  color: white;
  text-decoration: none;
  padding: 13px 20px;
  border-radius: 14px;
  font-weight: 600;
  font-size: 15px;
}

.empty {
  margin: 8px 0 0;
  color: #94a3b8;
  font-size: 14px;
}

@media (max-width: 1100px) {
  .calendar-row {
    grid-auto-columns: 360px;
  }
}

@media (max-width: 900px) {
  .header-inner {
    flex-direction: column;
    align-items: flex-start;
  }

  .header-right {
    width: 100%;
    align-items: flex-start;
  }

  .title {
    font-size: 30px;
  }

  .content {
    padding: 20px 16px;
  }

  .header {
    padding: 22px 16px 18px;
  }

  .alternates-sidebar {
    width: min(100%, 360px);
  }

  .calendar-row {
    grid-auto-columns: 320px;
  }
}

@media (max-width: 640px) {
  .activity-card,
  .alternate-card,
  .calendar-activity-card {
    padding: 14px 15px;
  }

  .activity-top-row {
    flex-direction: column;
    align-items: flex-start;
  }

  .time-btn,
  .time-pill {
    align-self: flex-start;
  }

  .day-body,
  .day-header {
    padding-left: 16px;
    padding-right: 16px;
  }

  .modal-card {
    max-width: 100%;
    border-radius: 22px;
  }

  .modal-header,
  .modal-body {
    padding-left: 18px;
    padding-right: 18px;
  }
}
</style>