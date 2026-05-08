import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import AppLayout from './components/layout/AppLayout'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Upload from './pages/Upload'
import SpendAnalysis from './pages/SpendAnalysis'
import CategoryAnalysis from './pages/CategoryAnalysis'
import SupplierAnalysis from './pages/SupplierAnalysis'
import InventoryAnalysis from './pages/InventoryAnalysis'
import BudgetAnalysis from './pages/BudgetAnalysis'
import GeographicAnalysis from './pages/GeographicAnalysis'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route element={<AppLayout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/upload" element={<Upload />} />
          <Route path="/spend" element={<SpendAnalysis />} />
          <Route path="/category" element={<CategoryAnalysis />} />
          <Route path="/supplier" element={<SupplierAnalysis />} />
          <Route path="/inventory" element={<InventoryAnalysis />} />
          <Route path="/budget" element={<BudgetAnalysis />} />
          <Route path="/geographic" element={<GeographicAnalysis />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
