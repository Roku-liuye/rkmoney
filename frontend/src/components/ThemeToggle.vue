<script setup lang="ts">
import { Moon, Sun } from 'lucide-vue-next'
import { useThemeStore } from '../store/theme'

const themeStore = useThemeStore()
</script>

<template>
  <button
    @click="themeStore.toggleDark()"
    class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
    :title="themeStore.isDark ? '切换到浅色模式' : '切换到深色模式'"
  >
    <Moon v-if="!themeStore.isDark" class="w-5 h-5 text-gray-600 dark:text-gray-300" />
    <Sun v-else class="w-5 h-5 text-yellow-400" />
  </button>
</template>
