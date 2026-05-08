import { useEffect, useState } from 'react'
import { AlertTriangle } from 'lucide-react'
import Header from '../components/layout/Header'
import ChartCard from '../components/charts/ChartCard'
import SpendBarChart from '../components/charts/SpendBarChart'
import SpendPieChart from '../components/charts/SpendPieChart'
import { getInventoryAnalysis, exportCsv } from '../services/api'
import { fmt } from '../lib/utils'

export default function InventoryAnalysis() {
  const [data, setData] = useState(null)

  useEffect(() => {
    getInventoryAnalysis().then((r) => setData(r.data)).catch(() => {})
  }, [])

  return (
    <div>
      <Header title="Inventory Analysis">
        <button onClick={() => exportCsv('inventory')} className="btn-secondary text-sm">Export CSV</button>
      </Header>
      <div className="p-6 space-y-6">
        {data && (
          <>
            {data.low_stock_count > 0 && (
              <div className="flex items-center gap-3 bg-amber-50 border border-amber-200 text-amber-800 rounded-xl px-5 py-3 text-sm">
                <AlertTriangle size={16} />
                <span><strong>{data.low_stock_count}</strong> product(s) at or below reorder level</span>
              </div>
            )}

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <ChartCard title="Current Stock Levels">
                <SpendBarChart data={data.stock_levels.slice(0, 20)} color="#20c997" />
              </ChartCard>
              <ChartCard title="Inventory Value by Warehouse">
                <SpendPieChart data={data.by_warehouse} />
              </ChartCard>
            </div>

            {data.low_stock.length > 0 && (
              <ChartCard title="Low Stock Alert">
                <div className="overflow-auto max-h-64">
                  <table className="w-full text-sm">
                    <thead className="bg-red-50 text-xs text-red-600 uppercase sticky top-0">
                      <tr>
                        {['Product', 'Category', 'Stock', 'Reorder', 'Warehouse'].map((h) => (
                          <th key={h} className="px-3 py-2 text-left">{h}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100">
                      {data.low_stock.map((r, i) => (
                        <tr key={i} className="hover:bg-red-50">
                          <td className="px-3 py-2 font-medium">{r.product}</td>
                          <td className="px-3 py-2 text-gray-500">{r.category}</td>
                          <td className="px-3 py-2 text-red-600 font-bold">{r.stock_level}</td>
                          <td className="px-3 py-2">{r.reorder_level}</td>
                          <td className="px-3 py-2">{r.warehouse}</td>
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
