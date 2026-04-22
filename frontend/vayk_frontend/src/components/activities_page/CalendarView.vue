<script setup>
import draggable from 'vuedraggable'
import { tripStore } from '../../stores/tripStores'
import CalendarActivityCard from './CalendarActivityCard.vue'

const emit = defineEmits(['edit-time', 'open-detail', 'remove-activity'])

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

function handleDayChange(dayId) {
  tripStore.handleDayActivitiesChange(dayId)
}
</script>

<template>
  <section class="calendar-view">
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
            <draggable
              v-model="day.activities"
              item-key="id"
              group="activities"
              handle=".drag-handle"
              ghost-class="drag-ghost"
              chosen-class="drag-chosen"
              drag-class="drag-dragging"
              :animation="200"
              class="calendar-dropzone"
              @change="handleDayChange(day.id)"
            >
              <template #item="{ element }">
                <CalendarActivityCard
                  :activity="element"
                  :day-id="day.id"
                  @edit-time="emit('edit-time', element.id, $event)"
                  @open-detail="emit('open-detail', element)"
                  @remove="emit('remove-activity', day.id, element.id)"
                />
              </template>
            </draggable>

            <p v-if="!day.activities.length" class="empty">
              No activities yet.
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
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

.calendar-day-body {
  padding: 16px;
  min-height: 520px;
}

.calendar-dropzone {
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-height: 24px;
  border-radius: 18px;
}

:deep(.drag-ghost) {
  opacity: 0.45;
}

:deep(.drag-chosen) {
  transform: scale(0.995);
}

:deep(.drag-dragging) {
  cursor: grabbing;
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
  .calendar-row {
    grid-auto-columns: 320px;
  }
}
</style>