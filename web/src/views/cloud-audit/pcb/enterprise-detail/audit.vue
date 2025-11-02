<template>
  <div class="audit-page p-4">
    <n-card title="审核结果总览" class="mb-4">
      <!-- 汇总统计 -->
      <n-card class="mb-4">
        <n-grid :cols="8" :x-gap="12">
          <n-gi>
            <n-statistic label="YⅠ (Ⅰ级指数)" :value="summary.y1 !== undefined ? summary.y1.toFixed(2) : '0.00'">
              <template #suffix>
                <n-tag v-if="summary.y1 >= 85" type="success" size="small" style="margin-left: 8px">达标</n-tag>
                <n-tag v-else type="warning" size="small" style="margin-left: 8px">未达标</n-tag>
              </template>
            </n-statistic>
          </n-gi>
          <n-gi>
            <n-statistic label="YⅡ (Ⅱ级指数)" :value="summary.y2 !== undefined ? summary.y2.toFixed(2) : '0.00'">
              <template #suffix>
                <n-tag v-if="summary.y2 >= 85" type="success" size="small" style="margin-left: 8px">达标</n-tag>
                <n-tag v-else type="warning" size="small" style="margin-left: 8px">未达标</n-tag>
              </template>
            </n-statistic>
          </n-gi>
          <n-gi>
            <n-statistic label="YⅢ (Ⅲ级指数)" :value="summary.y3 !== undefined ? summary.y3.toFixed(2) : '0.00'">
              <template #suffix>
                <n-tag v-if="summary.y3 === 100" type="success" size="small" style="margin-left: 8px">达标</n-tag>
                <n-tag v-else type="warning" size="small" style="margin-left: 8px">未达标</n-tag>
              </template>
            </n-statistic>
          </n-gi>
          <n-gi>
            <n-statistic label="清洁生产水平">
              <n-tag :type="getLevelTagType(summary.overallLevel)" size="large">{{ summary.overallLevel }}</n-tag>
            </n-statistic>
          </n-gi>
        <n-gi><n-statistic label="待改进项数" :value="summary.improvementItems" /></n-gi>
        <n-gi><n-statistic label="限定性指标" :value="summary.limitingIndicators" /></n-gi>
      </n-grid>
      </n-card>
      <!-- 审核进度图表 - 显示YⅠ、YⅡ、YⅢ指数 -->
      <div class="audit-chart">
        <n-grid :cols="3" :x-gap="24" responsive="screen">
          <n-gi>
            <div class="score-circle">
              <n-progress 
                type="circle" 
                :percentage="summary.y1 || 0" 
                :color="getProgressColor(summary.y1 || 0)"
                :size="140"
                :stroke-width="10"
              >
                <div class="score-content">
                  <div class="score-number">{{ (summary.y1 || 0).toFixed(1) }}</div>
                  <div style="font-size: 12px; color: #666;">YⅠ指数</div>
                  <n-tag v-if="summary.y1 >= 85" type="success" size="small" style="margin-top: 4px;">达标</n-tag>
                  <n-tag v-else type="warning" size="small" style="margin-top: 4px;">未达标</n-tag>
                </div>
              </n-progress>
            </div>
          </n-gi>
          <n-gi>
            <div class="score-circle">
              <n-progress 
                type="circle" 
                :percentage="summary.y2 || 0" 
                :color="getProgressColor(summary.y2 || 0)"
                :size="140"
                :stroke-width="10"
              >
                <div class="score-content">
                  <div class="score-number">{{ (summary.y2 || 0).toFixed(1) }}</div>
                  <div style="font-size: 12px; color: #666;">YⅡ指数</div>
                  <n-tag v-if="summary.y2 >= 85" type="success" size="small" style="margin-top: 4px;">达标</n-tag>
                  <n-tag v-else type="warning" size="small" style="margin-top: 4px;">未达标</n-tag>
                </div>
              </n-progress>
            </div>
          </n-gi>
          <n-gi>
            <div class="score-circle">
              <n-progress 
                type="circle" 
                :percentage="summary.y3 || 0" 
                :color="getProgressColor(summary.y3 || 0)"
                :size="140"
                :stroke-width="10"
              >
                <div class="score-content">
                  <div class="score-number">{{ (summary.y3 || 0).toFixed(1) }}</div>
                  <div style="font-size: 12px; color: #666;">YⅢ指数</div>
                  <n-tag v-if="summary.y3 === 100" type="success" size="small" style="margin-top: 4px;">达标</n-tag>
                  <n-tag v-else type="warning" size="small" style="margin-top: 4px;">未达标</n-tag>
                </div>
              </n-progress>
            </div>
          </n-gi>
        </n-grid>
        <div class="chart-legend mt-4">
          <n-space vertical>
          <n-space>
              <n-tag type="success">YⅠ ≥ 85 (Ⅰ级达标)</n-tag>
              <n-tag type="info">YⅡ ≥ 85 (Ⅱ级达标)</n-tag>
              <n-tag type="warning">YⅢ = 100 (Ⅲ级达标)</n-tag>
          </n-space>
            <div style="font-size: 12px; color: #666; margin-top: 8px;">
              判定规则：Ⅰ级需同时满足YⅠ≥85、限定性指标全部Ⅰ级、非限定性指标全部Ⅱ级及以上
            </div>
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
        <n-button type="success" @click="handleSubmitAudit" style="position: relative; z-index: 10;">
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
              :options="getLevelOptions(row.type)"
              placeholder="请选择评级"
              size="small"
              style="width: 100px"
              @update:value="handleIndicatorUpdate(row.id, $event)"
            />
          </template>
          
        </n-data-table>
      </n-card>

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
  NSelect,
  NProgress,
  NInputNumber
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
// 移除推荐方案相关状态
// const showSchemeModal = ref(false)
// const currentSchemes = ref([])

// 产品产量数据
const productOutputData = ref([])

// 审核汇总数据
const summary = ref({
  y1: 0,  // YⅠ指数
  y2: 0,  // YⅡ指数
  y3: 0,  // YⅢ指数
  totalScore: 0,
  overallLevel: '未评估',
  improvementItems: 0,
  limitingIndicators: 0,
  evaluationDetails: null  // 详细判定信息
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
    width: 70,
    align: 'center',
    render: (row) => {
      if (row.isCategory) return row.chineseIndex
      return row.id
    }
  },
  {
    title: '一级指标',
    key: 'primaryIndicator',
    width: 180,
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
    width: 230,
    render: (row) => {
      if (row.isCategory) return ''
      // 二级指标行：只显示二级指标名称
      return row.name
    }
  },
  {
    title: '当前值',
    key: 'currentValue',
    width: 110,
    align: 'center',
    render: (row) => {
      if (row.isCategory) return ''
      
      // 对于定性指标（指标1-6），显示文本形式的当前值
      if (row.type === 'qualitative' && row.id >= 1 && row.id <= 6) {
        return row.currentValue !== null && row.currentValue !== undefined 
          ? row.currentValue 
          : ''
      }
      
      // 对于指标19, 28, 29, 42-45, 46（资源综合利用相关），显示文本形式的当前值
      if ([19, 28, 29, 42, 43, 44, 45, 46].includes(row.id)) {
        return row.currentValue !== null && row.currentValue !== undefined 
          ? row.currentValue 
          : ''
      }
      
      // 对于指标47-49（温室气体排放），显示文本形式的当前值（无论是什么类型）
      if (row.id >= 47 && row.id <= 49) {
        return row.currentValue !== null && row.currentValue !== undefined 
          ? row.currentValue 
          : ''
      }
      
      // 对于指标50-53（产品特征），显示文本形式的当前值
      if (row.id >= 50 && row.id <= 53) {
        return row.currentValue !== null && row.currentValue !== undefined 
          ? row.currentValue 
          : ''
      }
      
      // 对于指标54-64（清洁生产管理），显示文本形式的当前值（无论是什么类型）
      if (row.id >= 54 && row.id <= 64) {
        return row.currentValue !== null && row.currentValue !== undefined 
          ? row.currentValue 
          : ''
      }
      
      // 对于定量指标，如果是数值则显示，否则显示原值
      return row.currentValue !== null && row.currentValue !== undefined 
        ? (typeof row.currentValue === 'number' 
          ? row.currentValue.toFixed(2) 
          : row.currentValue) 
        : ''
    }
  },
  {
    title: '产量(m²)',
    key: 'productionOutput',
    width: 130,
    align: 'center',
    render: (row) => {
      if (row.isCategory) return ''
      
      // 需要用户输入产量的指标ID范围
      const editableIndicatorIds = [
        ...Array.from({ length: 8 }, (_, i) => i + 7),   // 7-14
        ...Array.from({ length: 4 }, (_, i) => i + 15), // 15-18
        ...Array.from({ length: 8 }, (_, i) => i + 20), // 20-27
        ...Array.from({ length: 4 }, (_, i) => i + 30), // 30-33
        ...Array.from({ length: 4 }, (_, i) => i + 34), // 34-37
        ...Array.from({ length: 4 }, (_, i) => i + 38), // 38-41
      ]
      
      const isEditable = editableIndicatorIds.includes(row.id || row.indicator_id)
      
      // 如果是可编辑指标，显示输入框
      if (isEditable) {
        // 获取当前产量值（优先使用用户输入的，否则使用匹配的产品产量）
        const currentOutput = row.userInputOutput !== undefined 
          ? row.userInputOutput 
          : (getIndicatorOutput(row.id, row.name) || 0)
        
        return h(NInputNumber, {
          value: currentOutput,
          'onUpdate:value': (value) => {
            // 更新行数据中的用户输入产量
            row.userInputOutput = value || 0
            // 重新计算动态权重和综合评价指数
            if (row.is_dynamic_weight) {
              // 异步重新计算汇总数据（包含动态权重调整）
              setTimeout(() => {
                calculateSummary().catch(err => console.error('重新计算汇总失败:', err))
              }, 300)  // 防抖处理
            }
          },
          placeholder: '请输入产量',
          min: 0,
          precision: 2,
          size: 'small',
          style: 'width: 120px',
          showButton: false
        })
      } else {
        // 其他指标只显示匹配的产品产量（只读）
        const output = getIndicatorOutput(row.id, row.name)
        return output !== null && output > 0 
          ? output.toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
          : ''
      }
    }
  },
  {
    title: '一级指标权重',
    key: 'categoryWeight',
    width: 110,
    align: 'center',
    render: (row) => {
      if (row.isCategory) {
        // 一级指标行：显示一级指标权重（小数形式）
        const firstChild = row.children && row.children.length > 0 ? row.children[0] : null
        return firstChild && firstChild.category_weight !== undefined 
          ? firstChild.category_weight.toFixed(2)
          : ''
      } else {
        // 二级指标行：显示对应的一级指标权重（小数形式，保留2位）
        return row.category_weight !== undefined 
          ? row.category_weight.toFixed(2)
          : ''
      }
    }
  },
  {
    title: '二级指标权重',
    key: 'weight',
    width: 110,
    align: 'center',
    render: (row) => {
      if (row.isCategory) return ''
      // 如果是动态权重，需要根据产量计算实际权重
      let displayWeight = row.weight !== undefined ? row.weight : 0
      
      // 计算动态权重（如果有产量数据或用户输入）
      if (row.is_dynamic_weight) {
        // 优先使用用户输入的产量，否则使用匹配的产品产量
        const hasUserInput = row.userInputOutput !== undefined && row.userInputOutput !== null
        const hasOutputData = productOutputData.value.length > 0 || hasUserInput
        
        if (hasOutputData) {
          const actualWeight = calculateDynamicWeight(row.id, displayWeight, row.category, productOutputData.value)
          if (actualWeight !== null) {
            displayWeight = actualWeight
          }
        }
      }
      
      // 显示权重（保留2位小数）
      const weightValue = displayWeight.toFixed(2)
      
      // 根据动态权重类型显示不同的标记
      if (row.is_dynamic_weight) {
        // 检查是否是双星号标记（0.1**）
        if (row.id >= 38 && row.id <= 41) {
          return weightValue + '**'
        }
        return weightValue + '*'
      }
      return weightValue
    }
  },
  {
    title: '评级',
    key: 'level',
    width: 100,
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
  }
]

// 评级选项
const levelOptions = [
  { value: 'I级', label: 'I级' },
  { value: 'II级', label: 'II级' },
  { value: 'III级', label: 'III级' },
  { value: '未有该标准', label: '未有该标准' }
]

// 计算属性：检查是否所有指标都已评级（只检查实际的指标项，不包括分类项）
const canSubmit = computed(() => {
  // 遍历所有分类项，检查其下的所有指标项是否都已评级
  return auditTreeData.value.every(category => {
    // 如果是分类项，检查其子项（指标项）
    if (category.isCategory && category.children) {
      return category.children.every(indicator => {
        // 只检查非分类项（实际的指标项）
        return indicator.level && indicator.level !== '待评估'
      })
    }
    // 如果不是分类项（可能是扁平结构），直接检查
    return !category.isCategory ? (category.level && category.level !== '待评估') : true
  })
})

// 获取等级选项
// 所有指标统一使用相同的评级选项：Ⅰ级、Ⅱ级、Ⅲ级、不达标、未有该标准
const getLevelOptions = (type) => {
  // 不再区分limiting类型，所有指标使用统一的评级选项
  return [
    { label: 'I级', value: 'I级' },
    { label: 'II级', value: 'II级' },
    { label: 'III级', value: 'III级' },
    { label: '不达标', value: '不达标' },
    { label: '未有该标准', value: '未有该标准' }
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

// 移除推荐方案相关函数
// // 获取方案选项
// const getSchemeOptions = (schemes) => {
//   if (!schemes || schemes.length === 0) return []
//   return schemes.map(scheme => ({
//     label: scheme.name,
//     value: scheme.id,
//     type: scheme.type,
//     scheme: scheme
//   }))
// }

// // 处理方案选择
// const handleSchemeSelection = async (row, selectedSchemeIds) => {
//   try {
//     // 更新本地数据
//     row.selectedSchemes = selectedSchemeIds
//     
//     // 调用API更新审核结果
//     await api.pcb.audit.updateIndicator(props.enterpriseId, row.id, {
//       level: row.level,
//       selected_scheme_ids: selectedSchemeIds
//     })
//     
//     window.$message.success('方案选择已保存')
//   } catch (error) {
//     console.error('保存方案选择失败:', error)
//     window.$message.error('保存方案选择失败')
//   }
// }

// // 显示方案详情
// const showSchemeDetails = (row) => {
//   currentSchemes.value = row.recommendedSchemes || []
//   showSchemeModal.value = true
// }

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
      
      // 移除推荐方案更新逻辑
      // // 更新推荐方案
      // if (level && level !== 'I级') {
      //   try {
      //     const schemes = await getRecommendedSchemes(indicatorId)
      //     indicator.recommendedSchemes = schemes
      //     console.log(`指标 ${indicatorId} 更新后的推荐方案:`, schemes)
      //   } catch (error) {
      //     console.error(`获取指标 ${indicatorId} 的推荐方案失败:`, error)
      //     indicator.recommendedSchemes = []
      //   }
      // } else {
      //   indicator.recommendedSchemes = []
      //   indicator.selectedSchemes = []
      // }
      
      // 重新计算汇总数据
      await calculateSummary()
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
    
    // 为所有指标自动计算评级
    auditTreeData.value.forEach(category => {
      if (category.children) {
        category.children.forEach(indicator => {
          // 如果已经有评级，跳过
          if (indicator.level) {
            return
          }
          
          // 如果是定量指标且有当前值（数值类型），根据标准值计算评级
          if (indicator.type === 'quantitative' && indicator.currentValue !== null && typeof indicator.currentValue === 'number') {
            indicator.level = calculateQuantitativeLevel(indicator)
            indicator.score = calculateScore(indicator.level)
          }
          // 如果当前值是等级文本，根据最高等级自动评定
          else if (indicator.currentValue && typeof indicator.currentValue === 'string') {
            if (indicator.currentValue.includes('级') || indicator.currentValue === '均不符合' || indicator.currentValue === '不符合') {
              const autoLevel = extractHighestLevelFromCurrentValue(indicator.currentValue)
              if (autoLevel) {
                indicator.level = autoLevel
                indicator.score = calculateScore(autoLevel)
                console.log(`指标${indicator.id}(${indicator.name})自动计算: 当前值="${indicator.currentValue}" => 评级="${autoLevel}", 得分=${indicator.score}`)
              }
            }
          }
        })
      }
    })
    
    await calculateSummary()
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
      calculateSummary().catch(err => console.error('计算汇总失败:', err))
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
    // 移除方案选择收集
    // const selectedSchemes = []
    
    // 收集用户输入的产量数据（用于后端计算动态权重）
    const userInputOutputs = {}
    
    auditTreeData.value.forEach(category => {
      if (category.children) {
        category.children.forEach(indicator => {
          // 如果level还没有设置，但currentValue是等级文本，自动根据最高等级设置
          let finalLevel = indicator.level
          let finalScore = indicator.score
          
          if (!finalLevel && indicator.currentValue && typeof indicator.currentValue === 'string') {
            // 检查是否是等级文本格式（包含"级"字或"均不符合"、"不符合"）
            if (indicator.currentValue.includes('级') || indicator.currentValue === '均不符合' || indicator.currentValue === '不符合') {
              finalLevel = extractHighestLevelFromCurrentValue(indicator.currentValue)
              if (finalLevel) {
                finalScore = calculateScore(finalLevel)
                console.log(`指标${indicator.id}(${indicator.name})提交前自动评定: 当前值="${indicator.currentValue}" => 评级="${finalLevel}", 得分=${finalScore}`)
                // 更新本地数据
                indicator.level = finalLevel
                indicator.score = finalScore
              }
            }
          }
          
          // 确保分数已计算
          if (finalLevel && !finalScore) {
            finalScore = calculateScore(finalLevel)
          }
          
          // 收集指标审核结果（移除方案选择字段）
          indicators.push({
            indicator_id: indicator.id,
            current_value: typeof indicator.currentValue === 'string' ? null : indicator.currentValue,  // 字符串类型不存储到Decimal字段
            level: finalLevel,
            score: finalScore,
            remark: indicator.remark || ''
            // 移除方案选择
            // selected_scheme_ids: indicator.selectedSchemes || []
          })
          
          // 收集用户输入的产量（仅限需要输入产量的指标）
          if (indicator.userInputOutput !== undefined && indicator.userInputOutput !== null) {
            userInputOutputs[indicator.id] = indicator.userInputOutput
          }
          
          // 移除方案选择收集逻辑
          // // 收集选定的方案
          // if (indicator.selectedSchemes && indicator.selectedSchemes.length > 0) {
          //   indicator.selectedSchemes.forEach(schemeId => {
          //     selectedSchemes.push({
          //       indicator_id: indicator.id,
          //       scheme_id: schemeId
          //     })
          //   })
          // }
        })
      }
    })
    
    // 2. 构建提交数据（包含用户输入的产量）
    const auditData = {
      indicators,
      user_input_outputs: userInputOutputs,  // 用户输入的产量数据 {indicator_id: output_value}
      // selected_schemes: selectedSchemes,  // 移除方案选择
      auditor_name: '当前用户', // 从用户信息获取
      audit_date: new Date().toISOString().split('T')[0]
    }
    
    console.log('提交审核数据:', auditData)
    
    // 3. 提交到后端
    const response = await api.pcb.audit.batchUpdate(props.enterpriseId, auditData)
    
    window.$message.success('审核结果提交成功')
    
    // 4. 更新汇总信息（包含综合评价指数）
    if (response.data) {
      summary.value = {
        y1: response.data.y1 !== undefined ? response.data.y1 : 0,
        y2: response.data.y2 !== undefined ? response.data.y2 : 0,
        y3: response.data.y3 !== undefined ? response.data.y3 : 0,
        totalScore: response.data.total_score || response.data.y1 || 0,
        overallLevel: response.data.overall_level || '未评估',
        improvementItems: response.data.improvement_items || 0,
        limitingIndicators: response.data.limiting_indicators || 0,
        evaluationDetails: response.data.evaluation_details || null
      }
      console.log('提交后更新的汇总数据:', summary.value)
    } else {
      // 如果没有返回数据，重新获取汇总数据
      await calculateSummary()
    }
    
    // 6. 重新加载审核数据，确保与数据库同步
    await fetchAuditData()
    
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

// 移除方案类型颜色函数（不再需要）
// // 获取方案类型颜色
// const getSchemeTypeColor = (type) => {
//   const colorMap = {
//     '环保治理': 'success',
//     '技术改造': 'info',
//     '管理改进': 'warning',
//     '节能降耗': 'error',
//     '资源回收': 'default'
//   }
//   return colorMap[type] || 'default'
// }

// 移除推荐方案相关函数
// // 获取推荐方案
// const getRecommendedSchemes = async (indicatorId) => {
//   try {
//     console.log(`正在为指标ID ${indicatorId} 获取推荐方案...`)
//     
//     // 使用真实的API获取推荐方案
//     const response = await api.pcb.scheme.getByEnterpriseIndicator(
//       props.enterpriseId, 
//       indicatorId
//     )
//     
//     const schemes = response.data || []
//     console.log(`指标ID ${indicatorId} 的推荐方案:`, schemes)
//     
//     // 转换数据格式以适配前端组件
//     return schemes.map(scheme => ({
//       value: scheme.id,
//       label: scheme.name,
//       preview: {
//         type: scheme.scheme_type,
//         problemSolved: scheme.problem,
//         description: scheme.description,
//         economicBenefit: scheme.economic_benefit,
//         environmentalBenefit: scheme.environmental_benefit,
//         investment: scheme.investment,
//         paybackPeriod: scheme.payback_period
//       }
//     }))
//   } catch (error) {
//     console.error('获取推荐方案失败:', error)
//     return []
//   }
// }

// // 显示推荐方案
// const showRecommendedSchemes = (schemes) => {
//   currentSchemes.value = schemes
//   showSchemeModal.value = true
// }


// 收集用户输入的产量数据
const collectUserInputOutputs = () => {
  const userInputOutputs = {}
  auditTreeData.value.forEach(category => {
    if (category.children) {
      category.children.forEach(indicator => {
        // 需要用户输入产量的指标ID范围
        const editableIndicatorIds = [
          ...Array.from({ length: 8 }, (_, i) => i + 7),   // 7-14
          ...Array.from({ length: 4 }, (_, i) => i + 15), // 15-18
          ...Array.from({ length: 8 }, (_, i) => i + 20), // 20-27
          ...Array.from({ length: 4 }, (_, i) => i + 30), // 30-33
          ...Array.from({ length: 4 }, (_, i) => i + 34), // 34-37
          ...Array.from({ length: 4 }, (_, i) => i + 38), // 38-41
        ]
        
        if (editableIndicatorIds.includes(indicator.id || indicator.indicator_id)) {
          if (indicator.userInputOutput !== undefined && indicator.userInputOutput !== null) {
            userInputOutputs[indicator.id || indicator.indicator_id] = indicator.userInputOutput
          }
        }
      })
    }
  })
  return userInputOutputs
}

// 计算汇总数据（调用后端API获取综合评价指数）
const calculateSummary = async () => {
  try {
    // 收集用户输入的产量数据
    const userInputOutputs = collectUserInputOutputs()
    
    // 将用户输入的产量数据转换为JSON字符串
    const userInputOutputsStr = Object.keys(userInputOutputs).length > 0 
      ? JSON.stringify(userInputOutputs) 
      : null
    
    // 从后端获取综合评价指数计算结果（传递用户输入的产量）
    const response = await api.pcb.audit.getSummary(
      props.enterpriseId, 
      userInputOutputsStr
    )
    if (response.data) {
      summary.value = {
        y1: response.data.y1 || 0,
        y2: response.data.y2 || 0,
        y3: response.data.y3 || 0,
        totalScore: response.data.total_score || response.data.y1 || 0,
        overallLevel: response.data.overall_level || '未评估',
        improvementItems: response.data.improvement_items || 0,
        limitingIndicators: response.data.limiting_indicators || 0,
        evaluationDetails: response.data.evaluation_details || null
      }
    }
  } catch (error) {
    console.error('获取汇总数据失败:', error)
    // 如果API调用失败，使用简单的本地计算作为后备
    const allIndicators = []
    auditTreeData.value.forEach(category => {
      if (category.children) {
        allIndicators.push(...category.children)
      }
    })
    
    const improvementItems = allIndicators.filter(item => 
      item.level && item.level !== 'I级'
    ).length
    
    const limitingIndicators = allIndicators.filter(item => 
      item.isLimiting || item.type === 'limiting'
    ).length
    
    summary.value = {
      y1: 0,
      y2: 0,
      y3: 0,
      totalScore: 0,
      overallLevel: '未评估',
      improvementItems,
      limitingIndicators,
      evaluationDetails: null
    }
  }
}

// 获取进度条颜色
const getProgressColor = (score) => {
  if (score >= 90) return '#18a058'
  if (score >= 80) return '#2080f0'  
  if (score >= 60) return '#f0a020'
  return '#d03050'
}

// 计算动态权重（根据产量）
const calculateDynamicWeight = (indicatorId, baseWeight, category, productOutputData) => {
  if (!productOutputData || productOutputData.length === 0) {
    return null
  }
  
  // 动态权重分组配置
  // 格式: [指标ID范围, 权重总和, 一级权重]
  const dynamicGroups = [
    [[7, 14], 1.0, 0.1],      // 能源消耗
    [[15, 18], 0.5, 0.1],     // 水资源消耗
    [[20, 27], 1.0, 0.1],     // 原/辅料消耗
    [[30, 33], 0.2, 0.2],     // 废水产生量
    [[34, 37], 0.1, 0.2],     // 废水中铜产生量
    [[38, 41], 0.1, 0.2],     // 废水中COD总产生量
  ]
  
  // 找到当前指标所属的组
  let currentGroup = null
  for (const [[startId, endId], totalWeight, categoryWeight] of dynamicGroups) {
    if (startId <= indicatorId && indicatorId <= endId) {
      currentGroup = { startId, endId, totalWeight, categoryWeight }
      break
    }
  }
  
  if (!currentGroup) {
    return null  // 不是动态权重组
  }
  
  // 获取该组内所有指标的产量
  const groupOutputs = {}
  let groupTotalOutput = 0
  
  // 遍历该组内的所有指标ID，计算总产量
  for (let indId = currentGroup.startId; indId <= currentGroup.endId; indId++) {
    const output = getIndicatorOutput(indId, '')
    if (output && output > 0) {
      groupOutputs[indId] = output
      groupTotalOutput += output
    }
  }
  
  // 如果没有产量数据，返回null（使用原始权重）
  if (groupTotalOutput === 0) {
    return null
  }
  
  // 获取当前指标的产量（优先用户输入）
  let currentOutput = null
  
  // 首先检查用户输入
  auditTreeData.value.forEach(cat => {
    if (cat.children) {
      const indicator = cat.children.find(ind => (ind.id || ind.indicator_id) === indicatorId)
      if (indicator && indicator.userInputOutput !== undefined && indicator.userInputOutput !== null) {
        currentOutput = indicator.userInputOutput
      }
    }
  })
  
  // 如果没有用户输入，从产品数据中获取
  if (currentOutput === null) {
    currentOutput = getIndicatorOutput(indicatorId, '')
  }
  
  if (!currentOutput || currentOutput === 0) {
    return 0  // 如果没有产量，权重为0
  }
  
  // 计算权重占比
  // 例如：单面板产量500，总产量1500，权重总和1.0，一级权重0.1
  // 单面板权重 = (500/1500) * 1.0 * 0.1 = 0.0333...
  const outputRatio = currentOutput / groupTotalOutput
  const actualWeight = outputRatio * currentGroup.totalWeight * currentGroup.categoryWeight
  
  return actualWeight
}

// 根据指标ID和名称获取对应的产品产量（考虑用户输入）
const getIndicatorOutput = (indicatorId, indicatorName) => {
  // 首先检查是否有用户输入
  let userInput = null
  auditTreeData.value.forEach(cat => {
    if (cat.children) {
      const indicator = cat.children.find(ind => (ind.id || ind.indicator_id) === indicatorId)
      if (indicator && indicator.userInputOutput !== undefined && indicator.userInputOutput !== null) {
        userInput = indicator.userInputOutput
      }
    }
  })
  
  // 如果有用户输入，优先使用用户输入
  if (userInput !== null) {
    return userInput
  }
  
  // 否则从产品产量数据中匹配
  if (!productOutputData.value || productOutputData.value.length === 0) {
    return null
  }
  
  // 指标7-14: 能源消耗 - 单位产品电耗
  // 指标15-18: 水资源消耗 - 单位产品新鲜水耗
  // 指标20-27: 原/辅料消耗 - 覆铜板利用率
  // 指标30-33: 污染物产生与排放 - 废水产生量
  // 指标34-37: 污染物产生与排放 - 废水中铜产生量
  // 指标38-41: 污染物产生与排放 - 废水中COD总产生量
  
  // 匹配产品类型的映射
  const indicatorProductMap = {
    // 刚性单面板
    7: { type: 'rigid', mainProduct: '单面板', layers: 1 },
    15: { type: 'rigid', mainProduct: '单面板', layers: 1 },
    20: { type: 'rigid', mainProduct: '单面板', layers: 1 },
    30: { type: 'rigid', mainProduct: '单面板', layers: 1 },
    34: { type: 'rigid', mainProduct: '单面板', layers: 1 },
    38: { type: 'rigid', mainProduct: '单面板', layers: 1 },
    // 刚性双面板
    8: { type: 'rigid', mainProduct: '双面板', layers: 2 },
    16: { type: 'rigid', mainProduct: '双面板', layers: 2 },
    21: { type: 'rigid', mainProduct: '双面板', layers: 2 },
    31: { type: 'rigid', mainProduct: '双面板', layers: 2 },
    35: { type: 'rigid', mainProduct: '双面板', layers: 2 },
    39: { type: 'rigid', mainProduct: '双面板', layers: 2 },
    // 刚性多层板
    9: { type: 'rigid', mainProduct: '多层板', layers: null },
    17: { type: 'rigid', mainProduct: '多层板', layers: null },
    22: { type: 'rigid', mainProduct: '多层板', layers: null },
    32: { type: 'rigid', mainProduct: '多层板', layers: null },
    36: { type: 'rigid', mainProduct: '多层板', layers: null },
    40: { type: 'rigid', mainProduct: '多层板', layers: null },
    // 刚性HDI板
    10: { type: 'rigid', mainProduct: 'HDI板', layers: null },
    18: { type: 'rigid', mainProduct: 'HDI板', layers: null },
    23: { type: 'rigid', mainProduct: 'HDI板', layers: null },
    33: { type: 'rigid', mainProduct: 'HDI板', layers: null },
    37: { type: 'rigid', mainProduct: 'HDI板', layers: null },
    41: { type: 'rigid', mainProduct: 'HDI板', layers: null },
    // 挠性单面板
    11: { type: 'flexible', mainProduct: '单面板', layers: 1 },
    24: { type: 'flexible', mainProduct: '单面板', layers: 1 },
    // 挠性双面板
    12: { type: 'flexible', mainProduct: '双面板', layers: 2 },
    25: { type: 'flexible', mainProduct: '双面板', layers: 2 },
    // 挠性多层板
    13: { type: 'flexible', mainProduct: '多层板', layers: null },
    26: { type: 'flexible', mainProduct: '多层板', layers: null },
    // 挠性HDI板
    14: { type: 'flexible', mainProduct: 'HDI板', layers: null },
    27: { type: 'flexible', mainProduct: 'HDI板', layers: null },
  }
  
  const productInfo = indicatorProductMap[indicatorId]
  if (!productInfo) {
    return null  // 非产量相关指标
  }
  
  // 查找匹配的产品产量数据
  const matchedProduct = productOutputData.value.find(item => {
    if (item.type !== productInfo.type || item.mainProduct !== productInfo.mainProduct) {
      return false
    }
    // 如果指定了层数，需要匹配层数
    if (productInfo.layers !== null && item.layers !== productInfo.layers) {
      return false
    }
    return true
  })
  
  // 计算总产量（所有年份的总和）
  if (matchedProduct) {
    let totalOutput = 0
    // 遍历所有可能的年份字段
    Object.keys(matchedProduct).forEach(key => {
      if (key.startsWith('output_')) {
        const value = Number(matchedProduct[key] || 0)
        if (!isNaN(value)) {
          totalOutput += value
        }
      }
    })
    return totalOutput > 0 ? totalOutput : null
  }
  
  return null
}

// 将level数组转换为可读文本
const formatLevelArrayToText = (levelArray) => {
  if (!levelArray || !Array.isArray(levelArray) || levelArray.length === 0) {
    return ''
  }
  
  // 如果包含"none"，返回"均不符合"
  if (levelArray.includes('none')) {
    return '均不符合'
  }
  
  // 将level1、level2、level3转换为Ⅰ级、Ⅱ级、Ⅲ级
  const levelMap = {
    'level1': 'Ⅰ级',
    'level2': 'Ⅱ级',
    'level3': 'Ⅲ级'
  }
  
  // 按level1、level2、level3的顺序排列
  const sortedLevels = levelArray
    .filter(level => levelMap[level])
    .sort((a, b) => {
      const order = { 'level1': 1, 'level2': 2, 'level3': 3 }
      return (order[a] || 999) - (order[b] || 999)
    })
    .map(level => levelMap[level])
  
  return sortedLevels.join('、')
}

// 从当前值（等级文本）中提取最高等级并自动评定
const extractHighestLevelFromCurrentValue = (currentValue) => {
  if (!currentValue || typeof currentValue !== 'string') {
    return null
  }
  
  // 如果是"均不符合"，返回"不达标"
  if (currentValue === '均不符合') {
    return '不达标'
  }
  
  // 如果是"不符合"，返回"不达标"
  if (currentValue === '不符合') {
    return '不达标'
  }
  
  // 提取最高等级：Ⅰ级 > Ⅱ级 > Ⅲ级
  if (currentValue.includes('Ⅰ级')) {
    return 'I级'
  }
  if (currentValue.includes('Ⅱ级')) {
    return 'II级'
  }
  if (currentValue.includes('Ⅲ级')) {
    return 'III级'
  }
  
  return null
}

// 获取审核数据
const fetchAuditData = async () => {
  try {
    loading.value = true
    
    console.log('开始获取审核数据...')
    
    // 1. 获取所有指标定义
    console.log('获取指标列表...')
    const indicatorsResponse = await api.pcb.indicator.getList()
    const allIndicators = indicatorsResponse.data || []
    console.log(`获取到 ${allIndicators.length} 个指标`)
    
    // 2. 获取企业的审核结果
    console.log('获取审核结果...')
    const resultsResponse = await api.pcb.audit.getResults(props.enterpriseId)
    const auditResults = resultsResponse.data || []
    console.log(`获取到 ${auditResults.length} 个审核结果`)
    
    // 3. 获取预审核的生产工艺与装备要求数据（用于指标1-6的当前值）
    console.log('获取生产工艺与装备要求数据...')
    let processEquipmentData = null
    try {
      const processResponse = await api.pcb.auditOptions.getProcessRequirement(props.enterpriseId)
      processEquipmentData = processResponse.data || null
      console.log('获取到生产工艺与装备要求数据:', processEquipmentData)
    } catch (error) {
      console.warn('获取生产工艺与装备要求数据失败:', error)
      processEquipmentData = null
    }
    
    // 3.1. 获取预审核的清洁生产管理数据（用于指标54-64的当前值）
    console.log('获取清洁生产管理数据...')
    let cleanProductionData = null
    try {
      const cleanProductionResponse = await api.pcb.auditOptions.getCleanProductionManagement(props.enterpriseId)
      cleanProductionData = cleanProductionResponse.data || null
      console.log('获取到清洁生产管理数据:', cleanProductionData)
    } catch (error) {
      console.warn('获取清洁生产管理数据失败:', error)
      cleanProductionData = null
    }
    
    // 3.2. 获取预审核的温室气体排放数据（用于指标47-49的当前值）
    console.log('获取温室气体排放数据...')
    let greenhouseGasData = null
    try {
      const greenhouseGasResponse = await api.pcb.auditOptions.getGreenhouseGasEmission(props.enterpriseId)
      greenhouseGasData = greenhouseGasResponse.data || null
      console.log('获取到温室气体排放数据:', greenhouseGasData)
    } catch (error) {
      console.warn('获取温室气体排放数据失败:', error)
      greenhouseGasData = null
    }
    
    // 3.3. 获取预审核的产品特征数据（用于指标50-53的当前值）
    console.log('获取产品特征数据...')
    let productCharacteristicsData = null
    try {
      const productCharacteristicsResponse = await api.pcb.auditOptions.getProductCharacteristics(props.enterpriseId)
      productCharacteristicsData = productCharacteristicsResponse.data || null
      console.log('获取到产品特征数据:', productCharacteristicsData)
    } catch (error) {
      console.warn('获取产品特征数据失败:', error)
      productCharacteristicsData = null
    }
    
    // 3.4. 获取预审核的资源综合利用数据（用于指标46的当前值）
    console.log('获取资源综合利用数据...')
    let resourceReutilizationData = null
    try {
      const resourceReutilizationResponse = await api.pcb.auditOptions.getResourceReutilization(props.enterpriseId)
      resourceReutilizationData = resourceReutilizationResponse.data || null
      console.log('获取到资源综合利用数据:', resourceReutilizationData)
    } catch (error) {
      console.warn('获取资源综合利用数据失败:', error)
      resourceReutilizationData = null
    }
    
    // 4. 获取企业的产品产量数据（用于动态权重计算）
    console.log('获取产品产量数据...')
    try {
      const productionResponse = await api.pcb.production.getData(props.enterpriseId)
      const productionData = productionResponse.data || {}
      productOutputData.value = productionData.productOutput || []
      console.log(`获取到 ${productOutputData.value.length} 条产品产量数据`)
    } catch (error) {
      console.warn('获取产品产量数据失败:', error)
      productOutputData.value = []
    }
    
    // 4.1. 获取能源消耗数据（用于指标7-14）
    console.log('获取能源消耗数据...')
    let energyConsumptionData = []
    try {
      const energyResponse = await api.pcb.resourceUtilization.getEnergyConsumption(props.enterpriseId)
      energyConsumptionData = energyResponse.data || []
      console.log(`获取到 ${energyConsumptionData.length} 条能源消耗数据:`, energyConsumptionData)
    } catch (error) {
      console.warn('获取能源消耗数据失败:', error)
      energyConsumptionData = []
    }
    
    // 4.2. 获取新鲜水耗数据（用于指标15-18）
    console.log('获取新鲜水耗数据...')
    let freshWaterConsumptionData = []
    try {
      const freshWaterResponse = await api.pcb.resourceUtilization.getFreshWaterConsumption(props.enterpriseId)
      freshWaterConsumptionData = freshWaterResponse.data || []
      console.log(`获取到 ${freshWaterConsumptionData.length} 条新鲜水耗数据:`, freshWaterConsumptionData)
    } catch (error) {
      console.warn('获取新鲜水耗数据失败:', error)
      freshWaterConsumptionData = []
    }
    
    // 4.3. 获取原/辅料消耗（覆铜板）数据（用于指标20-27）
    console.log('获取原/辅料消耗（覆铜板）数据...')
    let rawMaterialConsumptionData = []
    try {
      const rawMaterialResponse = await api.pcb.resourceUtilization.getRawMaterialConsumption(props.enterpriseId)
      rawMaterialConsumptionData = rawMaterialResponse.data || []
      console.log(`获取到 ${rawMaterialConsumptionData.length} 条原/辅料消耗数据:`, rawMaterialConsumptionData)
      
      // 详细检查每条数据的字段
      if (rawMaterialConsumptionData.length > 0) {
        console.log('原/辅料消耗数据字段检查:', rawMaterialConsumptionData.map(item => ({
          id: item.id,
          type: item.type,
          mainProduct: item.mainProduct,
          main_product: item.main_product, // 检查是否有snake_case字段
          layers: item.layers,
          output: item.output,
          cclConsumption: item.cclConsumption,
          cclUtilization: item.cclUtilization,
          所有字段: Object.keys(item)
        })))
      }
    } catch (error) {
      console.error('获取原/辅料消耗数据失败:', error)
      console.error('错误详情:', error.response || error.message)
      rawMaterialConsumptionData = []
    }
    
    // 4.4. 获取废水总量数据（用于指标30-33）
    console.log('获取废水总量数据...')
    let wastewaterTotalConsumptionData = []
    try {
      const wastewaterTotalResponse = await api.pcb.resourceUtilization.getWastewaterTotalConsumption(props.enterpriseId)
      wastewaterTotalConsumptionData = wastewaterTotalResponse.data || []
      console.log(`获取到 ${wastewaterTotalConsumptionData.length} 条废水总量数据:`, wastewaterTotalConsumptionData)
    } catch (error) {
      console.warn('获取废水总量数据失败:', error)
      wastewaterTotalConsumptionData = []
    }
    
    // 4.5. 获取废水中总铜浓度数据（用于指标34-37）
    console.log('获取废水中总铜浓度数据...')
    let wastewaterCuConsumptionData = []
    try {
      const wastewaterCuResponse = await api.pcb.resourceUtilization.getWastewaterCuConsumption(props.enterpriseId)
      wastewaterCuConsumptionData = wastewaterCuResponse.data || []
      console.log(`获取到 ${wastewaterCuConsumptionData.length} 条废水中总铜浓度数据:`, wastewaterCuConsumptionData)
    } catch (error) {
      console.warn('获取废水中总铜浓度数据失败:', error)
      wastewaterCuConsumptionData = []
    }
    
    // 4.6. 获取废水中COD浓度数据（用于指标38-41）
    console.log('获取废水中COD浓度数据...')
    let wastewaterCODConsumptionData = []
    try {
      const wastewaterCODResponse = await api.pcb.resourceUtilization.getWastewaterCODConsumption(props.enterpriseId)
      wastewaterCODConsumptionData = wastewaterCODResponse.data || []
      console.log(`获取到 ${wastewaterCODConsumptionData.length} 条废水中COD浓度数据:`, wastewaterCODConsumptionData)
    } catch (error) {
      console.warn('获取废水中COD浓度数据失败:', error)
      wastewaterCODConsumptionData = []
    }
    
    // 5. 合并指标定义和审核结果
    const mergedData = allIndicators.map(indicator => {
      const result = auditResults.find(r => r.indicator_id === indicator.id)
      
      // 对于指标1-6（生产工艺与装备要求），从预审核数据中读取当前值
      let currentValue = result?.current_value || null
      
      if (indicator.id >= 1 && indicator.id <= 6 && processEquipmentData) {
        // 指标ID到数据库字段的映射
        const fieldMapping = {
          1: 'basicRequirements',        // 基本要求
          2: 'mechanicalFacilities',     // 机械加工及辅助设施
          3: 'printingProcess',          // 线路与阻焊图形形成
          4: 'cleaning',                 // 板面清洗
          5: 'etching',                  // 蚀刻
          6: 'plating'                   // 电镀与化学镀
        }
        
        const fieldName = fieldMapping[indicator.id]
        if (fieldName && processEquipmentData[fieldName]) {
          // 将level数组转换为可读文本
          currentValue = formatLevelArrayToText(processEquipmentData[fieldName])
          console.log(`指标${indicator.id}(${indicator.name})的当前值:`, currentValue)
        }
      }
      
      // 对于指标19, 28, 29, 42-45, 46（资源综合利用相关），从资源综合利用数据中读取当前值
      if (resourceReutilizationData) {
        // 指标ID到数据库字段的映射
        const fieldMapping = {
          19: 'waterReuse',                    // 水资源重复利用率
          28: 'etchingRecovery',               // 金属铜回收率（对应预审核的蚀刻液回收率）
          29: 'generalSolidUtil',              // 一般工业固体废物综合利用率
          42: 'wastewaterCollection',          // 废水收集与处理
          43: 'wasteGasTreatment',             // 废气收集与处理
          44: 'generalSolidCollection',        // 一般固体废物收集与处理
          45: 'hazardousWasteCollection',      // 危险废物收集与处理
          46: 'noise'                          // 噪声
        }
        
        const fieldName = fieldMapping[indicator.id]
        if (fieldName && resourceReutilizationData[fieldName]) {
          // 将level数组转换为可读文本
          currentValue = formatLevelArrayToText(resourceReutilizationData[fieldName])
          console.log(`指标${indicator.id}(${indicator.name})的当前值:`, currentValue)
        }
      }
      
      // 对于指标47-49（温室气体排放），从预审核数据中读取当前值
      if (indicator.id >= 47 && indicator.id <= 49 && greenhouseGasData) {
        // 指标ID到数据库字段的映射
        const fieldMapping = {
          47: 'carbonManagement',        // 碳减排管理
          48: 'emissionPerOutput',       // 单位产值碳排放量
          49: 'emissionIntensity'        // 碳排放强度
        }
        
        const fieldName = fieldMapping[indicator.id]
        if (fieldName && greenhouseGasData[fieldName]) {
          // 将level数组转换为可读文本
          currentValue = formatLevelArrayToText(greenhouseGasData[fieldName])
          console.log(`指标${indicator.id}(${indicator.name})的当前值:`, currentValue)
        }
      }
      
      // 对于指标50-53（产品特征），从预审核数据中读取当前值
      if (indicator.id >= 50 && indicator.id <= 53 && productCharacteristicsData) {
        // 指标ID到数据库字段的映射
        const fieldMapping = {
          50: 'auxiliaryMaterial',        // 使用无毒无害或低毒低害的生产辅助材料
          51: 'packaging',                // 包装
          52: 'hazardousSubstance',      // 有害物质限制使用
          53: 'productPerformance'        // 产品性能
        }
        
        const fieldName = fieldMapping[indicator.id]
        if (fieldName && productCharacteristicsData[fieldName]) {
          // 将level数组转换为可读文本
          currentValue = formatLevelArrayToText(productCharacteristicsData[fieldName])
          console.log(`指标${indicator.id}(${indicator.name})的当前值:`, currentValue)
        }
      }
      
      // 对于指标54-64（清洁生产管理），从预审核数据中读取当前值
      if (indicator.id >= 54 && indicator.id <= 64 && cleanProductionData) {
        // 指标ID到数据库字段的映射
        const fieldMapping = {
          54: 'environmentalLaw',           // 环保法律法规执行情况
          55: 'industrialPolicy',          // 产业政策符合性
          56: 'cleanProductionManagement', // 清洁生产管理
          57: 'cleanProductionAudit',     // 清洁生产审核
          58: 'energyManagement',          // 节能管理
          59: 'emissionMonitoring',        // 污染物排放监测
          60: 'chemicalManagement',        // 危险化学品管理
          61: 'measurementEquipment',      // 计量器具配备情况
          62: 'solidWasteDisposal',        // 固体废物处理处置
          63: 'soilPollutionRisk',         // 土壤污染隐患排查
          64: 'transportMode'              // 运输方式
        }
        
        const fieldName = fieldMapping[indicator.id]
        if (fieldName && cleanProductionData[fieldName]) {
          // 将level数组转换为可读文本
          currentValue = formatLevelArrayToText(cleanProductionData[fieldName])
          console.log(`指标${indicator.id}(${indicator.name})的当前值:`, currentValue)
        }
      }
      
      // 定义变量用于存储产量和匹配的数据
      let userInputOutput = null  // 产量（用于产量列）
      let matchedEnergyData = null
      let matchedFreshWaterData = null
      let matchedRawMaterialData = null
      let matchedWastewaterTotalData = null
      let matchedWastewaterCuData = null
      let matchedWastewaterCODData = null
      
      // 对于指标20-27（原/辅料消耗-覆铜板利用率），从原/辅料消耗表格读取数据
      if (indicator.id >= 20 && indicator.id <= 27 && rawMaterialConsumptionData.length > 0) {
        // 指标ID到产品类型的映射（原/辅料消耗表格使用type和mainProduct字段）
        const indicatorProductMap = {
          20: { type: 'rigid', mainProduct: 'rigid_single', layers: 1 },      // 刚性单面板
          21: { type: 'rigid', mainProduct: 'rigid_double', layers: 2 },      // 刚性双面板
          22: { type: 'rigid', mainProduct: 'rigid_multilayer', layers: null }, // 刚性多层板
          23: { type: 'rigid', mainProduct: 'rigid_hdi', layers: null },       // 刚性HDI板
          24: { type: 'flexible', mainProduct: 'flexible_single', layers: 1 }, // 挠性单面板
          25: { type: 'flexible', mainProduct: 'flexible_double', layers: 2 }, // 挠性双面板
          26: { type: 'flexible', mainProduct: 'flexible_multilayer', layers: null }, // 挠性多层板
          27: { type: 'flexible', mainProduct: 'flexible_hdi', layers: null }  // 挠性HDI板
        }
        
        const productInfo = indicatorProductMap[indicator.id]
        if (productInfo) {
          console.log(`[调试] 指标${indicator.id}(${indicator.name})开始匹配原/辅料消耗数据:`, {
            产品信息: productInfo,
            可用数据总数: rawMaterialConsumptionData.length,
            可用数据: rawMaterialConsumptionData.map(item => ({
              type: item.type,
              mainProduct: item.mainProduct,
              layers: item.layers,
              output: item.output,
              cclUtilization: item.cclUtilization
            }))
          })
          
          // 在原/辅料消耗数据中查找匹配的记录
          // 注意：使用 find() 只返回第一个匹配项，对于多层板和HDI板，可能需要匹配第一条有效数据
          matchedRawMaterialData = rawMaterialConsumptionData.find(item => {
            // 匹配类型和产品名称
            const typeMatch = item.type === productInfo.type
            const productMatch = item.mainProduct === productInfo.mainProduct
            
            if (!typeMatch || !productMatch) {
              // 不输出过多日志，只在调试时使用
              return false
            }
            
            // 如果指定了层数，需要精确匹配层数（单面板和双面板）
            if (productInfo.layers !== null) {
              if (item.layers !== productInfo.layers) {
                return false
              }
            }
            // 对于多层板和HDI板（layers为null），不检查层数，匹配第一条符合条件的记录
            
            // 必须有产量和覆铜板利用率数据
            const hasData = item.output && item.output > 0 && item.cclUtilization !== null && item.cclUtilization !== undefined
            if (!hasData) {
              return false
            }
            
            // 匹配成功，输出日志
            console.log(`[调试] 指标${indicator.id}找到匹配数据:`, {
              匹配的产品: item.mainProduct,
              类型: item.type,
              层数: item.layers,
              产量: item.output,
              利用率: item.cclUtilization
            })
            
            return true
          })
          
          if (matchedRawMaterialData) {
            // 读取产量（用于产量列）
            userInputOutput = matchedRawMaterialData.output || null
            
            // 读取覆铜板利用率（当前值，单位：%）
            // 确保正确读取cclUtilization字段，可能是数字或字符串
            const cclUtilizationValue = matchedRawMaterialData.cclUtilization
            if (cclUtilizationValue !== null && cclUtilizationValue !== undefined && cclUtilizationValue !== '') {
              const parsedValue = typeof cclUtilizationValue === 'string' ? parseFloat(cclUtilizationValue) : cclUtilizationValue
              if (!isNaN(parsedValue)) {
                currentValue = parsedValue
              }
            }
            
            console.log(`指标${indicator.id}(${indicator.name})匹配到原/辅料消耗数据:`, {
              产量: userInputOutput,
              当前值: currentValue,
              原始利用率值: cclUtilizationValue,
              数据类型: typeof cclUtilizationValue,
              评定等级: matchedRawMaterialData.rating,
              匹配到的完整数据: matchedRawMaterialData
            })
          } else {
            console.log(`指标${indicator.id}(${indicator.name})未匹配到原/辅料消耗数据，将设置为"未有该标准"`)
            console.log(`[调试] 指标${indicator.id}未匹配原因检查:`, {
              产品信息: productInfo,
              所有可用数据: rawMaterialConsumptionData.map(item => ({
                type: item.type,
                mainProduct: item.mainProduct,
                layers: item.layers,
                output: item.output,
                cclUtilization: item.cclUtilization
              }))
            })
          }
        }
      }
      
      // 对于指标30-33（废水产生量），从废水总量表格读取数据
      if (indicator.id >= 30 && indicator.id <= 33 && wastewaterTotalConsumptionData.length > 0) {
        // 指标ID到产品类型的映射（废水总量表格使用product字段：single/double/multilayer/hdi）
        const indicatorProductMap = {
          30: { product: 'single', layers: 1 },        // 单面板
          31: { product: 'double', layers: 2 },        // 双面板
          32: { product: 'multilayer', layers: null }, // 多层板
          33: { product: 'hdi', layers: null }          // HDI板
        }
        
        const productInfo = indicatorProductMap[indicator.id]
        if (productInfo) {
          // 在废水总量数据中查找匹配的记录
          matchedWastewaterTotalData = wastewaterTotalConsumptionData.find(item => {
            // 匹配产品类型
            if (item.product !== productInfo.product) {
              return false
            }
            // 如果指定了层数，需要匹配层数
            if (productInfo.layers !== null && item.layers !== productInfo.layers) {
              return false
            }
            // 必须有产量和废水总量数据
            return item.output && item.output > 0 && item.wastewaterTotal && item.wastewaterTotal > 0
          })
          
          if (matchedWastewaterTotalData) {
            // 读取产量（用于产量列）
            userInputOutput = matchedWastewaterTotalData.output || null
            
            // 读取单位产品废水量（当前值 = 废水总量 / 产量）
            if (matchedWastewaterTotalData.wastewaterTotal && matchedWastewaterTotalData.output && matchedWastewaterTotalData.output > 0) {
              const unitWastewater = matchedWastewaterTotalData.wastewaterTotal / matchedWastewaterTotalData.output
              currentValue = parseFloat(unitWastewater.toFixed(4))
            } else if (matchedWastewaterTotalData.unitWastewater) {
              // 如果已经有计算好的单位产品废水量，直接使用
              currentValue = parseFloat(matchedWastewaterTotalData.unitWastewater)
            }
            
            console.log(`指标${indicator.id}(${indicator.name})匹配到废水总量数据:`, {
              产量: userInputOutput,
              当前值: currentValue,
              评定等级: matchedWastewaterTotalData.rating
            })
          } else {
            console.log(`指标${indicator.id}(${indicator.name})未匹配到废水总量数据，将设置为"未有该标准"`)
          }
        }
      }
      
      // 对于指标34-37（废水中铜产生量），从废水中总铜浓度表格读取数据
      if (indicator.id >= 34 && indicator.id <= 37 && wastewaterCuConsumptionData.length > 0) {
        // 指标ID到产品类型的映射（废水中总铜浓度表格使用product字段：single/double/multilayer/hdi）
        const indicatorProductMap = {
          34: { product: 'single', layers: 1 },        // 单面板
          35: { product: 'double', layers: 2 },        // 双面板
          36: { product: 'multilayer', layers: null }, // 多层板
          37: { product: 'hdi', layers: null }          // HDI板
        }
        
        const productInfo = indicatorProductMap[indicator.id]
        if (productInfo) {
          // 在废水中总铜浓度数据中查找匹配的记录
          matchedWastewaterCuData = wastewaterCuConsumptionData.find(item => {
            // 匹配产品类型
            if (item.product !== productInfo.product) {
              return false
            }
            // 如果指定了层数，需要匹配层数
            if (productInfo.layers !== null && item.layers !== productInfo.layers) {
              return false
            }
            // 必须有产量和废水中总铜浓度数据
            return item.output && item.output > 0 && item.wastewaterCu && item.wastewaterCu > 0 && item.wastewaterTotal && item.wastewaterTotal > 0
          })
          
          if (matchedWastewaterCuData) {
            // 读取产量（用于产量列）
            userInputOutput = matchedWastewaterCuData.output || null
            
            // 读取单位产品废水铜产生量（当前值，单位：kg/m²）
            // 注意：表格中单位是g/m²，需要转换为kg/m²（除以1000）
            if (matchedWastewaterCuData.unitWastewaterCu) {
              // 如果已经有计算好的单位产品废水铜产生量（g/m²），转换为kg/m²
              currentValue = parseFloat((matchedWastewaterCuData.unitWastewaterCu / 1000).toFixed(4))
            } else if (matchedWastewaterCuData.wastewaterCu && matchedWastewaterCuData.wastewaterTotal && matchedWastewaterCuData.output && matchedWastewaterCuData.output > 0) {
              // 计算：废水中总铜浓度(g/m³) × 废水总量(m³) / 产量(m²) = g/m²，再转换为kg/m²
              const unitCu = (matchedWastewaterCuData.wastewaterCu * matchedWastewaterCuData.wastewaterTotal) / matchedWastewaterCuData.output / 1000
              currentValue = parseFloat(unitCu.toFixed(4))
            }
            
            console.log(`指标${indicator.id}(${indicator.name})匹配到废水中总铜浓度数据:`, {
              产量: userInputOutput,
              当前值: currentValue,
              评定等级: matchedWastewaterCuData.rating
            })
          } else {
            console.log(`指标${indicator.id}(${indicator.name})未匹配到废水中总铜浓度数据，将设置为"未有该标准"`)
          }
        }
      }
      
      // 对于指标38-41（废水中COD产生量），从废水中COD浓度表格读取数据
      if (indicator.id >= 38 && indicator.id <= 41 && wastewaterCODConsumptionData.length > 0) {
        // 指标ID到产品类型的映射（废水中COD浓度表格使用product字段：single/double/multilayer/hdi）
        const indicatorProductMap = {
          38: { product: 'single', layers: 1 },        // 单面板
          39: { product: 'double', layers: 2 },        // 双面板
          40: { product: 'multilayer', layers: null }, // 多层板
          41: { product: 'hdi', layers: null }          // HDI板
        }
        
        const productInfo = indicatorProductMap[indicator.id]
        if (productInfo) {
          // 在废水中COD浓度数据中查找匹配的记录
          matchedWastewaterCODData = wastewaterCODConsumptionData.find(item => {
            // 匹配产品类型
            if (item.product !== productInfo.product) {
              return false
            }
            // 如果指定了层数，需要匹配层数
            if (productInfo.layers !== null && item.layers !== productInfo.layers) {
              return false
            }
            // 必须有产量和废水中COD浓度数据
            return item.output && item.output > 0 && item.wastewaterCOD && item.wastewaterCOD > 0 && item.wastewaterTotal && item.wastewaterTotal > 0
          })
          
          if (matchedWastewaterCODData) {
            // 读取产量（用于产量列）
            userInputOutput = matchedWastewaterCODData.output || null
            
            // 读取单位产品COD产生量（当前值，单位：kg/m²）
            // 注意：表格中单位是g/m²，需要转换为kg/m²（除以1000）
            if (matchedWastewaterCODData.unitWastewaterCOD) {
              // 如果已经有计算好的单位产品COD产生量（g/m²），转换为kg/m²
              currentValue = parseFloat((matchedWastewaterCODData.unitWastewaterCOD / 1000).toFixed(4))
            } else if (matchedWastewaterCODData.wastewaterCOD && matchedWastewaterCODData.wastewaterTotal && matchedWastewaterCODData.output && matchedWastewaterCODData.output > 0) {
              // 计算：废水中COD浓度(g/m³) × 废水总量(m³) / 产量(m²) = g/m²，再转换为kg/m²
              const unitCOD = (matchedWastewaterCODData.wastewaterCOD * matchedWastewaterCODData.wastewaterTotal) / matchedWastewaterCODData.output / 1000
              currentValue = parseFloat(unitCOD.toFixed(4))
            }
            
            console.log(`指标${indicator.id}(${indicator.name})匹配到废水中COD浓度数据:`, {
              产量: userInputOutput,
              当前值: currentValue,
              评定等级: matchedWastewaterCODData.rating
            })
          } else {
            console.log(`指标${indicator.id}(${indicator.name})未匹配到废水中COD浓度数据，将设置为"未有该标准"`)
          }
        }
      }
      
      // 对于指标15-18（水资源消耗），从新鲜水耗表格读取数据
      if (indicator.id >= 15 && indicator.id <= 18 && freshWaterConsumptionData.length > 0) {
        // 指标ID到产品类型的映射（新鲜水耗表格使用product字段：single/double/multilayer/hdi）
        const indicatorProductMap = {
          15: { product: 'single', layers: 1 },        // 单面板
          16: { product: 'double', layers: 2 },        // 双面板
          17: { product: 'multilayer', layers: null }, // 多层板
          18: { product: 'hdi', layers: null }          // HDI板
        }
        
        const productInfo = indicatorProductMap[indicator.id]
        if (productInfo) {
          // 在新鲜水耗数据中查找匹配的记录
          matchedFreshWaterData = freshWaterConsumptionData.find(item => {
            // 匹配产品类型
            if (item.product !== productInfo.product) {
              return false
            }
            // 如果指定了层数，需要匹配层数（多层板和HDI板可能有多条记录，匹配第一条）
            if (productInfo.layers !== null && item.layers !== productInfo.layers) {
              return false
            }
            // 必须有产量和新鲜水耗数据
            return item.output && item.output > 0 && item.freshWater && item.freshWater > 0
          })
          
          if (matchedFreshWaterData) {
            // 读取产量（用于产量列）
            userInputOutput = matchedFreshWaterData.output || null
            
            // 读取单位产品新鲜水耗（当前值 = 新鲜水耗 / 产量）
            if (matchedFreshWaterData.freshWater && matchedFreshWaterData.output && matchedFreshWaterData.output > 0) {
              const unitFreshWater = matchedFreshWaterData.freshWater / matchedFreshWaterData.output
              currentValue = parseFloat(unitFreshWater.toFixed(4))
            } else if (matchedFreshWaterData.unitFreshWater) {
              // 如果已经有计算好的单位产品新鲜水耗，直接使用
              currentValue = parseFloat(matchedFreshWaterData.unitFreshWater)
            }
            
            console.log(`指标${indicator.id}(${indicator.name})匹配到新鲜水耗数据:`, {
              产量: userInputOutput,
              当前值: currentValue,
              评定等级: matchedFreshWaterData.rating
            })
          } else {
            console.log(`指标${indicator.id}(${indicator.name})未匹配到新鲜水耗数据，将设置为"未有该标准"`)
          }
        }
      }
      
      // 对于指标7-14（能源消耗），从能源消耗表格读取数据
      if (indicator.id >= 7 && indicator.id <= 14 && energyConsumptionData.length > 0) {
        // 指标ID到产品类型的映射
        const indicatorProductMap = {
          7: { type: 'rigid', mainProduct: 'rigid_single', layers: 1 },      // 刚性单面板
          8: { type: 'rigid', mainProduct: 'rigid_double', layers: 2 },      // 刚性双面板
          9: { type: 'rigid', mainProduct: 'rigid_multilayer', layers: null }, // 刚性多层板
          10: { type: 'rigid', mainProduct: 'rigid_hdi', layers: null },       // 刚性HDI板
          11: { type: 'flexible', mainProduct: 'flexible_single', layers: 1 }, // 挠性单面板
          12: { type: 'flexible', mainProduct: 'flexible_double', layers: 2 }, // 挠性双面板
          13: { type: 'flexible', mainProduct: 'flexible_multilayer', layers: null }, // 挠性多层板
          14: { type: 'flexible', mainProduct: 'flexible_hdi', layers: null }  // 挠性HDI板
        }
        
        const productInfo = indicatorProductMap[indicator.id]
        if (productInfo) {
          // 在能源消耗数据中查找匹配的记录
          matchedEnergyData = energyConsumptionData.find(item => {
            // 匹配类型和产品名称
            if (item.type !== productInfo.type || item.mainProduct !== productInfo.mainProduct) {
              return false
            }
            // 如果指定了层数，需要匹配层数（多层板和HDI板可能有多条记录，匹配第一条）
            if (productInfo.layers !== null && item.layers !== productInfo.layers) {
              return false
            }
            // 必须有产量和耗电量数据
            return item.output && item.output > 0 && item.electricity && item.electricity > 0
          })
          
          if (matchedEnergyData) {
            // 读取产量（用于产量列）
            userInputOutput = matchedEnergyData.output || null
            
            // 读取单位产品消耗量（当前值 = 耗电量 / 产量）
            if (matchedEnergyData.electricity && matchedEnergyData.output && matchedEnergyData.output > 0) {
              const unitConsumption = matchedEnergyData.electricity / matchedEnergyData.output
              currentValue = parseFloat(unitConsumption.toFixed(4))
            } else if (matchedEnergyData.unitConsumption) {
              // 如果已经有计算好的单位产品消耗量，直接使用
              currentValue = parseFloat(matchedEnergyData.unitConsumption)
            }
            
            console.log(`指标${indicator.id}(${indicator.name})匹配到能源消耗数据:`, {
              产量: userInputOutput,
              当前值: currentValue,
              评定等级: matchedEnergyData.rating
            })
          } else {
            console.log(`指标${indicator.id}(${indicator.name})未匹配到能源消耗数据，将设置为"未有该标准"`)
          }
        }
      }
      
      // 如果当前值是等级文本，自动根据最高等级进行评定
      let autoLevel = result?.level || null
      
      // 对于指标20-27，如果匹配到原/辅料消耗数据，使用其评定等级
      if (indicator.id >= 20 && indicator.id <= 27) {
        if (matchedRawMaterialData && matchedRawMaterialData.rating) {
          // 将评定等级从预审核格式转换为审核格式
          const ratingMap = {
            'level1': 'I级',
            'level2': 'II级',
            'level3': 'III级',
            'none': '不达标'
          }
          autoLevel = ratingMap[matchedRawMaterialData.rating] || matchedRawMaterialData.rating
          console.log(`指标${indicator.id}(${indicator.name})使用原/辅料消耗数据的评定等级:`, autoLevel)
        } else if (!matchedRawMaterialData) {
          // 如果没有匹配到数据，设置为"未有该标准"
          autoLevel = '未有该标准'
          console.log(`指标${indicator.id}(${indicator.name})未匹配到数据，设置为"未有该标准"`)
        }
      }
      
      // 对于指标30-33，如果匹配到废水总量数据，使用其评定等级
      if (indicator.id >= 30 && indicator.id <= 33) {
        if (matchedWastewaterTotalData && matchedWastewaterTotalData.rating) {
          // 将评定等级从预审核格式转换为审核格式
          const ratingMap = {
            'level1': 'I级',
            'level2': 'II级',
            'level3': 'III级',
            'none': '不达标'
          }
          autoLevel = ratingMap[matchedWastewaterTotalData.rating] || matchedWastewaterTotalData.rating
          console.log(`指标${indicator.id}(${indicator.name})使用废水总量数据的评定等级:`, autoLevel)
        } else if (!matchedWastewaterTotalData) {
          // 如果没有匹配到数据，设置为"未有该标准"
          autoLevel = '未有该标准'
          console.log(`指标${indicator.id}(${indicator.name})未匹配到数据，设置为"未有该标准"`)
        }
      }
      
      // 对于指标34-37，如果匹配到废水中总铜浓度数据，使用其评定等级
      if (indicator.id >= 34 && indicator.id <= 37) {
        if (matchedWastewaterCuData && matchedWastewaterCuData.rating) {
          // 将评定等级从预审核格式转换为审核格式
          const ratingMap = {
            'level1': 'I级',
            'level2': 'II级',
            'level3': 'III级',
            'none': '不达标'
          }
          autoLevel = ratingMap[matchedWastewaterCuData.rating] || matchedWastewaterCuData.rating
          console.log(`指标${indicator.id}(${indicator.name})使用废水中总铜浓度数据的评定等级:`, autoLevel)
        } else if (!matchedWastewaterCuData) {
          // 如果没有匹配到数据，设置为"未有该标准"
          autoLevel = '未有该标准'
          console.log(`指标${indicator.id}(${indicator.name})未匹配到数据，设置为"未有该标准"`)
        }
      }
      
      // 对于指标38-41，如果匹配到废水中COD浓度数据，使用其评定等级
      if (indicator.id >= 38 && indicator.id <= 41) {
        if (matchedWastewaterCODData && matchedWastewaterCODData.rating) {
          // 将评定等级从预审核格式转换为审核格式
          const ratingMap = {
            'level1': 'I级',
            'level2': 'II级',
            'level3': 'III级',
            'none': '不达标'
          }
          autoLevel = ratingMap[matchedWastewaterCODData.rating] || matchedWastewaterCODData.rating
          console.log(`指标${indicator.id}(${indicator.name})使用废水中COD浓度数据的评定等级:`, autoLevel)
        } else if (!matchedWastewaterCODData) {
          // 如果没有匹配到数据，设置为"未有该标准"
          autoLevel = '未有该标准'
          console.log(`指标${indicator.id}(${indicator.name})未匹配到数据，设置为"未有该标准"`)
        }
      }
      
      // 对于指标15-18，如果匹配到新鲜水耗数据，使用其评定等级
      if (indicator.id >= 15 && indicator.id <= 18) {
        if (matchedFreshWaterData && matchedFreshWaterData.rating) {
          // 将评定等级从预审核格式转换为审核格式
          const ratingMap = {
            'level1': 'I级',
            'level2': 'II级',
            'level3': 'III级',
            'none': '不达标'
          }
          autoLevel = ratingMap[matchedFreshWaterData.rating] || matchedFreshWaterData.rating
          console.log(`指标${indicator.id}(${indicator.name})使用新鲜水耗数据的评定等级:`, autoLevel)
        } else if (!matchedFreshWaterData) {
          // 如果没有匹配到数据，设置为"未有该标准"
          autoLevel = '未有该标准'
          console.log(`指标${indicator.id}(${indicator.name})未匹配到数据，设置为"未有该标准"`)
        }
      }
      
      // 对于指标7-14，如果匹配到能源消耗数据，使用其评定等级
      if (indicator.id >= 7 && indicator.id <= 14) {
        if (matchedEnergyData && matchedEnergyData.rating) {
          // 将评定等级从预审核格式转换为审核格式
          const ratingMap = {
            'level1': 'I级',
            'level2': 'II级',
            'level3': 'III级',
            'none': '不达标'
          }
          autoLevel = ratingMap[matchedEnergyData.rating] || matchedEnergyData.rating
          console.log(`指标${indicator.id}(${indicator.name})使用能源消耗数据的评定等级:`, autoLevel)
        } else if (!matchedEnergyData) {
          // 如果没有匹配到数据，设置为"未有该标准"
          autoLevel = '未有该标准'
          console.log(`指标${indicator.id}(${indicator.name})未匹配到数据，设置为"未有该标准"`)
        }
      }
      
      // 如果当前值是等级文本，自动根据最高等级进行评定
      if (!autoLevel && currentValue && typeof currentValue === 'string') {
        // 检查是否是等级文本格式（包含"级"字或"均不符合"、"不符合"）
        if (currentValue.includes('级') || currentValue === '均不符合' || currentValue === '不符合') {
          autoLevel = extractHighestLevelFromCurrentValue(currentValue)
          if (autoLevel) {
            // 自动计算得分
            const autoScore = calculateScore(autoLevel)
            console.log(`指标${indicator.id}(${indicator.name})自动评定: 当前值="${currentValue}" => 评级="${autoLevel}", 得分=${autoScore}`)
          }
        }
      }
      
      // 对于指标20-27，验证数据是否正确赋值
      if (indicator.id >= 20 && indicator.id <= 27) {
        console.log(`[验证] 指标${indicator.id}(${indicator.name})最终数据:`, {
          currentValue: currentValue,
          userInputOutput: userInputOutput,
          level: autoLevel || result?.level || null,
          matchedRawMaterialData: matchedRawMaterialData ? {
            type: matchedRawMaterialData.type,
            mainProduct: matchedRawMaterialData.mainProduct,
            cclUtilization: matchedRawMaterialData.cclUtilization,
            output: matchedRawMaterialData.output
          } : null
        })
      }
      
      return {
        ...indicator,
        currentValue: currentValue,
        level: autoLevel || result?.level || null,
        score: autoLevel && autoLevel !== '未有该标准' ? (result?.score || calculateScore(autoLevel)) : (autoLevel === '未有该标准' ? 0 : (result?.score || 0)),
        remark: result?.comment || result?.remark || '',
        // 从数据库读取一级指标权重和二级指标权重
        category_weight: indicator.category_weight || 0,
        weight: indicator.weight || 0,
        is_dynamic_weight: indicator.is_dynamic_weight || false,
        // 用户输入的产量（指标7-14从能源消耗数据读取，指标15-18从新鲜水耗数据读取，指标20-27从原/辅料消耗数据读取，指标30-41从废水相关数据读取，其他初始值为null）
        userInputOutput: userInputOutput !== null ? userInputOutput : (result?.userInputOutput || null),
        // 移除推荐方案相关字段
        // selectedSchemes: result?.selected_scheme_ids || [],
        // recommendedSchemes: result?.recommended_schemes || []
      }
    })
    
    console.log('合并后的数据:', mergedData.length)
    
    // 4. 构建树形结构（先不加载推荐方案，避免延迟）
    auditTreeData.value = buildTreeData(mergedData)
    // 计算汇总数据（使用新的综合评价指数方法）
    await calculateSummary()
    
    console.log('树形数据构建完成:', auditTreeData.value.length)
    
    // 移除推荐方案异步加载逻辑
    // 5. 异步加载推荐方案（不阻塞界面显示）
    // setTimeout(async () => {
    //   console.log('开始异步加载推荐方案...')
    //   for (const category of auditTreeData.value) {
    //     if (category.children) {
    //       for (const indicator of category.children) {
    //         if (indicator.level && indicator.level !== 'I级') {
    //           try {
    //             const schemes = await getRecommendedSchemes(indicator.id)
    //             indicator.recommendedSchemes = schemes
    //             console.log(`指标${indicator.id}加载了${schemes.length}个推荐方案`)
    //           } catch (error) {
    //             console.error(`获取指标${indicator.id}的推荐方案失败:`, error)
    //             indicator.recommendedSchemes = []
    //           }
    //         }
    //       }
    //     }
    //   }
    //   console.log('推荐方案加载完成')
    // }, 100)
    
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
      // 从数据库读取权重（category_weight 和 weight）
      category_weight: item.category_weight !== undefined ? item.category_weight : 0,
      weight: item.weight !== undefined ? item.weight : 0,
      is_dynamic_weight: item.is_dynamic_weight || false,
      currentValue: item.currentValue || null,
      // 用户输入的产量
      userInputOutput: item.userInputOutput !== undefined ? item.userInputOutput : null,
      // 移除推荐方案相关字段
      // recommendedSchemes: item.recommendedSchemes || [],
      // selectedSchemes: item.selectedSchemes || [],
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

.scheme-selector {
  display: flex;
  align-items: center;
  gap: 8px;
}

.scheme-option {
  padding: 4px 0;
}

.scheme-name {
  font-weight: 500;
  color: #333;
}

.scheme-type {
  font-size: 12px;
  color: #666;
  margin-top: 2px;
}

.scheme-details p {
  margin: 8px 0;
  line-height: 1.5;
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
