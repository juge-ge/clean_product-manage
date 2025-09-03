<template>
  <div class="notice-container">
    <!-- 搜索框 -->
    <div class="search-wrapper">
      <n-input-group style="width: 300px">
        <n-input
          v-model:value="searchKeyword"
          placeholder="搜索"
          clearable
          class="search-input"
        />
        <n-button type="primary" @click="handleSearch" style="padding: 0 24px">
          搜索
        </n-button>
      </n-input-group>
    </div>

    <!-- 两栏布局 -->
    <div class="notice-grid mt-4">
      <!-- 国家通知公告 -->
      <div class="notice-column">
        <n-card :bordered="false" class="notice-card">
          <template #header>
            <div class="card-header">
              <span class="header-title">国家通知公告</span>
              <n-button text type="primary" @click="goToList('national')" class="header-action">
                查看更多 <n-icon><i class="mdi" :class="arrowRightIcon" /></n-icon>
              </n-button>
            </div>
          </template>
          <n-list hoverable clickable>
            <n-list-item v-for="item in nationalNotices.slice(0, 6)" :key="item.id">
              <n-thing>
                <template #header>
                  <a href="javascript:;" @click="goToDetail(item.id)" class="notice-title">
                    {{ item.title }}
                  </a>
                </template>
                <template #description>
                  <n-space align="center">
                    <n-tag size="small" type="info">{{ item.source }}</n-tag>
                    <span class="notice-date">{{ item.publishDate }}</span>
                  </n-space>
                </template>
              </n-thing>
            </n-list-item>
          </n-list>

        </n-card>
      </div>

      <!-- 各省通知公告 -->
      <div class="notice-column">
        <n-card :bordered="false" class="notice-card">
          <template #header>
            <div class="card-header">
              <span class="header-title">各省通知公告</span>
              <n-button text type="primary" @click="goToList('provincial')" class="header-action">
                查看更多 <n-icon><i class="mdi" :class="arrowRightIcon" /></n-icon>
              </n-button>
            </div>
          </template>
          <n-list hoverable clickable>
            <n-list-item v-for="item in provincialNotices.slice(0, 6)" :key="item.id">
              <n-thing>
                <template #header>
                  <a href="javascript:;" @click="goToDetail(item.id)" class="notice-title">
                    {{ item.title }}
                  </a>
                </template>
                <template #description>
                  <n-space align="center">
                    <n-tag size="small" type="success">{{ item.province }}</n-tag>
                    <span class="notice-date">{{ item.publishDate }}</span>
                  </n-space>
                </template>
              </n-thing>
            </n-list-item>
          </n-list>

        </n-card>
      </div>
    </div>

    <!-- 详情弹窗 -->
    <notice-detail-modal
      v-model:show="showDetailModal"
      :notice-id="currentNoticeId"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { usePermissionStore } from '@/store'
import NoticeDetailModal from './components/NoticeDetailModal.vue'

// 使用项目自带的图标
const searchIcon = 'mdi-account-search'
const arrowRightIcon = 'mdi-arrow-right'

const router = useRouter()
const searchKeyword = ref('')

// 生成Mock数据的函数
const generateMockNotices = (type, count = 20) => {
  const notices = []
  const sources = type === 'national' 
    ? ['生态环境部', '国家发改委', '工信部', '财政部', '科技部', '农业农村部', '商务部', '应急管理部']
    : ['湖南省生态环境厅', '江苏省生态环境厅', '浙江省生态环境厅', '广东省生态环境厅', '山东省生态环境厅', '河南省生态环境厅', '四川省生态环境厅', '湖北省生态环境厅']
  
  const titles = type === 'national' 
    ? [
        '关于开展2025年度清洁生产审核评估工作的通知',
        '清洁生产审核评估专家库专家征集公告',
        '关于印发《清洁生产审核评估管理办法》的通知',
        '清洁生产技术创新项目申报指南',
        '清洁生产审核评估标准体系更新通知',
        '清洁生产审核评估专家培训计划',
        '清洁生产审核评估质量提升专项行动',
        '清洁生产审核评估信息化建设方案',
        '清洁生产审核评估国际合作项目',
        '清洁生产审核评估成果展示活动',
        '清洁生产审核评估政策解读培训',
        '清洁生产审核评估技术规范修订',
        '清洁生产审核评估专家考核办法',
        '清洁生产审核评估数据统计报告',
        '清洁生产审核评估典型案例汇编',
        '清洁生产审核评估工作推进会通知',
        '清洁生产审核评估技术交流会议',
        '清洁生产审核评估标准宣贯培训',
        '清洁生产审核评估质量检查通知',
        '清洁生产审核评估工作总结报告'
      ]
    : [
        '湖南省2025年清洁生产审核重点企业名单公示',
        '江苏省清洁生产审核评估专家选拔通知',
        '浙江省清洁生产示范企业认定结果公示',
        '广东省清洁生产审核评估工作部署',
        '山东省清洁生产审核评估专家库建设',
        '河南省清洁生产审核评估质量提升',
        '四川省清洁生产审核评估技术创新',
        '湖北省清洁生产审核评估标准制定',
        '福建省清洁生产审核评估专家培训',
        '安徽省清洁生产审核评估工作推进',
        '江西省清洁生产审核评估质量检查',
        '河北省清洁生产审核评估专家选拔',
        '山西省清洁生产审核评估技术创新',
        '内蒙古清洁生产审核评估工作部署',
        '辽宁省清洁生产审核评估专家库建设',
        '吉林省清洁生产审核评估质量提升',
        '黑龙江省清洁生产审核评估标准制定',
        '陕西省清洁生产审核评估专家培训',
        '甘肃省清洁生产审核评估工作推进',
        '青海省清洁生产审核评估质量检查',
        '宁夏清洁生产审核评估专家选拔'
      ]
  
  for (let i = 0; i < count; i++) {
    const randomMonth = Math.floor(Math.random() * 12) + 1
    const randomDay = Math.floor(Math.random() * 28) + 1
    const randomSource = sources[Math.floor(Math.random() * sources.length)]
    
    notices.push({
      id: type === 'national' ? i + 1 : i + 101,
      title: titles[i],
      publishDate: `2025-${String(randomMonth).padStart(2, '0')}-${String(randomDay).padStart(2, '0')}`,
      source: randomSource,
      province: type === 'provincial' ? randomSource.replace('生态环境厅', '省') : undefined
    })
  }
  
  // 按日期排序，最新的在前面
  return notices.sort((a, b) => new Date(b.publishDate) - new Date(a.publishDate))
}

// 生成Mock数据 - 各20条
const nationalNotices = ref(generateMockNotices('national', 20))
const provincialNotices = ref(generateMockNotices('provincial', 20))

// 显示详情弹窗
const showDetailModal = ref(false)
const currentNoticeId = ref(null)

const goToDetail = (id) => {
  currentNoticeId.value = id
  showDetailModal.value = true
}

// 跳转到列表页
const goToList = (type) => {
  console.log('跳转到列表页:', type)
  router.push({
    path: `/clean-production/policy/notice/list/${type}`
  }).catch(err => {
    console.error('路由跳转错误:', err)
    // 如果路由错误，尝试重新加载路由
    const permissionStore = usePermissionStore()
    permissionStore.generateRoutes().then(() => {
      router.push({
        path: `/clean-production/policy/notice/list/${type}`
      })
    })
  })
}

// 搜索处理
const handleSearch = () => {
  if (searchKeyword.value.trim()) {
    console.log('搜索关键词:', searchKeyword.value)
    router.push({
      name: 'notice-search',
      query: { keyword: searchKeyword.value }
    }).catch(err => {
      console.error('路由跳转错误:', err)
    })
  }
}


</script>

<style scoped>
.notice-container {
  padding: 16px;
}

.search-wrapper {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 16px;
}

.search-input :deep(.n-input__placeholder) {
  display: flex;
  align-items: center;
  justify-content: center;
}

.notice-grid {
  display: flex;
  gap: 12px;
  position: relative;
}

.notice-grid::after {
  content: '';
  position: absolute;
  left: 50%;
  top: 0;
  bottom: 0;
  border-left: 1px dashed #e5e5e5;
  transform: translateX(-50%);
}

.notice-column {
  flex: 1;
}

.notice-card {
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 8px;
  border-bottom: 2px solid var(--primary-color);
  margin-bottom: 8px;
}

.header-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.header-action {
  font-size: 14px;
  color: var(--primary-color);
  cursor: pointer;
  
  &:hover {
    opacity: 0.8;
  }
}

.notice-title {
  color: #333;
  text-decoration: none;
  font-size: 14px;
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.notice-title:hover {
  color: #2080f0;
}

.notice-date {
  color: #999;
  font-size: 12px;
}

.view-more {
  text-align: right;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #eee;
}

.mt-4 {
  margin-top: 16px;
}
</style>