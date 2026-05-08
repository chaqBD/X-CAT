import { useDropzone } from 'react-dropzone'
import { Upload, FileText } from 'lucide-react'
import { cn } from '../../lib/utils'

export default function DropZone({ onDrop, file }) {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: (files) => onDrop(files[0]),
    accept: { 'text/csv': ['.csv'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'] },
    maxFiles: 1,
  })

  return (
    <div
      {...getRootProps()}
      className={cn(
        'border-2 border-dashed rounded-xl p-10 text-center cursor-pointer transition-colors',
        isDragActive ? 'border-brand-500 bg-brand-50' : 'border-gray-300 hover:border-brand-400 hover:bg-gray-50'
      )}
    >
      <input {...getInputProps()} />
      {file ? (
        <div className="flex flex-col items-center gap-2 text-brand-600">
          <FileText size={40} />
          <p className="font-medium">{file.name}</p>
          <p className="text-sm text-gray-500">{(file.size / 1024).toFixed(1)} KB — click to change</p>
        </div>
      ) : (
        <div className="flex flex-col items-center gap-2 text-gray-400">
          <Upload size={40} />
          <p className="font-medium text-gray-600">Drop your CSV or Excel file here</p>
          <p className="text-sm">or click to browse</p>
        </div>
      )}
    </div>
  )
}
