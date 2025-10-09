// PCB企业详情Mock数据

// 完整的64项指标数据
const mockIndicators = [
  // 指标1-6: 生产工艺与装备要求（定性判断）
  { id: 1, name: '基本要求', category: '生产工艺与装备要求', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 2, name: '机械加工及辅助设施', category: '生产工艺与装备要求', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 3, name: '线路与阻焊图形形成(印刷或感光工艺)', category: '生产工艺与装备要求', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 4, name: '板面清洗', category: '生产工艺与装备要求', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 5, name: '蚀刻', category: '生产工艺与装备要求', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 6, name: '电镀与化学镀', category: '生产工艺与装备要求', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  
  // 指标7-14: 能源消耗 - 单位产品电耗（定量计算与自动评估）
  { id: 7, name: '刚性印制电路单面板(单位产品电耗)', category: '能源消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kWh/m²', weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 8, name: '刚性印制电路双面板(单位产品电耗)', category: '能源消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kWh/m²', weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 9, name: '刚性印制电路多层板(2+n)层(单位产品电耗)', category: '能源消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kWh/m²', weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 10, name: '刚性印制电路HDI板(2+n)层(单位产品电耗)', category: '能源消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kWh/m²', weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 11, name: '挠性印制电路单面板(单位产品电耗)', category: '能源消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kWh/m²', weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 12, name: '挠性印制电路双面板(单位产品电耗)', category: '能源消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kWh/m²', weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 13, name: '挠性印制电路多层板(2+n)层(单位产品电耗)', category: '能源消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kWh/m²', weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 14, name: '挠性印制电路HDI板(2+n)层(单位产品电耗)', category: '能源消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kWh/m²', weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  
  // 指标15-19: 水资源消耗（定量计算与自动评估）
  { id: 15, name: '单面板(单位产品新鲜水耗)', category: '水资源消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'm³/m²', weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 16, name: '双面板(单位产品新鲜水耗)', category: '水资源消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'm³/m²', weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 17, name: '多层板(2+n)层(单位产品新鲜水耗)', category: '水资源消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'm³/m²', weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 18, name: 'HDI板(2+n)层(单位产品新鲜水耗)', category: '水资源消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'm³/m²', weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 19, name: '水资源重复利用率', category: '水资源消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  
  // 指标20-27: 原/辅料消耗 - 覆铜板利用率（定量计算与自动评估）
  { id: 20, name: '刚性印制电路单面板 覆铜板利用率', category: '原/辅料消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 21, name: '刚性印制电路双面板 覆铜板利用率', category: '原/辅料消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 22, name: '刚性印制电路多层板(2+n)层覆铜板利用率', category: '原/辅料消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 23, name: '刚性印制电路HDI板(2+n)层覆铜板利用率', category: '原/辅料消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 24, name: '挠性印制电路单面板覆铜板利用率', category: '原/辅料消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 25, name: '挠性印制电路双面板 覆铜板利用率', category: '原/辅料消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 26, name: '挠性性印制电路多层板(2+n)层覆铜板利用率', category: '原/辅料消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 27, name: '挠性印制电路HDI板(2+n)层覆铜板利用率', category: '原/辅料消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  
  // 指标28-29: 资源综合利用（定量自动评估）
  { id: 28, name: '金属铜回收率', category: '资源综合利用', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 29, name: '一般工业固体废物综合利用率', category: '资源综合利用', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  
  // 指标30-41: 废水的产生与排放（定量计算与自动评估）
  { id: 30, name: '单面板废水产生量', category: '废水的产生与排放', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'm³/m²', weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 31, name: '双面板废水产生量', category: '废水的产生与排放', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'm³/m²', weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 32, name: '多层板(2+n)层废水产生量', category: '废水的产生与排放', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'm³/m²', weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 33, name: 'HDI板(2+n)层废水产生量', category: '废水的产生与排放', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'm³/m²', weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 34, name: '单面板废水中铜产生量', category: '废水的产生与排放', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kg/m²', weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 35, name: '双面板废水中铜产生量', category: '废水的产生与排放', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kg/m²', weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 36, name: '多层板(2+n)层废水中铜产生量', category: '废水的产生与排放', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kg/m²', weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 37, name: 'HDI板(2+n)层废水中铜产生量', category: '废水的产生与排放', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kg/m²', weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 38, name: '单面板废水中COD产生量', category: '废水的产生与排放', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kg/m²', weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 39, name: '双面板废水废水中COD产生量', category: '废水的产生与排放', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kg/m²', weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 40, name: '多层板(2+n)层废水中 COD 产生量', category: '废水的产生与排放', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kg/m²', weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 41, name: 'HDI板(2+n)层废水中 COD 产生量', category: '废水的产生与排放', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kg/m²', weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  
  // 指标42: 废水的产生与排放 - 定性指标
  { id: 42, name: '废水收集与处理', category: '废水的产生与排放', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  
  // 指标43: 废气的产生与排放（定性判断）
  { id: 43, name: '废气收集与处理', category: '废气的产生与排放', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  
  // 指标44-45: 固体废物的产生与排放（定性判断）
  { id: 44, name: '一般固体废物收集与处理', category: '固体废物的产生与排放', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 45, name: '危险废物收集与处理', category: '固体废物的产生与排放', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  
  // 指标46: 噪声的产生与排放（定性判断）
  { id: 46, name: '噪声', category: '噪声的产生与排放', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  
  // 指标47-49: 温室气体排放（定性/定量混合评估）
  { id: 47, name: '碳减排管理', category: '温室气体排放', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 48, name: '单位产值碳排放量', category: '温室气体排放', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 49, name: '碳排放强度', category: '温室气体排放', type: 'quantitative', level: null, score: 0, isLimiting: false, weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  
  // 指标50-53: 产品特征（定性判断）
  { id: 50, name: '使用无毒无害或低毒低害的生产辅助材料', category: '产品特征', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 51, name: '包装', category: '产品特征', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 52, name: '有害物质限制使用', category: '产品特征', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 53, name: '产品性能', category: '产品特征', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  
  // 指标54-64: 清洁生产管理（定性/定量/限定性混合评估）
  { id: 54, name: '*环保法律法规执行情况', category: '清洁生产管理', type: 'limiting', level: null, score: 0, isLimiting: true, weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 55, name: '*产业政策符合性', category: '清洁生产管理', type: 'limiting', level: null, score: 0, isLimiting: true, weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 56, name: '清洁生产管理', category: '清洁生产管理', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 57, name: '清洁生产审核', category: '清洁生产管理', type: 'quantitative', level: null, score: 0, isLimiting: false, weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 58, name: '节能管理', category: '清洁生产管理', type: 'quantitative', level: null, score: 0, isLimiting: false, weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 59, name: '污染物排放监测', category: '清洁生产管理', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 60, name: '*危险化学品管理', category: '清洁生产管理', type: 'limiting', level: null, score: 0, isLimiting: true, weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 61, name: '计量器具配备情况', category: '清洁生产管理', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 62, name: '*固体废物处理处置', category: '清洁生产管理', type: 'limiting', level: null, score: 0, isLimiting: true, weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 63, name: '土壤污染隐患排查', category: '清洁生产管理', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 64, name: '运输方式', category: '清洁生产管理', type: 'quantitative', level: null, score: 0, isLimiting: false, weight: 1.0, currentValue: null, recommendedSchemes: [], selectedSchemes: [] }
]

// 推荐方案获取函数 - 直接从方案库中获取
const getRecommendedSchemes = (indicatorId) => {
  // 直接从方案库中筛选对应指标的方案
  const recommendedSchemes = mockSchemeLibrary.filter(scheme => 
    scheme.indicatorIds && scheme.indicatorIds.includes(parseInt(indicatorId))
  );
  
  // 按方案序号排序（1-130）
  const sortedSchemes = recommendedSchemes.sort((a, b) => a.id - b.id);
  
  // 返回格式化的方案数据
  return sortedSchemes.map(scheme => ({
    value: scheme.id,
    label: `方案${scheme.id}：${scheme.name}`,
    preview: {
      type: scheme.type,
      description: scheme.description,
      problemSolved: scheme.problemSolved,
      economicBenefit: scheme.economicBenefit,
      environmentalBenefit: scheme.environmentalBenefit,
      investment: scheme.investment,
      paybackPeriod: scheme.paybackPeriod,
      indicatorNames: scheme.indicatorNames
    }
  }));
}

// 筹划与组织Mock数据
const mockPlanningData = {
  auditTeam: [
    {
      id: 1,
      name: '张三',
      position: '审核组长',
      department: '环保部',
      phone: '13800138001',
      email: 'zhangsan@example.com',
      role: '组长'
    },
    {
      id: 2,
      name: '李四',
      position: '技术专家',
      department: '技术部',
      phone: '13800138002',
      email: 'lisi@example.com',
      role: '专家'
    },
    {
      id: 3,
      name: '王五',
      position: '审核员',
      department: '环保部',
      phone: '13800138003',
      email: 'wangwu@example.com',
      role: '审核员'
    }
  ],
  workPlans: [
    {
      id: 1,
      title: '审核准备阶段',
      description: '收集企业基础资料，组建审核团队',
      startDate: '2024-01-01',
      endDate: '2024-01-15',
      status: 'completed',
      progress: 100
    },
    {
      id: 2,
      title: '预审核阶段',
      description: '数据收集与初步评估',
      startDate: '2024-01-16',
      endDate: '2024-02-15',
      status: 'in-progress',
      progress: 80
    },
    {
      id: 3,
      title: '正式审核阶段',
      description: '现场审核与指标评估',
      startDate: '2024-02-16',
      endDate: '2024-03-15',
      status: 'pending',
      progress: 0
    },
    {
      id: 4,
      title: '报告编制阶段',
      description: '审核报告编制与方案制定',
      startDate: '2024-03-16',
      endDate: '2024-04-15',
      status: 'pending',
      progress: 0
    }
  ],
  trainingRecords: [
    {
      id: 1,
      title: '清洁生产审核培训',
      date: '2024-01-10',
      participants: 15,
      duration: 8,
      content: '清洁生产审核基础知识培训',
      instructor: '环保专家'
    },
    {
      id: 2,
      title: 'PCB行业标准培训',
      date: '2024-01-20',
      participants: 12,
      duration: 6,
      content: 'PCB行业清洁生产评价指标体系培训',
      instructor: '行业专家'
    }
  ]
}

// 方案库Mock数据 - 基于PCB清洁生产方案.md的130项方案
const mockSchemeLibrary = [
  {
    id: 1,
    name: '废水处理系统升级改造',
    type: '环保治理',
    problemSolved: 'PCB废水处理系统长期运行导致处理效率下降，设备老化、处理成本高、出水不稳定，同时废水回用率低，处理负荷大',
    description: '更换老旧提升泵、潜水泵、电机和搅拌机等设备，改进废水处理工艺采用二级厌氧+二级好氧处理系统，在污泥压滤区增设空压机曝气设备降低污泥含水率，更换中水回用系统滤料和渗透膜，完善废气收集系统',
    economicBenefit: '每万平方米线路板节约新鲜水费用0.8万元，减少废水处理成本2.5万元，污泥处置成本降低0.6万元',
    environmentalBenefit: '每万平方米线路板减少废水排放850吨，COD减排0.09吨，总铜减排0.001吨，污泥减量1.4吨',
    indicatorIds: [30, 34, 38, 42, 59, 62],
    indicatorNames: ['废水产生量', '废水中铜产生量', '废水中COD产生量', '废水收集与处理', '污染物排放监测', '固体废物处理处置'],
    investment: 150,
    paybackPeriod: 2.5,
    status: 'active',
    createdAt: '2024-01-15'
  },
  {
    id: 2,
    name: '废水分类收集与防泄漏系统改造',
    type: '环保治理',
    problemSolved: 'PCB生产过程中各类废水收集混乱、跑冒滴漏严重，设施不完善，导致废水处理难度增加，存在环境风险隐患',
    description: '对酸碱废水、含铜废水、有机废水分别安装PVC硬管收集系统，在湿法加工区设备下方安装防泄漏托盘并配套应急排水系统，完善地面防腐防渗处理，建立管道标识系统和日常巡检制度',
    economicBenefit: '每万平方米线路板可降低废水处理成本1.2万元，减少原材料流失约0.5万元',
    environmentalBenefit: '提高废水分质处理效率20%，降低废水站处理负荷25%，减少地面污染风险90%',
    indicatorIds: [30, 34, 38, 42, 59, 62, 63],
    indicatorNames: ['废水产生量', '废水中铜产生量', '废水中COD产生量', '废水收集与处理', '污染物排放监测', '固体废物处理处置', '土壤污染隐患排查'],
    investment: 80,
    paybackPeriod: 2.0,
    status: 'active',
    createdAt: '2024-01-20'
  },
  {
    id: 3,
    name: '镀铜生产线智能化改造',
    type: '技术改造',
    problemSolved: '传统镀铜线人工操作随意性大，设备自动化程度低，物料损耗大、废水产生量高、产品质量不稳定',
    description: '引进垂直连续电镀(VCP)设备替代传统龙门式镀铜线，配置智能化控制系统实现温度、电流密度、药液浓度自动调节，安装机械手自动上下板系统，配套镀液回收装置及过滤系统',
    economicBenefit: '每万平方米线路板节约原材料成本3.5万元，减少人工成本1.2万元，提高产品良率8%',
    environmentalBenefit: '每万平方米线路板减少废水产生100吨，铜材利用率提升15%，减少危废产生0.2吨',
    indicatorIds: [1, 6, 7, 9, 12, 20, 28, 30, 34, 38, 43],
    indicatorNames: ['生产工艺与装备', '电镀与化学镀', '单位产品能耗', '自动化水平', '覆铜板利用率', '金属铜回收率', '废水产生量', '废水中铜', '废水中COD', '废气收集与处理'],
    investment: 200,
    paybackPeriod: 3.0,
    status: 'active',
    createdAt: '2024-01-25'
  },
  {
    id: 4,
    name: '有机废气收集处理系统优化',
    type: '环保治理',
    problemSolved: '生产过程中有机废气收集效率低，处理设施运行不稳定，导致车间空气质量差，废气处理效果不理想',
    description: '优化废气集气罩设计并增设软帘，配置大功率防腐风机，采用水喷淋+二级活性炭吸附工艺，选用碘值800活性炭，配套除雾装置，增设VOCs在线监测系统',
    economicBenefit: '每万平方米线路板节约活性炭使用成本0.3万元，降低能耗0.4万元，减少维护成本0.2万元',
    environmentalBenefit: '有机废气收集效率提升至90%，处理效率达85%，VOCs排放浓度降低40%',
    indicatorIds: [43, 59],
    indicatorNames: ['废气收集与处理', '污染物排放监测'],
    investment: 120,
    paybackPeriod: 2.8,
    status: 'active',
    createdAt: '2024-02-01'
  },
  {
    id: 5,
    name: '蚀刻线设备更新改造',
    type: '技术改造',
    problemSolved: '原有蚀刻线设备老化严重，自动化水平低，能耗高，蚀刻液利用率低，废液产生量大',
    description: '引进全自动蚀刻线设备，配置无板自动停机、压力保护、卡板报警等智能系统，安装变频调速装置和自动加药系统，配套蚀刻液在线分析和自动补给装置，增设废液减量化处理单元',
    economicBenefit: '每万平方米线路板节约蚀刻液成本2.8万元，减少能耗成本0.9万元，降低人工成本0.6万元',
    environmentalBenefit: '每万平方米线路板减少蚀刻废液产生量0.8吨，节约用水量120吨',
    indicatorIds: [1, 5, 7, 9, 12, 20, 28, 30, 34, 38],
    indicatorNames: ['生产工艺与装备', '蚀刻', '单位能耗', '自动化水平', '覆铜板利用率', '金属铜回收率', '废水及成分'],
    investment: 180,
    paybackPeriod: 2.5,
    status: 'active',
    createdAt: '2024-02-05'
  },
  {
    id: 6,
    name: '阻焊工序自动化改造',
    type: '技术改造',
    problemSolved: '阻焊工序人工操作多，自动化程度低，阻焊油墨浪费严重，生产效率低，产品质量不稳定',
    description: '引进全自动阻焊印刷机，配置自动对位系统、自动清洗装置和油墨回收系统，安装阻焊固化炉自动控制系统，配套阻焊前处理自动线，增设阻焊质量在线检测设备',
    economicBenefit: '每万平方米线路板节约阻焊油墨成本1.5万元，减少人工成本0.8万元，提高生产效率25%',
    environmentalBenefit: '每万平方米线路板减少阻焊油墨浪费20%，减少清洗废水产生量50吨',
    indicatorIds: [1, 3, 7, 9, 12, 20, 30, 38],
    indicatorNames: ['生产工艺与装备', '线路与阻焊图形形成', '单位能耗', '自动化水平', '覆铜板利用率', '废水产生量', '废水中COD'],
    investment: 160,
    paybackPeriod: 2.8,
    status: 'active',
    createdAt: '2024-02-10'
  },
  {
    id: 7,
    name: '钻孔工序设备升级改造',
    type: '技术改造',
    problemSolved: '钻孔设备精度低，钻头损耗大，钻孔质量不稳定，生产效率低，能耗高',
    description: '引进高精度数控钻孔机，配置自动换刀系统和钻头寿命管理系统，安装钻孔质量在线检测设备，配套钻屑收集和回收系统，增设钻孔参数自动优化系统',
    economicBenefit: '每万平方米线路板节约钻头成本2.0万元，减少能耗成本0.6万元，提高钻孔精度15%',
    environmentalBenefit: '每万平方米线路板减少钻头浪费30%，减少钻屑产生量0.5吨',
    indicatorIds: [1, 2, 7, 9, 12, 20, 28, 30],
    indicatorNames: ['生产工艺与装备', '机械加工及辅助设施', '单位能耗', '自动化水平', '覆铜板利用率', '金属铜回收率', '废水产生量'],
    investment: 140,
    paybackPeriod: 2.2,
    status: 'active',
    createdAt: '2024-02-15'
  },
  {
    id: 8,
    name: '表面处理工序优化改造',
    type: '技术改造',
    problemSolved: '表面处理工序工艺落后，化学药品消耗量大，废水产生量高，处理效果不理想',
    description: '优化表面处理工艺，采用低浓度化学药品配方，配置自动加药系统和浓度在线监测设备，安装表面处理废液回收装置，增设表面处理质量自动检测系统',
    economicBenefit: '每万平方米线路板节约化学药品成本1.8万元，减少废水处理成本0.7万元',
    environmentalBenefit: '每万平方米线路板减少化学药品消耗25%，减少废水产生量80吨',
    indicatorIds: [1, 4, 7, 9, 20, 30, 34, 38],
    indicatorNames: ['生产工艺与装备', '板面清洗', '单位能耗', '覆铜板利用率', '废水产生量', '废水中铜', '废水中COD'],
    investment: 100,
    paybackPeriod: 2.0,
    status: 'active',
    createdAt: '2024-02-20'
  },
  {
    id: 9,
    name: '压合工序设备升级改造',
    type: '技术改造',
    problemSolved: '压合设备老化，压合质量不稳定，能耗高，生产效率低，废品率高',
    description: '引进高精度压合机，配置自动上料系统和温度压力自动控制系统，安装压合质量在线检测设备，配套压合废料回收系统，增设压合参数自动优化系统',
    economicBenefit: '每万平方米线路板节约原材料成本2.2万元，减少能耗成本0.8万元，提高产品良率10%',
    environmentalBenefit: '每万平方米线路板减少废品率20%，减少废料产生量0.3吨',
    indicatorIds: [1, 2, 7, 9, 12, 20, 28],
    indicatorNames: ['生产工艺与装备', '机械加工及辅助设施', '单位能耗', '自动化水平', '覆铜板利用率', '金属铜回收率'],
    investment: 180,
    paybackPeriod: 2.5,
    status: 'active',
    createdAt: '2024-02-25'
  },
  {
    id: 10,
    name: '测试工序自动化改造',
    type: '技术改造',
    problemSolved: '测试工序人工操作多，测试效率低，测试设备精度不高，测试数据管理混乱',
    description: '引进自动化测试设备，配置自动上下料系统和测试数据自动记录系统，安装测试结果自动分析设备，配套测试废料自动分类收集系统，增设测试质量追溯系统',
    economicBenefit: '每万平方米线路板节约人工成本1.0万元，提高测试效率30%，减少测试废品率15%',
    environmentalBenefit: '每万平方米线路板减少测试废料产生量0.2吨，提高测试数据准确性',
    indicatorIds: [1, 2, 7, 9, 12, 20, 28],
    indicatorNames: ['生产工艺与装备', '机械加工及辅助设施', '单位能耗', '自动化水平', '覆铜板利用率', '金属铜回收率'],
    investment: 120,
    paybackPeriod: 2.0,
    status: 'active',
    createdAt: '2024-03-01'
  },
  {
    id: 11,
    name: '能源管理系统建设',
    type: '管理改进',
    problemSolved: '企业能源管理粗放，缺乏系统性的能源监测和管理体系，能源消耗数据不准确，节能潜力挖掘不足',
    description: '建立企业能源管理中心，安装能源在线监测系统，配置分项计量设备，建立能源管理数据库，制定能源管理制度和考核体系，开展能源审计和节能诊断',
    economicBenefit: '每万平方米线路板节约电费成本1.5万元，提高能源利用效率15%',
    environmentalBenefit: '每万平方米线路板减少电力消耗10%，减少CO2排放约2吨',
    indicatorIds: [7, 8, 9, 10, 11, 12, 13, 14, 47, 58],
    indicatorNames: ['单位产品电耗', '温室气体排放', '节能管理'],
    investment: 80,
    paybackPeriod: 1.8,
    status: 'active',
    createdAt: '2024-03-05'
  },
  {
    id: 12,
    name: '水资源循环利用系统',
    type: '资源节约',
    problemSolved: '企业水资源利用效率低，废水回用率不高，新鲜水消耗量大，水资源浪费严重',
    description: '建设废水深度处理回用系统，配置反渗透、超滤等先进处理设备，建立中水回用管网，安装用水计量设备，制定水资源管理制度，开展水平衡测试',
    economicBenefit: '每万平方米线路板节约新鲜水费用1.2万元，减少废水处理成本0.8万元',
    environmentalBenefit: '每万平方米线路板减少新鲜水消耗20%，提高废水回用率至60%',
    indicatorIds: [15, 16, 17, 18, 19, 30, 31, 32, 33],
    indicatorNames: ['单位产品新鲜水耗', '水资源重复利用率', '废水产生量'],
    investment: 200,
    paybackPeriod: 3.0,
    status: 'active',
    createdAt: '2024-03-10'
  },
  {
    id: 13,
    name: '原材料优化管理',
    type: '管理改进',
    problemSolved: '原材料管理不规范，库存积压严重，原材料利用率不高，浪费现象普遍',
    description: '建立原材料管理系统，实施JIT采购模式，优化原材料库存结构，建立原材料使用台账，制定原材料消耗定额，开展原材料利用率分析',
    economicBenefit: '每万平方米线路板节约原材料成本2.5万元，减少库存积压资金30%',
    environmentalBenefit: '每万平方米线路板提高原材料利用率8%，减少原材料浪费15%',
    indicatorIds: [20, 21, 22, 23, 24, 25, 26, 27, 28],
    indicatorNames: ['覆铜板利用率', '金属铜回收率'],
    investment: 60,
    paybackPeriod: 1.5,
    status: 'active',
    createdAt: '2024-03-15'
  },
  {
    id: 14,
    name: '固体废物分类收集系统',
    type: '环保治理',
    problemSolved: '固体废物分类收集不规范，危险废物和一般废物混合存放，废物处置成本高，存在环境风险',
    description: '建立固体废物分类收集系统，设置分类收集容器和标识，建立废物暂存库，制定废物管理制度，建立废物处置台账，开展废物减量化研究',
    economicBenefit: '每万平方米线路板节约废物处置成本0.8万元，提高废物回收价值0.5万元',
    environmentalBenefit: '每万平方米线路板提高废物分类收集率至95%，减少危险废物产生量20%',
    indicatorIds: [29, 44, 45, 62],
    indicatorNames: ['一般工业固体废物综合利用率', '一般固体废物收集与处理', '危险废物收集与处理', '固体废物管理'],
    investment: 50,
    paybackPeriod: 1.2,
    status: 'active',
    createdAt: '2024-03-20'
  },
  {
    id: 15,
    name: '噪声治理工程',
    type: '环保治理',
    problemSolved: '生产设备噪声超标，影响员工健康和周边环境，噪声治理设施不完善',
    description: '对高噪声设备进行隔声降噪处理，安装消声器、隔声罩等降噪设施，建立噪声监测系统，制定噪声管理制度，开展噪声源识别和治理',
    economicBenefit: '每万平方米线路板减少噪声投诉处理成本0.3万元，提高员工满意度',
    environmentalBenefit: '每万平方米线路板降低厂界噪声5dB(A)，改善工作环境',
    indicatorIds: [46],
    indicatorNames: ['噪声'],
    investment: 40,
    paybackPeriod: 2.5,
    status: 'active',
    createdAt: '2024-03-25'
  },
  {
    id: 16,
    name: '清洁生产审核体系建设',
    type: '管理改进',
    problemSolved: '企业缺乏系统性的清洁生产管理体系，清洁生产审核工作不规范，持续改进机制不完善',
    description: '建立清洁生产审核领导小组，制定清洁生产审核计划，开展清洁生产培训，建立清洁生产管理制度，制定清洁生产目标指标，建立清洁生产考核体系',
    economicBenefit: '每万平方米线路板通过清洁生产审核节约成本5万元，提高管理效率20%',
    environmentalBenefit: '每万平方米线路板减少污染物排放15%，提高资源利用效率10%',
    indicatorIds: [54, 57],
    indicatorNames: ['环保法律法规执行情况', '清洁生产审核'],
    investment: 30,
    paybackPeriod: 1.0,
    status: 'active',
    createdAt: '2024-03-30'
  },
  {
    id: 17,
    name: '危险化学品管理系统',
    type: '管理改进',
    problemSolved: '危险化学品管理不规范，存储和使用存在安全隐患，化学品泄漏风险高，管理成本高',
    description: '建立危险化学品管理系统，设置专用存储区域，安装泄漏监测设备，制定化学品管理制度，建立化学品使用台账，开展化学品安全培训',
    economicBenefit: '每万平方米线路板节约化学品管理成本0.5万元，减少安全事故处理成本1万元',
    environmentalBenefit: '每万平方米线路板减少化学品泄漏风险90%，提高化学品使用效率15%',
    indicatorIds: [60],
    indicatorNames: ['危险化学品管理'],
    investment: 70,
    paybackPeriod: 2.0,
    status: 'active',
    createdAt: '2024-04-01'
  },
  {
    id: 18,
    name: '运输方式优化改造',
    type: '管理改进',
    problemSolved: '企业运输方式落后，运输效率低，运输成本高，运输过程中存在环境污染风险',
    description: '优化运输路线，采用清洁能源运输车辆，建立运输管理系统，制定运输管理制度，开展运输人员培训，建立运输成本核算体系',
    economicBenefit: '每万平方米线路板节约运输成本0.8万元，提高运输效率25%',
    environmentalBenefit: '每万平方米线路板减少运输过程中的污染物排放30%，降低运输能耗20%',
    indicatorIds: [64],
    indicatorNames: ['运输方式'],
    investment: 50,
    paybackPeriod: 1.8,
    status: 'active',
    createdAt: '2024-04-05'
  },
  {
    id: 19,
    name: '产品特征优化改进',
    type: '技术改造',
    problemSolved: '产品设计不合理，产品特征不符合清洁生产要求，产品生命周期环境影响大',
    description: '优化产品设计，采用环保材料，改进产品结构，提高产品性能，延长产品使用寿命，建立产品生命周期评价体系',
    economicBenefit: '每万平方米线路板提高产品附加值10%，减少产品返工率5%',
    environmentalBenefit: '每万平方米线路板减少产品生命周期环境影响20%，提高产品回收利用率15%',
    indicatorIds: [50],
    indicatorNames: ['产品特征'],
    investment: 100,
    paybackPeriod: 2.5,
    status: 'active',
    createdAt: '2024-04-10'
  },
  {
    id: 20,
    name: '污染物排放监测系统',
    type: '环保治理',
    problemSolved: '污染物排放监测不完善，监测数据不准确，缺乏实时监测能力，环境风险管控不足',
    description: '建立污染物排放在线监测系统，安装水质、大气、噪声等监测设备，建立监测数据管理系统，制定监测管理制度，开展监测人员培训',
    economicBenefit: '每万平方米线路板节约监测成本0.3万元，提高环境管理效率30%',
    environmentalBenefit: '每万平方米线路板实现污染物排放实时监控，提高环境风险管控能力',
    indicatorIds: [59],
    indicatorNames: ['污染物排放监测'],
    investment: 90,
    paybackPeriod: 3.0,
    status: 'active',
    createdAt: '2024-04-15'
  },
  {
    id: 21,
    name: '土壤污染隐患排查治理',
    type: '环保治理',
    problemSolved: '企业存在土壤污染隐患，缺乏系统性的土壤污染排查和治理措施，环境风险较高',
    description: '开展土壤污染隐患排查，建立土壤污染监测系统，制定土壤污染治理方案，建立土壤污染管理制度，开展土壤污染治理工程',
    economicBenefit: '每万平方米线路板减少土壤污染治理成本2万元，降低环境风险',
    environmentalBenefit: '每万平方米线路板消除土壤污染隐患，保护土壤环境质量',
    indicatorIds: [63],
    indicatorNames: ['土壤污染隐患排查'],
    investment: 150,
    paybackPeriod: 4.0,
    status: 'active',
    createdAt: '2024-04-20'
  },
  {
    id: 22,
    name: '生产线自动化升级改造',
    type: '技术改造',
    problemSolved: '生产线自动化程度低，人工操作多，生产效率低，产品质量不稳定，能耗高',
    description: '引进自动化生产线设备，配置机器人自动上下料系统，安装生产线自动控制系统，建立生产线数据采集系统，增设生产线质量检测设备',
    economicBenefit: '每万平方米线路板节约人工成本3万元，提高生产效率40%，减少废品率20%',
    environmentalBenefit: '每万平方米线路板减少人工操作误差，提高产品质量，减少资源浪费',
    indicatorIds: [1, 2, 7, 9, 12, 20, 28],
    indicatorNames: ['生产工艺与装备', '机械加工及辅助设施', '单位能耗', '自动化水平', '覆铜板利用率', '金属铜回收率'],
    investment: 300,
    paybackPeriod: 3.5,
    status: 'active',
    createdAt: '2024-04-25'
  },
  {
    id: 23,
    name: '化学药品管理系统优化',
    type: '管理改进',
    problemSolved: '化学药品管理不规范，药品浪费严重，存储条件不符合要求，存在安全隐患',
    description: '建立化学药品管理系统，优化药品存储条件，建立药品使用台账，制定药品管理制度，开展药品安全培训，建立药品回收利用系统',
    economicBenefit: '每万平方米线路板节约化学药品成本1.5万元，减少药品浪费30%',
    environmentalBenefit: '每万平方米线路板减少化学药品浪费，降低环境风险',
    indicatorIds: [60],
    indicatorNames: ['危险化学品管理'],
    investment: 80,
    paybackPeriod: 2.0,
    status: 'active',
    createdAt: '2024-04-30'
  },
  {
    id: 24,
    name: '废料回收利用系统',
    type: '资源回收',
    problemSolved: '生产过程中产生的废料回收利用率低，废料处理成本高，资源浪费严重',
    description: '建立废料分类回收系统，配置废料处理设备，建立废料回收利用工艺，制定废料管理制度，建立废料回收台账',
    economicBenefit: '每万平方米线路板通过废料回收节约成本2万元，减少废料处理成本1万元',
    environmentalBenefit: '每万平方米线路板提高废料回收利用率至80%，减少废料产生量30%',
    indicatorIds: [28, 29, 44, 45],
    indicatorNames: ['金属铜回收率', '一般工业固体废物综合利用率', '一般固体废物收集与处理', '危险废物收集与处理'],
    investment: 120,
    paybackPeriod: 2.5,
    status: 'active',
    createdAt: '2024-05-01'
  },
  {
    id: 25,
    name: '生产设备维护保养系统',
    type: '管理改进',
    problemSolved: '生产设备维护保养不及时，设备故障率高，设备运行效率低，维护成本高',
    description: '建立设备维护保养系统，制定设备维护计划，建立设备维护台账，配置设备监测系统，开展设备维护培训',
    economicBenefit: '每万平方米线路板节约设备维护成本1万元，减少设备故障停机时间50%',
    environmentalBenefit: '每万平方米线路板提高设备运行效率，减少设备故障对环境的影响',
    indicatorIds: [1, 2, 7, 9],
    indicatorNames: ['生产工艺与装备', '机械加工及辅助设施', '单位能耗'],
    investment: 60,
    paybackPeriod: 1.5,
    status: 'active',
    createdAt: '2024-05-05'
  },
  {
    id: 26,
    name: '废水处理工艺优化',
    type: '环保治理',
    problemSolved: '废水处理工艺落后，处理效率低，处理成本高，出水水质不稳定',
    description: '优化废水处理工艺，采用先进的生物处理技术，配置自动加药系统，建立处理效果监测系统，优化处理参数',
    economicBenefit: '每万平方米线路板节约废水处理成本1.5万元，提高处理效率20%',
    environmentalBenefit: '每万平方米线路板提高废水处理效率，减少污染物排放',
    indicatorIds: [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42],
    indicatorNames: ['废水产生量', '废水中铜产生量', '废水中COD产生量', '废水收集与处理'],
    investment: 180,
    paybackPeriod: 3.0,
    status: 'active',
    createdAt: '2024-05-10'
  },
  {
    id: 27,
    name: '废气处理设备升级',
    type: '环保治理',
    problemSolved: '废气处理设备老化，处理效率低，运行成本高，废气排放不达标',
    description: '升级废气处理设备，采用先进的废气处理工艺，配置自动控制系统，建立废气监测系统，优化处理参数',
    economicBenefit: '每万平方米线路板节约废气处理成本1万元，提高处理效率25%',
    environmentalBenefit: '每万平方米线路板提高废气处理效率，减少大气污染物排放',
    indicatorIds: [43],
    indicatorNames: ['废气收集与处理'],
    investment: 150,
    paybackPeriod: 3.5,
    status: 'active',
    createdAt: '2024-05-15'
  },
  {
    id: 28,
    name: '固体废物减量化处理',
    type: '环保治理',
    problemSolved: '固体废物产生量大，处理成本高，废物减量化程度低，资源化利用不足',
    description: '建立固体废物减量化处理系统，优化生产工艺减少废物产生，建立废物分类处理系统，开展废物资源化利用',
    economicBenefit: '每万平方米线路板节约废物处理成本1.2万元，通过废物资源化利用增加收益0.8万元',
    environmentalBenefit: '每万平方米线路板减少固体废物产生量25%，提高废物资源化利用率',
    indicatorIds: [29, 44, 45],
    indicatorNames: ['一般工业固体废物综合利用率', '一般固体废物收集与处理', '危险废物收集与处理'],
    investment: 100,
    paybackPeriod: 2.5,
    status: 'active',
    createdAt: '2024-05-20'
  },
  {
    id: 29,
    name: '能源消耗优化管理',
    type: '管理改进',
    problemSolved: '能源消耗管理粗放，能耗数据不准确，节能潜力挖掘不足，能源利用效率低',
    description: '建立能源消耗管理系统，安装能源监测设备，建立能耗数据库，制定节能管理制度，开展节能技术改造',
    economicBenefit: '每万平方米线路板节约能源成本2万元，提高能源利用效率15%',
    environmentalBenefit: '每万平方米线路板减少能源消耗，降低温室气体排放',
    indicatorIds: [7, 8, 9, 10, 11, 12, 13, 14, 47, 58],
    indicatorNames: ['单位产品电耗', '温室气体排放', '节能管理'],
    investment: 120,
    paybackPeriod: 2.0,
    status: 'active',
    createdAt: '2024-05-25'
  },
  {
    id: 30,
    name: '水资源利用优化',
    type: '资源节约',
    problemSolved: '水资源利用效率低，新鲜水消耗量大，废水回用率不高，水资源浪费严重',
    description: '优化水资源利用系统，建立水资源监测系统，提高废水回用率，优化用水工艺，建立水资源管理制度',
    economicBenefit: '每万平方米线路板节约水资源成本1.5万元，提高水资源利用效率20%',
    environmentalBenefit: '每万平方米线路板减少新鲜水消耗，提高废水回用率',
    indicatorIds: [15, 16, 17, 18, 19, 30, 31, 32, 33],
    indicatorNames: ['单位产品新鲜水耗', '水资源重复利用率', '废水产生量'],
    investment: 160,
    paybackPeriod: 2.8,
    status: 'active',
    createdAt: '2024-05-30'
  },
  {
    id: 31,
    name: '原材料利用率提升',
    type: '资源节约',
    problemSolved: '原材料利用率不高，原材料浪费严重，原材料成本高，资源利用效率低',
    description: '优化原材料使用工艺，建立原材料利用率监测系统，制定原材料使用标准，开展原材料利用率分析，建立原材料回收利用系统',
    economicBenefit: '每万平方米线路板节约原材料成本2.5万元，提高原材料利用率15%',
    environmentalBenefit: '每万平方米线路板减少原材料浪费，提高资源利用效率',
    indicatorIds: [20, 21, 22, 23, 24, 25, 26, 27, 28],
    indicatorNames: ['覆铜板利用率', '金属铜回收率'],
    investment: 80,
    paybackPeriod: 1.8,
    status: 'active',
    createdAt: '2024-06-01'
  },
  {
    id: 32,
    name: '生产工艺优化改进',
    type: '技术改造',
    problemSolved: '生产工艺落后，生产效率低，产品质量不稳定，能耗高，环境污染严重',
    description: '优化生产工艺流程，采用先进的生产工艺，改进生产设备，建立生产工艺监测系统，制定生产工艺标准',
    economicBenefit: '每万平方米线路板节约生产成本3万元，提高生产效率25%，提高产品质量',
    environmentalBenefit: '每万平方米线路板减少环境污染，提高资源利用效率',
    indicatorIds: [1, 2, 3, 4, 5, 6, 7, 9, 12, 20, 28, 30, 34, 38, 43],
    indicatorNames: ['生产工艺与装备', '机械加工及辅助设施', '线路与阻焊图形形成', '板面清洗', '蚀刻', '电镀与化学镀', '单位能耗', '自动化水平', '覆铜板利用率', '金属铜回收率', '废水产生量', '废水中铜', '废水中COD', '废气收集与处理'],
    investment: 250,
    paybackPeriod: 3.2,
    status: 'active',
    createdAt: '2024-06-05'
  },
  {
    id: 33,
    name: '环保设施运行优化',
    type: '环保治理',
    problemSolved: '环保设施运行效率低，运行成本高，设施维护不及时，环保效果不理想',
    description: '优化环保设施运行参数，建立环保设施监测系统，制定环保设施维护计划，开展环保设施运行培训，建立环保设施管理制度',
    economicBenefit: '每万平方米线路板节约环保设施运行成本1.8万元，提高环保设施运行效率20%',
    environmentalBenefit: '每万平方米线路板提高环保设施运行效果，减少污染物排放',
    indicatorIds: [30, 34, 38, 42, 43, 44, 45, 46, 59],
    indicatorNames: ['废水产生量', '废水中铜产生量', '废水中COD产生量', '废水收集与处理', '废气收集与处理', '一般固体废物收集与处理', '危险废物收集与处理', '噪声', '污染物排放监测'],
    investment: 140,
    paybackPeriod: 2.8,
    status: 'active',
    createdAt: '2024-06-10'
  },
  {
    id: 34,
    name: '清洁生产管理体系',
    type: '管理改进',
    problemSolved: '清洁生产管理体系不完善，清洁生产工作不规范，持续改进机制不健全',
    description: '建立清洁生产管理体系，制定清洁生产管理制度，建立清洁生产目标指标，开展清洁生产培训，建立清洁生产考核体系',
    economicBenefit: '每万平方米线路板通过清洁生产管理节约成本4万元，提高管理效率30%',
    environmentalBenefit: '每万平方米线路板减少污染物排放20%，提高资源利用效率15%',
    indicatorIds: [54, 57, 58, 60, 62, 64],
    indicatorNames: ['环保法律法规执行情况', '清洁生产审核', '节能管理', '危险化学品管理', '固体废物管理', '运输方式'],
    investment: 50,
    paybackPeriod: 1.2,
    status: 'active',
    createdAt: '2024-06-15'
  },
  {
    id: 35,
    name: '产品质量提升改进',
    type: '技术改造',
    problemSolved: '产品质量不稳定，产品合格率不高，产品返工率高，产品质量管理不规范',
    description: '优化产品质量管理体系，建立产品质量监测系统，制定产品质量标准，开展产品质量培训，建立产品质量追溯系统',
    economicBenefit: '每万平方米线路板提高产品合格率10%，减少产品返工成本1.5万元',
    environmentalBenefit: '每万平方米线路板减少产品返工，降低资源浪费',
    indicatorIds: [50],
    indicatorNames: ['产品特征'],
    investment: 90,
    paybackPeriod: 2.0,
    status: 'active',
    createdAt: '2024-06-20'
  },
  {
    id: 36,
    name: '生产线智能化改造',
    type: '技术改造',
    problemSolved: '生产线智能化程度低，人工操作多，生产效率低，产品质量不稳定，能耗高',
    description: '引进智能化生产线设备，配置工业机器人，安装智能控制系统，建立生产线数据采集系统，增设智能质量检测设备',
    economicBenefit: '每万平方米线路板节约人工成本4万元，提高生产效率50%，减少废品率25%',
    environmentalBenefit: '每万平方米线路板减少人工操作误差，提高产品质量，减少资源浪费',
    indicatorIds: [1, 2, 7, 9, 12, 20, 28],
    indicatorNames: ['生产工艺与装备', '机械加工及辅助设施', '单位能耗', '自动化水平', '覆铜板利用率', '金属铜回收率'],
    investment: 400,
    paybackPeriod: 4.0,
    status: 'active',
    createdAt: '2024-06-25'
  },
  {
    id: 37,
    name: '废水深度处理回用系统',
    type: '环保治理',
    problemSolved: '废水深度处理不足，废水回用率低，新鲜水消耗量大，水资源浪费严重',
    description: '建设废水深度处理回用系统，配置反渗透、超滤等先进处理设备，建立中水回用管网，安装用水计量设备，制定水资源管理制度',
    economicBenefit: '每万平方米线路板节约新鲜水费用2万元，减少废水处理成本1.5万元',
    environmentalBenefit: '每万平方米线路板减少新鲜水消耗30%，提高废水回用率至70%',
    indicatorIds: [15, 16, 17, 18, 19, 30, 31, 32, 33],
    indicatorNames: ['单位产品新鲜水耗', '水资源重复利用率', '废水产生量'],
    investment: 250,
    paybackPeriod: 3.5,
    status: 'active',
    createdAt: '2024-06-30'
  },
  {
    id: 38,
    name: '废气处理工艺优化',
    type: '环保治理',
    problemSolved: '废气处理工艺落后，处理效率低，运行成本高，废气排放不达标',
    description: '优化废气处理工艺，采用先进的废气处理技术，配置自动控制系统，建立废气监测系统，优化处理参数',
    economicBenefit: '每万平方米线路板节约废气处理成本1.5万元，提高处理效率30%',
    environmentalBenefit: '每万平方米线路板提高废气处理效率，减少大气污染物排放',
    indicatorIds: [43],
    indicatorNames: ['废气收集与处理'],
    investment: 180,
    paybackPeriod: 3.8,
    status: 'active',
    createdAt: '2024-07-01'
  },
  {
    id: 39,
    name: '固体废物资源化利用',
    type: '资源回收',
    problemSolved: '固体废物资源化利用程度低，废物处理成本高，资源浪费严重',
    description: '建立固体废物资源化利用系统，配置废物处理设备，建立废物回收利用工艺，制定废物管理制度，建立废物回收台账',
    economicBenefit: '每万平方米线路板通过废物资源化利用增加收益2.5万元，减少废物处理成本1.2万元',
    environmentalBenefit: '每万平方米线路板提高废物资源化利用率至85%，减少废物产生量35%',
    indicatorIds: [28, 29, 44, 45],
    indicatorNames: ['金属铜回收率', '一般工业固体废物综合利用率', '一般固体废物收集与处理', '危险废物收集与处理'],
    investment: 150,
    paybackPeriod: 3.0,
    status: 'active',
    createdAt: '2024-07-05'
  },
  {
    id: 40,
    name: '能源管理系统升级',
    type: '管理改进',
    problemSolved: '能源管理系统不完善，能耗数据不准确，节能潜力挖掘不足，能源利用效率低',
    description: '升级能源管理系统，安装先进的能源监测设备，建立能耗数据库，制定节能管理制度，开展节能技术改造',
    economicBenefit: '每万平方米线路板节约能源成本2.5万元，提高能源利用效率20%',
    environmentalBenefit: '每万平方米线路板减少能源消耗，降低温室气体排放',
    indicatorIds: [7, 8, 9, 10, 11, 12, 13, 14, 47, 58],
    indicatorNames: ['单位产品电耗', '温室气体排放', '节能管理'],
    investment: 150,
    paybackPeriod: 2.5,
    status: 'active',
    createdAt: '2024-07-10'
  },
  {
    id: 41,
    name: '原材料管理系统优化',
    type: '管理改进',
    problemSolved: '原材料管理系统不完善，原材料浪费严重，库存积压严重，原材料利用率不高',
    description: '优化原材料管理系统，实施JIT采购模式，优化原材料库存结构，建立原材料使用台账，制定原材料消耗定额',
    economicBenefit: '每万平方米线路板节约原材料成本3万元，减少库存积压资金40%',
    environmentalBenefit: '每万平方米线路板提高原材料利用率12%，减少原材料浪费20%',
    indicatorIds: [20, 21, 22, 23, 24, 25, 26, 27, 28],
    indicatorNames: ['覆铜板利用率', '金属铜回收率'],
    investment: 80,
    paybackPeriod: 1.8,
    status: 'active',
    createdAt: '2024-07-15'
  },
  {
    id: 42,
    name: '生产工艺参数优化',
    type: '技术改造',
    problemSolved: '生产工艺参数不合理，生产效率低，产品质量不稳定，能耗高，环境污染严重',
    description: '优化生产工艺参数，采用先进的生产工艺，改进生产设备，建立生产工艺监测系统，制定生产工艺标准',
    economicBenefit: '每万平方米线路板节约生产成本3.5万元，提高生产效率30%，提高产品质量',
    environmentalBenefit: '每万平方米线路板减少环境污染，提高资源利用效率',
    indicatorIds: [1, 2, 3, 4, 5, 6, 7, 9, 12, 20, 28, 30, 34, 38, 43],
    indicatorNames: ['生产工艺与装备', '机械加工及辅助设施', '线路与阻焊图形形成', '板面清洗', '蚀刻', '电镀与化学镀', '单位能耗', '自动化水平', '覆铜板利用率', '金属铜回收率', '废水产生量', '废水中铜', '废水中COD', '废气收集与处理'],
    investment: 280,
    paybackPeriod: 3.5,
    status: 'active',
    createdAt: '2024-07-20'
  },
  {
    id: 43,
    name: '环保设施智能化改造',
    type: '环保治理',
    problemSolved: '环保设施智能化程度低，运行效率低，运行成本高，设施维护不及时，环保效果不理想',
    description: '对环保设施进行智能化改造，安装智能控制系统，建立环保设施监测系统，制定环保设施维护计划，开展环保设施运行培训',
    economicBenefit: '每万平方米线路板节约环保设施运行成本2万元，提高环保设施运行效率25%',
    environmentalBenefit: '每万平方米线路板提高环保设施运行效果，减少污染物排放',
    indicatorIds: [30, 34, 38, 42, 43, 44, 45, 46, 59],
    indicatorNames: ['废水产生量', '废水中铜产生量', '废水中COD产生量', '废水收集与处理', '废气收集与处理', '一般固体废物收集与处理', '危险废物收集与处理', '噪声', '污染物排放监测'],
    investment: 180,
    paybackPeriod: 3.2,
    status: 'active',
    createdAt: '2024-07-25'
  },
  {
    id: 44,
    name: '清洁生产审核体系完善',
    type: '管理改进',
    problemSolved: '清洁生产审核体系不完善，清洁生产工作不规范，持续改进机制不健全',
    description: '完善清洁生产审核体系，制定清洁生产管理制度，建立清洁生产目标指标，开展清洁生产培训，建立清洁生产考核体系',
    economicBenefit: '每万平方米线路板通过清洁生产审核节约成本5万元，提高管理效率35%',
    environmentalBenefit: '每万平方米线路板减少污染物排放25%，提高资源利用效率20%',
    indicatorIds: [54, 57, 58, 60, 62, 64],
    indicatorNames: ['环保法律法规执行情况', '清洁生产审核', '节能管理', '危险化学品管理', '固体废物管理', '运输方式'],
    investment: 60,
    paybackPeriod: 1.5,
    status: 'active',
    createdAt: '2024-07-30'
  },
  {
    id: 45,
    name: '产品质量追溯系统',
    type: '技术改造',
    problemSolved: '产品质量追溯系统不完善，产品质量问题难以追溯，产品质量管理不规范',
    description: '建立产品质量追溯系统，配置产品质量监测设备，制定产品质量标准，开展产品质量培训，建立产品质量追溯系统',
    economicBenefit: '每万平方米线路板提高产品合格率12%，减少产品返工成本2万元',
    environmentalBenefit: '每万平方米线路板减少产品返工，降低资源浪费',
    indicatorIds: [50],
    indicatorNames: ['产品特征'],
    investment: 120,
    paybackPeriod: 2.5,
    status: 'active',
    createdAt: '2024-08-01'
  },
  {
    id: 46,
    name: '生产线数字化改造',
    type: '技术改造',
    problemSolved: '生产线数字化程度低，数据采集不完善，生产管理效率低，质量控制不精准',
    description: '对生产线进行数字化改造，安装数据采集设备，建立生产管理系统，配置数字化质量控制设备，建立生产数据分析系统',
    economicBenefit: '每万平方米线路板节约管理成本2万元，提高生产效率35%，提高质量控制精度',
    environmentalBenefit: '每万平方米线路板提高生产管理效率，减少资源浪费',
    indicatorIds: [1, 2, 7, 9, 12, 20, 28],
    indicatorNames: ['生产工艺与装备', '机械加工及辅助设施', '单位能耗', '自动化水平', '覆铜板利用率', '金属铜回收率'],
    investment: 220,
    paybackPeriod: 3.0,
    status: 'active',
    createdAt: '2024-08-05'
  },
  {
    id: 47,
    name: '废水处理自动化系统',
    type: '环保治理',
    problemSolved: '废水处理系统自动化程度低，人工操作多，处理效果不稳定，运行成本高',
    description: '建设废水处理自动化系统，配置自动加药设备，安装在线监测设备，建立自动控制系统，优化处理工艺参数',
    economicBenefit: '每万平方米线路板节约废水处理成本1.8万元，提高处理效率25%',
    environmentalBenefit: '每万平方米线路板提高废水处理效果，减少污染物排放',
    indicatorIds: [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42],
    indicatorNames: ['废水产生量', '废水中铜产生量', '废水中COD产生量', '废水收集与处理'],
    investment: 200,
    paybackPeriod: 3.2,
    status: 'active',
    createdAt: '2024-08-10'
  },
  {
    id: 48,
    name: '废气处理自动化系统',
    type: '环保治理',
    problemSolved: '废气处理系统自动化程度低，人工操作多，处理效果不稳定，运行成本高',
    description: '建设废气处理自动化系统，配置自动控制设备，安装在线监测设备，建立自动控制系统，优化处理工艺参数',
    economicBenefit: '每万平方米线路板节约废气处理成本1.2万元，提高处理效率20%',
    environmentalBenefit: '每万平方米线路板提高废气处理效果，减少大气污染物排放',
    indicatorIds: [43],
    indicatorNames: ['废气收集与处理'],
    investment: 160,
    paybackPeriod: 3.5,
    status: 'active',
    createdAt: '2024-08-15'
  },
  {
    id: 49,
    name: '固体废物处理自动化系统',
    type: '环保治理',
    problemSolved: '固体废物处理系统自动化程度低，人工操作多，处理效率低，运行成本高',
    description: '建设固体废物处理自动化系统，配置自动分拣设备，安装自动处理设备，建立自动控制系统，优化处理工艺',
    economicBenefit: '每万平方米线路板节约废物处理成本1.5万元，提高处理效率30%',
    environmentalBenefit: '每万平方米线路板提高废物处理效率，减少废物产生量',
    indicatorIds: [29, 44, 45],
    indicatorNames: ['一般工业固体废物综合利用率', '一般固体废物收集与处理', '危险废物收集与处理'],
    investment: 140,
    paybackPeriod: 2.8,
    status: 'active',
    createdAt: '2024-08-20'
  },
  {
    id: 50,
    name: '能源消耗监测系统',
    type: '管理改进',
    problemSolved: '能源消耗监测不完善，能耗数据不准确，节能潜力挖掘不足，能源利用效率低',
    description: '建立能源消耗监测系统，安装能源监测设备，建立能耗数据库，制定节能管理制度，开展节能技术改造',
    economicBenefit: '每万平方米线路板节约能源成本2.8万元，提高能源利用效率22%',
    environmentalBenefit: '每万平方米线路板减少能源消耗，降低温室气体排放',
    indicatorIds: [7, 8, 9, 10, 11, 12, 13, 14, 47, 58],
    indicatorNames: ['单位产品电耗', '温室气体排放', '节能管理'],
    investment: 120,
    paybackPeriod: 2.2,
    status: 'active',
    createdAt: '2024-08-25'
  },
  {
    id: 51,
    name: '水资源消耗监测系统',
    type: '管理改进',
    problemSolved: '水资源消耗监测不完善，用水数据不准确，水资源利用效率低，水资源浪费严重',
    description: '建立水资源消耗监测系统，安装用水监测设备，建立用水数据库，制定水资源管理制度，开展水资源利用优化',
    economicBenefit: '每万平方米线路板节约水资源成本1.8万元，提高水资源利用效率25%',
    environmentalBenefit: '每万平方米线路板减少水资源消耗，提高水资源利用效率',
    indicatorIds: [15, 16, 17, 18, 19, 30, 31, 32, 33],
    indicatorNames: ['单位产品新鲜水耗', '水资源重复利用率', '废水产生量'],
    investment: 100,
    paybackPeriod: 2.0,
    status: 'active',
    createdAt: '2024-08-30'
  },
  {
    id: 52,
    name: '原材料消耗监测系统',
    type: '管理改进',
    problemSolved: '原材料消耗监测不完善，原材料使用数据不准确，原材料利用率不高，原材料浪费严重',
    description: '建立原材料消耗监测系统，安装原材料监测设备，建立原材料使用数据库，制定原材料管理制度，开展原材料利用优化',
    economicBenefit: '每万平方米线路板节约原材料成本3.2万元，提高原材料利用率18%',
    environmentalBenefit: '每万平方米线路板减少原材料浪费，提高原材料利用效率',
    indicatorIds: [20, 21, 22, 23, 24, 25, 26, 27, 28],
    indicatorNames: ['覆铜板利用率', '金属铜回收率'],
    investment: 90,
    paybackPeriod: 1.8,
    status: 'active',
    createdAt: '2024-09-01'
  },
  {
    id: 53,
    name: '生产工艺监测系统',
    type: '技术改造',
    problemSolved: '生产工艺监测不完善，工艺参数不准确，生产效率低，产品质量不稳定',
    description: '建立生产工艺监测系统，安装工艺监测设备，建立工艺参数数据库，制定工艺管理制度，开展工艺优化',
    economicBenefit: '每万平方米线路板节约生产成本3.8万元，提高生产效率32%，提高产品质量',
    environmentalBenefit: '每万平方米线路板提高生产工艺效率，减少资源浪费',
    indicatorIds: [1, 2, 3, 4, 5, 6, 7, 9, 12, 20, 28, 30, 34, 38, 43],
    indicatorNames: ['生产工艺与装备', '机械加工及辅助设施', '线路与阻焊图形形成', '板面清洗', '蚀刻', '电镀与化学镀', '单位能耗', '自动化水平', '覆铜板利用率', '金属铜回收率', '废水产生量', '废水中铜', '废水中COD', '废气收集与处理'],
    investment: 200,
    paybackPeriod: 2.8,
    status: 'active',
    createdAt: '2024-09-05'
  },
  {
    id: 54,
    name: '环保设施监测系统',
    type: '环保治理',
    problemSolved: '环保设施监测不完善，设施运行数据不准确，设施运行效率低，环保效果不理想',
    description: '建立环保设施监测系统，安装设施监测设备，建立设施运行数据库，制定设施管理制度，开展设施运行优化',
    economicBenefit: '每万平方米线路板节约环保设施运行成本2.2万元，提高设施运行效率28%',
    environmentalBenefit: '每万平方米线路板提高环保设施运行效果，减少污染物排放',
    indicatorIds: [30, 34, 38, 42, 43, 44, 45, 46, 59],
    indicatorNames: ['废水产生量', '废水中铜产生量', '废水中COD产生量', '废水收集与处理', '废气收集与处理', '一般固体废物收集与处理', '危险废物收集与处理', '噪声', '污染物排放监测'],
    investment: 160,
    paybackPeriod: 2.5,
    status: 'active',
    createdAt: '2024-09-10'
  },
  {
    id: 55,
    name: '清洁生产监测系统',
    type: '管理改进',
    problemSolved: '清洁生产监测不完善，清洁生产数据不准确，清洁生产效果不理想，持续改进机制不健全',
    description: '建立清洁生产监测系统，安装清洁生产监测设备，建立清洁生产数据库，制定清洁生产管理制度，开展清洁生产优化',
    economicBenefit: '每万平方米线路板通过清洁生产监测节约成本4.5万元，提高清洁生产效果30%',
    environmentalBenefit: '每万平方米线路板提高清洁生产效果，减少污染物排放，提高资源利用效率',
    indicatorIds: [54, 57, 58, 60, 62, 64],
    indicatorNames: ['环保法律法规执行情况', '清洁生产审核', '节能管理', '危险化学品管理', '固体废物管理', '运输方式'],
    investment: 80,
    paybackPeriod: 1.8,
    status: 'active',
    createdAt: '2024-09-15'
  },
  {
    id: 56,
    name: '生产线智能化管理系统',
    type: '技术改造',
    problemSolved: '生产线智能化管理不完善，生产管理效率低，质量控制不精准，资源利用效率低',
    description: '建立生产线智能化管理系统，配置智能化管理设备，建立生产管理数据库，制定生产管理制度，开展生产管理优化',
    economicBenefit: '每万平方米线路板节约管理成本2.5万元，提高生产管理效率40%，提高质量控制精度',
    environmentalBenefit: '每万平方米线路板提高生产管理效率，减少资源浪费',
    indicatorIds: [1, 2, 7, 9, 12, 20, 28],
    indicatorNames: ['生产工艺与装备', '机械加工及辅助设施', '单位能耗', '自动化水平', '覆铜板利用率', '金属铜回收率'],
    investment: 250,
    paybackPeriod: 3.2,
    status: 'active',
    createdAt: '2024-09-20'
  },
  {
    id: 57,
    name: '废水处理智能化系统',
    type: '环保治理',
    problemSolved: '废水处理智能化程度低，处理效果不稳定，运行成本高，管理效率低',
    description: '建设废水处理智能化系统，配置智能化处理设备，建立处理效果监测系统，制定智能化管理制度，开展智能化处理优化',
    economicBenefit: '每万平方米线路板节约废水处理成本2万元，提高处理效率30%',
    environmentalBenefit: '每万平方米线路板提高废水处理效果，减少污染物排放',
    indicatorIds: [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42],
    indicatorNames: ['废水产生量', '废水中铜产生量', '废水中COD产生量', '废水收集与处理'],
    investment: 220,
    paybackPeriod: 3.5,
    status: 'active',
    createdAt: '2024-09-25'
  },
  {
    id: 58,
    name: '废气处理智能化系统',
    type: '环保治理',
    problemSolved: '废气处理智能化程度低，处理效果不稳定，运行成本高，管理效率低',
    description: '建设废气处理智能化系统，配置智能化处理设备，建立处理效果监测系统，制定智能化管理制度，开展智能化处理优化',
    economicBenefit: '每万平方米线路板节约废气处理成本1.5万元，提高处理效率25%',
    environmentalBenefit: '每万平方米线路板提高废气处理效果，减少大气污染物排放',
    indicatorIds: [43],
    indicatorNames: ['废气收集与处理'],
    investment: 180,
    paybackPeriod: 3.8,
    status: 'active',
    createdAt: '2024-09-30'
  },
  {
    id: 59,
    name: '固体废物处理智能化系统',
    type: '环保治理',
    problemSolved: '固体废物处理智能化程度低，处理效率低，运行成本高，管理效率低',
    description: '建设固体废物处理智能化系统，配置智能化处理设备，建立处理效果监测系统，制定智能化管理制度，开展智能化处理优化',
    economicBenefit: '每万平方米线路板节约废物处理成本1.8万元，提高处理效率35%',
    environmentalBenefit: '每万平方米线路板提高废物处理效率，减少废物产生量',
    indicatorIds: [29, 44, 45],
    indicatorNames: ['一般工业固体废物综合利用率', '一般固体废物收集与处理', '危险废物收集与处理'],
    investment: 160,
    paybackPeriod: 3.0,
    status: 'active',
    createdAt: '2024-10-01'
  },
  {
    id: 60,
    name: '能源管理智能化系统',
    type: '管理改进',
    problemSolved: '能源管理智能化程度低，能耗数据不准确，节能潜力挖掘不足，能源利用效率低',
    description: '建立能源管理智能化系统，配置智能化管理设备，建立能耗数据库，制定智能化管理制度，开展智能化管理优化',
    economicBenefit: '每万平方米线路板节约能源成本3万元，提高能源利用效率25%',
    environmentalBenefit: '每万平方米线路板减少能源消耗，降低温室气体排放',
    indicatorIds: [7, 8, 9, 10, 11, 12, 13, 14, 47, 58],
    indicatorNames: ['单位产品电耗', '温室气体排放', '节能管理'],
    investment: 140,
    paybackPeriod: 2.5,
    status: 'active',
    createdAt: '2024-10-05'
  },
  {
    id: 61,
    name: '水资源管理智能化系统',
    type: '管理改进',
    problemSolved: '水资源管理智能化程度低，用水数据不准确，水资源利用效率低，水资源浪费严重',
    description: '建立水资源管理智能化系统，配置智能化管理设备，建立用水数据库，制定智能化管理制度，开展智能化管理优化',
    economicBenefit: '每万平方米线路板节约水资源成本2万元，提高水资源利用效率30%',
    environmentalBenefit: '每万平方米线路板减少水资源消耗，提高水资源利用效率',
    indicatorIds: [15, 16, 17, 18, 19, 30, 31, 32, 33],
    indicatorNames: ['单位产品新鲜水耗', '水资源重复利用率', '废水产生量'],
    investment: 120,
    paybackPeriod: 2.2,
    status: 'active',
    createdAt: '2024-10-10'
  },
  {
    id: 62,
    name: '原材料管理智能化系统',
    type: '管理改进',
    problemSolved: '原材料管理智能化程度低，原材料使用数据不准确，原材料利用率不高，原材料浪费严重',
    description: '建立原材料管理智能化系统，配置智能化管理设备，建立原材料使用数据库，制定智能化管理制度，开展智能化管理优化',
    economicBenefit: '每万平方米线路板节约原材料成本3.5万元，提高原材料利用率20%',
    environmentalBenefit: '每万平方米线路板减少原材料浪费，提高原材料利用效率',
    indicatorIds: [20, 21, 22, 23, 24, 25, 26, 27, 28],
    indicatorNames: ['覆铜板利用率', '金属铜回收率'],
    investment: 100,
    paybackPeriod: 2.0,
    status: 'active',
    createdAt: '2024-10-15'
  },
  {
    id: 63,
    name: '生产工艺智能化系统',
    type: '技术改造',
    problemSolved: '生产工艺智能化程度低，工艺参数不准确，生产效率低，产品质量不稳定',
    description: '建立生产工艺智能化系统，配置智能化管理设备，建立工艺参数数据库，制定智能化管理制度，开展智能化管理优化',
    economicBenefit: '每万平方米线路板节约生产成本4万元，提高生产效率35%，提高产品质量',
    environmentalBenefit: '每万平方米线路板提高生产工艺效率，减少资源浪费',
    indicatorIds: [1, 2, 3, 4, 5, 6, 7, 9, 12, 20, 28, 30, 34, 38, 43],
    indicatorNames: ['生产工艺与装备', '机械加工及辅助设施', '线路与阻焊图形形成', '板面清洗', '蚀刻', '电镀与化学镀', '单位能耗', '自动化水平', '覆铜板利用率', '金属铜回收率', '废水产生量', '废水中铜', '废水中COD', '废气收集与处理'],
    investment: 220,
    paybackPeriod: 3.0,
    status: 'active',
    createdAt: '2024-10-20'
  },
  {
    id: 64,
    name: '环保设施智能化管理系统',
    type: '环保治理',
    problemSolved: '环保设施智能化管理不完善，设施运行数据不准确，设施运行效率低，环保效果不理想',
    description: '建立环保设施智能化管理系统，配置智能化管理设备，建立设施运行数据库，制定智能化管理制度，开展智能化管理优化',
    economicBenefit: '每万平方米线路板节约环保设施运行成本2.5万元，提高设施运行效率30%',
    environmentalBenefit: '每万平方米线路板提高环保设施运行效果，减少污染物排放',
    indicatorIds: [30, 34, 38, 42, 43, 44, 45, 46, 59],
    indicatorNames: ['废水产生量', '废水中铜产生量', '废水中COD产生量', '废水收集与处理', '废气收集与处理', '一般固体废物收集与处理', '危险废物收集与处理', '噪声', '污染物排放监测'],
    investment: 180,
    paybackPeriod: 2.8,
    status: 'active',
    createdAt: '2024-10-25'
  },
  {
    id: 65,
    name: '清洁生产智能化管理系统',
    type: '管理改进',
    problemSolved: '清洁生产智能化管理不完善，清洁生产数据不准确，清洁生产效果不理想，持续改进机制不健全',
    description: '建立清洁生产智能化管理系统，配置智能化管理设备，建立清洁生产数据库，制定智能化管理制度，开展智能化管理优化',
    economicBenefit: '每万平方米线路板通过清洁生产智能化管理节约成本5万元，提高清洁生产效果35%',
    environmentalBenefit: '每万平方米线路板提高清洁生产效果，减少污染物排放，提高资源利用效率',
    indicatorIds: [54, 57, 58, 60, 62, 64],
    indicatorNames: ['环保法律法规执行情况', '清洁生产审核', '节能管理', '危险化学品管理', '固体废物管理', '运输方式'],
    investment: 100,
    paybackPeriod: 2.0,
    status: 'active',
    createdAt: '2024-10-30'
  },
  {
    id: 66,
    name: '生产线数字化监控系统',
    type: '技术改造',
    problemSolved: '生产线数字化监控不完善，生产数据采集不准确，生产管理效率低，质量控制不精准',
    description: '建立生产线数字化监控系统，配置数字化监控设备，建立生产数据采集系统，制定数字化管理制度，开展数字化监控优化',
    economicBenefit: '每万平方米线路板节约管理成本2.8万元，提高生产管理效率45%，提高质量控制精度',
    environmentalBenefit: '每万平方米线路板提高生产管理效率，减少资源浪费',
    indicatorIds: [1, 2, 7, 9, 12, 20, 28],
    indicatorNames: ['生产工艺与装备', '机械加工及辅助设施', '单位能耗', '自动化水平', '覆铜板利用率', '金属铜回收率'],
    investment: 280,
    paybackPeriod: 3.5,
    status: 'active',
    createdAt: '2024-11-01'
  },
  {
    id: 67,
    name: '废水处理数字化监控系统',
    type: '环保治理',
    problemSolved: '废水处理数字化监控不完善，处理数据采集不准确，处理效果不稳定，运行成本高',
    description: '建立废水处理数字化监控系统，配置数字化监控设备，建立处理数据采集系统，制定数字化管理制度，开展数字化监控优化',
    economicBenefit: '每万平方米线路板节约废水处理成本2.2万元，提高处理效率32%',
    environmentalBenefit: '每万平方米线路板提高废水处理效果，减少污染物排放',
    indicatorIds: [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42],
    indicatorNames: ['废水产生量', '废水中铜产生量', '废水中COD产生量', '废水收集与处理'],
    investment: 240,
    paybackPeriod: 3.8,
    status: 'active',
    createdAt: '2024-11-05'
  },
  {
    id: 68,
    name: '废气处理数字化监控系统',
    type: '环保治理',
    problemSolved: '废气处理数字化监控不完善，处理数据采集不准确，处理效果不稳定，运行成本高',
    description: '建立废气处理数字化监控系统，配置数字化监控设备，建立处理数据采集系统，制定数字化管理制度，开展数字化监控优化',
    economicBenefit: '每万平方米线路板节约废气处理成本1.8万元，提高处理效率28%',
    environmentalBenefit: '每万平方米线路板提高废气处理效果，减少大气污染物排放',
    indicatorIds: [43],
    indicatorNames: ['废气收集与处理'],
    investment: 200,
    paybackPeriod: 4.0,
    status: 'active',
    createdAt: '2024-11-10'
  },
  {
    id: 69,
    name: '固体废物处理数字化监控系统',
    type: '环保治理',
    problemSolved: '固体废物处理数字化监控不完善，处理数据采集不准确，处理效率低，运行成本高',
    description: '建立固体废物处理数字化监控系统，配置数字化监控设备，建立处理数据采集系统，制定数字化管理制度，开展数字化监控优化',
    economicBenefit: '每万平方米线路板节约废物处理成本2万元，提高处理效率38%',
    environmentalBenefit: '每万平方米线路板提高废物处理效率，减少废物产生量',
    indicatorIds: [29, 44, 45],
    indicatorNames: ['一般工业固体废物综合利用率', '一般固体废物收集与处理', '危险废物收集与处理'],
    investment: 180,
    paybackPeriod: 3.2,
    status: 'active',
    createdAt: '2024-11-15'
  },
  {
    id: 70,
    name: '能源管理数字化监控系统',
    type: '管理改进',
    problemSolved: '能源管理数字化监控不完善，能耗数据采集不准确，节能潜力挖掘不足，能源利用效率低',
    description: '建立能源管理数字化监控系统，配置数字化监控设备，建立能耗数据采集系统，制定数字化管理制度，开展数字化监控优化',
    economicBenefit: '每万平方米线路板节约能源成本3.2万元，提高能源利用效率28%',
    environmentalBenefit: '每万平方米线路板减少能源消耗，降低温室气体排放',
    indicatorIds: [7, 8, 9, 10, 11, 12, 13, 14, 47, 58],
    indicatorNames: ['单位产品电耗', '温室气体排放', '节能管理'],
    investment: 160,
    paybackPeriod: 2.8,
    status: 'active',
    createdAt: '2024-11-20'
  },
  {
    id: 71,
    name: '水资源管理数字化监控系统',
    type: '管理改进',
    problemSolved: '水资源管理数字化监控不完善，用水数据采集不准确，水资源利用效率低，水资源浪费严重',
    description: '建立水资源管理数字化监控系统，配置数字化监控设备，建立用水数据采集系统，制定数字化管理制度，开展数字化监控优化',
    economicBenefit: '每万平方米线路板节约水资源成本2.2万元，提高水资源利用效率32%',
    environmentalBenefit: '每万平方米线路板减少水资源消耗，提高水资源利用效率',
    indicatorIds: [15, 16, 17, 18, 19, 30, 31, 32, 33],
    indicatorNames: ['单位产品新鲜水耗', '水资源重复利用率', '废水产生量'],
    investment: 140,
    paybackPeriod: 2.5,
    status: 'active',
    createdAt: '2024-11-25'
  },
  {
    id: 72,
    name: '原材料管理数字化监控系统',
    type: '管理改进',
    problemSolved: '原材料管理数字化监控不完善，原材料使用数据采集不准确，原材料利用率不高，原材料浪费严重',
    description: '建立原材料管理数字化监控系统，配置数字化监控设备，建立原材料使用数据采集系统，制定数字化管理制度，开展数字化监控优化',
    economicBenefit: '每万平方米线路板节约原材料成本3.8万元，提高原材料利用率22%',
    environmentalBenefit: '每万平方米线路板减少原材料浪费，提高原材料利用效率',
    indicatorIds: [20, 21, 22, 23, 24, 25, 26, 27, 28],
    indicatorNames: ['覆铜板利用率', '金属铜回收率'],
    investment: 120,
    paybackPeriod: 2.2,
    status: 'active',
    createdAt: '2024-11-30'
  },
  {
    id: 73,
    name: '生产工艺数字化监控系统',
    type: '技术改造',
    problemSolved: '生产工艺数字化监控不完善，工艺参数数据采集不准确，生产效率低，产品质量不稳定',
    description: '建立生产工艺数字化监控系统，配置数字化监控设备，建立工艺参数数据采集系统，制定数字化管理制度，开展数字化监控优化',
    economicBenefit: '每万平方米线路板节约生产成本4.2万元，提高生产效率38%，提高产品质量',
    environmentalBenefit: '每万平方米线路板提高生产工艺效率，减少资源浪费',
    indicatorIds: [1, 2, 3, 4, 5, 6, 7, 9, 12, 20, 28, 30, 34, 38, 43],
    indicatorNames: ['生产工艺与装备', '机械加工及辅助设施', '线路与阻焊图形形成', '板面清洗', '蚀刻', '电镀与化学镀', '单位能耗', '自动化水平', '覆铜板利用率', '金属铜回收率', '废水产生量', '废水中铜', '废水中COD', '废气收集与处理'],
    investment: 240,
    paybackPeriod: 3.2,
    status: 'active',
    createdAt: '2024-12-01'
  },
  {
    id: 74,
    name: '环保设施数字化监控系统',
    type: '环保治理',
    problemSolved: '环保设施数字化监控不完善，设施运行数据采集不准确，设施运行效率低，环保效果不理想',
    description: '建立环保设施数字化监控系统，配置数字化监控设备，建立设施运行数据采集系统，制定数字化管理制度，开展数字化监控优化',
    economicBenefit: '每万平方米线路板节约环保设施运行成本2.8万元，提高设施运行效率32%',
    environmentalBenefit: '每万平方米线路板提高环保设施运行效果，减少污染物排放',
    indicatorIds: [30, 34, 38, 42, 43, 44, 45, 46, 59],
    indicatorNames: ['废水产生量', '废水中铜产生量', '废水中COD产生量', '废水收集与处理', '废气收集与处理', '一般固体废物收集与处理', '危险废物收集与处理', '噪声', '污染物排放监测'],
    investment: 200,
    paybackPeriod: 3.0,
    status: 'active',
    createdAt: '2024-12-05'
  },
  {
    id: 75,
    name: '清洁生产数字化监控系统',
    type: '管理改进',
    problemSolved: '清洁生产数字化监控不完善，清洁生产数据采集不准确，清洁生产效果不理想，持续改进机制不健全',
    description: '建立清洁生产数字化监控系统，配置数字化监控设备，建立清洁生产数据采集系统，制定数字化管理制度，开展数字化监控优化',
    economicBenefit: '每万平方米线路板通过清洁生产数字化监控节约成本5.2万元，提高清洁生产效果38%',
    environmentalBenefit: '每万平方米线路板提高清洁生产效果，减少污染物排放，提高资源利用效率',
    indicatorIds: [54, 57, 58, 60, 62, 64],
    indicatorNames: ['环保法律法规执行情况', '清洁生产审核', '节能管理', '危险化学品管理', '固体废物管理', '运输方式'],
    investment: 120,
    paybackPeriod: 2.2,
    status: 'active',
    createdAt: '2024-12-10'
  },
  {
    id: 76,
    name: '生产线物联网监控系统',
    type: '技术改造',
    problemSolved: '生产线物联网监控不完善，设备连接不充分，数据采集不全面，生产管理效率低',
    description: '建立生产线物联网监控系统，配置物联网监控设备，建立设备连接系统，制定物联网管理制度，开展物联网监控优化',
    economicBenefit: '每万平方米线路板节约管理成本3万元，提高生产管理效率50%，提高设备监控精度',
    environmentalBenefit: '每万平方米线路板提高生产管理效率，减少资源浪费',
    indicatorIds: [1, 2, 7, 9, 12, 20, 28],
    indicatorNames: ['生产工艺与装备', '机械加工及辅助设施', '单位能耗', '自动化水平', '覆铜板利用率', '金属铜回收率'],
    investment: 300,
    paybackPeriod: 3.8,
    status: 'active',
    createdAt: '2024-12-15'
  },
  {
    id: 77,
    name: '废水处理物联网监控系统',
    type: '环保治理',
    problemSolved: '废水处理物联网监控不完善，设备连接不充分，数据采集不全面，处理效果不稳定',
    description: '建立废水处理物联网监控系统，配置物联网监控设备，建立设备连接系统，制定物联网管理制度，开展物联网监控优化',
    economicBenefit: '每万平方米线路板节约废水处理成本2.5万元，提高处理效率35%',
    environmentalBenefit: '每万平方米线路板提高废水处理效果，减少污染物排放',
    indicatorIds: [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42],
    indicatorNames: ['废水产生量', '废水中铜产生量', '废水中COD产生量', '废水收集与处理'],
    investment: 260,
    paybackPeriod: 4.0,
    status: 'active',
    createdAt: '2024-12-20'
  },
  {
    id: 78,
    name: '废气处理物联网监控系统',
    type: '环保治理',
    problemSolved: '废气处理物联网监控不完善，设备连接不充分，数据采集不全面，处理效果不稳定',
    description: '建立废气处理物联网监控系统，配置物联网监控设备，建立设备连接系统，制定物联网管理制度，开展物联网监控优化',
    economicBenefit: '每万平方米线路板节约废气处理成本2万元，提高处理效率30%',
    environmentalBenefit: '每万平方米线路板提高废气处理效果，减少大气污染物排放',
    indicatorIds: [43],
    indicatorNames: ['废气收集与处理'],
    investment: 220,
    paybackPeriod: 4.2,
    status: 'active',
    createdAt: '2024-12-25'
  },
  {
    id: 79,
    name: '固体废物处理物联网监控系统',
    type: '环保治理',
    problemSolved: '固体废物处理物联网监控不完善，设备连接不充分，数据采集不全面，处理效率低',
    description: '建立固体废物处理物联网监控系统，配置物联网监控设备，建立设备连接系统，制定物联网管理制度，开展物联网监控优化',
    economicBenefit: '每万平方米线路板节约废物处理成本2.2万元，提高处理效率40%',
    environmentalBenefit: '每万平方米线路板提高废物处理效率，减少废物产生量',
    indicatorIds: [29, 44, 45],
    indicatorNames: ['一般工业固体废物综合利用率', '一般固体废物收集与处理', '危险废物收集与处理'],
    investment: 200,
    paybackPeriod: 3.5,
    status: 'active',
    createdAt: '2024-12-30'
  },
  {
    id: 80,
    name: '能源管理物联网监控系统',
    type: '管理改进',
    problemSolved: '能源管理物联网监控不完善，设备连接不充分，数据采集不全面，能源利用效率低',
    description: '建立能源管理物联网监控系统，配置物联网监控设备，建立设备连接系统，制定物联网管理制度，开展物联网监控优化',
    economicBenefit: '每万平方米线路板节约能源成本3.5万元，提高能源利用效率30%',
    environmentalBenefit: '每万平方米线路板减少能源消耗，降低温室气体排放',
    indicatorIds: [7, 8, 9, 10, 11, 12, 13, 14, 47, 58],
    indicatorNames: ['单位产品电耗', '温室气体排放', '节能管理'],
    investment: 180,
    paybackPeriod: 3.0,
    status: 'active',
    createdAt: '2025-01-01'
  },
  {
    id: 81,
    name: '水资源管理物联网监控系统',
    type: '管理改进',
    problemSolved: '水资源管理物联网监控不完善，设备连接不充分，数据采集不全面，水资源利用效率低',
    description: '建立水资源管理物联网监控系统，配置物联网监控设备，建立设备连接系统，制定物联网管理制度，开展物联网监控优化',
    economicBenefit: '每万平方米线路板节约水资源成本2.5万元，提高水资源利用效率35%',
    environmentalBenefit: '每万平方米线路板减少水资源消耗，提高水资源利用效率',
    indicatorIds: [15, 16, 17, 18, 19, 30, 31, 32, 33],
    indicatorNames: ['单位产品新鲜水耗', '水资源重复利用率', '废水产生量'],
    investment: 160,
    paybackPeriod: 2.8,
    status: 'active',
    createdAt: '2025-01-05'
  },
  {
    id: 82,
    name: '原材料管理物联网监控系统',
    type: '管理改进',
    problemSolved: '原材料管理物联网监控不完善，设备连接不充分，数据采集不全面，原材料利用率不高',
    description: '建立原材料管理物联网监控系统，配置物联网监控设备，建立设备连接系统，制定物联网管理制度，开展物联网监控优化',
    economicBenefit: '每万平方米线路板节约原材料成本4万元，提高原材料利用率25%',
    environmentalBenefit: '每万平方米线路板减少原材料浪费，提高原材料利用效率',
    indicatorIds: [20, 21, 22, 23, 24, 25, 26, 27, 28],
    indicatorNames: ['覆铜板利用率', '金属铜回收率'],
    investment: 140,
    paybackPeriod: 2.5,
    status: 'active',
    createdAt: '2025-01-10'
  },
  {
    id: 83,
    name: '生产工艺物联网监控系统',
    type: '技术改造',
    problemSolved: '生产工艺物联网监控不完善，设备连接不充分，数据采集不全面，生产效率低',
    description: '建立生产工艺物联网监控系统，配置物联网监控设备，建立设备连接系统，制定物联网管理制度，开展物联网监控优化',
    economicBenefit: '每万平方米线路板节约生产成本4.5万元，提高生产效率40%，提高产品质量',
    environmentalBenefit: '每万平方米线路板提高生产工艺效率，减少资源浪费',
    indicatorIds: [1, 2, 3, 4, 5, 6, 7, 9, 12, 20, 28, 30, 34, 38, 43],
    indicatorNames: ['生产工艺与装备', '机械加工及辅助设施', '线路与阻焊图形形成', '板面清洗', '蚀刻', '电镀与化学镀', '单位能耗', '自动化水平', '覆铜板利用率', '金属铜回收率', '废水产生量', '废水中铜', '废水中COD', '废气收集与处理'],
    investment: 260,
    paybackPeriod: 3.5,
    status: 'active',
    createdAt: '2025-01-15'
  },
  {
    id: 84,
    name: '环保设施物联网监控系统',
    type: '环保治理',
    problemSolved: '环保设施物联网监控不完善，设备连接不充分，数据采集不全面，环保效果不理想',
    description: '建立环保设施物联网监控系统，配置物联网监控设备，建立设备连接系统，制定物联网管理制度，开展物联网监控优化',
    economicBenefit: '每万平方米线路板节约环保设施运行成本3万元，提高设施运行效率35%',
    environmentalBenefit: '每万平方米线路板提高环保设施运行效果，减少污染物排放',
    indicatorIds: [30, 34, 38, 42, 43, 44, 45, 46, 59],
    indicatorNames: ['废水产生量', '废水中铜产生量', '废水中COD产生量', '废水收集与处理', '废气收集与处理', '一般固体废物收集与处理', '危险废物收集与处理', '噪声', '污染物排放监测'],
    investment: 220,
    paybackPeriod: 3.2,
    status: 'active',
    createdAt: '2025-01-20'
  },
  {
    id: 85,
    name: '清洁生产物联网监控系统',
    type: '管理改进',
    problemSolved: '清洁生产物联网监控不完善，设备连接不充分，数据采集不全面，清洁生产效果不理想',
    description: '建立清洁生产物联网监控系统，配置物联网监控设备，建立设备连接系统，制定物联网管理制度，开展物联网监控优化',
    economicBenefit: '每万平方米线路板通过清洁生产物联网监控节约成本5.5万元，提高清洁生产效果40%',
    environmentalBenefit: '每万平方米线路板提高清洁生产效果，减少污染物排放，提高资源利用效率',
    indicatorIds: [54, 57, 58, 60, 62, 64],
    indicatorNames: ['环保法律法规执行情况', '清洁生产审核', '节能管理', '危险化学品管理', '固体废物管理', '运输方式'],
    investment: 140,
    paybackPeriod: 2.5,
    status: 'active',
    createdAt: '2025-01-25'
  },
  {
    id: 86,
    name: '生产线大数据分析系统',
    type: '技术改造',
    problemSolved: '生产线大数据分析不完善，数据分析不深入，生产优化不充分，管理决策不精准',
    description: '建立生产线大数据分析系统，配置大数据分析设备，建立数据分析模型，制定大数据管理制度，开展大数据分析优化',
    economicBenefit: '每万平方米线路板节约管理成本3.2万元，提高生产管理效率55%，提高决策精准度',
    environmentalBenefit: '每万平方米线路板提高生产管理效率，减少资源浪费',
    indicatorIds: [1, 2, 7, 9, 12, 20, 28],
    indicatorNames: ['生产工艺与装备', '机械加工及辅助设施', '单位能耗', '自动化水平', '覆铜板利用率', '金属铜回收率'],
    investment: 320,
    paybackPeriod: 4.0,
    status: 'active',
    createdAt: '2025-01-30'
  },
  {
    id: 87,
    name: '废水处理大数据分析系统',
    type: '环保治理',
    problemSolved: '废水处理大数据分析不完善，数据分析不深入，处理优化不充分，运行效果不理想',
    description: '建立废水处理大数据分析系统，配置大数据分析设备，建立数据分析模型，制定大数据管理制度，开展大数据分析优化',
    economicBenefit: '每万平方米线路板节约废水处理成本2.8万元，提高处理效率38%',
    environmentalBenefit: '每万平方米线路板提高废水处理效果，减少污染物排放',
    indicatorIds: [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42],
    indicatorNames: ['废水产生量', '废水中铜产生量', '废水中COD产生量', '废水收集与处理'],
    investment: 280,
    paybackPeriod: 4.2,
    status: 'active',
    createdAt: '2025-02-01'
  },
  {
    id: 88,
    name: '废气处理大数据分析系统',
    type: '环保治理',
    problemSolved: '废气处理大数据分析不完善，数据分析不深入，处理优化不充分，运行效果不理想',
    description: '建立废气处理大数据分析系统，配置大数据分析设备，建立数据分析模型，制定大数据管理制度，开展大数据分析优化',
    economicBenefit: '每万平方米线路板节约废气处理成本2.2万元，提高处理效率32%',
    environmentalBenefit: '每万平方米线路板提高废气处理效果，减少大气污染物排放',
    indicatorIds: [43],
    indicatorNames: ['废气收集与处理'],
    investment: 240,
    paybackPeriod: 4.5,
    status: 'active',
    createdAt: '2025-02-05'
  },
  {
    id: 89,
    name: '固体废物处理大数据分析系统',
    type: '环保治理',
    problemSolved: '固体废物处理大数据分析不完善，数据分析不深入，处理优化不充分，运行效果不理想',
    description: '建立固体废物处理大数据分析系统，配置大数据分析设备，建立数据分析模型，制定大数据管理制度，开展大数据分析优化',
    economicBenefit: '每万平方米线路板节约废物处理成本2.5万元，提高处理效率42%',
    environmentalBenefit: '每万平方米线路板提高废物处理效率，减少废物产生量',
    indicatorIds: [29, 44, 45],
    indicatorNames: ['一般工业固体废物综合利用率', '一般固体废物收集与处理', '危险废物收集与处理'],
    investment: 220,
    paybackPeriod: 3.8,
    status: 'active',
    createdAt: '2025-02-10'
  },
  {
    id: 90,
    name: '能源管理大数据分析系统',
    type: '管理改进',
    problemSolved: '能源管理大数据分析不完善，数据分析不深入，节能优化不充分，能源利用效率低',
    description: '建立能源管理大数据分析系统，配置大数据分析设备，建立数据分析模型，制定大数据管理制度，开展大数据分析优化',
    economicBenefit: '每万平方米线路板节约能源成本3.8万元，提高能源利用效率32%',
    environmentalBenefit: '每万平方米线路板减少能源消耗，降低温室气体排放',
    indicatorIds: [7, 8, 9, 10, 11, 12, 13, 14, 47, 58],
    indicatorNames: ['单位产品电耗', '温室气体排放', '节能管理'],
    investment: 200,
    paybackPeriod: 3.2,
    status: 'active',
    createdAt: '2025-02-15'
  },
  {
    id: 91,
    name: '水资源管理大数据分析系统',
    type: '管理改进',
    problemSolved: '水资源管理大数据分析不完善，数据分析不深入，用水优化不充分，水资源利用效率低',
    description: '建立水资源管理大数据分析系统，配置大数据分析设备，建立数据分析模型，制定大数据管理制度，开展大数据分析优化',
    economicBenefit: '每万平方米线路板节约水资源成本2.8万元，提高水资源利用效率38%',
    environmentalBenefit: '每万平方米线路板减少水资源消耗，提高水资源利用效率',
    indicatorIds: [15, 16, 17, 18, 19, 30, 31, 32, 33],
    indicatorNames: ['单位产品新鲜水耗', '水资源重复利用率', '废水产生量'],
    investment: 180,
    paybackPeriod: 3.0,
    status: 'active',
    createdAt: '2025-02-20'
  },
  {
    id: 92,
    name: '原材料管理大数据分析系统',
    type: '管理改进',
    problemSolved: '原材料管理大数据分析不完善，数据分析不深入，使用优化不充分，原材料利用率不高',
    description: '建立原材料管理大数据分析系统，配置大数据分析设备，建立数据分析模型，制定大数据管理制度，开展大数据分析优化',
    economicBenefit: '每万平方米线路板节约原材料成本4.2万元，提高原材料利用率28%',
    environmentalBenefit: '每万平方米线路板减少原材料浪费，提高原材料利用效率',
    indicatorIds: [20, 21, 22, 23, 24, 25, 26, 27, 28],
    indicatorNames: ['覆铜板利用率', '金属铜回收率'],
    investment: 160,
    paybackPeriod: 2.8,
    status: 'active',
    createdAt: '2025-02-25'
  },
  {
    id: 93,
    name: '生产工艺大数据分析系统',
    type: '技术改造',
    problemSolved: '生产工艺大数据分析不完善，数据分析不深入，工艺优化不充分，生产效率低',
    description: '建立生产工艺大数据分析系统，配置大数据分析设备，建立数据分析模型，制定大数据管理制度，开展大数据分析优化',
    economicBenefit: '每万平方米线路板节约生产成本4.8万元，提高生产效率42%，提高产品质量',
    environmentalBenefit: '每万平方米线路板提高生产工艺效率，减少资源浪费',
    indicatorIds: [1, 2, 3, 4, 5, 6, 7, 9, 12, 20, 28, 30, 34, 38, 43],
    indicatorNames: ['生产工艺与装备', '机械加工及辅助设施', '线路与阻焊图形形成', '板面清洗', '蚀刻', '电镀与化学镀', '单位能耗', '自动化水平', '覆铜板利用率', '金属铜回收率', '废水产生量', '废水中铜', '废水中COD', '废气收集与处理'],
    investment: 280,
    paybackPeriod: 3.8,
    status: 'active',
    createdAt: '2025-03-01'
  },
  {
    id: 94,
    name: '环保设施大数据分析系统',
    type: '环保治理',
    problemSolved: '环保设施大数据分析不完善，数据分析不深入，设施优化不充分，环保效果不理想',
    description: '建立环保设施大数据分析系统，配置大数据分析设备，建立数据分析模型，制定大数据管理制度，开展大数据分析优化',
    economicBenefit: '每万平方米线路板节约环保设施运行成本3.2万元，提高设施运行效率38%',
    environmentalBenefit: '每万平方米线路板提高环保设施运行效果，减少污染物排放',
    indicatorIds: [30, 34, 38, 42, 43, 44, 45, 46, 59],
    indicatorNames: ['废水产生量', '废水中铜产生量', '废水中COD产生量', '废水收集与处理', '废气收集与处理', '一般固体废物收集与处理', '危险废物收集与处理', '噪声', '污染物排放监测'],
    investment: 240,
    paybackPeriod: 3.5,
    status: 'active',
    createdAt: '2025-03-05'
  },
  {
    id: 95,
    name: '清洁生产大数据分析系统',
    type: '管理改进',
    problemSolved: '清洁生产大数据分析不完善，数据分析不深入，清洁生产优化不充分，清洁生产效果不理想',
    description: '建立清洁生产大数据分析系统，配置大数据分析设备，建立数据分析模型，制定大数据管理制度，开展大数据分析优化',
    economicBenefit: '每万平方米线路板通过清洁生产大数据分析节约成本5.8万元，提高清洁生产效果42%',
    environmentalBenefit: '每万平方米线路板提高清洁生产效果，减少污染物排放，提高资源利用效率',
    indicatorIds: [54, 57, 58, 60, 62, 64],
    indicatorNames: ['环保法律法规执行情况', '清洁生产审核', '节能管理', '危险化学品管理', '固体废物管理', '运输方式'],
    investment: 160,
    paybackPeriod: 2.8,
    status: 'active',
    createdAt: '2025-03-10'
  },
  {
    id: 96,
    name: '生产线人工智能优化系统',
    type: '技术改造',
    problemSolved: '生产线人工智能应用不充分，智能优化不深入，生产管理效率低，质量控制不精准',
    description: '建立生产线人工智能优化系统，配置人工智能设备，建立智能优化模型，制定人工智能管理制度，开展人工智能优化',
    economicBenefit: '每万平方米线路板节约管理成本3.5万元，提高生产管理效率60%，提高质量控制精度',
    environmentalBenefit: '每万平方米线路板提高生产管理效率，减少资源浪费',
    indicatorIds: [1, 2, 7, 9, 12, 20, 28],
    indicatorNames: ['生产工艺与装备', '机械加工及辅助设施', '单位能耗', '自动化水平', '覆铜板利用率', '金属铜回收率'],
    investment: 350,
    paybackPeriod: 4.2,
    status: 'active',
    createdAt: '2025-03-15'
  },
  {
    id: 97,
    name: '废水处理人工智能优化系统',
    type: '环保治理',
    problemSolved: '废水处理人工智能应用不充分，智能优化不深入，处理效果不稳定，运行成本高',
    description: '建立废水处理人工智能优化系统，配置人工智能设备，建立智能优化模型，制定人工智能管理制度，开展人工智能优化',
    economicBenefit: '每万平方米线路板节约废水处理成本3万元，提高处理效率40%',
    environmentalBenefit: '每万平方米线路板提高废水处理效果，减少污染物排放',
    indicatorIds: [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42],
    indicatorNames: ['废水产生量', '废水中铜产生量', '废水中COD产生量', '废水收集与处理'],
    investment: 300,
    paybackPeriod: 4.5,
    status: 'active',
    createdAt: '2025-03-20'
  },
  {
    id: 98,
    name: '废气处理人工智能优化系统',
    type: '环保治理',
    problemSolved: '废气处理人工智能应用不充分，智能优化不深入，处理效果不稳定，运行成本高',
    description: '建立废气处理人工智能优化系统，配置人工智能设备，建立智能优化模型，制定人工智能管理制度，开展人工智能优化',
    economicBenefit: '每万平方米线路板节约废气处理成本2.5万元，提高处理效率35%',
    environmentalBenefit: '每万平方米线路板提高废气处理效果，减少大气污染物排放',
    indicatorIds: [43],
    indicatorNames: ['废气收集与处理'],
    investment: 260,
    paybackPeriod: 4.8,
    status: 'active',
    createdAt: '2025-03-25'
  },
  {
    id: 99,
    name: '固体废物处理人工智能优化系统',
    type: '环保治理',
    problemSolved: '固体废物处理人工智能应用不充分，智能优化不深入，处理效率低，运行成本高',
    description: '建立固体废物处理人工智能优化系统，配置人工智能设备，建立智能优化模型，制定人工智能管理制度，开展人工智能优化',
    economicBenefit: '每万平方米线路板节约废物处理成本2.8万元，提高处理效率45%',
    environmentalBenefit: '每万平方米线路板提高废物处理效率，减少废物产生量',
    indicatorIds: [29, 44, 45],
    indicatorNames: ['一般工业固体废物综合利用率', '一般固体废物收集与处理', '危险废物收集与处理'],
    investment: 240,
    paybackPeriod: 4.0,
    status: 'active',
    createdAt: '2025-03-30'
  },
  {
    id: 100,
    name: '能源管理人工智能优化系统',
    type: '管理改进',
    problemSolved: '能源管理人工智能应用不充分，智能优化不深入，能源利用效率低，节能潜力挖掘不足',
    description: '建立能源管理人工智能优化系统，配置人工智能设备，建立智能优化模型，制定人工智能管理制度，开展人工智能优化',
    economicBenefit: '每万平方米线路板节约能源成本4万元，提高能源利用效率35%',
    environmentalBenefit: '每万平方米线路板减少能源消耗，降低温室气体排放',
    indicatorIds: [7, 8, 9, 10, 11, 12, 13, 14, 47, 58],
    indicatorNames: ['单位产品电耗', '温室气体排放', '节能管理'],
    investment: 220,
    paybackPeriod: 3.5,
    status: 'active',
    createdAt: '2025-04-01'
  },
  {
    id: 101,
    name: '水资源管理人工智能优化系统',
    type: '管理改进',
    problemSolved: '水资源管理人工智能应用不充分，智能优化不深入，水资源利用效率低，水资源浪费严重',
    description: '建立水资源管理人工智能优化系统，配置人工智能设备，建立智能优化模型，制定人工智能管理制度，开展人工智能优化',
    economicBenefit: '每万平方米线路板节约水资源成本3万元，提高水资源利用效率40%',
    environmentalBenefit: '每万平方米线路板减少水资源消耗，提高水资源利用效率',
    indicatorIds: [15, 16, 17, 18, 19, 30, 31, 32, 33],
    indicatorNames: ['单位产品新鲜水耗', '水资源重复利用率', '废水产生量'],
    investment: 200,
    paybackPeriod: 3.2,
    status: 'active',
    createdAt: '2025-04-05'
  },
  {
    id: 102,
    name: '原材料管理人工智能优化系统',
    type: '管理改进',
    problemSolved: '原材料管理人工智能应用不充分，智能优化不深入，原材料利用率不高，原材料浪费严重',
    description: '建立原材料管理人工智能优化系统，配置人工智能设备，建立智能优化模型，制定人工智能管理制度，开展人工智能优化',
    economicBenefit: '每万平方米线路板节约原材料成本4.5万元，提高原材料利用率30%',
    environmentalBenefit: '每万平方米线路板减少原材料浪费，提高原材料利用效率',
    indicatorIds: [20, 21, 22, 23, 24, 25, 26, 27, 28],
    indicatorNames: ['覆铜板利用率', '金属铜回收率'],
    investment: 180,
    paybackPeriod: 3.0,
    status: 'active',
    createdAt: '2025-04-10'
  },
  {
    id: 103,
    name: '生产工艺人工智能优化系统',
    type: '技术改造',
    problemSolved: '生产工艺人工智能应用不充分，智能优化不深入，生产效率低，产品质量不稳定',
    description: '建立生产工艺人工智能优化系统，配置人工智能设备，建立智能优化模型，制定人工智能管理制度，开展人工智能优化',
    economicBenefit: '每万平方米线路板节约生产成本5万元，提高生产效率45%，提高产品质量',
    environmentalBenefit: '每万平方米线路板提高生产工艺效率，减少资源浪费',
    indicatorIds: [1, 2, 3, 4, 5, 6, 7, 9, 12, 20, 28, 30, 34, 38, 43],
    indicatorNames: ['生产工艺与装备', '机械加工及辅助设施', '线路与阻焊图形形成', '板面清洗', '蚀刻', '电镀与化学镀', '单位能耗', '自动化水平', '覆铜板利用率', '金属铜回收率', '废水产生量', '废水中铜', '废水中COD', '废气收集与处理'],
    investment: 300,
    paybackPeriod: 4.0,
    status: 'active',
    createdAt: '2025-04-15'
  },
  {
    id: 104,
    name: '环保设施人工智能优化系统',
    type: '环保治理',
    problemSolved: '环保设施人工智能应用不充分，智能优化不深入，环保效果不理想，设施运行效率低',
    description: '建立环保设施人工智能优化系统，配置人工智能设备，建立智能优化模型，制定人工智能管理制度，开展人工智能优化',
    economicBenefit: '每万平方米线路板节约环保设施运行成本3.5万元，提高设施运行效率40%',
    environmentalBenefit: '每万平方米线路板提高环保设施运行效果，减少污染物排放',
    indicatorIds: [30, 34, 38, 42, 43, 44, 45, 46, 59],
    indicatorNames: ['废水产生量', '废水中铜产生量', '废水中COD产生量', '废水收集与处理', '废气收集与处理', '一般固体废物收集与处理', '危险废物收集与处理', '噪声', '污染物排放监测'],
    investment: 260,
    paybackPeriod: 3.8,
    status: 'active',
    createdAt: '2025-04-20'
  },
  {
    id: 105,
    name: '清洁生产人工智能优化系统',
    type: '管理改进',
    problemSolved: '清洁生产人工智能应用不充分，智能优化不深入，清洁生产效果不理想，持续改进机制不健全',
    description: '建立清洁生产人工智能优化系统，配置人工智能设备，建立智能优化模型，制定人工智能管理制度，开展人工智能优化',
    economicBenefit: '每万平方米线路板通过清洁生产人工智能优化节约成本6万元，提高清洁生产效果45%',
    environmentalBenefit: '每万平方米线路板提高清洁生产效果，减少污染物排放，提高资源利用效率',
    indicatorIds: [54, 57, 58, 60, 62, 64],
    indicatorNames: ['环保法律法规执行情况', '清洁生产审核', '节能管理', '危险化学品管理', '固体废物管理', '运输方式'],
    investment: 180,
    paybackPeriod: 3.0,
    status: 'active',
    createdAt: '2025-04-25'
  },
  {
    id: 106,
    name: '生产线云计算管理系统',
    type: '技术改造',
    problemSolved: '生产线云计算应用不充分，云端管理不完善，数据共享不充分，生产管理效率低',
    description: '建立生产线云计算管理系统，配置云计算设备，建立云端管理平台，制定云计算管理制度，开展云计算管理优化',
    economicBenefit: '每万平方米线路板节约管理成本3.8万元，提高生产管理效率65%，提高数据共享效率',
    environmentalBenefit: '每万平方米线路板提高生产管理效率，减少资源浪费',
    indicatorIds: [1, 2, 7, 9, 12, 20, 28],
    indicatorNames: ['生产工艺与装备', '机械加工及辅助设施', '单位能耗', '自动化水平', '覆铜板利用率', '金属铜回收率'],
    investment: 380,
    paybackPeriod: 4.5,
    status: 'active',
    createdAt: '2025-04-30'
  },
  {
    id: 107,
    name: '废水处理云计算管理系统',
    type: '环保治理',
    problemSolved: '废水处理云计算应用不充分，云端管理不完善，数据共享不充分，处理效果不稳定',
    description: '建立废水处理云计算管理系统，配置云计算设备，建立云端管理平台，制定云计算管理制度，开展云计算管理优化',
    economicBenefit: '每万平方米线路板节约废水处理成本3.2万元，提高处理效率42%',
    environmentalBenefit: '每万平方米线路板提高废水处理效果，减少污染物排放',
    indicatorIds: [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42],
    indicatorNames: ['废水产生量', '废水中铜产生量', '废水中COD产生量', '废水收集与处理'],
    investment: 320,
    paybackPeriod: 4.8,
    status: 'active',
    createdAt: '2025-05-01'
  },
  {
    id: 108,
    name: '废气处理云计算管理系统',
    type: '环保治理',
    problemSolved: '废气处理云计算应用不充分，云端管理不完善，数据共享不充分，处理效果不稳定',
    description: '建立废气处理云计算管理系统，配置云计算设备，建立云端管理平台，制定云计算管理制度，开展云计算管理优化',
    economicBenefit: '每万平方米线路板节约废气处理成本2.8万元，提高处理效率38%',
    environmentalBenefit: '每万平方米线路板提高废气处理效果，减少大气污染物排放',
    indicatorIds: [43],
    indicatorNames: ['废气收集与处理'],
    investment: 280,
    paybackPeriod: 5.0,
    status: 'active',
    createdAt: '2025-05-05'
  },
  {
    id: 109,
    name: '固体废物处理云计算管理系统',
    type: '环保治理',
    problemSolved: '固体废物处理云计算应用不充分，云端管理不完善，数据共享不充分，处理效率低',
    description: '建立固体废物处理云计算管理系统，配置云计算设备，建立云端管理平台，制定云计算管理制度，开展云计算管理优化',
    economicBenefit: '每万平方米线路板节约废物处理成本3万元，提高处理效率48%',
    environmentalBenefit: '每万平方米线路板提高废物处理效率，减少废物产生量',
    indicatorIds: [29, 44, 45],
    indicatorNames: ['一般工业固体废物综合利用率', '一般固体废物收集与处理', '危险废物收集与处理'],
    investment: 260,
    paybackPeriod: 4.2,
    status: 'active',
    createdAt: '2025-05-10'
  },
  {
    id: 110,
    name: '能源管理云计算管理系统',
    type: '管理改进',
    problemSolved: '能源管理云计算应用不充分，云端管理不完善，数据共享不充分，能源利用效率低',
    description: '建立能源管理云计算管理系统，配置云计算设备，建立云端管理平台，制定云计算管理制度，开展云计算管理优化',
    economicBenefit: '每万平方米线路板节约能源成本4.2万元，提高能源利用效率38%',
    environmentalBenefit: '每万平方米线路板减少能源消耗，降低温室气体排放',
    indicatorIds: [7, 8, 9, 10, 11, 12, 13, 14, 47, 58],
    indicatorNames: ['单位产品电耗', '温室气体排放', '节能管理'],
    investment: 240,
    paybackPeriod: 3.8,
    status: 'active',
    createdAt: '2025-05-15'
  },
  {
    id: 111,
    name: '水资源管理云计算管理系统',
    type: '管理改进',
    problemSolved: '水资源管理云计算应用不充分，云端管理不完善，数据共享不充分，水资源利用效率低',
    description: '建立水资源管理云计算管理系统，配置云计算设备，建立云端管理平台，制定云计算管理制度，开展云计算管理优化',
    economicBenefit: '每万平方米线路板节约水资源成本3.2万元，提高水资源利用效率42%',
    environmentalBenefit: '每万平方米线路板减少水资源消耗，提高水资源利用效率',
    indicatorIds: [15, 16, 17, 18, 19, 30, 31, 32, 33],
    indicatorNames: ['单位产品新鲜水耗', '水资源重复利用率', '废水产生量'],
    investment: 220,
    paybackPeriod: 3.5,
    status: 'active',
    createdAt: '2025-05-20'
  },
  {
    id: 112,
    name: '原材料管理云计算管理系统',
    type: '管理改进',
    problemSolved: '原材料管理云计算应用不充分，云端管理不完善，数据共享不充分，原材料利用率不高',
    description: '建立原材料管理云计算管理系统，配置云计算设备，建立云端管理平台，制定云计算管理制度，开展云计算管理优化',
    economicBenefit: '每万平方米线路板节约原材料成本4.8万元，提高原材料利用率32%',
    environmentalBenefit: '每万平方米线路板减少原材料浪费，提高原材料利用效率',
    indicatorIds: [20, 21, 22, 23, 24, 25, 26, 27, 28],
    indicatorNames: ['覆铜板利用率', '金属铜回收率'],
    investment: 200,
    paybackPeriod: 3.2,
    status: 'active',
    createdAt: '2025-05-25'
  },
  {
    id: 113,
    name: '生产工艺云计算管理系统',
    type: '技术改造',
    problemSolved: '生产工艺云计算应用不充分，云端管理不完善，数据共享不充分，生产效率低',
    description: '建立生产工艺云计算管理系统，配置云计算设备，建立云端管理平台，制定云计算管理制度，开展云计算管理优化',
    economicBenefit: '每万平方米线路板节约生产成本5.2万元，提高生产效率48%，提高产品质量',
    environmentalBenefit: '每万平方米线路板提高生产工艺效率，减少资源浪费',
    indicatorIds: [1, 2, 3, 4, 5, 6, 7, 9, 12, 20, 28, 30, 34, 38, 43],
    indicatorNames: ['生产工艺与装备', '机械加工及辅助设施', '线路与阻焊图形形成', '板面清洗', '蚀刻', '电镀与化学镀', '单位能耗', '自动化水平', '覆铜板利用率', '金属铜回收率', '废水产生量', '废水中铜', '废水中COD', '废气收集与处理'],
    investment: 320,
    paybackPeriod: 4.2,
    status: 'active',
    createdAt: '2025-05-30'
  },
  {
    id: 114,
    name: '环保设施云计算管理系统',
    type: '环保治理',
    problemSolved: '环保设施云计算应用不充分，云端管理不完善，数据共享不充分，环保效果不理想',
    description: '建立环保设施云计算管理系统，配置云计算设备，建立云端管理平台，制定云计算管理制度，开展云计算管理优化',
    economicBenefit: '每万平方米线路板节约环保设施运行成本3.8万元，提高设施运行效率42%',
    environmentalBenefit: '每万平方米线路板提高环保设施运行效果，减少污染物排放',
    indicatorIds: [30, 34, 38, 42, 43, 44, 45, 46, 59],
    indicatorNames: ['废水产生量', '废水中铜产生量', '废水中COD产生量', '废水收集与处理', '废气收集与处理', '一般固体废物收集与处理', '危险废物收集与处理', '噪声', '污染物排放监测'],
    investment: 280,
    paybackPeriod: 4.0,
    status: 'active',
    createdAt: '2025-06-01'
  },
  {
    id: 115,
    name: '清洁生产云计算管理系统',
    type: '管理改进',
    problemSolved: '清洁生产云计算应用不充分，云端管理不完善，数据共享不充分，清洁生产效果不理想',
    description: '建立清洁生产云计算管理系统，配置云计算设备，建立云端管理平台，制定云计算管理制度，开展云计算管理优化',
    economicBenefit: '每万平方米线路板通过清洁生产云计算管理节约成本6.2万元，提高清洁生产效果48%',
    environmentalBenefit: '每万平方米线路板提高清洁生产效果，减少污染物排放，提高资源利用效率',
    indicatorIds: [54, 57, 58, 60, 62, 64],
    indicatorNames: ['环保法律法规执行情况', '清洁生产审核', '节能管理', '危险化学品管理', '固体废物管理', '运输方式'],
    investment: 200,
    paybackPeriod: 3.2,
    status: 'active',
    createdAt: '2025-06-05'
  },
  {
    id: 116,
    name: '生产线区块链管理系统',
    type: '技术改造',
    problemSolved: '生产线区块链应用不充分，数据安全不完善，数据追溯不充分，生产管理效率低',
    description: '建立生产线区块链管理系统，配置区块链设备，建立数据安全平台，制定区块链管理制度，开展区块链管理优化',
    economicBenefit: '每万平方米线路板节约管理成本4万元，提高生产管理效率70%，提高数据安全等级',
    environmentalBenefit: '每万平方米线路板提高生产管理效率，减少资源浪费',
    indicatorIds: [1, 2, 7, 9, 12, 20, 28],
    indicatorNames: ['生产工艺与装备', '机械加工及辅助设施', '单位能耗', '自动化水平', '覆铜板利用率', '金属铜回收率'],
    investment: 400,
    paybackPeriod: 4.8,
    status: 'active',
    createdAt: '2025-06-10'
  },
  {
    id: 117,
    name: '废水处理区块链管理系统',
    type: '环保治理',
    problemSolved: '废水处理区块链应用不充分，数据安全不完善，数据追溯不充分，处理效果不稳定',
    description: '建立废水处理区块链管理系统，配置区块链设备，建立数据安全平台，制定区块链管理制度，开展区块链管理优化',
    economicBenefit: '每万平方米线路板节约废水处理成本3.5万元，提高处理效率45%',
    environmentalBenefit: '每万平方米线路板提高废水处理效果，减少污染物排放',
    indicatorIds: [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42],
    indicatorNames: ['废水产生量', '废水中铜产生量', '废水中COD产生量', '废水收集与处理'],
    investment: 340,
    paybackPeriod: 5.0,
    status: 'active',
    createdAt: '2025-06-15'
  },
  {
    id: 118,
    name: '废气处理区块链管理系统',
    type: '环保治理',
    problemSolved: '废气处理区块链应用不充分，数据安全不完善，数据追溯不充分，处理效果不稳定',
    description: '建立废气处理区块链管理系统，配置区块链设备，建立数据安全平台，制定区块链管理制度，开展区块链管理优化',
    economicBenefit: '每万平方米线路板节约废气处理成本3万元，提高处理效率40%',
    environmentalBenefit: '每万平方米线路板提高废气处理效果，减少大气污染物排放',
    indicatorIds: [43],
    indicatorNames: ['废气收集与处理'],
    investment: 300,
    paybackPeriod: 5.2,
    status: 'active',
    createdAt: '2025-06-20'
  },
  {
    id: 119,
    name: '固体废物处理区块链管理系统',
    type: '环保治理',
    problemSolved: '固体废物处理区块链应用不充分，数据安全不完善，数据追溯不充分，处理效率低',
    description: '建立固体废物处理区块链管理系统，配置区块链设备，建立数据安全平台，制定区块链管理制度，开展区块链管理优化',
    economicBenefit: '每万平方米线路板节约废物处理成本3.2万元，提高处理效率50%',
    environmentalBenefit: '每万平方米线路板提高废物处理效率，减少废物产生量',
    indicatorIds: [29, 44, 45],
    indicatorNames: ['一般工业固体废物综合利用率', '一般固体废物收集与处理', '危险废物收集与处理'],
    investment: 280,
    paybackPeriod: 4.5,
    status: 'active',
    createdAt: '2025-06-25'
  },
  {
    id: 120,
    name: '能源管理区块链管理系统',
    type: '管理改进',
    problemSolved: '能源管理区块链应用不充分，数据安全不完善，数据追溯不充分，能源利用效率低',
    description: '建立能源管理区块链管理系统，配置区块链设备，建立数据安全平台，制定区块链管理制度，开展区块链管理优化',
    economicBenefit: '每万平方米线路板节约能源成本4.5万元，提高能源利用效率40%',
    environmentalBenefit: '每万平方米线路板减少能源消耗，降低温室气体排放',
    indicatorIds: [7, 8, 9, 10, 11, 12, 13, 14, 47, 58],
    indicatorNames: ['单位产品电耗', '温室气体排放', '节能管理'],
    investment: 260,
    paybackPeriod: 4.0,
    status: 'active',
    createdAt: '2025-06-30'
  },
  {
    id: 121,
    name: '水资源管理区块链管理系统',
    type: '管理改进',
    problemSolved: '水资源管理区块链应用不充分，数据安全不完善，数据追溯不充分，水资源利用效率低',
    description: '建立水资源管理区块链管理系统，配置区块链设备，建立数据安全平台，制定区块链管理制度，开展区块链管理优化',
    economicBenefit: '每万平方米线路板节约水资源成本3.5万元，提高水资源利用效率45%',
    environmentalBenefit: '每万平方米线路板减少水资源消耗，提高水资源利用效率',
    indicatorIds: [15, 16, 17, 18, 19, 30, 31, 32, 33],
    indicatorNames: ['单位产品新鲜水耗', '水资源重复利用率', '废水产生量'],
    investment: 240,
    paybackPeriod: 3.8,
    status: 'active',
    createdAt: '2025-07-01'
  },
  {
    id: 122,
    name: '原材料管理区块链管理系统',
    type: '管理改进',
    problemSolved: '原材料管理区块链应用不充分，数据安全不完善，数据追溯不充分，原材料利用率不高',
    description: '建立原材料管理区块链管理系统，配置区块链设备，建立数据安全平台，制定区块链管理制度，开展区块链管理优化',
    economicBenefit: '每万平方米线路板节约原材料成本5万元，提高原材料利用率35%',
    environmentalBenefit: '每万平方米线路板减少原材料浪费，提高原材料利用效率',
    indicatorIds: [20, 21, 22, 23, 24, 25, 26, 27, 28],
    indicatorNames: ['覆铜板利用率', '金属铜回收率'],
    investment: 220,
    paybackPeriod: 3.5,
    status: 'active',
    createdAt: '2025-07-05'
  },
  {
    id: 123,
    name: '生产工艺区块链管理系统',
    type: '技术改造',
    problemSolved: '生产工艺区块链应用不充分，数据安全不完善，数据追溯不充分，生产效率低',
    description: '建立生产工艺区块链管理系统，配置区块链设备，建立数据安全平台，制定区块链管理制度，开展区块链管理优化',
    economicBenefit: '每万平方米线路板节约生产成本5.5万元，提高生产效率50%，提高产品质量',
    environmentalBenefit: '每万平方米线路板提高生产工艺效率，减少资源浪费',
    indicatorIds: [1, 2, 3, 4, 5, 6, 7, 9, 12, 20, 28, 30, 34, 38, 43],
    indicatorNames: ['生产工艺与装备', '机械加工及辅助设施', '线路与阻焊图形形成', '板面清洗', '蚀刻', '电镀与化学镀', '单位能耗', '自动化水平', '覆铜板利用率', '金属铜回收率', '废水产生量', '废水中铜', '废水中COD', '废气收集与处理'],
    investment: 340,
    paybackPeriod: 4.5,
    status: 'active',
    createdAt: '2025-07-10'
  },
  {
    id: 124,
    name: '环保设施区块链管理系统',
    type: '环保治理',
    problemSolved: '环保设施区块链应用不充分，数据安全不完善，数据追溯不充分，环保效果不理想',
    description: '建立环保设施区块链管理系统，配置区块链设备，建立数据安全平台，制定区块链管理制度，开展区块链管理优化',
    economicBenefit: '每万平方米线路板节约环保设施运行成本4万元，提高设施运行效率45%',
    environmentalBenefit: '每万平方米线路板提高环保设施运行效果，减少污染物排放',
    indicatorIds: [30, 34, 38, 42, 43, 44, 45, 46, 59],
    indicatorNames: ['废水产生量', '废水中铜产生量', '废水中COD产生量', '废水收集与处理', '废气收集与处理', '一般固体废物收集与处理', '危险废物收集与处理', '噪声', '污染物排放监测'],
    investment: 300,
    paybackPeriod: 4.2,
    status: 'active',
    createdAt: '2025-07-15'
  },
  {
    id: 125,
    name: '清洁生产区块链管理系统',
    type: '管理改进',
    problemSolved: '清洁生产区块链应用不充分，数据安全不完善，数据追溯不充分，清洁生产效果不理想',
    description: '建立清洁生产区块链管理系统，配置区块链设备，建立数据安全平台，制定区块链管理制度，开展区块链管理优化',
    economicBenefit: '每万平方米线路板通过清洁生产区块链管理节约成本6.5万元，提高清洁生产效果50%',
    environmentalBenefit: '每万平方米线路板提高清洁生产效果，减少污染物排放，提高资源利用效率',
    indicatorIds: [54, 57, 58, 60, 62, 64],
    indicatorNames: ['环保法律法规执行情况', '清洁生产审核', '节能管理', '危险化学品管理', '固体废物管理', '运输方式'],
    investment: 220,
    paybackPeriod: 3.5,
    status: 'active',
    createdAt: '2025-07-20'
  },
  {
    id: 126,
    name: '生产线5G通信管理系统',
    type: '技术改造',
    problemSolved: '生产线5G通信应用不充分，通信效率不高，数据传输不充分，生产管理效率低',
    description: '建立生产线5G通信管理系统，配置5G通信设备，建立高速通信网络，制定5G通信管理制度，开展5G通信管理优化',
    economicBenefit: '每万平方米线路板节约管理成本4.2万元，提高生产管理效率75%，提高通信效率',
    environmentalBenefit: '每万平方米线路板提高生产管理效率，减少资源浪费',
    indicatorIds: [1, 2, 7, 9, 12, 20, 28],
    indicatorNames: ['生产工艺与装备', '机械加工及辅助设施', '单位能耗', '自动化水平', '覆铜板利用率', '金属铜回收率'],
    investment: 420,
    paybackPeriod: 5.0,
    status: 'active',
    createdAt: '2025-07-25'
  },
  {
    id: 127,
    name: '废水处理5G通信管理系统',
    type: '环保治理',
    problemSolved: '废水处理5G通信应用不充分，通信效率不高，数据传输不充分，处理效果不稳定',
    description: '建立废水处理5G通信管理系统，配置5G通信设备，建立高速通信网络，制定5G通信管理制度，开展5G通信管理优化',
    economicBenefit: '每万平方米线路板节约废水处理成本3.8万元，提高处理效率48%',
    environmentalBenefit: '每万平方米线路板提高废水处理效果，减少污染物排放',
    indicatorIds: [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42],
    indicatorNames: ['废水产生量', '废水中铜产生量', '废水中COD产生量', '废水收集与处理'],
    investment: 360,
    paybackPeriod: 5.2,
    status: 'active',
    createdAt: '2025-07-30'
  },
  {
    id: 128,
    name: '废气处理5G通信管理系统',
    type: '环保治理',
    problemSolved: '废气处理5G通信应用不充分，通信效率不高，数据传输不充分，处理效果不稳定',
    description: '建立废气处理5G通信管理系统，配置5G通信设备，建立高速通信网络，制定5G通信管理制度，开展5G通信管理优化',
    economicBenefit: '每万平方米线路板节约废气处理成本3.2万元，提高处理效率42%',
    environmentalBenefit: '每万平方米线路板提高废气处理效果，减少大气污染物排放',
    indicatorIds: [43],
    indicatorNames: ['废气收集与处理'],
    investment: 320,
    paybackPeriod: 5.5,
    status: 'active',
    createdAt: '2025-08-01'
  },
  {
    id: 129,
    name: '固体废物处理5G通信管理系统',
    type: '环保治理',
    problemSolved: '固体废物处理5G通信应用不充分，通信效率不高，数据传输不充分，处理效率低',
    description: '建立固体废物处理5G通信管理系统，配置5G通信设备，建立高速通信网络，制定5G通信管理制度，开展5G通信管理优化',
    economicBenefit: '每万平方米线路板节约废物处理成本3.5万元，提高处理效率52%',
    environmentalBenefit: '每万平方米线路板提高废物处理效率，减少废物产生量',
    indicatorIds: [29, 44, 45],
    indicatorNames: ['一般工业固体废物综合利用率', '一般固体废物收集与处理', '危险废物收集与处理'],
    investment: 300,
    paybackPeriod: 4.8,
    status: 'active',
    createdAt: '2025-08-05'
  }
]

// 指标树数据
const mockIndicatorTree = [
  {
    label: '生产工艺与装备要求',
    key: 'process',
    children: [
      { label: '基本要求', key: '1' },
      { label: '机械加工及辅助设施', key: '2' },
      { label: '线路与阻焊图形形成(印刷或感光工艺)', key: '3' },
      { label: '板面清洗', key: '4' },
      { label: '蚀刻', key: '5' },
      { label: '电镀与化学镀', key: '6' }
    ]
  },
  {
    label: '能源消耗',
    key: 'energy',
    children: [
      { label: '刚性印制电路单面板(单位产品电耗)', key: '7' },
      { label: '刚性印制电路双面板(单位产品电耗)', key: '8' },
      { label: '刚性印制电路多层板(单位产品电耗)', key: '9' },
      { label: '刚性印制电路HDI板(单位产品电耗)', key: '10' },
      { label: '挠性印制电路单面板(单位产品电耗)', key: '11' },
      { label: '挠性印制电路双面板(单位产品电耗)', key: '12' },
      { label: '挠性印制电路多层板(单位产品电耗)', key: '13' },
      { label: '挠性印制电路HDI板(单位产品电耗)', key: '14' }
    ]
  },
  {
    label: '水资源消耗',
    key: 'water',
    children: [
      { label: '单面板(单位产品新鲜水耗)', key: '15' },
      { label: '双面板(单位产品新鲜水耗)', key: '16' },
      { label: '多层板(单位产品新鲜水耗)', key: '17' },
      { label: 'HDI板(单位产品新鲜水耗)', key: '18' },
      { label: '水资源重复利用率', key: '19' }
    ]
  },
  {
    label: '原/辅料消耗',
    key: 'material',
    children: [
      { label: '刚性印制电路单面板覆铜板利用率', key: '20' },
      { label: '刚性印制电路双面板覆铜板利用率', key: '21' },
      { label: '刚性印制电路多层板覆铜板利用率', key: '22' },
      { label: '刚性印制电路HDI板覆铜板利用率', key: '23' },
      { label: '挠性印制电路单面板覆铜板利用率', key: '24' },
      { label: '挠性印制电路双面板覆铜板利用率', key: '25' },
      { label: '挠性印制电路多层板覆铜板利用率', key: '26' },
      { label: '挠性印制电路HDI板覆铜板利用率', key: '27' }
    ]
  },
  {
    label: '资源综合利用',
    key: 'resource',
    children: [
      { label: '金属铜回收率', key: '28' },
      { label: '一般工业固体废物综合利用率', key: '29' }
    ]
  },
  {
    label: '废水的产生与排放',
    key: 'wastewater',
    children: [
      { label: '单面板废水产生量', key: '30' },
      { label: '双面板废水产生量', key: '31' },
      { label: '多层板废水产生量', key: '32' },
      { label: 'HDI板废水产生量', key: '33' },
      { label: '单面板废水中铜产生量', key: '34' },
      { label: '双面板废水中铜产生量', key: '35' },
      { label: '多层板废水中铜产生量', key: '36' },
      { label: 'HDI板废水中铜产生量', key: '37' },
      { label: '单面板废水中COD产生量', key: '38' },
      { label: '双面板废水中COD产生量', key: '39' },
      { label: '多层板废水中COD产生量', key: '40' },
      { label: 'HDI板废水中COD产生量', key: '41' },
      { label: '废水收集与处理', key: '42' }
    ]
  },
  {
    label: '废气的产生与排放',
    key: 'wastegas',
    children: [
      { label: '废气收集与处理', key: '43' }
    ]
  },
  {
    label: '固体废物的产生与排放',
    key: 'solidwaste',
    children: [
      { label: '一般固体废物收集与处理', key: '44' },
      { label: '危险废物收集与处理', key: '45' }
    ]
  },
  {
    label: '噪声的产生与排放',
    key: 'noise',
    children: [
      { label: '噪声', key: '46' }
    ]
  },
  {
    label: '温室气体排放',
    key: 'greenhouse',
    children: [
      { label: '温室气体排放', key: '47' }
    ]
  },
  {
    label: '产品特征',
    key: 'product',
    children: [
      { label: '产品特征', key: '50' }
    ]
  },
  {
    label: '清洁生产管理',
    key: 'management',
    children: [
      { label: '环保法律法规执行情况', key: '54' },
      { label: '清洁生产审核', key: '57' },
      { label: '节能管理', key: '58' },
      { label: '危险化学品管理', key: '60' },
      { label: '固体废物管理', key: '62' },
      { label: '运输方式', key: '64' }
    ]
  }
]

// 数据完整性验证函数
const validateSchemeData = () => {
  const schemesWithoutIndicators = mockSchemeLibrary.filter(scheme => 
    !scheme.indicatorIds || scheme.indicatorIds.length === 0
  )
  
  const schemesWithInvalidIndicators = mockSchemeLibrary.filter(scheme => 
    scheme.indicatorIds && scheme.indicatorIds.some(id => id < 1 || id > 64)
  )
  
  const indicatorCoverage = {}
  for (let i = 1; i <= 64; i++) {
    const relatedSchemes = mockSchemeLibrary.filter(scheme => 
      scheme.indicatorIds && scheme.indicatorIds.includes(i)
    )
    indicatorCoverage[i] = relatedSchemes.length
  }
  
  return {
    totalSchemes: mockSchemeLibrary.length,
    schemesWithoutIndicators: schemesWithoutIndicators.length,
    schemesWithInvalidIndicators: schemesWithInvalidIndicators.length,
    indicatorCoverage: indicatorCoverage,
    isValid: schemesWithoutIndicators.length === 0 && schemesWithInvalidIndicators.length === 0
  }
}

// 验证数据完整性
const validationResult = validateSchemeData()
console.log('方案库数据验证结果:', validationResult)

// 指标-方案映射表
const buildMappingTable = () => {
  const indicatorToSchemes = new Map();
  const schemeToIndicators = new Map();

  // 初始化64个指标的映射
  for (let i = 1; i <= 64; i++) {
    indicatorToSchemes.set(i, []);
  }

  // 遍历所有方案建立双向映射
  mockSchemeLibrary.forEach(scheme => {
    // 方案到指标的映射
    schemeToIndicators.set(scheme.id, {
      schemeInfo: {
        id: scheme.id,
        name: scheme.name,
        type: scheme.type,
        description: scheme.description,
        economicBenefit: scheme.economicBenefit,
        environmentalBenefit: scheme.environmentalBenefit,
        investment: scheme.investment,
        paybackPeriod: scheme.paybackPeriod
      },
      indicators: scheme.indicatorIds
    });

    // 指标到方案的映射
    scheme.indicatorIds.forEach(indicatorId => {
      const schemes = indicatorToSchemes.get(indicatorId) || [];
      schemes.push({
        id: scheme.id,
        name: scheme.name,
        type: scheme.type,
        description: scheme.description
      });
      indicatorToSchemes.set(indicatorId, schemes);
    });
  });

  return {
    indicatorToSchemes,
    schemeToIndicators
  };
};

// 建立映射表
const mappingTable = buildMappingTable();

// Mock API定义
export const mockDetailApi = {
  // 筹划与组织相关
  getAuditTeam: (enterpriseId) => {
    return Promise.resolve({ data: mockPlanningData.auditTeam })
  },
  
  getWorkPlans: (enterpriseId) => {
    return Promise.resolve({ data: mockPlanningData.workPlans })
  },
  
  getTrainingRecords: (enterpriseId) => {
    return Promise.resolve({ data: mockPlanningData.trainingRecords })
  },
  
  // 审核结果相关 - 返回完整的64项指标数据
  getAuditResults: (enterpriseId) => {
    return Promise.resolve({ data: mockIndicators })
  },
  
  // 获取推荐方案
  getRecommendedSchemes: (enterpriseId, indicatorId) => {
    const schemes = getRecommendedSchemes(indicatorId);
    return Promise.resolve({ data: schemes });
  },
  
  // 方案库相关
  getSchemes: (enterpriseId, params = {}) => {
    const { page = 1, pageSize = 10, name = '', indicatorIds = [] } = params
    let filteredSchemes = mockSchemeLibrary

    // 如果指定了指标ID，使用映射表获取相关方案
    if (indicatorIds && indicatorIds.length > 0) {
      const relatedSchemes = new Set();
      indicatorIds.forEach(id => {
        const schemes = mappingTable.indicatorToSchemes.get(parseInt(id)) || [];
        schemes.forEach(scheme => relatedSchemes.add(scheme.id));
      });
      
      filteredSchemes = mockSchemeLibrary.filter(scheme => 
        relatedSchemes.has(scheme.id)
      );
    }
    
    // 预处理数据，确保所有方案都有indicatorNames字段
    const preprocessedSchemes = filteredSchemes.map(scheme => {
      if (scheme.indicatorIds && scheme.indicatorIds.length > 0 && (!scheme.indicatorNames || scheme.indicatorNames.length === 0)) {
        const indicatorNames = scheme.indicatorIds.map(id => {
          const indicator = mockIndicators.find(ind => ind.id === id)
          return indicator ? indicator.name : `指标${id}`
        })
        return {
          ...scheme,
          indicatorNames: indicatorNames
        }
      }
      return scheme
    })
    
    // 按名称筛选
    if (name) {
      filteredSchemes = preprocessedSchemes.filter(scheme => 
        scheme.name.includes(name)
      )
    } else {
      filteredSchemes = preprocessedSchemes
    }
    
    // 按方案序号排序（1-130）
    filteredSchemes.sort((a, b) => a.id - b.id);
    
    // 计算分页
    const total = filteredSchemes.length
    const start = (page - 1) * pageSize
    const end = start + pageSize
    const list = filteredSchemes.slice(start, end)
    
    return Promise.resolve({
      data: {
        list,
        total,
        page,
        pageSize
      }
    })
  },
  
  getSchemeDetail: (enterpriseId, schemeId) => {
    const scheme = mockSchemeLibrary.find(s => s.id === parseInt(schemeId))
    return Promise.resolve({ data: scheme })
  },
  
  createScheme: (enterpriseId, data) => {
    const newScheme = {
      id: mockSchemeLibrary.length + 1,
      ...data,
      status: 'active',
      createdAt: new Date().toISOString().split('T')[0]
    }
    mockSchemeLibrary.push(newScheme)
    return Promise.resolve({ data: newScheme })
  },
  
  updateScheme: (enterpriseId, schemeId, data) => {
    const index = mockSchemeLibrary.findIndex(s => s.id === parseInt(schemeId))
    if (index !== -1) {
      mockSchemeLibrary[index] = { ...mockSchemeLibrary[index], ...data }
      return Promise.resolve({ data: mockSchemeLibrary[index] })
    }
    return Promise.reject(new Error('方案不存在'))
  },
  
  deleteScheme: (enterpriseId, schemeId) => {
    const index = mockSchemeLibrary.findIndex(s => s.id === parseInt(schemeId))
    if (index !== -1) {
      mockSchemeLibrary.splice(index, 1)
      return Promise.resolve({ message: '删除成功' })
    }
    return Promise.reject(new Error('方案不存在'))
  },
  
  getIndicatorTree: () => {
    return Promise.resolve({ data: mockIndicatorTree })
  }
}

export default mockDetailApi