<script setup lang="ts">
import { onMounted } from 'vue'
import { useThemeStore } from './store/theme'
import ThemeToggle from './components/ThemeToggle.vue'

const themeStore = useThemeStore()

onMounted(() => {
  themeStore.initTheme()
})
</script>

<template>
  <div class="min-h-screen bg-white dark:bg-gray-900 transition-colors">
    <div class="fixed top-4 right-4 z-50">
      <ThemeToggle />
    </div>
    <router-view></router-view>
  </div>
</template>

<style>
</style>
