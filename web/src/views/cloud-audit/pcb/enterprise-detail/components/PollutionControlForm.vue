<template>
  <div class="pollution-control-form">
    <n-space vertical :size="16">
      <!-- 废水产生分析 -->
      <n-card title="废水产生分析" size="small" class="sub-module">
        <template #header-extra>
          <n-button type="primary" size="small" @click="addWastewaterRow">
            <template #icon>
              <TheIcon icon="carbon:add" />
            </template>
            添加废水类型
          </n-button>
        </template>
        
        <n-data-table
          :columns="wastewaterColumns"
          :data="formData.wastewater"
          :row-key="row => row.id"
          :pagination="false"
          size="small"
          :row-props="getWastewaterRowProps"
          :loading="loadingWastewater"
          class="sub-module"
        />
        
        <div class="wastewater-actions mt-4">
          <n-space>
            <n-button type="primary" @click="submitWastewaterData">
              <template #icon>
                <TheIcon icon="carbon:checkmark" />
              </template>
              提交
            </n-button>
          </n-space>
        </div>
      </n-card>

      <!-- 企业近三年废水情况统计 -->
      <n-card title="企业近三年废水情况统计" size="small" class="sub-module">
        <template #header-extra>
          <n-space>
            <div class="year-range-selector">
              <n-text strong>年份范围：</n-text>
              <n-select
                v-model:value="selectedWastewaterYearRange"
                :options="yearRangeOptions"
                style="width: 200px"
                @update:value="onWastewaterYearRangeChange"
              />
            </div>
            <n-button type="primary" size="small" @click="addWastewaterStatRow">
              <template #icon>
                <TheIcon icon="carbon:add" />
              </template>
              添加行
            </n-button>
          </n-space>
        </template>

        <n-data-table
          :columns="getWastewaterStatColumns()"
          :data="wastewaterStatTableData"
          :row-key="row => row.id"
          :pagination="false"
          size="small"
          :loading="loadingWastewaterStat"
        />
        
        <div class="wastewater-stat-actions mt-4">
          <n-space>
            <n-button type="primary" @click="submitWastewaterStatData">
              <template #icon>
                <TheIcon icon="carbon:checkmark" />
              </template>
              提交
            </n-button>
          </n-space>
        </div>
      </n-card>

      <!-- 废气产生情况 -->
      <n-card title="废气产生情况" size="small" class="sub-module">
        <template #header-extra>
          <n-button type="primary" size="small" @click="addWasteGasRow">
            <template #icon>
              <TheIcon icon="carbon:add" />
            </template>
            添加废气类型
          </n-button>
        </template>
        
        <n-data-table
          :columns="wasteGasColumns"
          :data="formData.wasteGas"
          :row-key="row => row.id"
          :pagination="false"
          size="small"
          :row-props="getWasteGasRowProps"
          :loading="loadingWasteGas"
          class="sub-module"
        />
        
        <div class="waste-gas-actions mt-4">
          <n-space>
            <n-button type="primary" @click="submitWasteGasData">
              <template #icon>
                <TheIcon icon="carbon:checkmark" />
              </template>
              提交
            </n-button>
          </n-space>
        </div>
      </n-card>
    </n-space>
  </div>
</template>

<script setup>
import { computed, h, watch, ref, onMounted } from 'vue'
import { 
  NSpace,
  NCard,
  NDataTable, 
  NButton, 
  NInput,
  NInputNumber, 
  NSelect,
  NText,
  useMessage
} from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'
import api from '@/api'

const message = useMessage()

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      wastewater: [],
      wasteGas: [],
      wastewaterStats: []
    })
  },
  enterpriseId: {
    type: Number,
    default: null
  }
})

const emit = defineEmits(['update:modelValue'])

const formData = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// 加载状态
const loadingWastewater = ref(false)
const loadingWastewaterStat = ref(false)
const loadingWasteGas = ref(false)

// 年份范围（与资源能源消耗一致）
const yearRangeOptions = [
  { label: '2022-2024', value: '2022-2024' },
  { label: '2021-2023', value: '2021-2023' },
  { label: '2020-2022', value: '2020-2022' }
]
const selectedWastewaterYearRange = ref('2022-2024')

// 废水产生分析表格列
const wastewaterColumns = [
  {
    title: '废水类别',
    key: 'category',
    width: 150,
    render: (row) => h(NInput, {
      value: row.category,
      placeholder: '如：含镍废水',
      onUpdateValue: (value) => { row.category = value }
    })
  },
  {
    title: '来源',
    key: 'source',
    width: 200,
    render: (row) => h(NInput, {
      value: row.source,
      type: 'textarea',
      placeholder: '如：电镀镍金、化学沉镍、化金等工序产生的废水及处理工序产生废气的废水',
      onUpdateValue: (value) => { row.source = value }
    })
  },
  {
    title: '主要污染物',
    key: 'pollutants',
    width: 200,
    render: (row) => h(NInput, {
      value: row.pollutants,
      type: 'textarea',
      placeholder: '如：pH、Ni²⁺、SS、CODcr、NH₄⁺、总氮、Cu²⁺、石油类',
      onUpdateValue: (value) => { row.pollutants = value }
    })
  },
  {
    title: '处置方式',
    key: 'disposal',
    width: 300,
    render: (row) => h(NInput, {
      value: row.disposal,
      type: 'textarea',
      placeholder: '如：管道收集分别收集至化学镍调节池和电镀镍废水调节池，化镍废水经过间歇芬顿反应沉淀处理后与电镀废水一并经过 "絮凝沉淀 + 芬顿 + 絮凝沉淀 + 离子交换" 达标处理后独立排放口计量排放至综合废水调节池',
      onUpdateValue: (value) => { row.disposal = value }
    })
  },
  {
    title: '操作',
    key: 'action',
    width: 80,
    render: (row, index) => h(NButton, {
      size: "small",
      type: "error",
      onClick: () => removeWastewaterRow(index)
    }, () => '删除')
  }
]

// 废水统计（仿用水统计，文案改为“废水”）
const wastewaterProjectOptions = [
  { label: '生产废水', value: '生产废水' },
  { label: '生活废水', value: '生活废水' }
]

const wastewaterUnitOptions = [
  { label: 'm³', value: 'm³' },
  { label: 'm³/a', value: 'm³/a' },
  { label: 'm³/m²', value: 'm³/m²' },
  { label: 'L', value: 'L' },
  { label: 'L/a', value: 'L/a' }
]

const getWastewaterStatColumns = () => {
  const baseColumns = [
    {
      title: '项目',
      key: 'project',
      width: 150,
      render: (row) => row.isTotal
        ? h('span', { style: 'font-weight: 600' }, row.project)
        : h(NSelect, {
            value: row.project,
            options: wastewaterProjectOptions,
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
            options: wastewaterUnitOptions,
            onUpdateValue: (value) => { row.unit = value }
          })
    }
  ]

  const yearRange = selectedWastewaterYearRange.value.split('-')
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
          size: 'small',
          type: 'error',
          onClick: () => removeWastewaterStatRow(index)
        }, () => '删除')
  }

  return [...baseColumns, ...yearColumns, actionColumn]
}

// 废气产生情况表格列
const wasteGasColumns = [
  {
    title: '序号',
    key: 'index',
    width: 60,
    render: (row, index) => index + 1
  },
  {
    title: '种类',
    key: 'type',
    width: 200,
    render: (row) => h(NInput, {
      value: row.type,
      type: 'textarea',
      placeholder: '如：电镀镍金酸性废气',
      onUpdateValue: (value) => { row.type = value }
    })
  },
  {
    title: '主要污染物',
    key: 'pollutants',
    width: 150,
    render: (row) => h(NInput, {
      value: row.pollutants,
      placeholder: '如：硫酸雾',
      onUpdateValue: (value) => { row.pollutants = value }
    })
  },
  {
    title: '产生部位',
    key: 'location',
    width: 250,
    render: (row) => h(NInput, {
      value: row.location,
      type: 'textarea',
      placeholder: '如：电镀镍金及化学沉金线中电镀镍、化学沉镍工序产生的酸性废气',
      onUpdateValue: (value) => { row.location = value }
    })
  },
  {
    title: '处理方法',
    key: 'treatment',
    width: 250,
    render: (row) => h(NInput, {
      value: row.treatment,
      type: 'textarea',
      placeholder: '如：统一收集至 B 栋楼顶经 "碱（氢氧化钠）喷淋" 处理达标至 25m 排气筒 G1 达标排气',
      onUpdateValue: (value) => { row.treatment = value }
    })
  },
  {
    title: '操作',
    key: 'action',
    width: 80,
    render: (row, index) => h(NButton, {
      size: "small",
      type: "error",
      onClick: () => removeWasteGasRow(index)
    }, () => '删除')
  }
]

// 添加废水行
const addWastewaterRow = () => {
  formData.value.wastewater.push({
    id: Date.now(),
    category: '',
    source: '',
    pollutants: '',
    disposal: ''
  })
}

// 废水统计行操作
const addWastewaterStatRow = () => {
  if (!formData.value.wastewaterStats) {
    formData.value.wastewaterStats = []
  }
  const newRow = {
    id: Date.now(),
    project: '',
    workshop: '',
    unit: 'm³'
  }
  const yearRange = selectedWastewaterYearRange.value.split('-')
  const startYear = parseInt(yearRange[0])
  const endYear = parseInt(yearRange[1])
  for (let y = startYear; y <= endYear; y++) {
    newRow[`amount_${y}`] = null
  }
  formData.value.wastewaterStats.push(newRow)
}

const removeWastewaterStatRow = (index) => {
  if (!formData.value.wastewaterStats) return
  formData.value.wastewaterStats.splice(index, 1)
}

// 添加废气行
const addWasteGasRow = () => {
  formData.value.wasteGas.push({
    id: Date.now(),
    type: '',
    pollutants: '',
    location: '',
    treatment: ''
  })
}

// 删除废水行
const removeWastewaterRow = (index) => {
  formData.value.wastewater.splice(index, 1)
}

// 删除废气行
const removeWasteGasRow = (index) => {
  formData.value.wasteGas.splice(index, 1)
}

// 获取废水行属性（增加行高）
const getWastewaterRowProps = (row, index) => {
  return {
    style: 'min-height: 80px;'
  }
}

// 获取废气行属性（增加行高）
const getWasteGasRowProps = (row, index) => {
  return {
    style: 'min-height: 80px;'
  }
}

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

// 加载废水产生分析数据
const loadWastewaterData = async () => {
  if (!props.enterpriseId) return
  
  try {
    loadingWastewater.value = true
    const response = await api.pcb.pollutionControl.getWastewaterAnalysis(props.enterpriseId)
    
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
      formData.value.wastewater = dataArray.map((item, idx) => ({
        id: item.id || Date.now() + idx,
        category: item.category || '',
        source: item.source || '',
        pollutants: item.pollutants || '',
        disposal: item.disposal || ''
      }))
    } else {
      if (formData.value.wastewater.length === 0) {
        addWastewaterRow()
      }
    }
  } catch (error) {
    console.error('加载废水产生分析数据失败:', error)
    message.warning('加载废水产生分析数据失败，已初始化空表格')
    if (formData.value.wastewater.length === 0) {
      addWastewaterRow()
    }
  } finally {
    loadingWastewater.value = false
  }
}

// 加载近三年废水情况统计数据
const loadWastewaterStatData = async () => {
  if (!props.enterpriseId) return
  
  try {
    loadingWastewaterStat.value = true
    const response = await api.pcb.pollutionControl.getThreeYearsWastewaterStat(
      props.enterpriseId,
      selectedWastewaterYearRange.value
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
      formData.value.wastewaterStats = dataArray.map((item, idx) => ({
        id: item.id || Date.now() + idx,
        project: item.project || '',
        workshop: item.workshop || '',
        unit: item.unit || 'm³',
        ...getYearData(item, selectedWastewaterYearRange.value)
      }))
    } else {
      if (formData.value.wastewaterStats.length === 0) {
        addWastewaterStatRow()
      }
    }
  } catch (error) {
    console.error('加载近三年废水情况统计数据失败:', error)
    message.warning('加载近三年废水情况统计数据失败，已初始化空表格')
    if (formData.value.wastewaterStats.length === 0) {
      addWastewaterStatRow()
    }
  } finally {
    loadingWastewaterStat.value = false
  }
}

// 加载废气产生情况数据
const loadWasteGasData = async () => {
  if (!props.enterpriseId) return
  
  try {
    loadingWasteGas.value = true
    const response = await api.pcb.pollutionControl.getWasteGasAnalysis(props.enterpriseId)
    
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
      formData.value.wasteGas = dataArray.map((item, idx) => ({
        id: item.id || Date.now() + idx,
        type: item.type || item.gas_type || '',
        pollutants: item.pollutants || '',
        location: item.location || '',
        treatment: item.treatment || ''
      }))
    } else {
      if (formData.value.wasteGas.length === 0) {
        addWasteGasRow()
      }
    }
  } catch (error) {
    console.error('加载废气产生情况数据失败:', error)
    message.warning('加载废气产生情况数据失败，已初始化空表格')
    if (formData.value.wasteGas.length === 0) {
      addWasteGasRow()
    }
  } finally {
    loadingWasteGas.value = false
  }
}

// 提交废水产生分析数据
const submitWastewaterData = async () => {
  if (!props.enterpriseId) {
    message.warning('企业ID不能为空')
    return
  }
  
  try {
    const items = formData.value.wastewater
      .filter(row => row.category)
      .map(row => ({
        category: row.category,
        source: row.source || '',
        pollutants: row.pollutants || '',
        disposal: row.disposal || ''
      }))
    
    await api.pcb.pollutionControl.batchSaveWastewaterAnalysis(props.enterpriseId, items)
    
    message.success('废水产生分析数据提交成功')
    await new Promise(resolve => setTimeout(resolve, 300))
    await loadWastewaterData()
  } catch (error) {
    console.error('提交废水产生分析数据失败:', error)
    message.error('提交废水产生分析数据失败: ' + (error.message || '未知错误'))
  }
}

// 提交近三年废水情况统计数据
const submitWastewaterStatData = async () => {
  if (!props.enterpriseId) {
    message.warning('企业ID不能为空')
    return
  }
  
  try {
    const items = formData.value.wastewaterStats
      .filter(row => !row.isTotal && row.project && row.unit)
      .map(row => {
        const item = {
          project: row.project,
          workshop: row.workshop || null,
          unit: row.unit
        }
        // 添加年份数据
        const yearRange = selectedWastewaterYearRange.value.split('-')
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
    
    await api.pcb.pollutionControl.saveThreeYearsWastewaterStat(
      props.enterpriseId,
      selectedWastewaterYearRange.value,
      items
    )
    
    message.success('近三年废水情况统计数据提交成功')
    await new Promise(resolve => setTimeout(resolve, 300))
    await loadWastewaterStatData()
  } catch (error) {
    console.error('提交近三年废水情况统计数据失败:', error)
    message.error('提交近三年废水情况统计数据失败: ' + (error.message || '未知错误'))
  }
}

// 提交废气产生情况数据
const submitWasteGasData = async () => {
  if (!props.enterpriseId) {
    message.warning('企业ID不能为空')
    return
  }
  
  try {
    const items = formData.value.wasteGas
      .filter(row => row.type)
      .map(row => ({
        type: row.type,
        pollutants: row.pollutants || '',
        location: row.location || '',
        treatment: row.treatment || ''
      }))
    
    await api.pcb.pollutionControl.batchSaveWasteGasAnalysis(props.enterpriseId, items)
    
    message.success('废气产生情况数据提交成功')
    await new Promise(resolve => setTimeout(resolve, 300))
    await loadWasteGasData()
  } catch (error) {
    console.error('提交废气产生情况数据失败:', error)
    message.error('提交废气产生情况数据失败: ' + (error.message || '未知错误'))
  }
}

// 年份范围变化处理
const onWastewaterYearRangeChange = async () => {
  await loadWastewaterStatData()
}

// 确保数据结构完整
watch(() => props.modelValue, (newVal) => {
  if (newVal) {
    if (!newVal.wastewater) {
      newVal.wastewater = []
    }
    if (!newVal.wasteGas) {
      newVal.wasteGas = []
    }
    if (!newVal.wastewaterStats) {
      newVal.wastewaterStats = []
    }
    
    // 如果表格为空，添加一条空白记录
    if (newVal.wastewater.length === 0) {
      addWastewaterRow()
    }
    if (newVal.wasteGas.length === 0) {
      addWasteGasRow()
    }
    if (newVal.wastewaterStats.length === 0) {
      addWastewaterStatRow()
    }
  }
}, { immediate: true, deep: true })

// 组件挂载时加载数据
onMounted(() => {
  if (props.enterpriseId) {
    loadWastewaterData()
    loadWastewaterStatData()
    loadWasteGasData()
  }
})

// 废水统计总计数据
const wastewaterStatTableData = computed(() => {
  const rows = formData.value.wastewaterStats || []
  const yearRange = selectedWastewaterYearRange.value.split('-')
  const startYear = parseInt(yearRange[0])
  const endYear = parseInt(yearRange[1])

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

  const totalProd = sumByProject('生产废水', '生产废水总计')
  const totalLife = sumByProject('生活废水', '生活废水总计')
  const grand = { id: 'total_all_wastewater', isTotal: true, project: '总废水量', unit: 'm³' }
  for (let y = startYear; y <= endYear; y++) {
    grand[`amount_${y}`] = Number(totalProd[`amount_${y}`] || 0) + Number(totalLife[`amount_${y}`] || 0)
  }

  return [...rows, totalProd, totalLife, grand]
})
</script>

<style scoped>
.pollution-control-form {
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
  padding: 12px;
  vertical-align: top;
}

:deep(.n-data-table .n-data-table-th) {
  background-color: #f8f9fa;
  font-weight: 600;
  color: #333;
}

/* 输入框样式 */
:deep(.n-input) {
  width: 100%;
}

:deep(.n-input .n-input__input-el) {
  min-height: 60px;
  line-height: 1.4;
}

/* 文本域样式 */
:deep(.n-input.n-input--textarea .n-input__input-el) {
  min-height: 60px;
  resize: vertical;
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
</style>






