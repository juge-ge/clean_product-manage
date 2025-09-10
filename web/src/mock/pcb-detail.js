// 审核团队mock数据
export const mockAuditTeam = {
  leader: {
    id: 1,
    name: '张专家',
    title: '高级工程师',
    role: 'leader',
    phone: '13800138000',
    email: 'zhang@example.com'
  },
  members: [
    {
      id: 2,
      name: '李工程师',
      title: '环保工程师',
      role: 'member',
      phone: '13800138001',
      email: 'li@example.com'
    },
    {
      id: 3,
      name: '王工程师',
      title: '清洁生产审核师',
      role: 'member',
      phone: '13800138002',
      email: 'wang@example.com'
    }
  ]
}

// 工作计划mock数据
export const mockWorkPlans = [
  {
    id: 1,
    title: '审核准备阶段',
    startDate: '2023-07-01',
    endDate: '2023-07-15',
    status: 'completed',
    tasks: [
      { id: 1, content: '成立审核小组', completed: true },
      { id: 2, content: '制定审核工作计划', completed: true },
      { id: 3, content: '开展动员培训', completed: true }
    ]
  },
  {
    id: 2,
    title: '预审核阶段',
    startDate: '2023-07-16',
    endDate: '2023-07-31',
    status: 'in-progress',
    tasks: [
      { id: 4, content: '收集基础数据', completed: true },
      { id: 5, content: '现场调研', completed: false },
      { id: 6, content: '编制预审核报告', completed: false }
    ]
  }
]

// 预审核数据mock
export const mockPreAuditData = {
  productionData: {
    unitPowerConsumption: 120,    // 单位产品电耗
    wastewaterGeneration: 0.25,   // 废水产生量
    solidWasteGeneration: 0.12,   // 固废产生量
    waterConsumption: 1.5,        // 新鲜水消耗量
    chemicalConsumption: 0.8      // 化学品消耗量
  },
  environmentalData: {
    wastewaterCOD: 80,           // 废水COD浓度
    wastewaterCopper: 0.5,       // 废水铜离子浓度
    airPollutants: 15,           // 大气污染物排放量
    noiseLevel: 65               // 厂界噪声水平
  },
  resourceData: {
    materialUtilization: 85,     // 原材料利用率
    energyEfficiency: 90,        // 能源使用效率
    waterRecycling: 75,          // 水回用率
    wasteRecovery: 80           // 废物回收率
  }
}

// 审核评估结果mock
export const mockAuditResults = {
  overall: {
    totalScore: 85,
    level: 'II级',
    status: '良好',
    date: '2023-07-20'
  },
  categories: [
    {
      name: '生产工艺',
      score: 88,
      level: 'II级',
      items: [
        { name: '工艺先进性', score: 90, comment: '设备自动化程度高' },
        { name: '工艺控制', score: 85, comment: '工艺参数控制稳定' }
      ]
    },
    {
      name: '资源消耗',
      score: 82,
      level: 'II级',
      items: [
        { name: '能源消耗', score: 80, comment: '需进一步优化能源使用效率' },
        { name: '水资源消耗', score: 85, comment: '水循环利用率有待提高' }
      ]
    },
    {
      name: '环境保护',
      score: 86,
      level: 'II级',
      items: [
        { name: '废水处理', score: 88, comment: '处理设施运行良好' },
        { name: '废气处理', score: 85, comment: '收集处理系统完善' }
      ]
    }
  ]
}

// 整改方案mock数据
export const mockSchemes = [
  {
    id: 1,
    title: '电镀生产线节能改造',
    type: '节能降耗',
    description: '通过更换高效整流器、优化电镀参数等措施降低能耗',
    implementation: '1. 更换高效整流器\n2. 优化电镀工艺参数\n3. 安装能耗监测系统',
    expectedEffect: '预计可降低电耗15%，年节约成本50万元',
    investment: 200,
    paybackPeriod: 4,
    status: 'pending'
  },
  {
    id: 2,
    title: '废水处理系统升级',
    type: '污染防治',
    description: '升级改造废水处理系统，提高处理效率和出水水质',
    implementation: '1. 增加预处理单元\n2. 更换高效膜处理设备\n3. 安装在线监测系统',
    expectedEffect: '处理效率提升30%，出水达到更高标准',
    investment: 300,
    paybackPeriod: 5,
    status: 'in-progress'
  }
]

// 审核报告模板mock数据
export const mockReportTemplate = {
  basic: {
    title: '清洁生产审核报告',
    version: '1.0',
    date: new Date().toISOString().split('T')[0]
  },
  sections: [
    {
      title: '1. 企业基本情况',
      content: '包括企业概况、生产工艺、原辅材料消耗等基本信息'
    },
    {
      title: '2. 清洁生产审核',
      content: '包括审核范围、审核过程、审核结果等内容'
    },
    {
      title: '3. 方案分析与实施',
      content: '包括方案识别、方案筛选、方案实施计划等'
    },
    {
      title: '4. 审核结论',
      content: '包括资源节约效果、环境改善效果、经济效益分析等'
    }
  ]
}

// API响应模拟
export const mockDetailApi = {
  // 审核团队相关
  getAuditTeam: (enterpriseId) => {
    return Promise.resolve({ data: mockAuditTeam })
  },
  updateAuditTeam: (enterpriseId, data) => {
    return Promise.resolve({ data: { ...mockAuditTeam, ...data } })
  },

  // 工作计划相关
  getWorkPlans: (enterpriseId) => {
    return Promise.resolve({ data: mockWorkPlans })
  },
  updateWorkPlan: (enterpriseId, planId, data) => {
    const plan = mockWorkPlans.find(p => p.id === planId)
    if (plan) {
      Object.assign(plan, data)
      return Promise.resolve({ data: plan })
    }
    return Promise.reject(new Error('计划不存在'))
  },

  // 预审核数据相关
  getPreAuditData: (enterpriseId) => {
    return Promise.resolve({ data: mockPreAuditData })
  },
  submitPreAuditData: (enterpriseId, data) => {
    return Promise.resolve({ data: { ...mockPreAuditData, ...data } })
  },

  // 审核结果相关
  getAuditResults: (enterpriseId) => {
    return Promise.resolve({ data: mockAuditResults })
  },
  submitAuditResults: (enterpriseId, data) => {
    return Promise.resolve({ data: { ...mockAuditResults, ...data } })
  },

  // 整改方案相关
  getSchemes: (enterpriseId) => {
    return Promise.resolve({ data: mockSchemes })
  },
  createScheme: (enterpriseId, data) => {
    const newScheme = {
      id: mockSchemes.length + 1,
      ...data,
      status: 'pending'
    }
    mockSchemes.push(newScheme)
    return Promise.resolve({ data: newScheme })
  },
  updateScheme: (enterpriseId, schemeId, data) => {
    const scheme = mockSchemes.find(s => s.id === schemeId)
    if (scheme) {
      Object.assign(scheme, data)
      return Promise.resolve({ data: scheme })
    }
    return Promise.reject(new Error('方案不存在'))
  },

  // 报告相关
  getReportTemplate: (enterpriseId) => {
    return Promise.resolve({ data: mockReportTemplate })
  },
  generateReport: (enterpriseId, data) => {
    return Promise.resolve({ 
      data: {
        ...mockReportTemplate,
        content: data
      }
    })
  }
}
