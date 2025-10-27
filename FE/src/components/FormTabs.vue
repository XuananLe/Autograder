<template>
  <div class="tabs-container">
    <div 
      v-for="(tab, index) in tabs" 
      :key="index"
      :class="['tab-item', {'tab-item--active': activeStep === index, 'tab-item--inactive': activeStep !== index}]"
      @click="$emit('changeStep', index)"
    >
      {{ tab.label }}
    </div>
  </div>
</template>

<script setup lang="ts">
// Khai báo kiểu cho Tab và props để TypeScript biết cấu trúc
interface Tab {
  label: string;
}

defineProps<{
  tabs: Tab[];
  activeStep: number;
}>();

// Khai báo sự kiện để gửi lên component cha khi tab được click
defineEmits(['changeStep']);
</script>

<style scoped>
@import url('../styles/form.css');
</style>