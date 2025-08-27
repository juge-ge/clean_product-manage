<template>
  <div class="capacity-page">
    <n-card title="能力建设" class="capacity-card">
      <div class="capacity-content">
        <n-empty description="能力建设功能开发中..." />
      </div>
    </n-card>
  </div>
</template>

<script setup>
import { NCard, NEmpty } from 'naive-ui'
</script>

<style scoped>
.capacity-page {
  padding: 20px;
}

.capacity-card {
  min-height: 400px;
}

.capacity-content {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}
</style>

