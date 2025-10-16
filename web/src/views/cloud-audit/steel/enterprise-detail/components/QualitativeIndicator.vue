<template>
  <div class="qualitative-indicator">
    <n-select
      v-model:value="indicator.level"
      :options="levelOptions"
      placeholder="请选择等级"
      size="small"
      style="width: 120px"
      @update:value="handleLevelChange"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { NSelect } from 'naive-ui'

const props = defineProps({
  indicator: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update'])

const levelOptions = [
  { label: 'I级', value: 'I级' },
  { label: 'II级', value: 'II级' },
  { label: 'III级', value: 'III级' },
  { label: '不达标', value: '不达标' }
]

const handleLevelChange = (value) => {
  // 根据等级计算得分
  const scoreMap = {
    'I级': 100,
    'II级': 80,
    'III级': 60,
    '不达标': 0
  }
  
  const updatedIndicator = {
    ...props.indicator,
    level: value,
    score: scoreMap[value] || 0
  }
  
  emit('update', updatedIndicator)
}
</script>

<style scoped>
.qualitative-indicator {
  display: flex;
  align-items: center;
}
</style>
