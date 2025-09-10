<template>
  <div class="standard-comparison">
    <n-tag 
      :type="getLevelType(level)"
      :bordered="false"
      size="small"
    >
      {{ getLevelText(level) }}
    </n-tag>
    <span class="ml-2 text-sm text-gray-500">
      标准值：{{ standard.value }} {{ standard.unit }}
    </span>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { NTag } from 'naive-ui'

const props = defineProps({
  value: Number,
  standard: Object
})

const level = computed(() => {
  if (!props.value || !props.standard) return 'unknown'
  
  const { value } = props
  const { level1, level2, level3 } = props.standard
  
  if (value <= level1) return 'level1'
  if (value <= level2) return 'level2'
  if (value <= level3) return 'level3'
  return 'unqualified'
})

const getLevelType = (level) => {
  const types = {
    level1: 'success',
    level2: 'info',
    level3: 'warning',
    unqualified: 'error',
    unknown: 'default'
  }
  return types[level] || 'default'
}

const getLevelText = (level) => {
  const texts = {
    level1: 'I级',
    level2: 'II级',
    level3: 'III级',
    unqualified: '不达标',
    unknown: '未评估'
  }
  return texts[level] || '未知'
}
</script>

<style scoped>
.standard-comparison {
  display: flex;
  align-items: center;
  margin-top: 8px;
}

.text-sm {
  font-size: 12px;
}

.text-gray-500 {
  color: #6b7280;
}

.ml-2 {
  margin-left: 8px;
}
</style>


