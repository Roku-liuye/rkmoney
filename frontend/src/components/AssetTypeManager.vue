<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { 
  Plus, 
  Trash2, 
  Edit, 
  X, 
  Package, 
  ShoppingBag, 
  CreditCard, 
  Box, 
  Tag,
  Smartphone,
  Laptop,
  Watch,
  Car,
  Home,
  Heart,
  Briefcase,
  Wallet,
  TrendingUp,
  Activity
} from 'lucide-vue-next'
import { assetTypesApi } from '../api'
import type { AssetType } from '../types'

const props = defineProps<{
  show: boolean
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'updated'): void
}>()

const showAddModal = ref(false)
const showEditModal = ref(false)
const selectedType = ref<AssetType | null>(null)

const newType = ref({
  name: '',
  icon: 'Package',
  color: 'gray'
})

const assetTypes = ref<AssetType[]>([])
const icons = ['Package', 'ShoppingBag', 'CreditCard', 'Box', 'Tag', 'Smartphone', 'Laptop', 'Watch', 'Car', 'Home', 'Heart', 'Briefcase', 'Wallet', 'TrendingUp', 'Activity']

const typeIcons: Record<string, any> = {
  Package, ShoppingBag, CreditCard, Box, Tag, Smartphone, Laptop, Watch, Car, Home, Heart, Briefcase, Wallet, TrendingUp, Activity
}

const defaultTypes = [
  { name: '数码', icon: 'Smartphone', color: 'blue' },
  { name: '生活', icon: 'ShoppingBag', color: 'green' },
  { name: '理财', icon: 'CreditCard', color: 'orange' },
  { name: '其他', icon: 'Package', color: 'gray' }
]

const fetchAssetTypes = async () => {
  try {
    const response = await assetTypesApi.getCustom()
    assetTypes.value = response.data.data
  } catch (err) {
    console.error('Failed to fetch asset types:', err)
  }
}

watch(() => props.show, (newVal) => {
  if (newVal) {
    fetchAssetTypes()
  }
})

const handleAddType = async () => {
  if (!newType.value.name) return
  
  try {
    await assetTypesApi.create(newType.value)
    showAddModal.value = false
    newType.value = { name: '', icon: 'Package', color: 'gray' }
    fetchAssetTypes()
    emit('updated')
  } catch (err) {
    console.error('Failed to add asset type:', err)
  }
}

const handleEditType = (type: AssetType) => {
  selectedType.value = type
  newType.value = {
    name: type.name,
    icon: type.icon,
    color: type.color || 'gray'
  }
  showEditModal.value = true
}

const handleUpdateType = async () => {
  if (!selectedType.value || !newType.value.name) return
  
  try {
    await assetTypesApi.update(selectedType.value.id, newType.value)
    showEditModal.value = false
    selectedType.value = null
    newType.value = { name: '', icon: 'Package', color: 'gray' }
    fetchAssetTypes()
    emit('updated')
  } catch (err) {
    console.error('Failed to update asset type:', err)
  }
}

const handleDeleteType = async (id: number) => {
  if (confirm('确定要删除该分类吗？')) {
    try {
      await assetTypesApi.delete(id)
      fetchAssetTypes()
      emit('updated')
    } catch (err) {
      console.error('Failed to delete asset type:', err)
    }
  }
}

const getIconComponent = (iconName: string) => {
  return typeIcons[iconName] || Package
}

const getColorClass = (color: string) => {
  const colorMap: Record<string, string> = {
    gray: 'bg-gray-100 text-gray-600',
    blue: 'bg-blue-100 text-blue-600',
    green: 'bg-green-100 text-green-600',
    red: 'bg-red-100 text-red-600',
    yellow: 'bg-yellow-100 text-yellow-600',
    orange: 'bg-orange-100 text-orange-600',
    purple: 'bg-purple-100 text-purple-600',
    pink: 'bg-pink-100 text-pink-600',
    indigo: 'bg-indigo-100 text-indigo-600',
    cyan: 'bg-cyan-100 text-cyan-600'
  }
  return colorMap[color] || colorMap.gray
}
</script>

<template>
  <div class="space-y-8">
    <!-- Custom Types -->
    <div class="space-y-4">
      <div class="flex items-center justify-between">
        <h3 class="text-sm font-bold text-gray-400 uppercase tracking-widest ml-1">自定义分类</h3>
        <button 
          @click="showAddModal = true"
          class="text-xs font-bold text-black hover:underline flex items-center gap-1"
        >
          <Plus :size="14" />
          <span>新增分类</span>
        </button>
      </div>

      <div v-if="assetTypes.length === 0" class="text-center py-8 bg-gray-50 rounded-2xl border border-dashed border-gray-200 text-gray-400 text-sm">
        暂无自定义分类
      </div>

      <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div 
          v-for="type in assetTypes" 
          :key="type.id"
          class="bg-white p-4 rounded-2xl border border-gray-100 hover:border-gray-300 hover:shadow-md transition-all group flex items-center justify-between"
        >
          <div class="flex items-center gap-4">
            <div :class="['p-3 rounded-xl', getColorClass(type.color)]">
              <component :is="getIconComponent(type.icon)" :size="20" />
            </div>
            <h3 class="font-bold text-gray-900">{{ type.name }}</h3>
          </div>
          <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
            <button 
              @click="handleEditType(type)"
              class="p-2 text-gray-400 hover:text-black hover:bg-gray-100 rounded-lg transition-all"
            >
              <Edit :size="16" />
            </button>
            <button 
              @click="handleDeleteType(type.id)"
              class="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-all"
            >
              <Trash2 :size="16" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Default Types -->
    <div class="space-y-4">
      <h3 class="text-sm font-bold text-gray-400 uppercase tracking-widest ml-1">系统默认</h3>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 opacity-60">
        <div 
          v-for="defaultType in defaultTypes" 
          :key="defaultType.name"
          class="bg-gray-50 p-4 rounded-2xl border border-transparent flex items-center gap-4"
        >
          <div :class="['p-3 rounded-xl', getColorClass(defaultType.color)]">
            <component :is="getIconComponent(defaultType.icon)" :size="20" />
          </div>
          <h3 class="font-bold text-gray-900">{{ defaultType.name }}</h3>
        </div>
      </div>
    </div>

    <!-- Modals -->
    <div v-if="showAddModal || showEditModal" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-[60] p-4 animate-in fade-in duration-300">
      <div class="bg-white rounded-[32px] w-full max-w-md p-10 shadow-2xl animate-in zoom-in-95 slide-in-from-bottom-10 duration-500">
        <div class="flex justify-between items-center mb-10">
          <h2 class="text-3xl font-black tracking-tight">{{ showEditModal ? '编辑分类' : '新增分类' }}</h2>
          <button @click="showAddModal = false; showEditModal = false" class="p-2 hover:bg-gray-100 rounded-full transition-all">
            <X :size="24" />
          </button>
        </div>

        <form @submit.prevent="showEditModal ? handleUpdateType() : handleAddType()" class="space-y-8">
          <div class="space-y-2">
            <label class="text-xs font-bold text-gray-400 uppercase tracking-widest ml-1">分类名称</label>
            <input v-model="newType.name" type="text" placeholder="例如：电子产品" class="w-full text-lg py-3" required />
          </div>

          <div class="space-y-2">
            <label class="text-xs font-bold text-gray-400 uppercase tracking-widest ml-1">选择图标</label>
            <div class="grid grid-cols-5 gap-4 max-h-40 overflow-y-auto p-2 border border-gray-100 rounded-2xl">
              <button 
                v-for="icon in icons" 
                :key="icon"
                type="button"
                @click="newType.icon = icon"
                class="flex flex-col items-center justify-center p-3 rounded-xl transition-all"
                :class="newType.icon === icon ? 'bg-black text-white shadow-lg' : 'hover:bg-gray-50 text-gray-400'"
              >
                <component :is="getIconComponent(icon)" :size="20" />
              </button>
            </div>
          </div>

          <div class="space-y-2">
            <label class="text-xs font-bold text-gray-400 uppercase tracking-widest ml-1">选择颜色</label>
            <div class="flex flex-wrap gap-3">
              <button 
                v-for="color in ['gray', 'blue', 'green', 'red', 'yellow', 'orange', 'purple', 'pink', 'indigo', 'cyan']" 
                :key="color"
                type="button"
                @click="newType.color = color"
                class="w-10 h-10 rounded-full transition-all border-4 flex items-center justify-center"
                :class="[
                  newType.color === color ? 'border-black' : 'border-transparent',
                  getColorClass(color)
                ]"
              >
                <div class="w-3 h-3 rounded-full bg-current"></div>
              </button>
            </div>
          </div>

          <button 
            type="submit" 
            class="w-full bg-black text-white py-5 rounded-2xl font-black text-lg hover:bg-gray-800 transition-all shadow-lg hover:shadow-xl active:scale-95"
          >
            {{ showEditModal ? '保存修改' : '确认添加' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>
