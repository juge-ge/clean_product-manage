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
        :data="formData.water"
        :row-key="row => row.id"
        :pagination="false"
        size="small"
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
        :data="formData.electricity"
        :row-key="row => row.id"
        :pagination="false"
        size="small"
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
            :data="formData.gas"
            :row-key="row => row.id"
            :pagination="false"
            size="small"
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
import { pcbApi } from '@/api/pcb'

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
  { label: '生活用水', value: '生活用水' },
  { label: '总用水量', value: '总用水量' },
  { label: '办公用水', value: '办公用水' },
  { label: '冷却用水', value: '冷却用水' },
  { label: '清洗用水', value: '清洗用水' }
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
  { label: '生产车间用电', value: '生产车间用电' },
  { label: '辅助生产用电', value: '辅助生产用电' },
  { label: '办公用电', value: '办公用电' },
  { label: '生活用电', value: '生活用电' },
  { label: '照明用电', value: '照明用电' },
  { label: '空调用电', value: '空调用电' }
]

const electricityUnitOptions = [
  { label: 'kWh', value: 'kWh' },
  { label: 'kWh/a', value: 'kWh/a' },
  { label: 'kWh/m²', value: 'kWh/m²' },
  { label: 'MWh', value: 'MWh' }
]

// 天然气相关选项
const gasProjectOptions = [
  { label: '锅炉天然气', value: '锅炉天然气' },
  { label: '工业煤气', value: '工业煤气' },
  { label: '生活用气', value: '生活用气' },
  { label: '生产用气', value: '生产用气' }
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
      render: (row) => h(NSelect, {
        value: row.project,
        options: waterProjectOptions,
        onUpdateValue: (value) => { row.project = value }
      })
    },
    { 
      title: '单位', 
      key: 'unit', 
      width: 100,
      render: (row) => h(NSelect, {
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
      render: (row) => h(NInputNumber, {
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
    render: (row, index) => h(NButton, {
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
      render: (row) => h(NSelect, {
        value: row.project,
        options: electricityProjectOptions,
        onUpdateValue: (value) => { row.project = value }
      })
    },
    { 
      title: '单位', 
      key: 'unit', 
      width: 100,
      render: (row) => h(NSelect, {
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
      render: (row) => h(NInputNumber, {
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
    render: (row, index) => h(NButton, {
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
    render: (row) => h(NSelect, {
        value: row.project,
        options: gasProjectOptions,
        onUpdateValue: (value) => { row.project = value }
    })
  },
  { 
      title: '单位', 
      key: 'unit', 
      width: 100,
      render: (row) => h(NSelect, {
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
    render: (row) => h(NInputNumber, {
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
    render: (row, index) => h(NButton, {
      size: "small",
      type: "error",
      onClick: () => removeGasRow(index)
    }, () => '删除')
  }

  return [...baseColumns, ...yearColumns, actionColumn]
}


// 事件处理函数
const onWaterYearRangeChange = (range) => {
  selectedWaterYearRange.value = range
  // 重新计算表格列
}

const onElectricityYearRangeChange = (range) => {
  selectedElectricityYearRange.value = range
  // 重新计算表格列
}

const onGasYearRangeChange = (range) => {
  selectedGasYearRange.value = range
  // 重新计算表格列
}

// 用水相关操作
const addWaterRow = () => {
  const newRow = {
    id: Date.now(),
    project: '',
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

const submitWaterData = () => {
  message.success('用水数据提交成功')
}

// 用电相关操作
const addElectricityRow = () => {
  const newRow = {
    id: Date.now(),
    project: '',
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

const submitElectricityData = () => {
  message.success('用电数据提交成功')
}

// 天然气相关操作
const addGasRow = () => {
  const newRow = {
    id: Date.now(),
    project: '',
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

const submitGasData = () => {
  message.success('天然气数据提交成功')
}


// 加载数据
const loading = ref(false)

const loadData = async () => {
  try {
    loading.value = true
    const response = await pcbApi.resourceConsumption.getAllData(props.enterpriseId)
    
    if (response.data && response.data.data) {
      const data = response.data.data
      
      // 转换用水数据格式
      if (data.water_records) {
        formData.value.water = data.water_records.map(record => ({
          id: record.id,
          project: record.project,
          unit: record.unit,
          amount_2020: record.amount_2020,
          amount_2021: record.amount_2021,
          amount_2022: record.amount_2022,
          amount_2023: record.amount_2023,
          amount_2024: record.amount_2024
        }))
      }
      
      // 转换用电数据格式
      if (data.electricity_records) {
        formData.value.electricity = data.electricity_records.map(record => ({
          id: record.id,
          project: record.project,
          unit: record.unit,
          amount_2020: record.amount_2020,
          amount_2021: record.amount_2021,
          amount_2022: record.amount_2022,
          amount_2023: record.amount_2023,
          amount_2024: record.amount_2024
        }))
      }
      
      // 转换天然气数据格式
      if (data.gas_records) {
        formData.value.gas = data.gas_records.map(record => ({
          id: record.id,
          project: record.project,
          unit: record.unit,
          amount_2020: record.amount_2020,
          amount_2021: record.amount_2021,
          amount_2022: record.amount_2022,
          amount_2023: record.amount_2023,
          amount_2024: record.amount_2024,
          gasType: record.gas_type,
          source: record.source,
          remark: record.remark
        }))
      }
    }
  } catch (error) {
    console.error('加载资源能源消耗数据失败:', error)
    message.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

// 保存数据
const saveData = async () => {
  try {
    loading.value = true
    
    // 转换数据格式
    const requestData = {
      water: {
        records: formData.value.water.map(record => ({
          project: record.project,
          unit: record.unit,
          amount_2020: record.amount_2020,
          amount_2021: record.amount_2021,
          amount_2022: record.amount_2022,
          amount_2023: record.amount_2023,
          amount_2024: record.amount_2024
        }))
      },
      electricity: {
        records: formData.value.electricity.map(record => ({
          project: record.project,
          unit: record.unit,
          amount_2020: record.amount_2020,
          amount_2021: record.amount_2021,
          amount_2022: record.amount_2022,
          amount_2023: record.amount_2023,
          amount_2024: record.amount_2024
        }))
      },
      gas: {
        records: formData.value.gas.map(record => ({
          project: record.project,
          unit: record.unit,
          amount_2020: record.amount_2020,
          amount_2021: record.amount_2021,
          amount_2022: record.amount_2022,
          amount_2023: record.amount_2023,
          amount_2024: record.amount_2024,
          gas_type: record.gasType,
          source: record.source,
          remark: record.remark
        }))
      }
    }
    
    const response = await pcbApi.resourceConsumption.saveAllData(props.enterpriseId, requestData)
    
    if (response.data && response.data.code === 200) {
      message.success('数据保存成功')
    } else {
      message.error('数据保存失败')
    }
  } catch (error) {
    console.error('保存资源能源消耗数据失败:', error)
    message.error('保存数据失败')
  } finally {
    loading.value = false
  }
}

// 暴露保存方法给父组件
defineExpose({
  saveData
})

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
  loadData()
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