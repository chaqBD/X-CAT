import { useEffect, useState, useCallback } from 'react'
import Header from '../components/layout/Header'
import ChartCard from '../components/charts/ChartCard'
import SpendBarChart from '../components/charts/SpendBarChart'
import SpendPieChart from '../components/charts/SpendPieChart'
import SpendTreeMap from '../components/charts/SpendTreeMap'
import TrendLineChart from '../components/charts/TrendLineChart'
import DashboardFilters from '../components/filters/DashboardFilters'
import { getSpendAnalysis, exportCsv } from '../services/api'
import { fmt } from '../lib/utils'

export default function SpendAnalysis() {
  const [data, setData] = useState(null)
  const [filters, setFilters] = useState({})
  const [loading, setLoading] = useState(true)

  const load = useCallback(() => {
    setLoading(true)
    getSpendAnalysis(filters)
      .then((r) => setData(r.data))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [filters])

  useEffect(() => { load() }, [load])

  return (
    <div>
      <Header title="Spend Analysis">
        <button onClick={() => exportCsv('procurement')} className="btn-secondary text-sm">Export CSV</button>
      </Header>

      <div className="p-6 space-y-6">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <DashboardFilters filters={filters} onChange={setFilters} />
          {data && (
            <div className="flex gap-6 text-sm">
              <span className="font-medium">Total: <span className="text-brand-600 font-bold">{fmt(data.total_spend)}</span></span>
              <span className="text-gray-500">{fmt(data.total_transactions, { type: 'number' })} transactions</span>
              <span className="text-gray-500">{data.total_suppliers} suppliers</span>
            </div>
          )}
        </div>

        {loading ? <p className="text-gray-400">Loading…</p> : !data ? null : (
          <div className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <ChartCard title="Spend by Category">
                <SpendBarChart data={data.by_category} />
              </ChartCard>
              <ChartCard title="Category Contribution">
                <SpendTreeMap data={data.by_category} />
              </ChartCard>
            </div>

            <ChartCard title="Monthly Spend Trend">
              <TrendLineChart data={data.monthly_trend} height={240} />
            </ChartCard>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <ChartCard title="Top Suppliers by Spend">
                <SpendBarChart data={data.by_supplier} color="#0ca678" />
              </ChartCard>
              <ChartCard title="Top 10 Products">
                <div className="overflow-auto max-h-72">
                  <table className="w-full text-sm">
                    <thead className="bg-gray-50 text-xs text-gray-500 uppercase sticky top-0">
                      <tr>
                        <th className="px-3 py-2 text-left">Product</th>
                        <th className="px-3 py-2 text-right">Spend</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100">
                      {data.top_products.map((p, i) => (
                        <tr key={i} className="hover:bg-gray-50">
                          <td className="px-3 py-2">{p.name}</td>
                          <td className="px-3 py-2 text-right font-medium">{fmt(p.value)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </ChartCard>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
