<template>
  <div class="notice-detail">
    <!-- 面包屑导航 -->
    <n-breadcrumb class="breadcrumb">
      <n-breadcrumb-item>
        <router-link to="/clean-production">清洁生产管理</router-link>
      </n-breadcrumb-item>
      <n-breadcrumb-item>
        <router-link to="/clean-production/policy">清洁生产政策与管理</router-link>
      </n-breadcrumb-item>
      <n-breadcrumb-item>
        <router-link to="/clean-production/policy/notice">通知公告</router-link>
      </n-breadcrumb-item>
      <n-breadcrumb-item>公告详情</n-breadcrumb-item>
    </n-breadcrumb>

    <n-card class="mt-4">
      <template #header>
        <div class="notice-header">
          <h1>{{ notice?.title }}</h1>
          <div class="notice-meta">
            <n-space justify="center">
              <span>发布时间：{{ notice?.publishDate }}</span>
              <n-divider vertical />
              <span>来源：{{ notice?.source }}</span>
              <template v-if="notice?.province">
                <n-divider vertical />
                <span>地区：{{ notice?.province }}</span>
              </template>
            </n-space>
          </div>
        </div>
      </template>
      
      <div class="notice-content">
        {{ notice?.content }}
      </div>
      
      <template #footer>
        <div class="notice-attachments" v-if="notice?.attachments?.length">
          <n-divider>附件下载</n-divider>
          <n-list>
            <n-list-item v-for="file in notice?.attachments" :key="file.name">
              <n-button text>
                <template #icon>
                  <n-icon><document-icon /></n-icon>
                </template>
                {{ file.name }}
              </n-button>
            </n-list-item>
          </n-list>
        </div>
      </template>
    </n-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { DocumentIcon } from '@vicons/carbon'

const route = useRoute()
const router = useRouter()

// 模拟数据获取
const notice = ref(null)

onMounted(() => {
  // 模拟API调用
  const noticeId = parseInt(route.params.id)
  
  // 模拟的通知数据
  const mockNotice = {
    1: {
      id: 1,
      title: '关于开展2025年度清洁生产审核评估工作的通知',
      content: `为深入贯彻习近平生态文明思想，全面落实党的二十大精神，推动清洁生产审核评估工作高质量发展，现就开展2025年度清洁生产审核评估工作通知如下：

一、工作目标
1. 全面提升企业清洁生产水平
2. 推动重点行业绿色转型
3. 建立健全清洁生产长效机制

二、重点任务
1. 开展重点企业清洁生产审核
2. 推进清洁生产技术创新
3. 强化清洁生产管理体系建设

三、工作要求
1. 加强组织领导
2. 严格过程管理
3. 确保工作质量`,
      publishDate: '2025-08-27',
      type: 'national',
      source: '生态环境部',
      attachments: [
        { name: '清洁生产审核评估工作方案.pdf' },
        { name: '清洁生产审核评估指标体系.xlsx' }
      ]
    }
  }
  
  notice.value = mockNotice[noticeId]
  
  // 如果没有找到对应的通知，跳转到404页面
  if (!notice.value) {
    router.push('/404')
  }
})
</script>

<style scoped>
.notice-detail {
  padding: 16px;
}

.breadcrumb {
  background-color: #fff;
  padding: 16px;
  border-radius: 3px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.notice-header {
  text-align: center;
  margin-bottom: 24px;
}

.notice-header h1 {
  font-size: 24px;
  margin-bottom: 16px;
  font-weight: 500;
  color: #333;
}

.notice-meta {
  color: #666;
  font-size: 14px;
}

.notice-content {
  padding: 24px 0;
  line-height: 1.8;
  font-size: 14px;
  white-space: pre-line;
  color: #333;
}

.notice-attachments {
  margin-top: 24px;
}

.mt-4 {
  margin-top: 16px;
}

:deep(.n-breadcrumb-item a) {
  color: #666;
  text-decoration: none;
}

:deep(.n-breadcrumb-item a:hover) {
  color: #2080f0;
}

:deep(.n-divider) {
  margin: 0 12px;
}
</style>
