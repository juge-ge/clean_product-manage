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
    }
  ]
}
