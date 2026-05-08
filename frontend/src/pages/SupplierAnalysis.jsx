import { useEffect, useState } from 'react'
import Header from '../components/layout/Header'
import ChartCard from '../components/charts/ChartCard'
import SpendBarChart from '../components/charts/SpendBarChart'
import SpendPieChart from '../components/charts/SpendPieChart'
import { getSupplierAnalysis, exportCsv } from '../services/api'
import { fmt } from '../lib/utils'

export default function SupplierAnalysis() {
  const [data, setData] = useState(null)

  useEffect(() => {
    getSupplierAnalysis().then((r) => setData(r.data)).catch(() => {})
  }, [])

  return (
    <div>
      <Header title="Supplier Analysis">
        <button onClick={() => exportCsv('supplier')} className="btn-secondary text-sm">Export CSV</button>
      </Header>
      <div className="p-6 space-y-6">
        {data && (
          <>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <ChartCard title="Supplier Rankings by Spend">
                <SpendBarChart data={data.rankings} color="#7950f2" />
              </ChartCard>
              <ChartCard title="Spend Concentration (Top 10)">
                <SpendPieChart data={data.concentration} />
              </ChartCard>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {data.lead_time_avg.length > 0 && (
                <ChartCard title="Average Lead Time by Supplier (days)">
                  <SpendBarChart data={data.lead_time_avg} color="#fd7e14" />
                </ChartCard>
              )}
              {data.risk_breakdown.length > 0 && (
                <ChartCard title="Supplier Risk Level Breakdown">
                  <SpendPieChart data={data.risk_breakdown} />
                </ChartCard>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  )
}
