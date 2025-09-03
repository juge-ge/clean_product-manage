<template>
  <div class="notice-list">
    <n-breadcrumb class="breadcrumb">
      <n-breadcrumb-item>
        <router-link to="/clean-production">清洁生产管理</router-link>
      </n-breadcrumb-item>
      <n-breadcrumb-item>
        <router-link to="/clean-production/policy">清洁生产政策与管理</router-link>
      </n-breadcrumb-item>
      <n-breadcrumb-item>
        <router-link to="/clean-production/policy/notice">通知公告</router-link>
      </n-breadcrumb-item>
      <n-breadcrumb-item>{{ pageTitle }}</n-breadcrumb-item>
    </n-breadcrumb>

    <n-card class="mt-4">
      <template #header>
        <n-space justify="space-between" align="center">
          <n-space align="center">
            <span class="page-title">{{ pageTitle }}</span>
            <n-button 
              type="primary" 
              ghost 
              size="small" 
              @click="goBack"
              style="margin-left: 16px"
            >
              返回
            </n-button>
          </n-space>
          <n-space>
            <n-input
              v-model:value="searchKeyword"
              placeholder="请输入关键词搜索"
              style="width: 200px"
            />
            <n-button type="primary" @click="handleSearch">搜索</n-button>
          </n-space>
        </n-space>
      </template>

      <n-list hoverable clickable>
        <n-list-item v-for="item in filteredNotices" :key="item.id">
          <n-thing>
            <template #header>
              <a href="javascript:;" @click="goToDetail(item.id)" class="notice-title">
                {{ item.title }}
              </a>
            </template>
            <template #description>
              <n-space align="center">
                <template v-if="item.province">
                  <n-tag size="small" type="success">{{ item.province }}</n-tag>
                </template>
                <template v-else>
                  <n-tag size="small" type="info">{{ item.source }}</n-tag>
                </template>
                <span class="notice-date">{{ item.publishDate }}</span>
              </n-space>
            </template>
          </n-thing>
        </n-list-item>
      </n-list>

      <div class="pagination">
        <n-pagination
          v-model:page="currentPage"
          :page-size="pageSize"
          :item-count="total"
          show-quick-jumper
          show-size-picker
          :page-sizes="[10, 20, 30, 40]"
        />
      </div>
    </n-card>

    <!-- 详情弹窗 -->
    <notice-detail-modal
      v-model:show="showDetailModal"
      :notice-id="currentNoticeId"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import NoticeDetailModal from './components/NoticeDetailModal.vue'

const route = useRoute()
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)
const searchKeyword = ref('')
const showDetailModal = ref(false)
const currentNoticeId = ref(null)

// 根据路由类型显示不同标题
const pageTitle = computed(() => {
  return route.params.type === 'national' ? '国家通知公告' : '各省通知公告'
})

// 生成Mock数据的函数
const generateMockNotices = (type, count = 50) => {
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
        '清洁生产审核评估工作总结报告',
        '清洁生产审核评估技术标准制定',
        '清洁生产审核评估专家库管理办法',
        '清洁生产审核评估质量监督制度',
        '清洁生产审核评估工作考核办法',
        '清洁生产审核评估技术指导手册',
        '清洁生产审核评估专家评审规则',
        '清洁生产审核评估数据管理办法',
        '清洁生产审核评估成果转化机制',
        '清洁生产审核评估国际合作指南',
        '清洁生产审核评估技术发展趋势',
        '清洁生产审核评估工作创新实践',
        '清洁生产审核评估标准体系建设',
        '清洁生产审核评估专家培养计划',
        '清洁生产审核评估质量提升工程',
        '清洁生产审核评估信息化平台',
        '清洁生产审核评估技术交流平台',
        '清洁生产审核评估成果展示平台',
        '清洁生产审核评估政策研究平台',
        '清洁生产审核评估技术服务平台',
        '清洁生产审核评估专家服务平台',
        '清洁生产审核评估数据服务平台',
        '清洁生产审核评估质量服务平台',
        '清洁生产审核评估创新服务平台'
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
        '宁夏清洁生产审核评估专家选拔',
        '新疆清洁生产审核评估技术创新',
        '西藏清洁生产审核评估工作部署',
        '海南清洁生产审核评估专家库建设',
        '重庆清洁生产审核评估质量提升',
        '天津清洁生产审核评估标准制定',
        '上海清洁生产审核评估专家培训',
        '北京清洁生产审核评估工作推进',
        '贵州清洁生产审核评估质量检查',
        '云南清洁生产审核评估专家选拔',
        '广西清洁生产审核评估技术创新',
        '黑龙江清洁生产审核评估工作部署',
        '吉林清洁生产审核评估专家库建设',
        '辽宁清洁生产审核评估质量提升',
        '河北清洁生产审核评估标准制定',
        '山东清洁生产审核评估专家培训',
        '河南清洁生产审核评估工作推进',
        '湖北清洁生产审核评估质量检查',
        '湖南清洁生产审核评估专家选拔',
        '江西清洁生产审核评估技术创新',
        '安徽清洁生产审核评估工作推进',
        '江苏清洁生产审核评估专家库建设',
        '浙江清洁生产审核评估质量提升',
        '福建清洁生产审核评估标准制定',
        '广东清洁生产审核评估专家培训',
        '海南清洁生产审核评估工作推进',
        '四川清洁生产审核评估质量检查',
        '重庆清洁生产审核评估专家选拔',
        '贵州清洁生产审核评估技术创新',
        '云南清洁生产审核评估工作部署',
        '西藏清洁生产审核评估专家库建设',
        '陕西清洁生产审核评估质量提升',
        '甘肃清洁生产审核评估标准制定',
        '青海清洁生产审核评估专家培训',
        '宁夏清洁生产审核评估工作推进',
        '新疆清洁生产审核评估质量检查',
        '内蒙古清洁生产审核评估专家选拔'
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

// 模拟数据 - 生成50条用于分页测试
const notices = ref([])

// 根据类型和搜索关键词过滤通知
const filteredNotices = computed(() => {
  let result = notices.value
  
  // 按类型过滤
  if (route.params.type === 'national') {
    result = result.filter(item => !item.province)
  } else {
    result = result.filter(item => item.province)
  }
  
  // 按关键词搜索
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    result = result.filter(item => 
      item.title.toLowerCase().includes(keyword) ||
      item.source.toLowerCase().includes(keyword)
    )
  }
  
  total.value = result.length
  
  // 分页
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  
  return result.slice(start, end)
})

// 显示详情
const goToDetail = (id) => {
  currentNoticeId.value = id
  showDetailModal.value = true
}

// 搜索
const handleSearch = () => {
  currentPage.value = 1
}

// 返回按钮
const goBack = () => {
  router.push({
    name: '通知公告'
  })
}

// 监听路由参数变化
onMounted(() => {
  // 这里可以调用API获取数据
  console.log('当前类型:', route.params.type)
  
  // 根据类型生成对应的Mock数据
  const type = route.params.type
  if (type) {
    notices.value = generateMockNotices(type, 50)
  }
})
</script>

<style scoped>
.notice-list {
  padding: 16px;
}

.breadcrumb {
  background-color: #fff;
  padding: 16px;
  border-radius: 3px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.page-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.notice-title {
  color: #333;
  text-decoration: none;
  font-size: 14px;
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  line-height: 1.5;
}

.notice-title:hover {
  color: #2080f0;
}

.notice-list-item {
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.notice-list-item:last-child {
  border-bottom: none;
}

.notice-list-item:hover {
  background-color: #f8f9fa;
}

.notice-date {
  color: #999;
  font-size: 12px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.mt-4 {
  margin-top: 16px;
}

:deep(.n-breadcrumb-item a) {
  color: #666;
  text-decoration: none;
}

:deep(.n-breadcrumb-item a:hover) {
  color: #2080f0;
}
</style>