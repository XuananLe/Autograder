<template>
  <div>
    <div class="section-header">
      <h2 class="section-title">Info</h2>
      <span class="section-hint">Configure the info for this exam</span>
    </div>

    <div v-for="(field, key) in fields" :key="key" class="form-field">
      <label :for="key" class="form-field__label">{{ field.label }}</label>
      
      <input 
        v-if="field.type !== 'date'"
        :id="key"
        :type="field.type"
        :placeholder="field.placeholder"
        :value="formData[key]"
        @input="$emit('update:formData', { ...formData, [key]: ($event.target as HTMLInputElement).value })"
        class="form-field__input"
      >
      
      <div v-else class="form-field__input form-field__input--date-wrapper">
         <input 
            :id="key"
            type="text"
            :value="formData[key]"
            @input="$emit('update:formData', { ...formData, [key]: ($event.target as HTMLInputElement)?.value ?? '' })"
            :placeholder="field.placeholder"
            class="form-field__input"
        >
        <span>🗓️</span> 
      </div>
    </div>
    
    <div class="form-field" style="margin-top: 24px;">
        <label for="due" class="form-field__label" style="color: #ef4444;">Due</label>
        <input id="due" type="text" class="form-field__input" style="background-color: white; color: black;">
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue';
defineProps({
  formData: {
    type: Object,
    required: true
  }
});

defineEmits(['update:formData']);

// Cấu hình các trường form (Tên hiển thị, Kiểu, Placeholder)
const fields = {
  institute: { label: 'Institute', type: 'text', placeholder: 'Zanista University' },
  department: { label: 'Department', type: 'text', placeholder: 'Mathematics' },
  courseTitle: { label: 'Course Title', type: 'text', placeholder: 'Biomechanics' },
  courseLevel: { label: 'Course Level', type: 'text', placeholder: 'Undergraduate' },
  subject: { label: 'Subject', type: 'text', placeholder: 'Bone Mechanics' },
  date: { label: 'Date', type: 'date', placeholder: '15 May 2025' },
};
</script>

<style scoped>
@import url('../styles/form.css');
/* Cần thêm style đặc biệt cho input date nếu có */
.form-field__input--date-wrapper {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
</style>