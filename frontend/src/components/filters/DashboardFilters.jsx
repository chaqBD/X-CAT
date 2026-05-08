export default function DashboardFilters({ filters, onChange }) {
  const set = (key, value) => onChange({ ...filters, [key]: value })

  return (
    <div className="flex flex-wrap gap-3 items-center">
      <div className="flex items-center gap-2">
        <label className="text-xs font-medium text-gray-500 whitespace-nowrap">From</label>
        <input
          type="date"
          value={filters.date_from || ''}
          onChange={(e) => set('date_from', e.target.value)}
          className="text-sm border border-gray-300 rounded-lg px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-brand-500"
        />
      </div>
      <div className="flex items-center gap-2">
        <label className="text-xs font-medium text-gray-500 whitespace-nowrap">To</label>
        <input
          type="date"
          value={filters.date_to || ''}
          onChange={(e) => set('date_to', e.target.value)}
          className="text-sm border border-gray-300 rounded-lg px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-brand-500"
        />
      </div>
      {(filters.date_from || filters.date_to) && (
        <button
          onClick={() => onChange({ ...filters, date_from: '', date_to: '' })}
          className="text-xs text-brand-600 hover:text-brand-700 underline"
        >
          Clear dates
        </button>
      )}
    </div>
  )
}
