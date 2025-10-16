<template>
  <n-card class="dynamic-card" hoverable @click="handleClick">
    <template #header>
      <div class="card-header">
        <span class="header-title">{{ title }}</span>
        <n-tag :type="getTagType(type)" size="small">{{ getTypeLabel(type) }}</n-tag>
      </div>
    </template>
    <div class="card-content">
      <p class="summary">{{ summary }}</p>
      <div class="card-footer">
        <div class="meta-info">
          <span class="source">{{ source }}</span>
          <span class="date">{{ publishDate }}</span>
        </div>
        <div class="stats">
          <n-icon size="14" color="#999">
            <i class="mdi mdi-eye" />
          </n-icon>
          <span class="view-count">{{ viewCount }}</span>
        </div>
      </div>
      <div v-if="tags && tags.length" class="tags">
        <n-tag 
          v-for="tag in tags.slice(0, 3)" 
          :key="tag"
          size="small"
          type="info"
          class="tag-item"
        >
          {{ tag }}
        </n-tag>
      </div>
    </div>
  </n-card>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  id: {
    type: [Number, String],
    required: true
  },
  title: {
    type: String,
    required: true
  },
  summary: {
    type: String,
    required: true
  },
  publishDate: {
    type: String,
    required: true
  },
  source: {
    type: String,
    required: true
  },
  type: {
    type: String,
    required: true,
    validator: (value) => ['domestic', 'provincial', 'international'].includes(value)
  },
  viewCount: {
    type: Number,
    default: 0
  },
  tags: {
    type: Array,
    default: () => []
  },
  isTop: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['click'])

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
    domestic: '国内',
    provincial: '省内',
    international: '国外'
  }
  return labelMap[type] || '未知'
}

const handleClick = () => {
  emit('click', props.id)
}
</script>

<style scoped>
.dynamic-card {
  height: 100%;
  transition: all 0.3s ease;
  cursor: pointer;
}

.dynamic-card:hover {
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
  height: calc(100% - 60px);
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

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.meta-info {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #999;
}

.source {
  font-weight: 500;
}

.date {
  color: #999;
}

.stats {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #999;
}

.view-count {
  font-size: 12px;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-top: auto;
}

.tag-item {
  font-size: 11px;
  padding: 2px 6px;
}

:deep(.n-card-header) {
  padding: 12px 16px 8px;
}

:deep(.n-card__content) {
  padding: 0 16px 16px;
}
</style>
