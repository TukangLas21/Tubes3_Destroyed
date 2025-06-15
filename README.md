# Tubes3_Destroyed
### Pemanfaatan Pattern Matching untuk Membangun Sistem ATS (Applicant Tracking System) Berbasis CV Digital

## Penjelasan Singkat
Projek ini mengimplementasikan sistem yang dapat melakukan deteksi informasi pelamar berbasis dokumen CV digital, terintegrasi dengan basis data. Metode yang akan digunakan untuk melakukan deteksi pola string dalam CV adalah algoritma Boyer-Moore, Knuth-Morris-Pratt, Aho-Corasick, dan Fuzzy String Matching.

#### Algoritma Boyer-Moore (BM)
Algoritma (BM) adalah algoritma pattern matching yang menggunakan dua teknik, yaitu Looking-Glass Technique dan Character-Jump Technique.  Teknis Looking-Glass artinya mencari pola dalam teks dengan bergerak dari kanan ke kiri dalam pola, sedangkan teknik Character-Jump digunakan ketika terjadi ketidakcocokan atau mismatch antara karakter dalam teks dengan karakter pola.

#### Algoritma Knuth-Morris-Pratt (KMP)
Algoritma KMP digunakan untuk mencari pattern dalam teks dengan menggunakan tabel fungsi Longest Proper Suffix (LPS). Algoritma ini memanfaatkan informasi dari kecocokan karakter sebelumnya untuk menghindari pemeriksaan ulang karakter yang tidak perlu seperti metode algoritma brute force. 



## Kebutuhan
Pastikan Anda memiliki [Python](https://www.python.org/downloads/) minimal versi 3.12.8

## Cara Menjalankan Program
Pertama, lakukan clone repository ini.
```shell
git clone https://github.com/TukangLas21/Tubes3_Destroyed.git
cd Tubes3_Destroyed
```

Kemudian, buat lingkungan virtual Anda sendiri di dalam repository ini dan aktifkan.
```shell
python -m venv env
env\Scripts\activate      # Untuk pengguna Windows
```

Terakhir, install semua dependensi yang diperlukan dari file `requirements.txt` di lingkungan virtual Anda. Pastikan lingkungan virtual Anda sudah aktif.
```shell
pip install -r requirements.txt
```

Untuk menjalankan program, masuk ke direktori src/gui dan jalankan program utama dengan Flet.
```shell
cd src/gui
flet run main.py
```
Tampilan GUI pertama kali akan berupa halaman login yang berisi host, username, password, database, dan encryption key. Pastikan Anda memiliki data username dan password serta setup database.

Untuk encryption key, gunakan key berikut
```shell
DESTROYEDBYstima
```

### Penting!
Pastikan lingkungan virtual Anda aktif saat mengembangkan proyek ini. Tampilan pada terminal akan seperti berikut:
```shell
(env) C:\directory\to\Tubes3_Destroyed
```

## Author
### **Kelompok 11 - Destroyed**
|   NIM    |                  Nama                  |
| :------: | :------------------------------------: |
| 13523014 |         Nicholas Andhika Lucas         |
| 13523112 |            Aria Judhistira             |
| 15223090 |         Ignacio Kevin Alberiann        |