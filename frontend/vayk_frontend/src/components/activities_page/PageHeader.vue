<script setup>
import { useRouter } from 'vue-router'
import { tripStore } from '../../stores/tripStores'
import { downloadICS } from '../../utils/exportICS'

const router = useRouter()

function goHome() {
  router.push('/')
}
</script>

<template>
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

        <button class="export-btn" @click="downloadICS">
          <span class="export-icon" aria-hidden="true">
            <svg viewBox="0 0 20 20" fill="none">
              <path d="M10 3V13" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
              <path d="M6 10L10 14L14 10" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
              <path d="M3 16H17" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
            </svg>
          </span>
          Export to Calendar
        </button>

        <button class="back-btn" @click="goHome">← Plan another trip</button>
      </div>
    </div>
  </header>
</template>

<style scoped>
.header {
  border-bottom: 1px solid #e5e7eb;
  padding: 28px 24px 20px;
}

.header-inner {
  max-width: 1360px;
  margin: 0 auto;
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

.toggle-icon svg {
  width: 100%;
  height: 100%;
  display: block;
}

.export-btn {
  border: 1px solid #e5e7eb;
  background: white;
  padding: 10px 16px;
  border-radius: 14px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  color: #334155;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06);
  transition: background 0.15s ease, box-shadow 0.15s ease;
}

.export-btn:hover {
  background: #f8fafc;
  box-shadow: 0 2px 6px rgba(15, 23, 42, 0.1);
}

.export-icon {
  width: 17px;
  height: 17px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.export-icon svg {
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

  .header {
    padding: 22px 16px 18px;
  }
}

@media (max-width: 640px) {
  .header {
    padding: 22px 16px 18px;
  }
}
</style>
