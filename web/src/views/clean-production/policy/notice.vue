<template>
  <n-card title="通知公告">
    <n-result
      status="404"
      title="功能开发中"
      description="通知公告功能正在开发中，敬请期待..."
    >
      <template #footer>
        <n-button @click="router.push('/')">返回首页</n-button>
      </template>
    </n-result>
  </n-card>
</template>

<script setup>
import { NCard, NResult, NButton } from 'naive-ui'
import { useRouter } from 'vue-router'

const router = useRouter()
</script>