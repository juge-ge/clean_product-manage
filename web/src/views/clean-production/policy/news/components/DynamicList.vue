<template>
  <div class="dynamic-list">
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
            <n-tag :type="getTagType(item.type)" size="small" class="type-tag">
              {{ getTypeLabel(item.type) }}
            </n-tag>
            <template v-if="item.isTop">
              <n-tag type="error" size="small" class="top-tag">置顶</n-tag>
            </template>
          </div>
          <div class="summary-section">
            <p class="item-summary">{{ item.summary }}</p>
          </div>
          <div class="meta-section">
            <div class="meta-left">
              <span class="source">{{ item.source }}</span>
              <span class="date">{{ item.publishDate }}</span>
            </div>
            <div class="meta-right">
              <div class="stats">
                <n-icon size="14" color="#999">
                  <i class="mdi mdi-eye" />
                </n-icon>
                <span class="view-count">{{ item.viewCount }}</span>
              </div>
            </div>
          </div>
          <div v-if="item.tags && item.tags.length" class="tags-section">
            <n-tag 
              v-for="tag in item.tags.slice(0, 4)" 
              :key="tag"
              size="small"
              type="info"
              class="tag-item"
            >
              {{ tag }}
            </n-tag>
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
import { ref, computed } from 'vue'

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
.dynamic-list {
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
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  flex-wrap: wrap;
}

.item-title {
  font-size: 16px;
  font-weight: 500;
  color: #333;
  text-decoration: none;
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.item-title:hover {
  color: var(--primary-color);
}

.type-tag {
  flex-shrink: 0;
}

.top-tag {
  flex-shrink: 0;
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
  margin-bottom: 8px;
}

.meta-left {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 12px;
  color: #999;
}

.source {
  font-weight: 500;
  color: #666;
}

.date {
  color: #999;
}

.meta-right {
  display: flex;
  align-items: center;
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

.tags-section {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.tag-item {
  font-size: 11px;
  padding: 2px 6px;
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
