<template>
  <div class="process-equipment-form">
    <n-tabs type="line">
      <n-tab-pane name="rigid" tab="刚性印制电路板">
        <n-space vertical :size="16">
          <!-- 基础板型 -->
          <n-card 
            v-for="(type, key) in rigidTypes" 
            :key="key"
            :title="type.label"
            size="small"
            class="sub-module"
          >
            <n-grid :cols="1" :y-gap="12">
              <n-form-item-gi label="产线">
                <n-input
                  v-model:value="formData.rigid[key].line"
                  placeholder="请输入产线信息"
                />
              </n-form-item-gi>
              <n-form-item-gi label="工序">
                <n-input
                  v-model:value="formData.rigid[key].process"
                  type="textarea"
                  placeholder="请输入工序信息"
                  :rows="2"
                />
              </n-form-item-gi>
              <n-form-item-gi label="设备">
                <n-input
                  v-model:value="formData.rigid[key].equipment"
                  type="textarea"
                  placeholder="请输入设备信息"
                  :rows="2"
                />
              </n-form-item-gi>
            </n-grid>
          </n-card>

          <!-- 多层板 -->
          <n-card 
            v-for="item in multilayerList.rigid" 
            :key="item.id"
            :title="item.label"
            size="small"
            class="sub-module"
          >
            <n-grid :cols="1" :y-gap="12">
              <n-form-item-gi label="产线">
                <n-input
                  v-model:value="formData.rigid[item.key].line"
                  placeholder="请输入产线信息"
                />
              </n-form-item-gi>
              <n-form-item-gi label="工序">
                <n-input
                  v-model:value="formData.rigid[item.key].process"
                  type="textarea"
                  placeholder="请输入工序信息"
                  :rows="2"
                />
              </n-form-item-gi>
              <n-form-item-gi label="设备">
                <n-input
                  v-model:value="formData.rigid[item.key].equipment"
                  type="textarea"
                  placeholder="请输入设备信息"
                  :rows="2"
                />
              </n-form-item-gi>
            </n-grid>
          </n-card>

          <!-- 添加多层板按钮 -->
          <div class="action-bar">
            <n-button type="primary" @click="showAddMultilayerModal('rigid')">
              <template #icon>
                <TheIcon icon="carbon:add" />
              </template>
              添加多层板
            </n-button>
          </div>
        </n-space>
      </n-tab-pane>
      
      <n-tab-pane name="flexible" tab="挠性印制板">
        <n-space vertical :size="16">
          <!-- 基础板型 -->
          <n-card 
            v-for="(type, key) in flexibleTypes" 
            :key="key"
            :title="type.label"
            size="small"
            class="sub-module"
          >
            <n-grid :cols="1" :y-gap="12">
              <n-form-item-gi label="产线">
                <n-input
                  v-model:value="formData.flexible[key].line"
                  placeholder="请输入产线信息"
                />
              </n-form-item-gi>
              <n-form-item-gi label="工序">
                <n-input
                  v-model:value="formData.flexible[key].process"
                  type="textarea"
                  placeholder="请输入工序信息"
                  :rows="2"
                />
              </n-form-item-gi>
              <n-form-item-gi label="设备">
                <n-input
                  v-model:value="formData.flexible[key].equipment"
                  type="textarea"
                  placeholder="请输入设备信息"
                  :rows="2"
                />
              </n-form-item-gi>
            </n-grid>
          </n-card>

          <!-- 多层板 -->
          <n-card 
            v-for="item in multilayerList.flexible" 
            :key="item.id"
            :title="item.label"
            size="small"
            class="sub-module"
          >
            <n-grid :cols="1" :y-gap="12">
              <n-form-item-gi label="产线">
                <n-input
                  v-model:value="formData.flexible[item.key].line"
                  placeholder="请输入产线信息"
                />
              </n-form-item-gi>
              <n-form-item-gi label="工序">
                <n-input
                  v-model:value="formData.flexible[item.key].process"
                  type="textarea"
                  placeholder="请输入工序信息"
                  :rows="2"
                />
              </n-form-item-gi>
              <n-form-item-gi label="设备">
                <n-input
                  v-model:value="formData.flexible[item.key].equipment"
                  type="textarea"
                  placeholder="请输入设备信息"
                  :rows="2"
                />
              </n-form-item-gi>
            </n-grid>
          </n-card>

          <!-- 添加多层板按钮 -->
          <div class="action-bar">
            <n-button type="primary" @click="showAddMultilayerModal('flexible')">
              <template #icon>
                <TheIcon icon="carbon:add" />
              </template>
              添加多层板
            </n-button>
          </div>
        </n-space>
      </n-tab-pane>
    </n-tabs>

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
  NTabs, 
  NTabPane, 
  NCard, 
  NSpace, 
  NGrid, 
  NFormItemGi, 
  NInput,
  NButton,
  NModal,
  NForm,
  NFormItem,
  NSelect,
  NIcon
} from 'naive-ui'
import { renderIcon } from '@/utils'
import TheIcon from '@/components/icon/TheIcon.vue'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      rigid: {
        single: { line: '', process: '', equipment: '' },
        double: { line: '', process: '', equipment: '' },
        multilayer: { line: '', process: '', equipment: '' }
      },
      flexible: {
        single: { line: '', process: '', equipment: '' },
        double: { line: '', process: '', equipment: '' },
        multilayer: { line: '', process: '', equipment: '' }
      }
    })
  }
})

const emit = defineEmits(['update:modelValue'])

const formData = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const rigidTypes = {
  single: { label: '单面板' },
  double: { label: '双面板' }
}

const flexibleTypes = {
  single: { label: '单面板' },
  double: { label: '双面板' }
}

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

// 多层板相关状态
const showModal = ref(false)
const currentMode = ref('') // 'rigid' or 'flexible'
const modalForm = ref({
  type: null,
  layers: null
})
const formRef = ref(null)
const multilayerList = ref({
  rigid: [],
  flexible: []
})

const modalRules = {
  type: { required: true, message: '请选择板类型' },
  layers: { required: true, message: '请选择层数' }
}

// 显示添加多层板弹窗
const showAddMultilayerModal = (mode) => {
  currentMode.value = mode
  modalForm.value = {
    type: null,
    layers: null
  }
  showModal.value = true
}

// 处理添加多层板
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
    
    multilayerList.value[currentMode.value].push(newItem)
    formData.value[currentMode.value][newItem.key] = { line: '', process: '', equipment: '' }
    
    showModal.value = false
    window.$message.success('添加成功')
  } catch (err) {
    // 表单验证失败
  }
}

// 确保数据结构完整
watch(() => props.modelValue, (newVal) => {
  if (newVal) {
    // 确保刚性板数据结构
    if (!newVal.rigid) newVal.rigid = {}
    Object.keys(rigidTypes).forEach(key => {
      if (!newVal.rigid[key]) {
        newVal.rigid[key] = { line: '', process: '', equipment: '' }
      }
    })
    
    // 确保挠性板数据结构
    if (!newVal.flexible) newVal.flexible = {}
    Object.keys(flexibleTypes).forEach(key => {
      if (!newVal.flexible[key]) {
        newVal.flexible[key] = { line: '', process: '', equipment: '' }
      }
    })
  }
}, { immediate: true, deep: true })
</script>

<style scoped>
.process-equipment-form {
  padding: 16px 0;
}

.action-bar {
  display: flex;
  justify-content: center;
  border-top: 1px solid var(--n-border-color);
  padding-top: 16px;
  margin-top: 16px;
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





