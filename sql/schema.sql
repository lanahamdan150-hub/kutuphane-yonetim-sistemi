PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    isbn TEXT NOT NULL UNIQUE,
    publication_year INTEGER NOT NULL,
    category TEXT NOT NULL,
    total_copies INTEGER NOT NULL CHECK (total_copies >= 0),
    available_copies INTEGER NOT NULL CHECK (available_copies >= 0),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (available_copies <= total_copies)
);

CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT NOT NULL,
    joined_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1))
);

CREATE TABLE IF NOT EXISTS loans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    loan_date TEXT NOT NULL DEFAULT CURRENT_DATE,
    due_date TEXT NOT NULL,
    return_date TEXT,
    status TEXT NOT NULL DEFAULT 'borrowed' CHECK (status IN ('borrowed', 'returned')),
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE RESTRICT,
    FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_books_title ON books(title);
CREATE INDEX IF NOT EXISTS idx_members_name ON members(full_name);
CREATE INDEX IF NOT EXISTS idx_loans_status ON loans(status);
