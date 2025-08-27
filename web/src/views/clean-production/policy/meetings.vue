<template>
  <div class="meetings-page">
    <n-card title="会议与宣传" class="meetings-card">
      <div class="meetings-content">
        <n-empty description="会议与宣传功能开发中..." />
      </div>
    </n-card>
  </div>
</template>

<script setup>
import { NCard, NEmpty } from 'naive-ui'
</script>

<style scoped>
.meetings-page {
  padding: 20px;
}

.meetings-card {
  min-height: 400px;
}

.meetings-content {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}
</style>

