<template>
  <div class="pre-audit-page p-4">
    <n-spin :show="loading">
      <n-form ref="formRef" :model="formData">
        <n-collapse default-expanded-names="1" accordion>
          <n-collapse-item title="1. 企业总体生产情况" name="1">
            <ProductionInfoForm v-model="formData.productionInfo" />
          </n-collapse-item>
          
          <n-collapse-item title="2. 原辅材料使用情况" name="2">
            <RawMaterialForm v-model="formData.rawMaterials" />
          </n-collapse-item>
          
          <n-collapse-item title="3. 主要工艺及装备" name="3">
            <ProcessEquipmentForm v-model="formData.processEquipment" />
          </n-collapse-item>
          
          <n-collapse-item title="4. 资源能源消耗" name="4">
            <ResourceConsumptionForm v-model="formData.resourceConsumption" />
          </n-collapse-item>
          
          <n-collapse-item title="5. 污染防治" name="5">
            <PollutionControlForm v-model="formData.pollutionControl" />
          </n-collapse-item>
          
          <n-collapse-item title="6. 工业固体废物管理" name="6">
            <SolidWasteForm v-model="formData.solidWaste" />
          </n-collapse-item>
          
          <n-collapse-item title="7. 自行监测情况" name="7">
            <SelfMonitoringForm v-model="formData.selfMonitoring" />
          </n-collapse-item>
        </n-collapse>
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
  NCollapse,
  NCollapseItem,
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
import { mockDetailApi } from '@/mock/steel-detail'

defineOptions({ name: '钢铁预审核' })

const props = defineProps({
  enterpriseId: {
    type: [String, Number],
    required: true
  }
})

const emit = defineEmits(['update', 'navigate'])

// 导航函数
const goToPrevious = () => {
  emit('navigate', 'planning')
}

const goToNext = () => {
  emit('navigate', 'audit')
}

// 数据状态
const loading = ref(false)
const formRef = ref(null)

// 表单数据 - 按技术方案设计的数据结构
const formData = ref({
  // 企业总体生产情况
  productionInfo: {
    capacity: null,
    output: {
      '2022': {
        crudeSteel: null,
        steelProducts: null,
        pigIron: null,
        coke: null,
        sinterOre: null,
        pellet: null
      },
      '2023': {
        crudeSteel: null,
        steelProducts: null,
        pigIron: null,
        coke: null,
        sinterOre: null,
        pellet: null
      },
      '2024': {
        crudeSteel: null,
        steelProducts: null,
        pigIron: null,
        coke: null,
        sinterOre: null,
        pellet: null
      }
    }
  },
  // 原辅材料使用情况
  rawMaterials: [],
  // 主要工艺及装备使用
  processEquipment: {
    sintering: { capacity: '', equipment: '', year: '' },
    pelletizing: { capacity: '', equipment: '', year: '' },
    coking: { capacity: '', equipment: '', year: '' },
    ironMaking: { capacity: '', equipment: '', year: '' },
    steelMaking: { capacity: '', equipment: '', year: '' },
    rolling: { capacity: '', equipment: '', year: '' }
  },
  // 资源能源消耗
  resourceConsumption: {
    energy: [],
    water: [],
    electricity: []
  },
  // 污染防治
  pollutionControl: {
    wastewater: {
      treatment: '',
      capacity: null,
      process: ''
    },
    wasteGas: {
      treatment: '',
      facilities: '',
      efficiency: null
    },
    solidWaste: {
      treatment: '',
      utilization: null
    }
  },
  // 工业固体废物管理
  solidWaste: {
    general: [],
    hazardous: []
  },
  // 自行监测情况
  selfMonitoring: {
    wastewater: {
      pollutants: '',
      frequency: '',
      compliance: ''
    },
    wasteGas: {
      pollutants: '',
      frequency: '',
      compliance: ''
    },
    noise: {
      points: null,
      frequency: '',
      compliance: ''
    }
  }
})

// 获取预审核数据
const fetchPreAuditData = async () => {
  try {
    loading.value = true
    const response = await mockDetailApi.getPreAuditData(props.enterpriseId)
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
    await mockDetailApi.submitPreAuditData(props.enterpriseId, formData.value)
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
    await mockDetailApi.submitPreAuditData(props.enterpriseId, formData.value)
    window.$message.success('预审核数据提交成功')
    emit('update', formData.value)
  } catch (error) {
    console.error('提交失败:', error)
    window.$message.error('提交失败')
  } finally {
    loading.value = false
  }
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
