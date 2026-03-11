import { defineStore } from 'pinia'
import api from '../api'
import type { Asset, AssetCreate, ApiResponse } from '../types'

export const useAssetStore = defineStore('asset', {
  state: () => ({
    assets: [] as Asset[],
    loading: false,
    error: null as string | null
  }),

  actions: {
    async fetchAssets() {
      this.loading = true
      try {
        const response = await api.get<ApiResponse<Asset[]>>('/assets')
        this.assets = response.data.data
      } catch (err: any) {
        this.error = err.message || 'Failed to fetch assets'
      } finally {
        this.loading = false
      }
    },

    async addAsset(asset: AssetCreate) {
      try {
        const response = await api.post<ApiResponse<Asset>>('/assets', asset)
        this.assets.push(response.data.data)
        return response.data.data
      } catch (err: any) {
        throw err
      }
    },

    async deleteAsset(id: number) {
      try {
        await api.delete(`/assets/${id}`)
        this.assets = this.assets.filter(a => a.id !== id)
      } catch (err: any) {
        throw err
      }
    },

    async sellAsset(id: number, sold_date: string, sold_price: number) {
      try {
        const response = await api.post<ApiResponse<Asset>>(`/assets/${id}/sell`, null, {
          params: { sold_date, sold_price }
        })
        const index = this.assets.findIndex(a => a.id === id)
        if (index !== -1) {
          this.assets[index] = response.data.data
        }
        return response.data.data
      } catch (err: any) {
        throw err
      }
    }
  }
})
