<template>
  <router-link h-80 f-c-c to="/" class="logo-container">
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
  justify-content: flex-start;
  height: 80px;
  padding: 0 12px;
  text-decoration: none;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  margin-bottom: 8px;
}

.logo-image {
  width: 36px;
  height: 36px;
  object-fit: contain;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  flex-shrink: 0;
  margin-right: 8px;
}

.logo-title-container {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  flex: 1;
}

.logo-title {
  font-size: 22px;
  font-weight: bold;
  color: var(--primary-color);
  line-height: 1.1;
  letter-spacing: 0.3px;
  text-align: left;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

/* 响应式设计 */
@media (max-width: 1600px) {
  .logo-image {
    width: 32px;
    height: 32px;
  }
  .logo-title {
    font-size: 20px;
  }
}

@media (max-width: 1400px) {
  .logo-image {
    width: 28px;
    height: 28px;
  }
  .logo-title {
    font-size: 18px;
  }
}

@media (max-width: 1200px) {
  .logo-image {
    width: 24px;
    height: 24px;
  }
  .logo-title {
    font-size: 16px;
  }
}
</style>
