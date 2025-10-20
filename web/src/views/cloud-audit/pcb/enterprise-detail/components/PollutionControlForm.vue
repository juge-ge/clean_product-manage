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
          class="sub-module"
        />
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
          class="sub-module"
        />
      </n-card>
    </n-space>
  </div>
</template>

<script setup>
import { computed, h, watch } from 'vue'
import { 
  NSpace,
  NCard,
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
      wastewater: [],
      wasteGas: []
    })
  }
})

const emit = defineEmits(['update:modelValue'])

const formData = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

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

// 确保数据结构完整
watch(() => props.modelValue, (newVal) => {
  if (newVal) {
    if (!newVal.wastewater) {
      newVal.wastewater = []
    }
    if (!newVal.wasteGas) {
      newVal.wasteGas = []
    }
    
    // 如果表格为空，添加一条空白记录
    if (newVal.wastewater.length === 0) {
      addWastewaterRow()
    }
    if (newVal.wasteGas.length === 0) {
      addWasteGasRow()
    }
  }
}, { immediate: true, deep: true })
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






