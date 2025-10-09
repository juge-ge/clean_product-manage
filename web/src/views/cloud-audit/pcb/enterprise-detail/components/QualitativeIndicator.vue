<template>
  <n-select
    :value="row.level"
    :options="options"
    placeholder="请选择评级"
    @update:value="handleUpdate"
    :disabled="disabled"
  >
    <template #option="{ option }">
      <div>
        <div>{{ option.label }}</div>
        <div class="text-xs text-gray-500">{{ option.description }}</div>
      </div>
    </template>
  </n-select>
</template>

<script setup>
import { NSelect } from 'naive-ui'

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

const options = [
  { value: 'I级', label: 'I级', description: '采用国际先进工艺和设备' },
  { value: 'II级', label: 'II级', description: '采用国内先进工艺和设备' },
  { value: 'III级', label: 'III级', description: '采用一般工艺和设备' },
  { value: '不达标', label: '不达标', description: '工艺和设备落后' }
]

const handleUpdate = (value) => {
  emit('update', props.row.id, value)
}
</script>

<style scoped>
.text-xs {
  font-size: 12px;
}

.text-gray-500 {
  color: #6b7280;
}
</style>
