import axios from 'axios'

const API_PORT = 8000
const api = axios.create({
  baseURL: `http://${window.location.hostname}:${API_PORT}/api`,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const assetTypesApi = {
  getAll: () => api.get('/types'),
  getCustom: () => api.get('/types/custom'),
  create: (data: any) => api.post('/types', data),
  update: (id: number, data: any) => api.put(`/types/${id}`, data),
  delete: (id: number) => api.delete(`/types/${id}`)
}

export default api
