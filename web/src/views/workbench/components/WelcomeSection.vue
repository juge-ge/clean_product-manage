<template>
  <n-card class="welcome-section" :bordered="false">
    <div class="welcome-content">
      <!-- 用户问候区域 -->
      <div class="user-greeting">
        <img 
          :src="userStore.avatar || '/default-avatar.png'" 
          class="user-avatar" 
          alt="用户头像"
        />
        <div class="greeting-text">
          <h2 class="greeting-title">{{ dynamicGreeting }}</h2>
          <p class="motivational-message">{{ motivationalMessage }}</p>
        </div>
      </div>
      
      <!-- 关键指标卡片组 -->
      <div class="metrics-grid">
        <MetricCard 
          v-for="metric in keyMetrics" 
          :key="metric.key"
          :metric="metric"
        />
      </div>
    </div>
  </n-card>
</template>

<script setup>
import { computed } from 'vue'
import { NCard } from 'naive-ui'
import { useUserStore } from '@/store'
import MetricCard from './MetricCard.vue'

const userStore = useUserStore()

// 动态问候语
const dynamicGreeting = computed(() => {
  const hour = new Date().getHours()
  const username = userStore.name || '用户'
  
  if (hour < 6) {
    return `夜深了，${username}，注意休息！`
  } else if (hour < 9) {
    return `早上好，${username}！`
  } else if (hour < 12) {
    return `上午好，${username}！`
  } else if (hour < 14) {
    return `中午好，${username}！`
  } else if (hour < 18) {
    return `下午好，${username}！`
  } else if (hour < 22) {
    return `晚上好，${username}！`
  } else {
    return `夜深了，${username}，注意休息！`
  }
})

// 励志消息
const motivationalMessage = computed(() => {
  const messages = [
    '今天又是元气满满的一天！',
    '让我们一起为清洁生产努力！',
    '每一个审核都是对环境的保护！',
    '您的专业让世界更美好！',
    '继续加油，您是最棒的！',
    '环保事业需要您的坚持！'
  ]
  return messages[Math.floor(Math.random() * messages.length)]
})

// 基础指标数据
const keyMetrics = computed(() => [
  {
    key: 'notifications',
    label: '通知',
    value: 8,
    unit: '',
    icon: 'carbon:notification',
    color: '#8B5CF6',
    trend: '+3'
  },
  {
    key: 'projects',
    label: '项目数',
    value: 25,
    unit: '',
    icon: 'carbon:chart-line',
    color: '#1890FF',
    trend: '+12%'
  },
  {
    key: 'todos',
    label: '待办',
    value: 4,
    total: 16,
    unit: '',
    icon: 'carbon:task',
    color: '#FA8C16',
    trend: '-2'
  }
])
</script>

<style lang="scss" scoped>
.welcome-section {
  border-radius: 10px;
  margin-bottom: 12px;
  
  .welcome-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    padding: 16px 20px;
  }
  
  .user-greeting {
    display: flex;
    align-items: center;
    gap: 16px;
    
    .user-avatar {
      width: 56px;
      height: 56px;
      border-radius: 50%;
      object-fit: cover;
      border: 3px solid #f0f0f0;
    }
    
    .greeting-text {
      font-family: 'Inter', 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
      
      .greeting-title {
        font-size: 22px;
        font-weight: 700;
        color: #262626;
        margin: 0 0 6px 0;
        line-height: 1.3;
        letter-spacing: 0.01em;
      }
      
      .motivational-message {
        font-size: 15px;
        font-weight: 500;
        color: #8C8C8C;
        margin: 0;
        line-height: 1.4;
        letter-spacing: 0.005em;
      }
    }
  }
  
  .metrics-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    min-width: 0;
  }
}

// 响应式设计
@media (max-width: 768px) {
  .welcome-section {
    .welcome-content {
      flex-direction: column;
      align-items: flex-start;
      gap: 16px;
    }
    
    .metrics-grid {
      grid-template-columns: repeat(3, 1fr);
      width: 100%;
      gap: 8px;
    }
  }
}

@media (max-width: 480px) {
  .welcome-section .metrics-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
}
</style>
