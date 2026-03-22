import { render, screen, waitFor } from '@testing-library/react'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import App from './App'

beforeEach(() => {
  vi.resetAllMocks()
})

describe('App', () => {
  it('renders the heading', () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => [],
    } as Response)

    render(<App />)
    expect(screen.getByRole('heading', { name: /learn to prompt/i })).toBeInTheDocument()
  })

  it('shows loading state initially', () => {
    global.fetch = vi.fn().mockReturnValue(new Promise(() => {}))

    render(<App />)
    expect(screen.getByText(/loading/i)).toBeInTheDocument()
  })

  it('shows empty message when no prompts', async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => [],
    } as Response)

    render(<App />)
    await waitFor(() => expect(screen.getByText(/no prompts yet/i)).toBeInTheDocument())
  })

  it('renders fetched prompts', async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => [
        { id: 1, title: 'My Prompt', content: 'Do something cool.', created_at: '2024-01-01T00:00:00' },
      ],
    } as Response)

    render(<App />)
    await waitFor(() => expect(screen.getByText('My Prompt')).toBeInTheDocument())
    expect(screen.getByText('Do something cool.')).toBeInTheDocument()
  })

  it('shows error when fetch fails', async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: false,
    } as Response)

    render(<App />)
    await waitFor(() => expect(screen.getByRole('alert')).toBeInTheDocument())
  })
})
