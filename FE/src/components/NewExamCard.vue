<template>
  <div class="exam-card exam-card--new" @click="navigateTo(to)">
    <div class="exam-card__info">
      <span class="mr-3">+</span>
      <slot></slot>
    </div>
    <span class="arrow-placeholder"></span> 
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'; 

// Định nghĩa props (đích đến của link)
defineProps({
  to: {
    type: String,
    required: true
  }
});

// 2. Lấy đối tượng router
const router = useRouter();

// 3. Định nghĩa hàm điều hướng
const navigateTo = (path:string) => {
  // Phương thức push sẽ chuyển hướng đến đường dẫn đã cho
  router.push(path);
};
</script>

<style scoped>
/* Giữ nguyên hoặc import CSS */
@import url('../styles/dashboard.css');

/* Cần thêm cursor: pointer để nhấn mạnh đây là element có thể click */
.exam-card--new {
  cursor: pointer;
}
</style>