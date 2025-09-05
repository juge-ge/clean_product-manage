import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/store'
import { getToken } from '@/utils'
import workbench from './modules/workbench'
import cleanProduction from './modules/cleanProduction'
import cloudAudit from './modules/cloudAudit'
import technologyIntegration from './modules/technologyIntegration'
import smartDecision from './modules/smartDecision'
import system from './modules/system'

// 创建路由实例的工厂函数
function createAppRouter() {
  return createRouter({
    history: createWebHistory(),
    routes: [...basicRoutes, ...businessRoutes]
  })
}

import Layout from '@/layout/index.vue'

// 基础路由
export const basicRoutes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login/index.vue'),
    meta: { 
      title: '登录',
      hidden: true 
    }
  }
]

// 业务路由
export const businessRoutes = [
  workbench,
  cleanProduction,
  cloudAudit,
  technologyIntegration,
  smartDecision,
  system
]

// 创建路由实例
export const router = createAppRouter()

// 重置路由方法
export function resetRouter() {
  const newRouter = createAppRouter()
  router.matcher = newRouter.matcher
}

// 路由守卫
router.beforeEach(async (to, from, next) => {
  console.log('🚦 路由守卫 - 开始导航:', {
    to: { path: to.path, name: to.name, meta: to.meta },
    from: { path: from.path, name: from.name }
  })
  
  // 设置页面标题
  document.title = to.meta?.title ? `${to.meta.title} - 清洁生产智慧管理平台` : '清洁生产智慧管理平台'
  
  // 检查是否需要登录
  const token = getToken()
  console.log('🔑 Token状态:', {
    exists: !!token,
    value: token
  })
  
  const userStore = useUserStore()
  console.log('👤 用户状态:', {
    userId: userStore.userId,
    name: userStore.name,
    isLoggedIn: !!userStore.userId
  })

  if (to.path === '/login') {
    console.log('🎯 访问登录页')
    if (token) {
      console.log('⏩ 已登录，重定向到首页')
      next('/')
    } else {
      console.log('✅ 允许访问登录页')
      next()
    }
    return
  }

  if (!token) {
    console.log('⚠️ 未登录，重定向到登录页')
    next('/login')
    return
  }

  // 确保用户信息已加载
  if (!userStore.userId && token) {
    console.log('🔄 开始加载用户信息')
    try {
      await userStore.getUserInfo()
      console.log('✅ 用户信息加载成功:', {
        userId: userStore.userId,
        name: userStore.name
      })
    } catch (error) {
      console.error('❌ 加载用户信息失败:', error)
      next('/login')
      return
    }
  }

  console.log('✅ 导航通过，目标页面:', to.path)
  next()
})

// 同时导出默认和命名导出
export default router