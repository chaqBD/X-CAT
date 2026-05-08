import axios from 'axios'
import useAuthStore from '../store/authStore'

const api = axios.create({
  baseURL: '/api',
})

api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  (r) => r,
  (err) => {
    if (err.response?.status === 401) {
      useAuthStore.getState().logout()
      window.location.href = '/login'
    }
    return Promise.reject(err)
  }
)

// Auth
export const register = (data) => api.post('/auth/register', data)
export const login = (data) => api.post('/auth/login', data)
export const me = () => api.get('/auth/me')

// Uploads
export const uploadFile = (formData) => api.post('/uploads/', formData)
export const getUploads = () => api.get('/uploads/')
export const getUpload = (id) => api.get(`/uploads/${id}`)
export const deleteUpload = (id) => api.delete(`/uploads/${id}`)

// Dashboard
export const getExecutiveDashboard = () => api.get('/dashboard/executive')

// Analytics
export const getSpendAnalysis = (params) => api.get('/analytics/spend', { params })
export const getCategoryAnalysis = (params) => api.get('/analytics/category', { params })
export const getSupplierAnalysis = () => api.get('/analytics/supplier')
export const getInventoryAnalysis = () => api.get('/analytics/inventory')
export const getBudgetAnalysis = () => api.get('/analytics/budget')
export const getGeographicAnalysis = () => api.get('/analytics/geographic')

// Exports
export const exportCsv = (datasetType) =>
  api.get(`/exports/csv/${datasetType}`, { responseType: 'blob' }).then((res) => {
    const url = window.URL.createObjectURL(new Blob([res.data]))
    const a = document.createElement('a')
    a.href = url
    a.download = `xcat_${datasetType}.csv`
    a.click()
    window.URL.revokeObjectURL(url)
  })

export default api
