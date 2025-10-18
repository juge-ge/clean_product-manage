<template>
  <div class="pre-audit-page p-4">
    <n-spin :show="loading">
      <n-form ref="formRef" :model="formData">
        <!-- 1. 企业总体生产情况 -->
        <n-card class="mb-4 production-info-card">
          <template #header>
            <div class="card-header">
              <div class="header-left">
                <TheIcon icon="carbon:chart-line" class="header-icon" />
                <span class="header-title">1. 企业总体生产情况</span>
              </div>
              <n-button type="primary" size="small" @click="saveModuleData('productionInfo')">
                <template #icon>
                  <TheIcon icon="carbon:save" />
                </template>
                暂存
              </n-button>
            </div>
          </template>
          <ProductionInfoForm v-model="formData.productionInfo" />
        </n-card>

        <!-- 2. 原辅材料使用情况 -->
        <n-card class="mb-4 raw-materials-card">
          <template #header>
            <div class="card-header">
              <div class="header-left">
                <TheIcon icon="carbon:cube" class="header-icon" />
                <span class="header-title">2. 原辅材料使用情况</span>
              </div>
              <n-button type="primary" size="small" @click="saveModuleData('rawMaterials')">
                <template #icon>
                  <TheIcon icon="carbon:save" />
                </template>
                暂存
              </n-button>
            </div>
          </template>
          <RawMaterialForm v-model="formData.rawMaterials" />
        </n-card>

        <!-- 3. 主要工艺及装备使用 -->
        <n-card class="mb-4 process-equipment-card">
          <template #header>
            <div class="card-header">
              <div class="header-left">
                <TheIcon icon="carbon:settings" class="header-icon" />
                <span class="header-title">3. 主要工艺及装备使用</span>
              </div>
              <n-button type="primary" size="small" @click="saveModuleData('processEquipment')">
                <template #icon>
                  <TheIcon icon="carbon:save" />
                </template>
                暂存
              </n-button>
            </div>
          </template>
          <ProcessEquipmentForm v-model="formData.processEquipment" />
        </n-card>

        <!-- 4. 资源能源消耗 -->
        <n-card class="mb-4 resource-consumption-card">
          <template #header>
            <div class="card-header">
              <div class="header-left">
                <TheIcon icon="carbon:energy" class="header-icon" />
                <span class="header-title">4. 资源能源消耗</span>
              </div>
              <n-button type="primary" size="small" @click="saveModuleData('resourceConsumption')">
                <template #icon>
                  <TheIcon icon="carbon:save" />
                </template>
                暂存
              </n-button>
            </div>
          </template>
          <ResourceConsumptionForm v-model="formData.resourceConsumption" />
        </n-card>

        <!-- 5. 污染防治 -->
        <n-card class="mb-4 pollution-control-card">
          <template #header>
            <div class="card-header">
              <div class="header-left">
                <TheIcon icon="carbon:cloud" class="header-icon" />
                <span class="header-title">5. 污染防治</span>
              </div>
              <n-button type="primary" size="small" @click="saveModuleData('pollutionControl')">
                <template #icon>
                  <TheIcon icon="carbon:save" />
                </template>
                暂存
              </n-button>
            </div>
          </template>
          <PollutionControlForm v-model="formData.pollutionControl" />
        </n-card>

        <!-- 6. 工业固体废物管理 -->
        <n-card class="mb-4 solid-waste-card">
          <template #header>
            <div class="card-header">
              <div class="header-left">
                <TheIcon icon="carbon:trash-can" class="header-icon" />
                <span class="header-title">6. 工业固体废物管理</span>
              </div>
              <n-button type="primary" size="small" @click="saveModuleData('solidWaste')">
                <template #icon>
                  <TheIcon icon="carbon:save" />
                </template>
                暂存
              </n-button>
            </div>
          </template>
          <SolidWasteForm v-model="formData.solidWaste" />
        </n-card>

        <!-- 7. 自行监测情况 -->
        <n-card class="mb-4 self-monitoring-card">
          <template #header>
            <div class="card-header">
              <div class="header-left">
                <TheIcon icon="carbon:chart-radar" class="header-icon" />
                <span class="header-title">7. 自行监测情况</span>
              </div>
              <n-button type="primary" size="small" @click="saveModuleData('selfMonitoring')">
                <template #icon>
                  <TheIcon icon="carbon:save" />
                </template>
                暂存
              </n-button>
            </div>
          </template>
          <SelfMonitoringForm v-model="formData.selfMonitoring" />
        </n-card>
      </n-form>
      <n-space justify="center" class="mt-6">
        <n-button @click="handleSaveDraft">保存草稿</n-button>
        <n-button type="primary" @click="handleSubmit">提交审核</n-button>
      </n-space>
    </n-spin>

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
import { ref, onMounted } from 'vue'
import { 
  NSpin, 
  NForm, 
  NCard,
  NSpace,
  NButton
} from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'
import ProductionInfoForm from './components/ProductionInfoForm.vue'
import RawMaterialForm from './components/RawMaterialForm.vue'
import ProcessEquipmentForm from './components/ProcessEquipmentForm.vue'
import ResourceConsumptionForm from './components/ResourceConsumptionForm.vue'
import PollutionControlForm from './components/PollutionControlForm.vue'
import SolidWasteForm from './components/SolidWasteForm.vue'
import SelfMonitoringForm from './components/SelfMonitoringForm.vue'
// import { mockDetailApi } from '@/mock/pcb-detail'
import api from '@/api'

defineOptions({ name: 'PCB预审核' })

const props = defineProps({
  enterpriseId: {
    type: [String, Number],
    required: true
  }
})

const emit = defineEmits(['update', 'navigate'])

// 数据状态
const loading = ref(false)
const formRef = ref(null)

// 表单数据 - 按技术方案设计的数据结构
const formData = ref({
  // 企业总体生产情况
  productionInfo: {
    productOutput: [],
    qualificationRate: [],
    outputValue: []
  },
  // 原辅材料使用情况
  rawMaterials: [],
  // 主要工艺及装备使用
  processEquipment: {
    rigid: {
      single: { line: '', process: '', equipment: '' },
      double: { line: '', process: '', equipment: '' },
      multilayer: { line: '', process: '', equipment: '' }
    },
    flexible: {
      single: { line: '', process: '', equipment: '' },
      double: { line: '', process: '', equipment: '' },
      multilayer: { line: '', process: '', equipment: '' }
    }
  },
  // 资源能源消耗
  resourceConsumption: {
    water: [],
    electricity: [],
    gas: []
  },
  // 污染防治
  pollutionControl: {
    copperRecovery: [],
    waterReuseRate: [],
    gasEmission: [],
    waterEmission: []
  },
  // 工业固体废物管理
  solidWaste: {
    general: [],
    hazardous: []
  },
  // 自行监测情况
  selfMonitoring: {
    organizedGas: { item: '', concentration: null, point: '', standard: '', reportFileId: '' },
    unorganizedGas: { item: '', concentration: null, point: '', standard: '', reportFileId: '' },
    wastewater: { item: '', concentration: null, point: '', standard: '', reportFileId: '' },
    noise: { item: '', level: null, point: '', standard: '', reportFileId: '' }
  }
})

// 获取预审核数据
const fetchPreAuditData = async () => {
  try {
    loading.value = true
    
    // 获取生产情况数据
    const productionResponse = await api.pcb.production.getData(props.enterpriseId)
    if (productionResponse.data) {
      formData.value.productionInfo = productionResponse.data
    }
    
    // 获取其他预审核数据
    const response = await api.pcb.preAudit.getData(props.enterpriseId)
    const data = response.data
    
    if (data) {
      formData.value = {
        ...formData.value,
        ...data
      }
    }
  } catch (error) {
    console.error('获取预审核数据失败:', error)
    window.$message.error('获取预审核数据失败')
  } finally {
    loading.value = false
  }
}

// 保存草稿
const handleSaveDraft = async () => {
  try {
    loading.value = true
    
    // 保存生产情况数据
    await api.pcb.production.saveData(props.enterpriseId, formData.value.productionInfo)
    
    // 保存其他预审核数据
    await api.pcb.preAudit.saveData(props.enterpriseId, formData.value)
    window.$message.success('草稿保存成功')
  } catch (error) {
    console.error('保存草稿失败:', error)
    window.$message.error('保存草稿失败')
  } finally {
    loading.value = false
  }
}

// 提交表单
const handleSubmit = async () => {
  try {
    loading.value = true
    await api.pcb.preAudit.submitData(props.enterpriseId)
    window.$message.success('预审核数据提交成功')
    emit('update', formData.value)
  } catch (error) {
    console.error('提交失败:', error)
    window.$message.error('提交失败')
  } finally {
    loading.value = false
  }
}

// 模块暂存方法
const saveModuleData = async (moduleName) => {
  try {
    loading.value = true
    
    // 根据模块名称保存对应的数据
    if (moduleName === 'productionInfo') {
      await api.pcb.production.saveData(props.enterpriseId, formData.value.productionInfo)
    } else {
      // 保存其他模块数据
      const moduleData = { [moduleName]: formData.value[moduleName] }
      await api.pcb.preAudit.saveModuleData(props.enterpriseId, moduleName, moduleData)
    }
    
    window.$message.success(`${getModuleDisplayName(moduleName)}暂存成功`)
  } catch (error) {
    console.error('模块暂存失败:', error)
    window.$message.error('模块暂存失败')
  } finally {
    loading.value = false
  }
}

// 获取模块显示名称
const getModuleDisplayName = (moduleName) => {
  const nameMap = {
    productionInfo: '企业总体生产情况',
    rawMaterials: '原辅材料使用情况',
    processEquipment: '主要工艺及装备使用',
    resourceConsumption: '资源能源消耗',
    pollutionControl: '污染防治',
    solidWaste: '工业固体废物管理',
    selfMonitoring: '自行监测情况'
  }
  return nameMap[moduleName] || moduleName
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
.pre-audit-page {
  max-width: 1200px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-icon {
  font-size: 18px;
  color: #1890ff;
}

.header-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
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
