<template>
  <div class="raw-material-form">
    <!-- 主表格区域 -->
    <div class="table-container sub-module">
      <div class="table-header">
        <h3 class="table-title">原辅材料使用情况</h3>
        <div class="table-actions">
          <div class="year-range-selector">
            <n-text strong>年份范围：</n-text>
            <n-select
              v-model:value="selectedYearRange"
              :options="yearRangeOptions"
              style="width: 200px"
              @update:value="onYearRangeChange"
            />
          </div>
          <n-button type="primary" @click="addRow" :disabled="loading">
            <template #icon>
              <TheIcon icon="carbon:add" />
            </template>
            新增行
          </n-button>
        </div>
      </div>
      
      <n-data-table
        :columns="getColumns()"
        :data="formData"
        :row-key="row => row.id"
        :pagination="false"
        :bordered="true"
        :loading="loading"
        class="material-table"
      />
      <div class="table-footer">
        <n-button 
          type="primary" 
          @click="submitRawMaterials"
          :loading="submitting"
        >
          <template #icon>
            <TheIcon icon="carbon:checkmark" />
          </template>
          提交
        </n-button>
      </div>
    </div>


    <!-- 新建材料弹窗 -->
    <n-modal v-model:show="showCreateModal" preset="card" title="新建材料" size="medium">
      <n-form
        ref="createFormRef"
        :model="newMaterial"
        :rules="createMaterialRules"
        label-placement="left"
        label-width="100px"
      >
        <n-form-item label="材料名称" path="name">
          <n-input v-model:value="newMaterial.name" placeholder="请输入材料名称" />
        </n-form-item>
        
        <n-form-item label="默认单位" path="unit">
          <n-select
            v-model:value="newMaterial.unit"
            :options="unitOptions"
            placeholder="选择单位"
          />
        </n-form-item>
        
        <n-form-item label="适用工序" path="process">
          <n-select
            v-model:value="newMaterial.process"
            :options="processOptions"
            placeholder="选择工序"
          />
        </n-form-item>
        
        <n-form-item label="材料描述" path="description">
          <n-input
            v-model:value="newMaterial.description"
            type="textarea"
            placeholder="请输入材料描述（可选）"
            :rows="3"
          />
        </n-form-item>
      </n-form>
      
      <template #footer>
        <div class="modal-footer">
          <n-button @click="showCreateModal = false">取消</n-button>
          <n-button type="primary" @click="createMaterial" :loading="creating">
            创建
          </n-button>
        </div>
      </template>
    </n-modal>
  </div>
</template>

<script setup>
import { computed, h, ref, onMounted, watch, nextTick } from 'vue'
import { 
  NDataTable, 
  NButton, 
  NInput, 
  NInputNumber, 
  NSelect, 
  NSpin,
  NModal,
  NForm,
  NFormItem,
  NText,
  useMessage
} from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'
import api from '@/api'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  },
  enterpriseId: {
    type: [String, Number],
    required: true
  }
})

const emit = defineEmits(['update:modelValue'])

const message = useMessage()

// 响应式数据
const loading = ref(false)
const creating = ref(false)
const submitting = ref(false)
const materialOptions = ref([])
// 产品产量数据（从企业总体生产情况读取）
const productOutputData = ref([])
// 产品类型/主要产品（与“1.近三年产品产量”保持一致）
const typeOptions = [
  { label: '刚性', value: 'rigid' },
  { label: '挠性', value: 'flexible' }
]
const rigidProductOptions = [
  { label: '刚性单面板', value: 'rigid_single' },
  { label: '刚性双面板', value: 'rigid_double' },
  { label: '刚性多面板', value: 'rigid_multilayer' },
  { label: '刚性HDI板', value: 'rigid_hdi' }
]
const flexibleProductOptions = [
  { label: '挠性单面板', value: 'flexible_single' },
  { label: '挠性双面板', value: 'flexible_double' },
  { label: '挠性多面板', value: 'flexible_multilayer' },
  { label: '挠性HDI板', value: 'flexible_hdi' }
]

const unitOptions = ref([
  { label: 'kg', value: 'kg' },
  { label: 'm²', value: 'm²' },
  { label: 'L', value: 'L' }
])

// 年份范围选项（与资源能源消耗一致）
const yearRangeOptions = [
  { label: '2022-2024', value: '2022-2024' },
  { label: '2021-2023', value: '2021-2023' },
  { label: '2020-2022', value: '2020-2022' }
]
const selectedYearRange = ref('2022-2024')

// 新建材料相关
const showCreateModal = ref(false)
const newMaterial = ref({
  name: '',
  unit: '',
  process: '',
  description: ''
})

const createMaterialRules = {
  name: [
    { required: true, message: '请输入材料名称', trigger: 'blur' }
  ],
  unit: [
    { required: true, message: '请选择单位', trigger: 'change' }
  ],
  process: [
    { required: true, message: '请选择工序', trigger: 'change' }
  ]
}

const formData = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// 统计信息（暂不展示，但保留可用）
const completedRows = computed(() => formData.value.length)
const incompleteRows = computed(() => 0)

// 获取材料列表
const fetchMaterials = async (keyword = '') => {
  try {
    loading.value = true
    const response = await api.pcb.rawMaterial.getMaterials({ keyword })
    const payload = response && response.data !== undefined ? response.data : response
    let materialsList = []
    if (Array.isArray(payload)) {
      materialsList = payload
    } else if (Array.isArray(payload?.materials)) {
      materialsList = payload.materials
    } else if (Array.isArray(payload?.data?.materials)) {
      materialsList = payload.data.materials
    } else if (Array.isArray(payload?.results)) {
      materialsList = payload.results
    } else if (Array.isArray(payload?.items)) {
      materialsList = payload.items
    } else {
      materialsList = []
    }

    const apiOptions = materialsList.map(material => ({
      label: material.name || material.label || material.value,
      value: material.name || material.value || material.label,
      material: material
    })).filter(opt => !!opt.value)

    const copperClad = { label: '覆铜板', value: '覆铜板' }
    const exist = apiOptions.some(o => o.value === copperClad.value)
    materialOptions.value = exist ? apiOptions : [copperClad, ...apiOptions]
  } catch (error) {
    console.error('获取材料列表失败:', error)
    message.error('获取材料列表失败')
    materialOptions.value = [{ label: '覆铜板', value: '覆铜板' }]
  } finally {
    loading.value = false
  }
}

// 获取企业原辅材料使用情况
const fetchEnterpriseMaterials = async () => {
  if (!props.enterpriseId) return
  
  try {
    loading.value = true
    const yearRange = selectedYearRange.value
    
    // 先确保产品产量数据已加载
    if (productOutputData.value.length === 0) {
      await fetchProductOutputData()
    }
    
    const response = await api.pcb.production.getThreeYearsRawMaterialUsage(
      props.enterpriseId,
      yearRange
    )
    
    if (response && response.data && Array.isArray(response.data)) {
      // 将数据转换为前端格式，并添加id字段
      formData.value = response.data.map((item, idx) => {
        const row = {
          id: Date.now() + idx,
          type: item.type || null,
          mainProduct: item.mainProduct || item.main_product || null,
          materialName: item.materialName || item.material_name || '',
          unit: item.unit || 'm²'
        }
        
        // 添加动态年份字段
        const [start, end] = yearRange.split('-').map(y => parseInt(y))
        for (let y = start; y <= end; y++) {
          row[`amount_${y}`] = item[`amount_${y}`] || null
          // 重新计算单位产品消耗量（使用对应年份的产品产量）
          calculateUnitConsumption(row, y)
        }
        
        return row
      })
      
      // 如果没有数据，至少添加一行覆铜板
      if (formData.value.length === 0) {
        addRow()
        // 确保第一行是覆铜板
        if (formData.value.length > 0) {
          formData.value[0].materialName = '覆铜板'
        }
      }
    } else {
      // 如果没有数据，添加默认行
      addRow()
      if (formData.value.length > 0) {
        formData.value[0].materialName = '覆铜板'
      }
    }
  } catch (error) {
    console.error('获取企业原辅材料使用情况失败:', error)
    message.warning('获取数据失败，已初始化空表格')
    // 如果获取失败，初始化空表格
    if (formData.value.length === 0) {
      addRow()
      if (formData.value.length > 0) {
        formData.value[0].materialName = '覆铜板'
      }
    }
  } finally {
    loading.value = false
  }
}

// 提交企业原辅材料使用情况
const submitRawMaterials = async () => {
  if (!props.enterpriseId) {
    message.warning('企业ID不能为空')
    return
  }
  
  // 必填校验：至少包含一行"覆铜板"
  const hasCopperClad = formData.value.some(row => row.materialName === '覆铜板')
  if (!hasCopperClad) {
    message.error('请至少添加一行原辅材料为"覆铜板"的记录')
    return
  }
  
  // 检查必填字段
  for (const item of formData.value) {
    if (!item.type || !item.mainProduct || !item.materialName || !item.unit) {
      message.warning('请完整填写产品类型、产品名称、原辅材料名称和单位')
      return
    }
  }
  
  try {
    submitting.value = true
    const yearRange = selectedYearRange.value
    
    // 转换数据格式，确保字段名正确
    // 注意：productOutput 字段不再提交，因为数据来源于企业总体生产情况
    const items = formData.value.map(row => {
      const item = {
        type: row.type,
        mainProduct: row.mainProduct,
        materialName: row.materialName,
        unit: row.unit
      }
      
      // 添加动态年份字段
      const [start, end] = yearRange.split('-').map(y => parseInt(y))
      for (let y = start; y <= end; y++) {
        // 处理年消耗量：0是有效值
        let amountValue = row[`amount_${y}`]
        if (amountValue === '' || amountValue === undefined) {
          amountValue = null
        } else if (amountValue !== null) {
          amountValue = typeof amountValue === 'number' ? amountValue : parseFloat(amountValue)
          if (isNaN(amountValue)) amountValue = null
        }
        item[`amount_${y}`] = amountValue
        
        // 处理单位产品消耗量：0是有效值
        let unitConsumptionValue = row[`unitConsumption_${y}`]
        if (unitConsumptionValue === '' || unitConsumptionValue === undefined) {
          unitConsumptionValue = null
        } else if (unitConsumptionValue !== null) {
          unitConsumptionValue = typeof unitConsumptionValue === 'number' ? unitConsumptionValue : parseFloat(unitConsumptionValue)
          if (isNaN(unitConsumptionValue)) unitConsumptionValue = null
        }
        item[`unitConsumption_${y}`] = unitConsumptionValue
      }
      
      return item
    })
    
    await api.pcb.production.saveThreeYearsRawMaterialUsage(
      props.enterpriseId,
      yearRange,
      items
    )
    
    message.success('原辅材料使用情况提交成功')
    
    // 延迟一下再获取数据，确保数据库已更新
    await new Promise(resolve => setTimeout(resolve, 300))
    
    // 重新获取数据以刷新显示
    await fetchEnterpriseMaterials()
  } catch (error) {
    console.error('提交原辅材料使用情况失败:', error)
    message.error('提交原辅材料使用情况失败: ' + (error.message || '未知错误'))
  } finally {
    submitting.value = false
  }
}

// 获取企业近三年产品产量数据
const fetchProductOutputData = async () => {
  if (!props.enterpriseId) return
  
  try {
    const yearRange = selectedYearRange.value
    const response = await api.pcb.production.getThreeYearsProductOutput(
      props.enterpriseId,
      yearRange
    )
    
    if (response && response.data && Array.isArray(response.data)) {
      productOutputData.value = response.data.map(item => ({
        type: item.type || null,
        mainProduct: item.mainProduct || item.main_product || null,
        unit: item.unit || null,
        layers: item.layers || null,
        ...(Object.keys(item).reduce((acc, key) => {
          if (key.startsWith('output_')) {
            acc[key] = item[key]
          }
          return acc
        }, {}))
      }))
    } else {
      productOutputData.value = []
    }
  } catch (error) {
    console.error('获取产品产量数据失败:', error)
    productOutputData.value = []
  }
}

// 根据产品类型和产品名称，从产品产量数据中获取对应年份的产量
const getProductOutputByYear = (type, mainProduct, year) => {
  if (!type || !mainProduct) return null
  
  const matchedItem = productOutputData.value.find(item => 
    item.type === type && item.mainProduct === mainProduct
  )
  
  if (!matchedItem) return null
  
  const yearKey = `output_${year}`
  return matchedItem[yearKey] || null
}

// 年份范围变化处理
const onYearRangeChange = async () => {
  // 重新获取产品产量数据
  await fetchProductOutputData()
  // 重新获取原辅材料数据
  await fetchEnterpriseMaterials()
}

// 搜索材料
const searchMaterials = async (keyword) => {
  if (keyword && keyword.length > 0) {
    await fetchMaterials(keyword)
  } else {
    await fetchMaterials()
  }
}

// 创建新材料
const createMaterial = async () => {
  try {
    creating.value = true
    await api.pcb.rawMaterial.create({
      name: newMaterial.value.name,
      unit: newMaterial.value.unit,
      process: newMaterial.value.process,
      description: newMaterial.value.description || null,
      category: 'PCB原辅材料'
    })
    
    message.success('材料创建成功')
    showCreateModal.value = false
    
    // 重置表单
    newMaterial.value = {
      name: '',
      unit: '',
      process: '',
      description: ''
    }
    
    // 刷新材料列表
    await fetchMaterials()
  } catch (error) {
    console.error('创建材料失败:', error)
    message.error('创建材料失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    creating.value = false
  }
}

// 当材料名称改变时，自动设置单位等（与显示字段 materialName 对齐）
const handleMaterialChange = (row, materialName) => {
  row.materialName = materialName
  const material = materialOptions.value.find(m => m.value === materialName)
  if (material && material.material) {
    if (material.material.unit) row.unit = material.material.unit
    if (material.material.process) row.process = material.material.process
  }
}

// 从其他年份继承数据
const inheritFromOtherYears = async () => {
  try {
    // 获取所有年份的数据
    const allYears = yearOptions.value.map(y => y.value)
    const currentYearIndex = allYears.indexOf(selectedYear.value)
    
    // 从最近的年份开始查找有数据的年份
    for (let i = currentYearIndex - 1; i >= 0; i--) {
      const year = allYears[i]
      try {
        const response = await api.pcb.enterpriseRawMaterial.getUsage(props.enterpriseId, year)
        if (response.data && response.data.length > 0) {
          // 继承数据，但清空用量
          formData.value = response.data.map(item => ({
            ...item,
            id: Date.now() + Math.random(),
            // year range 模式不做逐年字段清空，初始化由前端处理
            amount: null,
            unitConsumption: null
          }))
          message.info(`已从${year}年继承材料信息，请填写用量数据`)
          return
        }
      } catch (error) {
        console.log(`获取${year}年数据失败:`, error)
      }
    }
  } catch (error) {
    console.error('继承数据失败:', error)
  }
}

// 年份范围改变时重新加载数据
watch(selectedYearRange, () => {
  if (props.enterpriseId) {
    fetchEnterpriseMaterials()
  }
})

// 自动计算单位产品消耗量 = 对应年份的消耗量 / 对应年份的产品产量，保留两位小数
const calculateUnitConsumption = (row, year) => {
  const amount = row[`amount_${year}`]
  // 从产品产量数据中获取对应年份的产量
  const productOutput = getProductOutputByYear(row.type, row.mainProduct, year)
  
  if (amount != null && amount !== '' && productOutput != null && productOutput !== '' && productOutput > 0) {
    const amountNum = typeof amount === 'number' ? amount : parseFloat(amount)
    const outputNum = typeof productOutput === 'number' ? productOutput : parseFloat(productOutput)
    
    if (!isNaN(amountNum) && !isNaN(outputNum) && outputNum > 0) {
      const unitConsumption = (amountNum / outputNum).toFixed(2)
      row[`unitConsumption_${year}`] = parseFloat(unitConsumption)
    } else {
      row[`unitConsumption_${year}`] = null
    }
  } else {
    row[`unitConsumption_${year}`] = null
  }
}

// 添加行
const addRow = () => {
  const last = formData.value.length > 0 ? formData.value[formData.value.length - 1] : null
  const row = {
    id: Date.now() + Math.random(),
    materialName: '',
    type: last ? last.type : null,
    mainProduct: last ? last.mainProduct : null,
    unit: 'm²'
  }
  const [start, end] = selectedYearRange.value.split('-').map(y => parseInt(y))
  for (let y = start; y <= end; y++) {
    row[`amount_${y}`] = null
    row[`unitConsumption_${y}`] = null
  }
  formData.value.push(row)
  
  // 如果有类型和产品名称，自动计算单位产品消耗量
  if (row.type && row.mainProduct) {
    for (let y = start; y <= end; y++) {
      calculateUnitConsumption(row, y)
    }
  }
}


// 获取行样式类名（用于错误提示）
const getRowClassName = (row, index) => ''

// 验证输入
const validateInput = (value, type) => {
  if (type === 'amount' && value !== null && value !== undefined) {
    return value >= 0
  }
  return true
}

// 表格列定义（动态年份列）
const getColumns = () => {
  const base = [
    {
      title: '产品类型',
      key: 'type',
      width: 110,
      render: (row) => h(NSelect, {
        value: row.type,
        options: typeOptions,
        placeholder: '请选择类型',
        'onUpdate:value': (val) => { 
          row.type = val
          row.mainProduct = null
          // 产品类型变化时，重新计算所有年份的单位产品消耗量
          const [startYear, endYear] = selectedYearRange.value.split('-').map(y => parseInt(y))
          for (let y = startYear; y <= endYear; y++) {
            calculateUnitConsumption(row, y)
          }
        }
      })
    },
    {
      title: '产品名称',
      key: 'mainProduct',
      width: 160,
      render: (row) => {
        const options = row.type === 'rigid' ? rigidProductOptions : flexibleProductOptions
        return h(NSelect, {
          value: row.mainProduct,
          options,
          placeholder: '请选择产品',
          disabled: !row.type,
          'onUpdate:value': (val) => { 
            row.mainProduct = val
            // 产品名称变化时，重新计算所有年份的单位产品消耗量
            const [startYear, endYear] = selectedYearRange.value.split('-').map(y => parseInt(y))
            for (let y = startYear; y <= endYear; y++) {
              calculateUnitConsumption(row, y)
            }
          }
        })
      }
    },
    {
      title: '近三年产品产量(m²)',
      key: 'productOutput',
      width: 180,
      render: (row) => {
        // 产品产量为只读，从企业总体生产情况读取
        const [start, end] = selectedYearRange.value.split('-').map(y => parseInt(y))
        const outputValues = []
        for (let y = start; y <= end; y++) {
          const output = getProductOutputByYear(row.type, row.mainProduct, y)
          if (output != null) {
            outputValues.push(`${y}年: ${output.toFixed(2)}`)
          }
        }
        
        if (outputValues.length > 0) {
          return h('div', {
            style: { 
              padding: '4px 8px',
              backgroundColor: '#f5f5f5',
              borderRadius: '4px',
              fontSize: '12px',
              color: '#666'
            }
          }, outputValues.join(' | ') || '暂无数据')
        } else {
          return h('span', {
            style: { color: '#999', fontSize: '12px' }
          }, '请先在企业总体生产情况中录入产品产量')
        }
      }
    },
    {
      title: '原辅材料',
      key: 'materialName',
      width: 200,
      render: (row) => h(NSelect, {
        value: row.materialName,
        options: materialOptions.value,
        placeholder: '请选择或输入材料名称（支持手动输入）',
        filterable: true,
        remote: true,
        tag: true,
        onSearch: searchMaterials,
        'onUpdate:value': (value) => { row.materialName = value },
        'label-field': 'label',
        'value-field': 'value',
        'fallback-option': (val) => ({ label: String(val ?? ''), value: val })
      })
    },
    {
      title: '单位',
      key: 'unit',
      width: 90,
      render: (row) => h(NSelect, {
        value: row.unit,
        options: unitOptions.value,
        placeholder: '选择单位',
        'onUpdate:value': (val) => { row.unit = val }
      })
    }
  ]

  const [start, end] = selectedYearRange.value.split('-').map(y => parseInt(y))
  const yearCols = []
  for (let y = start; y <= end; y++) {
    yearCols.push({
      title: `${y} 年`,
      key: `amount_${y}`,
      width: 120,
      render: (row) => h(NInputNumber, {
        value: row[`amount_${y}`],
        min: 0,
        precision: 4,
        showButton: false,
        placeholder: '请输入',
        'onUpdate:value': (val) => { 
          row[`amount_${y}`] = val
          // 自动计算单位产品消耗量 = 消耗量 / 产品产量，保留两位小数
          calculateUnitConsumption(row, y)
        }
      })
    })
  }
  const amountGroup = {
    title: '年消耗量',
    key: 'amount_group',
    children: [...yearCols]
  }

  const unitYearCols = []
  for (let y = start; y <= end; y++) {
    unitYearCols.push({
      title: `${y} 年`,
      key: `unitConsumption_${y}`,
      width: 130,
      render: (row) => h(NInputNumber, {
        value: row[`unitConsumption_${y}`],
        min: 0,
        precision: 2,
        showButton: false,
        placeholder: '自动计算',
        readonly: true,
        style: { backgroundColor: '#f5f5f5' }
      })
    })
  }
  const unitGroup = {
    title: () => h('span', ['单位产品消耗量/','m²']),
    key: 'unit_group',
    children: [...unitYearCols]
  }

  const action = {
    title: '操作',
    key: 'action',
    width: 80,
    render: (row) => h(NButton, {
      size: 'small',
      type: 'error',
      onClick: () => {
        const idx = formData.value.findIndex(i => i.id === row.id)
        if (idx > -1) formData.value.splice(idx, 1)
      }
    }, () => '删除')
  }

  return [...base, amountGroup, unitGroup, action]
}

// 确保数据结构完整
watch(() => props.modelValue, (newVal) => {
  if (newVal && newVal.length === 0) {
    // 如果表格为空，添加一条空白记录
    addRow()
  }
}, { immediate: true, deep: true })

onMounted(async () => {
  await fetchMaterials()
  // 如果有企业ID，从后端获取数据
  if (props.enterpriseId) {
    // 先获取产品产量数据
    await fetchProductOutputData()
    // 然后获取原辅材料数据
    await fetchEnterpriseMaterials()
  } else {
    // 如果没有企业ID，初始化空表格
    if (formData.value.length === 0) {
      addRow()
    }
    // 确保存在一行"覆铜板"
    const hasCopperClad = formData.value.some(r => r.materialName === '覆铜板')
    if (!hasCopperClad) {
      const row = {
        id: Date.now() + Math.random(),
        materialName: '覆铜板',
        type: null,
        mainProduct: null,
        unit: 'm²'
      }
      const [start, end] = selectedYearRange.value.split('-').map(y => parseInt(y))
      for (let y = start; y <= end; y++) {
        row[`amount_${y}`] = null
        row[`unitConsumption_${y}`] = null
      }
      formData.value.unshift(row)
    }
  }
})
</script>

<style scoped>
.raw-material-form {
  display: flex;
  gap: 20px;
  padding: 16px 0;
}

.table-container {
  flex: 1;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
}

.table-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
  padding-bottom: 8px;
  display: inline-block;
  border-bottom: 2px solid #ff8c00;
}

.table-actions {
  display: flex;
  gap: 8px;
}

.material-table {
  border-radius: 0;
}

.sidebar {
  width: 280px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  height: fit-content;
}

.sidebar-section {
  margin-bottom: 24px;
}

.sidebar-section:last-child {
  margin-bottom: 0;
}

.section-title {
  margin: 0 0 12px 0;
  font-size: 14px;
  font-weight: 600;
  color: #2c3e50;
  padding-bottom: 8px;
  display: inline-block;
  border-bottom: 2px solid #ff8c00;
}

.year-selector {
  width: 100%;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.action-btn {
  width: 100%;
}

.statistics {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.stat-item:last-child {
  border-bottom: none;
}

.stat-label {
  font-size: 13px;
  color: #666;
}

.stat-value {
  font-size: 14px;
  font-weight: 600;
  color: #2c3e50;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* 错误样式 */
:deep(.error-row) {
  background-color: #fff2f0 !important;
}

:deep(.error-input .n-input),
:deep(.error-input .n-select) {
  border-color: #ff4d4f !important;
  box-shadow: 0 0 0 2px rgba(255, 77, 79, 0.2) !important;
}

:deep(.error-input .n-input:focus),
:deep(.error-input .n-select:focus) {
  border-color: #ff4d4f !important;
  box-shadow: 0 0 0 2px rgba(255, 77, 79, 0.2) !important;
}

/* 表格样式优化 */
:deep(.n-data-table) {
  border-radius: 0;
}

:deep(.n-data-table .n-data-table-th) {
  background-color: #fafafa;
  font-weight: 600;
  color: #2c3e50;
}

:deep(.n-data-table .n-data-table-td) {
  padding: 12px 16px;
}

/* 按钮样式 */
:deep(.n-button) {
  border-radius: 6px;
}

/* 选择器样式 */
:deep(.n-select) {
  border-radius: 6px;
}

:deep(.n-input-number) {
  border-radius: 6px;
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

/* 表标题样式 */
.table-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
  padding-bottom: 8px;
  display: inline-block;
  border-bottom: 2px solid #ff8c00;
}

/* 表格底部提交按钮样式 */
.table-footer {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  padding: 16px 20px;
  border-top: 1px solid #e9ecef;
  background: #fafafa;
}
</style>