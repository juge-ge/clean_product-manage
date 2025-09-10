<template>
  <div class="pre-audit-module">
    <n-card title="PCB企业清洁生产数据填报">
      <n-form ref="formRef" :model="formData" :rules="rules">
        <n-grid :cols="2" :x-gap="24">
          <!-- 产能产量数据 -->
          <n-form-item-gi label="单位产品电耗（kWh/m²）" path="unitPowerConsumption">
            <n-input-number 
              v-model:value="formData.unitPowerConsumption"
              placeholder="请输入单位产品电耗"
              :min="0"
              :precision="2"
              @update:value="handleDataChange('unitPowerConsumption', $event)"
            />
            <StandardComparison 
              :value="formData.unitPowerConsumption"
              :standard="standards.unitPowerConsumption"
              class="mt-2"
            />
          </n-form-item-gi>
          
          <n-form-item-gi label="废水产生量（m³/m²）" path="wastewaterGeneration">
            <n-input-number 
              v-model:value="formData.wastewaterGeneration"
              placeholder="请输入废水产生量"
              :min="0"
              :precision="3"
              @update:value="handleDataChange('wastewaterGeneration', $event)"
            />
            <StandardComparison 
              :value="formData.wastewaterGeneration"
              :standard="standards.wastewaterGeneration"
              class="mt-2"
            />
          </n-form-item-gi>
          
          <n-form-item-gi label="固体废物产生量（kg/m²）" path="solidWasteGeneration">
            <n-input-number 
              v-model:value="formData.solidWasteGeneration"
              placeholder="请输入固体废物产生量"
              :min="0"
              :precision="3"
              @update:value="handleDataChange('solidWasteGeneration', $event)"
            />
            <StandardComparison 
              :value="formData.solidWasteGeneration"
              :standard="standards.solidWasteGeneration"
              class="mt-2"
            />
          </n-form-item-gi>
          
          <n-form-item-gi label="新鲜水消耗量（m³/m²）" path="waterConsumption">
            <n-input-number 
              v-model:value="formData.waterConsumption"
              placeholder="请输入新鲜水消耗量"
              :min="0"
              :precision="2"
              @update:value="handleDataChange('waterConsumption', $event)"
            />
          </n-form-item-gi>
          
          <n-form-item-gi label="化学品消耗量（kg/m²）" path="chemicalConsumption">
            <n-input-number 
              v-model:value="formData.chemicalConsumption"
              placeholder="请输入化学品消耗量"
              :min="0"
              :precision="2"
              @update:value="handleDataChange('chemicalConsumption', $event)"
            />
          </n-form-item-gi>
        </n-grid>
      </n-form>
    </n-card>
    
    <!-- 环境数据 -->
    <n-card title="环境数据" class="mt-4">
      <n-form ref="envFormRef" :model="envData" :rules="envRules">
        <n-grid :cols="2" :x-gap="24">
          <n-form-item-gi label="废水COD浓度（mg/L）" path="wastewaterCOD">
            <n-input-number 
              v-model:value="envData.wastewaterCOD"
              placeholder="请输入废水COD浓度"
              :min="0"
              :precision="1"
            />
          </n-form-item-gi>
          
          <n-form-item-gi label="废水铜离子浓度（mg/L）" path="wastewaterCopper">
            <n-input-number 
              v-model:value="envData.wastewaterCopper"
              placeholder="请输入废水铜离子浓度"
              :min="0"
              :precision="2"
            />
          </n-form-item-gi>
          
          <n-form-item-gi label="大气污染物排放量（kg/m²）" path="airPollutants">
            <n-input-number 
              v-model:value="envData.airPollutants"
              placeholder="请输入大气污染物排放量"
              :min="0"
              :precision="2"
            />
          </n-form-item-gi>
          
          <n-form-item-gi label="厂界噪声水平（dB）" path="noiseLevel">
            <n-input-number 
              v-model:value="envData.noiseLevel"
              placeholder="请输入厂界噪声水平"
              :min="0"
              :precision="1"
            />
          </n-form-item-gi>
        </n-grid>
      </n-form>
    </n-card>

    <!-- 资源利用数据 -->
    <n-card title="资源利用数据" class="mt-4">
      <n-form ref="resourceFormRef" :model="resourceData" :rules="resourceRules">
        <n-grid :cols="2" :x-gap="24">
          <n-form-item-gi label="原材料利用率（%）" path="materialUtilization">
            <n-input-number 
              v-model:value="resourceData.materialUtilization"
              placeholder="请输入原材料利用率"
              :min="0"
              :max="100"
              :precision="1"
            />
          </n-form-item-gi>
          
          <n-form-item-gi label="能源使用效率（%）" path="energyEfficiency">
            <n-input-number 
              v-model:value="resourceData.energyEfficiency"
              placeholder="请输入能源使用效率"
              :min="0"
              :max="100"
              :precision="1"
            />
          </n-form-item-gi>
          
          <n-form-item-gi label="水回用率（%）" path="waterRecycling">
            <n-input-number 
              v-model:value="resourceData.waterRecycling"
              placeholder="请输入水回用率"
              :min="0"
              :max="100"
              :precision="1"
            />
          </n-form-item-gi>
          
          <n-form-item-gi label="废物回收率（%）" path="wasteRecovery">
            <n-input-number 
              v-model:value="resourceData.wasteRecovery"
              placeholder="请输入废物回收率"
              :min="0"
              :max="100"
              :precision="1"
            />
          </n-form-item-gi>
        </n-grid>
      </n-form>
    </n-card>
    
    <!-- 评估结果汇总 -->
    <n-card title="评估结果汇总" class="mt-4">
      <n-grid :cols="4" :x-gap="16">
        <n-statistic label="I级指标" :value="levelCounts.level1" />
        <n-statistic label="II级指标" :value="levelCounts.level2" />
        <n-statistic label="III级指标" :value="levelCounts.level3" />
        <n-statistic label="不达标指标" :value="levelCounts.unqualified" />
      </n-grid>
      
      <div class="mt-4">
        <n-button type="primary" @click="handleSubmit">
          提交预审核数据
        </n-button>
        <n-button class="ml-2" @click="resetForm">
          重置表单
        </n-button>
      </div>
    </n-card>

    <!-- 模块导航按钮 -->
    <div class="module-navigation mt-4">
      <n-space justify="space-between">
        <n-button @click="goToPrevious">
          <template #icon>
            <TheIcon icon="carbon:arrow-left" />
          </template>
          筹划与组织
        </n-button>
        <n-button type="primary" @click="goToNext">
          审核
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
  NForm, 
  NFormItem, 
  NFormItemGi,
  NGrid, 
  NInputNumber, 
  NStatistic,
  NButton
} from 'naive-ui'
import StandardComparison from '../components/StandardComparison.vue'
import { mockDetailApi } from '@/mock/pcb-detail'

defineOptions({ name: 'PCB预审核' })

const props = defineProps({
  enterpriseId: {
    type: [String, Number],
    required: true
  }
})

const emit = defineEmits(['update', 'navigate'])

// 表单引用
const formRef = ref(null)
const envFormRef = ref(null)
const resourceFormRef = ref(null)

// 表单数据
const formData = ref({
  unitPowerConsumption: null,
  wastewaterGeneration: null,
  solidWasteGeneration: null,
  waterConsumption: null,
  chemicalConsumption: null
})

const envData = ref({
  wastewaterCOD: null,
  wastewaterCopper: null,
  airPollutants: null,
  noiseLevel: null
})

const resourceData = ref({
  materialUtilization: null,
  energyEfficiency: null,
  waterRecycling: null,
  wasteRecovery: null
})

// 审核标准
const standards = ref({
  unitPowerConsumption: {
    level1: 100,
    level2: 150,
    level3: 200,
    unit: 'kWh/m²'
  },
  wastewaterGeneration: {
    level1: 0.2,
    level2: 0.3,
    level3: 0.4,
    unit: 'm³/m²'
  },
  solidWasteGeneration: {
    level1: 0.1,
    level2: 0.15,
    level3: 0.2,
    unit: 'kg/m²'
  }
})

// 评估结果
const levelCounts = ref({
  level1: 0,
  level2: 0,
  level3: 0,
  unqualified: 0
})

// 表单验证规则
const rules = {
  unitPowerConsumption: { required: true, message: '请输入单位产品电耗', trigger: 'change' },
  wastewaterGeneration: { required: true, message: '请输入废水产生量', trigger: 'change' },
  solidWasteGeneration: { required: true, message: '请输入固体废物产生量', trigger: 'change' },
  waterConsumption: { required: true, message: '请输入新鲜水消耗量', trigger: 'change' },
  chemicalConsumption: { required: true, message: '请输入化学品消耗量', trigger: 'change' }
}

const envRules = {
  wastewaterCOD: { required: true, message: '请输入废水COD浓度', trigger: 'change' },
  wastewaterCopper: { required: true, message: '请输入废水铜离子浓度', trigger: 'change' },
  airPollutants: { required: true, message: '请输入大气污染物排放量', trigger: 'change' },
  noiseLevel: { required: true, message: '请输入厂界噪声水平', trigger: 'change' }
}

const resourceRules = {
  materialUtilization: { required: true, message: '请输入原材料利用率', trigger: 'change' },
  energyEfficiency: { required: true, message: '请输入能源使用效率', trigger: 'change' },
  waterRecycling: { required: true, message: '请输入水回用率', trigger: 'change' },
  wasteRecovery: { required: true, message: '请输入废物回收率', trigger: 'change' }
}

// 获取预审核数据
const fetchPreAuditData = async () => {
  try {
    const response = await mockDetailApi.getPreAuditData(props.enterpriseId)
    const data = response.data
    
    // 填充表单数据
    formData.value = data.productionData || {}
    envData.value = data.environmentalData || {}
    resourceData.value = data.resourceData || {}
    
    // 计算评估结果
    calculateAssessment()
  } catch (error) {
    console.error('获取预审核数据失败:', error)
    window.$message.error('获取预审核数据失败')
  }
}

// 数据变化处理
const handleDataChange = (key, value) => {
  formData.value[key] = value
  // 实时计算评估结果
  calculateAssessment()
}

// 计算评估结果
const calculateAssessment = () => {
  let level1 = 0, level2 = 0, level3 = 0, unqualified = 0
  
  // 计算生产数据指标
  Object.keys(standards.value).forEach(key => {
    const value = formData.value[key]
    const standard = standards.value[key]
    
    if (value !== null && value !== undefined) {
      if (value <= standard.level1) {
        level1++
      } else if (value <= standard.level2) {
        level2++
      } else if (value <= standard.level3) {
        level3++
      } else {
        unqualified++
      }
    }
  })
  
  // 计算资源利用指标（百分比类型）
  const resourceKeys = ['materialUtilization', 'energyEfficiency', 'waterRecycling', 'wasteRecovery']
  resourceKeys.forEach(key => {
    const value = resourceData.value[key]
    if (value !== null && value !== undefined) {
      if (value >= 90) {
        level1++
      } else if (value >= 80) {
        level2++
      } else if (value >= 70) {
        level3++
      } else {
        unqualified++
      }
    }
  })
  
  levelCounts.value = { level1, level2, level3, unqualified }
}

// 提交表单
const handleSubmit = async () => {
  try {
    // 验证所有表单
    await Promise.all([
      formRef.value?.validate(),
      envFormRef.value?.validate(),
      resourceFormRef.value?.validate()
    ])
    
    const submitData = {
      productionData: formData.value,
      environmentalData: envData.value,
      resourceData: resourceData.value,
      assessmentResults: levelCounts.value
    }
    
    await mockDetailApi.submitPreAuditData(props.enterpriseId, submitData)
    window.$message.success('预审核数据提交成功')
    emit('update', submitData)
  } catch (error) {
    if (error?.message) {
      console.error('提交失败:', error)
      window.$message.error('提交失败')
    }
  }
}

// 重置表单
const resetForm = () => {
  formRef.value?.restoreValidation()
  envFormRef.value?.restoreValidation()
  resourceFormRef.value?.restoreValidation()
  fetchPreAuditData()
}

// 导航方法
const goToPrevious = () => {
  emit('navigate', 'planning')
}

const goToNext = () => {
  emit('navigate', 'audit')
}

onMounted(() => {
  fetchPreAuditData()
})
</script>

<style scoped>
.pre-audit-module {
  padding: 16px;
}

:deep(.n-statistic) {
  text-align: center;
}

:deep(.n-statistic .n-statistic-value) {
  font-size: 24px;
  font-weight: 600;
}

:deep(.n-statistic .n-statistic-label) {
  font-size: 14px;
  color: var(--n-text-color-secondary);
}
</style>
