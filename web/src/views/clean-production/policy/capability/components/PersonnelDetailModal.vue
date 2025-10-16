<template>
  <n-modal
    :show="show"
    @update:show="$emit('update:show', $event)"
    class="personnel-detail-modal"
    preset="card"
    style="max-width: 1000px"
    :title="personnel?.name"
    size="huge"
  >
    <div class="personnel-header">
      <div class="avatar-section">
        <n-avatar 
          :src="personnel?.avatar" 
          :size="80"
          round
          fallback-src="/default-avatar.png"
        >
          {{ personnel?.name?.charAt(0) }}
        </n-avatar>
        <div class="status-badge" :class="{ 'available': personnel?.isAvailable, 'unavailable': !personnel?.isAvailable }">
          <n-tag :type="personnel?.isAvailable ? 'success' : 'error'" size="small">
            {{ personnel?.isAvailable ? '可联系' : '暂不可联系' }}
          </n-tag>
        </div>
      </div>
      <div class="basic-info">
        <h2 class="name">{{ personnel?.name }}</h2>
        <p class="title">{{ personnel?.title }}</p>
        <p class="organization">{{ personnel?.organization }}</p>
        <p class="department">{{ personnel?.department }}</p>
        <n-tag :type="getTypeTagType(personnel?.type)" size="medium" class="type-tag">
          {{ getTypeLabel(personnel?.type) }}
        </n-tag>
      </div>
    </div>

    <n-divider />

    <div class="personnel-content">
      <n-grid :cols="2" :x-gap="24" :y-gap="16">
        <!-- 联系方式 -->
        <n-gi>
          <n-card title="联系方式" size="small">
            <div class="contact-info">
              <div class="contact-item" v-if="personnel?.phone">
                <n-icon size="16" color="#666">
                  <i class="mdi mdi-phone" />
                </n-icon>
                <span class="contact-label">电话：</span>
                <span class="contact-value">{{ personnel.phone }}</span>
              </div>
              <div class="contact-item" v-if="personnel?.email">
                <n-icon size="16" color="#666">
                  <i class="mdi mdi-email" />
                </n-icon>
                <span class="contact-label">邮箱：</span>
                <span class="contact-value">{{ personnel.email }}</span>
              </div>
            </div>
          </n-card>
        </n-gi>

        <!-- 教育背景 -->
        <n-gi>
          <n-card title="教育背景" size="small">
            <div class="education-info">
              <p class="education-text">{{ personnel?.education }}</p>
            </div>
          </n-card>
        </n-gi>

        <!-- 专业领域 -->
        <n-gi>
          <n-card title="专业领域" size="small">
            <div class="specialties-info">
              <n-tag 
                v-for="specialty in personnel?.specialties" 
                :key="specialty"
                size="medium"
                type="info"
                class="specialty-tag"
              >
                {{ specialty }}
              </n-tag>
            </div>
          </n-card>
        </n-gi>

        <!-- 资质证书 -->
        <n-gi>
          <n-card title="资质证书" size="small">
            <div class="certifications-info">
              <n-tag 
                v-for="cert in personnel?.certifications" 
                :key="cert"
                size="medium"
                type="success"
                class="cert-tag"
              >
                {{ cert }}
              </n-tag>
            </div>
          </n-card>
        </n-gi>
      </n-grid>

      <!-- 工作经历 -->
      <n-card title="工作经历" size="small" class="experience-card">
        <div class="experience-content">
          <p class="experience-text">{{ personnel?.experience }}</p>
        </div>
      </n-card>

      <!-- 主要成就 -->
      <n-card title="主要成就" size="small" class="achievements-card">
        <div class="achievements-content">
          <ul class="achievements-list">
            <li v-for="achievement in personnel?.achievements" :key="achievement" class="achievement-item">
              {{ achievement }}
            </li>
          </ul>
        </div>
      </n-card>

      <!-- 个人简介 -->
      <n-card title="个人简介" size="small" class="introduction-card">
        <div class="introduction-content">
          <p class="introduction-text">{{ personnel?.introduction }}</p>
        </div>
      </n-card>
    </div>

    <template #footer>
      <n-space justify="center">
        <n-button @click="handleClose">关闭</n-button>
        <n-button 
          type="primary" 
          @click="handleContact"
          :disabled="!personnel?.isAvailable"
        >
          {{ personnel?.isAvailable ? '联系' : '暂不可联系' }}
        </n-button>
        <n-button type="info" @click="handleShare">分享</n-button>
      </n-space>
    </template>
  </n-modal>
</template>

<script setup>
import { ref, watch } from 'vue'
import { mockPersonnelApi } from '../data/mockData.js'

const props = defineProps({
  show: {
    type: Boolean,
    required: true
  },
  personnelId: {
    type: [String, Number],
    default: null
  }
})

const emit = defineEmits(['update:show', 'contact'])

const personnel = ref(null)
const loading = ref(false)

const getTypeTagType = (type) => {
  const typeMap = {
    consultant: 'success',
    manager: 'warning'
  }
  return typeMap[type] || 'default'
}

const getTypeLabel = (type) => {
  const labelMap = {
    consultant: '咨询人员',
    manager: '管理人员'
  }
  return labelMap[type] || '未知'
}

// 获取人员详情
const getPersonnelDetail = async (id) => {
  if (!id) return
  
  loading.value = true
  try {
    const response = await mockPersonnelApi.getPersonnelDetail(id)
    personnel.value = response.data
  } catch (error) {
    console.error('获取人员详情失败:', error)
  } finally {
    loading.value = false
  }
}

// 监听ID变化
watch(
  () => props.personnelId,
  (newId) => {
    if (newId) {
      getPersonnelDetail(newId)
    }
  },
  { immediate: true }
)

const handleClose = () => {
  emit('update:show', false)
}

const handleContact = () => {
  if (personnel.value?.isAvailable) {
    emit('contact', personnel.value)
  }
}

const handleShare = () => {
  // 实现分享功能
  console.log('分享人员信息:', personnel.value?.name)
  // 这里可以集成分享到微信、微博等功能
}
</script>

<style scoped>
.personnel-header {
  display: flex;
  gap: 24px;
  align-items: flex-start;
  margin-bottom: 16px;
}

.avatar-section {
  position: relative;
  flex-shrink: 0;
}

.status-badge {
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
}

.basic-info {
  flex: 1;
  min-width: 0;
}

.name {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin: 0 0 8px 0;
  line-height: 1.2;
}

.title {
  font-size: 16px;
  color: #666;
  margin: 0 0 4px 0;
  font-weight: 500;
}

.organization {
  font-size: 14px;
  color: #999;
  margin: 0 0 2px 0;
}

.department {
  font-size: 13px;
  color: #999;
  margin: 0 0 12px 0;
}

.type-tag {
  font-size: 14px;
  padding: 4px 12px;
}

.personnel-content {
  margin: 24px 0;
}

.contact-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.contact-label {
  font-size: 14px;
  color: #666;
  font-weight: 500;
  min-width: 40px;
}

.contact-value {
  font-size: 14px;
  color: #333;
}

.education-info {
  padding: 8px 0;
}

.education-text {
  font-size: 14px;
  color: #333;
  margin: 0;
  line-height: 1.5;
}

.specialties-info {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.specialty-tag {
  font-size: 13px;
  padding: 4px 8px;
}

.certifications-info {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.cert-tag {
  font-size: 13px;
  padding: 4px 8px;
}

.experience-card,
.achievements-card,
.introduction-card {
  margin-top: 16px;
}

.experience-content,
.introduction-content {
  padding: 8px 0;
}

.experience-text,
.introduction-text {
  font-size: 14px;
  color: #333;
  margin: 0;
  line-height: 1.6;
}

.achievements-content {
  padding: 8px 0;
}

.achievements-list {
  margin: 0;
  padding-left: 20px;
}

.achievement-item {
  font-size: 14px;
  color: #333;
  margin-bottom: 8px;
  line-height: 1.5;
}

.achievement-item:last-child {
  margin-bottom: 0;
}

:deep(.n-card-header) {
  text-align: center;
  font-size: 20px;
  font-weight: 500;
  padding: 20px 24px 16px;
}

:deep(.n-card__content) {
  padding: 0 24px 24px;
}

:deep(.n-card__footer) {
  padding: 16px 24px 24px;
}

:deep(.n-card[title]) .n-card-header {
  text-align: left;
  font-size: 16px;
  font-weight: 600;
  padding: 12px 16px 8px;
}

:deep(.n-card[title]) .n-card__content {
  padding: 0 16px 16px;
}
</style>
