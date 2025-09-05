import Layout from '@/layout/index.vue'

export default {
  path: '/system',
  name: 'System',
  component: Layout,
  meta: { 
    title: '系统管理',
    icon: 'mdi:cog',
    order: 5
  },
  children: [
    {
      path: 'user',
      name: 'UserManagement',
      component: () => import('@/views/system/user/index.vue'),
      meta: { 
        title: '用户管理',
        icon: 'mdi:account'
      }
    },
    {
      path: 'role',
      name: 'RoleManagement',
      component: () => import('@/views/system/role/index.vue'),
      meta: { 
        title: '角色管理',
        icon: 'mdi:account-group'
      }
    },
    {
      path: 'department',
      name: 'DepartmentManagement',
      component: () => import('@/views/system/department/index.vue'),
      meta: { 
        title: '部门管理',
        icon: 'mdi:office-building'
      }
    },
    {
      path: 'menu',
      name: 'MenuManagement',
      component: () => import('@/views/system/menu/index.vue'),
      meta: { 
        title: '菜单管理',
        icon: 'mdi:menu'
      }
    },
    {
      path: 'log',
      name: 'LogManagement',
      component: () => import('@/views/system/log/index.vue'),
      meta: { 
        title: '日志管理',
        icon: 'mdi:file-document'
      }
    }
  ]
}
