# Back-And — File Manager API

Backend REST API untuk manajemen file dan folder berbasis **FastAPI**, dirancang untuk berjalan di belakang reverse proxy **Nginx** dengan prefix `/thorix`.

---

## Teknologi

- **Python 3.12+**
- **FastAPI** — framework web
- **Uvicorn** — ASGI server
- **python-dotenv** — manajemen environment variable

---

## Struktur Proyek

```
back-and/
├── main.py                  # Entry point aplikasi
└── app/
    ├── api/                 # Layer router (menerima request HTTP)
    │   ├── files.py
    │   ├── folders.py
    │   ├── storage.py
    │   └── pysystem.py
    └── service/             # Layer bisnis (logika utama)
        ├── files.py
        ├── folders.py
        ├── storage.py
        └── pysystem.py
```

---

## Instalasi

### 1. Clone / copy project
```bash
cd back-and
```

### 2. Buat virtual environment (opsional tapi disarankan)
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Install dependensi
```bash
# Instalasi manual
pip install fastapi uvicorn python-dotenv python-multipart 

# Atau menggunakan requirements.txt
pip install -r requirements.txt
```

### 4. Buat file `.env`
```env
DIR=/path/ke/direktori/penyimpanan
KEY=password_base64_kamu
BASE_URL=http://localhost:2026/thorix
```

| Variable   | Keterangan |
|------------|------------|
| `DIR`      | Path absolut direktori root penyimpanan file |
| `KEY`      | Nilai base64 dari password root (gunakan `path_to_id()` untuk generate) |
| `BASE_URL` | Base URL publik server, digunakan untuk generate `thumbnail_url` |

---

## Menjalankan Server

```bash
python main.py
```

Server berjalan di `http://0.0.0.0:2026` dengan hot-reload aktif.

---

## Konfigurasi Nginx

Aplikasi menggunakan `root_path="/thorix"`, sesuaikan konfigurasi Nginx:

```nginx
location /thorix/ {
    proxy_pass http://127.0.0.1:2026/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

---

## Endpoint API

### 📁 Folders

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| `GET` | `/folders/{folder_id}` | Tampilkan detail folder |
| `POST` | `/folders/` | Buat folder baru |
| `PATCH` | `/folders/{folder_id}` | Rename folder |
| `PATCH` | `/folders/{folder_id}/move` | Pindahkan folder |
| `DELETE` | `/folders/{folder_id}` | Hapus folder |

### 📄 Files

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| `GET` | `/files` | Tampilkan isi folder (`?path=.`) |
| `POST` | `/files/upload` | Upload file (`?path=.`) |
| `PUT` | `/files/{file_id}` | Rename file |
| `DELETE` | `/files/{file_id}` | Hapus file |
| `GET` | `/files/{id}/download` | Unduh file (`?preview=false`) |
| `GET` | `/files/{id}/thumbnail` | Tampilkan thumbnail gambar |

### 💾 Storage

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| `GET` | `/storage/info` | Info penggunaan disk |

### ⚙️ System

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| `POST` | `/system/{aksi}` | Reboot / shutdown server (`aksi`: `reboot` atau `shutdown`) |

---

## Autentikasi

Semua endpoint file dan folder menggunakan query parameter `password`. Nilai `password` adalah **virtual path** yang di-encode ke base64 URL-safe, dan harus cocok dengan nilai `KEY` di `.env`.

Contoh generate KEY:
```python
import base64
key = base64.urlsafe_b64encode("password-saya-sangat-aman".encode()).decode()
print(key)  # Masukkan nilai ini ke .env sebagai KEY
```

Gunakan saat request:
```
GET /files?password=/password-saya
```

---

## Fitur Keamanan

- **Path traversal protection** — mencegah akses ke luar direktori root (`../../etc/passwd`)
- **Lockdown mode** — saat sistem akan reboot/shutdown, semua operasi write (`POST`, `PUT`, `DELETE`, `PATCH`) diblokir otomatis
- **CORS** — terbuka untuk semua origin (sesuaikan untuk production)

---

## Dokumentasi Interaktif

Setelah server berjalan, buka:
- Swagger UI: `http://localhost:2026/thorix/docs`
- ReDoc: `http://localhost:2026/thorix/redoc`
