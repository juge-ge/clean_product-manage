// 能力建设Mock数据
const mockPersonnelData = {
  consultant: [
    {
      id: 1,
      name: '张清洁',
      title: '高级工程师',
      organization: '中国环境科学研究院',
      department: '清洁生产研究所',
      type: 'consultant',
      avatar: '/avatars/zhang.jpg',
      phone: '13800138001',
      email: 'zhang@example.com',
      specialties: ['清洁生产审核', '环境工程', '节能减排', '循环经济'],
      experience: '从事清洁生产工作15年，主持完成50+企业清洁生产审核，在清洁生产技术研发、节能减排方案设计等方面具有丰富经验。曾参与多项国家级清洁生产项目，发表相关论文20余篇。',
      education: '清华大学环境工程硕士',
      certifications: ['清洁生产审核师', '环境影响评价工程师', '注册环保工程师'],
      achievements: [
        '主持完成50+企业清洁生产审核',
        '参与制定清洁生产国家标准3项',
        '获得国家科技进步奖二等奖1项',
        '发表SCI论文15篇'
      ],
      introduction: '资深清洁生产专家，在清洁生产审核、技术研发、标准制定等方面具有丰富经验，是行业内知名的技术专家。',
      isAvailable: true
    },
    {
      id: 2,
      name: '李环保',
      title: '教授级高级工程师',
      organization: '生态环境部环境工程评估中心',
      department: '清洁生产评估部',
      type: 'consultant',
      avatar: '/avatars/li.jpg',
      phone: '13800138002',
      email: 'li@example.com',
      specialties: ['清洁生产评估', '环境管理', '政策研究', '技术咨询'],
      experience: '从事环保工作20年，专注于清洁生产评估和政策研究，参与制定多项清洁生产相关政策和标准，具有丰富的评估经验。',
      education: '北京大学环境科学博士',
      certifications: ['清洁生产审核师', '环境管理体系审核员', '高级工程师'],
      achievements: [
        '参与制定清洁生产政策10余项',
        '主持清洁生产评估项目100+',
        '获得省部级科技进步奖3项',
        '出版专著2部'
      ],
      introduction: '清洁生产政策研究专家，在清洁生产评估、政策制定、技术咨询等方面具有深厚造诣。',
      isAvailable: true
    },
    {
      id: 3,
      name: '王技术',
      title: '高级工程师',
      organization: '中国清洁生产中心',
      department: '技术开发部',
      type: 'consultant',
      avatar: '/avatars/wang.jpg',
      phone: '13800138003',
      email: 'wang@example.com',
      specialties: ['清洁生产技术', '工艺优化', '设备改造', '节能减排'],
      experience: '从事清洁生产技术研发12年，专注于工业清洁生产技术开发和工艺优化，在化工、钢铁、建材等行业具有丰富经验。',
      education: '中科院过程工程研究所博士',
      certifications: ['清洁生产审核师', '注册化工工程师', '高级工程师'],
      achievements: [
        '开发清洁生产技术20余项',
        '获得发明专利8项',
        '主持国家级项目5项',
        '技术成果转化产值超亿元'
      ],
      introduction: '清洁生产技术专家，在工业清洁生产技术开发、工艺优化、设备改造等方面具有丰富经验。',
      isAvailable: false
    },
    {
      id: 4,
      name: '赵管理',
      title: '高级工程师',
      organization: '中国环境科学学会',
      department: '清洁生产专业委员会',
      type: 'consultant',
      avatar: '/avatars/zhao.jpg',
      phone: '13800138004',
      email: 'zhao@example.com',
      specialties: ['清洁生产管理', '体系认证', '培训教育', '标准制定'],
      experience: '从事清洁生产管理工作10年，专注于清洁生产管理体系建设和人员培训，具有丰富的管理经验和培训经验。',
      education: '中国人民大学管理学硕士',
      certifications: ['清洁生产审核师', 'ISO14001审核员', '高级工程师'],
      achievements: [
        '建立清洁生产管理体系50+',
        '培训清洁生产人员1000+',
        '参与制定行业标准5项',
        '获得管理创新奖2项'
      ],
      introduction: '清洁生产管理专家，在清洁生产管理体系、人员培训、标准制定等方面具有丰富经验。',
      isAvailable: true
    },
    {
      id: 5,
      name: '陈研究',
      title: '研究员',
      organization: '中科院生态环境研究中心',
      department: '清洁生产技术研究室',
      type: 'consultant',
      avatar: '/avatars/chen.jpg',
      phone: '13800138005',
      email: 'chen@example.com',
      specialties: ['清洁生产研究', '技术评估', '政策分析', '国际合作'],
      experience: '从事清洁生产研究工作18年，专注于清洁生产技术评估和政策分析，参与多项国际合作项目，具有国际视野。',
      education: '中科院生态环境研究中心博士',
      certifications: ['清洁生产审核师', '研究员', '国际清洁生产专家'],
      achievements: [
        '主持国际合作项目10+',
        '发表国际期刊论文30+',
        '获得国际奖项2项',
        '参与国际标准制定3项'
      ],
      introduction: '清洁生产研究专家，在清洁生产技术评估、政策分析、国际合作等方面具有丰富经验和国际视野。',
      isAvailable: true
    }
  ],
  manager: [
    {
      id: 101,
      name: '李管理',
      title: '部门主任',
      organization: '生态环境部',
      department: '清洁生产司',
      type: 'manager',
      avatar: '/avatars/li_manager.jpg',
      phone: '13800138006',
      email: 'li_manager@example.com',
      specialties: ['政策制定', '项目管理', '团队建设', '战略规划'],
      experience: '从事环保管理工作20年，专注于清洁生产政策制定和项目管理，具有丰富的管理经验和政策制定经验。',
      education: '北京大学公共管理博士',
      certifications: ['高级工程师', '项目管理师', '公共管理师'],
      achievements: [
        '制定清洁生产政策20+',
        '管理国家级项目50+',
        '建设专业团队100+',
        '获得管理创新奖5项'
      ],
      introduction: '资深环保管理专家，在清洁生产政策制定、项目管理、团队建设等方面具有丰富经验。',
      isAvailable: true
    },
    {
      id: 102,
      name: '刘协调',
      title: '副司长',
      organization: '国家发展改革委',
      department: '资源节约和环境保护司',
      type: 'manager',
      avatar: '/avatars/liu.jpg',
      phone: '13800138007',
      email: 'liu@example.com',
      specialties: ['政策协调', '规划制定', '资源配置', '部门协调'],
      experience: '从事政策协调工作15年，专注于清洁生产政策协调和规划制定，具有丰富的协调经验和规划经验。',
      education: '清华大学公共管理硕士',
      certifications: ['高级工程师', '政策分析师', '规划师'],
      achievements: [
        '协调制定政策30+',
        '制定发展规划10+',
        '协调资源配置100+',
        '获得协调创新奖3项'
      ],
      introduction: '政策协调专家，在清洁生产政策协调、规划制定、资源配置等方面具有丰富经验。',
      isAvailable: true
    },
    {
      id: 103,
      name: '孙监督',
      title: '处长',
      organization: '工业和信息化部',
      department: '节能与综合利用司',
      type: 'manager',
      avatar: '/avatars/sun.jpg',
      phone: '13800138008',
      email: 'sun@example.com',
      specialties: ['监督管理', '标准制定', '行业指导', '质量管控'],
      experience: '从事监督管理工作12年，专注于清洁生产监督管理和标准制定，具有丰富的监督经验和标准制定经验。',
      education: '北京理工大学管理学硕士',
      certifications: ['高级工程师', '质量工程师', '标准化工程师'],
      achievements: [
        '制定行业标准20+',
        '监督管理企业500+',
        '指导行业发展100+',
        '获得监督创新奖2项'
      ],
      introduction: '监督管理专家，在清洁生产监督管理、标准制定、行业指导等方面具有丰富经验。',
      isAvailable: false
    },
    {
      id: 104,
      name: '周服务',
      title: '中心主任',
      organization: '中国清洁生产中心',
      department: '服务中心',
      type: 'manager',
      avatar: '/avatars/zhou.jpg',
      phone: '13800138009',
      email: 'zhou@example.com',
      specialties: ['服务管理', '平台建设', '资源整合', '客户服务'],
      experience: '从事服务管理工作8年，专注于清洁生产服务平台建设和资源整合，具有丰富的服务管理经验。',
      education: '复旦大学管理学硕士',
      certifications: ['高级工程师', '服务管理师', '平台架构师'],
      achievements: [
        '建设服务平台5个',
        '整合资源1000+',
        '服务客户500+',
        '获得服务创新奖3项'
      ],
      introduction: '服务管理专家，在清洁生产服务平台建设、资源整合、客户服务等方面具有丰富经验。',
      isAvailable: true
    },
    {
      id: 105,
      name: '吴培训',
      title: '培训部主任',
      organization: '中国环境科学学会',
      department: '培训部',
      type: 'manager',
      avatar: '/avatars/wu.jpg',
      phone: '13800138010',
      email: 'wu@example.com',
      specialties: ['培训管理', '课程设计', '师资建设', '能力提升'],
      experience: '从事培训管理工作10年，专注于清洁生产培训管理和课程设计，具有丰富的培训管理经验。',
      education: '北京师范大学教育学硕士',
      certifications: ['高级工程师', '培训师', '课程设计师'],
      achievements: [
        '设计培训课程50+',
        '培训人员2000+',
        '建设师资队伍100+',
        '获得培训创新奖4项'
      ],
      introduction: '培训管理专家，在清洁生产培训管理、课程设计、师资建设等方面具有丰富经验。',
      isAvailable: true
    }
  ]
}

export const mockPersonnelApi = {
  getPersonnelList: (params) => {
    const { type, page = 1, pageSize = 10, search = '' } = params
    let data = mockPersonnelData[type] || []
    
    if (search) {
      data = data.filter(item => 
        item.name.includes(search) || 
        item.organization.includes(search) ||
        item.specialties.some(specialty => specialty.includes(search))
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

  getPersonnelDetail: (id) => {
    const allData = [...mockPersonnelData.consultant, ...mockPersonnelData.manager]
    const item = allData.find(item => item.id === parseInt(id))
    return Promise.resolve({ data: item })
  },

  getPersonnelByType: (type, params = {}) => {
    const { page = 1, pageSize = 10, search = '' } = params
    let data = mockPersonnelData[type] || []
    
    if (search) {
      data = data.filter(item => 
        item.name.includes(search) || 
        item.organization.includes(search) ||
        item.specialties.some(specialty => specialty.includes(search))
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

export default mockPersonnelData
