<template>
  <div class="audit-progress">
    <n-steps
      :current="currentStep"
      :status="status"
      size="small"
    >
      <n-step
        v-for="(step, index) in steps"
        :key="index"
        :title="step.title"
        :description="step.description"
        @click="handleStepClick(step, index)"
        class="cursor-pointer"
      >
        <template #icon>
          <n-icon>
            <component :is="getStepIcon(index)" />
          </n-icon>
        </template>
      </n-step>
    </n-steps>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { NSteps, NStep } from 'naive-ui'
import { renderIcon } from '@/utils'

const props = defineProps({
  currentStep: {
    type: Number,
    default: 0
  },
  steps: {
    type: Array,
    default: () => [
      { title: '企业信息', description: '基本信息录入' },
      { title: '筹划与组织', description: '审核团队组建' },
      { title: '预审核', description: '数据填报评估' },
      { title: '审核', description: '指标审核' },
      { title: '方案库', description: '整改方案' },
      { title: '审核报告', description: '报告生成' }
    ]
  }
})

const emit = defineEmits(['step-click'])

const status = computed(() => {
  if (props.currentStep === props.steps.length - 1) return 'finish'
  return 'process'
})

const getStepIcon = (index) => {
  const icons = [
    'carbon:document',
    'carbon:user-multiple',
    'carbon:search',
    'carbon:checkmark-filled',
    'carbon:library',
    'carbon:document-text'
  ]
  return renderIcon(icons[index] || 'carbon:document')
}

const handleStepClick = (step, index) => {
  emit('step-click', { ...step, index })
}
</script>

<style scoped>
.audit-progress {
  padding: 20px;
  background: var(--n-color-light-hover);
  border-radius: 8px;
}

:deep(.n-step) {
  &.n-step--finish {
    .n-step-indicator {
      color: var(--n-color-success);
    }
  }

  &.n-step--process {
    .n-step-indicator {
      color: var(--n-color-primary);
    }
  }
}
</style>
