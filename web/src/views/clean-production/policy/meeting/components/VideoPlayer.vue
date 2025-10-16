<template>
  <div class="video-player">
    <div class="video-container">
      <video 
        ref="videoRef"
        :src="videoUrl"
        :poster="thumbnail"
        controls
        preload="metadata"
        @play="handlePlay"
        @pause="handlePause"
        @ended="handleEnded"
        @timeupdate="handleTimeUpdate"
        @loadedmetadata="handleLoadedMetadata"
      >
        您的浏览器不支持视频播放
      </video>
      <div class="video-overlay" v-if="!isPlaying && currentTime === 0">
        <div class="play-button" @click="playVideo">
          <n-icon size="48" color="white">
            <i class="mdi mdi-play" />
          </n-icon>
        </div>
      </div>
    </div>
    <div class="video-info">
      <h3 class="video-title">{{ title }}</h3>
      <p class="video-description">{{ description }}</p>
      <div class="video-meta">
        <div class="meta-item">
          <n-icon size="16" color="#999">
            <i class="mdi mdi-clock" />
          </n-icon>
          <span class="duration">{{ formatDuration(duration) }}</span>
        </div>
        <div class="meta-item">
          <n-icon size="16" color="#999">
            <i class="mdi mdi-eye" />
          </n-icon>
          <span class="view-count">{{ viewCount }} 次观看</span>
        </div>
        <div class="meta-item">
          <n-icon size="16" color="#999">
            <i class="mdi mdi-calendar" />
          </n-icon>
          <span class="publish-date">{{ publishDate }}</span>
        </div>
        <div class="meta-item" v-if="category">
          <n-tag size="small" type="info">{{ category }}</n-tag>
        </div>
      </div>
      <div class="video-tags" v-if="tags && tags.length">
        <n-tag 
          v-for="tag in tags" 
          :key="tag"
          size="small"
          type="info"
          class="tag-item"
        >
          {{ tag }}
        </n-tag>
      </div>
      <div class="video-progress" v-if="isPlaying">
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
        </div>
        <div class="time-display">
          <span class="current-time">{{ formatDuration(currentTime) }}</span>
          <span class="total-time">{{ formatDuration(duration) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  videoUrl: {
    type: String,
    required: true
  },
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    default: ''
  },
  thumbnail: {
    type: String,
    default: ''
  },
  duration: {
    type: Number,
    default: 0
  },
  category: {
    type: String,
    default: ''
  },
  tags: {
    type: Array,
    default: () => []
  },
  viewCount: {
    type: Number,
    default: 0
  },
  publishDate: {
    type: String,
    default: ''
  },
  isRecommended: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['play', 'pause', 'ended', 'timeupdate', 'view-count-update'])

const videoRef = ref(null)
const isPlaying = ref(false)
const currentTime = ref(0)
const duration = ref(0)

const progressPercentage = computed(() => {
  if (duration.value === 0) return 0
  return (currentTime.value / duration.value) * 100
})

const formatDuration = (seconds) => {
  if (!seconds || seconds === 0) return '00:00'
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = Math.floor(seconds % 60)
  
  if (hours > 0) {
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }
  return `${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

const playVideo = () => {
  if (videoRef.value) {
    videoRef.value.play()
  }
}

const handlePlay = () => {
  isPlaying.value = true
  emit('play')
}

const handlePause = () => {
  isPlaying.value = false
  emit('pause')
}

const handleEnded = () => {
  isPlaying.value = false
  currentTime.value = 0
  emit('ended')
}

const handleTimeUpdate = () => {
  if (videoRef.value) {
    currentTime.value = videoRef.value.currentTime
    emit('timeupdate', currentTime.value)
  }
}

const handleLoadedMetadata = () => {
  if (videoRef.value) {
    duration.value = videoRef.value.duration
  }
}

// 监听视频播放，更新观看次数
let hasUpdatedViewCount = false
const handleFirstPlay = () => {
  if (!hasUpdatedViewCount) {
    hasUpdatedViewCount = true
    emit('view-count-update')
  }
}

onMounted(() => {
  if (videoRef.value) {
    videoRef.value.addEventListener('play', handleFirstPlay)
  }
})

onUnmounted(() => {
  if (videoRef.value) {
    videoRef.value.removeEventListener('play', handleFirstPlay)
  }
})
</script>

<style scoped>
.video-player {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
}

.video-container {
  position: relative;
  width: 100%;
  background-color: #000;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 16px;
}

.video-container video {
  width: 100%;
  height: auto;
  display: block;
}

.video-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.video-overlay:hover {
  background-color: rgba(0, 0, 0, 0.5);
}

.play-button {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.play-button:hover {
  background-color: rgba(255, 255, 255, 0.3);
  transform: scale(1.1);
}

.video-info {
  padding: 0 8px;
}

.video-title {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin: 0 0 8px 0;
  line-height: 1.3;
}

.video-description {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
  margin: 0 0 12px 0;
}

.video-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  align-items: center;
  margin-bottom: 12px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #999;
}

.duration,
.view-count,
.publish-date {
  font-size: 13px;
}

.video-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 16px;
}

.tag-item {
  font-size: 12px;
  padding: 2px 8px;
}

.video-progress {
  background-color: #f5f5f5;
  border-radius: 4px;
  padding: 8px;
}

.progress-bar {
  width: 100%;
  height: 4px;
  background-color: #e0e0e0;
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-fill {
  height: 100%;
  background-color: var(--primary-color);
  transition: width 0.1s ease;
}

.time-display {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #666;
}

.current-time,
.total-time {
  font-size: 12px;
}

@media (max-width: 768px) {
  .video-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .video-title {
    font-size: 18px;
  }
}
</style>
