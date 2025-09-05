<template>
  <n-modal
    v-model:show="show"
    preset="card"
    title="动态详情"
    style="width: 800px; max-width: 90vw;"
    :bordered="false"
    size="huge"
    role="dialog"
    aria-modal="true"
  >
    <div v-if="dynamicData" class="dynamic-detail">
      <div class="detail-header">
        <h2 class="detail-title">{{ dynamicData.title }}</h2>
        <div class="detail-meta">
          <n-space align="center" size="small">
            <template v-if="dynamicData.province">
              <n-tag size="small" type="success">{{ dynamicData.province }}</n-tag>
            </template>
            <template v-else-if="dynamicData.country">
              <n-tag size="small" type="warning">{{ dynamicData.country }}</n-tag>
            </template>
            <template v-else>
              <n-tag size="small" type="info">{{ dynamicData.source }}</n-tag>
            </template>
            <span class="publish-date">{{ dynamicData.publishDate }}</span>
          </n-space>
        </div>
      </div>
      
      <div class="detail-content">
        <div class="content-section">
          <h3>内容摘要</h3>
          <p class="content-text">
            {{ getContentSummary() }}
          </p>
        </div>
        
        <div class="content-section">
          <h3>相关标签</h3>
          <div class="tags-container">
            <n-tag 
              v-for="tag in getTags()" 
              :key="tag" 
              size="small" 
              type="info"
              class="content-tag"
            >
              {{ tag }}
            </n-tag>
          </div>
        </div>
      </div>
    </div>
    
    <div v-else class="loading-content">
      <n-spin size="large" />
      <p>加载中...</p>
    </div>
    
    <template #footer>
      <div class="modal-footer">
        <n-space justify="end">
          <n-button @click="closeModal">关闭</n-button>
          <n-button type="primary" @click="viewFullContent">查看完整内容</n-button>
        </n-space>
      </div>
    </template>
  </n-modal>
</template>

<script setup>
import { ref, watch, computed } from 'vue'

// Props
const props = defineProps({
  show: {
    type: Boolean,
    required: true
  },
  dynamicId: {
    type: [String, Number],
    default: null
  }
})

// Emits
const emit = defineEmits(['update:show'])

// 响应式数据
const dynamicData = ref(null)
const loading = ref(false)

// 计算属性
const show = computed({
  get: () => props.show,
  set: (value) => emit('update:show', value)
})

// 监听动态ID变化，加载数据
watch(() => props.dynamicId, async (newId) => {
  if (newId && props.show) {
    await loadDynamicData(newId)
  }
}, { immediate: true })

// 监听弹窗显示状态
watch(() => props.show, async (newShow) => {
  if (newShow && props.dynamicId) {
    await loadDynamicData(props.dynamicId)
  } else {
    dynamicData.value = null
  }
})

// 加载动态数据
const loadDynamicData = async (id) => {
  if (!id) return
  
  loading.value = true
  try {
    // 模拟API调用，实际项目中这里会调用真实的API
    await new Promise(resolve => setTimeout(resolve, 500))
    
    // 根据ID生成模拟数据
    dynamicData.value = generateMockDynamicDetail(id)
  } catch (error) {
    console.error('加载动态数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 生成模拟的动态详情数据
const generateMockDynamicDetail = (id) => {
  const idNum = parseInt(id)
  
  if (idNum <= 100) {
    // 国内动态
    return {
      id: idNum,
      title: `工信部发布绿色制造名单，推动产业绿色发展 - ${idNum}`,
      source: '工信部',
      publishDate: '2025-01-15',
      type: 'domestic',
      content: '为深入贯彻落实绿色发展理念，推动制造业绿色化转型，工信部近日发布了2025年度绿色制造名单。本次名单涵盖了钢铁、化工、建材、机械等多个重点行业，共遴选出500家绿色工厂、100个绿色园区和50个绿色供应链管理企业。',
      tags: ['绿色制造', '产业转型', '绿色发展', '工信部']
    }
  } else if (idNum <= 200) {
    // 省内动态
    return {
      id: idNum,
      title: `江苏省启动清洁生产技术改造专项行动 - ${idNum}`,
      province: '江苏省',
      publishDate: '2025-01-14',
      type: 'provincial',
      content: '江苏省工信厅联合省生态环境厅启动清洁生产技术改造专项行动，计划在2025年投入50亿元专项资金，支持1000家企业实施清洁生产技术改造，推动全省工业绿色化水平显著提升。',
      tags: ['清洁生产', '技术改造', '江苏省', '专项行动']
    }
  } else {
    // 国外动态
    return {
      id: idNum,
      title: `欧盟发布新版生态设计指令，助力循环经济发展 - ${idNum}`,
      country: '欧盟',
      publishDate: '2025-01-13',
      type: 'international',
      content: '欧盟委员会发布新版生态设计指令(Ecodesign Directive)，进一步强化产品全生命周期的环境要求，推动循环经济发展。新指令涵盖了更多产品类别，并引入了数字化产品护照等创新机制。',
      tags: ['生态设计', '循环经济', '欧盟', '环境政策']
    }
  }
}

// 获取内容摘要
const getContentSummary = () => {
  if (!dynamicData.value) return ''
  
  const content = dynamicData.value.content || ''
  return content.length > 200 ? content.substring(0, 200) + '...' : content
}

// 获取标签
const getTags = () => {
  return dynamicData.value?.tags || []
}

// 关闭弹窗
const closeModal = () => {
  show.value = false
}

// 查看完整内容
const viewFullContent = () => {
  // 这里可以实现跳转到详情页面的逻辑
  console.log('查看完整内容:', dynamicData.value?.id)
  closeModal()
}
</script>

<style lang="scss" scoped>
.dynamic-detail {
  .detail-header {
    margin-bottom: 24px;
    padding-bottom: 16px;
    border-bottom: 1px solid #e5e5e5;
    
    .detail-title {
      font-size: 20px;
      font-weight: 600;
      color: #333;
      margin: 0 0 16px 0;
      line-height: 1.4;
    }
    
    .detail-meta {
      .publish-date {
        color: #999;
        font-size: 14px;
      }
    }
  }
  
  .detail-content {
    .content-section {
      margin-bottom: 20px;
      
      h3 {
        font-size: 16px;
        font-weight: 600;
        color: #333;
        margin: 0 0 12px 0;
      }
      
      .content-text {
        font-size: 14px;
        line-height: 1.6;
        color: #666;
        margin: 0;
        text-align: justify;
      }
      
      .tags-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        
        .content-tag {
          margin: 0;
        }
      }
    }
  }
}

.loading-content {
  text-align: center;
  padding: 40px 0;
  
  p {
    margin-top: 16px;
    color: #999;
    font-size: 14px;
  }
}

.modal-footer {
  padding-top: 16px;
  border-top: 1px solid #e5e5e5;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .dynamic-detail {
    .detail-header {
      .detail-title {
        font-size: 18px;
      }
    }
    
    .detail-content {
      .content-section {
        h3 {
          font-size: 15px;
        }
        
        .content-text {
          font-size: 13px;
        }
      }
    }
  }
}
</style>


