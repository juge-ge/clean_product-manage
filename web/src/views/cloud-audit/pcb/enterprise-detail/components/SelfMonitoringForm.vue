<template>
  <div class="self-monitoring-form">
    <n-space vertical :size="16">
      <!-- 有组织废气监测 -->
      <n-card title="有组织废气监测" size="small">
        <n-form :model="formData.organizedGas">
          <n-grid :cols="2" :x-gap="16" :y-gap="12">
            <n-form-item-gi label="监测项目">
              <n-input
                v-model:value="formData.organizedGas.item"
                placeholder="如：VOCs"
              />
            </n-form-item-gi>
            <n-form-item-gi label="浓度（mg/m³）">
              <n-input-number
                v-model:value="formData.organizedGas.concentration"
                :min="0"
                :precision="2"
              />
            </n-form-item-gi>
            <n-form-item-gi label="监测点位">
              <n-input
                v-model:value="formData.organizedGas.point"
                placeholder="如：RTO出口"
              />
            </n-form-item-gi>
            <n-form-item-gi label="执行标准">
              <n-input
                v-model:value="formData.organizedGas.standard"
                placeholder="如：DB32/4041-2021"
              />
            </n-form-item-gi>
            <n-form-item-gi label="监测报告" :span="2">
              <n-upload
                :file-list="organizedGasFiles"
                @update:file-list="handleOrganizedGasUpload"
                @before-upload="beforeUpload"
              >
                <n-button>
                  <template #icon>
                    <TheIcon icon="carbon:document-add" />
                  </template>
                  上传监测报告
                </n-button>
              </n-upload>
            </n-form-item-gi>
          </n-grid>
        </n-form>
      </n-card>

      <!-- 废水监测 -->
      <n-card title="废水监测" size="small">
        <n-form :model="formData.wastewater">
          <n-grid :cols="2" :x-gap="16" :y-gap="12">
            <n-form-item-gi label="监测项目">
              <n-input
                v-model:value="formData.wastewater.item"
                placeholder="如：COD、铜离子"
              />
            </n-form-item-gi>
            <n-form-item-gi label="浓度（mg/L）">
              <n-input-number
                v-model:value="formData.wastewater.concentration"
                :min="0"
                :precision="2"
              />
            </n-form-item-gi>
            <n-form-item-gi label="监测点位">
              <n-input
                v-model:value="formData.wastewater.point"
                placeholder="如：总排口"
              />
            </n-form-item-gi>
            <n-form-item-gi label="执行标准">
              <n-input
                v-model:value="formData.wastewater.standard"
                placeholder="如：GB21900-2008"
              />
            </n-form-item-gi>
            <n-form-item-gi label="监测报告" :span="2">
              <n-upload
                :file-list="wastewaterFiles"
                @update:file-list="handleWastewaterUpload"
                @before-upload="beforeUpload"
              >
                <n-button>
                  <template #icon>
                    <TheIcon icon="carbon:document-add" />
                  </template>
                  上传监测报告
                </n-button>
              </n-upload>
            </n-form-item-gi>
          </n-grid>
        </n-form>
      </n-card>

      <!-- 噪声监测 -->
      <n-card title="噪声监测" size="small">
        <n-form :model="formData.noise">
          <n-grid :cols="2" :x-gap="16" :y-gap="12">
            <n-form-item-gi label="监测项目">
              <n-input
                v-model:value="formData.noise.item"
                placeholder="如：厂界噪声"
              />
            </n-form-item-gi>
            <n-form-item-gi label="声级（dB）">
              <n-input-number
                v-model:value="formData.noise.level"
                :min="0"
                :precision="1"
              />
            </n-form-item-gi>
            <n-form-item-gi label="监测点位">
              <n-input
                v-model:value="formData.noise.point"
                placeholder="如：东厂界"
              />
            </n-form-item-gi>
            <n-form-item-gi label="执行标准">
              <n-input
                v-model:value="formData.noise.standard"
                placeholder="如：GB12348-2008"
              />
            </n-form-item-gi>
            <n-form-item-gi label="监测报告" :span="2">
              <n-upload
                :file-list="noiseFiles"
                @update:file-list="handleNoiseUpload"
                @before-upload="beforeUpload"
              >
                <n-button>
                  <template #icon>
                    <TheIcon icon="carbon:document-add" />
                  </template>
                  上传监测报告
                </n-button>
              </n-upload>
            </n-form-item-gi>
          </n-grid>
        </n-form>
      </n-card>
    </n-space>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { 
  NSpace,
  NCard,
  NForm,
  NFormItemGi,
  NGrid,
  NInput,
  NInputNumber,
  NUpload,
  NButton
} from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      organizedGas: { 
        item: '', 
        concentration: null, 
        point: '', 
        standard: '', 
        reportFileId: '' 
      },
      wastewater: { 
        item: '', 
        concentration: null, 
        point: '', 
        standard: '', 
        reportFileId: '' 
      },
      noise: { 
        item: '', 
        level: null, 
        point: '', 
        standard: '', 
        reportFileId: '' 
      }
    })
  }
})

const emit = defineEmits(['update:modelValue'])

const formData = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// 文件列表
const organizedGasFiles = ref([])
const wastewaterFiles = ref([])
const noiseFiles = ref([])

// 文件上传处理
const beforeUpload = (data) => {
  // 只允许PDF和图片文件
  const allowedTypes = ['application/pdf', 'image/jpeg', 'image/png', 'image/jpg']
  if (!allowedTypes.includes(data.file.file?.type)) {
    window.$message.error('只能上传PDF或图片文件')
    return false
  }
  
  // 限制文件大小为10MB
  if (data.file.file?.size > 10 * 1024 * 1024) {
    window.$message.error('文件大小不能超过10MB')
    return false
  }
  
  return true
}

const handleOrganizedGasUpload = (fileList) => {
  organizedGasFiles.value = fileList
  if (fileList.length > 0) {
    formData.value.organizedGas.reportFileId = fileList[fileList.length - 1].id || 'temp-' + Date.now()
  } else {
    formData.value.organizedGas.reportFileId = ''
  }
}

const handleWastewaterUpload = (fileList) => {
  wastewaterFiles.value = fileList
  if (fileList.length > 0) {
    formData.value.wastewater.reportFileId = fileList[fileList.length - 1].id || 'temp-' + Date.now()
  } else {
    formData.value.wastewater.reportFileId = ''
  }
}

const handleNoiseUpload = (fileList) => {
  noiseFiles.value = fileList
  if (fileList.length > 0) {
    formData.value.noise.reportFileId = fileList[fileList.length - 1].id || 'temp-' + Date.now()
  } else {
    formData.value.noise.reportFileId = ''
  }
}
</script>

<style scoped>
.self-monitoring-form {
  padding: 16px 0;
}
</style>

