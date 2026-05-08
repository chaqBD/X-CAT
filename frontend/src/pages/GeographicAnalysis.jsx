import { useEffect, useState } from 'react'
import Header from '../components/layout/Header'
import ChartCard from '../components/charts/ChartCard'
import SpendBarChart from '../components/charts/SpendBarChart'
import SpendPieChart from '../components/charts/SpendPieChart'
import { getGeographicAnalysis } from '../services/api'
import { fmt } from '../lib/utils'

export default function GeographicAnalysis() {
  const [data, setData] = useState(null)

  useEffect(() => {
    getGeographicAnalysis().then((r) => setData(r.data)).catch(() => {})
  }, [])

  return (
    <div>
      <Header title="Geographic / Regional Analysis" />
      <div className="p-6 space-y-6">
        {data && (
          <>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <ChartCard title="Spend by Region">
                <SpendBarChart data={data.spend_by_region} color="#1c7ed6" />
              </ChartCard>
              <ChartCard title="Supplier Distribution by Country">
                <SpendPieChart data={data.suppliers_by_country} />
              </ChartCard>
            </div>

            {data.regional_activity.length > 0 && (
              <ChartCard title="Regional Procurement Activity">
                <div className="overflow-auto max-h-72">
                  <table className="w-full text-sm">
                    <thead className="bg-gray-50 text-xs text-gray-500 uppercase sticky top-0">
                      <tr>
                        <th className="px-3 py-2 text-left">Region</th>
                        <th className="px-3 py-2 text-right">Total Spend</th>
                        <th className="px-3 py-2 text-right">Transactions</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100">
                      {data.regional_activity.map((r, i) => (
                        <tr key={i} className="hover:bg-gray-50">
                          <td className="px-3 py-2 font-medium">{r.region}</td>
                          <td className="px-3 py-2 text-right">{fmt(r.total_spend)}</td>
                          <td className="px-3 py-2 text-right">{r.transactions}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </ChartCard>
            )}
          </>
        )}
      </div>
    </div>
  )
}
