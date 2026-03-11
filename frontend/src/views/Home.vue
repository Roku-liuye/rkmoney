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
  Coins
} from 'lucide-vue-next'
import dayjs from 'dayjs'
import type { Asset } from '../types'

const store = useAssetStore()
const showAddModal = ref(false)
const showSellModal = ref(false)
const selectedAsset = ref<Asset | null>(null)

const newAsset = ref({
  name: '',
  amount: 0,
  purchase_date: dayjs().format('YYYY-MM-DD'),
  type: '其他'
})

const sellInfo = ref({
  sold_date: dayjs().format('YYYY-MM-DD'),
  sold_price: 0
})

const assetTypes = [
  { name: '数码', icon: Package },
  { name: '生活', icon: ShoppingBag },
  { name: '理财', icon: CreditCard },
  { name: '其他', icon: Package }
]

onMounted(() => {
  store.fetchAssets()
})

const totalDailyValue = computed(() => {
  return store.assets.reduce((sum, asset) => sum + (asset.sold_date ? 0 : asset.daily_value), 0)
})

const handleSubmit = async () => {
  if (!newAsset.value.name || newAsset.value.amount <= 0) return
  
  try {
    await store.addAsset({
      ...newAsset.value,
      type_icon: ''
    })
    showAddModal.value = false
    newAsset.value = {
      name: '',
      amount: 0,
      purchase_date: dayjs().format('YYYY-MM-DD'),
      type: '其他'
    }
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
</script>

<template>
  <div class="max-w-4xl mx-auto px-6 py-12">
    <!-- Header -->
    <header class="flex justify-between items-end mb-12">
      <div>
        <h1 class="text-3xl font-bold tracking-tight text-gray-900 mb-2">Rkmoney</h1>
        <p class="text-gray-500 font-medium">资产价值记录系统</p>
      </div>
      <button 
        @click="showAddModal = true"
        class="bg-black text-white px-6 py-2.5 rounded-full flex items-center gap-2 hover:bg-gray-800 transition-all shadow-sm active:scale-95"
      >
        <Plus :size="18" />
        <span class="font-medium">新增资产</span>
      </button>
    </header>

    <!-- Stats -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
      <div class="bg-gray-50 p-8 rounded-3xl border border-gray-100">
        <div class="flex items-center gap-2 text-gray-400 mb-3">
          <TrendingUp :size="16" />
          <span class="text-xs font-bold uppercase tracking-widest">总计日均价值消耗</span>
        </div>
        <div class="text-4xl font-bold tracking-tight">{{ formatCurrency(totalDailyValue) }}</div>
      </div>
      <div class="bg-gray-50 p-8 rounded-3xl border border-gray-100">
        <div class="flex items-center gap-2 text-gray-400 mb-3">
          <Package :size="16" />
          <span class="text-xs font-bold uppercase tracking-widest">持有资产总数</span>
        </div>
        <div class="text-4xl font-bold tracking-tight">{{ store.assets.filter(a => !a.sold_date).length }}</div>
      </div>
    </div>

    <!-- Section Title -->
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-xl font-bold text-gray-900">资产列表</h2>
      <div class="text-sm text-gray-400">共 {{ store.assets.length }} 个资产</div>
    </div>

    <!-- Asset List -->
    <div v-if="store.loading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-black"></div>
    </div>

    <div v-else-if="store.assets.length === 0" class="text-center py-20 bg-gray-50 rounded-3xl border border-dashed border-gray-200">
      <div class="text-gray-400 mb-4">开启您的资产管理之旅</div>
      <button @click="showAddModal = true" class="text-black font-bold hover:underline">点击此处添加您的第一个资产</button>
    </div>

    <div v-else class="space-y-4">
      <div 
        v-for="asset in store.assets" 
        :key="asset.id"
        class="group bg-white p-6 rounded-3xl border border-gray-100 hover:border-gray-300 hover:shadow-xl transition-all flex items-center gap-6"
        :class="{'opacity-60 grayscale-[0.5]': asset.sold_date}"
      >
        <!-- Icon -->
        <div class="h-14 w-14 bg-gray-50 rounded-2xl flex items-center justify-center text-gray-400 group-hover:bg-black group-hover:text-white transition-all duration-300">
          <Package v-if="asset.type === '数码'" :size="28" />
          <ShoppingBag v-else-if="asset.type === '生活'" :size="28" />
          <CreditCard v-else-if="asset.type === '理财'" :size="28" />
          <Package v-else :size="28" />
        </div>

        <!-- Info -->
        <div class="flex-1">
          <div class="flex items-center gap-2 mb-1">
            <h3 class="font-bold text-lg text-gray-900">{{ asset.name }}</h3>
            <span v-if="asset.sold_date" class="px-2 py-0.5 bg-gray-100 text-gray-500 text-[10px] font-bold rounded-md uppercase">已出售</span>
          </div>
          <div class="flex flex-wrap items-center gap-x-6 gap-y-1 text-sm text-gray-400">
            <span class="flex items-center gap-1.5">
              <CircleDollarSign :size="14" />
              {{ formatCurrency(asset.amount) }}
            </span>
            <span class="flex items-center gap-1.5">
              <Calendar :size="14" />
              {{ formatDate(asset.purchase_date) }}
            </span>
            <span v-if="!asset.sold_date" class="flex items-center gap-1.5">
              <History :size="14" />
              已持 {{ getDaysSincePurchase(asset.purchase_date) }} 天
            </span>
          </div>
        </div>

        <!-- Value -->
        <div class="text-right">
          <div class="text-[10px] text-gray-400 uppercase tracking-widest mb-1 font-bold">日均价值</div>
          <div class="text-2xl font-black tracking-tighter" :class="asset.sold_date ? 'text-gray-400' : 'text-black'">
            {{ formatCurrency(asset.daily_value) }}
          </div>
        </div>

        <!-- Actions -->
        <div class="flex items-center gap-1 ml-4">
          <button 
            v-if="!asset.sold_date"
            @click="openSellModal(asset)"
            class="opacity-0 group-hover:opacity-100 p-2 text-gray-400 hover:text-black hover:bg-gray-100 rounded-xl transition-all"
            title="标记为出售"
          >
            <Coins :size="20" />
          </button>
          <button 
            @click="handleDelete(asset.id)"
            class="opacity-0 group-hover:opacity-100 p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-xl transition-all"
            title="删除"
          >
            <Trash2 :size="20" />
          </button>
        </div>
      </div>
    </div>

    <!-- Add Modal -->
    <div v-if="showAddModal" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4 animate-in fade-in duration-300">
      <div class="bg-white rounded-[32px] w-full max-w-md p-10 shadow-2xl animate-in zoom-in-95 slide-in-from-bottom-10 duration-500">
        <div class="flex justify-between items-center mb-10">
          <h2 class="text-3xl font-black tracking-tight">新增资产</h2>
          <button @click="showAddModal = false" class="p-2 hover:bg-gray-100 rounded-full transition-all">
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
              <select v-model="newAsset.type" class="w-full text-lg py-3 appearance-none">
                <option v-for="t in assetTypes" :key="t.name" :value="t.name">{{ t.name }}</option>
              </select>
            </div>
          </div>

          <div class="space-y-2">
            <label class="text-xs font-bold text-gray-400 uppercase tracking-widest ml-1">购买日期</label>
            <input v-model="newAsset.purchase_date" type="date" class="w-full text-lg py-3" required />
          </div>

          <button 
            type="submit" 
            class="w-full bg-black text-white py-5 rounded-2xl font-black text-lg hover:bg-gray-800 transition-all shadow-lg hover:shadow-xl active:scale-95"
          >
            确认保存
          </button>
        </form>
      </div>
    </div>

    <!-- Sell Modal -->
    <div v-if="showSellModal" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4 animate-in fade-in duration-300">
      <div class="bg-white rounded-[32px] w-full max-w-md p-10 shadow-2xl animate-in zoom-in-95 slide-in-from-bottom-10 duration-500">
        <div class="flex justify-between items-center mb-10">
          <div>
            <h2 class="text-3xl font-black tracking-tight">出售资产</h2>
            <p class="text-gray-400 text-sm mt-1">记录 {{ selectedAsset?.name }} 的出售信息</p>
          </div>
          <button @click="showSellModal = false" class="p-2 hover:bg-gray-100 rounded-full transition-all">
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

          <div class="bg-blue-50 p-4 rounded-2xl text-blue-600 text-xs font-medium leading-relaxed">
            出售后，系统将根据购买价与出售价的差额重新计算日均价值消耗。
          </div>

          <button 
            type="submit" 
            class="w-full bg-black text-white py-5 rounded-2xl font-black text-lg hover:bg-gray-800 transition-all shadow-lg hover:shadow-xl active:scale-95"
          >
            确认出售
          </button>
        </form>
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
