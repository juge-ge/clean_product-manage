<template>
  <n-modal
    :show="show"
    @update:show="$emit('update:show', $event)"
    class="notice-detail-modal"
    preset="card"
    style="max-width: 900px"
    :title="notice?.title"
    size="huge"
  >
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

    <div class="notice-content">
      {{ notice?.content }}
    </div>

    <template v-if="notice?.attachments?.length">
      <n-divider>附件下载</n-divider>
      <n-list>
        <n-list-item v-for="file in notice?.attachments" :key="file.name">
          <n-button text>
            <template #icon>
              <n-icon><i class="mdi mdi-file-document-outline" /></n-icon>
            </template>
            {{ file.name }}
          </n-button>
        </n-list-item>
      </n-list>
    </template>

    <template #footer>
      <n-space justify="center">
        <n-button @click="handleClose">关闭</n-button>
      </n-space>
    </template>
  </n-modal>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  show: {
    type: Boolean,
    required: true
  },
  noticeId: {
    type: [String, Number],
    default: null
  }
})

const emit = defineEmits(['update:show'])

const notice = ref(null)

// 模拟获取通知详情
const getNoticeDetail = (id) => {
  // 这里模拟一些数据
  notice.value = {
    id,
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
    source: '生态环境部',
    attachments: [
      { name: '清洁生产审核评估工作方案.pdf' },
      { name: '清洁生产审核评估指标体系.xlsx' }
    ]
  }
}

// 监听ID变化
watch(
  () => props.noticeId,
  (newId) => {
    if (newId) {
      getNoticeDetail(newId)
    }
  },
  { immediate: true }
)

const handleClose = () => {
  emit('update:show', false)
}
</script>

<style scoped>
.notice-meta {
  margin-bottom: 24px;
  color: #666;
}

.notice-content {
  line-height: 1.8;
  font-size: 14px;
  white-space: pre-line;
  margin: 24px 0;
}

:deep(.n-card-header) {
  text-align: center;
  font-size: 20px;
  font-weight: 500;
}
</style>
