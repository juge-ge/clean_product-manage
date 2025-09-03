<template>
  <div class="page-container">
    <n-result
      status="404"
      title="功能开发中"
      description="法规政策功能正在开发中，敬请期待..."
    >
      <template #footer>
        <n-button @click="router.push('/')">返回首页</n-button>
      </template>
    </n-result>
  </div>
</template>

<script setup>
import { NResult, NButton } from 'naive-ui'
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<style scoped>
.page-container {
  padding: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}
</style>