from __future__ import annotations

import sqlite3
from datetime import date, timedelta
from typing import Iterable


def rows_to_dicts(rows: Iterable[sqlite3.Row]) -> list[dict]:
    return [dict(row) for row in rows]


class LibraryService:
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def add_book(
        self,
        title: str,
        author: str,
        isbn: str,
        publication_year: int,
        category: str,
        total_copies: int,
    ) -> int:
        cursor = self.connection.execute(
            """
            INSERT INTO books
            (title, author, isbn, publication_year, category, total_copies, available_copies)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (title, author, isbn, publication_year, category, total_copies, total_copies),
        )
        self.connection.commit()
        return int(cursor.lastrowid)

    def list_books(self) -> list[dict]:
        rows = self.connection.execute(
            """
            SELECT id, title, author, isbn, publication_year, category,
                   total_copies, available_copies
            FROM books
            ORDER BY title
            """
        ).fetchall()
        return rows_to_dicts(rows)

    def update_book(
        self,
        book_id: int,
        title: str,
        author: str,
        isbn: str,
        publication_year: int,
        category: str,
        total_copies: int,
    ) -> bool:
        current = self.connection.execute(
            "SELECT total_copies, available_copies FROM books WHERE id = ?",
            (book_id,),
        ).fetchone()

        if current is None:
            return False

        borrowed_count = current["total_copies"] - current["available_copies"]

        if total_copies < borrowed_count:
            raise ValueError("Toplam kopya sayisi oduncteki kitap sayisindan az olamaz.")

        available_copies = total_copies - borrowed_count

        cursor = self.connection.execute(
            """
            UPDATE books
            SET title = ?, author = ?, isbn = ?, publication_year = ?,
                category = ?, total_copies = ?, available_copies = ?
            WHERE id = ?
            """,
            (
                title,
                author,
                isbn,
                publication_year,
                category,
                total_copies,
                available_copies,
                book_id,
            ),
        )
        self.connection.commit()
        return cursor.rowcount > 0

    def delete_book(self, book_id: int) -> bool:
        cursor = self.connection.execute(
            "DELETE FROM books WHERE id = ?",
            (book_id,),
        )
        self.connection.commit()
        return cursor.rowcount > 0

    def add_member(self, full_name: str, email: str, phone: str) -> int:
        cursor = self.connection.execute(
            """
            INSERT INTO members (full_name, email, phone)
            VALUES (?, ?, ?)
            """,
            (full_name, email, phone),
        )
        self.connection.commit()
        return int(cursor.lastrowid)

    def list_members(self) -> list[dict]:
        rows = self.connection.execute(
            """
            SELECT id, full_name, email, phone, joined_at, is_active
            FROM members
            ORDER BY full_name
            """
        ).fetchall()
        return rows_to_dicts(rows)

    def update_member(
        self,
        member_id: int,
        full_name: str,
        email: str,
        phone: str,
    ) -> bool:
        cursor = self.connection.execute(
            """
            UPDATE members
            SET full_name = ?, email = ?, phone = ?
            WHERE id = ?
            """,
            (full_name, email, phone, member_id),
        )
        self.connection.commit()
        return cursor.rowcount > 0

    def delete_member(self, member_id: int) -> bool:
        cursor = self.connection.execute(
            "DELETE FROM members WHERE id = ?",
            (member_id,),
        )
        self.connection.commit()
        return cursor.rowcount > 0

    def borrow_book(
        self,
        book_id: int,
        member_id: int,
        days: int = 14,
    ) -> int:
        book = self.connection.execute(
            "SELECT available_copies FROM books WHERE id = ?",
            (book_id,),
        ).fetchone()

        if book is None:
            raise ValueError("Kitap bulunamadi.")

        if book["available_copies"] <= 0:
            raise ValueError("Bu kitabin uygun kopyasi yok.")

        member = self.connection.execute(
            "SELECT is_active FROM members WHERE id = ?",
            (member_id,),
        ).fetchone()

        if member is None:
            raise ValueError("Uye bulunamadi.")

        if member["is_active"] != 1:
            raise ValueError("Pasif uye odunc kitap alamaz.")

        due_date = date.today() + timedelta(days=days)

        cursor = self.connection.execute(
            """
            INSERT INTO loans (book_id, member_id, due_date)
            VALUES (?, ?, ?)
            """,
            (book_id, member_id, due_date.isoformat()),
        )

        self.connection.execute(
            "UPDATE books SET available_copies = available_copies - 1 WHERE id = ?",
            (book_id,),
        )

        self.connection.commit()
        return int(cursor.lastrowid)

    def return_book(self, loan_id: int) -> bool:
        loan = self.connection.execute(
            "SELECT book_id, status FROM loans WHERE id = ?",
            (loan_id,),
        ).fetchone()

        if loan is None:
            return False

        if loan["status"] == "returned":
            raise ValueError("Bu odunc kaydi zaten iade edilmis.")

        self.connection.execute(
            """
            UPDATE loans
            SET return_date = CURRENT_DATE, status = 'returned'
            WHERE id = ?
            """,
            (loan_id,),
        )

        self.connection.execute(
            "UPDATE books SET available_copies = available_copies + 1 WHERE id = ?",
            (loan["book_id"],),
        )

        self.connection.commit()
        return True

    def list_loans(self, only_active: bool = False) -> list[dict]:
        sql = """
            SELECT loans.id, books.title AS book_title, members.full_name AS member_name,
                   loans.loan_date, loans.due_date, loans.return_date, loans.status
            FROM loans
            JOIN books ON books.id = loans.book_id
            JOIN members ON members.id = loans.member_id
        """

        params: tuple = ()

        if only_active:
            sql += " WHERE loans.status = ?"
            params = ("borrowed",)

        sql += " ORDER BY loans.id DESC"

        rows = self.connection.execute(sql, params).fetchall()
        return rows_to_dicts(rows)
