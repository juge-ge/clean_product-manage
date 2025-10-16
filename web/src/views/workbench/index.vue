<template>
  <div class="workbench-container">
    <!-- 智能欢迎区域 -->
    <WelcomeSection />
    
    <!-- 最新动态和行业审核概览 -->
    <NewsIndustrySection />
    
    <!-- AI智能助手（可选） -->
    <ChatWidget />
  </div>
</template>

<script setup>
import WelcomeSection from './components/WelcomeSection.vue'
import NewsIndustrySection from './components/NewsIndustrySection.vue'
import ChatWidget from './components/AIAssistant/ChatWidget.vue'
</script>

<style lang="scss" scoped>
.workbench-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 0;
  max-width: 1400px;
  margin: 0 auto;
}

// 响应式设计
@media (max-width: 1200px) {
  .workbench-container {
    padding: 0 16px;
  }
}

@media (max-width: 768px) {
  .workbench-container {
    padding: 0 12px;
    gap: 12px;
  }
}
</style>