<template>
  <n-card class="news-section" :bordered="false">
    <div class="section-header">
      <h3 class="section-title">最新动态</h3>
      <n-button text type="primary" size="small" @click="viewAllNews">
        查看全部
      </n-button>
    </div>
    <div class="news-list">
      <NewsItem
        v-for="news in newsList"
        :key="news.id"
        :news="news"
        @click="handleNewsClick(news)"
      />
      <div v-if="newsList.length === 0" class="empty-state">
        <n-empty description="暂无最新动态" size="small">
          <template #icon>
            <TheIcon icon="carbon:notification" :size="32" />
          </template>
        </n-empty>
      </div>
    </div>
  </n-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { NCard, NButton, NEmpty, useMessage } from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'
import NewsItem from './NewsItem.vue'

const router = useRouter()
const message = useMessage()

// 最新动态数据
const newsList = ref([
  {
    id: 1,
    title: '新政策发布：清洁生产标准更新',
    type: 'policy',
    content: '国家发改委发布最新清洁生产标准，涉及钢铁、PCB等多个行业',
    time: '2024-01-15 10:30',
    author: '系统管理员',
    isRead: false
  },
  {
    id: 2,
    title: 'XX钢铁审核报告已完成',
    type: 'completion',
    content: '张三已完成XX钢铁有限公司的清洁生产审核报告',
    time: '2024-01-15 09:15',
    author: '张三',
    isRead: false
  },
  {
    id: 3,
    title: 'PCB审核流程更新通知',
    type: 'update',
    content: 'PCB行业审核流程已更新，请相关人员查看最新流程',
    time: '2024-01-14 16:45',
    author: '系统管理员',
    isRead: true
  },
  {
    id: 4,
    title: '系统维护公告',
    type: 'notification',
    content: '系统将于本周六进行例行维护，预计停机2小时',
    time: '2024-01-14 14:20',
    author: '系统管理员',
    isRead: false
  },
  {
    id: 5,
    title: '月度统计报告发布',
    type: 'report',
    content: '1月份清洁生产审核统计报告已发布，请查看',
    time: '2024-01-14 11:30',
    author: '数据分析师',
    isRead: true
  },
  {
    id: 6,
    title: '新用户培训通知',
    type: 'training',
    content: '新用户培训将于下周三举行，请相关人员准时参加',
    time: '2024-01-13 16:00',
    author: '培训管理员',
    isRead: false
  }
])

// 处理动态点击
const handleNewsClick = (news) => {
  console.log('点击动态:', news)
  // 标记为已读
  news.isRead = true
  message.info('查看详情功能开发中...')
}

// 查看全部动态
const viewAllNews = () => {
  router.push('/workbench/news')
}

onMounted(() => {
  console.log('最新动态组件已挂载')
})
</script>

<style lang="scss" scoped>
.news-section {
  border-radius: 10px;
  margin-bottom: 16px;
  height: 100%;
  
  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 2px solid #f0f0f0;
    
    .section-title {
      font-size: 16px;
      font-weight: 600;
      color: #262626;
      margin: 0;
    }
  }
  
  .news-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
    height: calc(100vh - 300px);
    overflow-y: auto;
    
    &::-webkit-scrollbar {
      width: 4px;
    }
    
    &::-webkit-scrollbar-track {
      background: #f0f0f0;
      border-radius: 2px;
    }
    
    &::-webkit-scrollbar-thumb {
      background: #d9d9d9;
      border-radius: 2px;
    }
    
    &::-webkit-scrollbar-thumb:hover {
      background: #bfbfbf;
    }
  }
  
  .empty-state {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 120px;
    color: #8C8C8C;
  }
}

// 响应式设计
@media (max-width: 768px) {
  .news-section {
    .section-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 8px;
    }
    
    .news-list {
      height: calc(100vh - 250px);
    }
  }
}
</style>
