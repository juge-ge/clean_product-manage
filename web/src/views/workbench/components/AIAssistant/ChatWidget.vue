<template>
  <div class="ai-chat-widget" :class="{ 'is-open': isOpen }">
    <!-- 聊天窗口 -->
    <div v-if="isOpen" class="chat-window">
      <div class="chat-header">
        <div class="header-info">
          <div class="ai-avatar">
            <TheIcon icon="carbon:ai" :size="20" />
          </div>
          <div class="ai-info">
            <h4 class="ai-name">AI审核助手</h4>
            <span class="ai-status">在线</span>
          </div>
        </div>
        <div class="header-actions">
          <n-button text @click="minimizeChat">
            <template #icon>
              <TheIcon icon="carbon:minimize" :size="16" />
            </template>
          </n-button>
          <n-button text @click="closeChat">
            <template #icon>
              <TheIcon icon="carbon:close" :size="16" />
            </template>
          </n-button>
        </div>
      </div>
      
      <div class="chat-messages" ref="messagesContainer">
        <div class="welcome-message">
          <div class="message-content">
            <p>您好！我是您的清洁生产审核助手，可以帮您：</p>
            <ul>
              <li>解答审核相关问题</li>
              <li>提供政策解读</li>
              <li>生成审核报告</li>
              <li>分析企业数据</li>
            </ul>
            <p>有什么可以帮助您的吗？</p>
          </div>
        </div>
        
        <MessageBubble
          v-for="message in messages"
          :key="message.id"
          :message="message"
        />
        
        <div v-if="isLoading" class="typing-indicator">
          <div class="typing-dots">
            <span></span>
            <span></span>
            <span></span>
          </div>
          <span class="typing-text">AI正在思考...</span>
        </div>
      </div>
      
      <div class="chat-input">
        <div class="input-actions">
          <n-button text @click="toggleVoiceInput">
            <template #icon>
              <TheIcon :icon="isVoiceInput ? 'carbon:microphone-filled' : 'carbon:microphone'" :size="16" />
            </template>
          </n-button>
          <n-button text @click="showQuickActions">
            <template #icon>
              <TheIcon icon="carbon:flash" :size="16" />
            </template>
          </n-button>
        </div>
        <n-input
          v-model:value="inputMessage"
          placeholder="输入您的问题..."
          @keyup.enter="sendMessage"
          :disabled="isLoading"
        />
        <n-button 
          type="primary" 
          @click="sendMessage"
          :disabled="!inputMessage.trim() || isLoading"
        >
          <template #icon>
            <TheIcon icon="carbon:send" :size="16" />
          </template>
        </n-button>
      </div>
      
      <!-- 快速操作面板 -->
      <div v-if="showQuickActionsPanel" class="quick-actions-panel">
        <div class="panel-header">
          <span>快速操作</span>
          <n-button text @click="showQuickActionsPanel = false">
            <template #icon>
              <TheIcon icon="carbon:close" :size="14" />
            </template>
          </n-button>
        </div>
        <div class="actions-grid">
          <div 
            v-for="action in quickActions"
            :key="action.key"
            class="action-item"
            @click="handleQuickAction(action)"
          >
            <TheIcon :icon="action.icon" :size="16" />
            <span>{{ action.label }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 浮动按钮 -->
    <div v-else class="floating-button" @click="openChat">
      <div class="button-icon">
        <TheIcon icon="carbon:ai" :size="24" />
      </div>
      <div class="button-badge" v-if="unreadCount > 0">
        {{ unreadCount }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted, onUnmounted } from 'vue'
import { NButton, NInput, useMessage } from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'
import MessageBubble from './MessageBubble.vue'

const message = useMessage()

// 状态管理
const isOpen = ref(false)
const isLoading = ref(false)
const isVoiceInput = ref(false)
const showQuickActionsPanel = ref(false)
const inputMessage = ref('')
const unreadCount = ref(0)
const messagesContainer = ref(null)

// 消息列表
const messages = ref([])

// 快速操作
const quickActions = ref([
  { key: 'policy', label: '政策解读', icon: 'carbon:policy' },
  { key: 'report', label: '生成报告', icon: 'carbon:document' },
  { key: 'analysis', label: '数据分析', icon: 'carbon:analytics' },
  { key: 'help', label: '使用帮助', icon: 'carbon:help' }
])

// 打开聊天
const openChat = () => {
  isOpen.value = true
  unreadCount.value = 0
  nextTick(() => {
    scrollToBottom()
  })
}

// 关闭聊天
const closeChat = () => {
  isOpen.value = false
}

// 最小化聊天
const minimizeChat = () => {
  isOpen.value = false
}

// 发送消息
const sendMessage = async () => {
  if (!inputMessage.value.trim() || isLoading.value) return
  
  const userMessage = {
    id: Date.now(),
    type: 'user',
    content: inputMessage.value,
    timestamp: new Date()
  }
  
  messages.value.push(userMessage)
  const currentMessage = inputMessage.value
  inputMessage.value = ''
  
  scrollToBottom()
  
  // 模拟AI回复
  isLoading.value = true
  setTimeout(() => {
    const aiMessage = {
      id: Date.now() + 1,
      type: 'ai',
      content: generateAIResponse(currentMessage),
      timestamp: new Date()
    }
    messages.value.push(aiMessage)
    isLoading.value = false
    scrollToBottom()
  }, 1500)
}

// 生成AI回复（模拟）
const generateAIResponse = (userMessage) => {
  const responses = [
    '根据您的问题，我建议您查看最新的清洁生产政策文件。',
    '这个问题涉及到环保指标的具体要求，让我为您详细分析一下。',
    '基于您提供的信息，我为您生成了以下建议方案。',
    '这是一个很好的问题，让我为您查找相关的政策依据。',
    '根据行业标准，我建议您采用以下审核流程。'
  ]
  return responses[Math.floor(Math.random() * responses.length)]
}

// 滚动到底部
const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

// 切换语音输入
const toggleVoiceInput = () => {
  isVoiceInput.value = !isVoiceInput.value
  message.info(isVoiceInput.value ? '语音输入已开启' : '语音输入已关闭')
}

// 显示快速操作
const showQuickActions = () => {
  showQuickActionsPanel.value = !showQuickActionsPanel.value
}

// 处理快速操作
const handleQuickAction = (action) => {
  showQuickActionsPanel.value = false
  const actionMessages = {
    policy: '请帮我解读最新的清洁生产政策',
    report: '请帮我生成一份审核报告模板',
    analysis: '请分析一下当前企业的环保指标',
    help: '请告诉我如何使用这个系统'
  }
  inputMessage.value = actionMessages[action.key]
}

// 键盘事件处理
const handleKeyDown = (event) => {
  if (event.key === 'Escape' && isOpen.value) {
    closeChat()
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleKeyDown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeyDown)
})
</script>

<style lang="scss" scoped>
.ai-chat-widget {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 1000;
  
  .chat-window {
    width: 400px;
    height: 600px;
    background: #ffffff;
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    animation: slideUp 0.3s ease;
  }
  
  .chat-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 16px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    .header-info {
      display: flex;
      align-items: center;
      gap: 12px;
      
      .ai-avatar {
        width: 36px;
        height: 36px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        backdrop-filter: blur(10px);
      }
      
      .ai-info {
        .ai-name {
          font-size: 14px;
          font-weight: 600;
          margin: 0 0 2px 0;
        }
        
        .ai-status {
          font-size: 11px;
          opacity: 0.8;
        }
      }
    }
    
    .header-actions {
      display: flex;
      gap: 4px;
    }
  }
  
  .chat-messages {
    flex: 1;
    padding: 16px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 12px;
    
    &::-webkit-scrollbar {
      width: 4px;
    }
    
    &::-webkit-scrollbar-track {
      background: #f0f0f0;
    }
    
    &::-webkit-scrollbar-thumb {
      background: #d9d9d9;
      border-radius: 2px;
    }
  }
  
  .welcome-message {
    background: #f6ffed;
    border: 1px solid #b7eb8f;
    border-radius: 12px;
    padding: 16px;
    
    .message-content {
      font-size: 13px;
      color: #262626;
      line-height: 1.5;
      
      ul {
        margin: 8px 0;
        padding-left: 16px;
        
        li {
          margin: 4px 0;
        }
      }
    }
  }
  
  .typing-indicator {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px 16px;
    background: #f0f0f0;
    border-radius: 12px;
    align-self: flex-start;
    
    .typing-dots {
      display: flex;
      gap: 4px;
      
      span {
        width: 6px;
        height: 6px;
        background: #8C8C8C;
        border-radius: 50%;
        animation: typing 1.4s infinite ease-in-out;
        
        &:nth-child(1) { animation-delay: -0.32s; }
        &:nth-child(2) { animation-delay: -0.16s; }
      }
    }
    
    .typing-text {
      font-size: 12px;
      color: #8C8C8C;
    }
  }
  
  .chat-input {
    padding: 16px;
    border-top: 1px solid #f0f0f0;
    display: flex;
    align-items: center;
    gap: 8px;
    
    .input-actions {
      display: flex;
      gap: 4px;
    }
    
    .n-input {
      flex: 1;
    }
  }
  
  .quick-actions-panel {
    position: absolute;
    bottom: 80px;
    left: 16px;
    right: 16px;
    background: #ffffff;
    border: 1px solid #f0f0f0;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    
    .panel-header {
      padding: 12px 16px;
      border-bottom: 1px solid #f0f0f0;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 12px;
      font-weight: 600;
      color: #262626;
    }
    
    .actions-grid {
      padding: 12px;
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 8px;
      
      .action-item {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px 12px;
        border-radius: 8px;
        cursor: pointer;
        transition: background-color 0.2s ease;
        font-size: 12px;
        color: #262626;
        
        &:hover {
          background: #f0f0f0;
        }
      }
    }
  }
  
  .floating-button {
    width: 60px;
    height: 60px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
    transition: all 0.3s ease;
    position: relative;
    
    &:hover {
      transform: scale(1.1);
      box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .button-icon {
      color: white;
    }
    
    .button-badge {
      position: absolute;
      top: -4px;
      right: -4px;
      background: #F5222D;
      color: white;
      font-size: 10px;
      font-weight: 600;
      padding: 2px 6px;
      border-radius: 10px;
      min-width: 16px;
      text-align: center;
    }
  }
}

@keyframes slideUp {
  from {
    transform: translateY(100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes typing {
  0%, 80%, 100% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

// 响应式设计
@media (max-width: 768px) {
  .ai-chat-widget {
    bottom: 16px;
    right: 16px;
    
    .chat-window {
      width: calc(100vw - 32px);
      height: calc(100vh - 100px);
      max-width: 400px;
    }
  }
}
</style>

