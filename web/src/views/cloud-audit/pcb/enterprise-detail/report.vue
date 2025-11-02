<template>
  <div class="report-container">
    <!-- 顶部操作栏 -->
    <n-card class="mb-4" :bordered="false" shadow="hover">
      <template #header>
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <TheIcon icon="carbon:document-attachment" size="24" class="text-primary" />
            <div>
              <h3 class="text-lg font-semibold m-0">PCB企业清洁生产审核评估报告</h3>
              <p class="text-gray-500 text-sm m-0 mt-1">{{ enterpriseData?.name || '企业名称' }}</p>
            </div>
          </div>
        <n-space>
            <n-button 
              type="primary" 
              @click="handleGenerateReport"
              :loading="generating"
              :disabled="!canGenerate"
            >
              <template #icon>
                <TheIcon icon="carbon:document-add" />
              </template>
              生成报告
            </n-button>
            <n-button 
              @click="handlePreview"
              :disabled="!reportGenerated"
              secondary
            >
              <template #icon>
                <TheIcon icon="carbon:view" />
              </template>
              预览报告
            </n-button>
            <n-button 
              type="success" 
              @click="handleExportWord"
              :loading="exporting"
              :disabled="!reportGenerated"
            >
              <template #icon>
                <TheIcon icon="carbon:download" />
              </template>
              导出Word
            </n-button>
        </n-space>
        </div>
      </template>
    </n-card>

    <!-- 报告内容区域 -->
    <n-card v-if="reportGenerated && previewMode" class="mb-4 report-preview-card" :bordered="false">
      <template #header>
        <div class="flex items-center justify-between">
          <span class="font-semibold">报告预览</span>
          <n-button quaternary @click="previewMode = false" size="small">
            <template #icon>
              <TheIcon icon="carbon:close" />
            </template>
          </n-button>
        </div>
      </template>
      <div class="report-content" v-html="previewContent"></div>
    </n-card>

    <!-- 报告生成状态和配置 -->
    <n-grid :cols="24" :x-gap="16" class="mb-4">
      <!-- 左侧：报告内容结构 -->
      <n-gi :span="16">
        <n-card title="报告内容结构" :bordered="false" shadow="hover">
          <template #header-extra>
            <n-switch v-model:value="autoGenerate" size="small">
              <template #checked>自动生成</template>
              <template #unchecked>手动编辑</template>
            </n-switch>
          </template>
          
          <n-steps :current="currentStep" vertical>
            <n-step
              title="企业信息"
              description="企业基本信息和概况"
              :status="getStepStatus(0)"
            >
              <template #icon>
                <TheIcon icon="carbon:enterprise" />
              </template>
            </n-step>
            <n-step
              title="筹划与组织"
              description="领导团队、工作团队、工作计划等"
              :status="getStepStatus(1)"
            >
              <template #icon>
                <TheIcon icon="carbon:group" />
              </template>
            </n-step>
            <n-step
              title="预审核"
              description="生产情况、原辅材料、工艺装备等"
              :status="getStepStatus(2)"
            >
              <template #icon>
                <TheIcon icon="carbon:document-view" />
              </template>
            </n-step>
            <n-step
              title="审核"
              description="64项指标审核结果和评估"
              :status="getStepStatus(3)"
            >
              <template #icon>
                <TheIcon icon="carbon:checkmark-outline" />
              </template>
            </n-step>
            <n-step
              title="问题及清洁生产方案"
              description="问题清单、方案库、权重计分等"
              :status="getStepStatus(4)"
            >
              <template #icon>
                <TheIcon icon="carbon:idea" />
              </template>
            </n-step>
          </n-steps>

          <!-- 各模块数据状态 -->
          <n-divider />
          <div class="data-status">
            <div class="status-item" v-for="(item, index) in reportSections" :key="index">
              <div class="flex items-center justify-between mb-2">
                <span class="font-medium">{{ item.title }}</span>
                <n-tag :type="item.hasData ? 'success' : 'warning'" size="small">
                  {{ item.hasData ? '数据已就绪' : '数据缺失' }}
                </n-tag>
              </div>
              <n-progress 
                :percentage="item.hasData ? 100 : 0" 
                :status="item.hasData ? 'success' : 'default'"
                :show-indicator="false"
                style="height: 4px"
              />
            </div>
          </div>
        </n-card>
      </n-gi>

      <!-- 右侧：报告统计和配置 -->
      <n-gi :span="8">
        <n-card title="报告统计" :bordered="false" shadow="hover" class="mb-4">
          <n-statistic label="报告状态" class="mb-4">
            <n-tag :type="reportStatusType" size="large">{{ reportStatusText }}</n-tag>
          </n-statistic>
          <n-statistic label="生成时间" :value="reportGeneratedAt || '未生成'" />
          <n-divider />
          <n-statistic label="数据完整度" :value="dataCompleteness + '%'" />
          <n-progress 
            :percentage="dataCompleteness" 
            :status="dataCompleteness >= 80 ? 'success' : dataCompleteness >= 50 ? 'warning' : 'error'"
            :show-indicator="true"
          />
        </n-card>

        <n-card title="报告配置" :bordered="false" shadow="hover">
          <n-space vertical>
            <n-switch v-model:value="includeTables">
              <template #checked>包含详细表格</template>
              <template #unchecked>仅包含摘要</template>
            </n-switch>
            <n-switch v-model:value="includeCharts">
              <template #checked>包含图表</template>
              <template #unchecked>仅文本</template>
            </n-switch>
            <n-switch v-model:value="includeRecommendations">
              <template #checked>包含改进建议</template>
              <template #unchecked>仅数据</template>
            </n-switch>
          </n-space>
        </n-card>
      </n-gi>
    </n-grid>

    <!-- 报告生成进度（模态框） -->
    <n-modal
      v-model:show="showGenerateModal"
      preset="dialog"
      title="生成报告"
      positive-text="确认生成"
      negative-text="取消"
      @positive-click="confirmGenerate"
    >
      <n-space vertical>
        <n-alert type="info" title="报告生成说明">
          系统将自动收集以下模块的数据并生成完整的审核报告：
        </n-alert>
        <n-checkbox-group v-model:value="selectedSections">
          <n-space vertical>
            <n-checkbox value="enterprise" label="企业信息" :disabled="true" checked />
            <n-checkbox value="planning" label="筹划与组织" />
            <n-checkbox value="preaudit" label="预审核" />
            <n-checkbox value="audit" label="审核" />
            <n-checkbox value="problem" label="问题及清洁生产方案" />
          </n-space>
        </n-checkbox-group>
      </n-space>
    </n-modal>

    <!-- 报告预览模态框 -->
    <n-modal
      v-model:show="showPreviewModal"
      preset="card"
      title="报告预览"
      style="width: 90vw; max-width: 1200px"
      :bordered="false"
    >
      <div class="report-preview-content" v-html="previewContent"></div>
      <template #footer>
        <n-space justify="end">
          <n-button @click="showPreviewModal = false">关闭</n-button>
          <n-button type="primary" @click="handleExportWord">
            <template #icon>
              <TheIcon icon="carbon:download" />
            </template>
            导出Word
          </n-button>
        </n-space>
      </template>
    </n-modal>

    <!-- 模块导航 -->
    <div class="module-navigation mt-4">
      <n-space justify="space-between">
        <n-button @click="goToPrevious">
          <template #icon>
            <TheIcon icon="carbon:arrow-left" />
          </template>
          问题及清洁生产方案
        </n-button>
        <n-button disabled>
          审核报告
          <template #icon>
            <TheIcon icon="carbon:arrow-right" />
          </template>
        </n-button>
      </n-space>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import {
  NCard,
  NButton,
  NSpace,
  NGrid,
  NGi,
  NSteps,
  NStep,
  NDivider,
  NStatistic,
  NTag,
  NProgress,
  NSwitch,
  NModal,
  NAlert,
  NCheckboxGroup,
  NCheckbox
} from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'
import api from '@/api'
import { getToken } from '@/utils/auth/token'

defineOptions({ name: 'PCB审核报告' })

const props = defineProps({
  enterpriseId: {
    type: [String, Number],
    required: true
  }
})

const emit = defineEmits(['update', 'navigate'])

// 状态管理
const generating = ref(false)
const exporting = ref(false)
const reportGenerated = ref(false)
const previewMode = ref(false)
const showGenerateModal = ref(false)
const showPreviewModal = ref(false)
const autoGenerate = ref(true)
const reportGeneratedAt = ref(null)
const previewContent = ref('')

// 报告配置
const includeTables = ref(true)
const includeCharts = ref(true)
const includeRecommendations = ref(true)
const selectedSections = ref(['enterprise', 'planning', 'preaudit', 'audit', 'problem'])

// 数据状态
const enterpriseData = ref({})
const reportSections = ref([
  { title: '企业信息', hasData: false },
  { title: '筹划与组织', hasData: false },
  { title: '预审核', hasData: false },
  { title: '审核', hasData: false },
  { title: '问题及清洁生产方案', hasData: false }
])

const currentStep = computed(() => {
  let step = 0
  reportSections.value.forEach((section, index) => {
    if (section.hasData) {
      step = Math.max(step, index + 1)
    }
  })
  return step
})

const canGenerate = computed(() => {
  return reportSections.value.some(s => s.hasData)
})

const reportStatusText = computed(() => {
  if (!reportGenerated.value) return '未生成'
  return '已生成'
})

const reportStatusType = computed(() => {
  return reportGenerated.value ? 'success' : 'default'
})

const dataCompleteness = computed(() => {
  const total = reportSections.value.length
  const completed = reportSections.value.filter(s => s.hasData).length
  return Math.round((completed / total) * 100)
})

// 获取步骤状态
const getStepStatus = (index) => {
  if (!reportGenerated.value) {
    return reportSections.value[index].hasData ? 'process' : 'wait'
  }
  return 'finish'
}

// 获取报告数据
const fetchReportData = async () => {
  try {
    // 获取企业信息
    const enterpriseResponse = await api.pcb.enterprise.getDetail(props.enterpriseId)
    enterpriseData.value = enterpriseResponse.data || {}
    reportSections.value[0].hasData = !!enterpriseData.value.name

    // 获取报告预览数据
    const previewResponse = await api.pcb.report.getPreview(props.enterpriseId)
    const previewData = previewResponse.data || {}
    
    // 更新各模块数据状态
    reportSections.value[1].hasData = previewData.planning_organization?.work_team_count > 0
    reportSections.value[2].hasData = previewData.pre_audit_data?.has_data || false
    reportSections.value[3].hasData = previewData.audit_results?.total_indicators > 0
    
    // 检查问题及清洁生产方案数据（需要单独获取）
    try {
      const problemResponse = await api.pcb.problemSolution.getIssues(props.enterpriseId)
      reportSections.value[4].hasData = (problemResponse.data || []).length > 0
    } catch (e) {
      console.warn('获取问题及清洁生产方案数据失败:', e)
    }

    // 检查是否已有生成的报告（通过尝试预览来检查）
    // 注意：报告是动态生成的Word文件，不需要检查数据库记录
    // 报告生成状态由generateReport API返回的文件路径确定
    // 这里不检查，让用户自己生成报告
  } catch (error) {
    console.error('获取报告数据失败:', error)
    window.$message.error('获取报告数据失败')
  }
}

// 生成报告
const handleGenerateReport = () => {
  if (!canGenerate.value) {
    window.$message.warning('请先完成相关模块的数据填写')
    return
  }
  showGenerateModal.value = true
}

const confirmGenerate = async () => {
  try {
    generating.value = true
    showGenerateModal.value = false

    // 调用生成报告API
    const response = await api.pcb.report.generateReport(props.enterpriseId, {
      sections: selectedSections.value,
      include_tables: includeTables.value,
      include_charts: includeCharts.value,
      include_recommendations: includeRecommendations.value
    })

    if (response.code === 200) {
      reportGenerated.value = true
      reportGeneratedAt.value = new Date().toLocaleString()
      window.$message.success('报告生成成功')
      
      // 获取报告预览内容
      await fetchPreviewContent()
    } else {
      window.$message.error(response.msg || '报告生成失败')
    }
  } catch (error) {
    console.error('生成报告失败:', error)
    window.$message.error('生成报告失败: ' + (error.message || '未知错误'))
  } finally {
    generating.value = false
  }
}

// 获取预览内容
const fetchPreviewContent = async () => {
  try {
    const response = await api.pcb.report.getPreview(props.enterpriseId)
    const previewData = response.data || {}
    
    // 构建预览HTML内容
    previewContent.value = buildPreviewHTML(previewData)
  } catch (error) {
    console.error('获取预览内容失败:', error)
    previewContent.value = '<p>预览内容加载失败</p>'
  }
}

// 构建预览HTML
const buildPreviewHTML = (data) => {
  if (!data) return '<p>暂无预览内容</p>'
  
  let html = '<div class="report-preview">'
  html += '<h1 style="text-align: center; margin-bottom: 30px;">PCB企业清洁生产审核评估报告</h1>'
  
  // 1. 企业信息
  if (data.enterprise_info) {
    html += '<h2>一、企业基本信息</h2>'
    html += '<table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">'
    html += '<tr><td style="width: 150px; padding: 8px; border: 1px solid #ddd; background: #f5f5f5; font-weight: bold;">企业名称</td><td style="padding: 8px; border: 1px solid #ddd;">' + (data.enterprise_info.name || '未填写') + '</td></tr>'
    html += '<tr><td style="padding: 8px; border: 1px solid #ddd; background: #f5f5f5; font-weight: bold;">统一社会信用代码</td><td style="padding: 8px; border: 1px solid #ddd;">' + (data.enterprise_info.unified_social_credit_code || '未填写') + '</td></tr>'
    html += '<tr><td style="padding: 8px; border: 1px solid #ddd; background: #f5f5f5; font-weight: bold;">所属地区</td><td style="padding: 8px; border: 1px solid #ddd;">' + (data.enterprise_info.region || '') + ' ' + (data.enterprise_info.district || '') + '</td></tr>'
    html += '<tr><td style="padding: 8px; border: 1px solid #ddd; background: #f5f5f5; font-weight: bold;">详细地址</td><td style="padding: 8px; border: 1px solid #ddd;">' + (data.enterprise_info.address || '未填写') + '</td></tr>'
    html += '<tr><td style="padding: 8px; border: 1px solid #ddd; background: #f5f5f5; font-weight: bold;">法人代表</td><td style="padding: 8px; border: 1px solid #ddd;">' + (data.enterprise_info.legal_representative || '未填写') + '</td></tr>'
    html += '<tr><td style="padding: 8px; border: 1px solid #ddd; background: #f5f5f5; font-weight: bold;">联系人</td><td style="padding: 8px; border: 1px solid #ddd;">' + (data.enterprise_info.contact_person || '未填写') + '</td></tr>'
    html += '<tr><td style="padding: 8px; border: 1px solid #ddd; background: #f5f5f5; font-weight: bold;">联系电话</td><td style="padding: 8px; border: 1px solid #ddd;">' + (data.enterprise_info.contact_phone || '未填写') + '</td></tr>'
    if (data.enterprise_info.capacity) {
      html += '<tr><td style="padding: 8px; border: 1px solid #ddd; background: #f5f5f5; font-weight: bold;">年产能</td><td style="padding: 8px; border: 1px solid #ddd;">' + data.enterprise_info.capacity + ' 万m²</td></tr>'
    }
    html += '</table>'
  }
  
  // 2. 筹划与组织
  if (data.planning_organization) {
    html += '<h2>二、筹划与组织</h2>'
    html += '<p><strong>领导团队人数：</strong>' + (data.planning_organization.leadership_team_count || 0) + '</p>'
    html += '<p><strong>工作团队人数：</strong>' + (data.planning_organization.work_team_count || 0) + '</p>'
    html += '<p><strong>工作计划数：</strong>' + (data.planning_organization.work_plans_count || 0) + '</p>'
    html += '<p><strong>培训记录数：</strong>' + (data.planning_organization.training_records_count || 0) + '</p>'
  }
  
  // 3. 预审核
  if (data.pre_audit_data) {
    html += '<h2>三、预审核数据</h2>'
    html += '<p><strong>状态：</strong>' + (data.pre_audit_data.has_data ? '已完成' : '未完成') + '</p>'
    if (data.pre_audit_data.has_data) {
      html += '<p>预审核数据已填写，包含生产情况、原辅材料、工艺装备、资源消耗、污染防治、固体废物、自行监测等信息。</p>'
    }
  }
  
  // 4. 审核结果
  if (data.audit_results) {
    html += '<h2>四、审核结果</h2>'
    html += '<p><strong>指标总数：</strong>' + (data.audit_results.total_indicators || 0) + '</p>'
    html += '<p><strong>已完成指标：</strong>' + (data.audit_results.completed_indicators || 0) + '</p>'
    if (data.audit_results.total_score !== null && data.audit_results.total_score !== undefined) {
      html += '<p><strong>综合得分：</strong>' + data.audit_results.total_score + ' 分</p>'
    }
    if (data.audit_results.overall_level) {
      html += '<p><strong>综合等级：</strong>' + data.audit_results.overall_level + '</p>'
    }
  }
  
  // 5. 问题及清洁生产方案
  if (data.problem_solution) {
    html += '<h2>五、问题及清洁生产方案</h2>'
    html += '<p><strong>问题数量：</strong>' + (data.problem_solution.issues_count || 0) + '</p>'
    if (data.problem_solution.issues && data.problem_solution.issues.length > 0) {
      html += '<p>已识别 ' + data.problem_solution.issues.length + ' 个需要改进的问题。</p>'
    }
  }
  
  html += '</div>'
  return html
}

// 预览报告
const handlePreview = async () => {
  if (!reportGenerated.value) {
    window.$message.warning('请先生成报告')
    return
  }
  
  await fetchPreviewContent()
  showPreviewModal.value = true
}

// 导出Word
const handleExportWord = async () => {
  if (!reportGenerated.value) {
    window.$message.warning('请先生成报告')
    return
  }

  try {
    exporting.value = true
    
    // 使用fetch直接下载文件，避免中间件的JSON解析问题
    const url = `/api/v1/pcb/enterprise/${props.enterpriseId}/report/download`
    
    // 获取token - 使用与拦截器相同的方法
    const token = getToken()
    
    // 调试：检查token是否存在
    console.log('🔑 下载文件时的Token状态:', {
      hasToken: !!token,
      tokenLength: token ? token.length : 0,
      tokenPreview: token ? token.substring(0, 20) + '...' : 'null'
    })
    
    if (!token) {
      window.$message.error('未获取到认证Token，请重新登录')
      exporting.value = false
      return
    }
    
    // 确保token是字符串类型
    const tokenStr = typeof token === 'string' ? token : String(token)
    
    const headers = {
      'Authorization': `Bearer ${tokenStr}`,
      'token': tokenStr
      // 注意：文件下载不需要Content-Type，让浏览器自动处理
    }
    
    const response = await fetch(url, {
      method: 'GET',
      headers: headers,
      credentials: 'include'  // 包含cookie
    })
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ msg: '下载失败' }))
      throw new Error(errorData.msg || `HTTP ${response.status}`)
    }
    
    // 获取文件名（从响应头或默认）
    const contentDisposition = response.headers.get('content-disposition') || ''
    let filename = `PCB审核报告_${enterpriseData.value.name || props.enterpriseId}_${new Date().toISOString().split('T')[0]}.docx`
    
    if (contentDisposition) {
      // 尝试从Content-Disposition头中提取文件名
      const filenameMatch = contentDisposition.match(/filename\*=UTF-8''(.+?)(?:;|$)/) || 
                            contentDisposition.match(/filename=["']?([^"';]+)["']?/i)
      if (filenameMatch && filenameMatch[1]) {
        filename = filenameMatch[1]
        // URL解码
        try {
          filename = decodeURIComponent(filename)
        } catch (e) {
          // 解码失败，使用原值
        }
      }
    }
    
    // 创建Blob并下载
    const blob = await response.blob()
    const downloadUrl = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = downloadUrl
    link.download = filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(downloadUrl)
    
    window.$message.success('Word报告下载成功')
  } catch (error) {
    console.error('导出Word失败:', error)
    window.$message.error('导出Word失败: ' + (error.message || '未知错误'))
  } finally {
    exporting.value = false
  }
}

// 导航方法
const goToPrevious = () => {
  emit('navigate', 'problem-solution')
}

onMounted(() => {
  fetchReportData()
})
</script>

<style scoped>
.report-container {
  padding: 20px;
  background: #f5f5f5;
  min-height: calc(100vh - 64px);
}

.report-preview-card {
  background: white;
}

.report-content {
  max-height: 600px;
  overflow-y: auto;
  padding: 20px;
  background: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
}

.report-preview-content {
  max-height: 70vh;
  overflow-y: auto;
  padding: 20px;
  background: #fafafa;
}

.data-status {
  margin-top: 16px;
}

.status-item {
  margin-bottom: 16px;
}

.module-navigation {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #e0e0e0;
}

.flex {
  display: flex;
}

.items-center {
  align-items: center;
}

.justify-between {
  justify-content: space-between;
}

.gap-3 {
  gap: 12px;
}

.text-primary {
  color: #18a058;
}

.text-lg {
  font-size: 18px;
}

.font-semibold {
  font-weight: 600;
}

.font-medium {
  font-weight: 500;
}

.m-0 {
  margin: 0;
}

.mt-1 {
  margin-top: 4px;
}

.mb-2 {
  margin-bottom: 8px;
}

.mb-4 {
  margin-bottom: 16px;
}

.mt-4 {
  margin-top: 16px;
}

.text-gray-500 {
  color: #6b7280;
}

.text-sm {
  font-size: 14px;
}

:deep(.n-card-header) {
  padding: 20px;
}

:deep(.n-step-header) {
  padding: 12px 0;
}

:deep(.report-preview) {
  font-family: 'Microsoft YaHei', sans-serif;
  line-height: 1.8;
}

:deep(.report-preview h1) {
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 30px;
}

:deep(.report-preview h2) {
  font-size: 18px;
  font-weight: bold;
  margin-top: 24px;
  margin-bottom: 12px;
  border-bottom: 2px solid #e0e0e0;
  padding-bottom: 8px;
}
</style>