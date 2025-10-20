<template>
  <div class="self-monitoring-form">
    <n-space vertical :size="16">
      <!-- 有组织废气检测表 -->
      <n-card title="有组织废气检测表" size="small" class="sub-module">
        <template #header-extra>
          <n-space>
            <n-button type="primary" size="small" @click="addOrganizedGasRow">
              <template #icon>
                <TheIcon icon="carbon:add" />
              </template>
              添加行
            </n-button>
            <n-button type="info" size="small" @click="addOrganizedGasColumn">
                  <template #icon>
                <TheIcon icon="carbon:add" />
                  </template>
              添加列
                </n-button>
          </n-space>
        </template>
        
        <n-data-table
          :columns="organizedGasColumns"
          :data="formData.organizedGas || []"
          :row-key="row => row.id"
          :pagination="false"
          size="small"
        />
      </n-card>

      <!-- 无组织废气检测表 -->
      <n-card title="无组织废气检测表" size="small" class="sub-module">
        <template #header-extra>
          <n-button type="primary" size="small" @click="addUnorganizedGasRow">
                  <template #icon>
              <TheIcon icon="carbon:add" />
                  </template>
            添加行
                </n-button>
        </template>
        
        <n-data-table
          :columns="unorganizedGasColumns"
          :data="formData.unorganizedGas || []"
          :row-key="row => row.id"
          :pagination="false"
          size="small"
        />
      </n-card>

      <!-- 废水排放监测情况表 -->
      <n-card title="废水排放监测情况表" size="small" class="sub-module">
        <template #header-extra>
          <n-space>
            <n-button type="primary" size="small" @click="addWastewaterRow">
              <template #icon>
                <TheIcon icon="carbon:add" />
              </template>
              添加行
            </n-button>
            <n-button type="info" size="small" @click="addWastewaterColumn">
              <template #icon>
                <TheIcon icon="carbon:add" />
              </template>
              添加列
            </n-button>
          </n-space>
        </template>
        
        <n-data-table
          :columns="wastewaterColumns"
          :data="formData.wastewater || []"
          :row-key="row => row.id"
          :pagination="false"
          size="small"
        />
      </n-card>

      <!-- 废气排放监测情况表 -->
      <n-card title="废气排放监测情况表" size="small" class="sub-module">
        <template #header-extra>
          <n-button type="primary" size="small" @click="addGasEmissionRow">
                  <template #icon>
              <TheIcon icon="carbon:add" />
                  </template>
            添加行
                </n-button>
        </template>
        
        <n-data-table
          :columns="gasEmissionColumns"
          :data="formData.gasEmission || []"
          :row-key="row => row.id"
          :pagination="false"
          size="small"
        />
      </n-card>

      <!-- 近三年厂界噪声监测情况表 -->
      <n-card title="近三年厂界噪声监测情况表" size="small" class="sub-module">
        <template #header-extra>
          <n-button type="primary" size="small" @click="addNoiseRow">
                  <template #icon>
              <TheIcon icon="carbon:add" />
                  </template>
            添加行
                </n-button>
        </template>
        
        <n-data-table
          :columns="noiseColumns"
          :data="formData.noise || []"
          :row-key="row => row.id"
          :pagination="false"
          size="small"
        />
      </n-card>
    </n-space>
  </div>
</template>

<script setup>
import { computed, ref, h, watch } from 'vue'
import { 
  NSpace,
  NCard,
  NDataTable,
  NInput,
  NInputNumber,
  NSelect,
  NButton,
  useMessage
} from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      organizedGas: [],
      unorganizedGas: [],
      wastewater: [],
      gasEmission: [],
      noise: []
    })
  }
})

const emit = defineEmits(['update:modelValue'])
const message = useMessage()

const formData = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// 监测因子选项
const monitoringFactorOptions = [
  { label: '氮氧化物', value: '氮氧化物' },
  { label: '氯化氢', value: '氯化氢' },
  { label: '氰化氢', value: '氰化氢' },
  { label: '硫酸雾', value: '硫酸雾' },
  { label: '铬酸雾', value: '铬酸雾' },
  { label: '氟化物', value: '氟化物' },
  { label: '酚类', value: '酚类' },
  { label: '非甲烷总烃', value: '非甲烷总烃' },
  { label: '苯', value: '苯' },
  { label: '甲苯', value: '甲苯' },
  { label: '二甲苯', value: '二甲苯' },
  { label: '甲苯与二甲苯合计', value: '甲苯与二甲苯合计' }
]

// 有组织废气检测表列
const organizedGasColumns = computed(() => {
  const baseColumns = [
    {
      title: '监测点位',
      key: 'monitoringPoint',
      width: 150,
      render: (row) => h(NInput, {
        value: row.monitoringPoint,
        placeholder: '监测点位',
        onUpdateValue: (value) => { row.monitoringPoint = value }
      })
    },
    {
      title: '监测时间',
      key: 'monitoringTime',
      width: 150,
      render: (row) => h(NInput, {
        value: row.monitoringTime,
        placeholder: '监测时间',
        onUpdateValue: (value) => { row.monitoringTime = value }
      })
    }
  ]

  // 动态添加监测项目列
  const projectColumns = []
  for (const factor of monitoringFactorOptions) {
    projectColumns.push({
      title: factor.label,
      key: `result_${factor.value}`,
      width: 120,
      render: (row) => h(NInputNumber, {
        value: row[`result_${factor.value}`],
        min: 0,
        precision: 2,
        placeholder: '结果',
        onUpdateValue: (value) => { row[`result_${factor.value}`] = value }
      })
    })
  }

  const actionColumn = {
    title: '操作',
    key: 'action',
    width: 80,
    render: (row, index) => h(NButton, {
      size: "small",
      type: "error",
      onClick: () => removeOrganizedGasRow(index)
    }, () => '删除')
  }

  return [...baseColumns, ...projectColumns, actionColumn]
})

// 无组织废气检测表列
const unorganizedGasColumns = [
  {
    title: '采样时间',
    key: 'samplingTime',
    width: 150,
    render: (row) => h(NInput, {
      value: row.samplingTime,
      placeholder: '采样时间',
      onUpdateValue: (value) => { row.samplingTime = value }
    })
  },
  {
    title: '采样点位',
    key: 'samplingPoint',
    width: 150,
    render: (row) => h(NInput, {
      value: row.samplingPoint,
      placeholder: '采样点位',
      onUpdateValue: (value) => { row.samplingPoint = value }
    })
  },
  {
    title: '监测因子',
    key: 'monitoringFactor',
    width: 150,
    render: (row) => h(NSelect, {
      value: row.monitoringFactor,
      options: monitoringFactorOptions,
      placeholder: '监测因子',
      onUpdateValue: (value) => { row.monitoringFactor = value }
    })
  },
  {
    title: '排放浓度（mg/m³）',
    key: 'emissionConcentration',
    width: 150,
    render: (row) => h(NInputNumber, {
      value: row.emissionConcentration,
      min: 0,
      precision: 2,
      placeholder: '排放浓度',
      onUpdateValue: (value) => { row.emissionConcentration = value }
    })
  },
  {
    title: '排放浓度限值（mg/m³）',
    key: 'emissionLimit',
    width: 150,
    render: (row) => h(NInputNumber, {
      value: row.emissionLimit,
      min: 0,
      precision: 2,
      placeholder: '限值',
      onUpdateValue: (value) => { row.emissionLimit = value }
    })
  },
  {
    title: '达标情况',
    key: 'compliance',
    width: 120,
    render: (row) => h(NSelect, {
      value: row.compliance,
      options: [
        { label: '达标', value: '达标' },
        { label: '不达标', value: '不达标' }
      ],
      placeholder: '达标情况',
      onUpdateValue: (value) => { row.compliance = value }
    })
  },
  {
    title: '操作',
    key: 'action',
    width: 80,
    render: (row, index) => h(NButton, {
      size: "small",
      type: "error",
      onClick: () => removeUnorganizedGasRow(index)
    }, () => '删除')
  }
]

// 废水排放监测情况表列
const wastewaterColumns = computed(() => {
  const baseColumns = [
    {
      title: '采样日期',
      key: 'samplingDate',
      width: 150,
      render: (row) => h(NInput, {
        value: row.samplingDate,
        placeholder: '采样日期',
        onUpdateValue: (value) => { row.samplingDate = value }
      })
    }
  ]

  // 基础检测项目
  const basicProjects = [
    { label: 'pH', value: 'pH' },
    { label: 'COD', value: 'COD' },
    { label: '氨氮', value: '氨氮' },
    { label: '总磷', value: '总磷' },
    { label: '总氮', value: '总氮' },
    { label: '总氰化物', value: '总氰化物' },
    { label: '总铜', value: '总铜' }
  ]

  const projectColumns = []
  for (const project of basicProjects) {
    projectColumns.push({
      title: `${project.label}（mg/L）`,
      key: `result_${project.value}`,
      width: 120,
      render: (row) => h(NInputNumber, {
        value: row[`result_${project.value}`],
        min: 0,
        precision: 2,
        placeholder: '结果',
        onUpdateValue: (value) => { row[`result_${project.value}`] = value }
      })
    })
  }

  const actionColumn = {
    title: '操作',
    key: 'action',
    width: 80,
    render: (row, index) => h(NButton, {
      size: "small",
      type: "error",
      onClick: () => removeWastewaterRow(index)
    }, () => '删除')
  }

  return [...baseColumns, ...projectColumns, actionColumn]
})

// 废气排放监测情况表列
const gasEmissionColumns = [
  {
    title: '检测点位',
    key: 'detectionPoint',
    width: 150,
    render: (row) => h(NInput, {
      value: row.detectionPoint,
      placeholder: '检测点位',
      onUpdateValue: (value) => { row.detectionPoint = value }
    })
  },
  {
    title: '检测项目',
    key: 'detectionItem',
    width: 150,
    render: (row) => h(NInput, {
      value: row.detectionItem,
      placeholder: '检测项目',
      onUpdateValue: (value) => { row.detectionItem = value }
    })
  },
  {
    title: '检测结果',
    key: 'detectionResult',
    width: 150,
    render: (row) => h(NInputNumber, {
      value: row.detectionResult,
      min: 0,
      precision: 2,
      placeholder: '检测结果',
      onUpdateValue: (value) => { row.detectionResult = value }
    })
  },
  {
    title: '许可排放浓度限值',
    key: 'permittedEmissionLimit',
    width: 150,
    render: (row) => h(NInputNumber, {
      value: row.permittedEmissionLimit,
      min: 0,
      precision: 2,
      placeholder: '限值',
      onUpdateValue: (value) => { row.permittedEmissionLimit = value }
    })
  },
  {
    title: '排气筒高（m）',
    key: 'stackHeight',
    width: 120,
    render: (row) => h(NInputNumber, {
      value: row.stackHeight,
      min: 0,
      precision: 1,
      placeholder: '高度',
      onUpdateValue: (value) => { row.stackHeight = value }
    })
  },
  {
    title: '操作',
    key: 'action',
    width: 80,
    render: (row, index) => h(NButton, {
      size: "small",
      type: "error",
      onClick: () => removeGasEmissionRow(index)
    }, () => '删除')
  }
]

// 近三年厂界噪声监测情况表列
const noiseColumns = [
  {
    title: '监测时间',
    key: 'monitoringTime',
    width: 150,
    render: (row) => h(NInput, {
      value: row.monitoringTime,
      placeholder: '监测时间',
      onUpdateValue: (value) => { row.monitoringTime = value }
    })
  },
  {
    title: '监测点位',
    key: 'monitoringPoint',
    width: 150,
    render: (row) => h(NInput, {
      value: row.monitoringPoint,
      placeholder: '监测点位',
      onUpdateValue: (value) => { row.monitoringPoint = value }
    })
  },
  {
    title: '检测结果 Leq（dB（A））昼间',
    key: 'daytimeResult',
    width: 180,
    render: (row) => h(NInputNumber, {
      value: row.daytimeResult,
      min: 0,
      precision: 1,
      placeholder: '昼间结果',
      onUpdateValue: (value) => { row.daytimeResult = value }
    })
  },
  {
    title: '检测结果 Leq（dB（A））夜间',
    key: 'nighttimeResult',
    width: 180,
    render: (row) => h(NInputNumber, {
      value: row.nighttimeResult,
      min: 0,
      precision: 1,
      placeholder: '夜间结果',
      onUpdateValue: (value) => { row.nighttimeResult = value }
    })
  },
  {
    title: '排放标准 Leq（dB（A））昼间',
    key: 'daytimeStandard',
    width: 180,
    render: (row) => h(NInputNumber, {
      value: row.daytimeStandard,
      min: 0,
      precision: 1,
      placeholder: '昼间标准',
      onUpdateValue: (value) => { row.daytimeStandard = value }
    })
  },
  {
    title: '排放标准 Leq（dB（A））夜间',
    key: 'nighttimeStandard',
    width: 180,
    render: (row) => h(NInputNumber, {
      value: row.nighttimeStandard,
      min: 0,
      precision: 1,
      placeholder: '夜间标准',
      onUpdateValue: (value) => { row.nighttimeStandard = value }
    })
  },
  {
    title: '操作',
    key: 'action',
    width: 80,
    render: (row, index) => h(NButton, {
      size: "small",
      type: "error",
      onClick: () => removeNoiseRow(index)
    }, () => '删除')
  }
]

// 添加行方法
const addOrganizedGasRow = () => {
  const newRow = { id: Date.now(), monitoringPoint: '', monitoringTime: '' }
  // 初始化所有监测项目结果
  for (const factor of monitoringFactorOptions) {
    newRow[`result_${factor.value}`] = null
  }
  formData.value.organizedGas.push(newRow)
}

const addUnorganizedGasRow = () => {
  formData.value.unorganizedGas.push({
    id: Date.now(),
    samplingTime: '',
    samplingPoint: '',
    monitoringFactor: '',
    emissionConcentration: null,
    emissionLimit: null,
    compliance: ''
  })
}

const addWastewaterRow = () => {
  const newRow = { id: Date.now(), samplingDate: '' }
  // 初始化基础检测项目结果
  const basicProjects = ['pH', 'COD', '氨氮', '总磷', '总氮', '总氰化物', '总铜']
  for (const project of basicProjects) {
    newRow[`result_${project}`] = null
  }
  formData.value.wastewater.push(newRow)
}

const addGasEmissionRow = () => {
  formData.value.gasEmission.push({
    id: Date.now(),
    detectionPoint: '',
    detectionItem: '',
    detectionResult: null,
    permittedEmissionLimit: null,
    stackHeight: null
  })
}

const addNoiseRow = () => {
  formData.value.noise.push({
    id: Date.now(),
    monitoringTime: '',
    monitoringPoint: '',
    daytimeResult: null,
    nighttimeResult: null,
    daytimeStandard: null,
    nighttimeStandard: null
  })
}

// 删除行方法
const removeOrganizedGasRow = (index) => {
  formData.value.organizedGas.splice(index, 1)
}

const removeUnorganizedGasRow = (index) => {
  formData.value.unorganizedGas.splice(index, 1)
}

const removeWastewaterRow = (index) => {
  formData.value.wastewater.splice(index, 1)
}

const removeGasEmissionRow = (index) => {
  formData.value.gasEmission.splice(index, 1)
}

const removeNoiseRow = (index) => {
  formData.value.noise.splice(index, 1)
}

// 添加列方法（暂时简化实现）
const addOrganizedGasColumn = () => {
  message.info('添加列功能待实现')
}

const addWastewaterColumn = () => {
  message.info('添加列功能待实现')
}

// 确保数据结构完整
watch(() => props.modelValue, (newVal) => {
  if (newVal) {
    if (!newVal.organizedGas) {
      newVal.organizedGas = []
    }
    if (!newVal.unorganizedGas) {
      newVal.unorganizedGas = []
    }
    if (!newVal.wastewater) {
      newVal.wastewater = []
    }
    if (!newVal.gasEmission) {
      newVal.gasEmission = []
    }
    if (!newVal.noise) {
      newVal.noise = []
    }
    
    // 如果表格为空，添加一条空白记录
    if (newVal.organizedGas.length === 0) {
      addOrganizedGasRow()
    }
    if (newVal.unorganizedGas.length === 0) {
      addUnorganizedGasRow()
    }
    if (newVal.wastewater.length === 0) {
      addWastewaterRow()
    }
    if (newVal.gasEmission.length === 0) {
      addGasEmissionRow()
    }
    if (newVal.noise.length === 0) {
      addNoiseRow()
    }
  }
}, { immediate: true, deep: true })
</script>

<style scoped>
.self-monitoring-form {
  padding: 16px 0;
}

.sub-module {
  border: 1px solid #e0e0e6;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.sub-module:hover {
  border-color: #18a058;
  box-shadow: 0 2px 8px rgba(24, 160, 88, 0.15);
}

/* 表格样式优化 */
:deep(.n-data-table) {
  border-radius: 6px;
}

:deep(.n-data-table .n-data-table-td) {
  padding: 8px 12px;
  vertical-align: middle;
}

:deep(.n-data-table .n-data-table-th) {
  background-color: #f8f9fa;
  font-weight: 600;
  color: #333;
}

/* 输入框样式 */
:deep(.n-select) {
  width: 100%;
}

:deep(.n-input-number) {
  width: 100%;
}

:deep(.n-input) {
  width: 100%;
}

/* 卡片标题样式 */
:deep(.n-card-header .n-card-header__main) {
  font-weight: 600;
  color: #333;
  display: inline-block;
  border-bottom: 2px solid #ff8c00;
  padding-bottom: 8px;
}

</style>






