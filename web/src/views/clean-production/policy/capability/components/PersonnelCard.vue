<template>
  <n-card class="personnel-card" hoverable @click="handleClick">
    <div class="card-content">
      <div class="avatar-section">
        <n-avatar 
          :src="personnel.avatar" 
          :size="60"
          round
          fallback-src="/default-avatar.png"
        >
          {{ personnel.name.charAt(0) }}
        </n-avatar>
        <div class="status-indicator" :class="{ 'available': personnel.isAvailable, 'unavailable': !personnel.isAvailable }">
          <n-icon size="12">
            <i class="mdi mdi-circle" />
          </n-icon>
        </div>
      </div>
      <div class="info-section">
        <h3 class="name">{{ personnel.name }}</h3>
        <p class="title">{{ personnel.title }}</p>
        <p class="organization">{{ personnel.organization }}</p>
        <p class="department">{{ personnel.department }}</p>
        <div class="specialties">
          <n-tag 
            v-for="specialty in personnel.specialties.slice(0, 3)" 
            :key="specialty"
            size="small"
            type="info"
            class="specialty-tag"
          >
            {{ specialty }}
          </n-tag>
          <span v-if="personnel.specialties.length > 3" class="more-specialties">
            +{{ personnel.specialties.length - 3 }}
          </span>
        </div>
        <div class="contact-info">
          <div class="contact-item" v-if="personnel.phone">
            <n-icon size="14" color="#999">
              <i class="mdi mdi-phone" />
            </n-icon>
            <span class="contact-text">{{ personnel.phone }}</span>
          </div>
          <div class="contact-item" v-if="personnel.email">
            <n-icon size="14" color="#999">
              <i class="mdi mdi-email" />
            </n-icon>
            <span class="contact-text">{{ personnel.email }}</span>
          </div>
        </div>
      </div>
    </div>
    <template #footer>
      <div class="card-footer">
        <n-button 
          type="primary" 
          size="small" 
          @click.stop="handleContact"
          :disabled="!personnel.isAvailable"
        >
          {{ personnel.isAvailable ? '联系' : '暂不可联系' }}
        </n-button>
        <n-button 
          type="info" 
          size="small" 
          @click.stop="handleViewDetail"
        >
          查看详情
        </n-button>
      </div>
    </template>
  </n-card>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  personnel: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['click', 'contact', 'view-detail'])

const handleClick = () => {
  emit('click', props.personnel)
}

const handleContact = () => {
  if (props.personnel.isAvailable) {
    emit('contact', props.personnel)
  }
}

const handleViewDetail = () => {
  emit('view-detail', props.personnel)
}
</script>

<style scoped>
.personnel-card {
  height: 100%;
  transition: all 0.3s ease;
  cursor: pointer;
}

.personnel-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.card-content {
  display: flex;
  gap: 16px;
  padding: 16px 0;
}

.avatar-section {
  position: relative;
  flex-shrink: 0;
}

.status-indicator {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid white;
}

.status-indicator.available {
  color: #18a058;
}

.status-indicator.unavailable {
  color: #d03050;
}

.info-section {
  flex: 1;
  min-width: 0;
}

.name {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0 0 4px 0;
  line-height: 1.2;
}

.title {
  font-size: 14px;
  color: #666;
  margin: 0 0 4px 0;
  font-weight: 500;
}

.organization {
  font-size: 13px;
  color: #999;
  margin: 0 0 2px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.department {
  font-size: 12px;
  color: #999;
  margin: 0 0 12px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.specialties {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-bottom: 12px;
  align-items: center;
}

.specialty-tag {
  font-size: 11px;
  padding: 2px 6px;
}

.more-specialties {
  font-size: 11px;
  color: #999;
  margin-left: 4px;
}

.contact-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #999;
}

.contact-text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  gap: 8px;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
}

:deep(.n-card__content) {
  padding: 16px 20px 12px;
}

:deep(.n-card__footer) {
  padding: 12px 20px 16px;
}
</style>
