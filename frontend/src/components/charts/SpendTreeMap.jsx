import { Treemap, ResponsiveContainer, Tooltip } from 'recharts'
import { COLORS, fmt } from '../../lib/utils'

const CustomContent = ({ x, y, width, height, name, value, depth, index }) => {
  if (width < 40 || height < 30) return null
  return (
    <g>
      <rect x={x} y={y} width={width} height={height} fill={COLORS[index % COLORS.length]} stroke="#fff" strokeWidth={2} rx={4} />
      {width > 60 && height > 40 && (
        <>
          <text x={x + 8} y={y + 18} fill="#fff" fontSize={11} fontWeight={600}>{name}</text>
          <text x={x + 8} y={y + 32} fill="rgba(255,255,255,0.8)" fontSize={10}>{fmt(value, { decimals: 0 })}</text>
        </>
      )}
    </g>
  )
}

export default function SpendTreeMap({ data = [], height = 280 }) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <Treemap data={data} dataKey="value" nameKey="name" content={<CustomContent />}>
        <Tooltip formatter={(v) => fmt(v, { decimals: 2 })} />
      </Treemap>
    </ResponsiveContainer>
  )
}
