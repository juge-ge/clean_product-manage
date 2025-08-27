<template>
  <div class="regulations-page">
    <n-card title="清洁生产法规政策" class="regulations-card">
      <div class="regulations-content">
        <n-empty description="清洁生产法规政策功能开发中..." />
      </div>
    </n-card>
  </div>
</template>

<script setup>
import { NCard, NEmpty } from 'naive-ui'
</script>

<style scoped>
.regulations-page {
  padding: 20px;
}

.regulations-card {
  min-height: 400px;
}

.regulations-content {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}
</style>

