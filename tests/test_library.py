import sqlite3
import unittest

from src.database import run_script, SCHEMA_PATH, SEED_PATH
from src.library import LibraryService


class LibraryServiceTest(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON;")

        run_script(self.connection, SCHEMA_PATH)
        run_script(self.connection, SEED_PATH)

        self.service = LibraryService(self.connection)

    def tearDown(self):
        self.connection.close()

    def test_add_and_list_book(self):
        book_id = self.service.add_book(
            "Algoritmalar",
            "Can Kaya",
            "9786050000099",
            2024,
            "Bilisim",
            3,
        )

        books = self.service.list_books()
        created = [book for book in books if book["id"] == book_id][0]

        self.assertEqual(created["title"], "Algoritmalar")
        self.assertEqual(created["available_copies"], 3)

    def test_update_member(self):
        member_id = self.service.add_member(
            "Ali Veli",
            "ali.veli@example.com",
            "05551112233",
        )

        updated = self.service.update_member(
            member_id,
            "Ali Veli Yilmaz",
            "ali.yilmaz@example.com",
            "05554445566",
        )

        member = [item for item in self.service.list_members() if item["id"] == member_id][0]

        self.assertTrue(updated)
        self.assertEqual(member["full_name"], "Ali Veli Yilmaz")

    def test_borrow_and_return_book(self):
        loan_id = self.service.borrow_book(book_id=1, member_id=1, days=7)

        active_loans = self.service.list_loans(only_active=True)
        book = [item for item in self.service.list_books() if item["id"] == 1][0]

        self.assertEqual(active_loans[0]["id"], loan_id)
        self.assertEqual(book["available_copies"], 3)

        returned = self.service.return_book(loan_id)
        book_after_return = [item for item in self.service.list_books() if item["id"] == 1][0]

        self.assertTrue(returned)
        self.assertEqual(book_after_return["available_copies"], 4)

    def test_borrow_book_without_available_copy_raises_error(self):
        book_id = self.service.add_book(
            "Tek Kopya Kitap",
            "Test Yazar",
            "9786050000100",
            2021,
            "Test",
            1,
        )

        self.service.borrow_book(book_id=book_id, member_id=1)

        with self.assertRaises(ValueError):
            self.service.borrow_book(book_id=book_id, member_id=2)


if __name__ == "__main__":
    unittest.main()
