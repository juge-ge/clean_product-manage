<template>
  <n-card class="meeting-card" hoverable @click="handleClick">
    <template #header>
      <div class="card-header">
        <span class="header-title">{{ meeting.title }}</span>
        <n-tag :type="getStatusTagType(meeting.status)" size="small">{{ getStatusLabel(meeting.status) }}</n-tag>
      </div>
    </template>
    <div class="card-content">
      <div class="meeting-info">
        <div class="info-item">
          <n-icon size="16" color="#666">
            <i class="mdi mdi-calendar" />
          </n-icon>
          <span class="info-text">{{ formatDateRange(meeting.startDate, meeting.endDate) }}</span>
        </div>
        <div class="info-item">
          <n-icon size="16" color="#666">
            <i class="mdi mdi-map-marker" />
          </n-icon>
          <span class="info-text">{{ meeting.location }}</span>
        </div>
        <div class="info-item">
          <n-icon size="16" color="#666">
            <i class="mdi mdi-account-group" />
          </n-icon>
          <span class="info-text">{{ meeting.organizer }}</span>
        </div>
        <div class="info-item">
          <n-icon size="16" color="#666">
            <i class="mdi mdi-account-multiple" />
          </n-icon>
          <span class="info-text">{{ meeting.participants }} 人参与</span>
        </div>
      </div>
      <p class="summary">{{ meeting.summary }}</p>
      <div class="meeting-type">
        <n-tag :type="getTypeTagType(meeting.type)" size="small">{{ getTypeLabel(meeting.type) }}</n-tag>
      </div>
    </div>
    <template #footer>
      <div class="card-footer">
        <n-button 
          type="primary" 
          size="small" 
          @click.stop="handleViewDetail"
        >
          查看详情
        </n-button>
        <n-button 
          type="info" 
          size="small" 
          @click.stop="handleViewAgenda"
          v-if="meeting.agenda && meeting.agenda.length"
        >
          查看议程
        </n-button>
        <n-button 
          type="success" 
          size="small" 
          @click.stop="handleDownload"
          v-if="meeting.attachments && meeting.attachments.length"
        >
          下载资料
        </n-button>
      </div>
    </template>
  </n-card>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  meeting: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['click', 'view-detail', 'view-agenda', 'download'])

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

const formatDateRange = (startDate, endDate) => {
  if (startDate === endDate) {
    return startDate
  }
  return `${startDate} - ${endDate}`
}

const handleClick = () => {
  emit('click', props.meeting)
}

const handleViewDetail = () => {
  emit('view-detail', props.meeting)
}

const handleViewAgenda = () => {
  emit('view-agenda', props.meeting)
}

const handleDownload = () => {
  emit('download', props.meeting)
}
</script>

<style scoped>
.meeting-card {
  height: 100%;
  transition: all 0.3s ease;
  cursor: pointer;
}

.meeting-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 8px;
  border-bottom: 2px solid var(--primary-color);
  margin-bottom: 12px;
}

.header-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  flex: 1;
  margin-right: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-content {
  display: flex;
  flex-direction: column;
  height: calc(100% - 120px);
}

.meeting-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 12px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #666;
}

.info-text {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.summary {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
  margin: 0 0 12px 0;
  flex: 1;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.meeting-type {
  margin-top: auto;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  gap: 8px;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
}

:deep(.n-card-header) {
  padding: 12px 16px 8px;
}

:deep(.n-card__content) {
  padding: 0 16px 12px;
}

:deep(.n-card__footer) {
  padding: 12px 16px 16px;
}
</style>
