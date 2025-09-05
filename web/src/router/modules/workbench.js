import Layout from '@/layout/index.vue'

export default {
  path: '/',
  name: 'Root',
  component: Layout,
  redirect: '/workbench',
  meta: { 
    title: '首页',
    icon: 'mdi:home',
    order: 0
  },
  children: [
    {
      path: 'workbench',
      name: 'Workbench',
      component: () => import('@/views/workbench/index.vue'),
      meta: { 
        title: '首页',
        icon: 'mdi:view-dashboard',
        affix: true
      }
    }
  ]
}
