import { useEffect, useState } from 'react'
import Header from '../components/layout/Header'
import ChartCard from '../components/charts/ChartCard'
import SpendBarChart from '../components/charts/SpendBarChart'
import { getBudgetAnalysis, exportCsv } from '../services/api'
import { fmt } from '../lib/utils'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

export default function BudgetAnalysis() {
  const [data, setData] = useState(null)

  useEffect(() => {
    getBudgetAnalysis().then((r) => setData(r.data)).catch(() => {})
  }, [])

  return (
    <div>
      <Header title="Budget & Variance Analysis">
        <button onClick={() => exportCsv('budget')} className="btn-secondary text-sm">Export CSV</button>
      </Header>
      <div className="p-6 space-y-6">
        {data && (
          <>
            <div className="flex gap-6 text-sm">
              <span>Budget Utilisation: <span className={`font-bold ${data.utilisation_pct > 100 ? 'text-red-600' : 'text-brand-600'}`}>{fmt(data.utilisation_pct, { type: 'percent', decimals: 1 })}</span></span>
              {data.overspending.length > 0 && <span className="text-red-600">{data.overspending.length} categories over budget</span>}
            </div>

            <ChartCard title="Budget vs Actual Spend by Category">
              <ResponsiveContainer width="100%" height={320}>
                <BarChart data={data.budget_vs_actual.slice(0, 15)} margin={{ top: 4, right: 8, left: 0, bottom: 60 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis dataKey="category" tick={{ fontSize: 11 }} angle={-35} textAnchor="end" interval={0} />
                  <YAxis tick={{ fontSize: 11 }} tickFormatter={(v) => fmt(v, { decimals: 0 })} width={80} />
                  <Tooltip formatter={(v) => fmt(v, { decimals: 2 })} />
                  <Legend />
                  <Bar dataKey="budget" name="Budget" fill="#3b5bdb" radius={[3, 3, 0, 0]} />
                  <Bar dataKey="actual" name="Actual" fill="#0ca678" radius={[3, 3, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </ChartCard>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <ChartCard title="Variance by Category">
                <div className="overflow-auto max-h-72">
                  <table className="w-full text-sm">
                    <thead className="bg-gray-50 text-xs text-gray-500 uppercase sticky top-0">
                      <tr>
                        <th className="px-3 py-2 text-left">Category</th>
                        <th className="px-3 py-2 text-right">Budget</th>
                        <th className="px-3 py-2 text-right">Actual</th>
                        <th className="px-3 py-2 text-right">Variance</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100">
                      {data.variance_table.map((r, i) => (
                        <tr key={i} className={r.variance > 0 ? 'bg-red-50' : ''}>
                          <td className="px-3 py-2">{r.category}</td>
                          <td className="px-3 py-2 text-right">{fmt(r.budget)}</td>
                          <td className="px-3 py-2 text-right">{fmt(r.actual)}</td>
                          <td className={`px-3 py-2 text-right font-medium ${r.variance > 0 ? 'text-red-600' : 'text-green-600'}`}>
                            {r.variance > 0 ? '+' : ''}{fmt(r.variance)}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </ChartCard>

              {data.by_region.length > 0 && (
                <ChartCard title="Spend by Region">
                  <SpendBarChart data={data.by_region} color="#e64980" />
                </ChartCard>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  )
}
