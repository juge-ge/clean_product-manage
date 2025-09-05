<template>
  <div class="dynamic-container">
    <!-- 首页模式 -->
    <div v-if="displayMode === 'home'">
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

      <!-- 三栏布局 -->
      <div class="dynamic-grid mt-4">
        <!-- 国内动态 -->
        <div class="dynamic-column">
          <n-card :bordered="false" class="dynamic-card">
            <template #header>
              <div class="card-header">
                <span class="header-title">国内动态</span>
                <n-button text type="primary" @click="goToList('domestic')" class="header-action">
                  查看更多 <n-icon><i class="mdi" :class="arrowRightIcon" /></n-icon>
                </n-button>
              </div>
            </template>
            <n-list hoverable clickable>
              <n-list-item v-for="item in domesticDynamics.slice(0, 3)" :key="item.id">
                <div class="dynamic-item">
                  <div class="title-section">
                    <a href="javascript:;" @click="goToDetail(item.id)" class="dynamic-title">
                      {{ item.title }}
                    </a>
                    <n-tag size="small" type="info" class="source-tag">{{ item.source }}</n-tag>
                  </div>
                  <span class="dynamic-date">{{ item.publishDate }}</span>
                </div>
              </n-list-item>
            </n-list>
          </n-card>
        </div>

        <!-- 省内动态 -->
        <div class="dynamic-column">
          <n-card :bordered="false" class="dynamic-card">
            <template #header>
              <div class="card-header">
                <span class="header-title">省内动态</span>
                <n-button text type="primary" @click="goToList('provincial')" class="header-action">
                  查看更多 <n-icon><i class="mdi" :class="arrowRightIcon" /></n-icon>
                </n-button>
              </div>
            </template>
            <n-list hoverable clickable>
              <n-list-item v-for="item in provincialDynamics.slice(0, 3)" :key="item.id">
                <div class="dynamic-item">
                  <div class="title-section">
                    <a href="javascript:;" @click="goToDetail(item.id)" class="dynamic-title">
                      {{ item.title }}
                    </a>
                    <n-tag size="small" type="success" class="province-tag">{{ item.province }}</n-tag>
                  </div>
                  <span class="dynamic-date">{{ item.publishDate }}</span>
                </div>
              </n-list-item>
            </n-list>
          </n-card>
        </div>

        <!-- 国外动态 -->
        <div class="international-column">
          <n-card :bordered="false" class="dynamic-card">
            <template #header>
              <div class="card-header">
                <span class="header-title">国外动态</span>
                <n-button text type="primary" @click="goToList('international')" class="header-action">
                  查看更多 <n-icon><i class="mdi" :class="arrowRightIcon" /></n-icon>
                </n-button>
              </div>
            </template>
            <n-list hoverable clickable>
              <n-list-item v-for="item in internationalDynamics.slice(0, 3)" :key="item.id">
                <div class="dynamic-item">
                  <div class="title-section">
                    <a href="javascript:;" @click="goToDetail(item.id)" class="dynamic-title">
                      {{ item.title }}
                    </a>
                    <n-tag size="small" type="warning" class="country-tag">{{ item.country }}</n-tag>
                  </div>
                  <span class="dynamic-date">{{ item.publishDate }}</span>
                </div>
              </n-list-item>
            </n-list>
          </n-card>
        </div>
      </div>
    </div>

    <!-- 列表模式 -->
    <div v-else-if="displayMode === 'list'">
      <!-- 列表内容 -->
      <n-card class="mt-2">
        <template #header>
          <n-space justify="space-between" align="center">
            <n-space align="center">
              <span class="page-title">{{ getListTitle() }}</span>
              <n-button 
                type="primary" 
                ghost 
                size="small" 
                @click="goHome"
                style="margin-left: 16px"
              >
                返回动态信息
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
          <n-list-item v-for="item in getFilteredDynamics()" :key="item.id">
            <div class="dynamic-item">
              <div class="title-section">
                <a href="javascript:;" @click="goToDetail(item.id)" class="dynamic-title">
                  {{ item.title }}
                </a>
                <template v-if="item.province">
                  <n-tag size="small" type="success" class="province-tag">{{ item.province }}</n-tag>
                </template>
                <template v-else-if="item.country">
                  <n-tag size="small" type="warning" class="country-tag">{{ item.country }}</n-tag>
                </template>
                <template v-else>
                  <n-tag size="small" type="info" class="source-tag">{{ item.source }}</n-tag>
                </template>
              </div>
              <span class="dynamic-date">{{ item.publishDate }}</span>
            </div>
          </n-list-item>
        </n-list>

        <!-- 分页 -->
        <div class="pagination-wrapper">
          <div class="pagination-content">
            <span class="total-count">共{{ getTotalCount() }}条</span>
            <n-pagination
              v-model:page="currentPage"
              :page-size="pageSize"
              :item-count="getTotalCount()"
              show-quick-jumper
              show-size-picker
              :page-sizes="[10, 20, 30, 50]"
              :page-count="Math.ceil(getTotalCount() / pageSize)"
              class="custom-pagination"
            />
          </div>
        </div>
      </n-card>
    </div>

    <!-- 详情弹窗 -->
    <dynamic-detail-modal
      v-model:show="showDetailModal"
      :dynamic-id="currentDynamicId"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { usePermissionStore } from '@/store'
import DynamicDetailModal from './components/DynamicDetailModal.vue'

// 使用项目自带的图标
const arrowRightIcon = 'mdi-arrow-right'

const router = useRouter()
const searchKeyword = ref('')

// 生成Mock数据的函数
const generateMockDynamics = (type, count = 20) => {
  const dynamics = []
  
  let titles, sources, provinces, countries
  
  if (type === 'domestic') {
    titles = [
      '工信部发布绿色制造名单，推动产业绿色发展',
      '生态环境部推进清洁生产审核评估工作',
      '国家发改委发布循环经济发展规划',
      '科技部支持清洁生产技术研发创新',
      '财政部设立绿色发展专项资金',
      '农业农村部推广农业清洁生产技术',
      '商务部推进绿色供应链建设',
      '应急管理部加强环保安全管理',
      '教育部培养清洁生产专业人才',
      '交通运输部推广绿色交通技术',
      '住建部推进绿色建筑发展',
      '水利部加强水资源清洁利用',
      '自然资源部推进绿色矿山建设',
      '文旅部发展生态旅游产业',
      '卫健委推进医疗废物清洁处理',
      '市场监管总局加强环保产品监管',
      '税务总局实施环保税收优惠',
      '人民银行支持绿色金融发展',
      '银保监会推进绿色保险创新',
      '证监会支持绿色债券发行'
    ]
    sources = ['工信部', '生态环境部', '国家发改委', '科技部', '财政部', '农业农村部', '商务部', '应急管理部', '教育部', '交通运输部']
  } else if (type === 'provincial') {
    titles = [
      '江苏省启动清洁生产技术改造专项行动',
      '浙江省推进绿色制造体系建设',
      '广东省实施清洁生产审核评估',
      '山东省建设清洁生产示范园区',
      '河南省推进工业绿色化改造',
      '四川省发展清洁能源产业',
      '湖北省建设绿色制造基地',
      '福建省推进清洁生产技术创新',
      '安徽省实施清洁生产审核',
      '江西省建设绿色工业园区',
      '河北省推进清洁生产评估',
      '山西省发展清洁煤炭技术',
      '内蒙古推进清洁能源利用',
      '辽宁省建设绿色制造体系',
      '吉林省发展清洁农业',
      '黑龙江省推进清洁生产',
      '陕西省建设清洁能源基地',
      '甘肃省推进清洁生产',
      '青海省发展清洁能源',
      '宁夏推进清洁生产'
    ]
    provinces = ['江苏省', '浙江省', '广东省', '山东省', '河南省', '四川省', '湖北省', '福建省', '安徽省', '江西省', '河北省', '山西省', '内蒙古', '辽宁省', '吉林省', '黑龙江省', '陕西省', '甘肃省', '青海省', '宁夏']
  } else if (type === 'international') {
    titles = [
      '欧盟发布新版生态设计指令，助力循环经济发展',
      '美国推进清洁能源技术创新',
      '日本实施绿色增长战略',
      '德国推进工业4.0绿色发展',
      '法国发布碳中和路线图',
      '英国推进绿色金融发展',
      '加拿大实施清洁技术计划',
      '澳大利亚推进清洁能源转型',
      '韩国发布绿色新政',
      '新加坡建设智慧绿色城市',
      '印度推进清洁能源发展',
      '巴西实施绿色经济计划',
      '俄罗斯推进清洁技术应用',
      '南非发展清洁能源产业',
      '墨西哥推进绿色制造',
      '土耳其实施清洁生产',
      '埃及推进清洁能源',
      '沙特推进绿色转型',
      '阿联酋建设绿色城市',
      '以色列发展清洁技术'
    ]
    countries = ['欧盟', '美国', '日本', '德国', '法国', '英国', '加拿大', '澳大利亚', '韩国', '新加坡', '印度', '巴西', '俄罗斯', '南非', '墨西哥', '土耳其', '埃及', '沙特', '阿联酋', '以色列']
  }
  
  for (let i = 0; i < count; i++) {
    const randomMonth = Math.floor(Math.random() * 12) + 1
    const randomDay = Math.floor(Math.random() * 28) + 1
    
    if (type === 'domestic') {
      const randomSource = sources[Math.floor(Math.random() * sources.length)]
      dynamics.push({
        id: i + 1,
        title: titles[i],
        publishDate: `2025-${String(randomMonth).padStart(2, '0')}-${String(randomDay).padStart(2, '0')}`,
        source: randomSource,
        type: 'domestic'
      })
    } else if (type === 'provincial') {
      const randomProvince = provinces[Math.floor(Math.random() * provinces.length)]
      dynamics.push({
        id: i + 101,
        title: titles[i],
        publishDate: `2025-${String(randomMonth).padStart(2, '0')}-${String(randomDay).padStart(2, '0')}`,
        province: randomProvince,
        type: 'provincial'
      })
    } else if (type === 'international') {
      const randomCountry = countries[Math.floor(Math.random() * countries.length)]
      dynamics.push({
        id: i + 201,
        title: titles[i],
        publishDate: `2025-${String(randomMonth).padStart(2, '0')}-${String(randomDay).padStart(2, '0')}`,
        country: randomCountry,
        type: 'international'
      })
    }
  }
  
  // 按日期排序，最新的在前面
  return dynamics.sort((a, b) => new Date(b.publishDate) - new Date(a.publishDate))
}

// 生成Mock数据 - 各20条
const domesticDynamics = ref(generateMockDynamics('domestic', 20))
const provincialDynamics = ref(generateMockDynamics('provincial', 20))
const internationalDynamics = ref(generateMockDynamics('international', 20))

// 显示详情弹窗
const showDetailModal = ref(false)
const currentDynamicId = ref(null)

// 控制显示模式：'home' 为首页，'list' 为列表页
const displayMode = ref('home')
const currentListType = ref('') // 当前显示的类型：'domestic'、'provincial'、'international'

// 分页相关
const currentPage = ref(1)
const pageSize = ref(10)

const goToDetail = (id) => {
  currentDynamicId.value = id
  showDetailModal.value = true
}

// 切换到列表显示模式
const goToList = (type) => {
  console.log('切换到列表模式:', type)
  currentListType.value = type
  displayMode.value = 'list'
  currentPage.value = 1 // 重置分页
}

// 搜索处理
const handleSearch = () => {
  if (searchKeyword.value.trim()) {
    console.log('搜索关键词:', searchKeyword.value)
    currentListType.value = 'search'
    displayMode.value = 'list'
    currentPage.value = 1 // 重置分页
  }
}

// 返回首页
const goHome = () => {
  displayMode.value = 'home'
  currentListType.value = ''
  searchKeyword.value = ''
  currentPage.value = 1
}

// 获取列表标题
const getListTitle = () => {
  if (currentListType.value === 'domestic') return '国内动态'
  if (currentListType.value === 'provincial') return '省内动态'
  if (currentListType.value === 'international') return '国外动态'
  if (currentListType.value === 'search') return '搜索结果'
  return '动态列表'
}

// 获取过滤后的动态列表
const getFilteredDynamics = () => {
  let dynamics = []
  
  if (currentListType.value === 'domestic') {
    dynamics = domesticDynamics.value
  } else if (currentListType.value === 'provincial') {
    dynamics = provincialDynamics.value
  } else if (currentListType.value === 'international') {
    dynamics = internationalDynamics.value
  } else if (currentListType.value === 'search') {
    // 搜索逻辑：合并所有动态并过滤
    const allDynamics = [...domesticDynamics.value, ...provincialDynamics.value, ...internationalDynamics.value]
    const keyword = searchKeyword.value.toLowerCase()
    dynamics = allDynamics.filter(item => 
      item.title.toLowerCase().includes(keyword) ||
      (item.source && item.source.toLowerCase().includes(keyword)) ||
      (item.province && item.province.toLowerCase().includes(keyword)) ||
      (item.country && item.country.toLowerCase().includes(keyword))
    )
  }
  
  // 分页处理
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return dynamics.slice(start, end)
}

// 获取总数
const getTotalCount = () => {
  if (currentListType.value === 'domestic') return domesticDynamics.value.length
  if (currentListType.value === 'provincial') return provincialDynamics.value.length
  if (currentListType.value === 'international') return internationalDynamics.value.length
  if (currentListType.value === 'search') {
    const allDynamics = [...domesticDynamics.value, ...provincialDynamics.value, ...internationalDynamics.value]
    const keyword = searchKeyword.value.toLowerCase()
    return allDynamics.filter(item => 
      item.title.toLowerCase().includes(keyword) ||
      (item.source && item.source.toLowerCase().includes(keyword)) ||
      (item.province && item.province.toLowerCase().includes(keyword)) ||
      (item.country && item.country.toLowerCase().includes(keyword))
    ).length
  }
  return 0
}
</script>

<style lang="scss" scoped>
.dynamic-container {
  padding: 12px;
  min-height: calc(100vh - 200px);  // 充分利用页面高度
}

.search-wrapper {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 12px;
}

.search-input :deep(.n-input__placeholder) {
  display: flex;
  align-items: center;
  justify-content: center;
}

.mt-4 {
  margin-top: 16px;
}

.mt-2 {
  margin-top: 8px;
}

/* 三栏布局样式 */
.dynamic-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;     // 上面两栏等宽
  grid-template-rows: auto auto;      // 两行
  gap: 12px;
  
  .dynamic-column {
    // 国内和省内动态列
  }
  
  .international-column {
    grid-column: 1;                   // 国外动态放在左列
    grid-row: 2;                      // 第二行
    margin: 0;                        // 不居中，靠左对齐
  }
}

.dynamic-card {
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 4px;  // 从8px减少到4px
  border-bottom: 2px solid var(--primary-color);
  margin-bottom: 4px;   // 从8px减少到4px
  position: relative;
  
  &::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    right: 0;
    height: 2px;
    background-color: var(--primary-color);
  }
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

/* 动态项样式 */
.dynamic-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  gap: 12px;
  min-height: 40px;  // 增加最小高度，充分利用空间
}

.title-section {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  min-height: 40px;  // 与动态项高度保持一致
  align-items: center;  // 垂直居中对齐
}

.dynamic-title {
  color: #333;
  text-decoration: none;
  font-size: 14px;
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  line-height: 1.4;
}

.dynamic-title:hover {
  color: #2080f0;
}

.source-tag, .province-tag, .country-tag {
  flex-shrink: 0;
  font-size: 11px;
  padding: 2px 6px;
}

.dynamic-date {
  flex-shrink: 0;
  min-width: 80px;
  text-align: right;
  font-size: 11px;
  color: #999;
  margin-left: auto;  // 确保时间始终在最右边
}

/* 列表模式样式 */
.page-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

/* 分页样式 */
.pagination-wrapper {
  margin-top: 12px;
  padding: 12px 0;
  border-top: 1px solid #e5e5e5;
}

.pagination-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.total-count {
  font-size: 14px;
  color: #666;
  font-weight: 500;
  flex-shrink: 0;
}

.pagination {
  display: flex;
  justify-content: center;
}

/* 分页组件样式优化 */
:deep(.n-pagination) {
  font-size: 13px;
}

:deep(.n-pagination-item) {
  min-width: 28px;
  height: 28px;
}

:deep(.n-pagination-item__content) {
  padding: 0 6px;
}

/* 列表项样式优化 */
:deep(.n-list-item) {
  padding: 4px 0;  // 从6px减少到4px，减少上下间距
}

:deep(.n-list-item:first-child) {
  padding-top: 2px;  // 第一个列表项的上边距更小
}

:deep(.n-thing-main) {
  padding: 2px 0;
}

:deep(.n-thing-header) {
  margin-bottom: 4px;
}

:deep(.n-tag) {
  font-size: 11px;
  padding: 2px 6px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .dynamic-grid {
    grid-template-columns: 1fr;
    grid-template-rows: auto auto auto;
    
    .international-column {
      grid-column: 1;
    }
  }
  
  .dynamic-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .dynamic-date {
    text-align: left;
  }
}
</style>
