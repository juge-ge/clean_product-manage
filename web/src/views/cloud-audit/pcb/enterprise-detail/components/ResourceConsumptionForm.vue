<template>
  <div class="resource-consumption-form">
    <!-- 企业近三年用水情况统计 -->
    <n-card class="mb-4 water-consumption-card sub-module" title="企业近三年用水情况统计">
      <template #header-extra>
        <n-space>
          <div class="year-range-selector">
            <n-text strong>年份范围：</n-text>
            <n-select
              v-model:value="selectedWaterYearRange"
              :options="yearRangeOptions"
              style="width: 200px"
              @update:value="onWaterYearRangeChange"
            />
          </div>
          <n-button type="primary" size="small" @click="addWaterRow">
            <template #icon>
              <TheIcon icon="carbon:add" />
            </template>
            添加行
          </n-button>
        </n-space>
      </template>
      
      <n-data-table
        :columns="getWaterColumns()"
        :data="waterTableData"
        :row-key="row => row.id"
        :pagination="false"
        size="small"
        :loading="loadingWater"
      />
      
      <div class="water-actions mt-4">
        <n-space>
          <n-button type="primary" @click="submitWaterData">
            <template #icon>
              <TheIcon icon="carbon:checkmark" />
            </template>
            提交
          </n-button>
        </n-space>
      </div>
    </n-card>

    <!-- 企业近三年用电情况统计 -->
    <n-card class="mb-4 electricity-consumption-card sub-module" title="企业近三年用电情况统计">
      <template #header-extra>
        <n-space>
          <div class="year-range-selector">
            <n-text strong>年份范围：</n-text>
            <n-select
              v-model:value="selectedElectricityYearRange"
              :options="yearRangeOptions"
              style="width: 200px"
              @update:value="onElectricityYearRangeChange"
            />
          </div>
          <n-button type="primary" size="small" @click="addElectricityRow">
            <template #icon>
              <TheIcon icon="carbon:add" />
            </template>
            添加行
          </n-button>
        </n-space>
      </template>
      
      <n-data-table
        :columns="getElectricityColumns()"
        :data="electricityTableData"
        :row-key="row => row.id"
        :pagination="false"
        size="small"
        :loading="loadingElectricity"
      />
      
      <div class="electricity-actions mt-4">
        <n-space>
          <n-button type="primary" @click="submitElectricityData">
            <template #icon>
              <TheIcon icon="carbon:checkmark" />
            </template>
            提交
          </n-button>
        </n-space>
      </div>
    </n-card>

    <!-- 天然气情况统计 -->
    <n-card class="mb-4 gas-consumption-card sub-module" title="企业近三年天然气（煤气）情况统计">
      <template #header-extra>
        <n-space>
          <div class="year-range-selector">
            <n-text strong>年份范围：</n-text>
            <n-select
              v-model:value="selectedGasYearRange"
              :options="yearRangeOptions"
              style="width: 200px"
              @update:value="onGasYearRangeChange"
            />
          </div>
          <n-button type="primary" size="small" @click="addGasRow">
            <template #icon>
              <TheIcon icon="carbon:add" />
            </template>
            添加行
          </n-button>
        </n-space>
      </template>
      
      <n-data-table
        :columns="getGasColumns()"
        :data="gasTableData"
        :row-key="row => row.id"
        :pagination="false"
        size="small"
        :loading="loadingGas"
      />
      
      <div class="gas-actions mt-4">
        <n-space>
          <n-button type="primary" @click="submitGasData">
            <template #icon>
              <TheIcon icon="carbon:checkmark" />
            </template>
            提交
          </n-button>
        </n-space>
        </div>
    </n-card>

  </div>
</template>

<script setup>
import { ref, computed, h, nextTick, onMounted, watch } from 'vue'
import { 
  NCard, 
  NDataTable, 
  NButton, 
  NInput,
  NInputNumber, 
  NSelect,
  NCheckbox,
  NCheckboxGroup,
  NRadio,
  NRadioGroup,
  NSpace,
  NText,
  NDivider,
  NModal,
  NForm,
  NFormItem,
  NTag,
  useMessage
} from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'
import api from '@/api'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      water: [],
      electricity: [],
      gas: []
    })
  },
  enterpriseId: {
    type: [String, Number],
    required: true
  }
})

const emit = defineEmits(['update:modelValue'])
const message = useMessage()

const formData = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// 年份范围选项
const yearRangeOptions = [
  { label: '2022-2024', value: '2022-2024' },
  { label: '2021-2023', value: '2021-2023' },
  { label: '2020-2022', value: '2020-2022' }
]

// 各模块的年份范围选择
const selectedWaterYearRange = ref('2022-2024')
const selectedElectricityYearRange = ref('2022-2024')
const selectedGasYearRange = ref('2022-2024')

// 用水相关选项
const waterProjectOptions = [
  { label: '生产用水', value: '生产用水' },
  { label: '生活用水', value: '生活用水' }
]

const waterUnitOptions = [
  { label: 'm³', value: 'm³' },
  { label: 'm³/a', value: 'm³/a' },
  { label: 'm³/m²', value: 'm³/m²' },
  { label: 'L', value: 'L' },
  { label: 'L/a', value: 'L/a' }
]

// 用电相关选项
const electricityProjectOptions = [
  { label: '生产用电', value: '生产用电' },
  { label: '非直接生产用电', value: '非直接生产用电' }
]

const electricityUnitOptions = [
  { label: 'kWh', value: 'kWh' },
  { label: 'kWh/a', value: 'kWh/a' },
  { label: 'kWh/m²', value: 'kWh/m²' },
  { label: 'MWh', value: 'MWh' }
]

// 天然气相关选项
const gasProjectOptions = [
  { label: '生产用气', value: '生产用气' },
  { label: '非直接生产用气', value: '非直接生产用气' }
]

const gasUnitOptions = [
  { label: 'm³', value: 'm³' },
  { label: '吨', value: '吨' },
  { label: 'kg', value: 'kg' },
  { label: 'L', value: 'L' }
]


// 获取用水表格列
const getWaterColumns = () => {
  const baseColumns = [
    { 
      title: '项目', 
      key: 'project', 
      width: 150,
      render: (row) => row.isTotal
        ? h('span', { style: 'font-weight: 600' }, row.project)
        : h(NSelect, {
            value: row.project,
            options: waterProjectOptions,
            onUpdateValue: (value) => { row.project = value }
          })
    },
    {
      title: '使用车间',
      key: 'workshop',
      width: 160,
      render: (row) => row.isTotal
        ? h('span', { style: 'font-weight: 600' }, '-')
        : h(NInput, {
            value: row.workshop,
            placeholder: '请输入使用车间',
            onUpdateValue: (value) => { row.workshop = value }
          })
    },
    { 
      title: '单位', 
      key: 'unit', 
      width: 100,
      render: (row) => row.isTotal
        ? h('span', { style: 'font-weight: 600' }, row.unit || '')
        : h(NSelect, {
            value: row.unit,
            options: waterUnitOptions,
            onUpdateValue: (value) => { row.unit = value }
          })
    }
  ]

  // 根据选择的年份范围动态添加列
  const yearRange = selectedWaterYearRange.value.split('-')
  const startYear = parseInt(yearRange[0])
  const endYear = parseInt(yearRange[1])
  
  const yearColumns = []
  for (let year = startYear; year <= endYear; year++) {
    yearColumns.push({
      title: `${year}年用量`,
      key: `amount_${year}`,
      width: 120,
      render: (row) => row.isTotal
        ? h('span', { style: 'font-weight: 600' }, (Number(row[`amount_${year}`] || 0)).toFixed(2))
        : h(NInputNumber, {
            value: row[`amount_${year}`],
            min: 0,
            precision: 2,
            placeholder: '请输入用量',
            onUpdateValue: (value) => { row[`amount_${year}`] = value }
          })
    })
  }

  const actionColumn = {
    title: '操作',
    key: 'action',
    width: 80,
    render: (row, index) => row.isTotal
      ? null
      : h(NButton, {
          size: "small",
          type: "error",
          onClick: () => removeWaterRow(index)
        }, () => '删除')
  }

  return [...baseColumns, ...yearColumns, actionColumn]
}

// 获取用电表格列
const getElectricityColumns = () => {
  const baseColumns = [
    { 
      title: '项目', 
      key: 'project', 
      width: 150,
      render: (row) => row.isTotal
        ? h('span', { style: 'font-weight: 600' }, row.project)
        : h(NSelect, {
            value: row.project,
            options: electricityProjectOptions,
            onUpdateValue: (value) => { row.project = value }
          })
    },
    {
      title: '使用车间',
      key: 'workshop',
      width: 160,
      render: (row) => row.isTotal
        ? h('span', { style: 'font-weight: 600' }, '-')
        : h(NInput, {
            value: row.workshop,
            placeholder: '请输入使用车间',
            onUpdateValue: (value) => { row.workshop = value }
          })
    },
    { 
      title: '单位', 
      key: 'unit', 
      width: 100,
      render: (row) => row.isTotal
        ? h('span', { style: 'font-weight: 600' }, row.unit || '')
        : h(NSelect, {
            value: row.unit,
            options: electricityUnitOptions,
            onUpdateValue: (value) => { row.unit = value }
          })
    }
  ]

  // 根据选择的年份范围动态添加列
  const yearRange = selectedElectricityYearRange.value.split('-')
  const startYear = parseInt(yearRange[0])
  const endYear = parseInt(yearRange[1])
  
  const yearColumns = []
  for (let year = startYear; year <= endYear; year++) {
    yearColumns.push({
      title: `${year}年用量`,
      key: `amount_${year}`,
      width: 120,
      render: (row) => row.isTotal
        ? h('span', { style: 'font-weight: 600' }, (Number(row[`amount_${year}`] || 0)).toFixed(2))
        : h(NInputNumber, {
            value: row[`amount_${year}`],
            min: 0,
            precision: 2,
            placeholder: '请输入用量',
            onUpdateValue: (value) => { row[`amount_${year}`] = value }
          })
    })
  }

  const actionColumn = {
    title: '操作',
    key: 'action',
    width: 80,
    render: (row, index) => row.isTotal
      ? null
      : h(NButton, {
          size: "small",
          type: "error",
          onClick: () => removeElectricityRow(index)
        }, () => '删除')
  }

  return [...baseColumns, ...yearColumns, actionColumn]
}

// 获取天然气表格列
const getGasColumns = () => {
  const baseColumns = [
    { 
      title: '项目', 
      key: 'project', 
      width: 150,
    render: (row) => row.isTotal
      ? h('span', { style: 'font-weight: 600' }, row.project)
      : h(NSelect, {
          value: row.project,
          options: gasProjectOptions,
          onUpdateValue: (value) => { row.project = value }
      })
  },
  {
      title: '使用车间',
      key: 'workshop',
      width: 160,
      render: (row) => row.isTotal
        ? h('span', { style: 'font-weight: 600' }, '-')
        : h(NInput, {
            value: row.workshop,
            placeholder: '请输入使用车间',
            onUpdateValue: (value) => { row.workshop = value }
          })
    },
  { 
      title: '单位', 
      key: 'unit', 
      width: 100,
      render: (row) => row.isTotal
        ? h('span', { style: 'font-weight: 600' }, row.unit || '')
        : h(NSelect, {
            value: row.unit,
            options: gasUnitOptions,
            onUpdateValue: (value) => { row.unit = value }
          })
    }
  ]

  // 根据选择的年份范围动态添加列
  const yearRange = selectedGasYearRange.value.split('-')
  const startYear = parseInt(yearRange[0])
  const endYear = parseInt(yearRange[1])
  
  const yearColumns = []
  for (let year = startYear; year <= endYear; year++) {
    yearColumns.push({
      title: `${year}年用量`,
      key: `amount_${year}`,
    width: 120,
    render: (row) => row.isTotal
      ? h('span', { style: 'font-weight: 600' }, (Number(row[`amount_${year}`] || 0)).toFixed(2))
      : h(NInputNumber, {
          value: row[`amount_${year}`],
        min: 0,
        precision: 2,
          placeholder: '请输入用量',
          onUpdateValue: (value) => { row[`amount_${year}`] = value }
        })
    })
  }

  const actionColumn = {
    title: '操作', 
    key: 'action', 
    width: 80,
    render: (row, index) => row.isTotal
      ? null
      : h(NButton, {
          size: "small",
          type: "error",
          onClick: () => removeGasRow(index)
        }, () => '删除')
  }

  return [...baseColumns, ...yearColumns, actionColumn]
}


// 事件处理函数
const onWaterYearRangeChange = async (range) => {
  selectedWaterYearRange.value = range
  await loadWaterData()
}

const onElectricityYearRangeChange = async (range) => {
  selectedElectricityYearRange.value = range
  await loadElectricityData()
}

const onGasYearRangeChange = async (range) => {
  selectedGasYearRange.value = range
  await loadGasData()
}

// 用水相关操作
const addWaterRow = () => {
  const newRow = {
    id: Date.now(),
    project: '',
    workshop: '',
    unit: 'm³'
  }
  
  // 根据选择的年份范围初始化数据
  const yearRange = selectedWaterYearRange.value.split('-')
  const startYear = parseInt(yearRange[0])
  const endYear = parseInt(yearRange[1])
  
  for (let year = startYear; year <= endYear; year++) {
    newRow[`amount_${year}`] = null
  }
  
  formData.value.water.push(newRow)
}

const removeWaterRow = (index) => {
  formData.value.water.splice(index, 1)
}

const submitWaterData = async () => {
  if (!props.enterpriseId) {
    message.warning('企业ID不能为空')
    return
  }
  
  try {
    const items = formData.value.water
      .filter(row => !row.isTotal && row.project && row.unit)
      .map(row => {
        const item = {
          project: row.project,
          workshop: row.workshop || null,
          unit: row.unit
        }
        // 添加年份数据
        const yearRange = selectedWaterYearRange.value.split('-')
        const startYear = parseInt(yearRange[0])
        const endYear = parseInt(yearRange[1])
        for (let year = startYear; year <= endYear; year++) {
          const amount = row[`amount_${year}`]
          if (amount !== null && amount !== undefined && amount !== '') {
            item[`amount_${year}`] = amount
          } else {
            item[`amount_${year}`] = null
          }
        }
        return item
      })
    
    await api.pcb.production.saveThreeYearsWaterConsumption(
      props.enterpriseId,
      selectedWaterYearRange.value,
      items
    )
    
    message.success('用水数据提交成功')
    await new Promise(resolve => setTimeout(resolve, 300))
    await loadWaterData()
  } catch (error) {
    console.error('提交用水数据失败:', error)
    message.error('提交用水数据失败: ' + (error.message || '未知错误'))
  }
}

// 用电相关操作
const addElectricityRow = () => {
  const newRow = {
    id: Date.now(),
    project: '',
    workshop: '',
    unit: 'kWh'
  }
  
  // 根据选择的年份范围初始化数据
  const yearRange = selectedElectricityYearRange.value.split('-')
  const startYear = parseInt(yearRange[0])
  const endYear = parseInt(yearRange[1])
  
  for (let year = startYear; year <= endYear; year++) {
    newRow[`amount_${year}`] = null
  }
  
  formData.value.electricity.push(newRow)
}

const removeElectricityRow = (index) => {
  formData.value.electricity.splice(index, 1)
}

const submitElectricityData = async () => {
  if (!props.enterpriseId) {
    message.warning('企业ID不能为空')
    return
  }
  
  try {
    const items = formData.value.electricity
      .filter(row => !row.isTotal && row.project && row.unit)
      .map(row => {
        const item = {
          project: row.project,
          workshop: row.workshop || null,
          unit: row.unit
        }
        // 添加年份数据
        const yearRange = selectedElectricityYearRange.value.split('-')
        const startYear = parseInt(yearRange[0])
        const endYear = parseInt(yearRange[1])
        for (let year = startYear; year <= endYear; year++) {
          const amount = row[`amount_${year}`]
          if (amount !== null && amount !== undefined && amount !== '') {
            item[`amount_${year}`] = amount
          } else {
            item[`amount_${year}`] = null
          }
        }
        return item
      })
    
    await api.pcb.production.saveThreeYearsElectricityConsumption(
      props.enterpriseId,
      selectedElectricityYearRange.value,
      items
    )
    
    message.success('用电数据提交成功')
    await new Promise(resolve => setTimeout(resolve, 300))
    await loadElectricityData()
  } catch (error) {
    console.error('提交用电数据失败:', error)
    message.error('提交用电数据失败: ' + (error.message || '未知错误'))
  }
}

// 天然气相关操作
const addGasRow = () => {
  const newRow = {
    id: Date.now(),
    project: '',
    workshop: '',
    unit: 'm³'
  }
  
  // 根据选择的年份范围初始化数据
  const yearRange = selectedGasYearRange.value.split('-')
  const startYear = parseInt(yearRange[0])
  const endYear = parseInt(yearRange[1])
  
  for (let year = startYear; year <= endYear; year++) {
    newRow[`amount_${year}`] = null
  }
  
  formData.value.gas.push(newRow)
}

const removeGasRow = (index) => {
  formData.value.gas.splice(index, 1)
}

const submitGasData = async () => {
  if (!props.enterpriseId) {
    message.warning('企业ID不能为空')
    return
  }
  
  try {
    const items = formData.value.gas
      .filter(row => !row.isTotal && row.project && row.unit)
      .map(row => {
        const item = {
          project: row.project,
          workshop: row.workshop || null,
          unit: row.unit
        }
        // 添加年份数据
        const yearRange = selectedGasYearRange.value.split('-')
        const startYear = parseInt(yearRange[0])
        const endYear = parseInt(yearRange[1])
        for (let year = startYear; year <= endYear; year++) {
          const amount = row[`amount_${year}`]
          if (amount !== null && amount !== undefined && amount !== '') {
            item[`amount_${year}`] = amount
          } else {
            item[`amount_${year}`] = null
          }
        }
        return item
      })
    
    await api.pcb.production.saveThreeYearsGasConsumption(
      props.enterpriseId,
      selectedGasYearRange.value,
      items
    )
    
    message.success('天然气数据提交成功')
    await new Promise(resolve => setTimeout(resolve, 300))
    await loadGasData()
  } catch (error) {
    console.error('提交天然气数据失败:', error)
    message.error('提交天然气数据失败: ' + (error.message || '未知错误'))
  }
}


// 加载数据
const loadingWater = ref(false)
const loadingElectricity = ref(false)
const loadingGas = ref(false)

// 辅助函数：从响应数据中提取年份数据
const getYearData = (item, yearRange) => {
  const data = {}
  const [startYear, endYear] = yearRange.split('-').map(y => parseInt(y))
  for (let year = startYear; year <= endYear; year++) {
    const amount = item[`amount_${year}`]
    if (amount !== null && amount !== undefined && amount !== '') {
      data[`amount_${year}`] = typeof amount === 'number' ? amount : parseFloat(amount)
    } else {
      data[`amount_${year}`] = null
    }
  }
  return data
}

const loadWaterData = async () => {
  if (!props.enterpriseId) return
  
  try {
    loadingWater.value = true
    const response = await api.pcb.production.getThreeYearsWaterConsumption(
      props.enterpriseId,
      selectedWaterYearRange.value
    )
    
    // 处理响应数据，兼容不同的响应格式
    let dataArray = []
    if (response) {
      if (Array.isArray(response.data)) {
        dataArray = response.data
      } else if (response.data && Array.isArray(response.data.data)) {
        dataArray = response.data.data
      } else if (Array.isArray(response)) {
        dataArray = response
      }
    }
    
    if (dataArray.length > 0) {
      formData.value.water = dataArray.map((item, idx) => ({
        id: item.id || Date.now() + idx,
        project: item.project || '',
        workshop: item.workshop || '',
        unit: item.unit || 'm³',
        ...getYearData(item, selectedWaterYearRange.value)
      }))
    } else {
      if (formData.value.water.length === 0) {
        addWaterRow()
      }
    }
  } catch (error) {
    console.error('加载用水数据失败:', error)
    message.warning('加载用水数据失败，已初始化空表格')
    if (formData.value.water.length === 0) {
      addWaterRow()
    }
  } finally {
    loadingWater.value = false
  }
}

const loadElectricityData = async () => {
  if (!props.enterpriseId) return
  
  try {
    loadingElectricity.value = true
    const response = await api.pcb.production.getThreeYearsElectricityConsumption(
      props.enterpriseId,
      selectedElectricityYearRange.value
    )
    
    // 处理响应数据，兼容不同的响应格式
    let dataArray = []
    if (response) {
      if (Array.isArray(response.data)) {
        dataArray = response.data
      } else if (response.data && Array.isArray(response.data.data)) {
        dataArray = response.data.data
      } else if (Array.isArray(response)) {
        dataArray = response
      }
    }
    
    if (dataArray.length > 0) {
      formData.value.electricity = dataArray.map((item, idx) => ({
        id: item.id || Date.now() + idx,
        project: item.project || '',
        workshop: item.workshop || '',
        unit: item.unit || 'kWh',
        ...getYearData(item, selectedElectricityYearRange.value)
      }))
    } else {
      if (formData.value.electricity.length === 0) {
        addElectricityRow()
      }
    }
  } catch (error) {
    console.error('加载用电数据失败:', error)
    message.warning('加载用电数据失败，已初始化空表格')
    if (formData.value.electricity.length === 0) {
      addElectricityRow()
    }
  } finally {
    loadingElectricity.value = false
  }
}

const loadGasData = async () => {
  if (!props.enterpriseId) return
  
  try {
    loadingGas.value = true
    const response = await api.pcb.production.getThreeYearsGasConsumption(
      props.enterpriseId,
      selectedGasYearRange.value
    )
    
    // 处理响应数据，兼容不同的响应格式
    let dataArray = []
    if (response) {
      if (Array.isArray(response.data)) {
        dataArray = response.data
      } else if (response.data && Array.isArray(response.data.data)) {
        dataArray = response.data.data
      } else if (Array.isArray(response)) {
        dataArray = response
      }
    }
    
    if (dataArray.length > 0) {
      formData.value.gas = dataArray.map((item, idx) => ({
        id: item.id || Date.now() + idx,
        project: item.project || '',
        workshop: item.workshop || '',
        unit: item.unit || 'm³',
        ...getYearData(item, selectedGasYearRange.value)
      }))
    } else {
      if (formData.value.gas.length === 0) {
        addGasRow()
      }
    }
  } catch (error) {
    console.error('加载天然气数据失败:', error)
    message.warning('加载天然气数据失败，已初始化空表格')
    if (formData.value.gas.length === 0) {
      addGasRow()
    }
  } finally {
    loadingGas.value = false
  }
}

// 确保数据结构完整
watch(() => props.modelValue, (newVal) => {
  if (newVal) {
    if (!newVal.water) {
      newVal.water = []
    }
    if (!newVal.electricity) {
      newVal.electricity = []
    }
    if (!newVal.gas) {
      newVal.gas = []
    }
    
    // 如果表格为空，添加一条空白记录
    if (newVal.water.length === 0) {
      addWaterRow()
    }
    if (newVal.electricity.length === 0) {
      addElectricityRow()
    }
    if (newVal.gas.length === 0) {
      addGasRow()
    }
  }
}, { immediate: true, deep: true })

// 组件挂载时加载数据
onMounted(() => {
  if (props.enterpriseId) {
    loadWaterData()
    loadElectricityData()
    loadGasData()
  }
})

// 计算用气表格展示数据（含三类总计行）
const gasTableData = computed(() => {
  const yearRange = selectedGasYearRange.value.split('-')
  const startYear = parseInt(yearRange[0])
  const endYear = parseInt(yearRange[1])
  const rows = formData.value.gas || []

  const sumByProject = (project, label) => {
    const total = { id: `total_${project}`, isTotal: true, project: label, unit: 'm³' }
    for (let y = startYear; y <= endYear; y++) {
      let s = 0
      rows.forEach(r => {
        if (r.project === project) {
          const v = Number(r[`amount_${y}`] || 0)
          if (!isNaN(v)) s += v
        }
      })
      total[`amount_${y}`] = s
    }
    return total
  }

  const totalProd = sumByProject('生产用气', '生产用气总计')
  const totalNonProd = sumByProject('非直接生产用气', '非直接生产用气总计')
  const grand = { id: 'total_all_gas', isTotal: true, project: '总用气量', unit: 'm³' }
  for (let y = startYear; y <= endYear; y++) {
    grand[`amount_${y}`] = Number(totalProd[`amount_${y}`] || 0) + Number(totalNonProd[`amount_${y}`] || 0)
  }

  return [...rows, totalProd, totalNonProd, grand]
})

// 计算用电表格展示数据（含三类总计行）
const electricityTableData = computed(() => {
  const yearRange = selectedElectricityYearRange.value.split('-')
  const startYear = parseInt(yearRange[0])
  const endYear = parseInt(yearRange[1])
  const rows = formData.value.electricity || []

  const sumByProject = (project, label) => {
    const total = { id: `total_${project}`, isTotal: true, project: label, unit: 'kWh' }
    for (let y = startYear; y <= endYear; y++) {
      let s = 0
      rows.forEach(r => {
        if (r.project === project) {
          const v = Number(r[`amount_${y}`] || 0)
          if (!isNaN(v)) s += v
        }
      })
      total[`amount_${y}`] = s
    }
    return total
  }

  const totalProd = sumByProject('生产用电', '生产用电总计')
  const totalNonProd = sumByProject('非直接生产用电', '非直接生产用电总计')
  const grand = { id: 'total_all_ele', isTotal: true, project: '总用电量', unit: 'kWh' }
  for (let y = startYear; y <= endYear; y++) {
    grand[`amount_${y}`] = Number(totalProd[`amount_${y}`] || 0) + Number(totalNonProd[`amount_${y}`] || 0)
  }

  return [...rows, totalProd, totalNonProd, grand]
})

// 计算用水表格展示数据（含三类总计行）
const waterTableData = computed(() => {
  const yearRange = selectedWaterYearRange.value.split('-')
  const startYear = parseInt(yearRange[0])
  const endYear = parseInt(yearRange[1])
  const rows = formData.value.water || []

  const sumByProject = (project) => {
    const total = { id: `total_${project}`, isTotal: true, project: `${project}总计`, unit: 'm³' }
    for (let y = startYear; y <= endYear; y++) {
      let s = 0
      rows.forEach(r => {
        if (r.project === project) {
          const v = Number(r[`amount_${y}`] || 0)
          if (!isNaN(v)) s += v
        }
      })
      total[`amount_${y}`] = s
    }
    return total
  }

  const totalProd = sumByProject('生产用水')
  const totalLife = sumByProject('生活用水')
  const grand = { id: 'total_all', isTotal: true, project: '总用水量', unit: 'm³' }
  for (let y = startYear; y <= endYear; y++) {
    grand[`amount_${y}`] = Number(totalProd[`amount_${y}`] || 0) + Number(totalLife[`amount_${y}`] || 0)
  }

  return [...rows, totalProd, totalLife, grand]
})
</script>

<style scoped>
.resource-consumption-form {
  padding: 16px 0;
}

.water-actions,
.electricity-actions,
.gas-actions {
  text-align: center;
  padding: 16px 0;
  border-top: 1px solid #e0e0e6;
}

.year-range-selector {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 表格样式优化 */
:deep(.n-data-table) {
  border-radius: 6px;
}

:deep(.n-data-table .n-data-table-th) {
  background: #f8f9fa;
  font-weight: 600;
}

:deep(.n-data-table .n-data-table-td) {
  padding: 8px 12px;
}

/* 卡片样式 */
:deep(.n-card-header) {
  background: #f8f9fa;
  border-bottom: 1px solid #e0e0e6;
}

:deep(.n-card-header .n-card-header__main) {
  font-weight: 600;
  color: #1f2937;
  display: inline-block;
  border-bottom: 2px solid #ff8c00;
  padding-bottom: 8px;
}

/* 按钮样式 */
:deep(.n-button--primary) {
  background: #1890ff;
  border-color: #1890ff;
}

:deep(.n-button--primary:hover) {
  background: #40a9ff;
  border-color: #40a9ff;
}

/* 输入框样式 */
:deep(.n-input-number) {
  width: 100%;
}

/* 表格模块样式 */
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

/* 卡片标题样式 */
:deep(.n-card-header .n-card-header__main) {
  font-weight: 600;
  color: #333;
  display: inline-block;
  border-bottom: 2px solid #ff8c00;
  padding-bottom: 8px;
}

:deep(.n-select) {
  width: 100%;
}

/* 标签样式 */
:deep(.n-tag) {
  margin-left: 4px;
}
</style>