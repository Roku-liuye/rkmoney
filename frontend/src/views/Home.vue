<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useAssetStore } from '../store'
import { 
  Plus, 
  Trash2, 
  CircleDollarSign, 
  Calendar, 
  Package, 
  X,
  TrendingUp,
  CreditCard,
  ShoppingBag,
  History,
  Coins,
  Edit,
  Box,
  Tag,
  Activity,
  Smartphone,
  Laptop,
  Watch,
  Car,
  Home,
  Heart,
  Briefcase,
  Wallet
} from 'lucide-vue-next'
import dayjs from 'dayjs'
import type { Asset, AssetType } from '../types'
import AssetTypeManager from '../components/AssetTypeManager.vue'

const store = useAssetStore()
const showAddModal = ref(false)
const showSellModal = ref(false)
const showEditModal = ref(false)
const showTypeManager = ref(false)
const selectedAsset = ref<Asset | null>(null)

const newAsset = ref({
  name: '',
  amount: 0,
  purchase_date: dayjs().format('YYYY-MM-DD'),
  type: '其他',
  type_icon: 'Package'
})

const editAsset = ref({
  id: 0,
  name: '',
  amount: 0,
  purchase_date: dayjs().format('YYYY-MM-DD'),
  type: '其他',
  type_icon: 'Package'
})

const sellInfo = ref({
  sold_date: dayjs().format('YYYY-MM-DD'),
  sold_price: 0
})

const assetTypes = ref<AssetType[]>([])

const typeIcons: Record<string, any> = {
  Package, ShoppingBag, CreditCard, Box, Tag, Smartphone, Laptop, Watch, Car, Home, Heart, Briefcase, Wallet, Activity, TrendingUp
}

const defaultTypes = [
  { id: -1, name: '数码', icon: 'Smartphone', color: 'blue' },
  { id: -2, name: '生活', icon: 'ShoppingBag', color: 'green' },
  { id: -3, name: '理财', icon: 'CreditCard', color: 'orange' },
  { id: -4, name: '其他', icon: 'Package', color: 'gray' }
]

const allTypes = computed(() => {
  return [...assetTypes.value, ...defaultTypes]
})

const getTypeIcon = (asset: Asset) => {
  if (asset.type_icon && typeIcons[asset.type_icon]) {
    return asset.type_icon
  }
  const found = allTypes.value.find(t => t.name === asset.type)
  return found?.icon || 'Package'
}

onMounted(() => {
  store.fetchAssets()
  fetchAssetTypes()
})

const fetchAssetTypes = async () => {
  try {
    const response = await fetch(`http://${window.location.hostname}:8000/api/types/custom`)
    const data = await response.json()
    assetTypes.value = data.data
  } catch (err) {
    console.error('Failed to fetch asset types:', err)
  }
}

const totalDailyValue = computed(() => {
  return store.assets.reduce((sum, asset) => sum + (asset.sold_date ? 0 : asset.daily_value), 0)
})

const handleSubmit = async () => {
  if (!newAsset.value.name || newAsset.value.amount <= 0) return
  
  const selectedType = allTypes.value.find(t => t.name === newAsset.value.type);
  const typeIcon = selectedType?.icon || 'Package';

  try {
    await store.addAsset({
      ...newAsset.value,
      type_icon: typeIcon
    })
    showAddModal.value = false
    newAsset.value = {
      name: '',
      amount: 0,
      purchase_date: dayjs().format('YYYY-MM-DD'),
      type: '其他',
      type_icon: 'Package'
    }
  } catch (err) {
    console.error(err)
  }
}

const handleEdit = async () => {
  if (!editAsset.value.name || editAsset.value.amount <= 0) return
  
  const selectedType = allTypes.value.find(t => t.name === editAsset.value.type);
  const typeIcon = selectedType?.icon || 'Package';

  try {
    await store.updateAsset(editAsset.value.id, {
      name: editAsset.value.name,
      amount: editAsset.value.amount,
      purchase_date: editAsset.value.purchase_date,
      type: editAsset.value.type,
      type_icon: typeIcon
    })
    showEditModal.value = false
  } catch (err) {
    console.error(err)
  }
}

const handleSell = async () => {
  if (!selectedAsset.value || sellInfo.value.sold_price < 0) return
  
  try {
    await store.sellAsset(
      selectedAsset.value.id, 
      sellInfo.value.sold_date, 
      sellInfo.value.sold_price
    )
    showSellModal.value = false
    selectedAsset.value = null
  } catch (err) {
    console.error(err)
  }
}

const openSellModal = (asset: Asset) => {
  selectedAsset.value = asset
  sellInfo.value.sold_price = asset.amount
  showSellModal.value = true
}

const openEditModal = (asset: Asset) => {
  editAsset.value = {
    id: asset.id,
    name: asset.name,
    amount: asset.amount,
    purchase_date: asset.purchase_date,
    type: asset.type || '其他',
    type_icon: asset.type_icon || 'Package'
  }
  showEditModal.value = true
}

const handleDelete = async (id: number) => {
  if (confirm('确定要删除该资产吗？')) {
    await store.deleteAsset(id)
  }
}

const formatCurrency = (value: number) => {
  return new Intl.NumberFormat('zh-CN', {
    style: 'currency',
    currency: 'CNY'
  }).format(value)
}

const formatDate = (date: string) => {
  return dayjs(date).format('YYYY年MM月DD日')
}

const getDaysSincePurchase = (purchaseDate: string) => {
  const days = dayjs().diff(dayjs(purchaseDate), 'day')
  return days === 0 ? 1 : days
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
  <div class="max-w-4xl mx-auto px-4 sm:px-6 py-6 sm:py-12">
    <!-- Header -->
    <header class="flex justify-between items-end mb-6 sm:mb-12">
      <div>
        <h1 class="text-2xl sm:text-3xl font-bold tracking-tight text-gray-900 dark:text-white mb-1 sm:mb-2">RkMoney</h1>
        <p class="text-gray-500 dark:text-gray-400 font-medium text-sm sm:text-base">记录你的物品价值</p>
      </div>
      <div class="flex items-center gap-2 sm:gap-3">
        <button 
          @click="showTypeManager = true"
          class="text-gray-600 dark:text-gray-400 hover:text-black dark:hover:text-white px-3 py-2 sm:px-4 sm:py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-all flex items-center gap-1.5 sm:gap-2"
        >
          <Package :size="16" />
          <span class="font-medium text-sm">分类</span>
        </button>
        <button 
          @click="showAddModal = true"
          class="bg-black dark:bg-white text-white dark:text-black px-4 py-2 sm:px-6 sm:py-2.5 rounded-full flex items-center gap-1.5 sm:gap-2 hover:bg-gray-800 dark:hover:bg-gray-200 transition-all shadow-sm active:scale-95"
        >
          <Plus :size="16" />
          <span class="font-medium text-sm">新增</span>
        </button>
      </div>
    </header>

    <!-- Stats -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6 mb-6 sm:mb-12">
      <div class="bg-gray-50 dark:bg-gray-800 p-5 sm:p-8 rounded-2xl sm:rounded-3xl border border-gray-100 dark:border-gray-700">
        <div class="flex items-center gap-2 text-gray-400 dark:text-gray-500 mb-2 sm:mb-3">
          <TrendingUp :size="14" />
          <span class="text-[10px] sm:text-xs font-bold uppercase tracking-widest">日均消耗</span>
        </div>
        <div class="text-2xl sm:text-4xl font-bold tracking-tight dark:text-white">{{ formatCurrency(totalDailyValue) }}</div>
      </div>
      <div class="bg-gray-50 dark:bg-gray-800 p-5 sm:p-8 rounded-2xl sm:rounded-3xl border border-gray-100 dark:border-gray-700">
        <div class="flex items-center gap-2 text-gray-400 dark:text-gray-500 mb-2 sm:mb-3">
          <Package :size="14" />
          <span class="text-[10px] sm:text-xs font-bold uppercase tracking-widest">持有资产</span>
        </div>
        <div class="text-2xl sm:text-4xl font-bold tracking-tight dark:text-white">{{ store.assets.filter(a => !a.sold_date).length }}</div>
      </div>
    </div>

    <!-- Section Title -->
    <div class="flex items-center justify-between mb-4 sm:mb-6">
      <h2 class="text-lg sm:text-xl font-bold text-gray-900 dark:text-white">资产列表</h2>
      <div class="text-xs sm:text-sm text-gray-400 dark:text-gray-500">共 {{ store.assets.length }} 个</div>
    </div>

    <!-- Asset List -->
    <div v-if="store.loading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-black dark:border-white"></div>
    </div>

    <div v-else-if="store.assets.length === 0" class="text-center py-12 sm:py-20 bg-gray-50 dark:bg-gray-800 rounded-2xl sm:rounded-3xl border border-dashed border-gray-200 dark:border-gray-700">
      <div class="text-gray-400 dark:text-gray-500 mb-3 sm:mb-4 text-sm sm:text-base">暂无资产</div>
      <button @click="showAddModal = true" class="text-black dark:text-white font-bold hover:underline text-sm sm:text-base">点击添加</button>
    </div>

    <div v-else class="space-y-4">
      <div 
        v-for="asset in store.assets" 
        :key="asset.id"
        class="group bg-white dark:bg-gray-800 p-4 sm:p-6 rounded-2xl sm:rounded-3xl border border-gray-100 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600 hover:shadow-xl transition-all flex items-center gap-3 sm:gap-6"
        :class="{'opacity-60 grayscale-[0.5]': asset.sold_date}"
      >
        <!-- Icon -->
        <div class="h-11 w-11 sm:h-14 sm:w-14 bg-gray-50 dark:bg-gray-700 rounded-xl sm:rounded-2xl flex items-center justify-center text-gray-400 group-hover:bg-black group-hover:text-white transition-all duration-300 flex-shrink-0">
          <component 
            :is="getIconComponent(getTypeIcon(asset))" 
            :size="22" 
          />
        </div>

        <!-- Info -->
        <div class="flex-1 min-w-0">
          <div class="flex items-center gap-2 mb-0.5">
            <h3 class="font-bold text-base sm:text-lg text-gray-900 dark:text-white truncate">{{ asset.name }}</h3>
            <span v-if="asset.sold_date" class="px-1.5 py-0.5 bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400 text-[9px] font-bold rounded-md uppercase flex-shrink-0">已出售</span>
          </div>
          <div class="flex flex-wrap items-center gap-x-3 sm:gap-x-6 gap-y-0.5 text-xs sm:text-sm text-gray-400 dark:text-gray-500">
            <span class="flex items-center gap-1 whitespace-nowrap">
              <CircleDollarSign :size="12" />
              {{ formatCurrency(asset.amount) }}
            </span>
            <span class="flex items-center gap-1 whitespace-nowrap">
              <Calendar :size="12" />
              {{ formatDate(asset.purchase_date) }}
            </span>
            <span v-if="!asset.sold_date" class="flex items-center gap-1 whitespace-nowrap">
              <History :size="12" />
              {{ getDaysSincePurchase(asset.purchase_date) }}天
            </span>
          </div>
        </div>

        <!-- Value -->
        <div class="text-right flex-shrink-0">
          <div class="text-[9px] sm:text-[10px] text-gray-400 dark:text-gray-500 uppercase tracking-widest mb-0.5 font-bold">日均</div>
          <div class="text-lg sm:text-2xl font-black tracking-tighter" :class="asset.sold_date ? 'text-gray-400' : 'text-black dark:text-white'">
            {{ formatCurrency(asset.daily_value) }}
          </div>
        </div>

        <!-- Actions -->
        <div class="flex items-center gap-0.5 sm:ml-2 flex-shrink-0">
          <button 
            v-if="!asset.sold_date"
            @click="openSellModal(asset)"
            class="sm:opacity-0 sm:group-hover:opacity-100 p-1.5 sm:p-2 text-gray-400 hover:text-black dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg sm:rounded-xl transition-all"
            title="标记为出售"
          >
            <Coins :size="16" />
          </button>
          <button 
            @click="openEditModal(asset)"
            class="sm:opacity-0 sm:group-hover:opacity-100 p-1.5 sm:p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded-lg sm:rounded-xl transition-all"
            title="编辑"
          >
            <Edit :size="16" />
          </button>
          <button 
            @click="handleDelete(asset.id)"
            class="sm:opacity-0 sm:group-hover:opacity-100 p-1.5 sm:p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/30 rounded-lg sm:rounded-xl transition-all"
            title="删除"
          >
            <Trash2 :size="16" />
          </button>
        </div>
      </div>
    </div>

    <!-- Add Modal -->
    <div v-if="showAddModal" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4 animate-in fade-in duration-300">
      <div class="bg-white dark:bg-gray-800 rounded-[32px] w-full max-w-md p-10 shadow-2xl animate-in zoom-in-95 slide-in-from-bottom-10 duration-500">
        <div class="flex justify-between items-center mb-10">
          <h2 class="text-3xl font-black tracking-tight dark:text-white">新增资产</h2>
          <button @click="showAddModal = false" class="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-full transition-all">
            <X :size="24" />
          </button>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-8">
          <div class="space-y-2">
            <label class="text-xs font-bold text-gray-400 uppercase tracking-widest ml-1">资产名称</label>
            <input v-model="newAsset.name" type="text" placeholder="例如：iPhone 15 Pro" class="w-full text-lg py-3" required />
          </div>

          <div class="grid grid-cols-2 gap-6">
            <div class="space-y-2">
              <label class="text-xs font-bold text-gray-400 uppercase tracking-widest ml-1">购买金额 (¥)</label>
              <input v-model.number="newAsset.amount" type="number" step="0.01" class="w-full text-lg py-3" required />
            </div>
            <div class="space-y-2">
              <label class="text-xs font-bold text-gray-400 uppercase tracking-widest ml-1">资产类型</label>
              <select v-model="newAsset.type" class="w-full text-lg py-3 appearance-none bg-white dark:bg-gray-700">
                <option v-for="t in allTypes" :key="t.id" :value="t.name">{{ t.name }}</option>
              </select>
            </div>
          </div>

          <div class="space-y-2">
            <label class="text-xs font-bold text-gray-400 uppercase tracking-widest ml-1">购买日期</label>
            <input v-model="newAsset.purchase_date" type="date" class="w-full text-lg py-3" required />
          </div>

          <button 
            type="submit" 
            class="w-full bg-black dark:bg-white text-white dark:text-black py-5 rounded-2xl font-black text-lg hover:bg-gray-800 dark:hover:bg-gray-200 transition-all shadow-lg hover:shadow-xl active:scale-95"
          >
            确认保存
          </button>
        </form>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4 animate-in fade-in duration-300">
      <div class="bg-white dark:bg-gray-800 rounded-[32px] w-full max-w-md p-10 shadow-2xl animate-in zoom-in-95 slide-in-from-bottom-10 duration-500">
        <div class="flex justify-between items-center mb-10">
          <h2 class="text-3xl font-black tracking-tight dark:text-white">编辑资产</h2>
          <button @click="showEditModal = false" class="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-full transition-all">
            <X :size="24" />
          </button>
        </div>

        <form @submit.prevent="handleEdit" class="space-y-8">
          <div class="space-y-2">
            <label class="text-xs font-bold text-gray-400 uppercase tracking-widest ml-1">资产名称</label>
            <input v-model="editAsset.name" type="text" class="w-full text-lg py-3" required />
          </div>

          <div class="grid grid-cols-2 gap-6">
            <div class="space-y-2">
              <label class="text-xs font-bold text-gray-400 uppercase tracking-widest ml-1">购买金额 (¥)</label>
              <input v-model.number="editAsset.amount" type="number" step="0.01" class="w-full text-lg py-3" required />
            </div>
            <div class="space-y-2">
              <label class="text-xs font-bold text-gray-400 uppercase tracking-widest ml-1">资产类型</label>
              <select v-model="editAsset.type" class="w-full text-lg py-3 appearance-none bg-white dark:bg-gray-700">
                <option v-for="t in allTypes" :key="t.id" :value="t.name">{{ t.name }}</option>
              </select>
            </div>
          </div>

          <div class="space-y-2">
            <label class="text-xs font-bold text-gray-400 uppercase tracking-widest ml-1">购买日期</label>
            <input v-model="editAsset.purchase_date" type="date" class="w-full text-lg py-3" required />
          </div>

          <button 
            type="submit" 
            class="w-full bg-black dark:bg-white text-white dark:text-black py-5 rounded-2xl font-black text-lg hover:bg-gray-800 dark:hover:bg-gray-200 transition-all shadow-lg hover:shadow-xl active:scale-95"
          >
            确认保存
          </button>
        </form>
      </div>
    </div>

    <!-- Sell Modal -->
    <div v-if="showSellModal" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4 animate-in fade-in duration-300">
      <div class="bg-white dark:bg-gray-800 rounded-[32px] w-full max-w-md p-10 shadow-2xl animate-in zoom-in-95 slide-in-from-bottom-10 duration-500">
        <div class="flex justify-between items-center mb-10">
          <div>
            <h2 class="text-3xl font-black tracking-tight dark:text-white">出售资产</h2>
            <p class="text-gray-400 dark:text-gray-500 text-sm mt-1">记录 {{ selectedAsset?.name }} 的出售信息</p>
          </div>
          <button @click="showSellModal = false" class="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-full transition-all">
            <X :size="24" />
          </button>
        </div>

        <form @submit.prevent="handleSell" class="space-y-8">
          <div class="space-y-2">
            <label class="text-xs font-bold text-gray-400 uppercase tracking-widest ml-1">出售价格 (¥)</label>
            <input v-model.number="sellInfo.sold_price" type="number" step="0.01" class="w-full text-lg py-3" required />
          </div>

          <div class="space-y-2">
            <label class="text-xs font-bold text-gray-400 uppercase tracking-widest ml-1">出售日期</label>
            <input v-model="sellInfo.sold_date" type="date" class="w-full text-lg py-3" required />
          </div>

          <div class="bg-blue-50 dark:bg-blue-900/30 p-4 rounded-2xl text-blue-600 dark:text-blue-400 text-xs font-medium leading-relaxed">
            出售后，系统将根据购买价与出售价的差额重新计算日均价值消耗。
          </div>

          <button 
            type="submit" 
            class="w-full bg-black dark:bg-white text-white dark:text-black py-5 rounded-2xl font-black text-lg hover:bg-gray-800 dark:hover:bg-gray-200 transition-all shadow-lg hover:shadow-xl active:scale-95"
          >
            确认出售
          </button>
        </form>
      </div>
    </div>

    <!-- Type Manager Modal -->
    <div v-if="showTypeManager" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4 animate-in fade-in duration-300">
      <div class="bg-white dark:bg-gray-800 rounded-[32px] w-full max-w-2xl h-[80vh] flex flex-col animate-in zoom-in-95 slide-in-from-bottom-10 duration-500">
        <div class="p-6 border-b border-gray-100 dark:border-gray-700 flex justify-between items-center">
          <h2 class="text-2xl font-black tracking-tight dark:text-white">分类管理</h2>
          <button @click="showTypeManager = false" class="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-full transition-all">
            <X :size="24" />
          </button>
        </div>
        
        <div class="flex-1 overflow-y-auto p-6">
          <AssetTypeManager :show="showTypeManager" @close="showTypeManager = false" @updated="fetchAssetTypes" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
input[type="date"]::-webkit-calendar-picker-indicator {
  cursor: pointer;
  filter: grayscale(1);
}

select {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%239ca3af'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'%3E%3C/path%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: 1.5em;
}
</style>
