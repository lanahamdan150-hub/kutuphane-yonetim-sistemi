from __future__ import annotations

import sqlite3

from src.database import initialize_database
from src.library import LibraryService


def ask_int(message: str) -> int:
    while True:
        value = input(message).strip()
        try:
            return int(value)
        except ValueError:
            print("Lutfen sayisal bir deger giriniz.")


def print_table(rows: list[dict]) -> None:
    if not rows:
        print("Kayit bulunamadi.")
        return

    headers = list(rows[0].keys())
    widths = {
        header: max(len(str(header)), *(len(str(row[header])) for row in rows))
        for header in headers
    }

    print(" | ".join(header.ljust(widths[header]) for header in headers))
    print("-+-".join("-" * widths[header] for header in headers))

    for row in rows:
        print(" | ".join(str(row[header]).ljust(widths[header]) for header in headers))


def add_book(service: LibraryService) -> None:
    title = input("Kitap adi: ").strip()
    author = input("Yazar: ").strip()
    isbn = input("ISBN: ").strip()
    publication_year = ask_int("Yayin yili: ")
    category = input("Kategori: ").strip()
    total_copies = ask_int("Toplam kopya: ")

    book_id = service.add_book(
        title,
        author,
        isbn,
        publication_year,
        category,
        total_copies,
    )

    print(f"Kitap eklendi. ID: {book_id}")


def update_book(service: LibraryService) -> None:
    book_id = ask_int("Guncellenecek kitap ID: ")
    title = input("Yeni kitap adi: ").strip()
    author = input("Yeni yazar: ").strip()
    isbn = input("Yeni ISBN: ").strip()
    publication_year = ask_int("Yeni yayin yili: ")
    category = input("Yeni kategori: ").strip()
    total_copies = ask_int("Yeni toplam kopya: ")

    if service.update_book(
        book_id,
        title,
        author,
        isbn,
        publication_year,
        category,
        total_copies,
    ):
        print("Kitap guncellendi.")
    else:
        print("Kitap bulunamadi.")


def add_member(service: LibraryService) -> None:
    full_name = input("Uye adi soyadi: ").strip()
    email = input("E-posta: ").strip()
    phone = input("Telefon: ").strip()

    member_id = service.add_member(full_name, email, phone)

    print(f"Uye eklendi. ID: {member_id}")


def update_member(service: LibraryService) -> None:
    member_id = ask_int("Guncellenecek uye ID: ")
    full_name = input("Yeni ad soyad: ").strip()
    email = input("Yeni e-posta: ").strip()
    phone = input("Yeni telefon: ").strip()

    if service.update_member(member_id, full_name, email, phone):
        print("Uye guncellendi.")
    else:
        print("Uye bulunamadi.")


def borrow_book(service: LibraryService) -> None:
    book_id = ask_int("Kitap ID: ")
    member_id = ask_int("Uye ID: ")
    days = ask_int("Kac gun odunc verilecek?: ")

    loan_id = service.borrow_book(book_id, member_id, days)

    print(f"Odunc kaydi olusturuldu. ID: {loan_id}")


def return_book(service: LibraryService) -> None:
    loan_id = ask_int("Iade edilecek odunc kaydi ID: ")

    if service.return_book(loan_id):
        print("Kitap iade edildi.")
    else:
        print("Odunc kaydi bulunamadi.")


def menu() -> None:
    connection = initialize_database()
    service = LibraryService(connection)

    actions = {
        "1": lambda: print_table(service.list_books()),
        "2": lambda: add_book(service),
        "3": lambda: update_book(service),
        "4": lambda: print(
            "Silindi."
            if service.delete_book(ask_int("Silinecek kitap ID: "))
            else "Kitap bulunamadi."
        ),
        "5": lambda: print_table(service.list_members()),
        "6": lambda: add_member(service),
        "7": lambda: update_member(service),
        "8": lambda: print(
            "Silindi."
            if service.delete_member(ask_int("Silinecek uye ID: "))
            else "Uye bulunamadi."
        ),
        "9": lambda: borrow_book(service),
        "10": lambda: return_book(service),
        "11": lambda: print_table(service.list_loans()),
        "12": lambda: print_table(service.list_loans(only_active=True)),
    }

    while True:
        print("\n=== Kutuphane Yonetim Sistemi ===")
        print("1. Kitaplari listele")
        print("2. Kitap ekle")
        print("3. Kitap guncelle")
        print("4. Kitap sil")
        print("5. Uyeleri listele")
        print("6. Uye ekle")
        print("7. Uye guncelle")
        print("8. Uye sil")
        print("9. Kitap odunc ver")
        print("10. Kitap iade al")
        print("11. Tum odunc kayitlarini listele")
        print("12. Aktif odunc kayitlarini listele")
        print("0. Cikis")

        choice = input("Seciminiz: ").strip()

        if choice == "0":
            connection.close()
            print("Program kapatildi.")
            break

        action = actions.get(choice)

        if action is None:
            print("Gecersiz secim.")
            continue

        try:
            action()
        except (sqlite3.IntegrityError, ValueError) as error:
            print(f"Hata: {error}")


if __name__ == "__main__":
    menu()