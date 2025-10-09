<template>
  <div class="limiting-indicator">
    <n-switch
      :value="isCompliant"
      @update:value="handleSwitchChange"
      :disabled="disabled"
    >
      <template #checked>
        <span class="text-green-600">达标</span>
      </template>
      <template #unchecked>
        <span class="text-red-600">不达标</span>
      </template>
    </n-switch>
    <n-tooltip trigger="hover" v-if="!isCompliant">
      <template #trigger>
        <n-icon class="ml-1 text-red-500 cursor-pointer">
          ⚠️
        </n-icon>
      </template>
      <span>限定性指标不达标，总评级不得高于III级</span>
    </n-tooltip>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { NSwitch, NTooltip, NIcon } from 'naive-ui'
import { useDialog } from 'naive-ui'

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
const dialog = useDialog()

const isCompliant = computed(() => {
  return props.row.level === 'I级'
})

const handleSwitchChange = (value) => {
  if (!value) {
    // 不达标时显示警告
    dialog.warning({
      title: '限定性指标警告',
      content: '该指标不达标，总评级不得高于III级。确定要继续吗？',
      positiveText: '确认',
      negativeText: '取消',
      onPositiveClick: () => {
        emit('update', props.row.id, '不达标')
      }
    })
  } else {
    emit('update', props.row.id, 'I级')
  }
}
</script>

<style scoped>
.limiting-indicator {
  display: flex;
  align-items: center;
}

.text-green-600 {
  color: #16a34a;
}

.text-red-600 {
  color: #dc2626;
}

.text-red-500 {
  color: #ef4444;
}

.ml-1 {
  margin-left: 4px;
}

.cursor-pointer {
  cursor: pointer;
}
</style>
