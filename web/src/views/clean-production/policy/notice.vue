<template>
  <div class="notice-page">
    <n-card title="通知公告" class="notice-card">
      <div class="notice-content">
        <n-empty description="通知公告功能开发中..." />
      </div>
    </n-card>
  </div>
</template>

<script setup>
import { NCard, NEmpty } from 'naive-ui'
</script>

<style scoped>
.notice-page {
  padding: 20px;
}

.notice-card {
  min-height: 400px;
}

.notice-content {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}
</style>

