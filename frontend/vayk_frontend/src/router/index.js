import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ActivitiesPage from '../views/ActivitiesPage.vue'
import LoadingView from '../views/LoadingView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/loading', name: 'loading', component: LoadingView },
    { path: '/activities', name: 'activities', component: ActivitiesPage },
  ],
})

export default router
