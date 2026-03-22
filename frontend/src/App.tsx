import { useEffect, useState } from 'react'
import './App.css'

interface Prompt {
  id: number
  title: string
  content: string
  created_at: string
}

function App() {
  const [prompts, setPrompts] = useState<Prompt[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetch('/api/prompts')
      .then((res) => {
        if (!res.ok) throw new Error('Failed to fetch prompts')
        return res.json() as Promise<Prompt[]>
      })
      .then((data) => {
        setPrompts(data)
        setLoading(false)
      })
      .catch((err: Error) => {
        setError(err.message)
        setLoading(false)
      })
  }, [])

  return (
    <main>
      <h1>Learn to Prompt</h1>
      <p>A guide for those learning to use AI in their everyday lives.</p>

      <section>
        <h2>Prompts</h2>
        {loading && <p>Loading...</p>}
        {error && <p role="alert">Error: {error}</p>}
        {!loading && !error && prompts.length === 0 && (
          <p>No prompts yet. Add one via the API!</p>
        )}
        <ul>
          {prompts.map((prompt) => (
            <li key={prompt.id}>
              <strong>{prompt.title}</strong>
              <p>{prompt.content}</p>
            </li>
          ))}
        </ul>
      </section>
    </main>
  )
}

export default App

