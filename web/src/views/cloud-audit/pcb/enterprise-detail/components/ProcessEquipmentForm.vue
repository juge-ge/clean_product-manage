<template>
  <div class="process-equipment-form">
    <n-tabs type="line">
      <n-tab-pane name="rigid" tab="刚性印制电路板">
        <n-space vertical :size="16">
          <n-card 
            v-for="(type, key) in rigidTypes" 
            :key="key"
            :title="type.label"
            size="small"
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
        </n-space>
      </n-tab-pane>
      
      <n-tab-pane name="flexible" tab="挠性印制板">
        <n-space vertical :size="16">
          <n-card 
            v-for="(type, key) in flexibleTypes" 
            :key="key"
            :title="type.label"
            size="small"
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
        </n-space>
      </n-tab-pane>
    </n-tabs>
  </div>
</template>

<script setup>
import { computed, watch } from 'vue'
import { 
  NTabs, 
  NTabPane, 
  NCard, 
  NSpace, 
  NGrid, 
  NFormItemGi, 
  NInput 
} from 'naive-ui'

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
  double: { label: '双面板' },
  multilayer: { label: '多层板' }
}

const flexibleTypes = {
  single: { label: '单面板' },
  double: { label: '双面板' },
  multilayer: { label: '多层板' }
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
</style>

