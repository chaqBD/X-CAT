import { NavLink } from 'react-router-dom'
import {
  LayoutDashboard, Upload, TrendingUp, Tag, Users,
  Package, DollarSign, Map, LogOut
} from 'lucide-react'
import useAuthStore from '../../store/authStore'
import { cn } from '../../lib/utils'

const NAV = [
  { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/upload', icon: Upload, label: 'Upload Data', roles: ['admin', 'analyst'] },
  { to: '/spend', icon: TrendingUp, label: 'Spend Analysis' },
  { to: '/category', icon: Tag, label: 'Category Analysis' },
  { to: '/supplier', icon: Users, label: 'Supplier Analysis' },
  { to: '/inventory', icon: Package, label: 'Inventory' },
  { to: '/budget', icon: DollarSign, label: 'Budget & Variance' },
  { to: '/geographic', icon: Map, label: 'Geographic' },
]

export default function Sidebar() {
  const { user, logout } = useAuthStore()

  return (
    <aside className="w-60 shrink-0 bg-brand-900 text-white flex flex-col h-screen sticky top-0">
      <div className="px-6 py-5 border-b border-brand-700">
        <span className="text-xl font-bold tracking-wide">X-CAT</span>
        <p className="text-xs text-brand-100 mt-0.5">Supply Chain Analytics</p>
      </div>

      <nav className="flex-1 py-4 overflow-y-auto">
        {NAV.filter(item => !item.roles || item.roles.includes(user?.role)).map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            className={({ isActive }) =>
              cn('flex items-center gap-3 px-5 py-2.5 text-sm transition-colors',
                isActive ? 'bg-brand-700 text-white font-medium' : 'text-brand-100 hover:bg-brand-800 hover:text-white')
            }
          >
            <Icon size={16} />
            {label}
          </NavLink>
        ))}
      </nav>

      <div className="px-5 py-4 border-t border-brand-700">
        <p className="text-xs text-brand-200 truncate mb-2">{user?.email}</p>
        <button
          onClick={logout}
          className="flex items-center gap-2 text-xs text-brand-200 hover:text-white transition-colors"
        >
          <LogOut size={14} /> Sign out
        </button>
      </div>
    </aside>
  )
}
