import Layout from '@/layout/index.vue'
import RouterView from '@/components/common/RouterView.vue'

export default {
  name: '清洁生产管理',
  path: '/clean-production',  // 添加前导斜杠
  component: Layout,         // 直接引用组件
  children: [
    {
      name: '清洁生产政策与管理',
      path: 'policy',
      component: RouterView,  // 直接引用组件
      children: [
        {
          name: '通知公告',
          path: 'notice',
          component: () => import('./policy/notice/index.vue'),
          children: [
            {
              name: 'notice-list',
              path: 'list/:type',
              component: () => import('./policy/notice/list.vue'),
              meta: {
                title: '通知列表',
                hideInMenu: true
              }
            },
            {
              name: 'notice-search',
              path: 'search',
              component: () => import('./policy/notice/list.vue'),
              meta: {
                title: '搜索结果',
                hideInMenu: true
              }
            },
            {
              name: 'notice-detail',
              path: 'detail/:id',
              component: () => import('./policy/notice/detail.vue'),
              meta: {
                title: '通知详情',
                hideInMenu: true
              }
            }
          ]
        },
        {
          name: '动态信息',
          path: 'dynamic-info',
          component: () => import('./policy/dynamic-info/index.vue')
        }
      ]
    },
    {
      name: '清洁生产云审核',
      path: 'audit',
      component: RouterView,
      children: [
        {
          name: 'PCB',
          path: 'pcb',
          component: RouterView,
          children: [
            {
              name: '企业基本信息',
              path: 'basic-info',
              component: () => import('./audit/pcb/basic-info/index.vue')
            }
          ]
        }
      ]
    },
    {
      name: '会议与宣传',
      path: 'meetings-publicity',
      component: () => import('./meetings-publicity/index.vue')
    },
    {
      name: '企业清洁生产审核管理',
      path: 'enterprise-audit-management',
      component: () => import('./enterprise-audit-management/index.vue')
    },
    {
      name: '清洁生产审核典型案例',
      path: 'typical-cases',
      component: () => import('./typical-cases/index.vue')
    },
    {
      name: '工业园区',
      path: 'industrial-parks',
      component: () => import('./industrial-parks/index.vue')
    },
    {
      name: '行业',
      path: 'industry',
      component: () => import('./industry/index.vue')
    },
    {
      name: '企业',
      path: 'enterprises',
      component: () => import('./enterprises/index.vue')
    },
    {
      name: '区域',
      path: 'regions',
      component: () => import('./regions/index.vue')
    },
    {
      name: '专家库',
      path: 'expert-database',
      component: () => import('./expert-database/index.vue')
    },
    {
      name: '国际合作',
      path: 'international-cooperation',
      component: () => import('./international-cooperation/index.vue')
    },
    {
      name: '清洁生产技术集成',
      path: 'technology-integration',
      component: () => import('./technology-integration/index.vue')
    },
    {
      name: '清洁生产智慧决策',
      path: 'smart-decision',
      component: () => import('./smart-decision/index.vue')
    }
  ]
}
