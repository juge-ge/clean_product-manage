<template>
  <n-modal
    :show="show"
    @update:show="$emit('update:show', $event)"
    class="meeting-detail-modal"
    preset="card"
    style="max-width: 1000px"
    :title="meeting?.title"
    size="huge"
  >
    <div class="meeting-meta">
      <n-space justify="center">
        <n-tag :type="getTypeTagType(meeting?.type)" size="medium">
          {{ getTypeLabel(meeting?.type) }}
        </n-tag>
        <n-tag :type="getStatusTagType(meeting?.status)" size="medium">
          {{ getStatusLabel(meeting?.status) }}
        </n-tag>
        <span>时间：{{ formatDateRange(meeting?.startDate, meeting?.endDate) }}</span>
        <n-divider vertical />
        <span>地点：{{ meeting?.location }}</span>
        <n-divider vertical />
        <span>主办方：{{ meeting?.organizer }}</span>
        <n-divider vertical />
        <span>参与人数：{{ meeting?.participants }} 人</span>
      </n-space>
    </div>

    <n-divider />

    <div class="meeting-content">
      <div class="content-text">{{ meeting?.content }}</div>
    </div>

    <!-- 会议议程 -->
    <template v-if="meeting?.agenda && meeting.agenda.length">
      <n-divider>会议议程</n-divider>
      <n-timeline>
        <n-timeline-item 
          v-for="(item, index) in meeting.agenda" 
          :key="index"
          :title="item.topic"
          :content="item.speaker"
          :time="item.time"
        />
      </n-timeline>
    </template>

    <!-- 演讲者 -->
    <template v-if="meeting?.speakers && meeting.speakers.length">
      <n-divider>演讲者</n-divider>
      <div class="speakers-section">
        <n-tag 
          v-for="speaker in meeting.speakers" 
          :key="speaker"
          size="medium"
          type="info"
          class="speaker-tag"
        >
          {{ speaker }}
        </n-tag>
      </div>
    </template>

    <!-- 附件下载 -->
    <template v-if="meeting?.attachments && meeting.attachments.length">
      <n-divider>附件下载</n-divider>
      <n-list>
        <n-list-item v-for="file in meeting.attachments" :key="file.name">
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
        <n-button type="primary" @click="handleDownloadAll" v-if="meeting?.attachments && meeting.attachments.length">
          下载全部附件
        </n-button>
        <n-button type="info" @click="handleShare">分享</n-button>
      </n-space>
    </template>
  </n-modal>
</template>

<script setup>
import { ref, watch } from 'vue'
import { mockMeetingApi } from '../data/mockData.js'

const props = defineProps({
  show: {
    type: Boolean,
    required: true
  },
  meetingId: {
    type: [String, Number],
    default: null
  }
})

const emit = defineEmits(['update:show'])

const meeting = ref(null)
const loading = ref(false)

const getTypeTagType = (type) => {
  const typeMap = {
    conference: 'error',
    training: 'warning',
    meeting: 'info'
  }
  return typeMap[type] || 'default'
}

const getTypeLabel = (type) => {
  const labelMap = {
    conference: '会议',
    training: '培训',
    meeting: '交流会'
  }
  return labelMap[type] || '未知'
}

const getStatusTagType = (status) => {
  const typeMap = {
    upcoming: 'info',
    ongoing: 'warning',
    completed: 'success'
  }
  return typeMap[status] || 'default'
}

const getStatusLabel = (status) => {
  const labelMap = {
    upcoming: '即将开始',
    ongoing: '进行中',
    completed: '已结束'
  }
  return labelMap[status] || '未知'
}

const formatDateRange = (startDate, endDate) => {
  if (!startDate) return ''
  if (startDate === endDate) {
    return startDate
  }
  return `${startDate} - ${endDate}`
}

// 获取会议详情
const getMeetingDetail = async (id) => {
  if (!id) return
  
  loading.value = true
  try {
    const response = await mockMeetingApi.getMeetingDetail(id)
    meeting.value = response.data
  } catch (error) {
    console.error('获取会议详情失败:', error)
  } finally {
    loading.value = false
  }
}

// 监听ID变化
watch(
  () => props.meetingId,
  (newId) => {
    if (newId) {
      getMeetingDetail(newId)
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
  if (meeting.value?.attachments) {
    meeting.value.attachments.forEach(file => {
      handleDownload(file)
    })
  }
}

const handleShare = () => {
  // 实现分享功能
  console.log('分享会议:', meeting.value?.title)
  // 这里可以集成分享到微信、微博等功能
}
</script>

<style scoped>
.meeting-meta {
  margin-bottom: 16px;
  color: #666;
  font-size: 14px;
}

.meeting-content {
  margin: 24px 0;
}

.content-text {
  line-height: 1.8;
  font-size: 15px;
  white-space: pre-line;
  color: #333;
}

.speakers-section {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 16px 0;
}

.speaker-tag {
  font-size: 14px;
  padding: 6px 12px;
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

:deep(.n-timeline-item-content) {
  font-size: 14px;
  color: #666;
}

:deep(.n-timeline-item-title) {
  font-size: 15px;
  font-weight: 500;
  color: #333;
}
</style>
