<template>
  <div class="quantitative-indicator">
    <n-input-number
      v-model:value="indicator.currentValue"
      placeholder="请输入当前值"
      :min="0"
      :precision="2"
      size="small"
      style="width: 120px"
      :show-button="false"
      @update:value="handleValueChange"
    />
    <span class="unit">{{ indicator.unit }}</span>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { NInputNumber } from 'naive-ui'

const props = defineProps({
  indicator: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update'])

const handleValueChange = (value) => {
  if (value === null || value === undefined) return
  
  // 根据标准值计算等级和得分
  const { standardValues } = props.indicator
  let level = '不达标'
  let score = 0
  
  if (standardValues) {
    if (value <= standardValues.level1) {
      level = 'I级'
      score = 100
    } else if (value <= standardValues.level2) {
      level = 'II级'
      score = 80
    } else if (value <= standardValues.level3) {
      level = 'III级'
      score = 60
    }
  }
  
  const updatedIndicator = {
    ...props.indicator,
    currentValue: value,
    level,
    score
  }
  
  emit('update', updatedIndicator)
}
</script>

<style scoped>
.quantitative-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
}

.unit {
  color: var(--n-text-color-secondary);
  font-size: 12px;
}
</style>
