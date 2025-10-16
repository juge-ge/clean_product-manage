<template>
  <div 
    class="industry-card" 
    :style="{ '--industry-color': industry.color }"
    @click="$emit('click')"
  >
    <div class="card-header">
      <div class="industry-icon">
        <TheIcon :icon="industry.icon" :size="24" />
      </div>
      <div class="industry-info">
        <h4 class="industry-name">{{ industry.name }}</h4>
        <div class="industry-stats">
          <span class="stat-item">
            <span class="stat-label">企业：</span>
            <span class="stat-value">{{ industry.totalEnterprises }}</span>
          </span>
          <span class="stat-item">
            <span class="stat-label">完成：</span>
            <span class="stat-value completed">{{ industry.completedAudits }}</span>
          </span>
        </div>
      </div>
    </div>
    
    <div class="card-content">
      <div class="progress-section">
        <div class="progress-header">
          <span class="progress-label">审核进度</span>
          <span class="progress-rate">{{ industry.completionRate }}%</span>
        </div>
        <div class="progress-bar">
          <div 
            class="progress-fill" 
            :style="{ 
              width: `${industry.completionRate}%`,
              background: industry.color 
            }"
          ></div>
        </div>
      </div>
      
      <div class="status-breakdown">
        <div class="status-item completed">
          <div class="status-dot"></div>
          <span class="status-label">已完成</span>
          <span class="status-count">{{ industry.completedAudits }}</span>
        </div>
        <div class="status-item in-progress">
          <div class="status-dot"></div>
          <span class="status-label">进行中</span>
          <span class="status-count">{{ industry.inProgressAudits }}</span>
        </div>
        <div class="status-item pending">
          <div class="status-dot"></div>
          <span class="status-label">待开始</span>
          <span class="status-count">{{ industry.pendingAudits }}</span>
        </div>
      </div>
    </div>
    
    <div class="card-footer">
      <div class="view-details">
        <span>查看详情</span>
        <TheIcon icon="carbon:arrow-right" :size="14" />
      </div>
    </div>
  </div>
</template>

<script setup>
import TheIcon from '@/components/icon/TheIcon.vue'

defineProps({
  industry: {
    type: Object,
    required: true
  }
})

defineEmits(['click'])
</script>

<style lang="scss" scoped>
.industry-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 8px 12px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  min-height: 0; // 确保卡片可以收缩
  height: fit-content; // 让卡片高度完全根据内容自适应
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: var(--industry-color);
    transform: scaleX(0);
    transition: transform 0.3s ease;
  }
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    border-color: var(--industry-color);
    
    &::before {
      transform: scaleX(1);
    }
    
    .industry-icon {
      background: var(--industry-color);
      color: white;
      transform: scale(1.05);
    }
    
    .view-details {
      color: var(--industry-color);
      
      .icon {
        transform: translateX(2px);
      }
    }
  }
  
  .card-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 6px;
    
    .industry-icon {
      width: 28px;
      height: 28px;
      border-radius: 6px;
      background: var(--industry-color);
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      transition: all 0.3s ease;
    }
    
    .industry-info {
      flex: 1;
      min-width: 0;
      
      .industry-name {
        font-size: 14px;
        font-weight: 600;
        color: #262626;
        margin: 0 0 4px 0;
        line-height: 1.3;
      }
      
      .industry-stats {
        display: flex;
        gap: 6px;
        
        .stat-item {
          font-size: 11px;
          color: #8C8C8C;
          
          .stat-label {
            margin-right: 1px;
          }
          
          .stat-value {
            font-weight: 600;
            color: #262626;
            
            &.completed {
              color: #52C41A;
            }
          }
        }
      }
    }
  }
  
  .card-content {
    margin-bottom: 4px;
    
    .progress-section {
      margin-bottom: 4px;
      
      .progress-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 4px;
        
        .progress-label {
          font-size: 11px;
          color: #8C8C8C;
        }
        
        .progress-rate {
          font-size: 12px;
          font-weight: 600;
          color: var(--industry-color);
        }
      }
      
      .progress-bar {
        height: 3px;
        background: #f0f0f0;
        border-radius: 2px;
        overflow: hidden;
        
        .progress-fill {
          height: 100%;
          border-radius: 1px;
          transition: width 0.5s ease;
        }
      }
    }
    
    .status-breakdown {
      display: flex;
      flex-direction: column;
      gap: 4px;
      
      .status-item {
        display: flex;
        align-items: center;
        gap: 4px;
        font-size: 10px;
        
        .status-dot {
          width: 2px;
          height: 2px;
          border-radius: 50%;
          flex-shrink: 0;
        }
        
        .status-label {
          color: #8C8C8C;
          flex: 1;
        }
        
        .status-count {
          font-weight: 600;
          color: #262626;
        }
        
        &.completed {
          .status-dot {
            background: #52C41A;
          }
        }
        
        &.in-progress {
          .status-dot {
            background: #1890FF;
          }
        }
        
        &.pending {
          .status-dot {
            background: #FA8C16;
          }
        }
      }
    }
  }
  
  .card-footer {
    .view-details {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 2px;
      font-size: 10px;
      color: #8C8C8C;
      transition: all 0.3s ease;
      
      .icon {
        transition: transform 0.3s ease;
      }
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .industry-card {
    padding: 12px;
    
    .card-header {
      .industry-icon {
        width: 32px;
        height: 32px;
      }
      
      .industry-info {
        .industry-name {
          font-size: 13px;
        }
        
        .industry-stats {
          flex-direction: column;
          gap: 2px;
        }
      }
    }
  }
}
</style>
