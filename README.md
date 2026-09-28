# The Build — Starter

**CIK3101 · Web Application Development · Sains Data · Semester 3 · Universitas Cakrawala**

Repo ini adalah tempat kerja kelompokmu selama 16 sesi. Artefak tiap sesi dikerjakan **di dalam
sesi** dan di-commit sebelum kelas selesai. **Tidak ada pekerjaan rumah.**

Repo ini sengaja **belum berisi aplikasi**. `frontend/` dan `backend/` kosong — kamu yang
mengisinya, mulai malam ini di Sesi 2. Yang sudah disediakan hanyalah rel: dokumen, CI, dan
pemeriksa nilai.

> **Proyek akhir mata kuliah ini bernama The Build, bobot 20% (Tugas Kelompok).**
> The Build bukan tugas tambahan. The Build adalah gabungan artefak Sesi 2–14 di repo ini,
> didemokan di Sesi 15 dan diverifikasi di Sesi 16. Baca **[`docs/PROJECT.md`](docs/PROJECT.md)**
> — itu piagam proyekmu, dan diisi malam ini.

---

## 0. Membuat repo kelompok (sekali saja, di Sesi 2)

Ini **administratif**, bukan tugas — sama seperti membawa laptop. Dikerjakan **ketua kelompok**,
sekali, di awal lab.

```bash
# 1. Di GitHub: buka repo template ini, klik "Use this template" -> "Create a new repository"
#    Nama repo : wad-2026-kNN     (NN = nomor kelompokmu, contoh wad-2026-k04)
#    Visibility: PUBLIC           (wajib — branch protection tidak tersedia di repo privat gratis)

# 2. Tambahkan 3 anggota lain sebagai collaborator
#    Settings -> Collaborators -> Add people   (pakai username GitHub mereka)

# 3. Semua anggota clone repo KELOMPOK, bukan template-nya
git clone https://github.com/<username-ketua>/wad-2026-kNN
cd wad-2026-kNN
cp .env.example .env
```

**4. Lindungi `main`** — ini butir 1 rubrik malam ini, dan dilakukan ketua:

> Settings → Branches → **Add branch protection rule**
> - Branch name pattern: `main`
> - ☑ **Require a pull request before merging**
> - ☑ **Do not allow bypassing the above settings**
> - Save changes

Setelah itu `git push` langsung ke `main` akan ditolak. Itu memang tujuannya. Semua perubahan
lewat branch `feature/*` dan pull request.

> "Require approvals" **jangan** dinyalakan malam ini — undangan collaborator mungkin belum
> diterima semua anggota, dan kamu akan terkunci tidak bisa merge. Naikkan ke 1 approval di
> Sesi 3, setelah semua anggota masuk.

**5. Kirim URL repo kelompokmu ke thread RISE.** Tanpa itu dosen tidak tahu ke mana harus menilai.

---

## 1. Prasyarat

| Alat | Versi | Cek |
|---|---|---|
| Git | apa saja | `git --version` |
| Node.js | 20 LTS atau lebih baru | `node -v` |
| Python | 3.11 atau lebih baru | `python --version` |
| Akun GitHub | — | sudah jadi anggota repo ini |

> Windows: saat install Python dari python.org, **centang "Add Python to PATH"**.
> Kalau `python` tidak dikenali, coba `py`.

Tidak ada yang perlu di-install untuk basis data sampai Sesi 5. Sampai sesi itu repo memakai
SQLite, yang sudah menyatu dengan Python.

## 2. Layanan

| Layanan | Port lokal | Mulai dipakai | Catatan |
|---|---|---|---|
| Frontend (Vite + Vue 3) | `5173` | Sesi 2 | kamu yang membuat isi `frontend/` |
| Backend (FastAPI + Uvicorn) | `8000` | Sesi 2 | kamu yang membuat isi `backend/` |
| Basis data | — | Sesi 3 | SQLite lokal; ganti ke Postgres (Neon) di Sesi 5 lewat `DATABASE_URL` |

## 3. Cara menjalankan

```bash
# sekali saja, setelah clone
cp .env.example .env

# --- backend (terminal 1) ---
cd backend
python -m venv venv
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# --- frontend (terminal 2) ---
cd frontend
npm install
npm run dev
```

## 4. Cara memverifikasi

Satu perintah, dipakai sepanjang semester:

```bash
python verify.py --sesi 2
```

`verify.py` adalah **perintah yang sama persis** yang dipakai dosen untuk memeriksa artefakmu.
Kalau hijau di laptopmu, hijau juga saat dinilai. Jalankan sebelum kamu keluar dari sesi.

> **CI merah saat repo baru itu normal.** Pemeriksa berjalan juga di GitHub Actions, dan pada
> repo kosong ia memang gagal — belum ada `frontend/` dan `backend/`. **Membuatnya hijau adalah
> tugasmu malam ini.** Ketentuan 7 (CI merah = 0 fungsionalitas) dinilai pada akhir sesi, bukan
> pada commit pertama.

Verifikasi manual yang juga dinilai:

- `http://localhost:5173` — halaman kerangka muncul, masih rapi di lebar 360px
- `http://localhost:8000/health` — balas `200` dengan `{"status":"ok"}`
- `http://localhost:8000/docs` — OpenAPI terbuka

### Verifikasi Cepat Requirement UTS (Kelompok 1 — Domain Pelatihan HR)

| Requirement | Cara Uji Cepat | Hasil yang Diharapkan |
|---|---|---|
| **B1** (GET /sessions) | Buka `http://localhost:8000/sessions?page=1&size=5&search=python` | HTTP 200, mengembalikan sesi pelatihan Python berpaginasi |
| **B2** (GET /sessions/{id}) | Buka `http://localhost:8000/sessions/999` di browser | HTTP 404 `{"detail": "Sesi pelatihan tidak ditemukan"}` |
| **B3** (POST /sessions) | Buka `/docs`, eksekusi `POST /sessions` dengan data baru | HTTP 201 Created dengan `id` baru ter-generate |
| **B4** (DELETE /sessions/{id}) | Buka `/docs`, eksekusi `DELETE /sessions/{id}` | HTTP 204 No Content |
| **B5** (CORS) | Cek header response untuk origin `localhost:5173` | `access-control-allow-origin: http://localhost:5173` |
| **F1 & F2** (4 State & Retry) | Matikan backend (`Ctrl+C`), refresh frontend $\rightarrow$ error & tombol retry muncul. Nyalakan backend, klik "Coba Lagi" $\rightarrow$ data muncul kembali | 4 state (loading, data, empty, error) teruji penuh |
| **F3** (Form Create) | Klik "+ Tambah Sesi", submit kosong $\rightarrow$ error validasi klien muncul | Validasi input klien dan tampilan error server |
| **F4** (Delete & Refresh) | Klik tombol "Hapus" pada baris sesi pelatihan | Dialog konfirmasi muncul; tabel otomatis ter-refresh |
| **Q1 & Q2** (HTML & Keyboard) | Navigasi halaman hanya dengan tombol `Tab` di keyboard | Kotak fokus terlihat tegas; semua input memiliki `<label>` |
| **Q4** (File < 100 baris) | Periksa line count berkas di `backend/app/` dan `frontend/src/` | Tidak ada berkas melebihi 100 baris |

### Pembagian Requirement UTS per Anggota (Kelompok 1)

| Anggota | Peran / Fokus | Requirement UTS | Ruang Lingkup |
|---|---|---|---|
| **Anggota 1** | Backend Lead & Data | **B1, B2** + Dataset | Dataset `data.py`, pagination, query search, 404 handler |
| **Anggota 2** | Backend Mutation | **B3, B4, B5** | Validasi Pydantic in/out, POST 201, DELETE 204, CORS |
| **Anggota 3** | Frontend State Lead | **F1, F2** | Render on mount + cleanup unmount, 4-state UI, tombol Retry |
| **Anggota 4** | Frontend Form & Quality | **F3, F4, Q1, Q2, Q4** | Form create, modal dialog konfirmasi delete, aksesibilitas keyboard |


## 5. Masalah yang sering muncul

| Gejala | Sebab biasanya | Tindakan |
|---|---|---|
| `python` tidak dikenali (Windows) | PATH tidak dicentang saat install | pakai `py`, atau install ulang dan centang "Add Python to PATH" |
| `npm run dev` jalan tapi halaman kosong | `index.html` tidak menunjuk `src/main.js` | cek `<script type="module" src="/src/main.js">` |
| `/health` 404 | `app.main` bukan modul yang dijalankan | jalankan `uvicorn` dari dalam folder `backend/` |
| CI merah karena `secret-scan` | ada rahasia ter-commit | **hapus nilainya, rotasi, commit ulang** — lihat Ketentuan 8 di bawah |
| `venv/` ikut ter-commit | `.gitignore` diubah | kembalikan `.gitignore` bawaan repo |
| Menu **Branches → Add rule** tidak ada | repo dibuat **Private** | Settings → General → Danger Zone → **Change visibility → Public** |
| Tidak bisa merge PR sendiri | "Require approvals" sudah dinyalakan | matikan dulu malam ini (lihat bagian 0 langkah 4) |

---

## Berkas siapa

| Punya kamu — kerjakan | Punya dosen — jangan diubah |
|---|---|
| `frontend/` (seluruhnya) | `verify.py` |
| `backend/` (seluruhnya) | `.github/workflows/` |
| `docs/PROJECT.md` (isian piagam) | `Dockerfile` |
| `docs/api-contract.md`, `docs/state.md` | `.gitignore`, `.env.example` |
| `CONTRIBUTORS.md` (isian nama) | `docs/DEPLOY.md` |
| `README.md` bagian 1–5 di atas | bagian **Ketentuan** di bawah |

Mengubah berkas milik dosen agar `verify.py` jadi hijau dihitung sebagai artefak yang tidak dapat
dipertahankan — nilainya 0 (Ketentuan 5).

## Peta sesi

| Sesi | Bobot | Yang jadi di ruang kelas |
|---|---|---|
| 1 | 2% | Jejak permintaan beranotasi |
| **2** | **2%** | **Repo + kerangka frontend/backend + README + 1 PR + piagam `docs/PROJECT.md`** |
| 3 | 2% | Endpoint pertama berjalan (FastAPI, Pydantic, status code) |
| 4 | **5%** | Diagram lapisan MVC + refactor satu endpoint |
| 5 | 2% | CRUD persisten + migrasi Alembic diterapkan · **pindah ke Postgres** |
| 6 | 2% | Rute + controller tipis + penanganan error terpusat |
| 7 | **5%** | `docs/api-contract.md` + model data (peer review) |
| **8** | **25%** | **UTS — ujian praktik individual** |
| 9 | 2% | Alur login berfungsi (JWT + bcrypt) |
| 10 | 2% | Otorisasi tingkat objek + RBAC |
| 11 | **5%** | Kerentanan ditemukan dan ditutup (break-in round) |
| 12 | 2% | Frontend terhubung + dua grafik + `docs/state.md` |
| 13 | 2% | Lima pengujian berjalan + tabel pengukuran di README |
| 14 | **5%** | **URL publik aktif + CI hijau** |
| 15 | 2% | **Demo The Build 8 menit di URL publik + pembelaan** |
| **16** | **25%** | **UAS — verifikasi submission + pembelaan tertulis** |

Urutan ini mengikuti RPS, bukan nomor berkas catatan mingguan.

## Ketentuan yang paling sering menghapus nilai

1. **Artefak wajib dapat dipertahankan.** Kode yang tidak bisa kamu jelaskan bernilai **0**,
   sebagus apa pun hasilnya. Berlaku juga untuk bagian yang ditulis anggota lain. Riwayat commit
   adalah bukti utama kepemilikan.
2. **Tidak dapat dijalankan = 0 fungsionalitas.** Gagal run, gagal build, atau CI merah bernilai
   0 pada komponen fungsionalitas. Aplikasi dinilai dengan **dijalankan di hadapan dosen**, bukan
   dari tangkapan layar.
3. **Tanpa commit atas namamu sendiri = 0 Tugas Kelompok**, berapa pun nilai timmu. Nilai
   individu = nilai kelompok × faktor kontribusi (0–1) dari commit/PR sendiri, peer assessment,
   dan kemampuan menjelaskan bagian **mana pun** dari kode.
4. **Kredensial ter-commit membatalkan nilai artefak sesi itu** — kunci API, kata sandi basis
   data, token. Berlaku **sejak Sesi 2**, jauh sebelum keamanan diajarkan formal. Karena itu
   `.env` ada di `.gitignore` dan CI menjalankan pemindai rahasia.
5. **Commit sebelum keluar.** Semua tenggat adalah akhir sesi. Waktu commit adalah bukti kerjamu
   dilakukan di dalam sesi.

## Penggunaan AI assistant

AI assistant **diizinkan** pada sesi praktikum, dan **dilarang pada UTS (Sesi 8) dan UAS
(Sesi 16)**. Syaratnya satu: tulis pengungkapan singkat di bawah ini, dan perbarui saat berubah.
Ketentuan 1 tetap berlaku penuh — kalau kamu tidak bisa menjelaskan kode yang dihasilkan AI,
nilainya 0.

<!-- ISI BAGIAN INI. Contoh:
- Sesi 2 — Claude, untuk menjelaskan pesan error `npm ERR! ENOENT`. Kode ditulis sendiri.
- Sesi 5 — GitHub Copilot, autocomplete pada model SQLAlchemy. Ditinjau dan diubah manual.
-->

- Sesi 7 & Persiapan UTS — Google Antigravity (Gemini), digunakan sebelum Sesi 8 untuk asistensi perancangan struktur folder, dataset sintetis in-memory, skema Pydantic, dan pemisahan komponen Vue modular <100 baris. Seluruh logika dipelajari mandiri oleh tiap anggota kelompok untuk persiapan pembelaan lisan.

## Kalau kamu tersendat

Tersendat di satu sesi tidak menghapus nilai sesi lain — **berhenti total yang menghapusnya**.
Kalau `frontend` atau `backend` tim belum jalan, tetap masuk sesi berikutnya, kerjakan yang bisa
dikerjakan, lalu minta waktu di 10 menit pertama sesi berikutnya. Lapor di thread RISE dengan
**seluruh pesan error**, bukan ringkasannya.
