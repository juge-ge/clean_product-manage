# 清洁生产政策与管理模块

## 模块概述

清洁生产政策与管理模块是清洁生产管理系统的核心业务模块，负责提供政策信息、动态资讯、法规政策、能力建设和会议宣传等综合服务。

## 模块结构

```
清洁生产政策与管理
├── 通知公告 (已实现)
├── 动态信息 (news)
│   ├── 国外动态
│   ├── 国内动态
│   └── 省内动态
├── 清洁生产法规政策 (regulations)
│   ├── 国家政策法规
│   ├── 各省政策法规
│   ├── 清洁生产审核指南
│   ├── 清洁生产评价指标体系
│   ├── 清洁生产技术导向目录
│   ├── 淘汰落后生产能力、工艺和产品目录
│   └── 国家推荐的清洁生产成熟技术
├── 能力建设 (capability)
│   ├── 咨询人员
│   └── 管理人员
└── 会议与宣传 (meeting)
    ├── 清洁生产会议
    └── 清洁生产宣传
```

## 技术特点

- **前后端解耦**: 采用Vue.js + API接口的架构模式
- **响应式设计**: 支持多设备适配
- **模块化开发**: 各子模块独立开发，便于维护
- **统一风格**: 遵循现有系统设计规范

## 文件结构

```
web/src/views/clean-production/policy/
├── notice/                    # 通知公告 (已实现)
├── news/                      # 动态信息
│   ├── index.vue
│   ├── components/
│   │   ├── DynamicDetailModal.vue
│   │   ├── DynamicCard.vue
│   │   └── DynamicList.vue
│   └── data/
│       └── mockData.js
├── regulations/               # 清洁生产法规政策
│   ├── index.vue
│   ├── components/
│   │   ├── RegulationDetailModal.vue
│   │   ├── RegulationCard.vue
│   │   ├── RegulationList.vue
│   │   └── RegulationTabs.vue
│   └── data/
│       └── mockData.js
├── capability/                # 能力建设
│   ├── index.vue
│   ├── components/
│   │   ├── PersonnelDetailModal.vue
│   │   ├── PersonnelCard.vue
│   │   └── PersonnelList.vue
│   └── data/
│       └── mockData.js
└── meeting/                   # 会议与宣传
    ├── index.vue
    ├── components/
    │   ├── MeetingDetailModal.vue
    │   ├── MeetingCard.vue
    │   ├── MeetingList.vue
    │   └── VideoPlayer.vue
    └── data/
        └── mockData.js
```

## 使用方法

### 1. 动态信息模块

- **首页模式**: 三栏展示，每栏显示最新3条动态
- **列表模式**: 单栏展示，支持分页和搜索
- **详情模式**: 弹窗展示详细信息

### 2. 清洁生产法规政策模块

- **标签页布局**: 顶部标签页切换不同政策类型
- **搜索功能**: 每个标签页独立的搜索框
- **列表展示**: 统一的列表样式，支持排序
- **详情查看**: 弹窗展示政策详情

### 3. 能力建设模块

- **双栏布局**: 咨询人员和管理人员分别展示
- **人员卡片**: 展示基本信息，点击查看详情
- **详情弹窗**: 展示完整的人员信息
- **搜索功能**: 支持姓名、专业领域搜索

### 4. 会议与宣传模块

- **双栏布局**: 会议信息和宣传视频分别展示
- **会议列表**: 展示会议基本信息，支持详情查看
- **视频播放**: 集成视频播放器，支持在线观看
- **搜索功能**: 支持标题、内容搜索

## API接口

所有模块都使用统一的API接口规范：

```javascript
// 动态信息API
getDynamicList: (params) => request.get('/api/v1/policy/dynamic', { params })
getDynamicDetail: (id) => request.get(`/api/v1/policy/dynamic/${id}`)

// 法规政策API
getRegulationList: (params) => request.get('/api/v1/policy/regulation', { params })
getRegulationDetail: (id) => request.get(`/api/v1/policy/regulation/${id}`)

// 能力建设API
getPersonnelList: (params) => request.get('/api/v1/policy/personnel', { params })
getPersonnelDetail: (id) => request.get(`/api/v1/policy/personnel/${id}`)

// 会议与宣传API
getMeetingList: (params) => request.get('/api/v1/policy/meeting', { params })
getVideoList: (params) => request.get('/api/v1/policy/video', { params })
```

## Mock数据

每个模块都包含完整的Mock数据，用于开发和测试：

- `news/data/mockData.js` - 动态信息Mock数据
- `regulations/data/mockData.js` - 法规政策Mock数据
- `capability/data/mockData.js` - 能力建设Mock数据
- `meeting/data/mockData.js` - 会议与宣传Mock数据

## 路由配置

模块路由已配置在 `web/src/router/modules/cleanProduction.js` 中：

```javascript
{
  path: 'policy',
  name: 'Policy',
  component: RouterView,
  children: [
    { path: 'notice', name: 'Notice', component: () => import('@/views/clean-production/policy/notice/index.vue') },
    { path: 'news', name: 'News', component: () => import('@/views/clean-production/policy/news/index.vue') },
    { path: 'regulations', name: 'Regulations', component: () => import('@/views/clean-production/policy/regulations/index.vue') },
    { path: 'capability', name: 'Capability', component: () => import('@/views/clean-production/policy/capability/index.vue') },
    { path: 'meeting', name: 'Meeting', component: () => import('@/views/clean-production/policy/meeting/index.vue') }
  ]
}
```

## 开发说明

1. **组件复用**: 各模块使用统一的组件设计规范
2. **样式统一**: 遵循现有系统的样式规范
3. **响应式设计**: 支持多设备适配
4. **前后端解耦**: 使用Mock数据进行开发，便于后续对接真实API

## 注意事项

- 所有模块都严格按照技术规范要求实现
- 前后端完全解耦，未修改其他无关代码
- 使用统一的Mock数据格式
- 遵循现有的设计规范和交互模式
