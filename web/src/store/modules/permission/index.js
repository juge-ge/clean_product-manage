import { defineStore } from 'pinia'
import { basicRoutes, vueModules } from '@/router/routes'
import Layout from '@/layout/index.vue'
import api from '@/api'

// * 后端路由相关函数
// 根据后端传来数据构建出前端路由

import RouterView from '@/components/common/RouterView.vue'

function buildRoutes(routes = []) {
  return routes.map((e) => {
    const route = {
      name: e.name,
      path: e.path,
      component: shallowRef(Layout),
      isHidden: e.is_hidden,
      redirect: e.redirect,
      meta: {
        title: e.name,
        icon: e.icon,
        order: e.order,
        keepAlive: e.keepalive,
      },
      children: [],
    }

    if (e.children && e.children.length > 0) {
      // 递归处理子菜单
      route.children = e.children.map((e_child) => {
        const childRoute = {
          name: e_child.name,
          path: e_child.path,
          // 如果是目录类型，使用RouterView组件而不是Layout
          component: e_child.component === 'Layout' ? shallowRef(RouterView) : vueModules[`/src/views${e_child.component}/index.vue`],
          isHidden: e_child.is_hidden,
          meta: {
            title: e_child.name,
            icon: e_child.icon,
            order: e_child.order,
            keepAlive: e_child.keepalive,
          },
          children: [],
        }
        
        // 递归处理三级菜单
        if (e_child.children && e_child.children.length > 0) {
          childRoute.children = e_child.children.map((e_grandchild) => ({
            name: e_grandchild.name,
            path: e_grandchild.path,
            component: vueModules[`/src/views${e_grandchild.component}/index.vue`],
            isHidden: e_grandchild.is_hidden,
            meta: {
              title: e_grandchild.name,
              icon: e_grandchild.icon,
              order: e_grandchild.order,
              keepAlive: e_grandchild.keepalive,
            },
          }))
        }
        
        return childRoute
      })
    } else {
      // 没有子菜单，创建一个默认的子路由
      route.children.push({
        name: `${e.name}Default`,
        path: '',
        component: vueModules[`/src/views${e.component}/index.vue`],
        isHidden: true,
        meta: {
          title: e.name,
          icon: e.icon,
          order: e.order,
          keepAlive: e.keepalive,
        },
      })
    }

    return route
  })
}

export const usePermissionStore = defineStore('permission', {
  state() {
    return {
      accessRoutes: [],
      accessApis: [],
    }
  },
  getters: {
    routes() {
      return basicRoutes.concat(this.accessRoutes)
    },
    menus() {
      return this.routes.filter((route) => route.name && !route.isHidden)
    },
    apis() {
      return this.accessApis
    },
  },
  actions: {
    async generateRoutes() {
      const res = await api.getUserMenu() // 调用接口获取后端传来的菜单路由
      this.accessRoutes = buildRoutes(res.data) // 处理成前端路由格式
      return this.accessRoutes
    },
    async getAccessApis() {
      const res = await api.getUserApi()
      this.accessApis = res.data
      return this.accessApis
    },
    resetPermission() {
      this.$reset()
    },
  },
})
