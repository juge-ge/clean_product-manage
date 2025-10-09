<template>
  <CommonPage title="PCB行业清洁生产审核">
    <!-- 企业列表视图 -->
    <div v-if="!currentEnterprise" class="enterprise-list">
      <!-- 搜索和操作栏 -->
      <div class="search-bar mb-4">
        <n-space>
          <n-input 
            v-model:value="searchKeyword" 
            placeholder="请输入企业名称/地市/区县"
            clearable
            style="width: 300px"
          />
          <n-button type="primary" @click="showCreateModal = true">
            <template #icon>
              <TheIcon icon="carbon:add" />
            </template>
            创建企业
          </n-button>
        </n-space>
      </div>
      
      <!-- 企业卡片网格 -->
      <div class="enterprise-grid">
        <EnterpriseCard 
          v-for="enterprise in enterprises"
          :key="enterprise.id"
          :enterprise="enterprise"
          @view="handleView"
          @edit="handleEdit"
          @delete="handleDelete"
        />
        </div>
      </div>
      
    <!-- 企业详情视图 -->
    <div v-else class="enterprise-detail">
      <!-- 顶部导航栏 -->
      <div class="detail-header mb-4">
        <div class="header-left">
          <n-space>
            <n-button 
              v-for="(step, index) in auditSteps"
              :key="step.key"
              :type="activeTab === step.key ? 'primary' : 'default'"
              :size="index === currentStep ? 'medium' : 'small'"
              @click="handleStepClick(step)"
              class="step-button"
            >
              <template #icon>
                <TheIcon :icon="getStepIcon(index)" />
              </template>
              {{ step.title }}
            </n-button>
          </n-space>
        </div>
        <div class="header-center">
        </div>
        <div class="header-right">
          <n-button @click="handleBack" size="small">
            <template #icon>
              <TheIcon icon="carbon:arrow-left" />
            </template>
            返回列表
          </n-button>
        </div>
      </div>
      
      <!-- 模块内容区域 -->
      <div class="content-area">
        <n-spin :show="loading">
          <keep-alive>
            <component 
              v-if="currentEnterprise && getCurrentComponent()"
              :is="getCurrentComponent()"
              :enterprise-id="currentEnterprise.id"
              :key="activeTab"
              @update="handleModuleUpdate"
              @navigate="handleModuleNavigate"
            />
          </keep-alive>
        </n-spin>
      </div>
    </div>

    <!-- 创建/编辑企业弹窗 -->
    <CrudModal
      v-model:visible="showCreateModal"
      :title="isEdit ? '编辑企业' : '创建企业'"
      @save="handleSave"
    >
      <EnterpriseForm ref="formRef" :data="currentEnterprise" />
    </CrudModal>
  </CommonPage>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { NButton, NInput, NSpace, NDivider, NSpin } from 'naive-ui'
import CommonPage from '@/components/page/CommonPage.vue'
import CrudModal from '@/components/table/CrudModal.vue'
import TheIcon from '@/components/icon/TheIcon.vue'
import EnterpriseCard from './components/EnterpriseCard.vue'
import EnterpriseForm from './components/EnterpriseForm.vue'
import AuditProgress from './components/AuditProgress.vue'
import BasicInfo from './enterprise-detail/basic-info.vue'
import Planning from './enterprise-detail/planning.vue'
import PreAudit from './enterprise-detail/pre-audit.vue'
import Audit from './enterprise-detail/audit.vue'
import SchemeLibrary from './enterprise-detail/scheme-library.vue'
import Report from './enterprise-detail/report.vue'
import { mockApi } from '@/mock/pcb'
import { mockDetailApi } from '@/mock/pcb-detail'

defineOptions({ name: 'PCB行业审核' })

const router = useRouter()
const searchKeyword = ref('')
const showCreateModal = ref(false)
const isEdit = ref(false)
const currentEnterprise = ref(null)
const enterprises = ref([])
const activeTab = ref('basic-info')
const currentStep = ref(0)
const loading = ref(false)

const auditSteps = [
  { title: '企业信息', description: '基本信息录入', key: 'basic-info' },
  { title: '筹划与组织', description: '审核团队组建', key: 'planning' },
  { title: '预审核', description: '数据填报评估', key: 'pre-audit' },
  { title: '审核', description: '指标审核', key: 'audit' },
  { title: '方案库', description: '整改方案', key: 'scheme-library' },
  { title: '审核报告', description: '报告生成', key: 'report' }
]

// 获取企业列表
const fetchEnterprises = async () => {
  try {
    const response = await mockApi.getEnterpriseList({
      search: searchKeyword.value
    })
    enterprises.value = response.data
  } catch (error) {
    console.error('获取企业列表失败:', error)
    window.$message.error('获取企业列表失败')
  }
}

// 查看企业详情
const handleView = async (id) => {
  try {
    loading.value = true
    const response = await mockApi.getEnterpriseDetail(id)
    // 等待DOM更新完成
    await nextTick()
    // 设置企业信息
    currentEnterprise.value = response.data
    activeTab.value = 'basic-info'
    currentStep.value = 0
    // 缓存状态
    cacheCurrentState()
  } catch (error) {
    console.error('获取企业详情失败:', error)
    window.$message.error('获取企业详情失败')
  } finally {
    loading.value = false
  }
}

// 返回列表
const handleBack = async () => {
  try {
    // 先清除缓存
    clearCache()
    // 重置状态
    activeTab.value = 'basic-info'
    currentStep.value = 0
    // 等待DOM更新完成
    await nextTick()
    // 重置企业信息
    currentEnterprise.value = null
    // 重新获取企业列表
    await fetchEnterprises()
  } catch (error) {
    console.error('返回列表失败:', error)
    window.$message.error('返回列表失败')
  }
}

// 处理步骤点击
const handleStepClick = (step) => {
  activeTab.value = step.key
  currentStep.value = auditSteps.findIndex(s => s.key === step.key)
}

// 获取当前组件
const getCurrentComponent = () => {
  if (!currentEnterprise.value) {
    return null
  }
  const componentMap = {
    'basic-info': BasicInfo,
    'planning': Planning,
    'pre-audit': PreAudit,
    'audit': Audit,
    'scheme-library': SchemeLibrary,
    'report': Report
  }
  return componentMap[activeTab.value] || BasicInfo
}

// 获取步骤图标
const getStepIcon = (index) => {
  const icons = [
    'carbon:document',
    'carbon:user-multiple',
    'carbon:search',
    'carbon:checkmark-filled',
    'carbon:library',
    'carbon:document-text'
  ]
  return icons[index] || 'carbon:document'
}

// 处理模块更新
const handleModuleUpdate = (data) => {
  // 根据当前模块类型调用相应的更新处理函数
  switch (activeTab.value) {
    case 'basic-info':
      handleInfoUpdate(data)
      break
    case 'planning':
      handlePlanningUpdate(data)
      break
    case 'pre-audit':
      handlePreAuditUpdate(data)
      break
    case 'audit':
      handleAuditUpdate(data)
      break
    case 'scheme-library':
      handleSchemeUpdate(data)
      break
    case 'report':
      handleReportUpdate(data)
      break
  }
}

// 处理模块导航
const handleModuleNavigate = (targetModule) => {
  activeTab.value = targetModule
  currentStep.value = auditSteps.findIndex(s => s.key === targetModule)
  cacheCurrentState()
}

// 编辑企业
const handleEdit = (enterprise) => {
  isEdit.value = true
  currentEnterprise.value = { ...enterprise }
  showCreateModal.value = true
}

// 删除企业
const handleDelete = async (id) => {
  try {
    await window.$dialog.confirm({
      title: '确认删除',
      content: '确定要删除该企业吗？此操作不可恢复。'
    })
    await mockApi.deleteEnterprise(id)
    window.$message.success('删除成功')
    fetchEnterprises()
  } catch (error) {
    if (error) {
      console.error('删除失败:', error)
      window.$message.error('删除失败')
    }
  }
}

// 保存企业
const handleSave = async () => {
  try {
    if (isEdit.value) {
      await mockApi.updateEnterprise(currentEnterprise.value.id, currentEnterprise.value)
    } else {
      await mockApi.createEnterprise(currentEnterprise.value)
    }
    window.$message.success('保存成功')
    showCreateModal.value = false
    fetchEnterprises()
  } catch (error) {
    console.error('保存失败:', error)
    window.$message.error('保存失败')
  }
}

// 处理各模块更新
const handleInfoUpdate = async (data) => {
  try {
    await mockApi.updateEnterprise(currentEnterprise.value.id, data)
    window.$message.success('企业信息更新成功')
    // 更新当前企业信息
    currentEnterprise.value = { ...currentEnterprise.value, ...data }
  } catch (error) {
    console.error('更新失败:', error)
    window.$message.error('更新失败')
  }
}

const handlePlanningUpdate = async (data) => {
  try {
    await mockDetailApi.updateAuditTeam(currentEnterprise.value.id, data)
    window.$message.success('筹划与组织信息更新成功')
  } catch (error) {
    console.error('更新失败:', error)
    window.$message.error('更新失败')
  }
}

const handlePreAuditUpdate = async (data) => {
  try {
    await mockDetailApi.submitPreAuditData(currentEnterprise.value.id, data)
    window.$message.success('预审核数据更新成功')
  } catch (error) {
    console.error('更新失败:', error)
    window.$message.error('更新失败')
  }
}

const handleAuditUpdate = async (data) => {
  try {
    await mockDetailApi.submitAuditResults(currentEnterprise.value.id, data)
    window.$message.success('审核结果更新成功')
  } catch (error) {
    console.error('更新失败:', error)
    window.$message.error('更新失败')
  }
}

const handleSchemeUpdate = async (data) => {
  try {
    await mockDetailApi.updateScheme(currentEnterprise.value.id, data.id, data)
    window.$message.success('方案更新成功')
  } catch (error) {
    console.error('更新失败:', error)
    window.$message.error('更新失败')
  }
}

const handleReportUpdate = async (data) => {
  try {
    await mockDetailApi.generateReport(currentEnterprise.value.id, data)
    window.$message.success('报告更新成功')
  } catch (error) {
    console.error('更新失败:', error)
    window.$message.error('更新失败')
  }
}

// 状态缓存管理
const cacheCurrentState = () => {
  sessionStorage.setItem('pcb_current_state', JSON.stringify({
    enterprise: currentEnterprise.value,
    tab: activeTab.value,
    step: currentStep.value
  }))
}

const restoreState = () => {
  const cached = sessionStorage.getItem('pcb_current_state')
  if (cached) {
    const state = JSON.parse(cached)
    // 只有在有企业数据且当前路由是PCB模块时才恢复状态
    if (state.enterprise && router.currentRoute.value.path.startsWith('/cloud-audit/pcb')) {
      currentEnterprise.value = state.enterprise
      activeTab.value = state.tab
      currentStep.value = state.step
    }
  }
}

const clearCache = () => {
  sessionStorage.removeItem('pcb_current_state')
}

// 监听搜索关键词变化
watch(searchKeyword, () => {
  fetchEnterprises()
})

onMounted(() => {
  fetchEnterprises()
  // 只有在路由包含企业ID时才恢复状态
  if (router.currentRoute.value.params.id) {
    restoreState()
  }
})
</script>

<style scoped>
.enterprise-list,
.enterprise-detail {
  min-height: 100%;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 0;
  border-bottom: 1px solid var(--n-border-color);
  gap: 20px;
}

.header-left {
  flex-shrink: 0;
}

.header-center {
  flex: 1;
  display: flex;
  justify-content: center;
}

.header-center h3 {
  margin: 0;
  font-size: 18px;
  color: var(--n-text-color);
  font-weight: 600;
}

.header-right {
  flex-shrink: 0;
}

.step-button {
  transition: all 0.3s ease;
}

.step-button:hover {
  transform: translateY(-1px);
}

.content-area {
  padding: 16px 0;
  min-height: 500px;
}

.enterprise-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .detail-header {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .header-center {
    order: 1;
  }
  
  .header-left {
    order: 2;
    text-align: center;
  }
  
  .header-right {
    order: 3;
    text-align: center;
  }
}

@media (max-width: 768px) {
  .header-center :deep(.n-space) {
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .step-button {
    font-size: 12px;
  }
}
</style>