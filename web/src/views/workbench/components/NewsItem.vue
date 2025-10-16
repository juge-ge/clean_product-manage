<template>
  <div 
    class="news-item" 
    :class="{ 'is-unread': !news.isRead }"
    @click="$emit('click')"
  >
    <div class="news-indicator">
      <div class="indicator-icon" :class="`type-${news.type}`">
        <TheIcon :icon="typeIcon" :size="16" />
      </div>
    </div>
    
    <div class="news-content">
      <div class="news-header">
        <h4 class="news-title">{{ news.title }}</h4>
        <div class="news-time">{{ formatTime }}</div>
      </div>
      
      <p class="news-description">{{ news.content }}</p>
      
      <div class="news-footer">
        <div class="news-author">
          <TheIcon icon="carbon:user" :size="12" />
          <span>{{ news.author }}</span>
        </div>
        <div class="news-type-tag" :class="`type-${news.type}`">
          {{ typeText }}
        </div>
      </div>
    </div>
    
    <div v-if="!news.isRead" class="unread-dot"></div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import TheIcon from '@/components/icon/TheIcon.vue'

const props = defineProps({
  news: {
    type: Object,
    required: true
  }
})

defineEmits(['click'])

// 类型图标
const typeIcon = computed(() => {
  const iconMap = {
    policy: 'carbon:policy',
    completion: 'carbon:checkmark-filled',
    update: 'carbon:update-now',
    notification: 'carbon:notification',
    warning: 'carbon:warning',
    info: 'carbon:information'
  }
  return iconMap[props.news.type] || 'carbon:information'
})

// 类型文本
const typeText = computed(() => {
  const typeMap = {
    policy: '政策',
    completion: '完成',
    update: '更新',
    notification: '通知',
    warning: '警告',
    info: '信息'
  }
  return typeMap[props.news.type] || '信息'
})

// 格式化时间
const formatTime = computed(() => {
  const newsTime = new Date(props.news.time)
  const now = new Date()
  const diffTime = now.getTime() - newsTime.getTime()
  const diffMinutes = Math.floor(diffTime / (1000 * 60))
  const diffHours = Math.floor(diffTime / (1000 * 60 * 60))
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffMinutes < 1) {
    return '刚刚'
  } else if (diffMinutes < 60) {
    return `${diffMinutes}分钟前`
  } else if (diffHours < 24) {
    return `${diffHours}小时前`
  } else if (diffDays < 7) {
    return `${diffDays}天前`
  } else {
    return newsTime.toLocaleDateString()
  }
})
</script>

<style lang="scss" scoped>
.news-item {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 10px 12px;
  display: flex;
  align-items: flex-start;
  gap: 8px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  
  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    border-color: #cbd5e1;
  }
  
  &.is-unread {
    background: #f0fdf4;
    border-left: 3px solid #22c55e;
    box-shadow: 0 1px 3px rgba(34, 197, 94, 0.1);
  }
  
  .news-indicator {
    flex-shrink: 0;
    margin-top: 1px;
    
    .indicator-icon {
      width: 24px;
      height: 24px;
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      
      &.type-policy {
        background: #dbeafe;
        color: #3b82f6;
      }
      
      &.type-completion {
        background: #dcfce7;
        color: #22c55e;
      }
      
      &.type-update {
        background: #fef3c7;
        color: #f59e0b;
      }
      
      &.type-notification {
        background: #e9d5ff;
        color: #8b5cf6;
      }
      
      &.type-warning {
        background: #fee2e2;
        color: #ef4444;
      }
      
      &.type-info {
        background: #f1f5f9;
        color: #64748b;
      }
      
      &.type-report {
        background: #dbeafe;
        color: #3b82f6;
      }
      
      &.type-training {
        background: #fef3c7;
        color: #f59e0b;
      }
    }
  }
  
  .news-content {
    flex: 1;
    min-width: 0;
    
    .news-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 4px;
      gap: 8px;
      
      .news-title {
        font-size: 13px;
        font-weight: 600;
        color: #262626;
        margin: 0;
        line-height: 1.3;
        flex: 1;
      }
      
      .news-time {
        font-size: 10px;
        color: #8C8C8C;
        flex-shrink: 0;
      }
    }
    
    .news-description {
      font-size: 11px;
      color: #8C8C8C;
      margin: 0 0 6px 0;
      line-height: 1.3;
      display: -webkit-box;
      -webkit-line-clamp: 1;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
    
    .news-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      
      .news-author {
        font-size: 10px;
        color: #8C8C8C;
        display: flex;
        align-items: center;
        gap: 3px;
      }
      
        .news-type-tag {
          font-size: 9px;
          font-weight: 500;
          padding: 1px 6px;
          border-radius: 10px;
          
          &.type-policy {
            background: #dbeafe;
            color: #3b82f6;
          }
          
          &.type-completion {
            background: #dcfce7;
            color: #22c55e;
          }
          
          &.type-update {
            background: #fef3c7;
            color: #f59e0b;
          }
          
          &.type-notification {
            background: #e9d5ff;
            color: #8b5cf6;
          }
          
          &.type-warning {
            background: #fee2e2;
            color: #ef4444;
          }
          
          &.type-info {
            background: #f1f5f9;
            color: #64748b;
          }
          
          &.type-report {
            background: #dbeafe;
            color: #3b82f6;
          }
          
          &.type-training {
            background: #fef3c7;
            color: #f59e0b;
          }
        }
    }
  }
  
  .unread-dot {
    position: absolute;
    top: 12px;
    right: 12px;
    width: 8px;
    height: 8px;
    background: #ef4444;
    border-radius: 50%;
    flex-shrink: 0;
    box-shadow: 0 0 0 2px #ffffff;
  }
}

// 响应式设计
@media (max-width: 768px) {
  .news-item {
    padding: 12px;
    
    .news-content {
      .news-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 4px;
      }
    }
  }
}
</style>

