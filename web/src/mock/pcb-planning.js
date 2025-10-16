// PCB筹划与组织模块Mock数据
// 注意：这些mock数据已经迁移到数据库中，不再使用

// 审核领导小组成员Mock数据
/* export const mockLeadershipTeam = [
  {
    id: 1,
    name: '张明',
    position: '总经理',
    department: '总经理办公室',
    phone: '13800138001',
    email: 'zhangming@company.com',
    role: '组长',
    responsibilities: '负责清洁生产审核工作的总体协调和决策，确保审核工作的顺利进行',
    createdAt: '2024-01-15 09:00:00'
  },
  {
    id: 2,
    name: '李华',
    position: '副总经理',
    department: '生产部',
    phone: '13800138002',
    email: 'lihua@company.com',
    role: '副组长',
    responsibilities: '协助组长开展清洁生产审核工作，负责生产部门的协调配合',
    createdAt: '2024-01-15 09:30:00'
  },
  {
    id: 3,
    name: '王强',
    position: '环保工程师',
    department: '环保部',
    phone: '13800138003',
    email: 'wangqiang@company.com',
    role: '成员',
    responsibilities: '负责环保技术指导，协助制定清洁生产改进方案',
    createdAt: '2024-01-15 10:00:00'
  },
  {
    id: 4,
    name: '陈丽',
    position: '财务经理',
    department: '财务部',
    phone: '13800138004',
    email: 'chenli@company.com',
    role: '成员',
    responsibilities: '负责清洁生产项目的财务预算和成本效益分析',
    createdAt: '2024-01-15 10:30:00'
  }
]

// 清洁生产工作小组成员Mock数据
export const mockWorkTeam = [
  {
    id: 1,
    name: '刘建国',
    position: '生产主管',
    department: '生产部',
    phone: '13800138005',
    email: 'liujianguo@company.com',
    role: '组长',
    responsibilities: '负责清洁生产工作小组的日常管理，协调各部门工作',
    createdAt: '2024-01-16 09:00:00'
  },
  {
    id: 2,
    name: '赵敏',
    position: '技术工程师',
    department: '技术部',
    phone: '13800138006',
    email: 'zhaomin@company.com',
    role: '副组长',
    responsibilities: '负责技术方案制定和实施，协助组长完成各项工作任务',
    createdAt: '2024-01-16 09:30:00'
  },
  {
    id: 3,
    name: '孙伟',
    position: '设备工程师',
    department: '设备部',
    phone: '13800138007',
    email: 'sunwei@company.com',
    role: '成员',
    responsibilities: '负责设备改造和维护，确保设备运行符合清洁生产要求',
    createdAt: '2024-01-16 10:00:00'
  },
  {
    id: 4,
    name: '周芳',
    position: '质量工程师',
    department: '质量部',
    phone: '13800138008',
    email: 'zhoufang@company.com',
    role: '成员',
    responsibilities: '负责产品质量控制和检测，确保产品符合环保标准',
    createdAt: '2024-01-16 10:30:00'
  },
  {
    id: 5,
    name: '吴刚',
    position: '安全工程师',
    department: '安全部',
    phone: '13800138009',
    email: 'wugang@company.com',
    role: '成员',
    responsibilities: '负责安全生产管理，确保清洁生产过程中的安全',
    createdAt: '2024-01-16 11:00:00'
  }
]

// 工作计划表Mock数据 - 十个阶段
export const mockWorkPlans = [
  {
    id: 1,
    stage: '审核准备',
    stageOrder: 1,
    workContent: '成立清洁生产审核领导小组和工作小组，制定审核计划，确定审核范围',
    plannedStartDate: new Date('2024-01-15').getTime(),
    plannedEndDate: new Date('2024-01-31').getTime(),
    responsibleDepartment: '总经理办公室',
    actualStartDate: new Date('2024-01-15').getTime(),
    actualEndDate: new Date('2024-01-30').getTime(),
    status: 'completed',
    progress: 100,
    remarks: '已按计划完成，领导小组和工作小组已成立'
  },
  {
    id: 2,
    stage: '预审核',
    stageOrder: 2,
    workContent: '收集企业基础资料，进行现状调研，识别清洁生产机会',
    plannedStartDate: new Date('2024-02-01').getTime(),
    plannedEndDate: new Date('2024-02-28').getTime(),
    responsibleDepartment: '环保部',
    actualStartDate: new Date('2024-02-01').getTime(),
    actualEndDate: null,
    status: 'in-progress',
    progress: 60,
    remarks: '正在进行中，基础资料收集完成，现状调研进行中'
  },
  {
    id: 3,
    stage: '审核',
    stageOrder: 3,
    workContent: '深入分析生产过程和污染物产生情况，确定审核重点',
    plannedStartDate: new Date('2024-03-01').getTime(),
    plannedEndDate: new Date('2024-03-31').getTime(),
    responsibleDepartment: '技术部',
    actualStartDate: null,
    actualEndDate: null,
    status: 'pending',
    progress: 0,
    remarks: '待开始'
  },
  {
    id: 4,
    stage: '实施方案的产生和筛选',
    stageOrder: 4,
    workContent: '提出清洁生产方案，进行技术经济分析，筛选可行方案',
    plannedStartDate: new Date('2024-04-01').getTime(),
    plannedEndDate: new Date('2024-04-30').getTime(),
    responsibleDepartment: '技术部',
    actualStartDate: null,
    actualEndDate: null,
    status: 'pending',
    progress: 0,
    remarks: '待开始'
  },
  {
    id: 5,
    stage: '实施方案的确定',
    stageOrder: 5,
    workContent: '确定最终实施方案，制定实施计划和时间表',
    plannedStartDate: new Date('2024-05-01').getTime(),
    plannedEndDate: new Date('2024-05-15').getTime(),
    responsibleDepartment: '生产部',
    actualStartDate: null,
    actualEndDate: null,
    status: 'pending',
    progress: 0,
    remarks: '待开始'
  },
  {
    id: 6,
    stage: '方案实施',
    stageOrder: 6,
    workContent: '按照确定的方案进行实施，包括设备改造、工艺优化等',
    plannedStartDate: new Date('2024-05-16').getTime(),
    plannedEndDate: new Date('2024-08-31').getTime(),
    responsibleDepartment: '生产部',
    actualStartDate: null,
    actualEndDate: null,
    status: 'pending',
    progress: 0,
    remarks: '待开始'
  },
  {
    id: 7,
    stage: '持续清洁生产',
    stageOrder: 7,
    workContent: '建立清洁生产管理制度，确保清洁生产持续改进',
    plannedStartDate: new Date('2024-09-01').getTime(),
    plannedEndDate: new Date('2024-09-30').getTime(),
    responsibleDepartment: '环保部',
    actualStartDate: null,
    actualEndDate: null,
    status: 'pending',
    progress: 0,
    remarks: '待开始'
  },
  {
    id: 8,
    stage: '编制报告',
    stageOrder: 8,
    workContent: '编制清洁生产审核报告，总结审核成果和经验',
    plannedStartDate: new Date('2024-10-01').getTime(),
    plannedEndDate: new Date('2024-10-31').getTime(),
    responsibleDepartment: '环保部',
    actualStartDate: null,
    actualEndDate: null,
    status: 'pending',
    progress: 0,
    remarks: '待开始'
  },
  {
    id: 9,
    stage: '申请验收',
    stageOrder: 9,
    workContent: '向相关部门申请清洁生产审核验收',
    plannedStartDate: new Date('2024-11-01').getTime(),
    plannedEndDate: new Date('2024-11-15').getTime(),
    responsibleDepartment: '总经理办公室',
    actualStartDate: null,
    actualEndDate: null,
    status: 'pending',
    progress: 0,
    remarks: '待开始'
  },
  {
    id: 10,
    stage: '现场验收',
    stageOrder: 10,
    workContent: '配合验收专家组进行现场验收，提供相关资料',
    plannedStartDate: new Date('2024-11-16').getTime(),
    plannedEndDate: new Date('2024-12-15').getTime(),
    responsibleDepartment: '总经理办公室',
    actualStartDate: null,
    actualEndDate: null,
    status: 'pending',
    progress: 0,
    remarks: '待开始'
  }
]

// 培训记录Mock数据
export const mockTrainingRecords = [
  {
    id: 1,
    title: '清洁生产基础知识培训',
    date: new Date('2024-01-20').getTime(),
    participants: 25,
    duration: 4,
    content: '清洁生产基本概念、法律法规、审核程序等基础知识',
    instructor: '张教授',
    location: '公司会议室',
    status: 'completed',
    createdAt: '2024-01-20 14:00:00'
  },
  {
    id: 2,
    title: '清洁生产审核方法培训',
    date: new Date('2024-02-10').getTime(),
    participants: 20,
    duration: 6,
    content: '清洁生产审核方法、工具使用、数据分析等专业技能',
    instructor: '李工程师',
    location: '公司培训中心',
    status: 'completed',
    createdAt: '2024-02-10 09:00:00'
  },
  {
    id: 3,
    title: '环保法律法规培训',
    date: new Date('2024-02-25').getTime(),
    participants: 30,
    duration: 3,
    content: '最新环保法律法规、政策解读、合规要求等',
    instructor: '王律师',
    location: '公司大会议室',
    status: 'completed',
    createdAt: '2024-02-25 14:00:00'
  },
  {
    id: 4,
    title: '清洁生产技术方案培训',
    date: new Date('2024-03-15').getTime(),
    participants: 18,
    duration: 5,
    content: '清洁生产技术方案制定、评估方法、实施要点等',
    instructor: '陈专家',
    location: '公司技术中心',
    status: 'scheduled',
    createdAt: '2024-03-10 10:00:00'
  }
]

// Mock API函数
export const mockPlanningApi = {
  // 获取审核领导小组
  getLeadershipTeam: async (enterpriseId) => {
    await new Promise(resolve => setTimeout(resolve, 500))
    return {
      code: 200,
      message: '获取成功',
      data: mockLeadershipTeam
    }
  },

  // 添加审核领导小组成员
  addLeadershipMember: async (enterpriseId, data) => {
    await new Promise(resolve => setTimeout(resolve, 500))
    const newMember = {
      id: Date.now(),
      ...data,
      createdAt: new Date().toISOString().slice(0, 19).replace('T', ' ')
    }
    mockLeadershipTeam.push(newMember)
    return {
      code: 200,
      message: '添加成功',
      data: newMember
    }
  },

  // 更新审核领导小组成员
  updateLeadershipMember: async (enterpriseId, memberId, data) => {
    await new Promise(resolve => setTimeout(resolve, 500))
    const index = mockLeadershipTeam.findIndex(member => member.id === memberId)
    if (index !== -1) {
      mockLeadershipTeam[index] = { ...mockLeadershipTeam[index], ...data }
      return {
        code: 200,
        message: '更新成功',
        data: mockLeadershipTeam[index]
      }
    }
    return {
      code: 404,
      message: '成员不存在'
    }
  },

  // 删除审核领导小组成员
  deleteLeadershipMember: async (enterpriseId, memberId) => {
    await new Promise(resolve => setTimeout(resolve, 500))
    const index = mockLeadershipTeam.findIndex(member => member.id === memberId)
    if (index !== -1) {
      mockLeadershipTeam.splice(index, 1)
      return {
        code: 200,
        message: '删除成功'
      }
    }
    return {
      code: 404,
      message: '成员不存在'
    }
  },

  // 获取清洁生产工作小组
  getWorkTeam: async (enterpriseId) => {
    await new Promise(resolve => setTimeout(resolve, 500))
    return {
      code: 200,
      message: '获取成功',
      data: mockWorkTeam
    }
  },

  // 添加清洁生产工作小组成员
  addWorkTeamMember: async (enterpriseId, data) => {
    await new Promise(resolve => setTimeout(resolve, 500))
    const newMember = {
      id: Date.now(),
      ...data,
      createdAt: new Date().toISOString().slice(0, 19).replace('T', ' ')
    }
    mockWorkTeam.push(newMember)
    return {
      code: 200,
      message: '添加成功',
      data: newMember
    }
  },

  // 更新清洁生产工作小组成员
  updateWorkTeamMember: async (enterpriseId, memberId, data) => {
    await new Promise(resolve => setTimeout(resolve, 500))
    const index = mockWorkTeam.findIndex(member => member.id === memberId)
    if (index !== -1) {
      mockWorkTeam[index] = { ...mockWorkTeam[index], ...data }
      return {
        code: 200,
        message: '更新成功',
        data: mockWorkTeam[index]
      }
    }
    return {
      code: 404,
      message: '成员不存在'
    }
  },

  // 删除清洁生产工作小组成员
  deleteWorkTeamMember: async (enterpriseId, memberId) => {
    await new Promise(resolve => setTimeout(resolve, 500))
    const index = mockWorkTeam.findIndex(member => member.id === memberId)
    if (index !== -1) {
      mockWorkTeam.splice(index, 1)
      return {
        code: 200,
        message: '删除成功'
      }
    }
    return {
      code: 404,
      message: '成员不存在'
    }
  },

  // 获取工作计划表
  getWorkPlans: async (enterpriseId) => {
    await new Promise(resolve => setTimeout(resolve, 500))
    return {
      code: 200,
      message: '获取成功',
      data: mockWorkPlans
    }
  },

  // 更新工作计划表
  updateWorkPlans: async (enterpriseId, data) => {
    await new Promise(resolve => setTimeout(resolve, 500))
    // 更新对应阶段的数据
    data.forEach(plan => {
      const index = mockWorkPlans.findIndex(p => p.id === plan.id)
      if (index !== -1) {
        mockWorkPlans[index] = { ...mockWorkPlans[index], ...plan }
      }
    })
    return {
      code: 200,
      message: '更新成功',
      data: mockWorkPlans
    }
  },

  // 获取培训记录
  getTrainingRecords: async (enterpriseId) => {
    await new Promise(resolve => setTimeout(resolve, 500))
    return {
      code: 200,
      message: '获取成功',
      data: mockTrainingRecords
    }
  },

  // 添加培训记录
  addTrainingRecord: async (enterpriseId, data) => {
    await new Promise(resolve => setTimeout(resolve, 500))
    const newRecord = {
      id: Date.now(),
      ...data,
      createdAt: new Date().toISOString().slice(0, 19).replace('T', ' ')
    }
    mockTrainingRecords.push(newRecord)
    return {
      code: 200,
      message: '添加成功',
      data: newRecord
    }
  },

  // 更新培训记录
  updateTrainingRecord: async (enterpriseId, recordId, data) => {
    await new Promise(resolve => setTimeout(resolve, 500))
    const index = mockTrainingRecords.findIndex(record => record.id === recordId)
    if (index !== -1) {
      mockTrainingRecords[index] = { ...mockTrainingRecords[index], ...data }
      return {
        code: 200,
        message: '更新成功',
        data: mockTrainingRecords[index]
      }
    }
    return {
      code: 404,
      message: '记录不存在'
    }
  },

  // 删除培训记录
  deleteTrainingRecord: async (enterpriseId, recordId) => {
    await new Promise(resolve => setTimeout(resolve, 500))
    const index = mockTrainingRecords.findIndex(record => record.id === recordId)
    if (index !== -1) {
      mockTrainingRecords.splice(index, 1)
      return {
        code: 200,
        message: '删除成功'
      }
    }
    return {
      code: 404,
      message: '记录不存在'
    }
  }
}

*/

// Mock API已经迁移到后端，不再使用
export default {}
