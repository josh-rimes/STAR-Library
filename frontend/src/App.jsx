import React, { useEffect, useState } from 'react'

const API_BASE = 'http://127.0.0.1:8000'

export default function App() {
  const [status, setStatus] = useState('...')
  const [items, setItems] = useState([])
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')

  useEffect(() => {
    fetch(API_BASE + '/health')
      .then(r => r.json())
      .then(d => setStatus(d.status))
      .catch(() => setStatus('unreachable'))

    fetchItems()
  }, [])

  function fetchItems() {
    fetch(API_BASE + '/items')
      .then(r => r.json())
      .then(d => setItems(d))
      .catch(() => setItems([]))
  }

  function submit(e) {
    e.preventDefault()
    const payload = { name, description }
    fetch(API_BASE + '/items', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
      .then(r => r.json())
      .then(() => {
        setName('')
        setDescription('')
        fetchItems()
      })
  }

  return (
    <div className="container">
      <h1>STAR Library</h1>
      <p>Backend status: <strong>{status}</strong></p>

      <form onSubmit={submit} className="item-form">
        <input value={name} onChange={e => setName(e.target.value)} placeholder="Name" required />
        <input value={description} onChange={e => setDescription(e.target.value)} placeholder="Description" />
        <button type="submit">Create</button>
      </form>

      <ul className="items">
        {items.map(it => (
          <li key={it.id}>
            <strong>{it.name}</strong>
            <div className="desc">{it.description}</div>
          </li>
        ))}
      </ul>
    </div>
  )
}
