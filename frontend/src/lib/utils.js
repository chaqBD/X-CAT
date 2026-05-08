import { clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs) {
  return twMerge(clsx(inputs))
}

export function fmt(value, opts = {}) {
  const { type = 'currency', decimals = 0 } = opts
  if (value == null) return '—'
  if (type === 'currency') {
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: decimals }).format(value)
  }
  if (type === 'percent') {
    return `${Number(value).toFixed(decimals)}%`
  }
  return new Intl.NumberFormat('en-US', { maximumFractionDigits: decimals }).format(value)
}

export const COLORS = [
  '#3b5bdb', '#1c7ed6', '#0ca678', '#f59f00', '#e64980',
  '#7950f2', '#20c997', '#fd7e14', '#74c0fc', '#f783ac',
]
