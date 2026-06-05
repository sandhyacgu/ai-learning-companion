import type { Page } from '../types'

interface NavbarProps {
  activePage: Page
  onPageChange: (page: Page) => void
}

const navItems: { id: Page; label: string; emoji: string }[] = [
  { id: 'explain', label: 'Explain', emoji: '💡' },
  { id: 'summary', label: 'Summary', emoji: '📝' },
  { id: 'quiz', label: 'Quiz', emoji: '🧪' },
  { id: 'notes', label: 'Notes', emoji: '📚' },
  { id: 'dashboard', label: 'Stats', emoji: '📊' },
]

function Navbar({ activePage, onPageChange }: NavbarProps) {
  return (
    <div className="flex border-b border-gray-700">
      {navItems.map((item) => (
        <button
          key={item.id}
          onClick={() => onPageChange(item.id)}
          className={`flex-1 py-1.5 text-[10px] font-medium transition-colors
            ${activePage === item.id
              ? 'text-blue-400 border-b-2 border-blue-400'
              : 'text-gray-400 hover:text-white'
            }`}
        >
          <div>{item.emoji}</div>
          <div>{item.label}</div>
        </button>
      ))}
    </div>
  )
}

export default Navbar