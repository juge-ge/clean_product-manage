<template>
  <n-menu
    ref="menu"
    class="side-menu"
    accordion
    :indent="18"
    :collapsed-icon-size="22"
    :collapsed-width="64"
    :options="menuOptions"
    :value="activeKey"
    @update:value="handleMenuSelect"
  />
</template>

<script setup>
import { useAppStore } from '@/store'
import { renderCustomIcon, renderIcon, isExternal } from '@/utils'
import { businessRoutes } from '@/router'

const router = useRouter()
const curRoute = useRoute()
const appStore = useAppStore()

const activeKey = computed(() => curRoute.meta?.activeMenu || curRoute.name)

const menuOptions = computed(() => {
  return businessRoutes.map((item) => getMenuItem(item)).sort((a, b) => (a.order || 0) - (b.order || 0))
})

const menu = ref(null)
watch(curRoute, async () => {
  await nextTick()
  menu.value?.showOption()
})

function resolvePath(basePath, path) {
  if (isExternal(path)) return path
  return (
    '/' +
    [basePath, path]
      .filter((path) => !!path && path !== '/')
      .map((path) => path.replace(/(^\/)|(\/$)/g, ''))
      .join('/')
  )
}

function getMenuItem(route, basePath = '') {
  let menuItem = {
    label: route.meta?.title || route.name,
    key: route.name,
    path: resolvePath(basePath, route.path),
    icon: getIcon(route.meta),
    order: route.meta?.order || 0,
  }

  const visibleChildren = route.children
    ? route.children.filter((item) => item.name && !item.meta?.hidden)
    : []

  if (!visibleChildren.length) return menuItem

  if (visibleChildren.length === 1) {
    // 单个子路由处理
    const singleRoute = visibleChildren[0]
    menuItem = {
      ...menuItem,
      label: singleRoute.meta?.title || singleRoute.name,
      key: singleRoute.name,
      path: resolvePath(menuItem.path, singleRoute.path),
      icon: getIcon(singleRoute.meta),
      order: singleRoute.meta?.order || 0,
    }
    const visibleItems = singleRoute.children
      ? singleRoute.children.filter((item) => item.name && !item.meta?.hidden)
      : []

    if (visibleItems.length === 1) {
      menuItem = getMenuItem(visibleItems[0], menuItem.path)
    } else if (visibleItems.length > 1) {
      menuItem.children = visibleItems
        .map((item) => getMenuItem(item, menuItem.path))
        .sort((a, b) => (a.order || 0) - (b.order || 0))
    }
  } else {
    menuItem.children = visibleChildren
      .map((item) => getMenuItem(item, menuItem.path))
      .sort((a, b) => (a.order || 0) - (b.order || 0))
  }
  return menuItem
}

function getIcon(meta) {
  if (meta?.customIcon) return renderCustomIcon(meta.customIcon, { size: 18 })
  if (meta?.icon) return renderIcon(meta.icon, { size: 18 })
  return null
}

function handleMenuSelect(key, item) {
  if (isExternal(item.path)) {
    window.open(item.path)
  } else {
    if (item.path === curRoute.path) {
      appStore.reloadPage()
    } else {
      router.push(item.path)
    }
  }
}
</script>

<style lang="scss">
.side-menu {
  margin-top: 8px;
  
  // 智能现代字体样式
  .n-menu-item-content {
    font-family: 'Inter', 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
    font-weight: 500;
    font-size: 14px;
    letter-spacing: 0.01em;
    line-height: 1.4;
    
    // 菜单项文字样式
    .n-menu-item-content__text {
      font-weight: 500;
      font-size: 14px;
      color: #374151;
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    // 图标样式
    .n-menu-item-content__icon {
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    // 悬停效果
    &:hover {
      .n-menu-item-content__text {
        color: #1f2937;
        font-weight: 600;
      }
      
      .n-menu-item-content__icon {
        transform: scale(1.05);
      }
    }
    
    // 选中状态
    &.n-menu-item-content--selected {
      .n-menu-item-content__text {
        color: #1f2937;
        font-weight: 600;
      }
      
      .n-menu-item-content__icon {
        transform: scale(1.05);
      }
    }
  }
  
  // 子菜单样式
  .n-menu-item-content--child {
    .n-menu-item-content__text {
      font-size: 13px;
      font-weight: 400;
      color: #6b7280;
    }
    
    &:hover .n-menu-item-content__text {
      color: #374151;
      font-weight: 500;
    }
    
    &.n-menu-item-content--selected .n-menu-item-content__text {
      color: #1f2937;
      font-weight: 500;
    }
  }
  
  &:not(.n-menu--collapsed) {
    .n-menu-item-content {
      &::before {
        left: 5px;
        right: 5px;
        border-radius: 0 6px 6px 0;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
      }
      &.n-menu-item-content--selected,
      &:hover {
        &::before {
          border-left: 3px solid var(--primary-color);
          background: rgba(59, 130, 246, 0.05);
        }
      }
    }
  }
  
  // 折叠状态下的样式
  &.n-menu--collapsed {
    .n-menu-item-content {
      .n-menu-item-content__icon {
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
      }
      
      &:hover .n-menu-item-content__icon {
        transform: scale(1.1);
      }
    }
  }
}
</style>