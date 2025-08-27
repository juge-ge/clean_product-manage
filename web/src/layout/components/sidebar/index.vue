<script setup>
import SideLogo from './components/SideLogo.vue'
import SideMenu from './components/SideMenu.vue'
</script>

<template>
  <div class="sidebar-container">
    <SideLogo />
    <SideMenu />
  </div>
</template>

<style scoped>
.sidebar-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: var(--n-color);
}
</style>
