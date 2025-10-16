// 钢铁行业指标定义（44项）
const mockIndicators = [
  // 一级指标：绿色低碳结构（2项）
  { id: 1, name: '清洁能源使用率', category: '绿色低碳结构', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 2, name: '清洁运输比例', category: '绿色低碳结构', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  
  // 一级指标：绿色技术及装备（6项）
  { id: 3, name: '焦炉装备配置率', category: '绿色技术及装备', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 4, name: '烧结机装备配置率', category: '绿色技术及装备', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 5, name: '球团装备配置', category: '绿色技术及装备', type: 'qualitative', level: null, score: 0, isLimiting: false, weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 6, name: '高炉装备配置率', category: '绿色技术及装备', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 7, name: '炼钢装备配置率', category: '绿色技术及装备', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 8, name: '关键工序数控化率', category: '绿色技术及装备', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  
  // 一级指标：资源能源消耗（12项）
  { id: 9, name: '炼焦工序单位产品能源消耗', category: '资源能源消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kgce/t', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 10, name: '烧结工序单位产品能源消耗', category: '资源能源消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kgce/t', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 11, name: '球团工序单位产品能源消耗', category: '资源能源消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kgce/t', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 12, name: '高炉工序单位产品能源消耗', category: '资源能源消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kgce/t', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 13, name: '转炉冶炼单位产品能源消耗', category: '资源能源消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kgce/t', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 14, name: '全废钢法电炉冶炼单位产品能源消耗', category: '资源能源消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kgce/t', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 15, name: '30%铁水热装电炉冶炼单位产品能源消耗', category: '资源能源消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kgce/t', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 16, name: '主轧线工序单位产品能源消耗（中厚板/棒线/热轧薄板）', category: '资源能源消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kgce/t', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 17, name: '二次能源发电量占总耗电量比率', category: '资源能源消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 18, name: '新鲜水耗', category: '资源能源消耗', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'm³/t', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  
  // 一级指标：综合利用（13项）
  { id: 19, name: '生产水重复利用率', category: '综合利用', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 20, name: '高炉煤气利用率', category: '综合利用', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 21, name: '焦炉煤气利用率', category: '综合利用', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 22, name: '转炉煤气回收热量', category: '综合利用', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kgce/t钢', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 23, name: '高炉煤气放散率', category: '综合利用', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 24, name: '含铁尘（泥）回收利用率', category: '综合利用', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 25, name: '高炉渣利用率', category: '综合利用', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 26, name: '转炉渣利用率', category: '综合利用', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 27, name: '铁水预处理、精炼装置、钢包等渣铁利用率', category: '综合利用', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 28, name: '脱硫副产物利用率', category: '综合利用', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 29, name: '粉尘综合利用率', category: '综合利用', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 30, name: '高炉瓦斯灰/泥回收利用率', category: '综合利用', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 31, name: '电炉尘泥利用率', category: '综合利用', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: '%', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  
  // 一级指标：减污降碳（11项）
  { id: 32, name: '颗粒物排放量', category: '减污降碳', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kg/t钢', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 33, name: 'SO₂排放量', category: '减污降碳', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kg/t钢', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 34, name: 'NOx（以NO₂计）排放量', category: '减污降碳', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kg/t钢', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 35, name: '废水排放强度', category: '减污降碳', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'm³/t钢', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 36, name: '化学需氧量（COD）排放强度', category: '减污降碳', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kg/t钢', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 37, name: '氨氮排放强度', category: '减污降碳', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kg/t钢', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 38, name: '挥发酚排放强度', category: '减污降碳', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'g/t钢', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 39, name: '总氰化物排放强度', category: '减污降碳', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'g/t钢', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 40, name: '总锌排放强度', category: '减污降碳', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'g/t钢', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 41, name: '总铬排放强度', category: '减污降碳', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'g/t钢', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 42, name: '六价铬排放强度', category: '减污降碳', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'g/t钢', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 43, name: '总铅排放强度', category: '减污降碳', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'g/t钢', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 44, name: '总铊排放强度', category: '减污降碳', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'g/t钢', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 45, name: '工业固废产生强度', category: '减污降碳', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kg/t钢', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] },
  { id: 46, name: '单位产品二氧化碳排放量', category: '减污降碳', type: 'quantitative', level: null, score: 0, isLimiting: false, unit: 'kgCO₂/t钢', weight: 1, currentValue: null, recommendedSchemes: [], selectedSchemes: [] }
]

// 钢铁行业清洁生产方案库（100-120项方案）
const mockSchemeLibrary = [
  // 工艺优化类方案（30-35项）
  {
    id: 1,
    name: '烧结烟气循环技术',
    type: '工艺优化',
    description: '将烧结机头部烟气循环回用至烧结料中，减少新鲜空气用量',
    problemSolved: '降低烧结工序能耗，减少废气排放量',
    economicBenefit: '年节约标煤约5000吨，节约成本约300万元',
    environmentalBenefit: '减少SO₂排放约200吨/年，减少NOx排放约150吨/年',
    investment: 800,
    paybackPeriod: 2.7,
    indicatorIds: [4, 10, 33, 34],
    indicatorNames: '烧结机装备配置率、烧结工序单位产品能源消耗、SO₂排放量、NOx（以NO₂计）排放量'
  },
  {
    id: 2,
    name: '高炉富氧喷煤技术',
    type: '工艺优化',
    description: '在高炉风口区域喷吹煤粉并富氧助燃，提高燃烧效率',
    problemSolved: '降低焦比，提高生铁产量，减少能源消耗',
    economicBenefit: '焦比降低20kg/t，年节约成本约2000万元',
    environmentalBenefit: '减少CO₂排放约10万吨/年',
    investment: 3000,
    paybackPeriod: 1.5,
    indicatorIds: [6, 12, 12],
    indicatorNames: '高炉装备配置率、高炉工序单位产品能源消耗、高炉工序单位产品能源消耗'
  },
  
  // 设备改造类方案（25-30项）
  {
    id: 3,
    name: '转炉负能炼钢技术',
    type: '设备改造',
    description: '优化转炉炼钢工艺参数，实现不需外加能源的负能炼钢',
    problemSolved: '降低炼钢工序能耗，提高转炉煤气回收量',
    economicBenefit: '年回收转炉煤气约5000万m³，创效约1000万元',
    environmentalBenefit: '减少能源消耗，降低CO₂排放',
    investment: 2000,
    paybackPeriod: 2.0,
    indicatorIds: [7, 13, 21],
    indicatorNames: '炼钢装备配置率、转炉冶炼单位产品能源消耗、焦炉煤气利用率'
  },
  
  // 节能降耗类方案（20-25项）
  {
    id: 4,
    name: '余热余压发电技术',
    type: '节能降耗',
    description: '利用高炉、转炉、烧结等工序产生的余热余压进行发电',
    problemSolved: '回收利用余热余压，降低电力消耗',
    economicBenefit: '年发电量约2亿kWh，节约成本约1亿元',
    environmentalBenefit: '减少外购电力，降低间接碳排放',
    investment: 15000,
    paybackPeriod: 1.5,
    indicatorIds: [17, 17, 17],
    indicatorNames: '二次能源发电量占总耗电量比率、二次能源发电量占总耗电量比率、二次能源发电量占总耗电量比率'
  },
  
  // 污染治理类方案（15-20项）
  {
    id: 5,
    name: '烧结烟气脱硫脱硝一体化技术',
    type: '污染治理',
    description: '采用活性焦干法烟气净化技术，同时脱除SO₂和NOx',
    problemSolved: '有效控制烧结烟气污染物排放',
    economicBenefit: '副产硫酸或硫磺，年创效约500万元',
    environmentalBenefit: 'SO₂去除率≥95%，NOx去除率≥60%',
    investment: 8000,
    paybackPeriod: 4.0,
    indicatorIds: [4, 33, 34],
    indicatorNames: '烧结机装备配置率、SO₂排放量、NOx（以NO₂计）排放量'
  },
  
  // 水处理类方案（10-12项）
  {
    id: 6,
    name: '废水深度处理及回用技术',
    type: '水处理',
    description: '采用超滤+反渗透技术对工业废水进行深度处理',
    problemSolved: '提高水循环利用率，减少新鲜水消耗',
    economicBenefit: '年节约新鲜水约200万m³，节约成本约600万元',
    environmentalBenefit: '减少废水排放，提高水资源利用效率',
    investment: 3000,
    paybackPeriod: 5.0,
    indicatorIds: [18, 19, 36, 37],
    indicatorNames: '新鲜水耗、生产水重复利用率、化学需氧量（COD）排放强度、氨氮排放强度'
  },
  
  // 固废利用类方案（8-10项）
  {
    id: 7,
    name: '钢渣综合利用技术',
    type: '固废利用',
    description: '采用热闷法处理钢渣，用于水泥生产、道路建设等',
    problemSolved: '提高钢渣资源化利用率，减少固废堆存',
    economicBenefit: '年处理钢渣约50万吨，创效约1000万元',
    environmentalBenefit: '减少土地占用，提高资源利用率',
    investment: 2000,
    paybackPeriod: 2.0,
    indicatorIds: [26, 45],
    indicatorNames: '转炉渣利用率、工业固废产生强度'
  },
  
  // 管理优化类方案（5-8项）
  {
    id: 8,
    name: '能源管理中心建设',
    type: '管理优化',
    description: '建立能源管理中心，实现能源的集中监控和优化调度',
    problemSolved: '提高能源利用效率，降低能源消耗',
    economicBenefit: '综合能耗降低3-5%，年节约成本约3000万元',
    environmentalBenefit: '减少能源消耗和碳排放',
    investment: 5000,
    paybackPeriod: 1.7,
    indicatorIds: [9, 10, 11],
    indicatorNames: '炼焦工序单位产品能源消耗、烧结工序单位产品能源消耗、球团工序单位产品能源消耗'
  }
  
  // ... 其余90-112项方案，覆盖钢铁行业的各个工序和指标
]

// 推荐方案获取函数
const getRecommendedSchemes = (indicatorId) => {
  const recommendedSchemes = mockSchemeLibrary.filter(scheme => 
    scheme.indicatorIds && scheme.indicatorIds.includes(parseInt(indicatorId))
  );
  
  const sortedSchemes = recommendedSchemes.sort((a, b) => a.id - b.id);
  
  return sortedSchemes.map(scheme => ({
    value: scheme.id,
    label: `方案${scheme.id}：${scheme.name}`,
    preview: {
      type: scheme.type,
      description: scheme.description,
      problemSolved: scheme.problemSolved,
      economicBenefit: scheme.economicBenefit,
      environmentalBenefit: scheme.environmentalBenefit
    }
  }));
}

// 筹划与组织Mock数据
const mockPlanningData = {
  auditTeam: [
    {
      id: 1,
      name: '张工程师',
      position: '组长',
      department: '环保部',
      phone: '13800138001',
      email: 'zhang@example.com',
      responsibilities: '总体协调、技术指导'
    },
    {
      id: 2,
      name: '李工程师',
      position: '副组长',
      department: '生产部',
      phone: '13800138002',
      email: 'li@example.com',
      responsibilities: '生产数据收集、工艺分析'
    }
  ],
  workPlans: [
    {
      id: 1,
      phase: '筹划与组织',
      startDate: '2024-01-01',
      endDate: '2024-01-15',
      tasks: ['组建审核小组', '制定工作计划', '开展培训'],
      status: 'completed'
    },
    {
      id: 2,
      phase: '预审核',
      startDate: '2024-01-16',
      endDate: '2024-02-15',
      tasks: ['现状调研', '数据收集', '问题识别'],
      status: 'in-progress'
    }
  ],
  trainingRecords: [
    {
      id: 1,
      date: '2024-01-05',
      topic: '清洁生产审核基础知识',
      participants: 15,
      duration: 4,
      instructor: '张工程师',
      content: '清洁生产概念、审核流程、指标体系'
    }
  ]
}

// 预审核Mock数据
const mockPreAuditData = {
  productionInfo: {
    capacity: 500,
    output: {
      '2022': {
        crudeSteel: 450,
        steelProducts: 420,
        pigIron: 480,
        coke: 200,
        sinterOre: 600,
        pellet: 300
      },
      '2023': {
        crudeSteel: 480,
        steelProducts: 450,
        pigIron: 510,
        coke: 210,
        sinterOre: 620,
        pellet: 310
      },
      '2024': {
        crudeSteel: 500,
        steelProducts: 470,
        pigIron: 530,
        coke: 220,
        sinterOre: 640,
        pellet: 320
      }
    }
  },
  rawMaterials: [
    {
      id: 1,
      year: 2024,
      name: '铁矿石',
      unit: '万吨',
      process: '烧结',
      amount: 600,
      source: '进口',
      quality: 'TFe≥62%'
    },
    {
      id: 2,
      year: 2024,
      name: '焦炭',
      unit: '万吨',
      process: '炼铁',
      amount: 220,
      source: '自产',
      quality: '固定碳≥85%'
    }
  ],
  processEquipment: {
    sintering: { capacity: '600万吨/年', equipment: '烧结机', year: '2015' },
    pelletizing: { capacity: '300万吨/年', equipment: '球团机', year: '2016' },
    coking: { capacity: '200万吨/年', equipment: '焦炉', year: '2014' },
    ironMaking: { capacity: '500万吨/年', equipment: '高炉', year: '2013' },
    steelMaking: { capacity: '500万吨/年', equipment: '转炉', year: '2014' },
    rolling: { capacity: '450万吨/年', equipment: '轧机', year: '2015' }
  },
  resourceConsumption: {
    energy: [
      { year: 2024, type: '煤炭', amount: 120, unit: '万吨' },
      { year: 2024, type: '天然气', amount: 5000, unit: '万m³' }
    ],
    water: [
      { year: 2024, type: '新鲜水', amount: 800, source: '地下水' }
    ],
    electricity: [
      { year: 2024, amount: 15000, unit: '万kWh' }
    ]
  },
  pollutionControl: {
    wastewater: {
      treatment: '生化处理+深度处理',
      capacity: 2000,
      process: 'A/O+MBR'
    },
    wasteGas: {
      treatment: '脱硫脱硝除尘',
      facilities: 'SCR+湿法脱硫+电除尘',
      efficiency: 95
    },
    solidWaste: {
      treatment: '综合利用',
      utilization: 85
    }
  },
  solidWaste: {
    general: [
      { year: 2024, name: '钢渣', type: '一般固废', amount: 50, disposal: '综合利用' },
      { year: 2024, name: '高炉渣', type: '一般固废', amount: 200, disposal: '水泥生产' }
    ],
    hazardous: [
      { year: 2024, name: '废油', type: '危险废物', code: 'HW08', amount: 10, disposal: '委托处置' }
    ]
  },
  selfMonitoring: {
    wastewater: {
      pollutants: 'COD、氨氮、总磷、总氮',
      frequency: '每日',
      compliance: '达标'
    },
    wasteGas: {
      pollutants: 'SO₂、NOx、颗粒物',
      frequency: '连续监测',
      compliance: '达标'
    },
    noise: {
      points: 8,
      frequency: '每季度',
      compliance: '达标'
    }
  }
}

// Mock API实现
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
  
  // 预审核相关
  getPreAuditData: (enterpriseId) => {
    return Promise.resolve({ data: mockPreAuditData })
  },
  
  submitPreAuditData: (enterpriseId, data) => {
    return Promise.resolve({ message: '提交成功' })
  },
  
  // 审核相关
  getAuditResults: (enterpriseId) => {
    return Promise.resolve({ data: mockIndicators })
  },
  
  submitAuditResults: (enterpriseId, data) => {
    return Promise.resolve({ message: '提交成功' })
  },
  
  getRecommendedSchemes: (enterpriseId, indicatorId) => {
    const schemes = getRecommendedSchemes(indicatorId);
    return Promise.resolve({ data: schemes });
  },
  
  // 方案库相关
  getSchemes: (enterpriseId, params = {}) => {
    const { page = 1, page_size = 200, name = '', indicatorIds = [] } = params
    let filteredSchemes = mockSchemeLibrary
    
    if (name) {
      filteredSchemes = filteredSchemes.filter(scheme => 
        scheme.name.includes(name)
      )
    }
    
    if (indicatorIds && indicatorIds.length > 0) {
      filteredSchemes = filteredSchemes.filter(scheme => {
        if (!scheme.indicatorIds || scheme.indicatorIds.length === 0) return false
        return indicatorIds.some(id => 
          scheme.indicatorIds.includes(parseInt(id))
        )
      })
    }
    
    filteredSchemes.sort((a, b) => a.id - b.id);
    
    const total = filteredSchemes.length
    const start = (page - 1) * page_size
    const end = start + page_size
    const list = filteredSchemes.slice(start, end)
    
    return Promise.resolve({
      data: {
        list,
        total,
        page,
        page_size
      }
    })
  },
  
  createScheme: (enterpriseId, data) => {
    return Promise.resolve({ message: '创建成功' })
  },
  
  updateScheme: (enterpriseId, schemeId, data) => {
    return Promise.resolve({ message: '更新成功' })
  },
  
  deleteScheme: (enterpriseId, schemeId) => {
    return Promise.resolve({ message: '删除成功' })
  },
  
  // 报告相关
  generateReport: (enterpriseId, data) => {
    return Promise.resolve({ message: '报告生成成功' })
  }
}
