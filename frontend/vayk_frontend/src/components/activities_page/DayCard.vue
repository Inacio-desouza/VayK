<script setup>
import draggable from 'vuedraggable'
import { tripStore } from '../../stores/tripStores'
import ActivityCard from './ActivityCard.vue'

defineProps({
  day: {
    type: Object,
    required: true,
  },
})

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
  <div class="day-card">
    <div class="day-header">
      <p class="day-number">Day {{ day.dayNumber }}</p>
      <p class="day-weekday">{{ splitDateLabel(day.dateLabel).weekday }}</p>
      <h2 class="day-date">{{ splitDateLabel(day.dateLabel).date }}</h2>
    </div>

    <div class="day-body">
      <draggable
        v-model="day.activities"
        item-key="id"
        group="activities"
        handle=".drag-handle"
        ghost-class="drag-ghost"
        chosen-class="drag-chosen"
        drag-class="drag-dragging"
        :animation="200"
        class="activities-dropzone"
        @change="handleDayChange(day.id)"
      >
        <template #item="{ element }">
          <ActivityCard
            :activity="element"
            :day-id="day.id"
            @edit-time="emit('edit-time', element.id, $event)"
            @open-detail="emit('open-detail', element)"
            @remove="emit('remove-activity', day.id, element.id)"
          />
        </template>
      </draggable>

      <p v-if="!day.activities.length" class="empty">
        No activities added for this day yet.
      </p>
    </div>
  </div>
</template>

<style scoped>
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
}

.activities-dropzone {
  display: flex;
  flex-direction: column;
  gap: 14px;
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

@media (max-width: 640px) {
  .day-body,
  .day-header {
    padding-left: 16px;
    padding-right: 16px;
  }
}
</style>