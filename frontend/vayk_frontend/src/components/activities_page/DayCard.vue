<script setup>
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
</script>

<template>
  <div class="day-card">
    <div class="day-header">
      <p class="day-number">Day {{ day.dayNumber }}</p>
      <p class="day-weekday">{{ splitDateLabel(day.dateLabel).weekday }}</p>
      <h2 class="day-date">{{ splitDateLabel(day.dateLabel).date }}</h2>
    </div>

    <div class="day-body">
      <ActivityCard
        v-for="activity in day.activities"
        :key="activity.id"
        :activity="activity"
        :day-id="day.id"
        @edit-time="emit('edit-time', activity.id, $event)"
        @open-detail="emit('open-detail', activity)"
        @remove="emit('remove-activity', day.id, activity.id)"
      />

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
  display: flex;
  flex-direction: column;
  gap: 14px;
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
