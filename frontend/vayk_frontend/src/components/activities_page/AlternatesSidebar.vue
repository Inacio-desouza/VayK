<script setup>
import draggable from 'vuedraggable'
import { tripStore } from '../../stores/tripStores'
import AlternatesCard from './AlternatesCard.vue'

defineEmits(['toggle', 'open-detail'])

function handleAlternatesChange() {
  tripStore.handleAlternatesChange()
}
</script>

<template>
  <aside class="alternates-sidebar" :class="{ open: tripStore.isAlternatesOpen }">
    <div class="alternates-header">
      <div>
        <h2>Alternate Activities</h2>
        <p>{{ tripStore.alternates.length }} available</p>
      </div>
      <button class="icon-btn" @click="$emit('toggle')">›</button>
    </div>

    <div class="alternates-body">
      <draggable
        v-model="tripStore.alternates"
        item-key="id"
        group="activities"
        handle=".drag-handle"
        ghost-class="drag-ghost"
        chosen-class="drag-chosen"
        drag-class="drag-dragging"
        :animation="200"
        class="alternates-dropzone"
        @change="handleAlternatesChange"
      >
        <template #item="{ element }">
          <AlternatesCard
            :activity="element"
            @open-detail="$emit('open-detail', element)"
          />
        </template>
      </draggable>

      <p v-if="!tripStore.alternates.length" class="empty">
        All alternate activities have been added.
      </p>
    </div>

    <div class="alternates-footer">
      Untimed activities can be dragged anywhere. Timed activities stay fixed, but editing their time will reposition them.
    </div>
  </aside>
</template>

<style scoped>
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
}

.alternates-dropzone {
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-height: 24px;
}

.alternates-footer {
  border-top: 1px solid #e5e7eb;
  background: #f8fafc;
  padding: 14px 16px;
  font-size: 12px;
  color: #475569;
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

@media (max-width: 900px) {
  .alternates-sidebar {
    width: min(100%, 360px);
  }
}
</style>