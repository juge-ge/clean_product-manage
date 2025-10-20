<template>
  <div class="raw-material-form">
    <!-- 主表格区域 -->
    <div class="table-container sub-module">
      <div class="table-header">
        <h3 class="table-title">原辅材料使用情况</h3>
        <div class="table-actions">
          <n-button type="primary" @click="addRow" :disabled="loading">
            <template #icon>
              <TheIcon icon="carbon:add" />
            </template>
            新增行
          </n-button>
          <n-button type="success" @click="saveEnterpriseMaterials" :disabled="loading">
            <template #icon>
              <TheIcon icon="carbon:save" />
            </template>
            保存
          </n-button>
        </div>
      </div>
      
      <n-data-table
        :columns="columns"
        :data="formData"
        :row-key="row => row.id"
        :pagination="false"
        :bordered="true"
        :loading="loading"
        class="material-table"
        :row-class-name="getRowClassName"
      />
    </div>

    <!-- 侧边功能区 -->
    <div class="sidebar">
      <div class="sidebar-section">
        <h4 class="section-title">年份选择</h4>
        <n-select
          v-model:value="selectedYear"
          :options="yearOptions"
          placeholder="选择年份"
          @update:value="handleYearChange"
          class="year-selector"
        />
      </div>
      

      <div class="sidebar-section">
        <h4 class="section-title">统计信息</h4>
        <div class="statistics">
          <div class="stat-item">
            <span class="stat-label">总记录数:</span>
            <span class="stat-value">{{ formData.length }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">已填写:</span>
            <span class="stat-value">{{ completedRows }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">未完成:</span>
            <span class="stat-value">{{ incompleteRows }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">当前年份:</span>
            <span class="stat-value">{{ selectedYear }}</span>
          </div>
        </div>
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
const materialOptions = ref([])
const processOptions = ref([
  { label: '下料', value: '下料' },
  { label: '叠层', value: '叠层' },
  { label: '蚀刻', value: '蚀刻' },
  { label: '丝印', value: '丝印' },
  { label: '干膜', value: '干膜' },
  { label: '电镀', value: '电镀' },
  { label: '公用', value: '公用' }
])

const unitOptions = ref([
  { label: 'm²', value: 'm²' },
  { label: 'kg', value: 'kg' },
  { label: 'L', value: 'L' },
  { label: 'g', value: 'g' }
])

const selectedYear = ref(new Date().getFullYear().toString())

// 年份选项（近五年）
const yearOptions = computed(() => {
  const currentYear = new Date().getFullYear()
  return [
    { label: (currentYear - 4).toString(), value: (currentYear - 4).toString() },
    { label: (currentYear - 3).toString(), value: (currentYear - 3).toString() },
    { label: (currentYear - 2).toString(), value: (currentYear - 2).toString() },
    { label: (currentYear - 1).toString(), value: (currentYear - 1).toString() },
    { label: currentYear.toString(), value: currentYear.toString() }
  ]
})

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

// 统计信息
const completedRows = computed(() => {
  return formData.value.filter(row => 
    row.name && row.unit && row.process && row.amount !== null && row.amount !== undefined
  ).length
})

const incompleteRows = computed(() => {
  return formData.value.length - completedRows.value
})

// 获取材料列表
const fetchMaterials = async (keyword = '') => {
  try {
    loading.value = true
    const response = await api.pcb.rawMaterial.getMaterials({ keyword })
    materialOptions.value = response.data.materials.map(material => ({
      label: material.name,
      value: material.name,
      material: material
    }))
  } catch (error) {
    console.error('获取材料列表失败:', error)
    message.error('获取材料列表失败')
    materialOptions.value = []
  } finally {
    loading.value = false
  }
}

// 获取企业原辅材料使用情况
const fetchEnterpriseMaterials = async () => {
  try {
    loading.value = true
    const response = await api.pcb.enterpriseRawMaterial.getUsage(props.enterpriseId, selectedYear.value)
    if (response.data && response.data.length > 0) {
      formData.value = response.data
    } else {
      // 如果没有数据，尝试从其他年份继承数据
      await inheritFromOtherYears()
      if (formData.value.length === 0) {
        addRow()
      }
    }
  } catch (error) {
    console.error('获取企业原辅材料使用情况失败:', error)
    message.error('获取企业原辅材料使用情况失败')
    // 如果获取失败，尝试从其他年份继承数据
    await inheritFromOtherYears()
    if (formData.value.length === 0) {
      addRow()
    }
  } finally {
    loading.value = false
  }
}

// 保存企业原辅材料使用情况
const saveEnterpriseMaterials = async () => {
  try {
    loading.value = true
    const data = {
      year: selectedYear.value,
      materials: formData.value.filter(row => row.name && row.unit && row.process)
    }
    
    await api.pcb.enterpriseRawMaterial.saveUsage(props.enterpriseId, data)
    message.success('保存成功')
  } catch (error) {
    console.error('保存企业原辅材料使用情况失败:', error)
    message.error('保存企业原辅材料使用情况失败')
  } finally {
    loading.value = false
  }
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

// 当材料名称改变时，自动设置单位和工序
const handleMaterialChange = (row, materialName) => {
  row.name = materialName
  const material = materialOptions.value.find(m => m.value === materialName)
  if (material && material.material) {
    row.unit = material.material.unit
    row.process = material.material.process
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
            year: selectedYear.value,
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

// 年份改变处理
const handleYearChange = (year) => {
  console.log('年份改变为:', year)
  // 重新加载该年份的数据
  fetchEnterpriseMaterials()
}

// 添加行
const addRow = () => {
  formData.value.push({
    id: Date.now() + Math.random(),
    year: selectedYear.value,
    name: '',
    unit: '',
    process: '',
    amount: null,
    unitConsumption: null
  })
}


// 获取行样式类名（用于错误提示）
const getRowClassName = (row, index) => {
  const hasError = !row.name || !row.unit || !row.process || row.amount === null || row.amount === undefined
  return hasError ? 'error-row' : ''
}

// 验证输入
const validateInput = (value, type) => {
  if (type === 'amount' && value !== null && value !== undefined) {
    return value >= 0
  }
  return true
}

// 表格列定义
const columns = [
  { 
    title: '序号', 
    key: 'index', 
    width: 80,
    render: (row, index) => index + 1
  },
  { 
    title: '名称', 
    key: 'name', 
    width: 200,
    render: (row, index) => {
      return h(NSelect, {
        value: row.name,
        options: materialOptions.value,
        placeholder: "请选择或输入材料名称",
        filterable: true,
        remote: true,
        onSearch: searchMaterials,
        onUpdateValue: (value) => handleMaterialChange(row, value),
        renderLabel: (option) => option.label,
        renderTag: (option) => option.label,
        class: !row.name ? 'error-input' : ''
      })
    }
  },
  { 
    title: '应用工序', 
    key: 'process', 
    width: 120,
    render: (row, index) => {
      return h(NSelect, {
        value: row.process,
        options: processOptions.value,
        placeholder: "选择工序",
        onUpdateValue: (value) => {
          row.process = value
        },
        class: !row.process ? 'error-input' : ''
      })
    }
  },
  { 
    title: '年总用量', 
    key: 'amount', 
    width: 120,
    render: (row, index) => {
      return h(NInputNumber, {
        value: row.amount,
        placeholder: "请输入年总用量",
        min: 0,
        precision: 2,
        onUpdateValue: (value) => {
          row.amount = value
        },
        class: (row.amount === null || row.amount === undefined) ? 'error-input' : ''
      })
    }
  },
  { 
    title: '单位', 
    key: 'unit', 
    width: 100,
    render: (row, index) => {
      return h(NSelect, {
        value: row.unit,
        options: unitOptions.value,
        placeholder: "选择单位",
        onUpdateValue: (value) => {
          row.unit = value
        },
        class: !row.unit ? 'error-input' : ''
      })
    }
  },
  { 
    title: '操作', 
    key: 'action', 
    width: 80,
    render: (row, index) => {
      return h(NButton, {
        size: "small",
        type: "error",
        onClick: () => {
          const idx = formData.value.findIndex(item => item.id === row.id)
          if (idx > -1) {
            formData.value.splice(idx, 1)
          }
        }
      }, () => '删除')
    }
  }
]

// 确保数据结构完整
watch(() => props.modelValue, (newVal) => {
  if (newVal && newVal.length === 0) {
    // 如果表格为空，添加一条空白记录
    addRow()
  }
}, { immediate: true, deep: true })

onMounted(async () => {
  await fetchMaterials()
  await fetchEnterpriseMaterials()
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
</style>