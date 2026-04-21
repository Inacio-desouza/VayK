<script setup>
import { onMounted } from 'vue'
import { tripStore } from '../stores/tripStores'
import itineraryMock from '../mock/itineraryMock.json'
import PageHeader from '../components/activities_page/PageHeader.vue'
import ListView from '../components/activities_page/ListView.vue'
import CalendarView from '../components/activities_page/CalendarView.vue'
import AlternatesTab from '../components/activities_page/AlternatesTab.vue'
import AlternatesSidebar from '../components/activities_page/AlternatesSidebar.vue'
import ActivityDetailModal from '../components/activities_page/ActivityDetailModal.vue'

onMounted(() => {
  if (!tripStore.days.length) {
    tripStore.initializeItineraryState(itineraryMock)
  }
})

function handleEditTime(activityId, newTime) {
  tripStore.updateActivityTime(activityId, newTime)
}

function handleOpenDetail(activity) {
  tripStore.openActivityDetail(activity)
}

function handleCloseDetail() {
  tripStore.closeActivityDetail()
}

function handleRemoveActivity(dayId, activityId) {
  tripStore.removeActivityFromDay(dayId, activityId)
}

function handleToggleAlternates() {
  tripStore.toggleAlternates()
}

function handleAddActivityFromAlternates(activity) {
  tripStore.moveActivityToDay(tripStore.days[0]?.id, activity)
}
</script>

<template>
  <div class="page">
    <PageHeader />

    <main class="content">
      <div class="content-inner">
        <ListView
          v-if="tripStore.activeView === 'list'"
          @edit-time="handleEditTime"
          @open-detail="handleOpenDetail"
          @remove-activity="handleRemoveActivity"
        />

        <CalendarView
          v-else
          @edit-time="handleEditTime"
          @open-detail="handleOpenDetail"
          @remove-activity="handleRemoveActivity"
        />
      </div>
    </main>

    <AlternatesTab @toggle="handleToggleAlternates" />

    <AlternatesSidebar
      @toggle="handleToggleAlternates"
      @open-detail="handleOpenDetail"
      @add-activity="handleAddActivityFromAlternates"
    />

    <ActivityDetailModal @close="handleCloseDetail" />
  </div>
</template>

<style scoped>
.page {
  min-height: 100vh;
  background: #fcfcfd;
  color: #111827;
  padding-bottom: 40px;
}

.content {
  padding: 28px 24px;
}

.content-inner {
  max-width: 1360px;
  margin: 0 auto;
}

@media (max-width: 900px) {
  .content {
    padding: 20px 16px;
  }
}
</style>
