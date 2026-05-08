import { CheckCircle, XCircle, AlertTriangle } from 'lucide-react'

export default function ValidationReport({ upload }) {
  if (!upload) return null

  const log = upload.error_log ? JSON.parse(upload.error_log) : { errors: [], warnings: [] }
  const isValid = upload.status === 'valid'

  return (
    <div className={`rounded-xl border p-5 ${isValid ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'}`}>
      <div className="flex items-center gap-2 mb-3">
        {isValid
          ? <CheckCircle size={18} className="text-green-600" />
          : <XCircle size={18} className="text-red-600" />}
        <span className={`font-semibold ${isValid ? 'text-green-700' : 'text-red-700'}`}>
          {isValid ? `Valid — ${upload.row_count} rows imported` : 'Validation failed'}
        </span>
      </div>

      {log.errors?.length > 0 && (
        <ul className="space-y-1 mb-2">
          {log.errors.map((e, i) => (
            <li key={i} className="flex items-start gap-2 text-sm text-red-700">
              <XCircle size={14} className="mt-0.5 shrink-0" /> {e}
            </li>
          ))}
        </ul>
      )}

      {log.warnings?.length > 0 && (
        <ul className="space-y-1">
          {log.warnings.map((w, i) => (
            <li key={i} className="flex items-start gap-2 text-sm text-yellow-700">
              <AlertTriangle size={14} className="mt-0.5 shrink-0" /> {w}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
