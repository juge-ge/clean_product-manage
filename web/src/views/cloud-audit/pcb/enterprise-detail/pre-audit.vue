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
            </div>
          </template>
          <ProductionInfoForm 
            v-model="formData.productionInfo" 
            :enterprise-id="enterpriseId"
          />
        </n-card>

        <!-- 2. 原辅材料使用情况 -->
        <n-card class="mb-4 raw-materials-card">
          <template #header>
            <div class="card-header">
              <div class="header-left">
                <TheIcon icon="carbon:cube" class="header-icon" />
                <span class="header-title">2. 原辅材料使用情况</span>
              </div>
            </div>
          </template>
          <RawMaterialForm v-model="formData.rawMaterials" :enterprise-id="enterpriseId" />
        </n-card>

        <!-- 3. 主要工艺及装备使用 -->
        <n-card class="mb-4 process-equipment-card">
          <template #header>
            <div class="card-header">
              <div class="header-left">
                <TheIcon icon="carbon:settings" class="header-icon" />
                <span class="header-title">3. 主要工艺及装备使用</span>
              </div>
            </div>
          </template>
          <ProcessEquipmentForm v-model="formData.processEquipment" :enterprise-id="enterpriseId" />
        </n-card>

        <!-- 4. 资源能源消耗 -->
        <n-card class="mb-4 resource-consumption-card">
          <template #header>
            <div class="card-header">
              <div class="header-left">
                <TheIcon icon="carbon:energy" class="header-icon" />
                <span class="header-title">4. 资源能源消耗</span>
              </div>
            </div>
          </template>
          <ResourceConsumptionForm ref="resourceConsumptionFormRef" v-model="formData.resourceConsumption" :enterprise-id="enterpriseId" />
        </n-card>

        <!-- 5. 污染防治 -->
        <n-card class="mb-4 pollution-control-card">
          <template #header>
            <div class="card-header">
              <div class="header-left">
                <TheIcon icon="carbon:cloud" class="header-icon" />
                <span class="header-title">5. 污染防治</span>
              </div>
            </div>
          </template>
          <PollutionControlForm v-model="formData.pollutionControl" :enterprise-id="enterpriseId" />
        </n-card>

        <!-- 6. 工业固体废物管理 -->
        <n-card class="mb-4 solid-waste-card">
          <template #header>
            <div class="card-header">
              <div class="header-left">
                <TheIcon icon="carbon:trash-can" class="header-icon" />
                <span class="header-title">6. 工业固体废物管理</span>
              </div>
            </div>
          </template>
          <SolidWasteForm v-model="formData.solidWaste" :enterprise-id="enterpriseId" />
        </n-card>

        <!-- 7. 自行监测情况 -->
        <n-card class="mb-4 self-monitoring-card">
          <template #header>
            <div class="card-header">
              <div class="header-left">
                <TheIcon icon="carbon:chart-radar" class="header-icon" />
                <span class="header-title">7. 自行监测情况</span>
              </div>
            </div>
          </template>
          <SelfMonitoringForm v-model="formData.selfMonitoring" :enterprise-id="enterpriseId" />
        </n-card>

        <!-- 8. 生产工艺与装备要求 -->
        <n-card class="mb-4 process-equipment-requirement-card">
          <template #header>
            <div class="card-header">
              <div class="header-left">
                <TheIcon icon="carbon:checklist" class="header-icon" />
                <span class="header-title">8. 生产工艺与装备要求</span>
              </div>
            </div>
          </template>
          <n-alert type="info" :closable="false" class="mb-2">
            选择规则：可多选，但需自下而上逐级满足（先勾选Ⅲ级，方可勾选Ⅱ级；需勾选Ⅱ/Ⅲ级后方可勾选Ⅰ级）。也可选择“均不符合”。
          </n-alert>
          <ProcessEquipmentRequirement v-model="formData.processRequirement" :enterprise-id="enterpriseId" />
        </n-card>

        <!-- 9. 温室气体排放 -->
        <n-card class="mb-4 greenhouse-gas-emission-card">
          <template #header>
            <div class="card-header">
              <div class="header-left">
                <TheIcon icon="carbon:earth" class="header-icon" />
                <span class="header-title">9. 温室气体排放</span>
              </div>
            </div>
          </template>
          <GreenhouseGasEmission v-model="formData.greenhouseGasEmission" :enterprise-id="enterpriseId" />
        </n-card>

        <!-- 10. 产品特征 -->
        <n-card class="mb-4 product-characteristics-card">
          <template #header>
            <div class="card-header">
              <div class="header-left">
                <TheIcon icon="carbon:box" class="header-icon" />
                <span class="header-title">10. 产品特征</span>
              </div>
            </div>
          </template>
          <ProductCharacteristics v-model="formData.productCharacteristics" :enterprise-id="enterpriseId" />
        </n-card>

        <!-- 11. 清洁生产管理 -->
        <n-card class="mb-4 clean-production-management-card">
          <template #header>
            <div class="card-header">
              <div class="header-left">
                <TheIcon icon="carbon:document-management" class="header-icon" />
                <span class="header-title">11. 清洁生产管理</span>
              </div>
            </div>
          </template>
          <CleanProductionManagement v-model="formData.cleanProductionManagement" :enterprise-id="enterpriseId" />
        </n-card>

        <!-- 12. 能源、水、原/辅材料的消耗利用和污染物的排放 -->
        <n-card class="mb-4 resource-utilization-card">
          <template #header>
            <div class="card-header">
              <div class="header-left">
                <TheIcon icon="carbon:energy-renewable" class="header-icon" />
                <span class="header-title">12. 能源、水、原/辅材料的消耗利用和污染物的排放</span>
              </div>
            </div>
          </template>
          <ResourceUtilization v-model="formData.resourceUtilization" :enterprise-id="enterpriseId" />
        </n-card>

        <!-- 13. 资源综合利用 -->
        <n-card class="mb-4 resource-reutilization-card">
          <template #header>
            <div class="card-header">
              <div class="header-left">
                <TheIcon icon="carbon:renew" class="header-icon" />
                <span class="header-title">13. 资源综合利用</span>
              </div>
            </div>
          </template>
          <ResourceReutilization v-model="formData.resourceReutilization" :enterprise-id="enterpriseId" />
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
  NButton,
  NAlert
} from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'
import ProductionInfoForm from './components/ProductionInfoForm.vue'
import RawMaterialForm from './components/RawMaterialForm.vue'
import ProcessEquipmentForm from './components/ProcessEquipmentForm.vue'
import ResourceConsumptionForm from './components/ResourceConsumptionForm.vue'
import PollutionControlForm from './components/PollutionControlForm.vue'
import SolidWasteForm from './components/SolidWasteForm.vue'
import SelfMonitoringForm from './components/SelfMonitoringForm.vue'
import ProcessEquipmentRequirement from './components/ProcessEquipmentRequirement.vue'
import GreenhouseGasEmission from './components/GreenhouseGasEmission.vue'
import ProductCharacteristics from './components/ProductCharacteristics.vue'
import CleanProductionManagement from './components/CleanProductionManagement.vue'
import ResourceUtilization from './components/ResourceUtilization.vue'
import ResourceReutilization from './components/ResourceReutilization.vue'
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
const resourceConsumptionFormRef = ref(null)

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
    equipment: []
  },
  // 资源能源消耗
  resourceConsumption: {
    water: [],
    electricity: [],
    gas: []
  },
  // 污染防治
  pollutionControl: {
    wastewater: [],
    wasteGas: []
  },
  // 工业固体废物管理
  solidWaste: {
    waste: []
  },
  // 自行监测情况
  selfMonitoring: {
    organizedGas: [],
    unorganizedGas: [],
    wastewater: [],
    gasEmission: [],
    noise: []
  },
  // 生产工艺与装备要求
  processRequirement: {
    basicRequirements: [],
    mechanicalFacilities: [],
    printingProcess: [],
    cleaning: [],
    etching: [],
    plating: []
  },
  // 温室气体排放
  greenhouseGasEmission: {
    carbonManagement: [],
    emissionPerOutput: [],
    emissionIntensity: []
  },
  // 产品特征
  productCharacteristics: {
    auxiliaryMaterial: [],
    packaging: [],
    hazardousSubstance: [],
    productPerformance: []
  },
  // 清洁生产管理
  cleanProductionManagement: {
    environmentalLaw: [],
    industrialPolicy: [],
    cleanProductionManagement: [],
    cleanProductionAudit: [],
    energyManagement: [],
    emissionMonitoring: [],
    chemicalManagement: [],
    measurementEquipment: [],
    solidWasteDisposal: [],
    soilPollutionRisk: [],
    transportMode: []
  },
  // 能源、水、原/辅材料的消耗利用和污染物的排放
  resourceUtilization: {
    energyConsumption: [],
    freshWaterConsumption: [],
    wastewaterTotalConsumption: [],
    wastewaterCuConsumption: [],
    wastewaterCODConsumption: [],
    rawMaterialConsumption: []
  },
  // 资源综合利用
  resourceReutilization: {
    waterReuse: [],
    etchingRecovery: [],
    generalSolidUtil: [],
    wastewaterCollection: [],
    wasteGasTreatment: [],
    generalSolidCollection: [],
    hazardousWasteCollection: [],
    noise: []
  }
})

// 获取预审核数据
const fetchPreAuditData = async () => {
  loading.value = true
  try {
    // 生产情况数据由ProductionInfoForm组件自己管理，不再在这里获取
    
    // 获取其他预审核数据（该接口后端自带空对象兜底）
    const response = await api.pcb.preAudit.getData(props.enterpriseId)
    const data = response?.data
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
    
    // 生产情况数据由ProductionInfoForm组件自己管理，不再在这里保存
    
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
    if (moduleName === 'resourceConsumption') {
      // 调用资源能源消耗组件的保存方法
      if (resourceConsumptionFormRef.value && resourceConsumptionFormRef.value.saveData) {
        await resourceConsumptionFormRef.value.saveData()
      }
    } else if (moduleName === 'processEquipment') {
      await api.pcb.processEquipment.saveAllData(props.enterpriseId, formData.value.processEquipment)
    } else if (moduleName === 'pollutionControl') {
      await api.pcb.pollutionControl.saveAllData(props.enterpriseId, formData.value.pollutionControl)
    } else if (moduleName === 'solidWaste') {
      await api.pcb.solidWaste.saveAllData(props.enterpriseId, formData.value.solidWaste)
    } else if (moduleName === 'selfMonitoring') {
      await api.pcb.selfMonitoring.saveAllData(props.enterpriseId, formData.value.selfMonitoring)
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
    selfMonitoring: '自行监测情况',
    processRequirement: '生产工艺与装备要求',
    greenhouseGasEmission: '温室气体排放',
    productCharacteristics: '产品特征',
    cleanProductionManagement: '清洁生产管理',
    resourceUtilization: '能源、水、原/辅材料的消耗利用和污染物的排放',
    resourceReutilization: '资源综合利用'
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
