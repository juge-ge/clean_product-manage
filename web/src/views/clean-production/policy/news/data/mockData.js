// 动态信息Mock数据
const mockDynamicData = {
  domestic: [
    {
      id: 1,
      title: '工信部发布绿色制造名单，推动产业绿色发展',
      content: '工信部发布2025年绿色制造名单，涵盖多个行业，推动产业绿色发展。详细内容如下：\n\n一、背景意义\n绿色制造是推动制造业高质量发展的重要途径，是建设制造强国的重要内容。\n\n二、主要措施\n1. 完善绿色制造标准体系\n2. 推进绿色工厂建设\n3. 发展绿色供应链\n4. 推广绿色设计产品\n\n三、保障措施\n1. 加强政策支持\n2. 完善标准体系\n3. 强化监督管理',
      summary: '工信部发布2025年绿色制造名单，涵盖多个行业，推动产业绿色发展，完善绿色制造标准体系，推进绿色工厂建设。',
      publishDate: '2025-01-15',
      source: '工信部',
      type: 'domestic',
      tags: ['绿色制造', '产业升级', '绿色发展'],
      viewCount: 1250,
      isTop: true,
      attachments: [
        { name: '2025年绿色制造名单.pdf', url: '/files/green-manufacturing-list-2025.pdf' }
      ]
    },
    {
      id: 2,
      title: '国家发改委发布循环经济发展规划',
      content: '国家发改委发布《"十四五"循环经济发展规划》，提出到2025年，循环型生产方式全面推行，绿色设计和清洁生产普遍推广，资源综合利用能力显著提升。\n\n主要目标：\n1. 资源利用效率大幅提高\n2. 再生资源对原生资源的替代比例进一步提高\n3. 循环经济对经济社会可持续发展的保障能力进一步增强',
      summary: '国家发改委发布《"十四五"循环经济发展规划》，提出到2025年循环型生产方式全面推行的目标。',
      publishDate: '2025-01-14',
      source: '国家发改委',
      type: 'domestic',
      tags: ['循环经济', '发展规划', '资源利用'],
      viewCount: 980,
      isTop: false,
      attachments: []
    },
    {
      id: 3,
      title: '生态环境部推进清洁生产审核工作',
      content: '生态环境部印发《关于深入推进清洁生产审核工作的通知》，要求各地生态环境部门加强组织领导，完善工作机制，确保清洁生产审核工作取得实效。\n\n重点工作：\n1. 强化重点行业清洁生产审核\n2. 完善清洁生产审核技术体系\n3. 加强清洁生产审核队伍建设\n4. 推进清洁生产审核信息化建设',
      summary: '生态环境部印发通知，要求各地深入推进清洁生产审核工作，强化重点行业审核，完善技术体系。',
      publishDate: '2025-01-13',
      source: '生态环境部',
      type: 'domestic',
      tags: ['清洁生产', '审核工作', '环境管理'],
      viewCount: 1560,
      isTop: true,
      attachments: [
        { name: '清洁生产审核工作通知.pdf', url: '/files/clean-production-audit-notice.pdf' }
      ]
    },
    {
      id: 4,
      title: '科技部启动清洁生产技术攻关项目',
      content: '科技部启动2025年清洁生产技术攻关项目，重点支持清洁生产技术研发、产业化应用和标准制定。\n\n支持方向：\n1. 清洁生产技术研发\n2. 清洁生产装备制造\n3. 清洁生产标准制定\n4. 清洁生产人才培养',
      summary: '科技部启动2025年清洁生产技术攻关项目，重点支持技术研发、产业化应用和标准制定。',
      publishDate: '2025-01-12',
      source: '科技部',
      type: 'domestic',
      tags: ['技术攻关', '清洁生产', '科技创新'],
      viewCount: 890,
      isTop: false,
      attachments: []
    },
    {
      id: 5,
      title: '财政部出台清洁生产财税支持政策',
      content: '财政部出台清洁生产财税支持政策，通过税收优惠、财政补贴等方式支持企业开展清洁生产。\n\n支持措施：\n1. 清洁生产设备购置税收优惠\n2. 清洁生产技术改造财政补贴\n3. 清洁生产审核费用补助\n4. 清洁生产示范项目奖励',
      summary: '财政部出台清洁生产财税支持政策，通过税收优惠、财政补贴等方式支持企业开展清洁生产。',
      publishDate: '2025-01-11',
      source: '财政部',
      type: 'domestic',
      tags: ['财税政策', '清洁生产', '企业支持'],
      viewCount: 1120,
      isTop: false,
      attachments: []
    }
  ],
  provincial: [
    {
      id: 101,
      title: '江苏省启动清洁生产技术改造专项行动',
      content: '江苏省启动清洁生产技术改造专项行动，计划用三年时间，对全省重点行业企业实施清洁生产技术改造。\n\n行动目标：\n1. 完成1000家重点企业清洁生产审核\n2. 实施500项清洁生产技术改造项目\n3. 培育50家清洁生产示范企业\n4. 建立清洁生产技术服务体系',
      summary: '江苏省启动清洁生产技术改造专项行动，计划用三年时间对全省重点行业企业实施清洁生产技术改造。',
      publishDate: '2025-01-14',
      province: '江苏省',
      type: 'provincial',
      tags: ['技术改造', '专项行动', '清洁生产'],
      viewCount: 890,
      isTop: false,
      attachments: [
        { name: '江苏省清洁生产技术改造专项行动方案.pdf', url: '/files/jiangsu-clean-production-plan.pdf' }
      ]
    },
    {
      id: 102,
      title: '浙江省发布清洁生产评价指标体系',
      content: '浙江省发布《清洁生产评价指标体系》，为全省清洁生产审核工作提供技术支撑。\n\n体系特点：\n1. 覆盖重点行业\n2. 指标科学合理\n3. 操作简便易行\n4. 结果可比可评',
      summary: '浙江省发布《清洁生产评价指标体系》，为全省清洁生产审核工作提供技术支撑。',
      publishDate: '2025-01-13',
      province: '浙江省',
      type: 'provincial',
      tags: ['评价体系', '指标体系', '技术支撑'],
      viewCount: 750,
      isTop: false,
      attachments: []
    },
    {
      id: 103,
      title: '广东省推进清洁生产示范园区建设',
      content: '广东省推进清洁生产示范园区建设，打造一批清洁生产示范园区，引领全省清洁生产发展。\n\n建设内容：\n1. 完善园区清洁生产基础设施\n2. 建立园区清洁生产管理体系\n3. 推广清洁生产技术\n4. 培育清洁生产服务产业',
      summary: '广东省推进清洁生产示范园区建设，打造一批清洁生产示范园区，引领全省清洁生产发展。',
      publishDate: '2025-01-12',
      province: '广东省',
      type: 'provincial',
      tags: ['示范园区', '园区建设', '清洁生产'],
      viewCount: 680,
      isTop: false,
      attachments: []
    },
    {
      id: 104,
      title: '山东省加强清洁生产审核队伍建设',
      content: '山东省加强清洁生产审核队伍建设，通过培训、考核等方式提升审核人员专业水平。\n\n主要措施：\n1. 开展清洁生产审核师培训\n2. 建立审核人员考核制度\n3. 完善审核人员管理体系\n4. 加强审核人员继续教育',
      summary: '山东省加强清洁生产审核队伍建设，通过培训、考核等方式提升审核人员专业水平。',
      publishDate: '2025-01-11',
      province: '山东省',
      type: 'provincial',
      tags: ['队伍建设', '人员培训', '审核师'],
      viewCount: 920,
      isTop: false,
      attachments: []
    },
    {
      id: 105,
      title: '湖南省启动清洁生产技术创新项目',
      content: '湖南省启动清洁生产技术创新项目，支持企业开展清洁生产技术研发和产业化应用。\n\n支持重点：\n1. 清洁生产技术研发\n2. 清洁生产装备制造\n3. 清洁生产标准制定\n4. 清洁生产人才培养',
      summary: '湖南省启动清洁生产技术创新项目，支持企业开展清洁生产技术研发和产业化应用。',
      publishDate: '2025-01-10',
      province: '湖南省',
      type: 'provincial',
      tags: ['技术创新', '技术研发', '产业化'],
      viewCount: 650,
      isTop: false,
      attachments: []
    }
  ],
  international: [
    {
      id: 201,
      title: '欧盟发布新版生态设计指令，助力循环经济发展',
      content: '欧盟发布新版生态设计指令，要求产品在设计阶段就考虑环境影响，助力循环经济发展。\n\n主要要求：\n1. 产品设计考虑环境影响\n2. 提高产品能效\n3. 延长产品使用寿命\n4. 促进产品回收利用',
      summary: '欧盟发布新版生态设计指令，要求产品在设计阶段就考虑环境影响，助力循环经济发展。',
      publishDate: '2025-01-13',
      country: '欧盟',
      type: 'international',
      tags: ['生态设计', '循环经济', '产品设计'],
      viewCount: 1560,
      isTop: true,
      attachments: [
        { name: '欧盟生态设计指令.pdf', url: '/files/eu-ecodesign-directive.pdf' }
      ]
    },
    {
      id: 202,
      title: '美国环保署发布清洁生产最佳实践指南',
      content: '美国环保署发布清洁生产最佳实践指南，为企业提供清洁生产实施指导。\n\n指南内容：\n1. 清洁生产基本原理\n2. 清洁生产实施步骤\n3. 清洁生产技术选择\n4. 清洁生产效果评估',
      summary: '美国环保署发布清洁生产最佳实践指南，为企业提供清洁生产实施指导。',
      publishDate: '2025-01-12',
      country: '美国',
      type: 'international',
      tags: ['最佳实践', '实施指南', '清洁生产'],
      viewCount: 1200,
      isTop: false,
      attachments: []
    },
    {
      id: 203,
      title: '日本推进清洁生产技术标准化工作',
      content: '日本推进清洁生产技术标准化工作，建立清洁生产技术标准体系，促进清洁生产技术推广。\n\n标准化内容：\n1. 清洁生产技术标准\n2. 清洁生产评价标准\n3. 清洁生产管理标准\n4. 清洁生产服务标准',
      summary: '日本推进清洁生产技术标准化工作，建立清洁生产技术标准体系，促进清洁生产技术推广。',
      publishDate: '2025-01-11',
      country: '日本',
      type: 'international',
      tags: ['技术标准', '标准化', '技术推广'],
      viewCount: 980,
      isTop: false,
      attachments: []
    },
    {
      id: 204,
      title: '德国启动工业4.0清洁生产项目',
      content: '德国启动工业4.0清洁生产项目，将清洁生产理念融入智能制造，推动制造业绿色发展。\n\n项目特点：\n1. 智能制造与清洁生产结合\n2. 数字化清洁生产管理\n3. 智能化清洁生产技术\n4. 网络化清洁生产服务',
      summary: '德国启动工业4.0清洁生产项目，将清洁生产理念融入智能制造，推动制造业绿色发展。',
      publishDate: '2025-01-10',
      country: '德国',
      type: 'international',
      tags: ['工业4.0', '智能制造', '绿色发展'],
      viewCount: 1350,
      isTop: false,
      attachments: []
    },
    {
      id: 205,
      title: '韩国发布清洁生产2030愿景',
      content: '韩国发布清洁生产2030愿景，提出到2030年建成清洁生产强国的目标。\n\n愿景目标：\n1. 清洁生产技术达到世界先进水平\n2. 清洁生产产业规模显著扩大\n3. 清洁生产服务体系完善\n4. 清洁生产国际合作深化',
      summary: '韩国发布清洁生产2030愿景，提出到2030年建成清洁生产强国的目标。',
      publishDate: '2025-01-09',
      country: '韩国',
      type: 'international',
      tags: ['2030愿景', '清洁生产', '强国目标'],
      viewCount: 1100,
      isTop: false,
      attachments: []
    }
  ]
}

export const mockDynamicApi = {
  getDynamicList: (params) => {
    const { type, page = 1, pageSize = 10, search = '' } = params
    let data = mockDynamicData[type] || []
    
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
  
  getDynamicDetail: (id) => {
    const allData = [...mockDynamicData.domestic, ...mockDynamicData.provincial, ...mockDynamicData.international]
    const item = allData.find(item => item.id === parseInt(id))
    return Promise.resolve({ data: item })
  },

  getDynamicByType: (type, params = {}) => {
    const { page = 1, pageSize = 3, search = '' } = params
    let data = mockDynamicData[type] || []
    
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
  }
}

export default mockDynamicData
