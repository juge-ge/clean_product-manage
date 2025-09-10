<template>
  <CommonPage>
    <!-- 顶部导航栏 -->
    <template #header>
      <div class="flex justify-between items-center">
        <n-breadcrumb>
          <n-breadcrumb-item @click="$router.push('/cloud-audit/pcb')">
            PCB行业审核
          </n-breadcrumb-item>
          <n-breadcrumb-item>{{ enterprise.name }}</n-breadcrumb-item>
        </n-breadcrumb>
        <n-button @click="$router.push('/cloud-audit/pcb')">
          返回列表
        </n-button>
      </div>
    </template>

    <!-- 审核进度条 -->
    <AuditProgress 
      :current-step="currentStep"
      :steps="auditSteps"
      class="mb-4"
    />
    
    <!-- 模块导航 -->
    <n-tabs 
      v-model:value="activeTab" 
      type="line"
      @update:value="handleTabChange"
    >
      <n-tab-pane name="basic-info" tab="企业信息">
        <BasicInfo 
          :enterprise-id="enterpriseId" 
          @update="handleInfoUpdate"
        />
      </n-tab-pane>
      <n-tab-pane name="planning" tab="筹划与组织">
        <Planning 
          :enterprise-id="enterpriseId"
          @update="handlePlanningUpdate"
        />
      </n-tab-pane>
      <n-tab-pane name="pre-audit" tab="预审核">
        <PreAudit 
          :enterprise-id="enterpriseId"
          @update="handlePreAuditUpdate"
        />
      </n-tab-pane>
      <n-tab-pane name="audit" tab="审核">
        <Audit 
          :enterprise-id="enterpriseId"
          @update="handleAuditUpdate"
        />
      </n-tab-pane>
      <n-tab-pane name="scheme-library" tab="方案库">
        <SchemeLibrary 
          :enterprise-id="enterpriseId"
          @update="handleSchemeUpdate"
        />
      </n-tab-pane>
      <n-tab-pane name="report" tab="审核报告">
        <Report 
          :enterprise-id="enterpriseId"
          @update="handleReportUpdate"
        />
      </n-tab-pane>
    </n-tabs>
  </CommonPage>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { NBreadcrumb, NBreadcrumbItem, NButton, NTabs, NTabPane } from 'naive-ui'
import CommonPage from '@/components/page/CommonPage.vue'
import AuditProgress from '../components/AuditProgress.vue'
import BasicInfo from './basic-info.vue'
import Planning from './planning.vue'
import PreAudit from './pre-audit.vue'
import Audit from './audit.vue'
import SchemeLibrary from './scheme-library.vue'
import Report from './report.vue'
import { mockApi } from '@/mock/pcb'
import { mockDetailApi } from '@/mock/pcb-detail'

defineOptions({ name: 'PCB企业详情' })

const route = useRoute()
const router = useRouter()
const enterpriseId = computed(() => route.params.id)
const activeTab = ref(route.path.split('/').pop() || 'basic-info')
const enterprise = ref({})
const currentStep = ref(0)

const auditSteps = [
  { title: '企业信息', description: '基本信息录入', key: 'basic-info' },
  { title: '筹划与组织', description: '审核团队组建', key: 'planning' },
  { title: '预审核', description: '数据填报评估', key: 'pre-audit' },
  { title: '审核', description: '指标审核', key: 'audit' },
  { title: '方案库', description: '整改方案', key: 'scheme-library' },
  { title: '审核报告', description: '报告生成', key: 'report' }
]

// 获取企业信息
const fetchEnterprise = async () => {
  try {
    const response = await mockApi.getEnterpriseDetail(enterpriseId.value)
    enterprise.value = response.data
    updateCurrentStep()
  } catch (error) {
    console.error('获取企业信息失败:', error)
    window.$message.error('获取企业信息失败')
  }
}

// 更新当前步骤
const updateCurrentStep = () => {
  const stepIndex = auditSteps.findIndex(step => step.key === activeTab.value)
  currentStep.value = stepIndex > -1 ? stepIndex : 0
}

// 处理标签页切换
const handleTabChange = (tab) => {
  router.push(`/cloud-audit/pcb/${enterpriseId.value}/${tab}`)
}

// 处理各模块更新
const handleInfoUpdate = async (data) => {
  try {
    await mockApi.updateEnterprise(enterpriseId.value, data)
    window.$message.success('企业信息更新成功')
    fetchEnterprise()
  } catch (error) {
    console.error('更新失败:', error)
    window.$message.error('更新失败')
  }
}

const handlePlanningUpdate = async (data) => {
  try {
    await mockDetailApi.updateAuditTeam(enterpriseId.value, data)
    window.$message.success('筹划与组织信息更新成功')
  } catch (error) {
    console.error('更新失败:', error)
    window.$message.error('更新失败')
  }
}

const handlePreAuditUpdate = async (data) => {
  try {
    await mockDetailApi.submitPreAuditData(enterpriseId.value, data)
    window.$message.success('预审核数据更新成功')
  } catch (error) {
    console.error('更新失败:', error)
    window.$message.error('更新失败')
  }
}

const handleAuditUpdate = async (data) => {
  try {
    await mockDetailApi.submitAuditResults(enterpriseId.value, data)
    window.$message.success('审核结果更新成功')
  } catch (error) {
    console.error('更新失败:', error)
    window.$message.error('更新失败')
  }
}

const handleSchemeUpdate = async (data) => {
  try {
    await mockDetailApi.updateScheme(enterpriseId.value, data.id, data)
    window.$message.success('方案更新成功')
  } catch (error) {
    console.error('更新失败:', error)
    window.$message.error('更新失败')
  }
}

const handleReportUpdate = async (data) => {
  try {
    await mockDetailApi.generateReport(enterpriseId.value, data)
    window.$message.success('报告更新成功')
  } catch (error) {
    console.error('更新失败:', error)
    window.$message.error('更新失败')
  }
}

// 监听路由变化
watch(
  () => route.path,
  () => {
    activeTab.value = route.path.split('/').pop() || 'basic-info'
    updateCurrentStep()
  }
)

onMounted(() => {
  fetchEnterprise()
})
</script>

<style scoped>
.enterprise-detail {
  min-height: 100%;
  display: flex;
  flex-direction: column;
}

:deep(.n-tabs-content) {
  flex: 1;
  padding: 16px 0;
}
</style>
