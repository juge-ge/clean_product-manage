<template>
  <div class="quantitative-indicator">
    <div class="value-display">
      <span class="current-value">{{ formatValue(row.currentValue, row.unit) }}</span>
      <n-tag 
        :type="getLevelTagType(row.level)" 
        size="small"
        class="ml-2"
      >
        {{ row.level || '待评估' }}
      </n-tag>
    </div>
    <n-button 
      size="small" 
      type="primary" 
      @click="showManualOverride"
      :disabled="disabled"
    >
      手动调整
    </n-button>
    
    <!-- 手动调整弹窗 -->
    <n-modal v-model:show="showOverrideModal" preset="card" title="手动调整评级" style="width: 400px">
      <n-form :model="overrideForm" :rules="overrideRules" ref="formRef">
        <n-form-item label="当前值" path="currentValue">
          <n-input-number
            v-model:value="overrideForm.currentValue"
            :min="0"
            :precision="2"
            :disabled="true"
          />
        </n-form-item>
        <n-form-item label="评级" path="level">
          <n-select
            v-model:value="overrideForm.level"
            :options="options"
            placeholder="请选择评级"
          />
        </n-form-item>
        <n-form-item label="调整原因" path="reason">
          <n-input
            v-model:value="overrideForm.reason"
            type="textarea"
            placeholder="请输入调整原因"
            :rows="3"
          />
        </n-form-item>
      </n-form>
      <template #footer>
        <n-space justify="end">
          <n-button @click="showOverrideModal = false">取消</n-button>
          <n-button type="primary" @click="handleOverride">确认</n-button>
        </n-space>
      </template>
    </n-modal>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { NSelect, NTag, NButton, NModal, NForm, NFormItem, NInputNumber, NInput, NSpace } from 'naive-ui'

const props = defineProps({
  row: {
    type: Object,
    required: true
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update'])

const showOverrideModal = ref(false)
const formRef = ref(null)

const overrideForm = ref({
  currentValue: null,
  level: '',
  reason: ''
})

const overrideRules = {
  level: [
    { required: true, message: '请选择评级', trigger: 'change' }
  ],
  reason: [
    { required: true, message: '请输入调整原因', trigger: 'blur' }
  ]
}

const options = [
  { value: 'I级', label: 'I级' },
  { value: 'II级', label: 'II级' },
  { value: 'III级', label: 'III级' },
  { value: '不达标', label: '不达标' }
]

const formatValue = (value, unit) => {
  if (value === null || value === undefined) return '-'
  return `${value.toFixed(2)}${unit || ''}`
}

const getLevelTagType = (level) => {
  const types = {
    'I级': 'success',
    'II级': 'info',
    'III级': 'warning',
    '不达标': 'error'
  }
  return types[level] || 'default'
}

const showManualOverride = () => {
  overrideForm.value = {
    currentValue: props.row.currentValue,
    level: props.row.level || '',
    reason: ''
  }
  showOverrideModal.value = true
}

const handleOverride = async () => {
  try {
    await formRef.value?.validate()
    emit('update', props.row.id, overrideForm.value.level, overrideForm.value.reason)
    showOverrideModal.value = false
  } catch (error) {
    console.error('表单验证失败:', error)
  }
}
</script>

<style scoped>
.quantitative-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
}

.value-display {
  display: flex;
  align-items: center;
}

.current-value {
  font-weight: 500;
  color: #333;
}

.ml-2 {
  margin-left: 8px;
}
</style>
