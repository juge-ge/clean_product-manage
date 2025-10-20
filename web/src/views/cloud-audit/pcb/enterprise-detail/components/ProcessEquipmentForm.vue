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
      />
          </n-card>
  </div>
</template>

<script setup>
import { ref, computed, h, watch } from 'vue'
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

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      equipment: []
    })
  }
})

const emit = defineEmits(['update:modelValue'])
const message = useMessage()

const formData = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// 设备名称选项（枚举 + 自定义输入）
const equipmentNameOptions = [
  { label: '镀镍金自动线', value: '镀镍金自动线' },
  { label: '蚀刻机', value: '蚀刻机' },
  { label: '钻孔机', value: '钻孔机' },
  { label: '压合机', value: '压合机' },
  { label: '曝光机', value: '曝光机' },
  { label: '显影机', value: '显影机' },
  { label: '电镀线', value: '电镀线' },
  { label: '测试机', value: '测试机' }
]

// 设备型号选项
const equipmentModelOptions = [
  { label: '镀铬镀镍金自动处理线', value: '镀铬镀镍金自动处理线' },
  { label: '全自动蚀刻生产线', value: '全自动蚀刻生产线' },
  { label: '高精度钻孔机', value: '高精度钻孔机' },
  { label: '多层板压合机', value: '多层板压合机' },
  { label: 'UV曝光机', value: 'UV曝光机' },
  { label: '自动显影机', value: '自动显影机' },
  { label: '连续电镀线', value: '连续电镀线' },
  { label: '在线测试机', value: '在线测试机' }
]

// 电机型号选项
const motorModelOptions = [
  { label: 'MAV21325A-02', value: 'MAV21325A-02' },
  { label: 'MAV21325A-01', value: 'MAV21325A-01' },
  { label: 'MAV21325B-01', value: 'MAV21325B-01' },
  { label: 'MAV21325B-02', value: 'MAV21325B-02' },
  { label: 'MAV21325C-01', value: 'MAV21325C-01' },
  { label: 'MAV21325C-02', value: 'MAV21325C-02' }
]

// 应用工艺选项
const processOptions = [
  { label: '镀镍金自动线', value: '镀镍金自动线' },
  { label: '蚀刻工艺', value: '蚀刻工艺' },
  { label: '钻孔工艺', value: '钻孔工艺' },
  { label: '压合工艺', value: '压合工艺' },
  { label: '曝光工艺', value: '曝光工艺' },
  { label: '显影工艺', value: '显影工艺' },
  { label: '电镀工艺', value: '电镀工艺' },
  { label: '测试工艺', value: '测试工艺' }
]

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
    render: (row) => h(NSelect, {
      value: row.equipmentName,
      options: equipmentNameOptions,
      filterable: true,
      tag: true,
      placeholder: '请选择或输入设备名称',
      onUpdateValue: (value) => { row.equipmentName = value }
    })
  },
  {
    title: '设备型号',
    key: 'equipmentModel',
    width: 180,
    render: (row) => h(NSelect, {
      value: row.equipmentModel,
      options: equipmentModelOptions,
      filterable: true,
      tag: true,
      placeholder: '请选择或输入设备型号',
      onUpdateValue: (value) => { row.equipmentModel = value }
    })
  },
  {
    title: '电机型号',
    key: 'motorModel',
    width: 150,
    render: (row) => h(NSelect, {
      value: row.motorModel,
      options: motorModelOptions,
      filterable: true,
      tag: true,
      placeholder: '请选择或输入电机型号',
      onUpdateValue: (value) => { row.motorModel = value }
    })
  },
  {
    title: '功率(KW)',
    key: 'power',
    width: 100,
    render: (row) => h(NInputNumber, {
      value: row.power,
      min: 0,
      precision: 1,
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
      placeholder: '数量',
      onUpdateValue: (value) => { row.quantity = value }
    })
  },
  {
    title: '应用工艺',
    key: 'process',
    width: 150,
    render: (row) => h(NSelect, {
      value: row.process,
      options: processOptions,
      filterable: true,
      tag: true,
      placeholder: '请选择或输入应用工艺',
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

// 确保数据结构完整
watch(() => props.modelValue, (newVal) => {
  if (newVal) {
    if (!newVal.equipment) {
      newVal.equipment = []
    }
    
    // 如果表格为空，添加一条空白记录
    if (newVal.equipment.length === 0) {
      addEquipmentRow()
    }
  }
}, { immediate: true, deep: true })
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
</style>





