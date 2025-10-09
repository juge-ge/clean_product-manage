<template>
  <div class="production-info-form">
    <!-- 产能部分 -->
    <n-card class="sub-module">
      <n-h3 class="cursor-pointer hover:text-primary" @click="handleTitleClick">产能</n-h3>
      <n-tabs type="line">
        <n-tab-pane 
          v-for="year in years" 
          :key="year" 
          :name="year" 
          :tab="`${year}年产能`"
        >
          <n-grid :cols="2" :x-gap="24">
            <n-form-item-gi 
              v-for="type in baseProductionTypes" 
              :key="type.key"
              :label="`${type.label}（${type.unit}）`"
            >
              <n-input-number 
                v-model:value="formData.capacity[year][type.key]"
                placeholder="请输入产能"
                :min="0"
                :precision="2"
              />
            </n-form-item-gi>
          </n-grid>

          <!-- 多层板产能 -->
          <div v-for="item in multilayerCapacityList" :key="item.id" class="mt-4">
            <n-grid :cols="2" :x-gap="24">
              <n-form-item-gi :label="`${item.label}（平方米/年）`">
                <n-input-number 
                  v-model:value="formData.capacity[year][item.key]"
                  placeholder="请输入产能"
                  :min="0"
                  :precision="2"
                />
              </n-form-item-gi>
            </n-grid>
          </div>

          <!-- 添加多层板按钮 -->
          <div class="action-bar">
            <n-button type="primary" @click="showAddMultilayerModal('capacity')">
              <template #icon>
                <TheIcon icon="carbon:add" />
              </template>
              添加多层板
            </n-button>
          </div>
        </n-tab-pane>
      </n-tabs>
    </n-card>
    
    <!-- 产量部分 -->
    <n-card class="mt-4 sub-module">
      <n-h3 class="cursor-pointer hover:text-primary" @click="handleTitleClick">产量</n-h3>
      <n-tabs type="line">
        <n-tab-pane 
          v-for="year in years" 
          :key="year" 
          :name="year" 
          :tab="`${year}年产量`"
        >
          <n-grid :cols="2" :x-gap="24">
            <n-form-item-gi 
              v-for="type in baseProductionTypes" 
              :key="type.key"
              :label="`${type.label}（${type.unit}）`"
            >
              <n-input-number 
                v-model:value="formData.output[year][type.key]"
                placeholder="请输入产量"
                :min="0"
                :precision="2"
              />
            </n-form-item-gi>
          </n-grid>

          <!-- 多层板产量 -->
          <div v-for="item in multilayerOutputList" :key="item.id" class="mt-4">
            <n-grid :cols="2" :x-gap="24">
              <n-form-item-gi :label="`${item.label}（平方米/年）`">
                <n-input-number 
                  v-model:value="formData.output[year][item.key]"
                  placeholder="请输入产量"
                  :min="0"
                  :precision="2"
                />
              </n-form-item-gi>
            </n-grid>
          </div>

          <!-- 添加多层板按钮 -->
          <div class="action-bar mt-4">
            <n-button type="primary" @click="showAddMultilayerModal('output')">
              <template #icon>
                <TheIcon icon="carbon:add" />
              </template>
              添加多层板
            </n-button>
          </div>
        </n-tab-pane>
      </n-tabs>
    </n-card>

    <!-- 添加多层板弹窗 -->
    <n-modal v-model:show="showModal" preset="dialog" title="添加多层板">
      <n-form ref="formRef" :model="modalForm" :rules="modalRules">
        <n-form-item label="板类型" path="type">
          <n-select
            v-model:value="modalForm.type"
            :options="multilayerTypes"
            placeholder="请选择板类型"
          />
        </n-form-item>
        <n-form-item label="层数" path="layers">
          <n-select
            v-model:value="modalForm.layers"
            :options="layerOptions"
            placeholder="请选择层数"
          />
        </n-form-item>
      </n-form>
      <template #action>
        <n-button type="primary" @click="handleAddMultilayer">确认</n-button>
      </template>
    </n-modal>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { 
  NFormItem, NInputNumber, NTabs, NTabPane, NGrid, NFormItemGi, NCard,
  NButton, NModal, NForm, NSelect, NH3, NIcon
} from 'naive-ui'
import { renderIcon } from '@/utils'
import TheIcon from '@/components/icon/TheIcon.vue'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      capacity: {
        '2022': {},
        '2023': {},
        '2024': {}
      },
      output: {
        '2022': {},
        '2023': {},
        '2024': {}
      }
    })
  }
})

const emit = defineEmits(['update:modelValue'])

// 常量定义
const years = ['2022', '2023', '2024']
const baseProductionTypes = [
  { key: 'rigidSingle', label: '刚性单面板', unit: '平方米/年' },
  { key: 'rigidDouble', label: '刚性双面板', unit: '平方米/年' },
  { key: 'flexibleSingle', label: '挠性单面板', unit: '平方米/年' },
  { key: 'flexibleDouble', label: '挠性双面板', unit: '平方米/年' }
]

const multilayerTypes = [
  { key: 'rigidMultilayer', label: '刚性多层板' },
  { key: 'rigidHDI', label: '刚性HDI板' },
  { key: 'flexibleMultilayer', label: '挠性多层板' },
  { key: 'flexibleHDI', label: '挠性HDI板' }
]

const layerOptions = Array.from({ length: 30 }, (_, i) => ({
  label: `${i + 3}层`,
  value: i + 3
}))

const modalRules = {
  type: { required: true, message: '请选择板类型' },
  layers: { required: true, message: '请选择层数' }
}

// 响应式状态
const showModal = ref(false)
const currentMode = ref('') // 'capacity' or 'output'
const modalForm = ref({
  type: null,
  layers: null
})
const formRef = ref(null)
const multilayerCapacityList = ref([])
const multilayerOutputList = ref([])

// 计算属性
const formData = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// 方法定义
const handleTitleClick = (title) => {
  window.$message.info(`点击了${title}`)
}

const showAddMultilayerModal = (mode) => {
  currentMode.value = mode
  modalForm.value = {
    type: null,
    layers: null
  }
  showModal.value = true
}

const handleAddMultilayer = async () => {
  try {
    await formRef.value?.validate()
    const { type, layers } = modalForm.value
    const selectedType = multilayerTypes.find(t => t.key === type)
    const newItem = {
      id: Date.now(),
      key: `${type}_${layers}`,
      label: `${selectedType.label}(${layers}层)`
    }
    
    if (currentMode.value === 'capacity') {
      multilayerCapacityList.value.push(newItem)
      years.forEach(year => {
        if (!formData.value.capacity[year]) {
          formData.value.capacity[year] = {}
        }
        formData.value.capacity[year][newItem.key] = null
      })
    } else {
      multilayerOutputList.value.push(newItem)
      years.forEach(year => {
        if (!formData.value.output[year]) {
          formData.value.output[year] = {}
        }
        formData.value.output[year][newItem.key] = null
      })
    }
    
    showModal.value = false
    window.$message.success('添加成功')
  } catch (err) {
    // 表单验证失败
  }
}

// 确保数据结构完整
watch(() => props.modelValue, (newVal) => {
  if (newVal) {
    // 确保产能数据结构完整
    if (!newVal.capacity) {
      newVal.capacity = {}
    }
    years.forEach(year => {
      if (!newVal.capacity[year]) {
        newVal.capacity[year] = {}
      }
      baseProductionTypes.forEach(type => {
        if (!(type.key in newVal.capacity[year])) {
          newVal.capacity[year][type.key] = null
        }
      })
    })

    // 确保产量数据结构完整
    if (!newVal.output) {
      newVal.output = {}
    }
    years.forEach(year => {
      if (!newVal.output[year]) {
        newVal.output[year] = {}
      }
      baseProductionTypes.forEach(type => {
        if (!(type.key in newVal.output[year])) {
          newVal.output[year][type.key] = null
        }
      })
    })
  }
}, { immediate: true, deep: true })
</script>

<style scoped>
.production-info-form {
  padding: 16px 0;
}

.action-bar {
  display: flex;
  justify-content: center;
  border-top: 1px solid var(--n-border-color);
  padding-top: 16px;
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
</style>




