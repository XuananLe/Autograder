<template>
  <div class="new-exam-container">
    <router-link to="/" class="back-link">&lt;&lt; Back to AI Grader</router-link>

    <div class="flex justify-between items-center border-b pb-4 mb-8">
      <h1 class="title">Mechanics 1</h1>
      <span class="text-gray-500 cursor-pointer">🗑️</span>
    </div>

    <FormTabs 
      :tabs="tabs" 
      :activeStep="currentStep" 
      @changeStep="currentStep = $event"
    />

    <div class="form-content">
      
      <StepInfo 
        v-if="currentStep === 0" 
        :formData="formData"
        @update:formData="formData = $event"
      />

      <div v-else-if="currentStep === 1">
        <h2 class="section-title">Rubric Content (Step 2)</h2>
        <p class="text-gray-500">Nội dung tạo/tải Rubric ở đây.</p>
      </div>
      
      </div>
    
    <button class="next-button" @click="nextStep">
      Next: {{ tabs[currentStep + 1]?.label ?? 'Submit' }} →
    </button>

  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { RouterLink } from 'vue-router';
import FormTabs from '../components/FormTabs.vue';
import StepInfo from '../components/StepInfo.vue';

// 1. Quản lý trạng thái bước hiện tại
const currentStep = ref(0);

// 2. Định nghĩa các bước (tabs)
const tabs = ref([
  { label: 'Info', component: 'StepInfo' },
  { label: 'Rubric', component: 'StepRubric' },
  { label: 'Student answers', component: 'StepAnswers' },
  { label: 'Grading', component: 'StepGrading' },
]);

// 3. Dữ liệu Form (Lưu trữ trạng thái toàn bộ form)
const formData = ref({
  institute: 'Zanista University',
  department: 'Mathematics',
  courseTitle: 'Biomechanics',
  courseLevel: 'Undergraduate',
  subject: 'Bone Mechanics',
  date: '15 May 2025',
  due: ''
});

// 4. Logic chuyển bước
const nextStep = () => {
  if (currentStep.value < tabs.value.length - 1) {
    currentStep.value++;
  } else {
    // Logic khi submit form cuối cùng
    alert('Form Submitted! Data: ' + JSON.stringify(formData.value, null, 2));
  }
};
</script>

<style scoped>
@import url('../styles/form.css');
/* Import các style chung từ dashboard.css */
@import url('../styles/dashboard.css');

/* Cần thêm một chút style cho thanh header chung */
.main-header {
  border-bottom: none; /* Bỏ border nếu form này có header riêng */
}
</style>