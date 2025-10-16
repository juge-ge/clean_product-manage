<template>
  <CommonPage title="钢铁行业清洁生产审核">
    <template #header>
      <div class="flex justify-between items-center">
        <div></div>
        <n-button @click="$router.push('/cloud-audit/steel')">
          返回列表
        </n-button>
      </div>
    </template>

    <AuditProgress 
      :current-step="currentStep"
      :steps="auditSteps"
      class="mb-4"
    />
    
    <n-tabs 
      v-model:value="activeTab" 
      type="line"
      @update:value="handleTabChange"
    >
      <n-tab-pane name="basic-info" tab="企业信息">
        <BasicInfo 
          v-if="enterpriseId"
          :enterprise-id="enterpriseId"
          :enterprise="enterprise"
          @update="handleInfoUpdate"
        />
        <div v-else class="loading-placeholder">
          <n-spin size="large" />
        </div>
      </n-tab-pane>
      <n-tab-pane name="planning" tab="筹划与组织">
        <Planning 
          v-if="enterpriseId"
          :enterprise-id="enterpriseId"
          @update="handlePlanningUpdate"
        />
        <div v-else class="loading-placeholder">
          <n-spin size="large" />
        </div>
      </n-tab-pane>
      <n-tab-pane name="pre-audit" tab="预审核">
        <PreAudit 
          v-if="enterpriseId"
          :enterprise-id="enterpriseId"
          @update="handlePreAuditUpdate"
        />
        <div v-else class="loading-placeholder">
          <n-spin size="large" />
        </div>
      </n-tab-pane>
      <n-tab-pane name="audit" tab="审核">
        <Audit 
          v-if="enterpriseId"
          :enterprise-id="enterpriseId"
          @update="handleAuditUpdate"
        />
        <div v-else class="loading-placeholder">
          <n-spin size="large" />
        </div>
      </n-tab-pane>
      <n-tab-pane name="scheme-library" tab="方案库">
        <SchemeLibrary 
          v-if="enterpriseId"
          :enterprise-id="enterpriseId"
          @update="handleSchemeUpdate"
        />
        <div v-else class="loading-placeholder">
          <n-spin size="large" />
        </div>
      </n-tab-pane>
      <n-tab-pane name="report" tab="审核报告">
        <Report 
          v-if="enterpriseId"
          :enterprise-id="enterpriseId"
          @update="handleReportUpdate"
        />
        <div v-else class="loading-placeholder">
          <n-spin size="large" />
        </div>
      </n-tab-pane>
    </n-tabs>
  </CommonPage>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { NButton, NBreadcrumb, NBreadcrumbItem, NTabs, NTabPane, NSpin, useMessage } from 'naive-ui'
import CommonPage from '@/components/page/CommonPage.vue'
import AuditProgress from '../components/AuditProgress.vue'
import BasicInfo from './basic-info.vue'
import Planning from './planning.vue'
import PreAudit from './pre-audit.vue'
import Audit from './audit.vue'
import SchemeLibrary from './scheme-library.vue'
import Report from './report.vue'
import { mockApi } from '@/mock/steel'

const route = useRoute()
const router = useRouter()
const message = useMessage()

const enterprise = ref(null)
const currentStep = ref(0)
const activeTab = ref('basic-info')

const enterpriseId = computed(() => route.params.id)

const auditSteps = ref([
  {
    key: 'basic-info',
    title: '企业信息',
    icon: 'carbon:enterprise'
  },
  {
    key: 'planning',
    title: '筹划组织',
    icon: 'carbon:plan'
  },
  {
    key: 'pre-audit',
    title: '预审核',
    icon: 'carbon:document-attachment'
  },
  {
    key: 'audit',
    title: '审核',
    icon: 'carbon:checkmark-filled'
  },
  {
    key: 'scheme-library',
    title: '方案库',
    icon: 'carbon:library'
  },
  {
    key: 'report',
    title: '报告',
    icon: 'carbon:document'
  }
])

const loadEnterpriseDetail = async () => {
  console.log('企业ID:', enterpriseId.value)
  if (!enterpriseId.value) {
    console.error('企业ID为空')
    message.error('企业ID不能为空')
    return
  }
  
  try {
    console.log('开始加载企业详情，ID:', enterpriseId.value)
    const response = await mockApi.getEnterpriseDetail(enterpriseId.value)
    console.log('企业详情响应:', response)
    enterprise.value = response.data
    console.log('企业数据:', enterprise.value)
  } catch (error) {
    console.error('加载企业详情失败:', error)
    message.error('加载企业详情失败')
  }
}

const handleTabChange = (value) => {
  activeTab.value = value
  currentStep.value = auditSteps.value.findIndex(s => s.key === value)
}

const handleInfoUpdate = (data) => {
  console.log('企业信息更新:', data)
  message.success('企业信息保存成功')
}

const handlePlanningUpdate = (data) => {
  console.log('筹划组织更新:', data)
  message.success('筹划组织信息保存成功')
}

const handlePreAuditUpdate = (data) => {
  console.log('预审核更新:', data)
  message.success('预审核信息保存成功')
}

const handleAuditUpdate = (data) => {
  console.log('审核更新:', data)
  message.success('审核信息保存成功')
}

const handleSchemeUpdate = (data) => {
  console.log('方案库更新:', data)
  message.success('方案库信息保存成功')
}

const handleReportUpdate = (data) => {
  console.log('报告更新:', data)
  message.success('报告保存成功')
}

watch(() => route.params.id, (newId) => {
  if (newId) {
    loadEnterpriseDetail()
  }
}, { immediate: true })

onMounted(() => {
  loadEnterpriseDetail()
})
</script>

<style scoped>
.loading-placeholder {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}
</style>
