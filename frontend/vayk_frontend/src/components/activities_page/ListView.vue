<script setup>
import { tripStore } from '../../stores/tripStores'
import DayCard from './DayCard.vue'

defineEmits(['edit-time', 'open-detail', 'remove-activity'])
</script>

<template>
  <section class="list-view">
    <DayCard
      v-for="day in tripStore.days"
      :key="day.id"
      :day="day"
      @edit-time="(activityId, time) => $emit('edit-time', activityId, time)"
      @open-detail="(activity) => $emit('open-detail', activity)"
      @remove-activity="(dayId, activityId) => $emit('remove-activity', dayId, activityId)"
    />
  </section>
</template>

<style scoped>
.list-view {
  display: flex;
  flex-direction: column;
  gap: 24px;
}
</style>