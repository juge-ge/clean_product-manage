<template>
  <router-link to="/" class="logo-container">
    <div class="logo-content">
      <img 
        src="@/assets/logo.png" 
        alt="Logo" 
        class="logo-image"
      />
      <div
        v-show="!appStore.collapsed"
        class="logo-title-container"
      >
        <div class="logo-title">清洁生产智慧管理平台</div>
      </div>
    </div>
  </router-link>
</template>

<script setup>
import { useAppStore } from '@/store'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const title = t('app_name')

const appStore = useAppStore()
</script>

<style scoped>
.logo-container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100px;
  padding: 10px 12px;
  text-decoration: none;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  margin-bottom: 8px;
}

.logo-content {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  width: 100%;
}

.logo-image {
  width: 160px;
  height: 60px;
  object-fit: contain;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 8px;
}

.logo-title-container {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.logo-title {
  font-size: 24px;
  font-weight: bold;
  color: var(--primary-color);
  line-height: 1.1;
  letter-spacing: 0.3px;
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

/* 响应式设计 */
@media (max-width: 1600px) {
  .logo-image {
    width: 140px;
    height: 50px;
  }
  .logo-title {
    font-size: 22px;
  }
}

@media (max-width: 1400px) {
  .logo-image {
    width: 120px;
    height: 45px;
  }
  .logo-title {
    font-size: 20px;
  }
}

@media (max-width: 1200px) {
  .logo-image {
    width: 100px;
    height: 40px;
  }
  .logo-title {
    font-size: 18px;
  }
}
</style>
