<template>
  <div class="ai-chat-widget" :class="{ 'is-open': isOpen }">
    <!-- 聊天窗口 -->
    <transition name="slide-up">
      <div v-if="isOpen" class="chat-window">
        <div class="chat-header">
          <div class="header-left">
            <div class="ai-avatar">
              <TheIcon icon="carbon:ai" :size="20" />
            </div>
            <div class="header-info">
              <h4 class="ai-name">AI审核助手</h4>
              <span class="ai-status" :class="{ 'online': isOnline }">
                {{ isOnline ? '在线' : '离线' }}
              </span>
            </div>
          </div>
          <div class="header-actions">
            <n-button text @click="minimizeChat" size="small">
              <template #icon>
                <TheIcon icon="carbon:minimize" :size="18" />
              </template>
            </n-button>
            <n-button text @click="closeChat" size="small">
              <template #icon>
                <TheIcon icon="carbon:close" :size="18" />
              </template>
            </n-button>
          </div>
        </div>
        
        <div class="chat-messages" ref="messagesContainer">
          <!-- 欢迎消息 -->
          <div v-if="messages.length === 0" class="welcome-message">
            <div class="welcome-content">
              <div class="welcome-icon">
                <TheIcon icon="carbon:chat-bot" :size="32" />
              </div>
              <h3>您好！我是您的清洁生产审核助手</h3>
              <p>我可以帮您：</p>
              <ul>
                <li>解答审核相关问题</li>
                <li>提供政策解读</li>
                <li>生成审核报告</li>
                <li>分析企业数据</li>
              </ul>
              <p class="welcome-footer">有什么可以帮助您的吗？</p>
            </div>
          </div>
          
          <!-- 消息列表 -->
          <MessageBubble
            v-for="message in messages"
            :key="message.id"
            :message="message"
            :is-loading="isLoading && message.type === 'ai' && message.id === currentAiMessageId"
          />
          
          <!-- 正在输入指示器 -->
          <div v-if="isLoading && messages.length > 0 && messages[messages.length - 1].type !== 'ai'" class="typing-indicator">
            <div class="typing-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <span class="typing-text">AI正在思考...</span>
          </div>
        </div>
        
        <!-- 输入区域 -->
        <div class="chat-input-wrapper">
          <div class="input-toolbar">
            <n-button text @click="showQuickActions = !showQuickActions" size="small">
              <template #icon>
                <TheIcon icon="carbon:flash" :size="16" />
              </template>
            </n-button>
            <n-button text @click="clearHistory" size="small" :disabled="messages.length === 0">
              <template #icon>
                <TheIcon icon="carbon:trash-can" :size="16" />
              </template>
            </n-button>
          </div>
          
          <!-- 快速操作面板 -->
          <transition name="fade">
            <div v-if="showQuickActions" class="quick-actions">
              <div 
                v-for="action in quickActions"
                :key="action.key"
                class="quick-action-item"
                @click="handleQuickAction(action)"
              >
                <TheIcon :icon="action.icon" :size="16" />
                <span>{{ action.label }}</span>
              </div>
            </div>
          </transition>
          
          <div class="input-area">
            <n-input
              v-model:value="inputMessage"
              type="textarea"
              placeholder="输入您的问题..."
              :rows="2"
              :autosize="{ minRows: 1, maxRows: 4 }"
              @keydown.enter.prevent="handleEnter"
              :disabled="isLoading"
              :show-count="false"
            />
            <n-button 
              type="primary" 
              @click="sendMessage"
              :disabled="!inputMessage.trim() || isLoading"
              :loading="isLoading"
              class="send-button"
            >
              <template #icon>
                <TheIcon icon="carbon:send" :size="18" />
              </template>
            </n-button>
          </div>
        </div>
      </div>
    </transition>
    
    <!-- 浮动按钮 -->
    <transition name="scale">
      <div v-if="!isOpen" class="floating-button" @click="openChat">
        <div class="button-icon">
          <TheIcon icon="carbon:ai" :size="28" />
        </div>
        <div class="button-pulse"></div>
        <div v-if="unreadCount > 0" class="button-badge">
          {{ unreadCount > 99 ? '99+' : unreadCount }}
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted, onUnmounted, watch } from 'vue'
import { NButton, NInput, useMessage } from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'
import MessageBubble from './MessageBubble.vue'
import { getToken } from '@/utils/auth/token'

const message = useMessage()

// 状态管理
const isOpen = ref(false)
const isLoading = ref(false)
const isOnline = ref(true)
const showQuickActions = ref(false)
const inputMessage = ref('')
const unreadCount = ref(0)
const messagesContainer = ref(null)
const currentAiMessageId = ref(null)

// 消息列表
const messages = ref([])

// 快速操作
const quickActions = ref([
  { key: 'policy', label: '政策解读', icon: 'carbon:document', prompt: '请帮我解读最新的清洁生产政策' },
  { key: 'report', label: '生成报告', icon: 'carbon:report', prompt: '请帮我生成一份审核报告模板' },
  { key: 'analysis', label: '数据分析', icon: 'carbon:analytics', prompt: '请分析一下当前企业的环保指标' },
  { key: 'help', label: '使用帮助', icon: 'carbon:help', prompt: '请告诉我如何使用这个系统' }
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
  if (messages.value.length > 0 && !isOpen.value) {
    unreadCount.value = messages.value.filter(m => m.type === 'ai' && !m.read).length
  }
}

// 清除历史
const clearHistory = () => {
  messages.value = []
  message.success('聊天记录已清除')
}

// 发送消息
const sendMessage = async () => {
  if (!inputMessage.value.trim() || isLoading.value) return
  
  const userMessage = {
    id: Date.now(),
    type: 'user',
    content: inputMessage.value.trim(),
    timestamp: new Date(),
    read: true
  }
  
  messages.value.push(userMessage)
  const question = inputMessage.value.trim()
  inputMessage.value = ''
  showQuickActions.value = false
  scrollToBottom()

  // 创建AI消息占位符
  currentAiMessageId.value = Date.now() + 1
  const aiMessage = {
    id: currentAiMessageId.value,
    type: 'ai',
    content: '',
    timestamp: new Date(),
    read: false
  }
  messages.value.push(aiMessage)
  isLoading.value = true
  scrollToBottom()

  try {
    // 构建消息历史（保留最近10条）
    const history = messages.value
      .filter(m => m.content && m.id !== aiMessage.id)
      .slice(-10)
      .map(m => ({
        role: m.type === 'user' ? 'user' : 'assistant',
        content: m.content
      }))

    const payload = {
      messages: [
        {
          role: 'system',
          content: '你是一位专业的清洁生产审核助手。你的任务是帮助用户解答审核相关问题、提供政策解读、生成审核报告和分析企业数据。请用专业、友好、准确的方式回答用户的问题。'
        },
        ...history
      ],
      model: 'gpt-oss-120b',
      stream: true,
      max_tokens: 2048,
      temperature: 0.7,
      top_p: 0.7,
      extra_body: { top_k: 50 }
    }

    const url = `${import.meta.env.VITE_BASE_API}/ai/chat`
    const token = getToken()
    
    console.log('发送AI请求:', { url, payload: { ...payload, messages: payload.messages.map(m => ({ role: m.role, content: m.content.substring(0, 50) + '...' })) } })
    
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'text/event-stream, application/json',
        ...(token ? { 'Authorization': `Bearer ${token}`, 'token': token } : {})
      },
      body: JSON.stringify(payload)
    })
    
    console.log('收到响应:', { 
      status: response.status, 
      statusText: response.statusText,
      contentType: response.headers.get('content-type'),
      ok: response.ok 
    })

    if (!response.ok) {
      const errorText = await response.text()
      throw new Error(errorText || `HTTP ${response.status}`)
    }

    // 检查响应类型
    const contentType = response.headers.get('content-type') || ''
    
    // 处理JSON响应（非流式）
    if (contentType.includes('application/json')) {
      const data = await response.json()
      const content = data?.choices?.[0]?.message?.content || 
                     data?.choices?.[0]?.text || 
                     data?.content ||
                     data?.message ||
                     'AI返回了空内容'
      aiMessage.content = content
      messages.value = [...messages.value]
      aiMessage.read = true
      return
    }

    // 处理流式响应
    if (!response.body) {
      throw new Error('响应体为空')
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder('utf-8')
    let hasReceivedData = false
    
    try {
      while (true) {
        const { done, value } = await reader.read()
        
        if (done) break
        
        if (value) {
          hasReceivedData = true
          
          // 解码为文本（后端直接发送UTF-8编码的纯文本流）
          const textChunk = decoder.decode(value, { stream: true })
          
          if (textChunk && textChunk.length > 0) {
            // 找到消息在数组中的索引，确保响应式更新
            const messageIndex = messages.value.findIndex(m => m.id === aiMessage.id)
            
            if (messageIndex !== -1) {
              // 直接追加文本内容到消息对象
              messages.value[messageIndex].content += textChunk
              // 同时更新aiMessage对象以保持同步
              aiMessage.content += textChunk
              // 强制触发Vue响应式更新：创建新数组引用
              messages.value = [...messages.value]
              // 使用nextTick确保DOM更新
              await nextTick()
              scrollToBottom()
            } else {
              // 如果找不到消息，直接更新aiMessage
              aiMessage.content += textChunk
              messages.value = [...messages.value]
              await nextTick()
              scrollToBottom()
            }
            
            // 调试日志（仅在开始几个chunk时输出）
            if (aiMessage.content.length <= 200) {
              console.log('[AI流式] 收到文本块，长度:', textChunk.length, '累计:', aiMessage.content.length)
            }
          }
        }
      }
      
      // 等待所有异步更新完成
      await nextTick()
      
    } finally {
      reader.releaseLock()
    }
    
    // 确保最终内容正确同步到消息数组
    const finalMessageIndex = messages.value.findIndex(m => m.id === aiMessage.id)
    if (finalMessageIndex !== -1) {
      // 确保内容和状态同步
      messages.value[finalMessageIndex].content = aiMessage.content
      messages.value[finalMessageIndex].read = true
      // 强制触发响应式更新
      messages.value = [...messages.value]
    } else {
      aiMessage.read = true
      messages.value = [...messages.value]
    }
    
    // 调试：输出接收到的内容
    console.log('[AI完成] 响应接收完成，内容长度:', aiMessage.content.length)
    if (aiMessage.content && aiMessage.content.length > 0) {
      console.log('[AI完成] 响应预览:', aiMessage.content.substring(0, 200))
    }

    // 如果最终内容为空，显示错误提示
    if (!aiMessage.content || !aiMessage.content.trim()) {
      console.warn('[AI错误] 响应为空，hasReceivedData:', hasReceivedData)
      const errorIndex = messages.value.findIndex(m => m.id === aiMessage.id)
      if (errorIndex !== -1) {
        messages.value[errorIndex].content = '抱歉，未能获取AI响应。请检查网络连接或稍后重试。'
        messages.value = [...messages.value]
      } else {
        aiMessage.content = '抱歉，未能获取AI响应。请检查网络连接或稍后重试。'
        messages.value = [...messages.value]
      }
    } else {
      console.log('[AI成功] 响应成功接收，最终内容长度:', aiMessage.content.length)
    }
    
  } catch (err) {
    console.error('发送消息失败:', err)
    aiMessage.content = `抱歉，发生了错误：${err.message || '未知错误'}。请稍后重试。`
    aiMessage.read = true
    messages.value = [...messages.value]
    message.error('发送消息失败，请稍后重试')
  } finally {
    isLoading.value = false
    currentAiMessageId.value = null
    scrollToBottom()
  }
}

// 处理回车键
const handleEnter = (e) => {
  if (e.shiftKey) {
    return // Shift+Enter换行
  }
  sendMessage()
}

// 滚动到底部
const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

// 处理快速操作
const handleQuickAction = (action) => {
  showQuickActions.value = false
  inputMessage.value = action.prompt
  sendMessage()
}

// 监听消息变化，更新未读数量
watch(() => messages.value.length, () => {
  if (!isOpen.value && messages.value.length > 0) {
    unreadCount.value = messages.value.filter(m => m.type === 'ai' && !m.read).length
  }
})

// 键盘事件处理
const handleKeyDown = (event) => {
  if (event.key === 'Escape' && isOpen.value) {
    minimizeChat()
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
    width: 420px;
    height: 680px;
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
    flex-shrink: 0;
    
    .header-left {
      display: flex;
      align-items: center;
      gap: 12px;
      
      .ai-avatar {
        width: 40px;
        height: 40px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        backdrop-filter: blur(10px);
      }
      
      .header-info {
        .ai-name {
          font-size: 15px;
          font-weight: 600;
          margin: 0 0 4px 0;
          color: white;
        }
        
        .ai-status {
          font-size: 12px;
          opacity: 0.9;
          
          &.online {
            &::before {
              content: '●';
              color: #52c41a;
              margin-right: 4px;
            }
          }
        }
      }
    }
    
    .header-actions {
      display: flex;
      gap: 4px;
      
      :deep(.n-button) {
        color: white;
        
        &:hover {
          background: rgba(255, 255, 255, 0.1);
        }
      }
    }
  }
  
  .chat-messages {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 16px;
    background: #fafafa;
    
    &::-webkit-scrollbar {
      width: 6px;
    }
    
    &::-webkit-scrollbar-track {
      background: transparent;
    }
    
    &::-webkit-scrollbar-thumb {
      background: #d9d9d9;
      border-radius: 3px;
      
      &:hover {
        background: #bfbfbf;
      }
    }
  }
  
  .welcome-message {
    margin: 20px 0;
    
    .welcome-content {
      text-align: center;
      padding: 24px;
      
      .welcome-icon {
        margin: 0 auto 16px;
        width: 64px;
        height: 64px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
      }
      
      h3 {
        font-size: 18px;
        font-weight: 600;
        margin: 0 0 12px;
        color: #262626;
      }
      
      p {
        font-size: 14px;
        color: #595959;
        margin: 8px 0;
      }
      
      ul {
        text-align: left;
        display: inline-block;
        margin: 12px 0;
        padding-left: 20px;
        
        li {
          font-size: 13px;
          color: #595959;
          margin: 6px 0;
        }
      }
      
      .welcome-footer {
        margin-top: 16px;
        font-weight: 500;
        color: #262626;
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
    max-width: 80%;
    
    .typing-dots {
      display: flex;
      gap: 4px;
      
      span {
        width: 8px;
        height: 8px;
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
  
  .chat-input-wrapper {
    border-top: 1px solid #f0f0f0;
    background: white;
    padding: 12px 16px;
    flex-shrink: 0;
    
    .input-toolbar {
      display: flex;
      gap: 4px;
      margin-bottom: 8px;
      justify-content: flex-end;
    }
    
    .quick-actions {
      display: flex;
      gap: 8px;
      margin-bottom: 8px;
      padding: 8px;
      background: #fafafa;
      border-radius: 8px;
      flex-wrap: wrap;
      
      .quick-action-item {
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 6px 12px;
        background: white;
        border: 1px solid #e8e8e8;
        border-radius: 6px;
        cursor: pointer;
        font-size: 12px;
        transition: all 0.2s;
        color: #595959;
        
        &:hover {
          background: #f0f0f0;
          border-color: #667eea;
          color: #667eea;
        }
      }
    }
    
    .input-area {
      display: flex;
      gap: 8px;
      align-items: flex-end;
      
      :deep(.n-input) {
        flex: 1;
      }
      
      .send-button {
        flex-shrink: 0;
      }
    }
  }
  
  .floating-button {
    width: 64px;
    height: 64px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
    transition: all 0.3s ease;
    position: relative;
    
    &:hover {
      transform: scale(1.1);
      box-shadow: 0 6px 24px rgba(102, 126, 234, 0.5);
    }
    
    .button-icon {
      color: white;
      position: relative;
      z-index: 2;
    }
    
    .button-pulse {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      border-radius: 50%;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      animation: pulse 2s infinite;
    }
    
    .button-badge {
      position: absolute;
      top: -4px;
      right: -4px;
      background: #F5222D;
      color: white;
      font-size: 11px;
      font-weight: 600;
      padding: 2px 6px;
      border-radius: 12px;
      min-width: 18px;
      text-align: center;
      z-index: 3;
      border: 2px solid white;
    }
  }
}

// 动画
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

@keyframes scale {
  from {
    transform: scale(0);
    opacity: 0;
  }
  to {
    transform: scale(1);
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

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.7;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

// 响应式设计
@media (max-width: 768px) {
  .ai-chat-widget {
    bottom: 16px;
    right: 16px;
    
    .chat-window {
      width: calc(100vw - 32px);
      height: calc(100vh - 100px);
      max-width: 420px;
    }
    
    .floating-button {
      width: 56px;
      height: 56px;
    }
  }
}
</style>
