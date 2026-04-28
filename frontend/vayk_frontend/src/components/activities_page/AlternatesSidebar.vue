<script setup>
import { ref } from 'vue'
import draggable from 'vuedraggable'
import { tripStore } from '../../stores/tripStores'
import AlternatesCard from './AlternatesCard.vue'

defineEmits(['toggle', 'open-detail'])

const sidebarWidth = ref(360)
const isResizing = ref(false)

function onResizeStart() {
  isResizing.value = true
  document.addEventListener('mousemove', onResize)
  document.addEventListener('mouseup', onResizeEnd)
}

function onResize(e) {
  if (!isResizing.value) return

  const newWidth = window.innerWidth - e.clientX
  // Set min/max width constraints
  if (newWidth >= 250 && newWidth <= 600) {
    sidebarWidth.value = newWidth
  }
}

function onResizeEnd() {
  isResizing.value = false
  document.removeEventListener('mousemove', onResize)
  document.removeEventListener('mouseup', onResizeEnd)
}

function onDragStart() {
  tripStore.isDraggingAlternate = true
}

function onDragEnd() {
  tripStore.isDraggingAlternate = false
}
</script>

<template>
  <aside
    class="alternates-sidebar"
    data-tour="alternates"
    :class="{ open: tripStore.isAlternatesOpen, resizing: isResizing }"
    :style="{ 
      width: `${sidebarWidth}px`,
      pointerEvents: tripStore.isDraggingAlternate ? 'none' : 'auto'
    }"
  >
    <div 
      class="resize-handle"
      @mousedown="onResizeStart"
      :class="{ active: isResizing }"
    />

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
        :group="{ name: 'activities', pull: true, put: true }"
        handle=".drag-handle"
        ghost-class="drag-ghost"
        chosen-class="drag-chosen"
        drag-class="drag-dragging"
        :animation="200"
        fallback-class="drag-fallback"
        class="alternates-dropzone"
        @start="onDragStart"
        @end="onDragEnd"
        @remove="tripStore.handleAlternatesChange()"
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
  z-index: 1000;
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

.alternates-sidebar.resizing {
  transition: none;
  user-select: none;
}

.resize-handle {
  position: absolute;
  left: 0;
  top: 0;
  width: 4px;
  height: 100%;
  cursor: ew-resize;
  background: transparent;
  transition: background 0.15s ease;
  z-index: 100;
}

.resize-handle:hover,
.resize-handle.active {
  background: #3b82f6;
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
