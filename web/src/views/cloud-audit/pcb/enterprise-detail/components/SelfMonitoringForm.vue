<template>
  <div class="self-monitoring-form">
    <n-space vertical :size="16">
      <!-- 有组织废气检测表 -->
      <n-card title="有组织废气检测表" size="small" class="sub-module">
        <template #header-extra>
            <n-button type="primary" size="small" @click="addOrganizedGasRow">
              <template #icon>
                <TheIcon icon="carbon:add" />
              </template>
              添加行
            </n-button>
        </template>
        
        <n-data-table
          :columns="organizedGasColumns"
          :data="formData.organizedGas || []"
          :row-key="row => row.id"
          :pagination="false"
          size="small"
          :loading="loadingOrganizedGas"
        />
        
        <template #footer>
          <div style="text-align: left; padding-top: 16px;">
            <n-button 
              type="primary" 
              :loading="loadingOrganizedGas"
              @click="submitOrganizedGasData"
            >
              <template #icon>
                <TheIcon icon="carbon:checkmark" />
              </template>
              提交
            </n-button>
          </div>
        </template>
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
          :loading="loadingUnorganizedGas"
        />
        
        <template #footer>
          <div style="text-align: left; padding-top: 16px;">
            <n-button 
              type="primary" 
              :loading="loadingUnorganizedGas"
              @click="submitUnorganizedGasData"
            >
              <template #icon>
                <TheIcon icon="carbon:checkmark" />
              </template>
              提交
            </n-button>
          </div>
        </template>
      </n-card>

      <!-- 废水排放监测情况表 -->
      <n-card title="废水排放监测情况表" size="small" class="sub-module">
        <template #header-extra>
            <n-button type="primary" size="small" @click="addWastewaterRow">
              <template #icon>
                <TheIcon icon="carbon:add" />
              </template>
              添加行
            </n-button>
        </template>
        
        <n-data-table
          :columns="wastewaterColumns"
          :data="formData.wastewater || []"
          :row-key="row => row.id"
          :pagination="false"
          size="small"
          :loading="loadingWastewater"
        />
        
        <template #footer>
          <div style="text-align: left; padding-top: 16px;">
            <n-button 
              type="primary" 
              :loading="loadingWastewater"
              @click="submitWastewaterData"
            >
              <template #icon>
                <TheIcon icon="carbon:checkmark" />
              </template>
              提交
            </n-button>
          </div>
        </template>
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
          :loading="loadingGasEmission"
        />
        
        <template #footer>
          <div style="text-align: left; padding-top: 16px;">
            <n-button 
              type="primary" 
              :loading="loadingGasEmission"
              @click="submitGasEmissionData"
            >
              <template #icon>
                <TheIcon icon="carbon:checkmark" />
              </template>
              提交
            </n-button>
          </div>
        </template>
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
          :loading="loadingNoise"
        />
        
        <template #footer>
          <div style="text-align: left; padding-top: 16px;">
            <n-button 
              type="primary" 
              :loading="loadingNoise"
              @click="submitNoiseData"
            >
              <template #icon>
                <TheIcon icon="carbon:checkmark" />
              </template>
              提交
            </n-button>
          </div>
        </template>
      </n-card>
    </n-space>
  </div>
</template>

<script setup>
import { computed, ref, h, watch, onMounted } from 'vue'
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
import api from '@/api/pcb'

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
  },
  enterpriseId: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['update:modelValue'])
const message = useMessage()

// 加载状态
const loadingOrganizedGas = ref(false)
const loadingUnorganizedGas = ref(false)
const loadingWastewater = ref(false)
const loadingGasEmission = ref(false)
const loadingNoise = ref(false)

const formData = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// 监测因子选项（有组织废气，增加 VOCs）
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
  { label: '甲苯与二甲苯合计', value: '甲苯与二甲苯合计' },
  { label: 'VOCs', value: 'VOCs' }
]

// 有组织废气检测表列
const organizedGasColumns = computed(() => {
  const baseColumns = [
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
      title: '监测地点',
      key: 'monitoringPoint',
      width: 150,
      render: (row) => h(NInput, {
        value: row.monitoringPoint,
        placeholder: '监测地点',
        onUpdateValue: (value) => { row.monitoringPoint = value }
      })
    }
  ]

  // 动态添加监测项目列（支持ND输入）
  const projectChildren = []
  for (const factor of monitoringFactorOptions) {
    projectChildren.push({
      title: factor.label,
      key: `result_${factor.value}`,
      width: 120,
      render: (row) => h(NInput, {
        value: row[`result_${factor.value}`] != null ? String(row[`result_${factor.value}`]) : '',
        placeholder: '结果（可输入ND或小数）',
        showButton: false,
        onUpdateValue: (value) => { 
          // 保持字符串格式，支持ND和小数输入
          if (value === '' || value === null || value === undefined) {
            row[`result_${factor.value}`] = null
          } else {
            // 保持字符串格式，支持ND和小数输入
            row[`result_${factor.value}`] = value
          }
        }
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

  return [...baseColumns, { title: '监测项目及化验结果 单位mg/m³', key: 'organized_group', children: projectChildren }, actionColumn]
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
    render: (row) => h(NInput, {
      value: row.emissionConcentration != null ? String(row.emissionConcentration) : '',
      placeholder: '排放浓度（可输入ND或小数）',
      onUpdateValue: (value) => { 
        // 保持字符串格式，支持ND和小数输入
        if (value === '' || value === null || value === undefined) {
          row.emissionConcentration = null
        } else {
          // 保持字符串格式，支持ND和小数输入
          row.emissionConcentration = value
        }
      }
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
      title: '监测地点',
      key: 'monitoringPoint',
      width: 150,
      render: (row) => h(NInput, {
        value: row.monitoringPoint,
        placeholder: '监测地点',
        onUpdateValue: (value) => { row.monitoringPoint = value }
      })
    }
  ]

  // 基础检测项目（顺序与要求一致）
  const basicProjects = [
    { label: 'pH', value: 'pH' },
    { label: '氨氮', value: '氨氮' },
    { label: '总氮', value: '总氮' },
    { label: 'COD', value: 'COD' },
    { label: '镍', value: '镍' },
    { label: '铜', value: '铜' },
    { label: '总磷', value: '总磷' },
    { label: '总氰化物', value: '总氰化物' },
    { label: '镍（镍排口）', value: '镍（镍排口）' }
  ]

  const projectChildren = []
  for (const project of basicProjects) {
    projectChildren.push({
      title: `${project.label}`,
      key: `result_${project.value}`,
      width: 120,
      render: (row) => h(NInputNumber, {
        value: row[`result_${project.value}`],
        min: 0,
        precision: 2,
        showButton: false,
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

  return [...baseColumns, { title: '监测项目 单位 mg/L', key: 'wastewater_group', children: projectChildren }, actionColumn]
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
    title: '排放速率（kg/h）',
    key: 'emissionRate',
    width: 150,
    render: (row) => h(NInputNumber, {
      value: row.emissionRate,
      min: 0,
      placeholder: '排放速率',
      onUpdateValue: (value) => { row.emissionRate = value }
    })
  },
  {
    title: '标杆流量（m³/h）',
    key: 'benchmarkFlow',
    width: 150,
    render: (row) => h(NInputNumber, {
      value: row.benchmarkFlow,
      min: 0,
      placeholder: '标杆流量',
      onUpdateValue: (value) => { row.benchmarkFlow = value }
    })
  },
  {
    title: '检测结果',
    key: 'detectionResult',
    width: 150,
    render: (row) => h(NInput, {
      value: row.detectionResult != null ? String(row.detectionResult) : '',
      placeholder: '检测结果（可输入ND或小数）',
      onUpdateValue: (value) => { 
        // 保持原始输入值（字符串），支持ND和小数
        if (value === '' || value === null || value === undefined) {
          row.detectionResult = null
        } else {
          // 保持字符串格式，支持ND和小数输入
          row.detectionResult = value
        }
      }
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
  const newRow = { 
    id: Date.now(), 
    monitoringTime: '',
    monitoringPoint: ''
  }
  // 初始化基础检测项目结果（按前端实际使用的字段名）
  const basicProjects = ['pH', 'COD', '氨氮', '总氮', '总磷', '铜', '镍', '总氰化物', '镍（镍排口）']
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
    emissionRate: null,
    benchmarkFlow: null,
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

// 加载有组织废气检测数据
const loadOrganizedGasData = async () => {
  if (!props.enterpriseId) return
  
  loadingOrganizedGas.value = true
  try {
    const response = await api.selfMonitoring.getOrganizedGasBatch(props.enterpriseId)
    if (response.data && Array.isArray(response.data)) {
      formData.value.organizedGas = response.data.map(item => ({
        id: item.id || Date.now() + Math.random(),
        monitoringPoint: item.monitoringPoint || '',
        monitoringTime: item.monitoringTime || '',
        ...Object.fromEntries(
          Object.entries(item).filter(([key]) => key.startsWith('result_'))
        )
      }))
    }
  } catch (error) {
    console.error('加载有组织废气检测数据失败:', error)
    message.error('加载有组织废气检测数据失败: ' + (error.message || '未知错误'))
  } finally {
    loadingOrganizedGas.value = false
  }
}

// 提交有组织废气检测数据
const submitOrganizedGasData = async () => {
  if (!props.enterpriseId) {
    message.warning('企业ID不能为空')
    return
  }
  
  loadingOrganizedGas.value = true
  try {
    const items = formData.value.organizedGas
      .filter(row => row.monitoringPoint && row.monitoringTime)
      .map(row => {
        const resultData = {}
        // 处理所有result_开头的字段，支持ND值和小数
        for (const [key, value] of Object.entries(row)) {
          if (key.startsWith('result_')) {
            // 保持字符串格式，支持ND和小数
            if (value === 'ND' || value === '') {
              resultData[key] = 'ND'
            } else if (value != null && value !== undefined) {
              // 转换为字符串，保持原始格式（支持小数）
              resultData[key] = String(value).trim()
              if (resultData[key] === '') {
                resultData[key] = null
              }
            } else {
              resultData[key] = null
            }
          }
        }
        return {
          monitoringPoint: row.monitoringPoint,
          monitoringTime: row.monitoringTime,
          ...resultData
        }
      })
    
    await api.selfMonitoring.batchSaveOrganizedGas(props.enterpriseId, items)
    message.success('有组织废气检测数据提交成功')
    await new Promise(resolve => setTimeout(resolve, 300))
    await loadOrganizedGasData()
  } catch (error) {
    console.error('提交有组织废气检测数据失败:', error)
    message.error('提交有组织废气检测数据失败: ' + (error.message || '未知错误'))
  } finally {
    loadingOrganizedGas.value = false
  }
}

// 加载无组织废气检测数据
const loadUnorganizedGasData = async () => {
  if (!props.enterpriseId) return
  
  loadingUnorganizedGas.value = true
  try {
    const response = await api.selfMonitoring.getUnorganizedGasBatch(props.enterpriseId)
    if (response.data && Array.isArray(response.data)) {
      formData.value.unorganizedGas = response.data.map(item => ({
        id: item.id || Date.now() + Math.random(),
        samplingTime: item.samplingTime || '',
        samplingPoint: item.samplingPoint || '',
        monitoringFactor: item.monitoringFactor || '',
        emissionConcentration: item.emissionConcentration,
        emissionLimit: item.emissionLimit,
        compliance: item.compliance || ''
      }))
    }
  } catch (error) {
    console.error('加载无组织废气检测数据失败:', error)
    message.error('加载无组织废气检测数据失败: ' + (error.message || '未知错误'))
  } finally {
    loadingUnorganizedGas.value = false
  }
}

// 提交无组织废气检测数据
const submitUnorganizedGasData = async () => {
  if (!props.enterpriseId) {
    message.warning('企业ID不能为空')
    return
  }
  
  loadingUnorganizedGas.value = true
  try {
    const items = formData.value.unorganizedGas
      .filter(row => row.samplingTime && row.samplingPoint && row.monitoringFactor)
      .map(row => {
        // 处理排放浓度：保持字符串格式，支持ND和小数
        let emissionConcentration = row.emissionConcentration
        if (emissionConcentration === 'ND' || emissionConcentration === '') {
          emissionConcentration = 'ND'
        } else if (emissionConcentration != null && emissionConcentration !== undefined) {
          // 转换为字符串，保持原始格式（支持小数）
          emissionConcentration = String(emissionConcentration).trim()
          if (emissionConcentration === '') {
            emissionConcentration = null
          }
        } else {
          emissionConcentration = null
        }
        
        return {
          samplingTime: row.samplingTime,
          samplingPoint: row.samplingPoint,
          monitoringFactor: row.monitoringFactor,
          emissionConcentration: emissionConcentration,
          emissionLimit: row.emissionLimit || null,
          compliance: row.compliance || ''
        }
      })
    
    await api.selfMonitoring.batchSaveUnorganizedGas(props.enterpriseId, items)
    message.success('无组织废气检测数据提交成功')
    await new Promise(resolve => setTimeout(resolve, 300))
    await loadUnorganizedGasData()
  } catch (error) {
    console.error('提交无组织废气检测数据失败:', error)
    message.error('提交无组织废气检测数据失败: ' + (error.message || '未知错误'))
  } finally {
    loadingUnorganizedGas.value = false
  }
}

// 加载废水排放监测数据
const loadWastewaterData = async () => {
  if (!props.enterpriseId) return
  
  loadingWastewater.value = true
  try {
    const response = await api.selfMonitoring.getWastewaterBatch(props.enterpriseId)
    if (response.data && Array.isArray(response.data)) {
      formData.value.wastewater = response.data.map(item => ({
        id: item.id || Date.now() + Math.random(),
        monitoringTime: item.monitoringTime || '',
        monitoringPoint: item.monitoringPoint || '',
        ...Object.fromEntries(
          Object.entries(item).filter(([key]) => key.startsWith('result_'))
        )
      }))
    }
  } catch (error) {
    console.error('加载废水排放监测数据失败:', error)
    message.error('加载废水排放监测数据失败: ' + (error.message || '未知错误'))
  } finally {
    loadingWastewater.value = false
  }
}

// 提交废水排放监测数据
const submitWastewaterData = async () => {
  if (!props.enterpriseId) {
    message.warning('企业ID不能为空')
    return
  }
  
  loadingWastewater.value = true
  try {
    const items = formData.value.wastewater
      .filter(row => row.monitoringTime)
      .map(row => ({
        monitoringTime: row.monitoringTime,
        monitoringPoint: row.monitoringPoint || '',
        ...Object.fromEntries(
          Object.entries(row).filter(([key]) => key.startsWith('result_'))
        )
      }))
    
    await api.selfMonitoring.batchSaveWastewater(props.enterpriseId, items)
    message.success('废水排放监测数据提交成功')
    await new Promise(resolve => setTimeout(resolve, 300))
    await loadWastewaterData()
  } catch (error) {
    console.error('提交废水排放监测数据失败:', error)
    message.error('提交废水排放监测数据失败: ' + (error.message || '未知错误'))
  } finally {
    loadingWastewater.value = false
  }
}

// 加载废气排放监测数据
const loadGasEmissionData = async () => {
  if (!props.enterpriseId) return
  
  loadingGasEmission.value = true
  try {
    const response = await api.selfMonitoring.getGasEmissionBatch(props.enterpriseId)
    if (response.data && Array.isArray(response.data)) {
      formData.value.gasEmission = response.data.map(item => ({
        id: item.id || Date.now() + Math.random(),
        detectionPoint: item.detectionPoint || '',
        detectionItem: item.detectionItem || '',
        emissionRate: item.emissionRate || item.emission_rate || null,
        benchmarkFlow: item.benchmarkFlow || item.benchmark_flow || null,
        detectionResult: item.detectionResult !== null && item.detectionResult !== undefined ? item.detectionResult : null,
        permittedEmissionLimit: item.permittedEmissionLimit || null,
        stackHeight: item.stackHeight || null
      }))
    }
  } catch (error) {
    console.error('加载废气排放监测数据失败:', error)
    message.error('加载废气排放监测数据失败: ' + (error.message || '未知错误'))
  } finally {
    loadingGasEmission.value = false
  }
}

// 提交废气排放监测数据
const submitGasEmissionData = async () => {
  if (!props.enterpriseId) {
    message.warning('企业ID不能为空')
    return
  }
  
  loadingGasEmission.value = true
  try {
    const items = formData.value.gasEmission
      .filter(row => row.detectionPoint && row.detectionItem)
      .map(row => {
        // 处理检测结果：保持字符串格式，支持ND和小数
        let detectionResult = row.detectionResult
        if (detectionResult === 'ND' || detectionResult === '') {
          detectionResult = 'ND'
        } else if (detectionResult != null && detectionResult !== undefined) {
          // 转换为字符串，保持原始格式（支持小数）
          detectionResult = String(detectionResult).trim()
          // 如果转换后为空，设为null
          if (detectionResult === '') {
            detectionResult = null
          }
        } else {
          detectionResult = null
        }
        
        return {
          detectionPoint: row.detectionPoint,
          detectionItem: row.detectionItem,
          emissionRate: row.emissionRate || null,
          benchmarkFlow: row.benchmarkFlow || null,
          detectionResult: detectionResult,
          permittedEmissionLimit: row.permittedEmissionLimit || null,
          stackHeight: row.stackHeight || null
        }
      })
    
    await api.selfMonitoring.batchSaveGasEmission(props.enterpriseId, items)
    message.success('废气排放监测数据提交成功')
    await new Promise(resolve => setTimeout(resolve, 300))
    await loadGasEmissionData()
  } catch (error) {
    console.error('提交废气排放监测数据失败:', error)
    message.error('提交废气排放监测数据失败: ' + (error.message || '未知错误'))
  } finally {
    loadingGasEmission.value = false
  }
}

// 加载噪声监测数据
const loadNoiseData = async () => {
  if (!props.enterpriseId) return
  
  loadingNoise.value = true
  try {
    const response = await api.selfMonitoring.getNoiseBatch(props.enterpriseId)
    if (response.data && Array.isArray(response.data)) {
      formData.value.noise = response.data.map(item => ({
        id: item.id || Date.now() + Math.random(),
        monitoringTime: item.monitoringTime || '',
        monitoringPoint: item.monitoringPoint || '',
        daytimeResult: item.daytimeResult,
        nighttimeResult: item.nighttimeResult,
        daytimeStandard: item.daytimeStandard,
        nighttimeStandard: item.nighttimeStandard
      }))
    }
  } catch (error) {
    console.error('加载噪声监测数据失败:', error)
    message.error('加载噪声监测数据失败: ' + (error.message || '未知错误'))
  } finally {
    loadingNoise.value = false
  }
}

// 提交噪声监测数据
const submitNoiseData = async () => {
  if (!props.enterpriseId) {
    message.warning('企业ID不能为空')
    return
  }
  
  loadingNoise.value = true
  try {
    const items = formData.value.noise
      .filter(row => row.monitoringTime && row.monitoringPoint)
      .map(row => ({
        monitoringTime: row.monitoringTime,
        monitoringPoint: row.monitoringPoint,
        daytimeResult: row.daytimeResult,
        nighttimeResult: row.nighttimeResult,
        daytimeStandard: row.daytimeStandard,
        nighttimeStandard: row.nighttimeStandard
      }))
    
    await api.selfMonitoring.batchSaveNoise(props.enterpriseId, items)
    message.success('噪声监测数据提交成功')
    await new Promise(resolve => setTimeout(resolve, 300))
    await loadNoiseData()
  } catch (error) {
    console.error('提交噪声监测数据失败:', error)
    message.error('提交噪声监测数据失败: ' + (error.message || '未知错误'))
  } finally {
    loadingNoise.value = false
  }
}

// 初始化加载数据
onMounted(() => {
  if (props.enterpriseId) {
    loadOrganizedGasData()
    loadUnorganizedGasData()
    loadWastewaterData()
    loadGasEmissionData()
    loadNoiseData()
  }
})

// 监听企业ID变化
watch(() => props.enterpriseId, (newId) => {
  if (newId) {
    loadOrganizedGasData()
    loadUnorganizedGasData()
    loadWastewaterData()
    loadGasEmissionData()
    loadNoiseData()
  }
})

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






