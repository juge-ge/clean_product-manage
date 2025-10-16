<template>
  <n-modal
    :show="show"
    @update:show="$emit('update:show', $event)"
    class="dynamic-detail-modal"
    preset="card"
    style="max-width: 1000px"
    :title="dynamic?.title"
    size="huge"
  >
    <div class="dynamic-meta">
      <n-space justify="center">
        <n-tag :type="getTagType(dynamic?.type)" size="medium">
          {{ getTypeLabel(dynamic?.type) }}
        </n-tag>
        <span>发布时间：{{ dynamic?.publishDate }}</span>
        <n-divider vertical />
        <span>来源：{{ dynamic?.source }}</span>
        <template v-if="dynamic?.province">
          <n-divider vertical />
          <span>地区：{{ dynamic?.province }}</span>
        </template>
        <template v-if="dynamic?.country">
          <n-divider vertical />
          <span>国家：{{ dynamic?.country }}</span>
        </template>
      </n-space>
    </div>

    <div class="dynamic-stats">
      <n-space justify="center">
        <div class="stat-item">
          <n-icon size="16" color="#999">
            <i class="mdi mdi-eye" />
          </n-icon>
          <span>{{ dynamic?.viewCount || 0 }} 次浏览</span>
        </div>
        <template v-if="dynamic?.tags && dynamic.tags.length">
          <n-divider vertical />
          <div class="tags-display">
            <span class="tags-label">标签：</span>
            <n-tag 
              v-for="tag in dynamic.tags" 
              :key="tag"
              size="small"
              type="info"
              class="tag-item"
            >
              {{ tag }}
            </n-tag>
          </div>
        </template>
      </n-space>
    </div>

    <n-divider />

    <div class="dynamic-content">
      <div class="content-text">{{ dynamic?.content }}</div>
    </div>

    <template v-if="dynamic?.attachments && dynamic.attachments.length">
      <n-divider>附件下载</n-divider>
      <n-list>
        <n-list-item v-for="file in dynamic.attachments" :key="file.name">
          <n-button text @click="handleDownload(file)">
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
        <n-button type="primary" @click="handleShare">分享</n-button>
      </n-space>
    </template>
  </n-modal>
</template>

<script setup>
import { ref, watch } from 'vue'
import { mockDynamicApi } from '../data/mockData.js'

const props = defineProps({
  show: {
    type: Boolean,
    required: true
  },
  dynamicId: {
    type: [String, Number],
    default: null
  }
})

const emit = defineEmits(['update:show'])

const dynamic = ref(null)
const loading = ref(false)

const getTagType = (type) => {
  const typeMap = {
    domestic: 'success',
    provincial: 'warning', 
    international: 'info'
  }
  return typeMap[type] || 'default'
}

const getTypeLabel = (type) => {
  const labelMap = {
    domestic: '国内动态',
    provincial: '省内动态',
    international: '国外动态'
  }
  return labelMap[type] || '未知'
}

// 获取动态详情
const getDynamicDetail = async (id) => {
  if (!id) return
  
  loading.value = true
  try {
    const response = await mockDynamicApi.getDynamicDetail(id)
    dynamic.value = response.data
  } catch (error) {
    console.error('获取动态详情失败:', error)
  } finally {
    loading.value = false
  }
}

// 监听ID变化
watch(
  () => props.dynamicId,
  (newId) => {
    if (newId) {
      getDynamicDetail(newId)
    }
  },
  { immediate: true }
)

const handleClose = () => {
  emit('update:show', false)
}

const handleShare = () => {
  // 实现分享功能
  console.log('分享动态:', dynamic.value?.title)
  // 这里可以集成分享到微信、微博等功能
}

const handleDownload = (file) => {
  // 实现文件下载功能
  console.log('下载文件:', file.name)
  // 这里可以实现文件下载逻辑
  if (file.url) {
    window.open(file.url, '_blank')
  }
}
</script>

<style scoped>
.dynamic-meta {
  margin-bottom: 16px;
  color: #666;
  font-size: 14px;
}

.dynamic-stats {
  margin-bottom: 16px;
  color: #666;
  font-size: 14px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.tags-display {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.tags-label {
  font-size: 14px;
  color: #666;
  white-space: nowrap;
}

.tag-item {
  font-size: 12px;
  padding: 2px 6px;
}

.dynamic-content {
  margin: 24px 0;
}

.content-text {
  line-height: 1.8;
  font-size: 15px;
  white-space: pre-line;
  color: #333;
}

:deep(.n-card-header) {
  text-align: center;
  font-size: 20px;
  font-weight: 500;
  padding: 20px 24px 16px;
}

:deep(.n-card__content) {
  padding: 0 24px 24px;
}

:deep(.n-card__footer) {
  padding: 16px 24px 24px;
}
</style>
