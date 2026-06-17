# Kutuphane Yonetim Sistemi

Bu proje, IYU 228 Is Yeri Uygulamasi dersi kapsaminda gelistirilmis basit bir kutuphane yonetim sistemidir. Uygulama Python ile yazilmistir ve veriler SQLite veritabaninda tutulmaktadir.

## Projenin Amaci

Projenin amaci; kitap, uye ve odunc alma islemlerinin bir SQL veritabani uzerinden yonetilmesini saglayan bir uygulama gelistirmektir. Sistem komut satiri arayuzu ile calisir ve temel CRUD islemlerini destekler.

## Kullanilan Teknolojiler

- Python 3
- SQLite
- SQL
- GitHub
- unittest

## Ozellikler

- Kitap ekleme, listeleme, guncelleme ve silme
- Uye ekleme, listeleme, guncelleme ve silme
- Kitap odunc verme
- Kitap iade alma
- Aktif ve tum odunc kayitlarini listeleme
- SQL tablo olusturma betikleri
- Ornek veri ekleme betikleri
- Birim testleri

## Proje Yapisi

```text
kutuphane-yonetim-sistemi/
  app.py
  README.md
  requirements.txt
  sql/
    schema.sql
    seed.sql
  src/
    __init__.py
    database.py
    library.py
  tests/
    test_library.py

## Veritabani Tasarimi

Projede uc temel tablo bulunur:

- `books`: Kitap bilgilerini tutar.
- `members`: Kutuphane uyelerini tutar.
- `loans`: Kitap odunc alma ve iade kayitlarini tutar.

`loans` tablosu, `books` ve `members` tablolarina foreign key ile baglidir.
Bu sayede hangi kitabin hangi uye tarafindan odunc alindigi takip edilir.

## Kurulum

1. Projeyi bilgisayara indirin veya GitHub deposunu klonlayin.
2. Proje klasorune girin.
3. Python 3 kurulu oldugundan emin olun.

Ek paket kurulumu gerekmez. Proje yalnizca Python standart kutuphanesini
kullanir.

## Calistirma

```bash
python app.py
```

Program ilk calistiginda `library.sqlite` adinda SQLite veritabanini olusturur.
Tablolar `sql/schema.sql` dosyasindan, ornek veriler ise `sql/seed.sql`
dosyasindan yuklenir.

## Testleri Calistirma

```bash
python -m unittest discover -s tests
```

## Ornek Kullanim

Program acildiginda asagidaki menu gorunur:

```text
1. Kitaplari listele
2. Kitap ekle
3. Kitap guncelle
4. Kitap sil
5. Uyeleri listele
6. Uye ekle
7. Uye guncelle
8. Uye sil
9. Kitap odunc ver
10. Kitap iade al
11. Tum odunc kayitlarini listele
12. Aktif odunc kayitlarini listele
0. Cikis
```

## GitHub Teslim Notu

Bu proje GitHub'a public repository olarak yuklenmelidir. Commit mesajlari
anlamli tutulmalidir. Ornek commit sirasi:

```text
Initial project structure
Add database schema and seed data
Implement library CRUD operations
Add CLI menu
Add unit tests and documentation
```

