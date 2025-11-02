<template>
  <div class="process-equipment-form">
    <!-- 设备管理表格 -->
    <n-card title="设备管理" size="small" class="equipment-card sub-module">
      <template #header-extra>
        <n-button type="primary" size="small" @click="addEquipmentRow">
          <template #icon>
            <TheIcon icon="carbon:add" />
          </template>
          添加设备
        </n-button>
      </template>
      
      <n-data-table
        :columns="equipmentColumns"
        :data="formData.equipment"
        :row-key="row => row.id"
        :pagination="false"
        size="small"
        :row-props="getRowProps"
        :loading="loading"
      />
      <div class="table-footer">
        <n-button
          type="primary"
          @click="submitEquipment"
          :loading="submitting"
        >
          <template #icon>
            <TheIcon icon="carbon:checkmark" />
          </template>
          提交
        </n-button>
      </div>
    </n-card>
  </div>
</template>

<script setup>
import { ref, computed, h, watch, onMounted } from 'vue'
import { 
  NCard, 
  NDataTable,
  NButton,
  NInput,
  NSelect,
  NInputNumber,
  useMessage
} from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'
import api from '@/api'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      equipment: []
    })
  },
  enterpriseId: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['update:modelValue'])
const message = useMessage()

const loading = ref(false)
const submitting = ref(false)

const formData = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// 设备名称、设备型号、电机型号、应用工艺改为手动输入，取消枚举依赖，保持与数据库解耦

// 运行状况选项
const statusOptions = [
  { label: '良好', value: '良好' },
  { label: '正常', value: '正常' },
  { label: '一般', value: '一般' },
  { label: '需维护', value: '需维护' },
  { label: '故障', value: '故障' }
]

// 设备表格列定义
const equipmentColumns = [
  {
    title: '序号',
    key: 'index',
    width: 60,
    render: (row, index) => index + 1
  },
  {
    title: '设备名称',
    key: 'equipmentName',
    width: 150,
    render: (row) => h(NInput, {
      value: row.equipmentName,
      placeholder: '请输入设备名称',
      onUpdateValue: (value) => { row.equipmentName = value }
    })
  },
  {
    title: '设备型号',
    key: 'equipmentModel',
    width: 180,
    render: (row) => h(NInput, {
      value: row.equipmentModel,
      placeholder: '请输入设备型号',
      onUpdateValue: (value) => { row.equipmentModel = value }
    })
  },
  {
    title: '电机型号',
    key: 'motorModel',
    width: 150,
    render: (row) => h(NInput, {
      value: row.motorModel,
      placeholder: '请输入电机型号',
      onUpdateValue: (value) => { row.motorModel = value }
    })
  },
  {
    title: '功率(KW)',
    key: 'power',
    width: 100,
    render: (row) => h(NInputNumber, {
      value: row.power,
      min: 0.1,
      precision: 1,
      showButton: false,
      placeholder: '功率',
      onUpdateValue: (value) => { row.power = value }
    })
  },
  {
    title: '数量',
    key: 'quantity',
    width: 80,
    render: (row) => h(NInputNumber, {
      value: row.quantity,
      min: 1,
      precision: 0,
      showButton: false,
      placeholder: '数量',
      onUpdateValue: (value) => { row.quantity = value }
    })
  },
  {
    title: '应用工艺',
    key: 'process',
    width: 150,
    render: (row) => h(NInput, {
      value: row.process,
      placeholder: '请输入应用工艺',
      onUpdateValue: (value) => { row.process = value }
    })
  },
  {
    title: '运行状况',
    key: 'status',
    width: 100,
    render: (row) => h(NSelect, {
      value: row.status,
      options: statusOptions,
      placeholder: '运行状况',
      onUpdateValue: (value) => { row.status = value }
    })
  },
  {
    title: '操作',
    key: 'action',
    width: 80,
    render: (row, index) => h(NButton, {
      size: "small",
      type: "error",
      onClick: () => removeEquipmentRow(index)
    }, () => '删除')
  }
]

// 添加设备行
const addEquipmentRow = () => {
  formData.value.equipment.push({
    id: Date.now(),
    equipmentName: '',
    equipmentModel: '',
    motorModel: '',
    power: null,
    quantity: 1,
    process: '',
    status: '良好'
  })
}

// 删除设备行
const removeEquipmentRow = (index) => {
  formData.value.equipment.splice(index, 1)
}

// 获取行属性（用于样式）
const getRowProps = (row, index) => {
  return {
    style: 'min-height: 48px;'
  }
}

// 获取企业设备信息
const fetchEquipment = async () => {
  if (!props.enterpriseId) return
  
  try {
    loading.value = true
    
    const response = await api.pcb.processEquipment.getEquipment(props.enterpriseId)
    
    if (response && response.data && Array.isArray(response.data)) {
      // 将数据转换为前端格式，并添加id字段
      formData.value.equipment = response.data.map((item, idx) => {
        return {
          id: item.id || Date.now() + idx,
          equipmentName: item.equipmentName || item.equipment_name || '',
          equipmentModel: item.equipmentModel || item.equipment_model || '',
          motorModel: item.motorModel || item.motor_model || '',
          power: item.power || null,
          quantity: item.quantity || 1,
          process: item.process || '',
          status: item.status || '良好',
          remark: item.remark || null
        }
      })
      
      // 如果表格为空，添加一条空白记录
      if (formData.value.equipment.length === 0) {
        addEquipmentRow()
      }
    } else {
      // 如果没有数据，添加默认行
      if (formData.value.equipment.length === 0) {
        addEquipmentRow()
      }
    }
  } catch (error) {
    console.error('获取企业设备信息失败:', error)
    message.warning('获取数据失败，已初始化空表格')
    // 如果获取失败，初始化空表格
    if (formData.value.equipment.length === 0) {
      addEquipmentRow()
    }
  } finally {
    loading.value = false
  }
}

// 提交企业设备信息
const submitEquipment = async () => {
  if (!props.enterpriseId) {
    message.warning('企业ID不能为空')
    return
  }
  
  // 移除必填字段验证，允许空字段提交
  
  try {
    submitting.value = true
    
    // 转换数据格式，确保字段名正确，允许空值
    const items = formData.value.equipment.map(row => {
      return {
        equipmentName: row.equipmentName || '',
        equipmentModel: row.equipmentModel || '',
        motorModel: row.motorModel || '',
        power: row.power || null,
        quantity: row.quantity || 1,
        process: row.process || '',
        status: row.status || '良好',
        remark: row.remark || null
      }
    })
    
    await api.pcb.processEquipment.saveEquipment(
      props.enterpriseId,
      items
    )
    
    message.success('设备信息提交成功')
    
    // 延迟一下再获取数据，确保数据库已更新
    await new Promise(resolve => setTimeout(resolve, 300))
    
    // 重新获取数据以刷新显示
    await fetchEquipment()
  } catch (error) {
    console.error('提交设备信息失败:', error)
    message.error('提交设备信息失败: ' + (error.message || '未知错误'))
  } finally {
    submitting.value = false
  }
}

// 确保数据结构完整
watch(() => props.modelValue, (newVal) => {
  if (newVal) {
    if (!newVal.equipment) {
      newVal.equipment = []
    }
  }
}, { immediate: true, deep: true })

// 组件挂载时获取数据
onMounted(() => {
  if (props.enterpriseId) {
    fetchEquipment()
  }
})
</script>

<style scoped>
.process-equipment-form {
  padding: 16px 0;
}

.equipment-card {
  border: 1px solid #e0e0e6;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.equipment-card:hover {
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

/* 表格底部提交按钮样式 */
.table-footer {
  margin-top: 16px;
  display: flex;
  justify-content: flex-start;
}
</style>





