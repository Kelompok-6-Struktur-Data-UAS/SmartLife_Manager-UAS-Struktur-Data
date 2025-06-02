
# SmartLife Manager

**SmartLife Manager** adalah aplikasi web inovatif yang dirancang sebagai asisten pribadi digital Anda. Aplikasi ini bertujuan untuk membantu pengguna dalam mengelola berbagai aspek penting kehidupan sehari-hari secara lebih terstruktur, efisien, dan cerdas, dengan penekanan pada aspek edukasi penerapan struktur data.

## Fitur Utama
Saat ini, SmartLife Manager memiliki fitur-fitur berikut (dan akan terus dikembangkan):
* **Autentikasi Pengguna:** Registrasi akun baru dan sistem login yang aman.
* **Dashboard Pengguna:** Tampilan ringkasan aktivitas dan akses cepat ke berbagai modul.
* **Manajemen Tugas (Antrean):** Menambah, melihat, dan memproses tugas berdasarkan urutan masuk (konsep Queue).
* **Penjadwalan Kegiatan:** Mengelola acara dan janji temu, tersimpan di database dan ditampilkan secara terurut.
* **Pencatatan:** Membuat, melihat, mengedit, dan menghapus catatan pribadi.
* **Tujuan & Prioritas:** Menetapkan tujuan dan melacak progresnya (dengan potensi sub-tugas).
* **Relasi Sosial (Kontak):** Mengelola daftar kontak pribadi.
* **Profil Pengguna:** Melihat dan memperbarui informasi akun.
* **Halaman Edukasi:** Penjelasan mengenai aplikasi dan konsep struktur data yang digunakan.
* **Panel Admin:** Akses untuk administrator mengelola data aplikasi.

## Teknologi yang Digunakan
* **Backend:** Python, Django Framework
* **Frontend:** HTML, CSS, JavaScript (dengan Bootstrap 5 untuk styling dasar)
* **Database:** SQLite (default Django untuk pengembangan)
* **Struktur Data yang Diterapkan/Dijelaskan:** List/Array, Antrean (Queue), Tumpukan (Stack), Heap (Priority Queue), Pohon (Tree), Graf (Graph), Tabel Hash (Dictionary).

## Prasyarat
Sebelum Anda memulai, pastikan Anda memiliki:
* Python (versi 3.8 atau lebih tinggi direkomendasikan)
* pip (Python package installer)
* Git (untuk cloning repositori)

## Instalasi dan Setup Virtual Environment (venv)

Untuk menjalankan aplikasi ini secara lokal, ikuti langkah-langkah berikut:

1.  **Clone Repositori (jika proyek Anda di GitHub):**
    ```bash
    git clone [https://github.com/EskelandLab/ANDA](https://github.com/EskelandLab/ANDA)
    cd nama-folder-repositori
    ```
    Jika Anda bekerja lokal dan sudah memiliki folder proyek (misalnya, `SmartLife_Manager_Django`), navigasikan ke direktori tersebut.

2.  **Buat Virtual Environment:**
    Sangat direkomendasikan untuk menggunakan virtual environment agar dependensi proyek terisolasi.

    * Di dalam direktori root proyek Anda (folder yang berisi `manage.py`), jalankan:
        ```bash
        python -m venv venv
        ```
        Ini akan membuat folder `venv` di dalam proyek Anda.

3.  **Aktifkan Virtual Environment:**
    * **Untuk Windows (PowerShell):**
        ```powershell
        .\venv\Scripts\Activate.ps1
        ```
        Jika ada masalah eksekusi skrip, Anda mungkin perlu mengatur Execution Policy: `Set-ExecutionPolicy Unrestricted -Scope Process` (jalankan PowerShell sebagai Administrator).
    * **Untuk Windows (Command Prompt):**
        ```bash
        venv\Scripts\activate.bat
        ```
    * **Untuk macOS dan Linux:**
        ```bash
        source venv/bin/activate
        ```
    Setelah berhasil, Anda akan melihat `(venv)` di awal prompt terminal Anda.

4.  **Install Dependensi:**
    Jika Anda memiliki file `requirements.txt` (yang berisi daftar pustaka Python yang dibutuhkan), jalankan:
    ```bash
    pip install -r requirements.txt
    ```
    Jika Anda belum memiliki `requirements.txt`, Anda perlu menginstal Django secara manual di dalam venv:
    ```bash
    pip install Django
    ```
    (Jika ada pustaka lain yang Anda gunakan, instal juga di sini).

## Menjalankan Aplikasi

Setelah instalasi selesai dan virtual environment aktif:

1.  **Lakukan Migrasi Database:**
    Perintah ini akan membuat skema database berdasarkan model yang telah Anda definisikan.
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
    *Catatan: Jika Anda baru memulai dan belum membuat model untuk semua aplikasi yang terdaftar di `INSTALLED_APPS`, jalankan `python manage.py makemigrations nama_app_spesifik` untuk setiap aplikasi yang modelnya sudah siap.*

2.  **Buat Superuser (Admin Utama):**
    Ini diperlukan untuk mengakses panel admin Django dan mengelola data awal.
    ```bash
    python manage.py createsuperuser
    ```
    Ikuti prompt untuk membuat username, email (opsional), dan password.

3.  **Jalankan Server Pengembangan:**
    ```bash
    python manage.py runserver
    ```
    Secara default, server akan berjalan di `http://127.0.0.1:8000/`.

4.  **Akses Aplikasi:**
    Buka web browser Anda dan navigasikan ke `http://127.0.0.1:8000/`. Anda akan diarahkan ke halaman login.
aplikasi
## Struktur Pembuat 

| Nama | NIM | Bagian |
| ------------- | ------------- | ------------- |
| RIZMA INDRA PRAMUDYA  | 24111814117  | Full-Stack Developor |
| ⁠Naufal yudantara saputra | 24111814023  | help Lend a Device |
| Bagus Adibrata | 24111814090 | Frontend |
| Dedi Firmansyah | 24111814021 | Document |
| Given Dimas Ara Dea | 24111814101 |

