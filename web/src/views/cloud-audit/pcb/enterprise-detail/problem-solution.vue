<template>
  <div class="problem-solution-page p-4">
    <n-spin :show="loading">
      <!-- Part 1: 问题清单（来自审核：Ⅱ级及以下） -->
      <n-card class="mb-4" size="small">
        <template #header>
          <div class="card-header">
            <div class="header-left">
              <TheIcon icon="carbon:warning-alt" class="header-icon" />
              <span class="header-title">Ⅱ级清洁生产指标及以下</span>
            </div>
            <n-space>
              <n-input v-model:value="issueSearch" placeholder="搜索一级/二级指标或评级" clearable style="width: 320px" />
            </n-space>
          </div>
        </template>
        <n-data-table
          :columns="issueColumns"
          :data="filteredIssues"
          :pagination="false"
          :bordered="true"
          size="small"
          class="issue-table"
        />
      </n-card>

      <!-- Part 1.5: 权重总和计分排序（计算模块） -->
      <n-card class="mb-4" size="small">
        <template #header>
          <div class="card-header">
            <div class="header-left">
              <TheIcon icon="carbon:table" class="header-icon" />
              <span class="header-title">权重总和计分排序（计算模块）</span>
            </div>
            <n-space>
              <n-button size="small" @click="openAddFactor">新增因素</n-button>
              <n-button size="small" @click="openAddFocus">新增审核重点</n-button>
              <n-button size="small" tertiary @click="resetScore">重置</n-button>
            </n-space>
          </div>
        </template>
        <div class="score-table-wrapper">
          <table class="score-table">
            <thead>
              <tr>
                <th style="width: 160px">因素</th>
                <th style="width: 60px">W</th>
                <th v-for="(f, idx) in focuses" :key="'h-'+idx" class="focus-col">
                  <div class="focus-title">
                    <n-input size="small" v-model:value="f.name" placeholder="审核重点" />
                    <n-button size="tiny" quaternary @click="removeFocus(idx)" v-if="focuses.length>1">移除</n-button>
                  </div>
                  <div class="subhead">R / RW</div>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(factor, rowIdx) in factors" :key="factor.key">
                <td>
                  <div class="cell-flex" style="justify-content:space-between;gap:8px">
                    <span>{{ factor.name }}</span>
                    <n-button size="tiny" quaternary @click="removeFactor(rowIdx)" v-if="factors.length>1">移除</n-button>
                  </div>
                </td>
                <td class="w-cell">{{ factor.w }}</td>
                <td v-for="(f, colIdx) in focuses" :key="'c-'+rowIdx+'-'+colIdx">
                  <div class="cell-flex" v-if="scores[String(f.id)] && scores[String(f.id)][factor.key]">
                    <n-input-number size="tiny" v-model:value="scores[String(f.id)][factor.key].r" :min="0" :max="10" :precision="0" style="width: 70px" @update:value="() => debouncedSaveScoringConfig()" />
                    <n-input-number size="tiny" v-model:value="scores[String(f.id)][factor.key].rw" :min="0" :max="100" :precision="0" style="width: 70px" @update:value="() => debouncedSaveScoringConfig()" />
                  </div>
                  <div v-else>--</div>
                </td>
              </tr>
              <tr class="total-row">
                <td>总分 Σ R*W</td>
                <td></td>
                <td v-for="f in focuses" :key="'t-'+f.id" class="bold">{{ getTotalScore(f.id) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="ranking mt-2">
          <span class="mr-2">排序：</span>
          <n-tag v-for="f in rankedFocuses" :key="'rk-'+f.id" type="info" class="mr-2">{{ f.name }}（{{ getTotalScore(f.id) }}）</n-tag>
        </div>
        <template #footer>
          <div style="text-align: left; padding-top: 12px">
            <n-button type="primary" @click="submitScoringConfig" :loading="savingScoring">提交</n-button>
          </div>
        </template>
      </n-card>

      <!-- Part 2: 无/低费方案库（供审核人员选择） -->
      <n-card class="mb-4" size="small">
        <template #header>
          <div class="card-header">
            <div class="header-left">
              <TheIcon icon="carbon:idea" class="header-icon" />
              <span class="header-title">无/低费方案库</span>
            </div>
            <n-space>
              <n-input v-model:value="lowSearch" placeholder="搜索方案关键词" clearable style="width: 280px" />
              <n-button type="primary" ghost @click="openCreateLow">新建自定义方案</n-button>
              <n-button secondary @click="importFromLibrary('low')">从方案库导入</n-button>
              <n-button secondary @click="linkSelectedSchemes('low')" :disabled="!selectedLowSchemeIds.length">关联到问题</n-button>
            </n-space>
          </div>
        </template>
        <n-data-table
          :columns="lowSchemeColumns"
          :data="filteredLowSchemes"
          :row-key="row => row.id"
          @update:checked-row-keys="(keys) => selectedLowSchemeIds = keys"
          checkable
          size="small"
          :bordered="true"
        />
        <template #footer>
          <div style="text-align: left; padding-top: 12px">
            <n-button type="primary" @click="submitLowCostSchemes" :loading="savingLowSchemes">提交</n-button>
          </div>
        </template>
      </n-card>

      <!-- Part 3: 中高费方案库（可选择或自定义编辑） -->
      <n-card class="mb-2" size="small">
        <template #header>
          <div class="card-header">
            <div class="header-left">
              <TheIcon icon="carbon:currency" class="header-icon" />
              <span class="header-title">中高费方案库</span>
            </div>
            <n-space>
              <n-input v-model:value="mhSearch" placeholder="搜索方案关键词" clearable style="width: 280px" />
              <n-button type="primary" ghost @click="openCreateMedium">新建自定义方案</n-button>
              <n-button secondary @click="importFromLibrary('mh')">从方案库导入</n-button>
              <n-button secondary @click="linkSelectedSchemes('mh')" :disabled="!selectedMhSchemeIds.length">关联到问题</n-button>
            </n-space>
          </div>
        </template>
        <n-data-table
          :columns="mhSchemeColumns"
          :data="filteredMhSchemes"
          :row-key="row => row.id"
          checkable
          @update:checked-row-keys="(keys) => selectedMhSchemeIds = keys"
          size="small"
          :bordered="true"
        />
        <template #footer>
          <div style="text-align: left; padding-top: 12px">
            <n-button type="primary" @click="submitMediumHighCostSchemes" :loading="savingMhSchemes">提交</n-button>
          </div>
        </template>
      </n-card>

      <n-space justify="center" class="mt-4">
        <n-button @click="emit('navigate', 'audit')">返回审核</n-button>
        <n-button type="primary" @click="emit('navigate', 'scheme-library')">前往方案库</n-button>
      </n-space>
    </n-spin>

    <!-- 自定义方案编辑弹窗 -->
    <n-modal v-model:show="showEditModal" preset="card" title="新建自定义方案" style="width: 600px">
      <n-form :model="editForm" ref="editFormRef" label-placement="left" label-width="100">
        <n-form-item label="方案名称" path="name">
          <n-input v-model:value="editForm.name" placeholder="请输入方案名称" />
        </n-form-item>
        <n-form-item label="方案简介">
          <n-input v-model:value="editForm.intro" type="textarea" rows="3" placeholder="简要介绍方案内容" />
        </n-form-item>
        <n-form-item label="经济效益">
          <n-input v-model:value="editForm.economic_benefit" type="textarea" rows="2" placeholder="年节约费用/回收期等" />
        </n-form-item>
        <n-form-item label="环境效益">
          <n-input v-model:value="editForm.environment_benefit" type="textarea" rows="2" placeholder="减排效果、达标情况等" />
        </n-form-item>
      </n-form>
      <template #action>
        <n-space justify="end">
          <n-button @click="showEditModal = false">取消</n-button>
          <n-button type="primary" :loading="savingScheme" @click="saveCustomScheme">保存</n-button>
        </n-space>
      </template>
    </n-modal>

    <!-- 新增因素弹窗 -->
    <n-modal v-model:show="showAddFactor" preset="dialog" title="新增因素">
      <n-form :model="addFactorForm" label-width="80" label-placement="left">
        <n-form-item label="因素名称">
          <n-input v-model:value="addFactorForm.name" placeholder="如 废水可生化性" />
        </n-form-item>
        <n-form-item label="权重W">
          <n-input-number v-model:value="addFactorForm.weight" :min="0" :max="20" :precision="0" />
        </n-form-item>
      </n-form>
      <template #action>
        <n-space justify="end">
          <n-button quaternary @click="showAddFactor = false">取消</n-button>
          <n-button type="primary" @click="confirmAddFactor">确定</n-button>
        </n-space>
      </template>
    </n-modal>

    <!-- 新增审核重点弹窗 -->
    <n-modal v-model:show="showAddFocus" preset="dialog" title="新增审核重点">
      <n-form :model="addFocusForm" label-width="100" label-placement="left">
        <n-form-item label="审核重点名称">
          <n-input v-model:value="addFocusForm.name" placeholder="如 二车间" />
        </n-form-item>
      </n-form>
      <template #action>
        <n-space justify="end">
          <n-button quaternary @click="showAddFocus = false">取消</n-button>
          <n-button type="primary" @click="confirmAddFocus">确定</n-button>
        </n-space>
      </template>
    </n-modal>

    <!-- 方案库导入弹窗 -->
    <n-modal 
      v-model:show="showImportModal" 
      preset="card" 
      :title="importModalTitle" 
      style="width: 900px"
      :mask-closable="false"
    >
      <div style="margin-bottom: 16px">
        <n-space>
          <span>选择指标筛选：</span>
          <n-select
            v-model:value="selectedIndicatorIds"
            multiple
            filterable
            placeholder="选择指标（不选则显示所有方案）"
            :options="indicatorOptions"
            style="width: 400px"
            @update:value="onIndicatorFilterChange"
          />
          <n-button @click="selectedIndicatorIds = []">清空筛选</n-button>
        </n-space>
      </div>
      <n-data-table
        :columns="librarySchemeColumns"
        :data="filteredLibrarySchemes"
        :row-key="row => row.id"
        checkable
        @update:checked-row-keys="(keys) => selectedLibrarySchemeIds = keys"
        size="small"
        :bordered="true"
        :max-height="400"
        :loading="loadingLibrarySchemes"
      />
      <template #footer>
        <div style="text-align: right">
          <n-space>
            <n-button @click="showImportModal = false">取消</n-button>
            <n-button type="primary" @click="confirmImportSchemes" :disabled="selectedLibrarySchemeIds.length === 0" :loading="importingSchemes">
              导入选中方案（{{ selectedLibrarySchemeIds.length }}）
            </n-button>
          </n-space>
        </div>
      </template>
    </n-modal>
  </div>
  
</template>

<script setup>
import { ref, computed, onMounted, watch, h } from 'vue'
import {
  NSpin,
  NCard,
  NSpace,
  NInput,
  NButton,
  NDataTable,
  NModal,
  NForm,
  NFormItem,
  NSelect,
  NTag
} from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'
import api from '@/api'

defineOptions({ name: 'PCB问题及清洁生产方案' })

const props = defineProps({
  enterpriseId: {
    type: [String, Number],
    required: true
  }
})

const emit = defineEmits(['update', 'navigate'])

// 状态
const loading = ref(false)
const savingIssues = ref(false)
const savingScheme = ref(false)
const savingScoring = ref(false)
const savingLowSchemes = ref(false)
const savingMhSchemes = ref(false)
const showImportModal = ref(false)
const importModalType = ref('low') // 'low' or 'mh'
const loadingLibrarySchemes = ref(false)
const importingSchemes = ref(false)
const librarySchemes = ref([])
const selectedLibrarySchemeIds = ref([])
const selectedIndicatorIds = ref([])
const indicatorOptions = ref([])

// Part 1: 问题清单
const issueSearch = ref('')
const issues = ref([])
const issueColumns = [
  { title: '序号', key: 'index', width: 60, render: (_, idx) => String((idx ?? 0) + 1) },
  { title: '一级指标', key: 'primary_indicator' },
  { title: '一级指标权重', key: 'primary_weight', width: 130 },
  { title: '二级指标', key: 'secondary_indicator' },
  { title: '二级指标权重', key: 'secondary_weight', width: 130 },
  { title: '当前评级', key: 'current_level', width: 100 }
]
const filteredIssues = computed(() => {
  if (!issueSearch.value) return issues.value
  const kw = issueSearch.value.toLowerCase()
  return issues.value.filter(i => `${i.primary_indicator}${i.secondary_indicator}${i.current_level}`.toLowerCase().includes(kw))
})

// Part 2: 无/低费方案库
const lowSearch = ref('')
const lowSchemes = ref([])
const selectedLowSchemeIds = ref([])
const lowSchemeColumns = [
  { type: 'selection' },
  { title: '方案名称', key: 'name' },
  { title: '方案简介', key: 'intro' },
  { title: '经济效益', key: 'economic_benefit' },
  { title: '环境效益', key: 'environment_benefit' },
  {
    title: '操作',
    key: 'actions',
    width: 100,
    render: (row) => {
      return h('div', { style: 'display: flex; justify-content: center;' }, [
        h('n-button', {
          size: 'small',
          type: 'error',
          tertiary: true,
          onClick: () => handleDeleteScheme('low', row.id)
        }, { default: () => '删除' })
      ])
    }
  }
]
const filteredLowSchemes = computed(() => filterByKeyword(lowSchemes.value, lowSearch.value))

// Part 3: 中高费方案库
const mhSearch = ref('')
const mhSchemes = ref([])
const selectedMhSchemeIds = ref([])
const mhSchemeColumns = [
  { type: 'selection' },
  { title: '方案名称', key: 'name' },
  { title: '方案简介', key: 'intro' },
  { title: '经济效益', key: 'economic_benefit' },
  { title: '环境效益', key: 'environment_benefit' },
  {
    title: '操作',
    key: 'actions',
    width: 100,
    render: (row) => {
      return h('div', { style: 'display: flex; justify-content: center;' }, [
        h('n-button', {
          size: 'small',
          type: 'error',
          tertiary: true,
          onClick: () => handleDeleteScheme('mh', row.id)
        }, { default: () => '删除' })
      ])
    }
  }
]
const filteredMhSchemes = computed(() => filterByKeyword(mhSchemes.value, mhSearch.value))

// 方案库导入相关
const librarySchemeColumns = computed(() => [
  { type: 'selection' },
  { title: '方案名称', key: 'name', width: 200 },
  { title: '方案简介', key: 'description', ellipsis: true },
  { title: '关联指标', key: 'related_indicator_names', width: 250, render: (row) => {
    const names = row.related_indicator_names || []
    return names.length > 0 ? names.join('、') : '无'
  }},
  { title: '经济效益', key: 'economic_benefit', ellipsis: true },
  { title: '环境效益', key: 'environmental_benefit', ellipsis: true }
])

const filteredLibrarySchemes = computed(() => {
  return librarySchemes.value
})

const importModalTitle = computed(() => {
  return importModalType.value === 'low' ? '从方案库导入无/低费方案' : '从方案库导入中/高费方案'
})

// 自定义方案编辑
const showEditModal = ref(false)
const editFormRef = ref(null)
const editForm = ref({ name: '', intro: '', economic_benefit: '', environment_benefit: '' })
const currentSchemeType = ref('low') // 'low' or 'mh'

function filterByKeyword(list, kw) {
  if (!kw) return list
  const k = String(kw).toLowerCase()
  return list.filter(it => JSON.stringify(it).toLowerCase().includes(k))
}

// API 拉取
const fetchAll = async () => {
  if (loading.value) return // 防止重复加载
  loading.value = true
  try {
    // 并行加载数据，提高性能
    const [issuesRes, lowRes, mhRes] = await Promise.allSettled([
      api.pcb.problemSolution.getIssues(props.enterpriseId),
      api.pcb.problemSolution.getLowCostSchemes(props.enterpriseId),
      api.pcb.problemSolution.getMediumHighCostSchemes(props.enterpriseId)
    ])
    
    // 处理问题清单
    if (issuesRes.status === 'fulfilled' && issuesRes.value?.data) {
      issues.value = Array.isArray(issuesRes.value.data) ? issuesRes.value.data : []
    } else {
      issues.value = []
      console.error('加载问题清单失败:', issuesRes.reason)
    }
    
    // 处理无/低费方案
    if (lowRes.status === 'fulfilled' && lowRes.value?.data) {
      lowSchemes.value = Array.isArray(lowRes.value.data) ? lowRes.value.data : []
    } else {
      lowSchemes.value = []
      console.error('加载无/低费方案失败:', lowRes.reason)
    }
    
    // 处理中/高费方案
    if (mhRes.status === 'fulfilled' && mhRes.value?.data) {
      mhSchemes.value = Array.isArray(mhRes.value.data) ? mhRes.value.data : []
    } else {
      mhSchemes.value = []
      console.error('加载中/高费方案失败:', mhRes.reason)
    }
    
    // 加载权重计分配置（单独处理，因为需要初始化默认值）
    await loadScoringConfig()
  } catch (e) {
    console.error('加载数据失败:', e)
    // 即使出错也初始化默认值，防止页面崩溃
    issues.value = []
    lowSchemes.value = []
    mhSchemes.value = []
    window.$message.error('加载数据失败: ' + (e.message || '未知错误'))
  } finally {
    loading.value = false
  }
}

// 加载权重计分配置
const loadScoringConfig = async () => {
  try {
    const res = await api.pcb.problemSolution.getScoringConfig(props.enterpriseId)
    
    // 确保 factors 和 focuses 有默认值
    if (!factors.value || factors.value.length === 0) {
      factors.value = [
        { key: 'waste_amount', name: '废弃物量', w: 10 },
        { key: 'toxicity', name: '废弃物毒性', w: 9 },
        { key: 'energy', name: '能源消耗', w: 9 },
        { key: 'env_cost', name: '环保费用', w: 8 },
        { key: 'cp_potential', name: 'CP潜力', w: 6 },
        { key: 'positivity', name: '车间积极', w: 5 }
      ]
    }
    
    if (res?.data && res.data.factors && res.data.focuses) {
      // 转换factors格式（从{key, name, weight}转为{key, name, w}）
      if (res.data.factors.length > 0) {
        factors.value = res.data.factors.map(f => ({
          key: f.key,
          name: f.name,
          w: f.weight || f.w || 0
        }))
      }
      
      // 设置focuses
      if (res.data.focuses.length > 0) {
        focuses.value = res.data.focuses
      } else if (focuses.value.length === 0) {
        focuses.value = [{ id: 1, name: '审核重点1' }]
      }
      
      // 初始化scores结构 - 确保完整性
      scores.value = {}
      for (const focus of focuses.value) {
        const focusId = String(focus.id)
        if (!scores.value[focusId]) {
          scores.value[focusId] = {}
        }
        for (const factor of factors.value) {
          const savedScore = res.data.scores?.[focusId]?.[factor.key]
          if (savedScore && typeof savedScore === 'object') {
            scores.value[focusId][factor.key] = {
              r: Number(savedScore.r || 0),
              rw: Number(savedScore.rw || 0)
            }
          } else {
            scores.value[focusId][factor.key] = { r: 0, rw: 0 }
          }
        }
      }
    } else {
      // 如果没有数据，初始化默认结构
      if (focuses.value.length === 0) {
        focuses.value = [{ id: 1, name: '审核重点1' }]
      }
      scores.value = {}
      for (const focus of focuses.value) {
        const focusId = String(focus.id)
        scores.value[focusId] = {}
        for (const factor of factors.value) {
          scores.value[focusId][factor.key] = { r: 0, rw: 0 }
        }
      }
    }
  } catch (e) {
    console.error('加载权重计分配置失败:', e)
    // 初始化默认结构
    if (focuses.value.length === 0) {
      focuses.value = [{ id: 1, name: '审核重点1' }]
    }
    scores.value = {}
    for (const focus of focuses.value) {
      const focusId = String(focus.id)
      scores.value[focusId] = {}
      for (const factor of factors.value) {
        scores.value[focusId][factor.key] = { r: 0, rw: 0 }
      }
    }
  }
}

const saveIssues = async () => {
  try {
    savingIssues.value = true
      await api.pcb.problemSolution.saveIssues(props.enterpriseId, issues.value)
    window.$message.success('问题清单已暂存')
    await fetchAll() // 重新加载数据
  } catch (e) {
    window.$message.error('保存失败: ' + (e.message || '未知错误'))
  } finally {
    savingIssues.value = false
  }
}

// 从方案库导入方案 - 打开弹窗
const importFromLibrary = async (type) => {
  importModalType.value = type
  selectedLibrarySchemeIds.value = []
  selectedIndicatorIds.value = []
  
  // 初始化指标选项
  indicatorOptions.value = issues.value.map(issue => ({
    label: `${issue.primary_indicator} - ${issue.secondary_indicator}`,
    value: issue.indicator_id
  }))
  
  // 加载方案库数据
  await loadLibrarySchemes()
  showImportModal.value = true
}

// 加载方案库方案
const loadLibrarySchemes = async () => {
  loadingLibrarySchemes.value = true
  try {
    const indicatorIds = selectedIndicatorIds.value.length > 0 ? selectedIndicatorIds.value : null
    
    if (importModalType.value === 'low') {
      const res = await api.pcb.problemSolution.getLibraryLowCostSchemes(props.enterpriseId, indicatorIds)
      librarySchemes.value = res?.data || []
    } else {
      const res = await api.pcb.problemSolution.getLibraryMediumHighCostSchemes(props.enterpriseId, indicatorIds, null)
      librarySchemes.value = res?.data || []
    }
  } catch (e) {
    console.error('加载方案库失败:', e)
    window.$message.error('加载方案库失败: ' + (e.message || '未知错误'))
    librarySchemes.value = []
  } finally {
    loadingLibrarySchemes.value = false
  }
}

// 指标筛选变化
const onIndicatorFilterChange = () => {
  loadLibrarySchemes()
}

// 确认导入方案
const confirmImportSchemes = async () => {
  if (selectedLibrarySchemeIds.value.length === 0) {
    window.$message.warning('请至少选择一个方案')
    return
  }
  
  importingSchemes.value = true
  try {
    if (importModalType.value === 'low') {
      await api.pcb.problemSolution.importLowCostSchemes(props.enterpriseId, selectedLibrarySchemeIds.value)
      window.$message.success(`成功导入 ${selectedLibrarySchemeIds.value.length} 个无/低费方案`)
    } else {
      await api.pcb.problemSolution.importMediumHighCostSchemes(props.enterpriseId, {
        scheme_ids: selectedLibrarySchemeIds.value,
        cost_level: 'middle' // 默认中费，用户可在表格中编辑
      })
      window.$message.success(`成功导入 ${selectedLibrarySchemeIds.value.length} 个中/高费方案`)
    }
    showImportModal.value = false
    await fetchAll()
  } catch (e) {
    console.error('导入方案失败:', e)
    window.$message.error('导入方案失败: ' + (e.message || '未知错误'))
  } finally {
    importingSchemes.value = false
  }
}

// 提交权重计分配置
const submitScoringConfig = async () => {
  savingScoring.value = true
  try {
    const payload = buildScoringPayload()
    await api.pcb.problemSolution.saveScoringConfig(props.enterpriseId, payload)
    window.$message.success('权重计分配置已提交')
  } catch (e) {
    console.error('提交权重计分配置失败:', e)
    window.$message.error('提交失败: ' + (e.message || '未知错误'))
  } finally {
    savingScoring.value = false
  }
}

// 提交无/低费方案
const submitLowCostSchemes = async () => {
  savingLowSchemes.value = true
  try {
    const schemes = lowSchemes.value.map(scheme => ({
      name: scheme.name || '',
      intro: scheme.intro || '',
      economic_benefit: scheme.economic_benefit || '',
      environment_benefit: scheme.environment_benefit || '',
      source: scheme.source || 'custom',
      scheme_id: scheme.scheme_id || null,
      indicator_ids: scheme.indicator_ids || [],
      remark: scheme.remark || ''
    }))
    await api.pcb.problemSolution.batchSaveLowCostSchemes(props.enterpriseId, schemes)
    window.$message.success(`成功提交 ${schemes.length} 个无/低费方案`)
    await fetchAll()
  } catch (e) {
    console.error('提交无/低费方案失败:', e)
    window.$message.error('提交失败: ' + (e.message || '未知错误'))
  } finally {
    savingLowSchemes.value = false
  }
}

// 提交中/高费方案
const submitMediumHighCostSchemes = async () => {
  savingMhSchemes.value = true
  try {
    const schemes = mhSchemes.value.map(scheme => ({
      name: scheme.name || '',
      intro: scheme.intro || '',
      economic_benefit: scheme.economic_benefit || '',
      environment_benefit: scheme.environment_benefit || '',
      cost_level: scheme.cost_level || 'middle',
      source: scheme.source || 'custom',
      scheme_id: scheme.scheme_id || null,
      indicator_ids: scheme.indicator_ids || [],
      problem: scheme.problem || '',
      content: scheme.content || '',
      effect: scheme.effect || '',
      remark: scheme.remark || ''
    }))
    await api.pcb.problemSolution.batchSaveMediumHighCostSchemes(props.enterpriseId, schemes)
    window.$message.success(`成功提交 ${schemes.length} 个中/高费方案`)
    await fetchAll()
  } catch (e) {
    console.error('提交中/高费方案失败:', e)
    window.$message.error('提交失败: ' + (e.message || '未知错误'))
  } finally {
    savingMhSchemes.value = false
  }
}

// 关联方案到问题清单（占位功能，可根据需求实现）
const linkSelectedSchemes = async (type) => {
  const ids = type === 'low' ? selectedLowSchemeIds.value : selectedMhSchemeIds.value
  if (!ids.length) {
    window.$message.warning('请先选择方案')
    return
  }
  window.$message.info('方案已关联到问题清单（功能待完善）')
}

const saveCustomScheme = async () => {
  try {
    savingScheme.value = true
    
    // 构建方案数据（只包含4个字段）
    const schemeData = {
      name: editForm.value.name || '',
      intro: editForm.value.intro || '',
      economic_benefit: editForm.value.economic_benefit || '',
      environment_benefit: editForm.value.environment_benefit || '',
      source: 'custom'
    }
    
    // 根据currentSchemeType决定保存到哪个表
    if (currentSchemeType.value === 'low') {
      // 保存到无/低费方案，直接保存到数据库
      await api.pcb.problemSolution.createLowCostScheme(props.enterpriseId, schemeData)
      window.$message.success('无/低费方案创建成功')
    } else {
      // 保存到中/高费方案，需要设置费用等级（默认为中费）
      schemeData.cost_level = 'middle'
      await api.pcb.problemSolution.createMediumHighCostScheme(props.enterpriseId, schemeData)
      window.$message.success('中/高费方案创建成功')
    }
    
    showEditModal.value = false
    await fetchAll() // 刷新列表
  } catch (e) {
    window.$message.error('保存失败: ' + (e.message || '未知错误'))
  } finally {
    savingScheme.value = false
  }
}

onMounted(() => {
  fetchAll()
})

// 低费方案-新建
const openCreateLow = () => {
  currentSchemeType.value = 'low'
  editForm.value = { 
    name: '', 
    intro: '', 
    economic_benefit: '', 
    environment_benefit: '' 
  }
  showEditModal.value = true
}

// 中高费方案-新建
const openCreateMedium = () => {
  currentSchemeType.value = 'mh'
  editForm.value = { 
    name: '', 
    intro: '', 
    economic_benefit: '', 
    environment_benefit: '' 
  }
  showEditModal.value = true
}

// 删除方案
const handleDeleteScheme = async (type, schemeId) => {
  try {
    await window.$dialog.warning({
      title: '确认删除',
      content: '确定要删除这个方案吗？删除后无法恢复。',
      positiveText: '确定',
      negativeText: '取消',
      onPositiveClick: async () => {
        try {
          if (type === 'low') {
            await api.pcb.problemSolution.deleteLowCostScheme(props.enterpriseId, schemeId)
            window.$message.success('删除成功')
          } else {
            await api.pcb.problemSolution.deleteMediumHighCostScheme(props.enterpriseId, schemeId)
            window.$message.success('删除成功')
          }
          await fetchAll() // 刷新列表
        } catch (e) {
          window.$message.error('删除失败: ' + (e.message || '未知错误'))
        }
      }
    })
  } catch (e) {
    // 用户取消删除
  }
}

// 计分模块：数据结构
const factors = ref([
  { key: 'waste_amount', name: '废弃物量', w: 10 },
  { key: 'toxicity', name: '废弃物毒性', w: 9 },
  { key: 'energy', name: '能源消耗', w: 9 },
  { key: 'env_cost', name: '环保费用', w: 8 },
  { key: 'cp_potential', name: 'CP潜力', w: 6 },
  { key: 'positivity', name: '车间积极', w: 5 }
])

const focuses = ref([{ id: 1, name: '审核重点1' }])

// 初始化 scores 结构，确保不会访问未定义的值
const scores = ref({})
// 初始化默认 scores
const initScores = () => {
  scores.value = {}
  for (const focus of focuses.value) {
    const focusId = String(focus.id)
    scores.value[focusId] = {}
    for (const factor of factors.value) {
      scores.value[focusId][factor.key] = { r: 0, rw: 0 }
    }
  }
}
// 初始化一次
initScores()

const addFocus = () => {
  const id = Date.now()
  focuses.value.push({ id, name: `审核重点${focuses.value.length + 1}` })
  const focusId = String(id)
  scores.value[focusId] = {}
  for (const f of factors.value) {
    scores.value[focusId][f.key] = { r: 0, rw: 0 }
  }
}

const removeFocus = async (idx) => {
  const removed = focuses.value.splice(idx, 1)[0]
  if (removed) delete scores.value[String(removed.id)]
  await saveScoringConfig()
}

const removeFactor = async (idx) => {
  const removed = factors.value.splice(idx, 1)[0]
  if (!removed) return
  // 清理各审核重点对应分值
  for (const f of focuses.value) {
    const focusId = String(f.id)
    if (scores.value[focusId]) delete scores.value[focusId][removed.key]
  }
  // 保存评分配置
  await saveScoringConfig()
}

const getTotalScore = (focusId) => {
  try {
    const focusIdStr = String(focusId)
    const one = scores.value[focusIdStr] || {}
    return factors.value.reduce((sum, f) => {
      const score = one[f.key]
      const rw = score && typeof score === 'object' ? (score.rw || 0) : 0
      const weight = f.w || 0
      return sum + (Number(rw) * Number(weight))
    }, 0)
  } catch (e) {
    console.error('计算总分失败:', e)
    return 0
  }
}

const rankedFocuses = computed(() => {
  try {
    if (!focuses.value || focuses.value.length === 0) {
      return []
    }
    return [...focuses.value].sort((a, b) => {
      const scoreA = getTotalScore(a.id)
      const scoreB = getTotalScore(b.id)
      return scoreB - scoreA
    })
  } catch (e) {
    console.error('排序失败:', e)
    return focuses.value || []
  }
})

const resetScore = async () => {
  focuses.value = [{ id: 1, name: '审核重点1' }]
  scores.value = {
    '1': {}
  }
  // 为所有因素初始化分值
  for (const f of factors.value) {
    scores.value['1'][f.key] = { r: 0, rw: 0 }
  }
  await saveScoringConfig()
}

// 新增因素/审核重点 —— 弹窗
const showAddFactor = ref(false)
const showAddFocus = ref(false)
const addFactorForm = ref({ name: '', weight: 5 })
const addFocusForm = ref({ name: '' })

const openAddFactor = () => {
  addFactorForm.value = { name: '', weight: 5 }
  showAddFactor.value = true
}
const openAddFocus = () => {
  addFocusForm.value = { name: `审核重点${focuses.value.length + 1}` }
  showAddFocus.value = true
}

const confirmAddFactor = async () => {
  const key = `f_${Date.now()}`
  factors.value.push({ key, name: addFactorForm.value.name || '自定义因素', w: Number(addFactorForm.value.weight || 0) })
  // 为所有审核重点补一列
  for (const f of focuses.value) {
    const focusId = String(f.id)
    if (!scores.value[focusId]) {
      scores.value[focusId] = {}
    }
    scores.value[focusId][key] = { r: 0, rw: 0 }
  }
  showAddFactor.value = false
  // 使用防抖保存
  debouncedSaveScoringConfig()
}

const confirmAddFocus = async () => {
  const id = Date.now()
  const newFocus = { id, name: addFocusForm.value.name || `审核重点${focuses.value.length + 1}` }
  focuses.value.push(newFocus)
  const focusId = String(id)
  if (!scores.value[focusId]) {
    scores.value[focusId] = {}
  }
  for (const f of factors.value) {
    scores.value[focusId][f.key] = { r: 0, rw: 0 }
  }
  showAddFocus.value = false
  // 使用防抖保存
  debouncedSaveScoringConfig()
}

const buildScoringPayload = () => ({
  factors: factors.value.map(f => ({ key: f.key, name: f.name, weight: f.w })),
  focuses: focuses.value.map(f => ({ id: f.id, name: f.name })),
  scores: Object.keys(scores.value).reduce((acc, focusId) => {
    acc[focusId] = {}
    for (const factor of factors.value) {
      if (scores.value[focusId][factor.key]) {
        acc[focusId][factor.key] = scores.value[focusId][factor.key]
      }
    }
    return acc
  }, {})
})

// 保存权重计分配置
let saveScoringConfigTimer = null
const saveScoringConfig = async () => {
  try {
    const payload = buildScoringPayload()
    await api.pcb.problemSolution.saveScoringConfig(props.enterpriseId, payload)
  } catch (e) {
    console.error('保存权重计分配置失败:', e)
  }
}

// 防抖保存，避免频繁API调用
const debouncedSaveScoringConfig = () => {
  if (saveScoringConfigTimer) {
    clearTimeout(saveScoringConfigTimer)
  }
  saveScoringConfigTimer = setTimeout(() => {
    saveScoringConfig()
  }, 500) // 500ms 防抖
}

</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-icon {
  font-size: 18px;
  color: #1890ff;
}

.header-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--n-text-color);
}

.issue-table :deep(textarea.n-input__textarea-el) {
  font-size: 12px;
}

.score-table-wrapper {
  overflow-x: auto;
}

.score-table {
  width: 100%;
  border-collapse: collapse;
}

.score-table th,
.score-table td {
  border: 1px solid var(--n-border-color);
  padding: 6px 8px;
  text-align: center;
}

.score-table .w-cell { width: 60px; }

.cell-flex { display: flex; gap: 6px; justify-content: center; }

.focus-title { display: flex; align-items: center; gap: 6px; justify-content: center; }

.total-row .bold { font-weight: 600; }

/* 弹窗样式细化 */
.modal-row { display: flex; gap: 12px; }
</style>


