import { useEffect, useState } from 'react'
import Header from '../components/layout/Header'
import ChartCard from '../components/charts/ChartCard'
import SpendBarChart from '../components/charts/SpendBarChart'
import SpendPieChart from '../components/charts/SpendPieChart'
import DashboardFilters from '../components/filters/DashboardFilters'
import { getCategoryAnalysis } from '../services/api'
import { fmt } from '../lib/utils'

export default function CategoryAnalysis() {
  const [data, setData] = useState(null)
  const [filters, setFilters] = useState({})

  useEffect(() => {
    getCategoryAnalysis(filters).then((r) => setData(r.data)).catch(() => {})
  }, [filters])

  return (
    <div>
      <Header title="Category Analysis" />
      <div className="p-6 space-y-6">
        <DashboardFilters filters={filters} onChange={setFilters} />
        {data && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <ChartCard title="Category Rankings">
                <SpendBarChart data={data.rankings} />
              </ChartCard>
              <ChartCard title="Category Contribution %">
                <SpendPieChart data={data.contribution} dataKey="value" />
              </ChartCard>
            </div>

            {data.budget_utilisation.length > 0 && (
              <ChartCard title="Budget Utilisation % by Category">
                <SpendBarChart data={data.budget_utilisation} color="#f59f00" />
              </ChartCard>
            )}

            {data.mom_growth.length > 0 && (
              <ChartCard title="Month-on-Month Growth (%)">
                <div className="overflow-auto max-h-64">
                  <table className="w-full text-sm">
                    <thead className="bg-gray-50 text-xs text-gray-500 uppercase sticky top-0">
                      <tr>
                        <th className="px-3 py-2 text-left">Category</th>
                        <th className="px-3 py-2 text-right">MoM Growth</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100">
                      {data.mom_growth.map((r, i) => (
                        <tr key={i}>
                          <td className="px-3 py-2">{r.name}</td>
                          <td className={`px-3 py-2 text-right font-medium ${r.value >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                            {r.value >= 0 ? '+' : ''}{fmt(r.value, { type: 'percent', decimals: 1 })}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </ChartCard>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
