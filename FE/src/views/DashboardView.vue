<template>
  <div class="dashboard-container">

    <header class="main-header">
      <div class="main-header__logo">
        <span class="text-xl font-bold">⚙️</span>
        <span class="ml-2 text-sm">Dashboard</span>
      </div>
      <div class="main-header__user-icon">
        <span class="text-xl">👤</span>
      </div>
    </header>

    <main class="dashboard-main">
      
      <router-link to="/" class="back-link">
        &lt;&lt; Back to Dashboard
      </router-link>

      <div class="dashboard-header">
        <h1 class="dashboard-title">GoodPoint</h1>
        <p class="dashboard-subtitle">
          Create a new exam or select a previous one
        </p>
      </div>

      <div class="exam-list">
        
        <div v-for="exam in exams" :key="exam.id">
          
          <NewExamCard 
            v-if="exam.type === 'header' && exam.status === 'new'" 
            to="/new-exam"
          >
            {{ exam.name }}
          </NewExamCard>

          <div v-else-if="exam.type === 'header'" :class="['exam-card', `exam-card--${exam.status}-header`]">
            <div class="exam-card__info">
              <span class="mr-3">{{ exam.status === 'ongoing' ? '📄' : '📜' }}</span>
              {{ exam.name }}
            </div>
            <button class="delete-icon">🗑️</button>
          </div>

          <div v-else :class="['exam-card', `exam-card--${exam.status}-item`]">
            <div class="exam-card__info">
              <span class="mr-3">{{ exam.status === 'ongoing' ? '📄' : '📜' }}</span>
              {{ exam.name }}
            </div>
            <span class="exam-card__date">{{ exam.date }}</span>
            
            <div v-if="exam.status === 'ongoing'" class="exam-card__action exam-card__upload-rubric">
              Upload rubric ⬆️
            </div>
            <div v-else class="exam-card__action exam-card__graded-label">
              Graded <span class="ml-2">✅</span>
            </div>
          </div>

        </div>

      </div>

    </main>

  </div>
</template>

<script setup lang ="ts">
import { ref } from 'vue';
import { RouterLink } from 'vue-router';
import NewExamCard from '../components/NewExamCard.vue';

// Dữ liệu Mock Data
const exams = ref([
  { id: 1, name: 'New Exam', date: '', type: 'header', status: 'new' },
  { id: 2, name: 'Ongoing Exams', date: '', type: 'header', status: 'ongoing' },
  { id: 3, name: 'Yr 7 Maths', date: '19 May 2025', type: 'item', status: 'ongoing' },
  { id: 4, name: 'Graded Exams', date: '', type: 'header', status: 'graded' },
  { id: 5, name: 'Old Exam', date: '18 May 2025', type: 'item', status: 'graded' },
]);
</script>

<style scoped src="../styles/dashboard.css"></style>