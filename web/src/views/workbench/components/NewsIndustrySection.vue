<template>
  <div class="news-industry-section">
    <!-- 内容区域 -->
    <div class="content-grid">
      <!-- 最新动态 -->
      <div class="news-panel">
        <div class="panel-header">
          <div class="panel-title">
            <TheIcon icon="carbon:notification" :size="20" />
            <span>最新动态</span>
          </div>
          <n-button text type="primary" size="small" @click="viewAllNews">
            查看更多
          </n-button>
        </div>
        <div class="news-content">
          <NewsItem
            v-for="news in displayedNewsList"
            :key="news.id"
            :news="news"
            @click="handleNewsClick(news)"
          />
          <div v-if="displayedNewsList.length === 0" class="empty-state">
            <n-empty description="暂无最新动态" size="small">
              <template #icon>
                <TheIcon icon="carbon:notification" :size="32" />
              </template>
            </n-empty>
          </div>
        </div>
      </div>
      
      <!-- 行业审核概览 -->
      <div class="industry-panel">
        <div class="panel-header">
          <div class="panel-title">
            <TheIcon icon="carbon:chart-line" :size="20" />
            <span>行业审核概览</span>
          </div>
        </div>
        <div class="industry-content">
          <IndustryCard
            v-for="industry in industryData"
            :key="industry.key"
            :industry="industry"
            @click="handleIndustryClick(industry)"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { NCard, NButton, NEmpty, useMessage } from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'
import NewsItem from './NewsItem.vue'
import IndustryCard from './IndustryCard.vue'

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

// 行业数据
const industryData = ref([
  {
    key: 'steel',
    name: '钢铁行业',
    icon: 'carbon:industry',
    color: '#1890FF',
    totalEnterprises: 25,
    completedAudits: 20,
    inProgressAudits: 3,
    pendingAudits: 2,
    completionRate: 80,
    route: '/cloud-audit/steel'
  },
  {
    key: 'pcb',
    name: 'PCB行业',
    icon: 'carbon:chip',
    color: '#52C41A',
    totalEnterprises: 18,
    completedAudits: 15,
    inProgressAudits: 2,
    pendingAudits: 1,
    completionRate: 83,
    route: '/cloud-audit/pcb'
  },
  {
    key: 'glass',
    name: '平板玻璃',
    icon: 'carbon:glass',
    color: '#FA8C16',
    totalEnterprises: 12,
    completedAudits: 10,
    inProgressAudits: 1,
    pendingAudits: 1,
    completionRate: 83,
    route: '/cloud-audit/glass'
  },
  {
    key: 'coking',
    name: '焦化行业',
    icon: 'carbon:chemistry',
    color: '#F5222D',
    totalEnterprises: 8,
    completedAudits: 6,
    inProgressAudits: 1,
    pendingAudits: 1,
    completionRate: 75,
    route: '/cloud-audit/coking'
  },
  {
    key: 'furniture',
    name: '家具行业',
    icon: 'carbon:sofa',
    color: '#722ED1',
    totalEnterprises: 15,
    completedAudits: 12,
    inProgressAudits: 2,
    pendingAudits: 1,
    completionRate: 80,
    route: '/cloud-audit/furniture'
  },
  {
    key: 'auto-repair',
    name: '汽修行业',
    icon: 'carbon:car',
    color: '#13C2C2',
    totalEnterprises: 22,
    completedAudits: 18,
    inProgressAudits: 3,
    pendingAudits: 1,
    completionRate: 82,
    route: '/cloud-audit/auto-repair'
  }
])

// 计算总统计
const totalEnterprises = computed(() => {
  return industryData.value.reduce((sum, industry) => sum + industry.totalEnterprises, 0)
})

const totalCompleted = computed(() => {
  return industryData.value.reduce((sum, industry) => sum + industry.completedAudits, 0)
})

const overallCompletionRate = computed(() => {
  if (totalEnterprises.value === 0) return 0
  return Math.round((totalCompleted.value / totalEnterprises.value) * 100)
})

// 只显示前4条最新动态
const displayedNewsList = computed(() => {
  return newsList.value.slice(0, 4)
})

// 处理动态点击
const handleNewsClick = (news) => {
  console.log('点击动态:', news)
  // 标记为已读
  news.isRead = true
  message.info('查看详情功能开发中...')
}

// 处理行业点击
const handleIndustryClick = (industry) => {
  console.log('点击行业:', industry)
  router.push(industry.route)
}

// 查看全部动态
const viewAllNews = () => {
  router.push('/workbench/news')
}

onMounted(() => {
  console.log('最新动态和行业概览组件已挂载')
})
</script>

<style lang="scss" scoped>
.news-industry-section {
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  margin-bottom: 24px;
  overflow: hidden;
  height: auto;
  min-height: 400px;
  
  // 内容网格
  .content-grid {
    display: grid;
    grid-template-columns: 1fr 1.5fr;
    height: auto;
    min-height: 400px;
    
    .news-panel,
    .industry-panel {
      display: flex;
      flex-direction: column;
      padding: 20px 24px;
      
      .panel-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 1px solid #f1f5f9;
        
        .panel-title {
          display: flex;
          align-items: center;
          gap: 8px;
          font-size: 16px;
          font-weight: 600;
          color: #1e293b;
        }
      }
    }
    
    // 最新动态面板
    .news-panel {
      border-right: 1px solid #f1f5f9;
      background: #fafbfc;
      
      .news-content {
        display: flex;
        flex-direction: column;
        gap: 6px;
        flex: 1;
        overflow: hidden;
        
        // 移除滚动条，因为只显示5条
        &::-webkit-scrollbar {
          display: none;
        }
      }
      
      .empty-state {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 120px;
        color: #64748b;
      }
    }
    
           // 行业概览面板
           .industry-panel {
             .industry-content {
               display: grid;
               grid-template-columns: repeat(3, 1fr);
               grid-template-rows: repeat(2, auto);
               gap: 8px;
               flex: 1;
               min-height: 0; // 确保网格可以收缩
               align-content: start; // 内容从顶部开始排列
             }
           }
  }
}

// 响应式设计
@media (max-width: 1200px) {
  .news-industry-section {
    .content-grid {
      grid-template-columns: 1fr;
      height: auto;
      
      .news-panel {
        border-right: none;
        border-bottom: 1px solid #f1f5f9;
        min-height: 300px;
      }
      
      .industry-panel .industry-content {
        grid-template-columns: repeat(2, 1fr);
        grid-template-rows: repeat(3, 1fr);
      }
    }
  }
}

@media (max-width: 768px) {
  .news-industry-section {
    height: auto;
    margin-bottom: 16px;
    
    .section-header {
      padding: 20px 24px;
      flex-direction: column;
      align-items: flex-start;
      gap: 16px;
      
      .header-stats {
        width: 100%;
        justify-content: space-between;
        gap: 12px;
        
        .stat-card {
          flex: 1;
          padding: 10px 12px;
          
          .stat-number {
            font-size: 18px;
          }
        }
      }
    }
    
    .content-grid {
      .news-panel,
      .industry-panel {
        padding: 20px 24px;
      }
      
      .industry-panel .industry-content {
        grid-template-columns: 1fr;
        grid-template-rows: repeat(6, 1fr);
      }
    }
  }
}
</style>

