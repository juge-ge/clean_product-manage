<template>
  <div class="report-module">
    <n-card title="钢铁企业清洁生产审核评估报告">
      <template #header-extra>
        <n-space>
          <n-button @click="previewReport">预览报告</n-button>
          <n-button type="primary" @click="exportReport('pdf')">导出PDF</n-button>
          <n-button type="primary" @click="exportReport('word')">导出Word</n-button>
        </n-space>
      </template>
      
      <!-- 暂时注释掉ReportEditor组件 -->
      <!-- <ReportEditor
        ref="editorRef"
        v-model:content="reportContent"
        :enterprise-data="enterpriseData"
        :audit-data="auditData"
        :scheme-data="schemeData"
      /> -->
      
      <!-- 临时替代内容 -->
      <div class="temp-content">
        <n-input
          v-model:value="reportContent"
          type="textarea"
          placeholder="请输入报告内容..."
          :rows="20"
        />
      </div>
    </n-card>

    <!-- 模块导航按钮 -->
    <div class="module-navigation mt-4">
      <n-space justify="space-between">
        <n-button @click="goToPrevious">
          <template #icon>
            <TheIcon icon="carbon:arrow-left" />
          </template>
          方案库
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
import { ref, onMounted } from 'vue'
import { NCard, NButton, NSpace, NInput } from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'
// import ReportEditor from '@/views/cloud-audit/steel/enterprise-detail/components/ReportEditor.vue'
import { mockDetailApi } from '@/mock/steel-detail'

defineOptions({ name: '钢铁审核报告' })

const props = defineProps({
  enterpriseId: {
    type: [String, Number],
    required: true
  }
})

const emit = defineEmits(['update', 'navigate'])

// 导航函数
const goToPrevious = () => {
  emit('navigate', 'scheme-library')
}

// 数据状态
const editorRef = ref(null)
const reportContent = ref('')
const enterpriseData = ref({})
const auditData = ref({})
const schemeData = ref([])

// 获取报告数据
const fetchReportData = async () => {
  try {
    const response = await mockDetailApi.generateReport(props.enterpriseId)
    reportContent.value = response.data.content || generateDefaultReport()
    
    // 获取相关数据
    const [auditResponse, schemeResponse] = await Promise.all([
      mockDetailApi.getAuditResults(props.enterpriseId),
      mockDetailApi.getSchemes(props.enterpriseId)
    ])
    
    auditData.value = auditResponse.data
    schemeData.value = schemeResponse.data.list || []
  } catch (error) {
    console.error('获取报告数据失败:', error)
    window.$message.error('获取报告数据失败')
  }
}

// 生成默认报告
const generateDefaultReport = () => {
  return `
# 钢铁企业清洁生产审核评估报告

## 1. 企业基本情况

### 1.1 企业概况
- 企业名称：${enterpriseData.value.name || '待填写'}
- 所属地市：${enterpriseData.value.city || '待填写'}
- 所属县：${enterpriseData.value.county || '待填写'}
- 企业规模：${enterpriseData.value.scale || '待填写'}

### 1.2 生产工艺
- 主要产品：钢铁制造
- 年产钢量：${enterpriseData.value.annualOutput || '待填写'}万吨
- 生产能力：${enterpriseData.value.productionCapacity || '待填写'}万吨/年
- 建厂时间：${enterpriseData.value.establishmentDate || '待填写'}

## 2. 清洁生产审核

### 2.1 审核范围
本次审核范围包括企业的主要生产车间、辅助设施、环保设施等，涵盖烧结、球团、焦化、炼铁、炼钢、轧钢等主要工序。

### 2.2 审核过程
- 审核时间：${new Date().toLocaleDateString()}
- 审核团队：由专业审核人员组成
- 审核方法：现场调研、资料分析、数据收集

### 2.3 审核结果
- 总体评分：${auditData.value.totalScore || 0}分
- 审核等级：${auditData.value.overallLevel || '待评估'}
- 待改进项数：${auditData.value.improvementItems || 0}项
- 限定性指标：${auditData.value.limitingIndicators || 0}项

## 3. 方案分析与实施

### 3.1 方案识别
通过审核，识别出以下清洁生产改进方案：

${schemeData.value.map(scheme => `
#### ${scheme.name}
- 方案类型：${scheme.type}
- 投资估算：${scheme.investment}万元
- 投资回收期：${scheme.paybackPeriod}年
- 预期效果：${scheme.expectedEffect}
- 经济效益：${scheme.economicBenefit}
- 环境效益：${scheme.environmentalBenefit}
`).join('')}

### 3.2 方案筛选
根据技术可行性、经济合理性、环境效益等因素，对识别出的方案进行筛选。

### 3.3 方案实施计划
制定详细的方案实施计划，包括实施时间、责任部门、资金安排等。

## 4. 审核结论

### 4.1 资源节约效果
通过实施清洁生产方案，预计可实现：
- 节能效果：待评估
- 节水效果：待评估
- 原材料节约：待评估

### 4.2 环境改善效果
- 废水减排：待评估
- 废气减排：待评估
- 固废减量：待评估

### 4.3 经济效益分析
- 投资总额：待评估
- 年节约成本：待评估
- 投资回收期：待评估

## 5. 建议与措施

### 5.1 管理建议
1. 建立健全清洁生产管理制度
2. 加强员工培训，提高清洁生产意识
3. 定期开展清洁生产审核

### 5.2 技术建议
1. 采用先进的生产工艺和设备
2. 加强资源综合利用
3. 完善环保设施

### 5.3 持续改进
1. 建立清洁生产持续改进机制
2. 定期评估清洁生产效果
3. 不断优化清洁生产方案

---
报告生成时间：${new Date().toLocaleString()}
  `
}

// 预览报告
const previewReport = () => {
  window.$message.info('预览功能待开发')
}

// 导出报告
const exportReport = async (format) => {
  try {
    await mockDetailApi.exportReport(props.enterpriseId, format)
    window.$message.success(`报告导出成功（${format.toUpperCase()}格式）`)
  } catch (error) {
    console.error('导出报告失败:', error)
    window.$message.error('导出报告失败')
  }
}

onMounted(() => {
  fetchReportData()
})
</script>

<style scoped>
.report-module {
  padding: 16px;
}

:deep(.n-card-header) {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
