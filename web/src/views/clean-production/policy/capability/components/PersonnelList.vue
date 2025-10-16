<template>
  <div class="personnel-list">
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
          <div class="avatar-section">
            <n-avatar 
              :src="item.avatar" 
              :size="50"
              round
              fallback-src="/default-avatar.png"
            >
              {{ item.name.charAt(0) }}
            </n-avatar>
            <div class="status-indicator" :class="{ 'available': item.isAvailable, 'unavailable': !item.isAvailable }">
              <n-icon size="10">
                <i class="mdi mdi-circle" />
              </n-icon>
            </div>
          </div>
          <div class="info-section">
            <div class="title-section">
              <h3 class="name">{{ item.name }}</h3>
              <n-tag :type="getTypeTagType(item.type)" size="small" class="type-tag">
                {{ getTypeLabel(item.type) }}
              </n-tag>
            </div>
            <div class="details-section">
              <p class="title">{{ item.title }}</p>
              <p class="organization">{{ item.organization }}</p>
              <p class="department">{{ item.department }}</p>
            </div>
            <div class="specialties-section">
              <n-tag 
                v-for="specialty in item.specialties.slice(0, 4)" 
                :key="specialty"
                size="small"
                type="info"
                class="specialty-tag"
              >
                {{ specialty }}
              </n-tag>
              <span v-if="item.specialties.length > 4" class="more-specialties">
                +{{ item.specialties.length - 4 }}
              </span>
            </div>
            <div class="contact-section">
              <div class="contact-item" v-if="item.phone">
                <n-icon size="12" color="#999">
                  <i class="mdi mdi-phone" />
                </n-icon>
                <span class="contact-text">{{ item.phone }}</span>
              </div>
              <div class="contact-item" v-if="item.email">
                <n-icon size="12" color="#999">
                  <i class="mdi mdi-email" />
                </n-icon>
                <span class="contact-text">{{ item.email }}</span>
              </div>
            </div>
          </div>
          <div class="action-section">
            <n-button 
              type="primary" 
              size="small" 
              @click.stop="handleContact(item)"
              :disabled="!item.isAvailable"
            >
              {{ item.isAvailable ? '联系' : '暂不可联系' }}
            </n-button>
            <n-button 
              type="info" 
              size="small" 
              @click.stop="handleViewDetail(item)"
            >
              详情
            </n-button>
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

const emit = defineEmits(['item-click', 'contact', 'view-detail', 'page-change', 'page-size-change'])

const currentPage = ref(1)

const getTypeTagType = (type) => {
  const typeMap = {
    consultant: 'success',
    manager: 'warning'
  }
  return typeMap[type] || 'default'
}

const getTypeLabel = (type) => {
  const labelMap = {
    consultant: '咨询人员',
    manager: '管理人员'
  }
  return labelMap[type] || '未知'
}

const handleItemClick = (item) => {
  emit('item-click', item)
}

const handleContact = (item) => {
  if (item.isAvailable) {
    emit('contact', item)
  }
}

const handleViewDetail = (item) => {
  emit('view-detail', item)
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
.personnel-list {
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
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 16px 0;
}

.avatar-section {
  position: relative;
  flex-shrink: 0;
}

.status-indicator {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid white;
}

.status-indicator.available {
  color: #18a058;
}

.status-indicator.unavailable {
  color: #d03050;
}

.info-section {
  flex: 1;
  min-width: 0;
}

.title-section {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.name {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0;
  line-height: 1.2;
}

.type-tag {
  flex-shrink: 0;
}

.details-section {
  margin-bottom: 8px;
}

.title {
  font-size: 14px;
  color: #666;
  margin: 0 0 2px 0;
  font-weight: 500;
}

.organization {
  font-size: 13px;
  color: #999;
  margin: 0 0 2px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.department {
  font-size: 12px;
  color: #999;
  margin: 0 0 8px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.specialties-section {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-bottom: 8px;
  align-items: center;
}

.specialty-tag {
  font-size: 11px;
  padding: 2px 6px;
}

.more-specialties {
  font-size: 11px;
  color: #999;
  margin-left: 4px;
}

.contact-section {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #999;
}

.contact-text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.action-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex-shrink: 0;
  min-width: 80px;
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
