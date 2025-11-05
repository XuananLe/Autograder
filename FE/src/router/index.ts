// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import NewExamView from '../views/NewExamView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: DashboardView // Trang chính
    },
    {
      path: '/new-exam',
      name: 'newExam',
      component: NewExamView // Trang chuyển hướng
    },
  ]
})

export default router