<template>
  <div class="audit-progress">
    <n-card title="审核进度">
      <div class="progress-steps">
        <div 
          v-for="(step, index) in steps" 
          :key="step.key"
          class="step-item"
          :class="{ 
            'active': currentStep === index,
            'completed': currentStep > index,
            'disabled': currentStep < index
          }"
        >
          <div class="step-icon">
            <TheIcon 
              :icon="step.icon" 
              :size="20"
            />
          </div>
          <div class="step-content">
            <div class="step-title">{{ step.title }}</div>
            <div class="step-description">{{ step.description }}</div>
          </div>
          <div v-if="index < steps.length - 1" class="step-connector"></div>
        </div>
      </div>
    </n-card>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { NCard } from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'

const props = defineProps({
  currentStep: {
    type: Number,
    default: 0
  },
  steps: {
    type: Array,
    default: () => [
      {
        key: 'basic-info',
        title: '企业信息',
        description: '基本信息录入',
        icon: 'carbon:enterprise'
      },
      {
        key: 'planning',
        title: '筹划组织',
        description: '审核计划制定',
        icon: 'carbon:plan'
      },
      {
        key: 'pre-audit',
        title: '预审核',
        description: '初步审核评估',
        icon: 'carbon:document-attachment'
      },
      {
        key: 'audit',
        title: '审核',
        description: '正式审核实施',
        icon: 'carbon:checkmark-filled'
      },
      {
        key: 'scheme-library',
        title: '方案库',
        description: '方案制定管理',
        icon: 'carbon:library'
      },
      {
        key: 'report',
        title: '报告',
        description: '审核报告生成',
        icon: 'carbon:document'
      }
    ]
  }
})
</script>

<style scoped>
.audit-progress {
  margin-bottom: 24px;
}

.progress-steps {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  overflow-x: auto;
  padding: 16px 0;
}

.step-item {
  display: flex;
  align-items: center;
  position: relative;
  min-width: 200px;
  flex-shrink: 0;
}

.step-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f5f5;
  color: #999;
  transition: all 0.3s ease;
  margin-right: 12px;
}

.step-item.active .step-icon {
  background-color: #18a058;
  color: white;
}

.step-item.completed .step-icon {
  background-color: #18a058;
  color: white;
}

.step-item.disabled .step-icon {
  background-color: #f5f5f5;
  color: #ccc;
}

.step-content {
  flex: 1;
}

.step-title {
  font-weight: 500;
  color: #333;
  margin-bottom: 4px;
}

.step-item.active .step-title {
  color: #18a058;
}

.step-item.disabled .step-title {
  color: #ccc;
}

.step-description {
  font-size: 12px;
  color: #666;
}

.step-item.disabled .step-description {
  color: #ccc;
}

.step-connector {
  position: absolute;
  right: -8px;
  top: 20px;
  width: 16px;
  height: 2px;
  background-color: #e0e0e0;
  z-index: 1;
}

.step-item.completed + .step-item .step-connector {
  background-color: #18a058;
}

@media (max-width: 768px) {
  .progress-steps {
    flex-direction: column;
    gap: 12px;
  }
  
  .step-item {
    min-width: auto;
  }
  
  .step-connector {
    display: none;
  }
}
</style>
