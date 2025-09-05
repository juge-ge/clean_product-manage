<template>
  <div class="workbench-container">
    <n-card class="welcome-card">
      <div class="welcome-content">
        <div class="user-info">
          <img class="avatar" :src="userStore.avatar || '/default-avatar.png'" alt="user avatar" />
          <div class="greeting">
            <p class="hello">
              {{ $t('views.workbench.text_hello', { username: userStore.name }) }}
            </p>
            <p class="welcome">{{ $t('views.workbench.text_welcome') }}</p>
          </div>
        </div>
        <n-space :size="12" :wrap="false">
          <n-statistic v-for="item in statisticData" :key="item.id" v-bind="item"></n-statistic>
        </n-space>
      </div>
    </n-card>

    <n-card
      :title="$t('views.workbench.label_project')"
      size="small"
      :segmented="true"
      class="project-card"
    >
      <template #header-extra>
        <n-button text type="primary">{{ $t('views.workbench.label_more') }}</n-button>
      </template>
      <div class="project-grid">
        <n-card
          v-for="i in 9"
          :key="i"
          class="project-item"
          title="清洁生产智慧管理平台"
          size="small"
        >
          <p class="project-desc">{{ dummyText }}</p>
        </n-card>
      </div>
    </n-card>
  </div>
</template>

<script setup>
import { useUserStore } from '@/store'
import { useI18n } from 'vue-i18n'

const dummyText = '一个基于清洁生产理念的智慧管理平台，集成环保监控、数据分析、决策支持等功能'
const { t } = useI18n({ useScope: 'global' })

const statisticData = computed(() => [
  {
    id: 0,
    label: t('views.workbench.label_number_of_items'),
    value: '25',
  },
  {
    id: 1,
    label: t('views.workbench.label_upcoming'),
    value: '4/16',
  },
  {
    id: 2,
    label: t('views.workbench.label_information'),
    value: '12',
  },
])

const userStore = useUserStore()
</script>

<style lang="scss" scoped>
.workbench-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.welcome-card {
  border-radius: 10px;
  
  .welcome-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .user-info {
    display: flex;
    align-items: center;

    .avatar {
      width: 60px;
      height: 60px;
      border-radius: 50%;
      object-fit: cover;
    }

    .greeting {
      margin-left: 16px;

      .hello {
        font-size: 20px;
        font-weight: 600;
      }

      .welcome {
        margin-top: 8px;
        font-size: 14px;
        opacity: 0.6;
      }
    }
  }
}

.project-card {
  border-radius: 10px;

  .project-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 16px;
    padding: 8px 0;
  }

  .project-item {
    cursor: pointer;
    transition: all 0.3s ease;
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }

    .project-desc {
      opacity: 0.6;
    }
  }
}

/* 修复浏览器兼容性问题 */
.welcome-card,
.project-card {
  @supports (-webkit-backdrop-filter: blur(10px)) or (backdrop-filter: blur(10px)) {
    -webkit-backdrop-filter: blur(10px);
    backdrop-filter: blur(10px);
  }
}

@media (max-width: 768px) {
  .welcome-content {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }

  .project-grid {
    grid-template-columns: 1fr !important;
  }
}
</style>