<template>
  <n-modal
    :show="show"
    @update:show="$emit('update:show', $event)"
    class="regulation-detail-modal"
    preset="card"
    style="max-width: 1200px"
    :title="regulation?.title"
    size="huge"
  >
    <div class="regulation-meta">
      <n-space justify="center">
        <n-tag :type="getLevelTagType(regulation?.level)" size="medium">
          {{ getLevelLabel(regulation?.level) }}
        </n-tag>
        <span>发布时间：{{ regulation?.publishDate }}</span>
        <template v-if="regulation?.effectiveDate">
          <n-divider vertical />
          <span>生效时间：{{ regulation?.effectiveDate }}</span>
        </template>
        <n-divider vertical />
        <span>发布机构：{{ regulation?.source }}</span>
        <template v-if="regulation?.province">
          <n-divider vertical />
          <span>地区：{{ regulation?.province }}</span>
        </template>
      </n-space>
    </div>

    <div class="regulation-stats">
      <n-space justify="center">
        <div class="stat-item">
          <n-icon size="16" color="#999">
            <i class="mdi mdi-eye" />
          </n-icon>
          <span>{{ regulation?.viewCount || 0 }} 次浏览</span>
        </div>
        <n-divider vertical />
        <div class="stat-item">
          <n-icon size="16" color="#999">
            <i class="mdi mdi-download" />
          </n-icon>
          <span>{{ regulation?.downloadCount || 0 }} 次下载</span>
        </div>
        <template v-if="regulation?.tags && regulation.tags.length">
          <n-divider vertical />
          <div class="tags-display">
            <span class="tags-label">标签：</span>
            <n-tag 
              v-for="tag in regulation.tags" 
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

    <div class="regulation-content">
      <div class="content-text">{{ regulation?.content }}</div>
    </div>

    <template v-if="regulation?.attachments && regulation.attachments.length">
      <n-divider>附件下载</n-divider>
      <n-list>
        <n-list-item v-for="file in regulation.attachments" :key="file.name">
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
        <n-button type="primary" @click="handleDownloadAll">下载全部附件</n-button>
        <n-button type="info" @click="handleShare">分享</n-button>
      </n-space>
    </template>
  </n-modal>
</template>

<script setup>
import { ref, watch } from 'vue'
import { mockRegulationApi } from '../data/mockData.js'

const props = defineProps({
  show: {
    type: Boolean,
    required: true
  },
  regulationId: {
    type: [String, Number],
    default: null
  }
})

const emit = defineEmits(['update:show'])

const regulation = ref(null)
const loading = ref(false)

const getLevelTagType = (level) => {
  const typeMap = {
    national: 'error',
    provincial: 'warning'
  }
  return typeMap[level] || 'default'
}

const getLevelLabel = (level) => {
  const labelMap = {
    national: '国家级',
    provincial: '省级'
  }
  return labelMap[level] || '未知'
}

// 获取法规详情
const getRegulationDetail = async (id) => {
  if (!id) return
  
  loading.value = true
  try {
    const response = await mockRegulationApi.getRegulationDetail(id)
    regulation.value = response.data
  } catch (error) {
    console.error('获取法规详情失败:', error)
  } finally {
    loading.value = false
  }
}

// 监听ID变化
watch(
  () => props.regulationId,
  (newId) => {
    if (newId) {
      getRegulationDetail(newId)
    }
  },
  { immediate: true }
)

const handleClose = () => {
  emit('update:show', false)
}

const handleDownload = (file) => {
  // 实现文件下载功能
  console.log('下载文件:', file.name)
  if (file.url) {
    window.open(file.url, '_blank')
  }
}

const handleDownloadAll = () => {
  // 下载全部附件
  if (regulation.value?.attachments) {
    regulation.value.attachments.forEach(file => {
      handleDownload(file)
    })
  }
}

const handleShare = () => {
  // 实现分享功能
  console.log('分享法规:', regulation.value?.title)
  // 这里可以集成分享到微信、微博等功能
}
</script>

<style scoped>
.regulation-meta {
  margin-bottom: 16px;
  color: #666;
  font-size: 14px;
}

.regulation-stats {
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

.regulation-content {
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
