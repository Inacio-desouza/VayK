git commit<script setup>
import { tripStore } from '../../stores/tripStores'

defineEmits(['toggle'])
</script>

<template>
  <button
    v-if="!tripStore.isAlternatesOpen"
    class="alternates-tab"
    @click="$emit('toggle')"
  >
    <span class="tab-arrow">‹</span>
    <span class="tab-text">Alternates {{ tripStore.alternates.length }}</span>
  </button>

  <div
    v-if="tripStore.isAlternatesOpen"
    class="sidebar-backdrop"
    @click="$emit('toggle')"
  />
</template>

<style scoped>
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

.sidebar-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.08);
  z-index: 45;
}
</style>
