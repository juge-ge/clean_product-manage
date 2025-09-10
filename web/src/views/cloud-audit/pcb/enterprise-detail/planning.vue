<template>
  <div class="planning-module">
    <!-- 审核工作组 -->
    <n-card title="审核工作组" class="mb-4">
      <template #header-extra>
        <n-button type="primary" @click="showAddMemberModal = true">
          <template #icon>
            <TheIcon icon="carbon:add" />
          </template>
          添加成员
        </n-button>
      </template>
      
      <div class="team-section">
        <div class="team-leader mb-4">
          <h4>审核组长</h4>
          <n-card v-if="auditTeam.leader" class="leader-card">
            <div class="member-info">
              <div class="member-avatar">
                <n-avatar size="large" round>
                  {{ auditTeam.leader.name.charAt(0) }}
                </n-avatar>
              </div>
              <div class="member-details">
                <h5>{{ auditTeam.leader.name }}</h5>
                <p>{{ auditTeam.leader.title }}</p>
                <p>{{ auditTeam.leader.phone }}</p>
                <p>{{ auditTeam.leader.email }}</p>
              </div>
            </div>
          </n-card>
        </div>

        <div class="team-members">
          <h4>审核成员</h4>
          <div class="members-grid">
            <n-card 
              v-for="member in auditTeam.members" 
              :key="member.id"
              class="member-card"
            >
              <div class="member-info">
                <div class="member-avatar">
                  <n-avatar size="medium" round>
                    {{ member.name.charAt(0) }}
                  </n-avatar>
                </div>
                <div class="member-details">
                  <h5>{{ member.name }}</h5>
                  <p>{{ member.title }}</p>
                  <p>{{ member.phone }}</p>
                  <p>{{ member.email }}</p>
                </div>
                <div class="member-actions">
                  <n-button size="small" @click="editMember(member)">编辑</n-button>
                  <n-button size="small" type="error" @click="deleteMember(member.id)">删除</n-button>
                </div>
              </div>
            </n-card>
          </div>
        </div>
      </div>
    </n-card>

    <!-- 工作计划 -->
    <n-card title="工作计划" class="mb-4">
      <template #header-extra>
        <n-button type="primary" @click="showPlanModal = true">
          <template #icon>
            <TheIcon icon="carbon:add" />
          </template>
          制定计划
        </n-button>
      </template>
      
      <n-timeline>
        <n-timeline-item 
          v-for="plan in workPlans"
          :key="plan.id"
          :title="plan.title"
          :content="plan.description"
          :time="`${plan.startDate} - ${plan.endDate}`"
          :type="getPlanType(plan.status)"
        >
          <template #header>
            <div class="plan-header">
              <h5>{{ plan.title }}</h5>
              <n-tag :type="getStatusType(plan.status)">
                {{ getStatusText(plan.status) }}
              </n-tag>
            </div>
          </template>
          <div class="plan-content">
            <p><strong>时间：</strong>{{ plan.startDate }} - {{ plan.endDate }}</p>
            <div class="plan-tasks">
              <h6>任务清单：</h6>
              <ul>
                <li 
                  v-for="task in plan.tasks" 
                  :key="task.id"
                  :class="{ completed: task.completed }"
                >
                  <n-checkbox 
                    v-model:checked="task.completed"
                    @update:checked="updateTaskStatus(plan.id, task.id, $event)"
                  >
                    {{ task.content }}
                  </n-checkbox>
                </li>
              </ul>
            </div>
          </div>
        </n-timeline-item>
      </n-timeline>
    </n-card>

    <!-- 宣传与培训 -->
    <n-card title="宣传与培训">
      <template #header-extra>
        <n-button type="primary" @click="showTrainingModal = true">
          <template #icon>
            <TheIcon icon="carbon:add" />
          </template>
          添加培训记录
        </n-button>
      </template>
      
      <n-data-table
        :columns="trainingColumns"
        :data="trainingRecords"
        :pagination="false"
      />
    </n-card>

    <!-- 添加成员弹窗 -->
    <CrudModal
      v-model:visible="showAddMemberModal"
      title="添加团队成员"
      @save="handleAddMember"
    >
      <n-form ref="memberFormRef" :model="memberForm" :rules="memberRules">
        <n-form-item label="姓名" path="name">
          <n-input v-model:value="memberForm.name" placeholder="请输入姓名" />
        </n-form-item>
        <n-form-item label="职务" path="title">
          <n-input v-model:value="memberForm.title" placeholder="请输入职务" />
        </n-form-item>
        <n-form-item label="联系电话" path="phone">
          <n-input v-model:value="memberForm.phone" placeholder="请输入联系电话" />
        </n-form-item>
        <n-form-item label="邮箱" path="email">
          <n-input v-model:value="memberForm.email" placeholder="请输入邮箱" />
        </n-form-item>
        <n-form-item label="角色" path="role">
          <n-select
            v-model:value="memberForm.role"
            :options="roleOptions"
            placeholder="请选择角色"
          />
        </n-form-item>
      </n-form>
    </CrudModal>

    <!-- 添加计划弹窗 -->
    <CrudModal
      v-model:visible="showPlanModal"
      title="制定工作计划"
      @save="handleAddPlan"
    >
      <n-form ref="planFormRef" :model="planForm" :rules="planRules">
        <n-form-item label="计划标题" path="title">
          <n-input v-model:value="planForm.title" placeholder="请输入计划标题" />
        </n-form-item>
        <n-form-item label="开始日期" path="startDate">
          <n-date-picker
            v-model:value="planForm.startDate"
            type="date"
            placeholder="请选择开始日期"
            style="width: 100%"
          />
        </n-form-item>
        <n-form-item label="结束日期" path="endDate">
          <n-date-picker
            v-model:value="planForm.endDate"
            type="date"
            placeholder="请选择结束日期"
            style="width: 100%"
          />
        </n-form-item>
        <n-form-item label="计划描述" path="description">
          <n-input
            v-model:value="planForm.description"
            type="textarea"
            placeholder="请输入计划描述"
            :rows="3"
          />
        </n-form-item>
      </n-form>
    </CrudModal>

    <!-- 添加培训记录弹窗 -->
    <CrudModal
      v-model:visible="showTrainingModal"
      title="添加培训记录"
      @save="handleAddTraining"
    >
      <n-form ref="trainingFormRef" :model="trainingForm" :rules="trainingRules">
        <n-form-item label="培训主题" path="title">
          <n-input v-model:value="trainingForm.title" placeholder="请输入培训主题" />
        </n-form-item>
        <n-form-item label="培训时间" path="date">
          <n-date-picker
            v-model:value="trainingForm.date"
            type="date"
            placeholder="请选择培训时间"
            style="width: 100%"
          />
        </n-form-item>
        <n-form-item label="培训地点" path="location">
          <n-input v-model:value="trainingForm.location" placeholder="请输入培训地点" />
        </n-form-item>
        <n-form-item label="参与人数" path="participants">
          <n-input-number
            v-model:value="trainingForm.participants"
            placeholder="请输入参与人数"
            :min="1"
          />
        </n-form-item>
        <n-form-item label="培训内容" path="content">
          <n-input
            v-model:value="trainingForm.content"
            type="textarea"
            placeholder="请输入培训内容"
            :rows="3"
          />
        </n-form-item>
      </n-form>
    </CrudModal>

    <!-- 模块导航按钮 -->
    <div class="module-navigation mt-4">
      <n-space justify="space-between">
        <n-button @click="goToPrevious">
          <template #icon>
            <TheIcon icon="carbon:arrow-left" />
          </template>
          企业信息
        </n-button>
        <n-button type="primary" @click="goToNext">
          预审核
          <template #icon>
            <TheIcon icon="carbon:arrow-right" />
          </template>
        </n-button>
      </n-space>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { 
  NCard, 
  NButton, 
  NTimeline, 
  NTimelineItem, 
  NTag, 
  NCheckbox, 
  NDataTable,
  NForm,
  NFormItem,
  NInput,
  NInputNumber,
  NSelect,
  NDatePicker,
  NAvatar
} from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'
import CrudModal from '@/components/table/CrudModal.vue'
import { mockDetailApi } from '@/mock/pcb-detail'

defineOptions({ name: '筹划与组织' })

const props = defineProps({
  enterpriseId: {
    type: [String, Number],
    required: true
  }
})

const emit = defineEmits(['update', 'navigate'])

// 数据状态
const auditTeam = ref({ leader: null, members: [] })
const workPlans = ref([])
const trainingRecords = ref([])

// 弹窗状态
const showAddMemberModal = ref(false)
const showPlanModal = ref(false)
const showTrainingModal = ref(false)

// 表单数据
const memberForm = ref({
  name: '',
  title: '',
  phone: '',
  email: '',
  role: 'member'
})

const planForm = ref({
  title: '',
  startDate: null,
  endDate: null,
  description: ''
})

const trainingForm = ref({
  title: '',
  date: null,
  location: '',
  participants: null,
  content: ''
})

// 选项数据
const roleOptions = [
  { label: '审核组长', value: 'leader' },
  { label: '审核成员', value: 'member' }
]

// 表格列配置
const trainingColumns = [
  {
    title: '培训主题',
    key: 'title',
    width: 200
  },
  {
    title: '培训时间',
    key: 'date',
    width: 120
  },
  {
    title: '培训地点',
    key: 'location',
    width: 150
  },
  {
    title: '参与人数',
    key: 'participants',
    width: 100
  },
  {
    title: '培训内容',
    key: 'content',
    ellipsis: { tooltip: true }
  }
]

// 表单验证规则
const memberRules = {
  name: { required: true, message: '请输入姓名', trigger: 'blur' },
  title: { required: true, message: '请输入职务', trigger: 'blur' },
  phone: { required: true, message: '请输入联系电话', trigger: 'blur' },
  email: { required: true, message: '请输入邮箱', trigger: 'blur' },
  role: { required: true, message: '请选择角色', trigger: 'change' }
}

const planRules = {
  title: { required: true, message: '请输入计划标题', trigger: 'blur' },
  startDate: { required: true, message: '请选择开始日期', trigger: 'change' },
  endDate: { required: true, message: '请选择结束日期', trigger: 'change' },
  description: { required: true, message: '请输入计划描述', trigger: 'blur' }
}

const trainingRules = {
  title: { required: true, message: '请输入培训主题', trigger: 'blur' },
  date: { required: true, message: '请选择培训时间', trigger: 'change' },
  location: { required: true, message: '请输入培训地点', trigger: 'blur' },
  participants: { required: true, message: '请输入参与人数', trigger: 'change' },
  content: { required: true, message: '请输入培训内容', trigger: 'blur' }
}

// 获取数据
const fetchData = async () => {
  try {
    const [teamResponse, plansResponse] = await Promise.all([
      mockDetailApi.getAuditTeam(props.enterpriseId),
      mockDetailApi.getWorkPlans(props.enterpriseId)
    ])
    
    auditTeam.value = teamResponse.data
    workPlans.value = plansResponse.data
  } catch (error) {
    console.error('获取数据失败:', error)
    window.$message.error('获取数据失败')
  }
}

// 状态相关方法
const getStatusType = (status) => {
  const types = {
    completed: 'success',
    'in-progress': 'info',
    pending: 'default'
  }
  return types[status] || 'default'
}

const getStatusText = (status) => {
  const texts = {
    completed: '已完成',
    'in-progress': '进行中',
    pending: '待开始'
  }
  return texts[status] || '未知'
}

const getPlanType = (status) => {
  const types = {
    completed: 'success',
    'in-progress': 'info',
    pending: 'default'
  }
  return types[status] || 'default'
}

// 成员管理
const handleAddMember = async () => {
  try {
    await mockDetailApi.addTeamMember(props.enterpriseId, memberForm.value)
    window.$message.success('添加成员成功')
    showAddMemberModal.value = false
    fetchData()
  } catch (error) {
    console.error('添加成员失败:', error)
    window.$message.error('添加成员失败')
  }
}

const editMember = (member) => {
  memberForm.value = { ...member }
  showAddMemberModal.value = true
}

const deleteMember = async (memberId) => {
  try {
    await window.$dialog.confirm({
      title: '确认删除',
      content: '确定要删除该成员吗？'
    })
    await mockDetailApi.deleteTeamMember(props.enterpriseId, memberId)
    window.$message.success('删除成功')
    fetchData()
  } catch (error) {
    if (error) {
      console.error('删除失败:', error)
      window.$message.error('删除失败')
    }
  }
}

// 计划管理
const handleAddPlan = async () => {
  try {
    await mockDetailApi.createWorkPlan(props.enterpriseId, planForm.value)
    window.$message.success('添加计划成功')
    showPlanModal.value = false
    fetchData()
  } catch (error) {
    console.error('添加计划失败:', error)
    window.$message.error('添加计划失败')
  }
}

const updateTaskStatus = async (planId, taskId, completed) => {
  try {
    const plan = workPlans.value.find(p => p.id === planId)
    if (plan) {
      const task = plan.tasks.find(t => t.id === taskId)
      if (task) {
        task.completed = completed
        await mockDetailApi.updateWorkPlan(props.enterpriseId, planId, plan)
      }
    }
  } catch (error) {
    console.error('更新任务状态失败:', error)
  }
}

// 培训管理
const handleAddTraining = async () => {
  try {
    await mockDetailApi.createTrainingRecord(props.enterpriseId, trainingForm.value)
    window.$message.success('添加培训记录成功')
    showTrainingModal.value = false
    fetchData()
  } catch (error) {
    console.error('添加培训记录失败:', error)
    window.$message.error('添加培训记录失败')
  }
}

// 导航方法
const goToPrevious = () => {
  emit('navigate', 'basic-info')
}

const goToNext = () => {
  emit('navigate', 'pre-audit')
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.planning-module {
  padding: 16px;
}

.team-section h4 {
  margin-bottom: 16px;
  color: var(--n-text-color);
}

.leader-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.member-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.member-avatar {
  flex-shrink: 0;
}

.member-details {
  flex: 1;
}

.member-details h5 {
  margin: 0 0 8px 0;
  font-size: 16px;
  font-weight: 600;
}

.member-details p {
  margin: 4px 0;
  font-size: 14px;
  opacity: 0.8;
}

.member-actions {
  display: flex;
  gap: 8px;
}

.members-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.member-card {
  transition: all 0.3s ease;
}

.member-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.plan-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.plan-header h5 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}

.plan-content p {
  margin: 8px 0;
}

.plan-tasks {
  margin-top: 12px;
}

.plan-tasks h6 {
  margin: 0 0 8px 0;
  font-size: 14px;
  font-weight: 600;
}

.plan-tasks ul {
  margin: 0;
  padding-left: 20px;
}

.plan-tasks li {
  margin: 4px 0;
  list-style: none;
}

.plan-tasks li.completed {
  text-decoration: line-through;
  opacity: 0.6;
}

.cursor-pointer {
  cursor: pointer;
}
</style>
