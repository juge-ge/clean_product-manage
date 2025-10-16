<template>
  <div class="limiting-indicator">
    <n-select
      v-model:value="indicator.level"
      :options="levelOptions"
      placeholder="请选择"
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
  { label: '符合', value: '符合' },
  { label: '不符合', value: '不符合' }
]

const handleLevelChange = (value) => {
  // 限定性指标：符合得满分，不符合得0分
  const score = value === '符合' ? 100 : 0
  
  const updatedIndicator = {
    ...props.indicator,
    level: value,
    score
  }
  
  emit('update', updatedIndicator)
}
</script>

<style scoped>
.limiting-indicator {
  display: flex;
  align-items: center;
}
</style>
