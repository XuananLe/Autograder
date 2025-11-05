import { createApp } from 'vue';
import App from './App.vue';
import router from './router';  

// Tùy chọn: Import CSS gốc/toàn cục (nếu có)
import './assets/main.css'; 

const app = createApp(App);

// Dòng quan trọng: Gắn Vue Router vào ứng dụng
app.use(router); 

// Gắn ứng dụng Vue vào phần tử HTML có id="app" (trong index.html)
app.mount('#app');