<template>
  <div class="metric-card" :class="`metric-${metric.key}`">
    <div class="metric-icon">
      <TheIcon :icon="metric.icon" :size="24" />
    </div>
    <div class="metric-content">
      <div class="metric-value">
        <span class="value-number">{{ animatedValue }}</span>
        <span v-if="metric.total" class="value-total">/{{ metric.total }}</span>
        <span class="value-unit">{{ metric.unit }}</span>
      </div>
      <div class="metric-label">{{ metric.label }}</div>
      <div v-if="metric.trend" class="metric-trend" :class="trendClass">
        <TheIcon :icon="trendIcon" :size="12" />
        <span>{{ metric.trend }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch, onMounted } from 'vue'
import TheIcon from '@/components/icon/TheIcon.vue'

const props = defineProps({
  metric: {
    type: Object,
    required: true
  }
})

const animatedValue = ref(0)

// 趋势图标和样式
const trendIcon = computed(() => {
  if (props.metric.trend?.startsWith('+')) {
    return 'carbon:arrow-up'
  } else if (props.metric.trend?.startsWith('-')) {
    return 'carbon:arrow-down'
  }
  return 'carbon:arrow-right'
})

const trendClass = computed(() => {
  if (props.metric.trend?.startsWith('+')) {
    return 'trend-up'
  } else if (props.metric.trend?.startsWith('-')) {
    return 'trend-down'
  }
  return 'trend-neutral'
})

// 数字滚动动画
const animateValue = (start, end, duration = 500) => {
  const startTime = performance.now()
  
  const animate = (currentTime) => {
    const elapsed = currentTime - startTime
    const progress = Math.min(elapsed / duration, 1)
    
    // 使用缓动函数
    const easeOutQuart = 1 - Math.pow(1 - progress, 4)
    const currentValue = Math.round(start + (end - start) * easeOutQuart)
    
    animatedValue.value = currentValue
    
    if (progress < 1) {
      requestAnimationFrame(animate)
    }
  }
  
  requestAnimationFrame(animate)
}

// 监听指标值变化
watch(() => props.metric.value, (newValue) => {
  animateValue(animatedValue.value, newValue)
}, { immediate: true })

onMounted(() => {
  // 初始动画
  setTimeout(() => {
    animateValue(0, props.metric.value)
  }, 100)
})
</script>

<style lang="scss" scoped>
.metric-card {
  background: linear-gradient(135deg, #ffffff 0%, #fafafa 100%);
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: v-bind('metric.color');
    opacity: 0.8;
  }
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    border-color: v-bind('metric.color');
  }
  
  .metric-icon {
    width: 40px;
    height: 40px;
    border-radius: 8px;
    background: v-bind('metric.color + "15"');
    display: flex;
    align-items: center;
    justify-content: center;
    color: v-bind('metric.color');
    flex-shrink: 0;
  }
  
  .metric-content {
    flex: 1;
    min-width: 0;
    
    .metric-value {
      display: flex;
      align-items: baseline;
      gap: 2px;
      margin-bottom: 4px;
      
      .value-number {
        font-size: 20px;
        font-weight: 600;
        color: #262626;
        line-height: 1;
      }
      
      .value-total {
        font-size: 14px;
        color: #8C8C8C;
        font-weight: 400;
      }
      
      .value-unit {
        font-size: 12px;
        color: #8C8C8C;
        font-weight: 400;
      }
    }
    
    .metric-label {
      font-size: 12px;
      color: #8C8C8C;
      margin-bottom: 4px;
      line-height: 1;
    }
    
    .metric-trend {
      display: flex;
      align-items: center;
      gap: 2px;
      font-size: 11px;
      font-weight: 500;
      line-height: 1;
      
      &.trend-up {
        color: #52C41A;
      }
      
      &.trend-down {
        color: #F5222D;
      }
      
      &.trend-neutral {
        color: #8C8C8C;
      }
    }
  }
}

// 特殊样式
.metric-todos {
  .metric-value .value-number {
    color: #FA8C16;
  }
}

.metric-messages {
  .metric-value .value-number {
    color: #1890FF;
  }
}

.metric-completion {
  .metric-value .value-number {
    color: #52C41A;
  }
}

// 响应式设计
@media (max-width: 768px) {
  .metric-card {
    padding: 12px;
    
    .metric-icon {
      width: 32px;
      height: 32px;
    }
    
    .metric-content {
      .metric-value .value-number {
        font-size: 18px;
      }
    }
  }
}
</style>

