INSERT OR IGNORE INTO books
(id, title, author, isbn, publication_year, category, total_copies, available_copies)
VALUES
(1, 'Tutunamayanlar', 'Oguz Atay', '9789754700114', 1972, 'Roman', 4, 4),
(2, 'Saatleri Ayarlama Enstitusu', 'Ahmet Hamdi Tanpinar', '9789759955908', 1961, 'Roman', 3, 3),
(3, 'Kurk Mantolu Madonna', 'Sabahattin Ali', '9789753638029', 1943, 'Roman', 5, 5),
(4, 'Python ile Programlama', 'Ali Yilmaz', '9786050000001', 2023, 'Bilisim', 2, 2),
(5, 'Veritabani Sistemleri', 'Ayse Demir', '9786050000002', 2022, 'Bilisim', 2, 2);

INSERT OR IGNORE INTO members
(id, full_name, email, phone)
VALUES
(1, 'Zeynep Kaya', 'zeynep.kaya@example.com', '05550000001'),
(2, 'Mehmet Celik', 'mehmet.celik@example.com', '05550000002'),
(3, 'Elif Arslan', 'elif.arslan@example.com', '05550000003');
