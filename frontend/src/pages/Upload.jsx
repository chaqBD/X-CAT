import { useState, useEffect } from 'react'
import { Trash2 } from 'lucide-react'
import Header from '../components/layout/Header'
import DropZone from '../components/upload/DropZone'
import ValidationReport from '../components/upload/ValidationReport'
import { uploadFile, getUploads, deleteUpload } from '../services/api'

const TYPES = [
  { value: '', label: 'Auto-detect' },
  { value: 'procurement', label: 'Procurement Transactions' },
  { value: 'supplier', label: 'Supplier Data' },
  { value: 'inventory', label: 'Inventory' },
  { value: 'budget', label: 'Budget' },
]

const STATUS_BADGE = {
  valid: 'bg-green-100 text-green-700',
  invalid: 'bg-red-100 text-red-700',
  processing: 'bg-yellow-100 text-yellow-700',
  pending: 'bg-gray-100 text-gray-600',
}

export default function Upload() {
  const [file, setFile] = useState(null)
  const [type, setType] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [history, setHistory] = useState([])

  const loadHistory = () => getUploads().then((r) => setHistory(r.data)).catch(() => {})

  useEffect(() => { loadHistory() }, [])

  const submit = async (e) => {
    e.preventDefault()
    if (!file) return
    setLoading(true)
    setResult(null)
    try {
      const fd = new FormData()
      fd.append('file', file)
      if (type) fd.append('dataset_type', type)
      const { data } = await uploadFile(fd)
      setResult(data)
      loadHistory()
    } catch (err) {
      alert(err.response?.data?.detail || 'Upload failed')
    } finally {
      setLoading(false)
    }
  }

  const remove = async (id) => {
    if (!confirm('Delete this upload and all its data?')) return
    await deleteUpload(id).catch(() => {})
    loadHistory()
  }

  return (
    <div>
      <Header title="Upload Data" />
      <div className="p-6 max-w-3xl mx-auto space-y-6">
        <div className="card p-6">
          <form onSubmit={submit} className="space-y-5">
            <DropZone onDrop={setFile} file={file} />
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Dataset Type</label>
              <select value={type} onChange={(e) => setType(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500">
                {TYPES.map((t) => <option key={t.value} value={t.value}>{t.label}</option>)}
              </select>
            </div>
            <button type="submit" disabled={!file || loading} className="btn-primary w-full justify-center">
              {loading ? 'Processing…' : 'Upload & Validate'}
            </button>
          </form>

          {result && <div className="mt-5"><ValidationReport upload={result} /></div>}
        </div>

        <div className="card">
          <div className="px-5 py-4 border-b border-gray-100">
            <h2 className="font-semibold text-gray-800">Upload History</h2>
          </div>
          {history.length === 0
            ? <p className="p-5 text-sm text-gray-400">No uploads yet.</p>
            : (
              <table className="w-full text-sm">
                <thead className="bg-gray-50 text-xs text-gray-500 uppercase">
                  <tr>
                    {['File', 'Type', 'Rows', 'Status', 'Date', ''].map((h) => (
                      <th key={h} className="px-4 py-3 text-left">{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {history.map((u) => (
                    <tr key={u.id} className="hover:bg-gray-50">
                      <td className="px-4 py-3 font-medium truncate max-w-[200px]">{u.filename}</td>
                      <td className="px-4 py-3 capitalize">{u.dataset_type}</td>
                      <td className="px-4 py-3">{u.row_count}</td>
                      <td className="px-4 py-3">
                        <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${STATUS_BADGE[u.status]}`}>{u.status}</span>
                      </td>
                      <td className="px-4 py-3 text-gray-500">{new Date(u.created_at).toLocaleDateString()}</td>
                      <td className="px-4 py-3">
                        <button onClick={() => remove(u.id)} className="text-gray-400 hover:text-red-500 transition-colors">
                          <Trash2 size={14} />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
        </div>
      </div>
    </div>
  )
}
