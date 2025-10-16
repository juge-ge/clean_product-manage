// 法规政策Mock数据
const mockRegulationData = {
  national: [
    {
      id: 1,
      title: '中华人民共和国清洁生产促进法',
      content: '为了促进清洁生产，提高资源利用效率，减少和避免污染物的产生，保护和改善环境，保障人体健康，促进经济与社会可持续发展，制定本法。\n\n第一章 总则\n第一条 为了促进清洁生产，提高资源利用效率，减少和避免污染物的产生，保护和改善环境，保障人体健康，促进经济与社会可持续发展，制定本法。\n\n第二条 本法所称清洁生产，是指不断采取改进设计、使用清洁的能源和原料、采用先进的工艺技术与设备、改善管理、综合利用等措施，从源头削减污染，提高资源利用效率，减少或者避免生产、服务和产品使用过程中污染物的产生和排放，以减轻或者消除对人类健康和环境的危害。\n\n第三条 在中华人民共和国领域内，从事生产和服务活动的单位以及从事相关管理活动的部门，应当依照本法规定，组织、实施清洁生产。',
      summary: '为了促进清洁生产，提高资源利用效率，减少和避免污染物的产生，保护和改善环境，保障人体健康，促进经济与社会可持续发展，制定本法。',
      publishDate: '2024-12-01',
      effectiveDate: '2025-01-01',
      source: '全国人大常委会',
      category: 'national',
      level: 'national',
      tags: ['清洁生产', '法律', '促进法'],
      viewCount: 2500,
      downloadCount: 1200,
      isImportant: true,
      attachments: [
        { name: '中华人民共和国清洁生产促进法.pdf', url: '/files/clean-production-promotion-law.pdf' }
      ]
    },
    {
      id: 2,
      title: '清洁生产审核办法',
      content: '为促进清洁生产，规范清洁生产审核行为，根据《中华人民共和国清洁生产促进法》，制定本办法。\n\n第一章 总则\n第一条 为促进清洁生产，规范清洁生产审核行为，根据《中华人民共和国清洁生产促进法》，制定本办法。\n\n第二条 本办法所称清洁生产审核，是指按照一定程序，对生产和服务过程进行调查和诊断，找出能耗高、物耗高、污染重的原因，提出减少有毒有害物料的使用、产生，降低能耗、物耗以及废物产生的方案，进而选定技术经济及环境可行的清洁生产方案的过程。',
      summary: '为促进清洁生产，规范清洁生产审核行为，根据《中华人民共和国清洁生产促进法》，制定本办法。',
      publishDate: '2024-11-15',
      effectiveDate: '2024-12-01',
      source: '国家发展改革委',
      category: 'national',
      level: 'national',
      tags: ['清洁生产', '审核', '办法'],
      viewCount: 1800,
      downloadCount: 900,
      isImportant: true,
      attachments: [
        { name: '清洁生产审核办法.pdf', url: '/files/clean-production-audit-method.pdf' }
      ]
    },
    {
      id: 3,
      title: '清洁生产评价指标体系编制通则',
      content: '为规范清洁生产评价指标体系的编制，指导企业开展清洁生产评价，制定本通则。\n\n1 范围\n本通则规定了清洁生产评价指标体系编制的基本原则、指标体系结构、指标分类、指标权重确定方法、评价方法等。\n\n2 规范性引用文件\n下列文件对于本文件的应用是必不可少的。凡是注日期的引用文件，仅注日期的版本适用于本文件。',
      summary: '为规范清洁生产评价指标体系的编制，指导企业开展清洁生产评价，制定本通则。',
      publishDate: '2024-10-20',
      effectiveDate: '2024-11-01',
      source: '国家发展改革委',
      category: 'national',
      level: 'national',
      tags: ['评价体系', '指标体系', '编制通则'],
      viewCount: 1200,
      downloadCount: 600,
      isImportant: false,
      attachments: []
    }
  ],
  provincial: [
    {
      id: 101,
      title: '江苏省清洁生产审核管理办法',
      content: '为促进清洁生产，规范清洁生产审核行为，根据《中华人民共和国清洁生产促进法》和《清洁生产审核办法》，结合本省实际，制定本办法。\n\n第一章 总则\n第一条 为促进清洁生产，规范清洁生产审核行为，根据《中华人民共和国清洁生产促进法》和《清洁生产审核办法》，结合本省实际，制定本办法。\n\n第二条 本办法适用于本省行政区域内从事生产和服务活动的单位以及从事相关管理活动的部门。',
      summary: '为促进清洁生产，规范清洁生产审核行为，根据《中华人民共和国清洁生产促进法》和《清洁生产审核办法》，结合本省实际，制定本办法。',
      publishDate: '2024-11-15',
      effectiveDate: '2024-12-01',
      source: '江苏省生态环境厅',
      category: 'provincial',
      level: 'provincial',
      province: '江苏省',
      tags: ['审核管理', '办法', '江苏省'],
      viewCount: 1800,
      downloadCount: 900,
      isImportant: false,
      attachments: [
        { name: '江苏省清洁生产审核管理办法.pdf', url: '/files/jiangsu-clean-production-audit.pdf' }
      ]
    },
    {
      id: 102,
      title: '浙江省清洁生产促进条例',
      content: '为促进清洁生产，提高资源利用效率，减少和避免污染物的产生，保护和改善环境，根据《中华人民共和国清洁生产促进法》等法律、行政法规，结合本省实际，制定本条例。\n\n第一章 总则\n第一条 为促进清洁生产，提高资源利用效率，减少和避免污染物的产生，保护和改善环境，根据《中华人民共和国清洁生产促进法》等法律、行政法规，结合本省实际，制定本条例。',
      summary: '为促进清洁生产，提高资源利用效率，减少和避免污染物的产生，保护和改善环境，根据《中华人民共和国清洁生产促进法》等法律、行政法规，结合本省实际，制定本条例。',
      publishDate: '2024-10-10',
      effectiveDate: '2024-11-01',
      source: '浙江省人大常委会',
      category: 'provincial',
      level: 'provincial',
      province: '浙江省',
      tags: ['促进条例', '浙江省', '清洁生产'],
      viewCount: 1500,
      downloadCount: 750,
      isImportant: false,
      attachments: []
    }
  ],
  guide: [
    {
      id: 201,
      title: '清洁生产审核指南',
      content: '本指南旨在指导企业开展清洁生产审核工作，帮助企业识别清洁生产机会，制定清洁生产方案，实现清洁生产目标。\n\n1 清洁生产审核概述\n1.1 清洁生产审核的定义\n清洁生产审核是指按照一定程序，对生产和服务过程进行调查和诊断，找出能耗高、物耗高、污染重的原因，提出减少有毒有害物料的使用、产生，降低能耗、物耗以及废物产生的方案，进而选定技术经济及环境可行的清洁生产方案的过程。',
      summary: '本指南旨在指导企业开展清洁生产审核工作，帮助企业识别清洁生产机会，制定清洁生产方案，实现清洁生产目标。',
      publishDate: '2024-09-15',
      effectiveDate: '2024-10-01',
      source: '生态环境部',
      category: 'guide',
      level: 'national',
      tags: ['审核指南', '指导', '清洁生产'],
      viewCount: 2000,
      downloadCount: 1000,
      isImportant: true,
      attachments: [
        { name: '清洁生产审核指南.pdf', url: '/files/clean-production-audit-guide.pdf' }
      ]
    }
  ],
  evaluation: [
    {
      id: 301,
      title: '清洁生产评价指标体系编制通则',
      content: '为规范清洁生产评价指标体系的编制，指导企业开展清洁生产评价，制定本通则。\n\n1 范围\n本通则规定了清洁生产评价指标体系编制的基本原则、指标体系结构、指标分类、指标权重确定方法、评价方法等。',
      summary: '为规范清洁生产评价指标体系的编制，指导企业开展清洁生产评价，制定本通则。',
      publishDate: '2024-08-20',
      effectiveDate: '2024-09-01',
      source: '国家发展改革委',
      category: 'evaluation',
      level: 'national',
      tags: ['评价体系', '指标体系', '编制通则'],
      viewCount: 1600,
      downloadCount: 800,
      isImportant: false,
      attachments: []
    }
  ],
  technology: [
    {
      id: 401,
      title: '清洁生产技术导向目录（2024年版）',
      content: '为引导企业采用先进的清洁生产技术，提高清洁生产水平，促进产业结构调整和优化升级，制定本目录。\n\n一、编制原则\n（一）技术先进性原则。选择技术先进、成熟可靠、经济合理的技术。\n（二）环境友好性原则。选择能够显著减少污染物产生和排放的技术。\n（三）经济可行性原则。选择投资合理、运行成本低、经济效益好的技术。',
      summary: '为引导企业采用先进的清洁生产技术，提高清洁生产水平，促进产业结构调整和优化升级，制定本目录。',
      publishDate: '2024-07-10',
      effectiveDate: '2024-08-01',
      source: '国家发展改革委',
      category: 'technology',
      level: 'national',
      tags: ['技术导向', '目录', '清洁生产技术'],
      viewCount: 2200,
      downloadCount: 1100,
      isImportant: true,
      attachments: [
        { name: '清洁生产技术导向目录（2024年版）.pdf', url: '/files/clean-production-technology-directory-2024.pdf' }
      ]
    }
  ],
  elimination: [
    {
      id: 501,
      title: '淘汰落后生产能力、工艺和产品目录（2024年版）',
      content: '为加快淘汰落后生产能力、工艺和产品，促进产业结构调整和优化升级，制定本目录。\n\n一、编制原则\n（一）技术落后原则。淘汰技术落后、能耗高、污染重的生产能力、工艺和产品。\n（二）安全环保原则。淘汰不符合安全环保要求的生产能力、工艺和产品。\n（三）市场淘汰原则。淘汰市场竞争力弱、经济效益差的生产能力、工艺和产品。',
      summary: '为加快淘汰落后生产能力、工艺和产品，促进产业结构调整和优化升级，制定本目录。',
      publishDate: '2024-06-15',
      effectiveDate: '2024-07-01',
      source: '工业和信息化部',
      category: 'elimination',
      level: 'national',
      tags: ['淘汰目录', '落后产能', '工艺产品'],
      viewCount: 1900,
      downloadCount: 950,
      isImportant: true,
      attachments: [
        { name: '淘汰落后生产能力、工艺和产品目录（2024年版）.pdf', url: '/files/elimination-directory-2024.pdf' }
      ]
    }
  ],
  mature: [
    {
      id: 601,
      title: '国家推荐的清洁生产成熟技术目录（2024年版）',
      content: '为推广清洁生产成熟技术，提高清洁生产技术水平，促进清洁生产产业发展，制定本目录。\n\n一、编制原则\n（一）技术成熟原则。选择技术成熟、应用广泛、效果显著的技术。\n（二）经济合理原则。选择投资合理、运行成本低、经济效益好的技术。\n（三）环境友好原则。选择能够显著减少污染物产生和排放的技术。',
      summary: '为推广清洁生产成熟技术，提高清洁生产技术水平，促进清洁生产产业发展，制定本目录。',
      publishDate: '2024-05-20',
      effectiveDate: '2024-06-01',
      source: '国家发展改革委',
      category: 'mature',
      level: 'national',
      tags: ['成熟技术', '推荐目录', '清洁生产技术'],
      viewCount: 2100,
      downloadCount: 1050,
      isImportant: true,
      attachments: [
        { name: '国家推荐的清洁生产成熟技术目录（2024年版）.pdf', url: '/files/mature-technology-directory-2024.pdf' }
      ]
    }
  ]
}

// 标签页配置
export const regulationTabs = [
  {
    key: 'national',
    label: '国家政策法规',
    icon: 'mdi:flag'
  },
  {
    key: 'provincial',
    label: '各省政策法规',
    icon: 'mdi:map-marker'
  },
  {
    key: 'guide',
    label: '清洁生产审核指南',
    icon: 'mdi:book-open'
  },
  {
    key: 'evaluation',
    label: '清洁生产评价指标体系',
    icon: 'mdi:chart-line'
  },
  {
    key: 'technology',
    label: '清洁生产技术导向目录',
    icon: 'mdi:cog'
  },
  {
    key: 'elimination',
    label: '淘汰落后生产能力、工艺和产品目录',
    icon: 'mdi:delete'
  },
  {
    key: 'mature',
    label: '国家推荐的清洁生产成熟技术',
    icon: 'mdi:check-circle'
  }
]

export const mockRegulationApi = {
  getRegulationList: (params) => {
    const { category, page = 1, pageSize = 10, search = '' } = params
    let data = mockRegulationData[category] || []
    
    if (search) {
      data = data.filter(item => 
        item.title.includes(search) || 
        item.summary.includes(search) ||
        (item.tags && item.tags.some(tag => tag.includes(search)))
      )
    }
    
    const start = (page - 1) * pageSize
    const end = start + pageSize
    
    return Promise.resolve({
      data: {
        list: data.slice(start, end),
        total: data.length,
        page,
        pageSize
      }
    })
  },

  getRegulationDetail: (id) => {
    const allData = Object.values(mockRegulationData).flat()
    const item = allData.find(item => item.id === parseInt(id))
    return Promise.resolve({ data: item })
  },

  getRegulationByCategory: (category, params = {}) => {
    const { page = 1, pageSize = 10, search = '' } = params
    let data = mockRegulationData[category] || []
    
    if (search) {
      data = data.filter(item => 
        item.title.includes(search) || 
        item.summary.includes(search)
      )
    }
    
    const start = (page - 1) * pageSize
    const end = start + pageSize
    
    return Promise.resolve({
      data: {
        list: data.slice(start, end),
        total: data.length,
        page,
        pageSize
      }
    })
  },

  downloadRegulation: (id) => {
    const allData = Object.values(mockRegulationData).flat()
    const item = allData.find(item => item.id === parseInt(id))
    return Promise.resolve({ data: item })
  }
}

export default mockRegulationData
