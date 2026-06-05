import { useState } from 'react'

interface ExplainPageProps {
  selectedText: string
}

function ExplainPage({ selectedText }: ExplainPageProps) {
  const [result, setResult] = useState<string>('')
  const [loading, setLoading] = useState<boolean>(false)
  const [error, setError] = useState<string>('')

  const handleExplain = async () => {
    if (!selectedText) return
    setLoading(true)
    setError('')
    setResult('')

    try {
      const response = await fetch('http://localhost:8000/api/explain', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: selectedText })
      })
      const data = await response.json()
      setResult(data.result)
    } catch (err) {
      setError('Backend se connect nahi ho paya!')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-4 flex flex-col gap-4">
      <div className="bg-gray-800 rounded-lg p-3">
        <p className="text-xs text-gray-400 mb-1">Selected Text</p>
        <p className="text-sm text-white">
          {selectedText || 'Select any text on a webpage to get started...'}
        </p>
      </div>

      <button
        onClick={handleExplain}
        disabled={!selectedText || loading}
        className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 
          text-white font-medium py-2 px-4 rounded-lg transition-colors">
        {loading ? '⏳ Explaining...' : '💡 Explain This'}
      </button>

      {error && (
        <p className="text-red-400 text-xs">{error}</p>
      )}

      <div className="bg-gray-800 rounded-lg p-3 min-h-[200px]">
        <p className="text-xs text-gray-400 mb-2">Explanation</p>
        <p className="text-sm text-white whitespace-pre-wrap">
          {result || 'Explanation will appear here...'}
        </p>
      </div>
    </div>
  )
}

export default ExplainPage