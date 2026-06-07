import { useState, useEffect } from 'react'
import type { Page } from './types'
import Navbar from './components/Navbar'
import ExplainPage from './pages/ExplainPage'
import SummaryPage from './pages/SummaryPage'
import QuizPage from './pages/QuizPage'
import NotesPage from './pages/NotesPage'
import DashboardPage from './pages/DashboardPage'

function App() {
  const [activePage, setActivePage] = useState<Page>('explain')
  const [selectedText, setSelectedText] = useState<string>('')

  useEffect(() => {
    setTimeout(() => {
      try {
        chrome.runtime.sendMessage(
          { type: 'GET_SELECTED_TEXT' },
          (res) => {
            if (chrome.runtime.lastError) return
            if (res?.text) {
              setSelectedText(res.text)
            }
          }
        )
      } catch (err) {
        console.log('Error:', err)
      }
    }, 100)
  }, [])

  const renderPage = () => {
    switch (activePage) {
      case 'explain': return <ExplainPage selectedText={selectedText} />
      case 'summary': return <SummaryPage selectedText={selectedText} />
      case 'quiz': return <QuizPage selectedText={selectedText} />
      case 'notes': return <NotesPage selectedText={selectedText} />
      case 'dashboard': return <DashboardPage />
    }
  }

  return (
    <div className="w-[340px] h-[500px] bg-gray-900 text-white flex flex-col">
      <div className="px-4 py-3 border-b border-gray-700">
        <h1 className="text-sm font-bold text-blue-400">
          AI Learning Companion 🧠
        </h1>
        {selectedText && (
          <p className="text-xs text-gray-400 mt-1 truncate">
            📌 "{selectedText.substring(0, 50)}..."
          </p>
        )}
      </div>
      <Navbar activePage={activePage} onPageChange={setActivePage} />
      <div className="flex-1 overflow-y-auto">
        {renderPage()}
      </div>
    </div>
  )
}

export default App