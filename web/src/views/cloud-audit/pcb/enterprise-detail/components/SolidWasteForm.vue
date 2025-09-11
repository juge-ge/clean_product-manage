<template>
  <div class="solid-waste-form">
    <n-tabs type="line">
      <n-tab-pane name="general" tab="一般固废">
        <div class="waste-section">
          <n-data-table
            :columns="generalColumns"
            :data="formData.general"
            :row-key="row => row.id"
            :pagination="false"
          />
          <n-button type="primary" class="mt-4" @click="addGeneralRow">
            <template #icon>
              <TheIcon icon="carbon:add" />
            </template>
            添加一般固废数据
          </n-button>
        </div>
      </n-tab-pane>
      
      <n-tab-pane name="hazardous" tab="危险废物">
        <div class="waste-section">
          <n-data-table
            :columns="hazardousColumns"
            :data="formData.hazardous"
            :row-key="row => row.id"
            :pagination="false"
          />
          <n-button type="primary" class="mt-4" @click="addHazardousRow">
            <template #icon>
              <TheIcon icon="carbon:add" />
            </template>
            添加危险废物数据
          </n-button>
        </div>
      </n-tab-pane>
    </n-tabs>
  </div>
</template>

<script setup>
import { computed, h } from 'vue'
import { 
  NTabs, 
  NTabPane, 
  NDataTable, 
  NButton, 
  NInput,
  NInputNumber, 
  NSelect 
} from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      general: [],
      hazardous: []
    })
  }
})

const emit = defineEmits(['update:modelValue'])

const formData = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const yearOptions = [
  { label: '2022', value: 2022 },
  { label: '2023', value: 2023 },
  { label: '2024', value: 2024 }
]

// 一般固废表格列
const generalColumns = [
  { 
    title: '年份', 
    key: 'year', 
    width: 100,
    render: (row) => h(NSelect, {
      value: row.year,
      options: yearOptions,
      onUpdateValue: (value) => { row.year = value }
    })
  },
  { 
    title: '废物名称', 
    key: 'name', 
    width: 180,
    render: (row) => h(NInput, {
      value: row.name,
      placeholder: "如：废覆铜板边角料",
      onUpdateValue: (value) => { row.name = value }
    })
  },
  { 
    title: '废物类别', 
    key: 'type', 
    width: 120,
    render: (row) => h(NSelect, {
      value: row.type,
      options: [
        { label: 'HW49', value: 'HW49' },
        { label: '一般工业固废', value: '一般工业固废' },
        { label: '其他', value: '其他' }
      ],
      onUpdateValue: (value) => { row.type = value }
    })
  },
  { 
    title: '产生量（t）', 
    key: 'amount', 
    width: 120,
    render: (row) => h(NInputNumber, {
      value: row.amount,
      min: 0,
      precision: 2,
      onUpdateValue: (value) => { row.amount = value }
    })
  },
  { 
    title: '操作', 
    key: 'action', 
    width: 80,
    render: (row, index) => h(NButton, {
      size: "small",
      type: "error",
      onClick: () => removeGeneralRow(index)
    }, () => '删除')
  }
]

// 危险废物表格列
const hazardousColumns = [
  { 
    title: '年份', 
    key: 'year', 
    width: 100,
    render: (row) => h(NSelect, {
      value: row.year,
      options: yearOptions,
      onUpdateValue: (value) => { row.year = value }
    })
  },
  { 
    title: '废物名称', 
    key: 'name', 
    width: 150,
    render: (row) => h(NInput, {
      value: row.name,
      placeholder: "如：废蚀刻液",
      onUpdateValue: (value) => { row.name = value }
    })
  },
  { 
    title: '危废类别', 
    key: 'type', 
    width: 100,
    render: (row) => h(NSelect, {
      value: row.type,
      options: [
        { label: 'HW17', value: 'HW17' },
        { label: 'HW22', value: 'HW22' },
        { label: 'HW49', value: 'HW49' },
        { label: '其他', value: '其他' }
      ],
      onUpdateValue: (value) => { row.type = value }
    })
  },
  { 
    title: '废物代码', 
    key: 'code', 
    width: 130,
    render: (row) => h(NInput, {
      value: row.code,
      placeholder: "如：336-064-17",
      onUpdateValue: (value) => { row.code = value }
    })
  },
  { 
    title: '产生量（t）', 
    key: 'amount', 
    width: 120,
    render: (row) => h(NInputNumber, {
      value: row.amount,
      min: 0,
      precision: 2,
      onUpdateValue: (value) => { row.amount = value }
    })
  },
  { 
    title: '操作', 
    key: 'action', 
    width: 80,
    render: (row, index) => h(NButton, {
      size: "small",
      type: "error",
      onClick: () => removeHazardousRow(index)
    }, () => '删除')
  }
]

// 添加数据行方法
const addGeneralRow = () => {
  formData.value.general.push({
    id: Date.now(),
    year: 2023,
    name: '',
    type: '',
    amount: null
  })
}

const addHazardousRow = () => {
  formData.value.hazardous.push({
    id: Date.now(),
    year: 2023,
    name: '',
    type: '',
    code: '',
    amount: null
  })
}

// 删除数据行方法
const removeGeneralRow = (index) => {
  formData.value.general.splice(index, 1)
}

const removeHazardousRow = (index) => {
  formData.value.hazardous.splice(index, 1)
}
</script>

<style scoped>
.solid-waste-form {
  padding: 16px 0;
}

.waste-section {
  min-height: 200px;
}
</style>

