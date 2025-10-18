<template>
  <div class="audit-page p-4">
    <n-card title="审核结果总览" class="mb-4">
      <!-- 汇总统计 -->
      <n-grid :cols="4" :x-gap="16" class="mb-4">
        <n-gi><n-statistic label="最终得分" :value="summary.totalScore.toFixed(2)" /></n-gi>
        <n-gi><n-statistic label="综合等级">
          <n-tag :type="getLevelTagType(summary.overallLevel)">{{ summary.overallLevel }}</n-tag>
        </n-statistic></n-gi>
        <n-gi><n-statistic label="待改进项数" :value="summary.improvementItems" /></n-gi>
        <n-gi><n-statistic label="限定性指标" :value="summary.limitingIndicators" /></n-gi>
      </n-grid>
      <!-- 审核进度图表 -->
      <div class="audit-chart">
        <div class="score-circle">
          <n-progress 
            type="circle" 
            :percentage="summary.totalScore" 
            :color="getProgressColor(summary.totalScore)"
            :size="140"
            :stroke-width="10"
          >
            <div class="score-content">
              <div class="score-number">{{ summary.totalScore.toFixed(1) }}分</div>
            </div>
          </n-progress>
        </div>
        <div class="chart-legend mt-4">
          <n-space>
            <n-tag type="success">I级 (≥90分)</n-tag>
            <n-tag type="info">II级 (80-89分)</n-tag>
            <n-tag type="warning">III级 (60-79分)</n-tag>
            <n-tag type="error">不达标 (<60分)</n-tag>
          </n-space>
        </div>
      </div>
    </n-card>

    <!-- 审核操作栏 -->
    <n-card class="mb-4">
      <n-space>
        <n-button type="primary" @click="handleAutoCalculate">
          <template #icon>
            <TheIcon icon="carbon:calculator" />
          </template>
          自动计算评估
        </n-button>
        <n-button @click="handleResetAudit">
          <template #icon>
            <TheIcon icon="carbon:reset" />
          </template>
          重置审核
        </n-button>
        <n-button type="success" @click="handleSubmitAudit" :disabled="!canSubmit">
          <template #icon>
            <TheIcon icon="carbon:checkmark" />
          </template>
          提交审核结果
        </n-button>
      </n-space>
    </n-card>

      <!-- 详细审核表 -->
      <n-card>
        <n-data-table
          :columns="columns"
          :data="auditTreeData"
          :row-key="row => row.key"
          :default-expand-all="true"
          :pagination="false"
          :loading="tableLoading"
          :cascade="false"
        >
          <!-- 序号列 -->
          <template #index="{ row }">
            <span v-if="!row.isCategory">{{ row.id }}</span>
          </template>
          
          <!-- 一级指标列 -->
          <template #primaryIndicator="{ row }">
            <span v-if="row.isCategory">{{ row.name }}</span>
          </template>
          
          <!-- 二级指标列 -->
          <template #secondaryIndicator="{ row }">
            <div v-if="!row.isCategory" class="indicator-name">
              <span v-if="row.isLimiting" class="limiting-indicator">*</span>
              {{ row.name }}
            </div>
          </template>
          
          <!-- 当前值列 -->
          <template #currentValue="{ row }">
            <n-input-number
              v-if="!row.isCategory"
              v-model:value="row.currentValue"
              :min="0"
              :precision="2"
              placeholder="请输入当前值"
              size="small"
              style="width: 120px"
            />
          </template>
          
          <!-- 指标权重列 -->
          <template #weight="{ row }">
            <span v-if="!row.isCategory">{{ row.weight }}%</span>
          </template>
          
          <!-- 评级列 -->
          <template #level="{ row }">
            <n-select
              v-if="!row.isCategory"
              v-model:value="row.level"
              :options="levelOptions"
              placeholder="请选择评级"
              size="small"
              style="width: 100px"
              @update:value="handleIndicatorUpdate(row.id, $event)"
            />
          </template>
          
          <!-- 推荐方案列 -->
          <template #schemes="{ row }">
            <n-select
              v-if="!row.isCategory"
              v-model:value="row.selectedSchemes"
              :options="row.recommendedSchemes"
              placeholder="选择方案"
              size="small"
              style="width: 250px"
              clearable
              multiple
              max-tag-count="2"
            />
          </template>
        </n-data-table>
      </n-card>
    
    <!-- 推荐方案弹窗 -->
    <n-modal v-model:show="showSchemeModal">
      <n-card style="width: 600px" title="推荐改进方案">
        <div v-for="scheme in currentSchemes" :key="scheme.id" class="mb-2">
          <strong>{{ scheme.name }}:</strong> {{ scheme.description }}
        </div>
      </n-card>
    </n-modal>

    <!-- 模块导航按钮 -->
    <div class="module-navigation mt-4">
      <n-space justify="space-between">
        <n-button @click="goToPrevious">
          <template #icon>
            <TheIcon icon="carbon:arrow-left" />
          </template>
          预审核
        </n-button>
        <n-button type="primary" @click="goToNext">
          方案库
          <template #icon>
            <TheIcon icon="carbon:arrow-right" />
          </template>
        </n-button>
      </n-space>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, h } from 'vue'
import { 
  NCard, 
  NDataTable,
  NButton,
  NSpace,
  NGrid,
  NGi,
  NStatistic,
  NTag,
  NModal,
  NSelect,
  NProgress,
  NTooltip
} from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'
// import { mockDetailApi } from '@/mock/pcb-detail'
import api from '@/api'
import QualitativeIndicator from './components/QualitativeIndicator.vue'
import QuantitativeIndicator from './components/QuantitativeIndicator.vue'
import LimitingIndicator from './components/LimitingIndicator.vue'

defineOptions({ name: 'PCB审核' })

const props = defineProps({
  enterpriseId: {
    type: [String, Number],
    required: true
  }
})

const emit = defineEmits(['update', 'navigate'])

// 数据状态
const loading = ref(false)
const tableLoading = ref(false)
const showSchemeModal = ref(false)
const currentSchemes = ref([])

// 审核汇总数据
const summary = ref({
  totalScore: 0,
  overallLevel: '未评估',
  improvementItems: 0,
  limitingIndicators: 0
})

// 审核树数据
const auditTreeData = ref([])

// 64项指标的具体定义 - 严格按照PCB具体内容技术方案.md
const indicators = [
  // 指标1-6: 生产工艺与装备要求（定性判断）
  { id: 1, name: '基本要求', category: '生产工艺与装备要求', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 1.5, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 2, name: '机械加工及辅助设施', category: '生产工艺与装备要求', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 1.5, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 3, name: '线路与阻焊图形形成(印刷或感光工艺)', category: '生产工艺与装备要求', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 1.5, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 4, name: '板面清洗', category: '生产工艺与装备要求', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 1.5, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 5, name: '蚀刻', category: '生产工艺与装备要求', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 1.5, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 6, name: '电镀与化学镀', category: '生产工艺与装备要求', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 1.5, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  
  // 指标7-14: 能源消耗 - 单位产品电耗（定量计算与自动评估）
  { id: 7, name: '刚性印制电路单面板(单位产品电耗)', category: '能源消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kWh/m²', weight: 2.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 8, name: '刚性印制电路双面板(单位产品电耗)', category: '能源消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kWh/m²', weight: 2.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 9, name: '刚性印制电路多层板(2+n)层(单位产品电耗)', category: '能源消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kWh/m²', weight: 2.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 10, name: '刚性印制电路HDI板(2+n)层(单位产品电耗)', category: '能源消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kWh/m²', weight: 2.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 11, name: '挠性印制电路单面板(单位产品电耗)', category: '能源消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kWh/m²', weight: 2.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 12, name: '挠性印制电路双面板(单位产品电耗)', category: '能源消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kWh/m²', weight: 2.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 13, name: '挠性印制电路多层板(2+n)层(单位产品电耗)', category: '能源消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kWh/m²', weight: 2.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 14, name: '挠性印制电路HDI板(2+n)层(单位产品电耗)', category: '能源消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kWh/m²', weight: 2.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  
  // 指标15-19: 水资源消耗（定量计算与自动评估）
  { id: 15, name: '单面板(单位产品新鲜水耗)', category: '水资源消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'm³/m²', weight: 2.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 16, name: '双面板(单位产品新鲜水耗)', category: '水资源消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'm³/m²', weight: 2.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 17, name: '多层板(2+n)层(单位产品新鲜水耗)', category: '水资源消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'm³/m²', weight: 2.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 18, name: 'HDI板(2+n)层(单位产品新鲜水耗)', category: '水资源消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'm³/m²', weight: 2.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 19, name: '水资源重复利用率', category: '水资源消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 2.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  
  // 指标20-27: 原/辅料消耗 - 覆铜板利用率（定量计算与自动评估）
  { id: 20, name: '刚性印制电路单面板 覆铜板利用率', category: '原/辅料消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1.8, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 21, name: '刚性印制电路双面板 覆铜板利用率', category: '原/辅料消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1.8, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 22, name: '刚性印制电路多层板(2+n)层覆铜板利用率', category: '原/辅料消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1.8, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 23, name: '刚性印制电路HDI板(2+n)层覆铜板利用率', category: '原/辅料消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1.8, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 24, name: '挠性印制电路单面板覆铜板利用率', category: '原/辅料消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1.8, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 25, name: '挠性印制电路双面板 覆铜板利用率', category: '原/辅料消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1.8, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 26, name: '挠性性印制电路多层板(2+n)层覆铜板利用率', category: '原/辅料消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1.8, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 27, name: '挠性印制电路HDI板(2+n)层覆铜板利用率', category: '原/辅料消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1.8, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  
  // 指标28-29: 资源综合利用（定量自动评估）
  { id: 28, name: '金属铜回收率', category: '资源综合利用', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1.5, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 29, name: '一般工业固体废物综合利用率', category: '资源综合利用', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1.5, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  
  // 指标30-41: 废水的产生与排放（定量计算与自动评估）
  { id: 30, name: '单面板废水产生量', category: '废水的产生与排放', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'm³/m²', weight: 2.5, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 31, name: '双面板废水产生量', category: '废水的产生与排放', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'm³/m²', weight: 2.5, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 32, name: '多层板(2+n)层废水产生量', category: '废水的产生与排放', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'm³/m²', weight: 2.5, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 33, name: 'HDI板(2+n)层废水产生量', category: '废水的产生与排放', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'm³/m²', weight: 2.5, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 34, name: '单面板废水中铜产生量', category: '废水的产生与排放', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kg/m²', weight: 2.5, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 35, name: '双面板废水中铜产生量', category: '废水的产生与排放', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kg/m²', weight: 2.5, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 36, name: '多层板(2+n)层废水中铜产生量', category: '废水的产生与排放', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kg/m²', weight: 2.5, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 37, name: 'HDI板(2+n)层废水中铜产生量', category: '废水的产生与排放', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kg/m²', weight: 2.5, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 38, name: '单面板废水中COD产生量', category: '废水的产生与排放', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kg/m²', weight: 2.5, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 39, name: '双面板废水废水中COD产生量', category: '废水的产生与排放', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kg/m²', weight: 2.5, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 40, name: '多层板(2+n)层废水中 COD 产生量', category: '废水的产生与排放', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kg/m²', weight: 2.5, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 41, name: 'HDI板(2+n)层废水中 COD 产生量', category: '废水的产生与排放', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kg/m²', weight: 2.5, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  
  // 指标42: 废水的产生与排放 - 定性指标
  { id: 42, name: '废水收集与处理', category: '废水的产生与排放', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 2.5, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  
  // 指标43: 废气的产生与排放（定性判断）
  { id: 43, name: '废气收集与处理', category: '废气的产生与排放', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 2.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  
  // 指标44-45: 固体废物的产生与排放（定性判断）
  { id: 44, name: '一般固体废物收集与处理', category: '固体废物的产生与排放', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 2.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 45, name: '危险废物收集与处理', category: '固体废物的产生与排放', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 2.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  
  // 指标46: 噪声的产生与排放（定性判断）
  { id: 46, name: '噪声', category: '噪声的产生与排放', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 1.5, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  
  // 指标47-49: 温室气体排放（定性/定量混合评估）
  { id: 47, name: '碳减排管理', category: '温室气体排放', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 1.8, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 48, name: '单位产值碳排放量', category: '温室气体排放', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 1.8, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 49, name: '碳排放强度', category: '温室气体排放', type: 'quantitative', level: null, score: 0, isLimiting: false, weight: 1.8, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  
  // 指标50-53: 产品特征（定性判断）
  { id: 50, name: '使用无毒无害或低毒低害的生产辅助材料', category: '产品特征', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 1.5, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 51, name: '包装', category: '产品特征', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 1.5, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 52, name: '有害物质限制使用', category: '产品特征', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 1.5, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 53, name: '产品性能', category: '产品特征', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 1.5, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  
  // 指标54-64: 清洁生产管理（定性/定量/限定性混合评估）
  { id: 54, name: '*环保法律法规执行情况', category: '清洁生产管理', type: 'limiting', level: null, score: 0, isLimiting: true, weight: 2.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 55, name: '*产业政策符合性', category: '清洁生产管理', type: 'limiting', level: null, score: 0, isLimiting: true, weight: 2.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 56, name: '清洁生产管理', category: '清洁生产管理', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 2.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 57, name: '清洁生产审核', category: '清洁生产管理', type: 'quantitative', level: null, score: 0, isLimiting: false, weight: 2.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 58, name: '节能管理', category: '清洁生产管理', type: 'quantitative', level: null, score: 0, isLimiting: false, weight: 2.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 59, name: '污染物排放监测', category: '清洁生产管理', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 2.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 60, name: '*危险化学品管理', category: '清洁生产管理', type: 'limiting', level: null, score: 0, isLimiting: true, weight: 2.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 61, name: '计量器具配备情况', category: '清洁生产管理', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 2.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 62, name: '*固体废物处理处置', category: '清洁生产管理', type: 'limiting', level: null, score: 0, isLimiting: true, weight: 2.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 63, name: '土壤污染隐患排查', category: '清洁生产管理', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 2.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 64, name: '运输方式', category: '清洁生产管理', type: 'quantitative', level: null, score: 0, isLimiting: false, weight: 2.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] }
]

// 表格列定义
const columns = [
  {
    title: '序号',
    key: 'index',
    width: 80,
    align: 'center',
    render: (row) => {
      if (row.isCategory) return row.chineseIndex
      return row.id
    }
  },
  {
    title: '一级指标',
    key: 'primaryIndicator',
    width: 200,
    tree: true,
    render: (row) => {
      if (row.isCategory) {
        // 一级指标行：显示一级指标名称（加粗）
        return h('span', { 
          style: { 
            fontWeight: 'bold',
            fontSize: '14px',
            color: '#262626'
          } 
        }, row.name)
      } else {
        // 二级指标行：显示对应的一级指标名称（不加粗，靠左对齐）
        const parentCategory = auditTreeData.value.find(cat => 
          cat.children && cat.children.some(child => child.id === row.id)
        )
        return parentCategory ? h('span', { 
          style: { 
            textAlign: 'left',
            fontSize: '13px',
            color: '#595959'
          } 
        }, parentCategory.name) : ''
      }
    }
  },
  {
    title: '二级指标',
    key: 'secondaryIndicator',
    width: 250,
    render: (row) => {
      if (row.isCategory) return ''
      // 二级指标行：只显示二级指标名称
      return row.name
    }
  },
  {
    title: '当前值',
    key: 'currentValue',
    width: 120,
    align: 'center',
    render: (row) => {
      if (row.isCategory) return ''
      return row.currentValue || ''
    }
  },
  {
    title: '指标权重',
    key: 'weight',
    width: 100,
    align: 'center',
    render: (row) => {
      if (row.isCategory) return ''
      return row.weight || ''
    }
  },
  {
    title: '评级',
    key: 'level',
    width: 120,
    align: 'center',
    render: (row) => {
      if (row.isCategory) return ''
      return h(NSelect, {
        value: row.level,
        'onUpdate:value': (val) => handleIndicatorUpdate(row.id, val),
        options: getLevelOptions(row.type),
        placeholder: '请选择评级',
        size: 'small',
        style: 'width: 100px'
      })
    }
  },
  {
    title: '推荐方案',
    key: 'schemes',
    width: 250,
    align: 'center',
    render: (row) => {
      if (row.isCategory) return ''
      
      return h(NSelect, {
        value: row.selectedSchemes || [],
        'onUpdate:value': (val) => {
          row.selectedSchemes = val || []
        },
        options: row.recommendedSchemes,
        placeholder: '选择方案',
        size: 'small',
        style: 'width: 250px',
        clearable: true,
        multiple: true,
        maxTagCount: 2,
        renderOption: ({ node, option }) => {
          return h(NTooltip, {
            trigger: 'hover',
            placement: 'right',
            style: 'max-width: 400px;'
          }, {
            trigger: () => h('div', {
              style: 'padding: 8px 12px; cursor: pointer;'
            }, option.label),
            default: () => {
              if (option.preview) {
                return h('div', {
                  class: 'scheme-preview'
                }, [
                  h('div', {
                    class: 'preview-header',
                    style: 'display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid #e0e0e0;'
                  }, [
                    h('h4', {
                      style: 'margin: 0; font-size: 14px; font-weight: 600;'
                    }, option.label),
                    h('n-tag', {
                      type: getSchemeTypeColor(option.preview.type),
                      size: 'small'
                    }, option.preview.type)
                  ]),
                  h('div', {
                    class: 'preview-content'
                  }, [
                    h('p', {
                      style: 'margin: 6px 0; font-size: 12px; line-height: 1.4;'
                    }, [
                      h('strong', {
                        style: 'color: #1890ff; margin-right: 4px;'
                      }, '解决问题：'),
                      option.preview.problemSolved
                    ]),
                    h('p', {
                      style: 'margin: 6px 0; font-size: 12px; line-height: 1.4;'
                    }, [
                      h('strong', {
                        style: 'color: #1890ff; margin-right: 4px;'
                      }, '方案描述：'),
                      option.preview.description
                    ]),
                    h('p', {
                      style: 'margin: 6px 0; font-size: 12px; line-height: 1.4;'
                    }, [
                      h('strong', {
                        style: 'color: #1890ff; margin-right: 4px;'
                      }, '经济效益：'),
                      option.preview.economicBenefit
                    ]),
                    h('p', {
                      style: 'margin: 6px 0; font-size: 12px; line-height: 1.4;'
                    }, [
                      h('strong', {
                        style: 'color: #1890ff; margin-right: 4px;'
                      }, '环境效益：'),
                      option.preview.environmentalBenefit
                    ])
                  ])
                ])
              }
              return '暂无详细信息'
            }
          })
        }
      })
    }
  }
]

// 评级选项
const levelOptions = [
  { value: 'I级', label: 'I级' },
  { value: 'II级', label: 'II级' },
  { value: 'III级', label: 'III级' }
]

// 计算属性
const canSubmit = computed(() => {
  return auditTreeData.value.every(item => item.level && item.level !== '待评估')
})

// 获取等级选项
const getLevelOptions = (type) => {
  if (type === 'limiting') {
    return [
      { label: '符合', value: 'I级' },
      { label: '不符合', value: '不达标' }
    ]
  }
  return [
    { label: 'I级', value: 'I级' },
    { label: 'II级', value: 'II级' },
    { label: 'III级', value: 'III级' },
    { label: '不达标', value: '不达标' }
  ]
}

// 获取指标组件
const getIndicatorComponent = (row) => {
  if (row.type === 'qualitative') {
    return 'QualitativeIndicator'
  } else if (row.type === 'quantitative') {
    return 'QuantitativeIndicator'
  } else if (row.isLimiting) {
    return 'LimitingIndicator'
  }
  return 'div'
}

// 格式化数值
const formatValue = (value, unit) => {
  if (value === null || value === undefined) return '-'
  return `${value.toFixed(2)}${unit || ''}`
}

// 获取等级类型
const getLevelType = (level) => {
  const types = {
    'I级': 'success',
    'II级': 'info', 
    'III级': 'warning',
    '不达标': 'error'
  }
  return types[level] || 'default'
}

// 获取汇总等级标签类型
const getLevelTagType = (level) => {
  return getLevelType(level)
}

// 更新指标等级
const handleIndicatorUpdate = async (indicatorId, level, reason = null) => {
  try {
    // 在树形数据中查找指标
    let indicator = null
    auditTreeData.value.forEach(category => {
      if (category.children) {
        const found = category.children.find(item => item.id === indicatorId)
        if (found) indicator = found
      }
    })
    
    if (indicator) {
      indicator.level = level
      indicator.score = calculateScore(level)
      
      // 如果是限定性指标不达标，显示警告
      if (indicator.isLimiting && level === '不达标') {
        window.$dialog.warning({
          title: '限定性指标警告',
          content: '存在限定性指标不达标，总评级不得高于III级',
          positiveText: '确认'
        })
      }
      
      // 更新推荐方案
      if (level && level !== 'I级') {
        try {
          const schemes = await getRecommendedSchemes(indicatorId)
          indicator.recommendedSchemes = schemes
          console.log(`指标 ${indicatorId} 更新后的推荐方案:`, schemes)
        } catch (error) {
          console.error(`获取指标 ${indicatorId} 的推荐方案失败:`, error)
          indicator.recommendedSchemes = []
        }
      } else {
        indicator.recommendedSchemes = []
        indicator.selectedSchemes = []
      }
      
      // 重新计算汇总数据
      calculateSummary()
    }
  } catch (error) {
    console.error('更新指标等级失败:', error)
    window.$message.error('更新指标等级失败')
  }
}


// 自动计算评估
const handleAutoCalculate = async () => {
  try {
    tableLoading.value = true
    // 模拟自动计算过程
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // 为定量指标自动计算评级
    auditTreeData.value.forEach(indicator => {
      if (indicator.type === 'quantitative' && indicator.currentValue !== null) {
        indicator.level = calculateQuantitativeLevel(indicator)
        indicator.score = calculateScore(indicator.level)
      }
    })
    
    calculateSummary()
    window.$message.success('自动计算完成')
  } catch (error) {
    console.error('自动计算失败:', error)
    window.$message.error('自动计算失败')
  } finally {
    tableLoading.value = false
  }
}

// 重置审核
const handleResetAudit = () => {
  window.$dialog.warning({
    title: '确认重置',
    content: '确定要重置所有审核结果吗？此操作不可撤销。',
    positiveText: '确认',
    negativeText: '取消',
    onPositiveClick: () => {
      auditTreeData.value.forEach(item => {
        item.level = null
        item.score = 0
        item.recommendedSchemes = []
      })
      calculateSummary()
      window.$message.success('审核结果已重置')
    }
  })
}

// 提交审核结果
const handleSubmitAudit = async () => {
  try {
    loading.value = true
    
    // 1. 收集所有指标的审核结果
    const indicators = []
    const selectedSchemes = []
    
    auditTreeData.value.forEach(category => {
      if (category.children) {
        category.children.forEach(indicator => {
          // 收集指标审核结果
          indicators.push({
            indicator_id: indicator.id,
            current_value: indicator.currentValue,
            level: indicator.level,
            score: indicator.score,
            remark: indicator.remark || ''
          })
          
          // 收集选定的方案
          if (indicator.selectedSchemes && indicator.selectedSchemes.length > 0) {
            indicator.selectedSchemes.forEach(schemeId => {
              selectedSchemes.push({
                indicator_id: indicator.id,
                scheme_id: schemeId
              })
            })
          }
        })
      }
    })
    
    // 2. 构建提交数据
    const auditData = {
      indicators,
      selected_schemes: selectedSchemes,
      auditor_name: '当前用户', // 从用户信息获取
      audit_date: new Date().toISOString().split('T')[0]
    }
    
    console.log('提交审核数据:', auditData)
    
    // 3. 提交到后端
    const response = await api.pcb.audit.batchUpdate(props.enterpriseId, auditData)
    
    window.$message.success('审核结果提交成功')
    
    // 4. 更新汇总信息
    if (response.data) {
      summary.value = {
        totalScore: response.data.total_score || 0,
        overallLevel: response.data.overall_level || '未评估',
        improvementItems: response.data.improvement_items || 0,
        limitingIndicators: response.data.limiting_indicators || 0
      }
    }
    
  } catch (error) {
    console.error('提交审核结果失败:', error)
    window.$message.error('提交审核结果失败')
  } finally {
    loading.value = false
  }
}

// 计算定量指标等级
const calculateQuantitativeLevel = (indicator) => {
  // 这里应该根据具体的标准进行计算
  // 暂时使用简单的逻辑
  const value = indicator.currentValue
  if (value <= 50) return 'I级'
  if (value <= 100) return 'II级'
  if (value <= 150) return 'III级'
  return '不达标'
}

// 计算分数
const calculateScore = (level) => {
  const scores = {
    'I级': 100,
    'II级': 80,
    'III级': 60,
    '不达标': 0
  }
  return scores[level] || 0
}

// 获取方案类型颜色
const getSchemeTypeColor = (type) => {
  const colorMap = {
    '环保治理': 'success',
    '技术改造': 'info',
    '管理改进': 'warning',
    '节能降耗': 'error',
    '资源回收': 'default'
  }
  return colorMap[type] || 'default'
}

// 获取推荐方案
const getRecommendedSchemes = async (indicatorId) => {
  try {
    console.log(`正在为指标ID ${indicatorId} 获取推荐方案...`)
    
    // 使用真实的API获取推荐方案
    const response = await api.pcb.scheme.getByEnterpriseIndicator(
      props.enterpriseId, 
      indicatorId
    )
    
    const schemes = response.data || []
    console.log(`指标ID ${indicatorId} 的推荐方案:`, schemes)
    
    // 转换数据格式以适配前端组件
    return schemes.map(scheme => ({
      value: scheme.id,
      label: scheme.name,
      preview: {
        type: scheme.scheme_type,
        problemSolved: scheme.problem,
        description: scheme.description,
        economicBenefit: scheme.economic_benefit,
        environmentalBenefit: scheme.environmental_benefit,
        investment: scheme.investment,
        paybackPeriod: scheme.payback_period
      }
    }))
  } catch (error) {
    console.error('获取推荐方案失败:', error)
    return []
  }
}

// 显示推荐方案
const showRecommendedSchemes = (schemes) => {
  currentSchemes.value = schemes
  showSchemeModal.value = true
}


// 计算汇总数据
const calculateSummary = () => {
  // 收集所有二级指标（非分类节点）
  const allIndicators = []
  auditTreeData.value.forEach(category => {
    if (category.children) {
      allIndicators.push(...category.children)
    }
  })
  
  // 计算加权总分
  let totalWeightedScore = 0
  let totalWeight = 0
  let evaluatedCount = 0
  
  allIndicators.forEach(indicator => {
    if (indicator.level && indicator.score !== undefined) {
      const weight = indicator.weight || 1.0
      totalWeightedScore += indicator.score * weight
      totalWeight += weight
      evaluatedCount++
    }
  })
  
  // 计算加权平均分
  const avgScore = totalWeight > 0 ? totalWeightedScore / totalWeight : 0
  
  let overallLevel = '未评估'
  if (evaluatedCount === 0) {
    overallLevel = '未评估'
  } else if (avgScore >= 90) {
    overallLevel = 'I级'
  } else if (avgScore >= 80) {
    overallLevel = 'II级' 
  } else if (avgScore >= 60) {
    overallLevel = 'III级'
  } else {
    overallLevel = '不达标'
  }
  
  // 检查限定性指标
  const limitingIndicators = allIndicators.filter(item => 
    item.type === 'limiting' && item.level === '不达标'
  ).length
  
  if (limitingIndicators > 0 && overallLevel !== '不达标') {
    overallLevel = 'III级'
  }
  
  const improvementItems = allIndicators.filter(item => 
    item.level && item.level !== 'I级'
  ).length
  
  summary.value = {
    totalScore: avgScore,
    overallLevel,
    improvementItems,
    limitingIndicators
  }
}

// 获取进度条颜色
const getProgressColor = (score) => {
  if (score >= 90) return '#18a058'
  if (score >= 80) return '#2080f0'  
  if (score >= 60) return '#f0a020'
  return '#d03050'
}

// 获取审核数据
const fetchAuditData = async () => {
  try {
    loading.value = true
    
    // 1. 获取所有指标定义
    const indicatorsResponse = await api.pcb.indicator.getList()
    const allIndicators = indicatorsResponse.data || []
    
    // 2. 获取企业的审核结果
    const resultsResponse = await api.pcb.audit.getResults(props.enterpriseId)
    const auditResults = resultsResponse.data || []
    
    // 3. 合并指标定义和审核结果
    const mergedData = allIndicators.map(indicator => {
      const result = auditResults.find(r => r.indicator_id === indicator.id)
      return {
        ...indicator,
        currentValue: result?.current_value || null,
        level: result?.level || null,
        score: result?.score || 0,
        remark: result?.remark || '',
        recommendedSchemes: [],
        selectedSchemes: []
      }
    })
    
    // 4. 为每个指标加载推荐方案
    for (const indicator of mergedData) {
      if (indicator.level && indicator.level !== 'I级') {
        try {
          const schemes = await getRecommendedSchemes(indicator.id)
          indicator.recommendedSchemes = schemes
        } catch (error) {
          console.error(`获取指标${indicator.id}的推荐方案失败:`, error)
          indicator.recommendedSchemes = []
        }
      }
    }
    
    // 5. 构建树形结构
    auditTreeData.value = buildTreeData(mergedData)
    calculateSummary()
  } catch (error) {
    console.error('获取审核数据失败:', error)
    window.$message.error('获取审核数据失败')
    auditTreeData.value = buildTreeData([])
  } finally {
    loading.value = false
  }
}

// 构建树形数据
const buildTreeData = (data) => {
  const treeData = []
  const categoryMap = new Map()
  
  // 定义一级指标编号映射
  const categoryOrder = [
    '生产工艺与装备要求',
    '能源消耗', 
    '水资源消耗',
    '原/辅料消耗',
    '资源综合利用',
    '废水的产生与排放',
    '废气的产生与排放',
    '固体废物的产生与排放',
    '噪声的产生与排放',
    '温室气体排放',
    '产品特征',
    '清洁生产管理'
  ]
  
  // 中文数字映射
  const chineseNumbers = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二']
  
  // 按类别分组
  data.forEach(item => {
    // 确保每个指标都有完整的字段
    const completeItem = {
      ...item,
      weight: item.weight || getDefaultWeight(item.category),
      currentValue: item.currentValue || null,
      recommendedSchemes: item.recommendedSchemes || [],
      selectedSchemes: item.selectedSchemes || [],
      isCategory: false,
      key: `indicator-${item.id}`,
      // 确保字段名匹配
      category: item.category,
      name: item.name,
      type: item.indicator_type || item.type,
      isLimiting: item.is_limiting || item.isLimiting || false
    }
    
    if (!categoryMap.has(item.category)) {
      const categoryIndex = categoryOrder.indexOf(item.category)
      categoryMap.set(item.category, {
        id: `category-${item.category}`,
        key: `category-${item.category}`,
        name: item.category,
        categoryIndex: categoryIndex,
        chineseIndex: chineseNumbers[categoryIndex],
        children: [],
        isCategory: true,
        expanded: true
      })
    }
    categoryMap.get(item.category).children.push(completeItem)
  })
  
  // 按顺序构建树形结构
  categoryOrder.forEach(categoryName => {
    if (categoryMap.has(categoryName)) {
      treeData.push(categoryMap.get(categoryName))
    }
  })
  
  console.log('构建的树形数据:', treeData)
  return treeData
}

// 获取默认权重 - 统一为平均分
const getDefaultWeight = (category) => {
  // 所有指标权重统一为平均分
  return 1.0
}

// 导航方法
const goToPrevious = () => {
  emit('navigate', 'pre-audit')
}

const goToNext = () => {
  emit('navigate', 'scheme-library')
}

onMounted(() => {
  fetchAuditData()
})
</script>

<style scoped>
.audit-page {
  background: #f8f9fa;
}

.audit-chart {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.score-circle {
  position: relative;
}

.score-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.score-number {
  font-size: 28px;
  font-weight: 700;
  color: #262626;
  line-height: 1;
  text-align: center;
}

.chart-legend {
  display: flex;
  justify-content: center;
}

.indicator-name {
  display: flex;
  align-items: center;
}

.limiting-indicator {
  color: #ff4d4f;
  font-weight: bold;
  margin-right: 4px;
}

.text-gray-400 {
  color: #9ca3af;
}

.scheme-content {
  background: var(--n-color-light-hover);
  padding: 12px;
  border-radius: 4px;
  white-space: pre-wrap;
  font-size: 14px;
  line-height: 1.5;
}

.score-text {
  font-weight: 600;
  color: var(--n-color-primary);
}

:deep(.n-statistic) {
  text-align: center;
}

:deep(.n-statistic .n-statistic-value) {
  font-size: 20px;
  font-weight: 600;
}

:deep(.n-statistic .n-statistic-label) {
  font-size: 14px;
  color: var(--n-text-color-secondary);
}
</style>
