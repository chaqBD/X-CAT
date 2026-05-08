import { useEffect, useState } from 'react'
import { TrendingUp, ShoppingCart, Users, Tag, DollarSign, AlertTriangle } from 'lucide-react'
import Header from '../components/layout/Header'
import ChartCard from '../components/charts/ChartCard'
import SpendBarChart from '../components/charts/SpendBarChart'
import TrendLineChart from '../components/charts/TrendLineChart'
import SpendPieChart from '../components/charts/SpendPieChart'
import { getExecutiveDashboard } from '../services/api'
import { fmt } from '../lib/utils'

const KPICard = ({ icon: Icon, label, value, color = 'text-brand-600', bg = 'bg-brand-50' }) => (
  <div className="kpi-card">
    <div className={`w-9 h-9 rounded-lg ${bg} flex items-center justify-center mb-1`}>
      <Icon size={18} className={color} />
    </div>
    <p className="text-xs text-gray-500">{label}</p>
    <p className="text-xl font-bold text-gray-900">{value}</p>
  </div>
)

export default function Dashboard() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getExecutiveDashboard()
      .then((r) => setData(r.data))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="p-8 text-gray-400">Loading dashboard…</div>

  if (!data || !data.total_transactions) {
    return (
      <div>
        <Header title="Executive Dashboard" />
        <div className="p-8 text-center">
          <p className="text-gray-500 mb-3">No data yet. Upload a dataset to see your dashboard.</p>
          <a href="/upload" className="btn-primary inline-block">Upload Data</a>
        </div>
      </div>
    )
  }

  return (
    <div>
      <Header title="Executive Dashboard" />
      <div className="p-6 space-y-6">
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          <KPICard icon={DollarSign} label="Total Spend" value={fmt(data.total_spend)} />
          <KPICard icon={ShoppingCart} label="Transactions" value={fmt(data.total_transactions, { type: 'number' })} bg="bg-emerald-50" color="text-emerald-600" />
          <KPICard icon={Users} label="Suppliers" value={fmt(data.total_suppliers, { type: 'number' })} bg="bg-violet-50" color="text-violet-600" />
          <KPICard icon={Tag} label="Top Category" value={data.top_category} bg="bg-amber-50" color="text-amber-600" />
          <KPICard icon={TrendingUp} label="Budget Used" value={fmt(data.budget_utilisation_pct, { type: 'percent', decimals: 1 })} bg="bg-sky-50" color="text-sky-600" />
          <KPICard icon={AlertTriangle} label="Low Stock Items" value={data.low_stock_count} bg="bg-rose-50" color="text-rose-600" />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <ChartCard title="Spend by Category">
            <SpendBarChart data={data.spend_by_category} color="#3b5bdb" />
          </ChartCard>
          <ChartCard title="Top Suppliers by Spend">
            <SpendPieChart data={data.top_suppliers} />
          </ChartCard>
        </div>

        <ChartCard title="Monthly Spend Trend">
          <TrendLineChart data={data.monthly_trend} height={240} />
        </ChartCard>
      </div>
    </div>
  )
}
