import React, { useEffect, useState, useMemo } from 'react'

const API_BASE = 'http://127.0.0.1:8000'

function useData() {
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [authors, setAuthors] = useState([])
  const [books, setBooks] = useState([])
  const [readers, setReaders] = useState([])
  const [relations, setRelations] = useState([])

  useEffect(() => {
    setLoading(true)
    setError(null)

    Promise.all([
      fetch(API_BASE + '/authors').then(r => r.json()),
      fetch(API_BASE + '/books').then(r => r.json()),
      fetch(API_BASE + '/readers').then(r => r.json()),
      fetch(API_BASE + '/book-readers').then(r => r.json()),
    ])
      .then(([a, b, r, rel]) => {
        setAuthors(a || [])
        setBooks(b || [])
        setReaders(r || [])
        setRelations(rel || [])
      })
      .catch(err => setError(err.message || String(err)))
      .finally(() => setLoading(false))
  }, [])

  return { loading, error, authors, books, readers, relations }
}

export default function App() {
  const { loading, error, authors, books, readers, relations } = useData()

  // assume single signed-in user = first reader in DB
  const currentUser = readers && readers.length ? readers[0] : null

  // book -> reader count map
  const bookReaderCounts = useMemo(() => {
    const map = new Map()
    relations.forEach(r => {
      map.set(r.book_id, (map.get(r.book_id) || 0) + 1)
    })
    return map
  }, [relations])

  // most popular books sorted by reader count desc
  const popularBooks = useMemo(() => {
    return [...books]
      .map(b => ({ ...b, readers: bookReaderCounts.get(b.id) || 0, author: authors.find(a => a.id === b.author_id) }))
      .sort((x, y) => y.readers - x.readers)
  }, [books, authors, bookReaderCounts])

  // most popular author (based on unique readers across their books)
  const mostPopularAuthor = useMemo(() => {
    if (!authors.length) return null
    let best = null
    authors.forEach(author => {
      // find all books for this author
      const authorBooks = books.filter(b => b.author_id === author.id)
      // collect unique reader ids across those books
      const readerSet = new Set()
      authorBooks.forEach(book => {
        relations.filter(rr => rr.book_id === book.id).forEach(rr => readerSet.add(rr.reader_id))
      })
      const count = readerSet.size
      if (!best || count > best.count) best = { author, count }
    })
    return best
  }, [authors, books, relations])

  // total number of books read by current user
  const totalBooksReadByUser = useMemo(() => {
    if (!currentUser) return 0
    return relations.filter(r => r.reader_id === currentUser.id).length
  }, [relations, currentUser])

  // user's top 3 authors by number of books they have read for each author
  const userTopAuthors = useMemo(() => {
    if (!currentUser) return []
    const counts = new Map()
    relations
      .filter(r => r.reader_id === currentUser.id)
      .forEach(rel => {
        const book = books.find(b => b.id === rel.book_id)
        if (!book) return
        counts.set(book.author_id, (counts.get(book.author_id) || 0) + 1)
      })
    const arr = [...counts.entries()].map(([author_id, cnt]) => ({ author: authors.find(a => a.id === author_id), count: cnt }))
    return arr.sort((a, b) => b.count - a.count).slice(0, 3)
  }, [relations, books, authors, currentUser])

  if (loading) return <div className="container"><h1>STAR Library</h1><p>Loading data…</p></div>
  if (error) return <div className="container"><h1>STAR Library</h1><p className="error">Error loading data: {error}</p></div>

  return (
    <div className="container">
      <header>
        <h1>STAR Library</h1>
        <div className="user">Signed in as: <strong>{currentUser ? currentUser.name : 'Guest'}</strong></div>
      </header>

      <div className="layout">
        <section className="panel books">
          <h2>Most Popular Books</h2>
          {popularBooks.length === 0 ? (
            <p>No books available</p>
          ) : (
            <ol className="book-list">
              {popularBooks.map(b => (
                <li key={b.id} className="book-item">
                  <div className="title">{b.title}</div>
                  <div className="meta">by {b.author ? b.author.name : 'Unknown'} — {b.readers} readers</div>
                </li>
              ))}
            </ol>
          )}
        </section>

        <aside className="panel dashboard">
          <h2>Dashboard</h2>

          <div className="stat">
            <div className="label">Most popular author</div>
            <div className="value">{mostPopularAuthor ? `${mostPopularAuthor.author.name} (${mostPopularAuthor.count} unique readers)` : '—'}</div>
          </div>

          <div className="stat">
            <div className="label">Books read (you)</div>
            <div className="value">{totalBooksReadByUser}</div>
          </div>

          <div className="stat">
            <div className="label">Your top 3 authors</div>
            <div className="value">
              {userTopAuthors.length === 0 ? <div>—</div> : (
                <ol>
                  {userTopAuthors.map(u => (
                    <li key={u.author.id}>{u.author.name} — {u.count} book{u.count !== 1 ? 's' : ''}</li>
                  ))}
                </ol>
              )}
            </div>
          </div>
        </aside>
      </div>
    </div>
  )
}
