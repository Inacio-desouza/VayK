<script setup>
import { tripStore } from '../../stores/tripStores'

defineEmits(['close'])

function titleFor(activity) {
  return tripStore.getActivityTitle(activity)
}
</script>

<template>
  <div
    v-if="tripStore.selectedActivity"
    class="modal-backdrop"
    @click="$emit('close')"
  >
    <div class="modal-card" @click.stop>
      <div class="modal-header">
        <h2>{{ titleFor(tripStore.selectedActivity) }}</h2>
        <button class="icon-btn" @click="$emit('close')">×</button>
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
</template>

<style scoped>
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

@media (max-width: 640px) {
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
