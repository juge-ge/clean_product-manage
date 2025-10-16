<template>
  <div class="meeting-list">
    <div class="list-header" v-if="showHeader">
      <div class="header-left">
        <slot name="header-left"></slot>
      </div>
      <div class="header-right">
        <slot name="header-right"></slot>
      </div>
    </div>
    
    <n-list hoverable clickable>
      <n-list-item 
        v-for="(item, index) in data" 
        :key="item.id || index"
        @click="handleItemClick(item)"
        class="list-item"
      >
        <div class="list-item-content">
          <div class="title-section">
            <a href="javascript:;" class="item-title" @click.stop="handleItemClick(item)">
              {{ item.title }}
            </a>
            <div class="title-tags">
              <n-tag :type="getTypeTagType(item.type)" size="small" class="type-tag">
                {{ getTypeLabel(item.type) }}
              </n-tag>
              <n-tag :type="getStatusTagType(item.status)" size="small" class="status-tag">
                {{ getStatusLabel(item.status) }}
              </n-tag>
            </div>
          </div>
          <div class="summary-section">
            <p class="item-summary">{{ item.summary }}</p>
          </div>
          <div class="meta-section">
            <div class="meta-left">
              <div class="meta-item">
                <n-icon size="14" color="#999">
                  <i class="mdi mdi-calendar" />
                </n-icon>
                <span class="meta-text">{{ formatDateRange(item.startDate, item.endDate) }}</span>
              </div>
              <div class="meta-item">
                <n-icon size="14" color="#999">
                  <i class="mdi mdi-map-marker" />
                </n-icon>
                <span class="meta-text">{{ item.location }}</span>
              </div>
              <div class="meta-item">
                <n-icon size="14" color="#999">
                  <i class="mdi mdi-account-group" />
                </n-icon>
                <span class="meta-text">{{ item.organizer }}</span>
              </div>
              <div class="meta-item">
                <n-icon size="14" color="#999">
                  <i class="mdi mdi-account-multiple" />
                </n-icon>
                <span class="meta-text">{{ item.participants }} 人参与</span>
              </div>
            </div>
          </div>
        </div>
      </n-list-item>
    </n-list>
    
    <div class="list-footer" v-if="showPagination">
      <n-pagination
        v-model:page="currentPage"
        :page-size="pageSize"
        :item-count="total"
        show-quick-jumper
        show-size-picker
        :page-sizes="[10, 20, 30, 50]"
        @update:page="handlePageChange"
        @update:page-size="handlePageSizeChange"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  data: {
    type: Array,
    default: () => []
  },
  showHeader: {
    type: Boolean,
    default: true
  },
  showPagination: {
    type: Boolean,
    default: true
  },
  total: {
    type: Number,
    default: 0
  },
  pageSize: {
    type: Number,
    default: 10
  }
})

const emit = defineEmits(['item-click', 'page-change', 'page-size-change'])

const currentPage = ref(1)

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
  if (startDate === endDate) {
    return startDate
  }
  return `${startDate} - ${endDate}`
}

const handleItemClick = (item) => {
  emit('item-click', item)
}

const handlePageChange = (page) => {
  currentPage.value = page
  emit('page-change', page)
}

const handlePageSizeChange = (pageSize) => {
  emit('page-size-change', pageSize)
}
</script>

<style scoped>
.meeting-list {
  width: 100%;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding: 0 4px;
}

.list-item {
  border-bottom: 1px dashed #e5e5e5;
  transition: all 0.3s ease;
}

.list-item:hover {
  background-color: #f8f9fa;
}

.list-item:last-child {
  border-bottom: none;
}

.list-item-content {
  width: 100%;
  padding: 12px 0;
}

.title-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
  gap: 12px;
}

.item-title {
  font-size: 16px;
  font-weight: 500;
  color: #333;
  text-decoration: none;
  flex: 1;
  line-height: 1.4;
}

.item-title:hover {
  color: var(--primary-color);
}

.title-tags {
  display: flex;
  gap: 6px;
  flex-shrink: 0;
}

.type-tag,
.status-tag {
  font-size: 11px;
  padding: 2px 6px;
}

.summary-section {
  margin-bottom: 8px;
}

.item-summary {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.meta-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.meta-left {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  align-items: center;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #999;
}

.meta-text {
  font-size: 12px;
}

.list-footer {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #e5e5e5;
  display: flex;
  justify-content: center;
}

:deep(.n-list-item) {
  padding: 0 16px;
}

:deep(.n-list-item:hover) {
  background-color: #f8f9fa;
}
</style>
