import { Download } from 'lucide-react'
import html2canvas from 'html2canvas'
import { useRef } from 'react'

export default function ChartCard({ title, children, className = '' }) {
  const ref = useRef(null)

  const exportPng = async () => {
    if (!ref.current) return
    const canvas = await html2canvas(ref.current, { scale: 2 })
    const a = document.createElement('a')
    a.href = canvas.toDataURL('image/png')
    a.download = `${title.replace(/\s+/g, '_')}.png`
    a.click()
  }

  return (
    <div ref={ref} className={`card p-5 ${className}`}>
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold text-gray-800 text-sm">{title}</h3>
        <button onClick={exportPng} title="Export PNG" className="text-gray-400 hover:text-gray-600 transition-colors">
          <Download size={15} />
        </button>
      </div>
      {children}
    </div>
  )
}
