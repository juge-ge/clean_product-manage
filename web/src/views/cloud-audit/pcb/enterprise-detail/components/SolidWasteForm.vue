<template>
  <div class="solid-waste-form">
    <!-- 工业固体废物管理表格 -->
    <n-card title="工业固体废物管理" size="small" class="waste-card sub-module">
      <template #header-extra>
        <n-space>
          <div class="year-range-selector">
            <n-text strong>年份范围：</n-text>
            <n-select
              v-model:value="selectedYearRange"
              :options="yearRangeOptions"
              style="width: 200px"
              @update:value="onYearRangeChange"
            />
          </div>
          <n-button type="primary" size="small" @click="addWasteRow">
            <template #icon>
              <TheIcon icon="carbon:add" />
            </template>
            添加废物
          </n-button>
        </n-space>
      </template>
      
        <n-data-table
          :columns="wasteColumns"
          :data="formData.waste"
          :row-key="row => row.id"
          :pagination="false"
          size="small"
        />
    </n-card>
  </div>
</template>

<script setup>
import { computed, h, ref, watch } from 'vue'
import { 
  NCard,
  NDataTable, 
  NButton, 
  NInput,
  NInputNumber, 
  NSelect,
  NSpace,
  NText
} from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      waste: []
    })
  }
})

const emit = defineEmits(['update:modelValue'])

const formData = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// 年份范围选项
const yearRangeOptions = [
  { label: '2020-2022', value: '2020-2022' },
  { label: '2021-2023', value: '2021-2023' },
  { label: '2022-2024', value: '2022-2024' }
]

const selectedYearRange = ref('2020-2022')

// 废物类别选项
const wasteCategoryOptions = [
  { label: '一般废物', value: '一般废物' },
  { label: '生活垃圾', value: '生活垃圾' },
  { label: '危险废物', value: '危险废物' }
]

// 单位选项
const unitOptions = [
  { label: '吨', value: '吨' },
  { label: 'kg', value: 'kg' },
  { label: 'm³', value: 'm³' }
]

// 废物管理表格列
const wasteColumns = computed(() => {
  const baseColumns = [
    {
      title: '类别',
      key: 'category',
      width: 120,
      render: (row) => h(NSelect, {
        value: row.category,
        options: wasteCategoryOptions,
        placeholder: '请选择类别',
        onUpdateValue: (value) => { row.category = value }
      })
    },
    {
      title: '名称',
      key: 'name',
      width: 150,
      render: (row) => h(NInput, {
        value: row.name,
        placeholder: '如：生活垃圾',
        onUpdateValue: (value) => { row.name = value }
      })
    },
    {
      title: '单位',
      key: 'unit',
      width: 100,
      render: (row) => h(NSelect, {
        value: row.unit,
        options: unitOptions,
        placeholder: '单位',
        onUpdateValue: (value) => { row.unit = value }
      })
    }
  ]

  // 根据选择的年份范围动态添加列
  const yearRange = selectedYearRange.value.split('-')
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
        placeholder: '用量',
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
      onClick: () => removeWasteRow(index)
    }, () => '删除')
  }

  return [...baseColumns, ...yearColumns, actionColumn]
})

// 年份范围变化处理
const onYearRangeChange = (range) => {
  selectedYearRange.value = range
  // 重新计算表格列
}

// 添加废物行
const addWasteRow = () => {
  const newRow = {
    id: Date.now(),
    category: '',
    name: '',
    unit: '吨'
  }
  
  // 根据选择的年份范围初始化数据
  const yearRange = selectedYearRange.value.split('-')
  const startYear = parseInt(yearRange[0])
  const endYear = parseInt(yearRange[1])
  
  for (let year = startYear; year <= endYear; year++) {
    newRow[`amount_${year}`] = null
  }
  
  formData.value.waste.push(newRow)
}

// 删除废物行
const removeWasteRow = (index) => {
  formData.value.waste.splice(index, 1)
}

// 确保数据结构完整
watch(() => props.modelValue, (newVal) => {
  if (newVal) {
    if (!newVal.waste) {
      newVal.waste = []
    }
    
    // 如果表格为空，添加一条空白记录
    if (newVal.waste.length === 0) {
      addWasteRow()
    }
  }
}, { immediate: true, deep: true })
</script>

<style scoped>
.solid-waste-form {
  padding: 16px 0;
}

.waste-card {
  border: 1px solid #e0e0e6;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.waste-card:hover {
  border-color: #18a058;
  box-shadow: 0 2px 8px rgba(24, 160, 88, 0.15);
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







