<template>
  <div class="message-bubble" :class="[`message-${message.type}`, { 'is-loading': isLoading }]">
    <div class="message-avatar" v-if="message.type === 'ai'">
      <TheIcon icon="carbon:ai" :size="16" />
    </div>
    
    <div class="message-content">
      <div class="message-text" v-html="formattedContent"></div>
      <div class="message-time">{{ formatTime }}</div>
    </div>
    
    <div class="message-avatar" v-if="message.type === 'user'">
      <TheIcon icon="carbon:user" :size="16" />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import TheIcon from '@/components/icon/TheIcon.vue'

const props = defineProps({
  message: {
    type: Object,
    required: true
  },
  isLoading: {
    type: Boolean,
    default: false
  }
})

// 格式化内容
const formattedContent = computed(() => {
  if (!props.message.content) return ''
  
  // 简单的文本格式化
  return props.message.content
    .replace(/\n/g, '<br>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
})

// 格式化时间
const formatTime = computed(() => {
  if (!props.message.timestamp) return ''
  
  const time = new Date(props.message.timestamp)
  const now = new Date()
  const diffTime = now.getTime() - time.getTime()
  const diffMinutes = Math.floor(diffTime / (1000 * 60))
  
  if (diffMinutes < 1) {
    return '刚刚'
  } else if (diffMinutes < 60) {
    return `${diffMinutes}分钟前`
  } else {
    return time.toLocaleTimeString('zh-CN', { 
      hour: '2-digit', 
      minute: '2-digit' 
    })
  }
})
</script>

<style lang="scss" scoped>
.message-bubble {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  max-width: 80%;
  
  &.message-user {
    align-self: flex-end;
    flex-direction: row-reverse;
    
    .message-content {
      background: #1890FF;
      color: white;
      
      .message-text {
        color: white;
      }
      
      .message-time {
        color: rgba(255, 255, 255, 0.7);
      }
    }
    
    .message-avatar {
      background: #1890FF;
      color: white;
    }
  }
  
  &.message-ai {
    align-self: flex-start;
    
    .message-content {
      background: #f0f0f0;
      color: #262626;
    }
    
    .message-avatar {
      background: #667eea;
      color: white;
    }
  }
  
  .message-avatar {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-top: 2px;
  }
  
  .message-content {
    border-radius: 12px;
    padding: 12px 16px;
    position: relative;
    
    .message-text {
      font-size: 13px;
      line-height: 1.5;
      margin-bottom: 4px;
      
      :deep(strong) {
        font-weight: 600;
      }
      
      :deep(em) {
        font-style: italic;
      }
    }
    
    .message-time {
      font-size: 10px;
      opacity: 0.7;
    }
  }
  
  &.is-loading {
    .message-content {
      opacity: 0.7;
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .message-bubble {
    max-width: 90%;
    
    .message-avatar {
      width: 24px;
      height: 24px;
    }
    
    .message-content {
      padding: 10px 12px;
      
      .message-text {
        font-size: 12px;
      }
    }
  }
}
</style>

