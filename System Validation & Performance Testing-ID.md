# Dokumentasi Pengujian Privacy Shield LLM

## 1. Tujuan Pengujian

Dokumentasi ini berisi hasil pengujian terhadap **Privacy Shield LLM**, khususnya pada proses:

- deteksi data sensitif;
- penyamaran data sensitif;
- penyimpanan pemetaan token pada Redis;
- pemulihan data asli;
- penanganan masukan yang tidak valid;
- pengujian dengan berbagai tingkat kompleksitas data klinis;
- pengukuran performa sistem.

Pengujian dilakukan untuk memastikan bahwa sistem tidak hanya berhasil melakukan penyamaran, tetapi juga mampu mempertahankan hubungan antara **data asli → token → data asli** selama proses pemulihan.

---

# 2. Struktur Dokumentasi Bukti

Bukti pengujian disimpan pada direktori:

```text
images/
└── Week 4/
    ├── Functional Testing/
    │   ├── case 1 - simple/
    │   ├── case 2 - medium/
    │   └── case 3 - duplicate entity/
    │
    ├── Performance Testing/
    │   ├── case 1 - small clinical/
    │   ├── case 2 - medium clinical/
    │   └── case 3 - Large clinical/
    │
    └── Validation Testing/
        ├── case 1 - empty input/
        ├── case 2 - normal text/
        ├── case 3 - restore no token/
        ├── case 4 - unknown text/
        └── case 5 - empty restore/
```

Dokumentasi ini menggunakan gambar pada struktur tersebut sebagai bukti visual pengujian.

---

# 3. Pengujian Fungsional

## 3.1 Kasus 1 — Teks Sederhana

### Tujuan

Memastikan sistem mampu memproses teks klinis sederhana yang memiliki beberapa jenis data sensitif.

### Skenario

Teks masukan berisi data seperti:

- nama pasien;
- nama dokter;
- tanggal;
- alamat;
- alamat surel;
- nomor telepon;
- identitas pasien.

### Hasil yang Diharapkan

Sistem harus:

1. menerima teks;
2. mendeteksi entitas sensitif;
3. menghasilkan token untuk setiap entitas;
4. menampilkan teks yang telah disamarkan;
5. menyimpan pemetaan token pada Redis;
6. dapat mengembalikan data asli melalui proses pemulihan.

### Bukti

**Hasil penyamaran:**

![Hasil penyamaran kasus sederhana](images/Week%204/Functional%20Testing/case%201%20-%20simple/redacted%20text.png)

**Bukti Redis:**

![Bukti Redis kasus sederhana](images/Week%204/Functional%20Testing/case%201%20-%20simple/redis%20server.png)

**Hasil pemulihan:**

![Hasil pemulihan kasus sederhana](images/Week%204/Functional%20Testing/case%201%20-%20simple/restored%20text.png)

### Kesimpulan

Kasus sederhana digunakan sebagai pengujian dasar untuk memastikan seluruh alur utama sistem dapat berjalan dari deteksi hingga pemulihan.

---

# 4. Pengujian Fungsional Kasus 2 — Banyak Entitas

## 4.1 Tujuan

Pengujian ini digunakan untuk memastikan sistem dapat menangani teks yang memiliki lebih banyak entitas sensitif dalam satu masukan.

### Skenario

Teks klinis memiliki beberapa pasien, dokter, alamat, tanggal, nomor identitas, alamat surel, dan nomor telepon.

### Hasil yang Diharapkan

Sistem harus mampu:

- mendeteksi banyak entitas;
- memberikan token berbeda untuk setiap entitas;
- mempertahankan jenis entitas;
- menyimpan seluruh pemetaan pada Redis;
- melakukan pemulihan tanpa kehilangan data.

### Bukti

**Hasil penyamaran:**

![Hasil penyamaran kasus banyak entitas](images/Week%204/Functional%20Testing/case%202%20-%20mixed%20entity/redacted%20text.png)

**Bukti Redis:**

![Bukti Redis kasus banyak entitas](images/Week%204/Functional%20Testing/case%202%20-%20mixed%20entity/redis%20server.png)

**Hasil pemulihan:**

![Hasil pemulihan kasus banyak entitas](images/Week%204/Functional%20Testing/case%202%20-%20mixed%20entity/restored%20text.png)

### Kesimpulan

Kasus ini memvalidasi bahwa sistem tidak hanya bekerja pada satu atau dua entitas, tetapi juga dapat menangani beberapa entitas dalam satu dokumen klinis.

---

# 5. Pengujian Fungsional Kasus 3 — Entitas Duplikat

## 5.1 Tujuan

Pengujian ini berfokus pada entitas yang muncul lebih dari satu kali.

### Skenario

Satu data pribadi yang sama atau beberapa data yang sama muncul berulang kali dalam teks klinis.

Contohnya:

```text
Patient John Anderson visited the hospital.
The patient John Anderson was examined by the doctor.
John Anderson returned for a follow-up examination.
```

### Hal yang Diperiksa

Pengujian ini memastikan:

- sistem tidak kehilangan kemunculan entitas;
- setiap kemunculan ditangani dengan benar;
- pemetaan Redis tetap konsisten;
- proses pemulihan menghasilkan data yang sesuai.

### Bukti

**Hasil penyamaran:**

![Hasil penyamaran entitas duplikat](images/Week%204/Functional%20Testing/case%203%20-%20duplicate%20entity/redacted%20text.png)

**Bukti Redis:**

![Bukti Redis entitas duplikat](images/Week%204/Functional%20Testing/case%203%20-%20duplicate%20entity/redis%20server.png)

**Hasil pemulihan:**

![Hasil pemulihan entitas duplikat](images/Week%204/Functional%20Testing/case%203%20-%20duplicate%20entity/restored%20text.png)

### Kesimpulan

Kasus ini digunakan untuk memastikan mekanisme pseudonimisasi dan pemetaan tidak mengalami konflik ketika entitas muncul berulang kali.

---

# 6. Pengujian Performa

Pengujian performa digunakan untuk mengetahui bagaimana sistem merespons ketika ukuran teks klinis bertambah.

Pengujian dibagi menjadi tiga skala:

1. kecil;
2. sedang;
3. besar.

---

## 6.1 Kasus 1 — Dokumen Klinis Kecil

### Tujuan

Mengukur waktu pemrosesan ketika sistem menerima dokumen klinis dengan jumlah teks dan entitas yang relatif sedikit.

### Parameter yang Diamati

- waktu pemrosesan;
- jumlah entitas;
- hasil penyamaran;
- hasil pemulihan;
- pemetaan Redis.

### Bukti Hasil Penyamaran

![Hasil performa dokumen kecil](images/Week%204/Performance%20Testing/case%201%20-%20small%20clinical/redacted%20text.png)

### Bukti Redis

![Redis dokumen kecil](images/Week%204/Performance%20Testing/case%201%20-%20small%20clinical/redis%20server.png)

### Bukti Pemulihan

![Pemulihan dokumen kecil](images/Week%204/Performance%20Testing/case%201%20-%20small%20clinical/restored%20text.png)

---

# 7. Pengujian Performa Kasus 2 — Dokumen Klinis Sedang

## Tujuan

Mengetahui kemampuan sistem ketika jumlah teks dan entitas meningkat dibandingkan kasus kecil.

### Bukti Hasil Penyamaran

![Hasil performa dokumen sedang](images/Week%204/Performance%20Testing/case%202-%20medium%20clinical/redacted%20text.png)

### Bukti Redis

![Redis dokumen sedang](images/Week%204/Performance%20Testing/case%202-%20medium%20clinical/redis%20server.png)

### Bukti Pemulihan

![Pemulihan dokumen sedang](images/Week%204/Performance%20Testing/case%202-%20medium%20clinical/restored%20text.png)

### Kesimpulan

Kasus ini digunakan untuk membandingkan perubahan waktu pemrosesan ketika beban data meningkat.

---

# 8. Pengujian Performa Kasus 3 — Dokumen Klinis Besar

## Tujuan

Menguji sistem menggunakan teks klinis berukuran besar dengan jumlah entitas yang lebih banyak.

### Bukti Hasil Penyamaran

![Hasil performa dokumen besar](images/Week%204/Performance%20Testing/case%203%20-%20Large%20clinical/redacted%20text.png)

### Bukti Redis Bagian 1

![Redis dokumen besar bagian 1](images/Week%204/Performance%20Testing/case%203%20-%20Large%20clinical/redis%20server%20part%201.png)

### Bukti Redis Bagian 2

![Redis dokumen besar bagian 2](images/Week%204/Performance%20Testing/case%203%20-%20Large%20clinical/redis%20server%20part%202.png)

### Bukti Pemulihan

![Pemulihan dokumen besar](images/Week%204/Performance%20Testing/case%203%20-%20Large%20clinical/restored%20text.png)

### Kesimpulan

Kasus ini menjadi pengujian beban terbesar dalam rangkaian pengujian dan digunakan untuk melihat apakah sistem tetap mampu melakukan penyamaran, pemetaan, serta pemulihan ketika jumlah data meningkat secara signifikan.

---

# 9. Pengujian Validasi

Pengujian validasi digunakan untuk memastikan sistem memberikan respons yang benar terhadap kondisi normal maupun kondisi yang tidak valid.

---

## 9.1 Kasus 1 — Masukan Kosong

### Tujuan

Memastikan sistem tidak memproses masukan kosong.

### Skenario

Pengguna menekan tombol penyamaran tanpa memasukkan teks klinis.

### Hasil yang Diharapkan

Sistem harus menolak proses dan memberikan pemberitahuan bahwa masukan tidak boleh kosong.

### Bukti

![Validasi masukan kosong](images/Week%204/Validation%20Testing/case%201%20-%20empty%20input/null%20redacted.png)

![Validasi pemulihan masukan kosong](images/Week%204/Validation%20Testing/case%201%20-%20empty%20input/null%20restored.png)

### Kesimpulan

Validasi masukan kosong memastikan sistem tidak melakukan pemrosesan yang tidak diperlukan terhadap data kosong.

---

# 10. Pengujian Validasi Kasus 2 — Teks Normal

## Tujuan

Memastikan sistem dapat menerima teks yang tidak memiliki entitas sensitif.

### Skenario

Pengguna memberikan teks biasa tanpa informasi pribadi atau medis yang perlu disamarkan.

### Hasil yang Diharapkan

Sistem tetap dapat memproses masukan tanpa menghasilkan token yang tidak diperlukan.

### Bukti

![Validasi teks normal](images/Week%204/Validation%20Testing/case%202%20-%20normal%20text/redacrted%20text.png)

### Kesimpulan

Kasus ini memastikan sistem tidak secara berlebihan menyamarkan seluruh teks yang diterima.

---

# 11. Pengujian Validasi Kasus 3 — Pemulihan Tanpa Token

## Tujuan

Memastikan sistem dapat menangani proses pemulihan ketika teks yang diberikan tidak memiliki token yang terdaftar pada Redis.

### Skenario

Pengguna memasukkan teks yang tidak memiliki token pseudonimisasi yang valid.

### Hasil yang Diharapkan

Sistem tidak boleh menghasilkan data palsu atau melakukan penggantian secara sembarangan.

### Bukti

![Pemulihan tanpa token](images/Week%204/Validation%20Testing/case%203%20-%20restore%20no%20token/restored%20text.png)

### Kesimpulan

Pengujian ini memastikan mekanisme pemulihan tidak melakukan substitusi terhadap token yang tidak diketahui.

---

# 12. Pengujian Validasi Kasus 4 — Teks Tidak Dikenal

## Tujuan

Menguji perilaku sistem ketika menerima teks yang tidak sesuai dengan pola dokumen klinis yang biasanya digunakan.

### Hasil yang Diharapkan

Sistem tetap memberikan respons yang stabil dan tidak mengalami kegagalan proses.

### Bukti

![Validasi teks tidak dikenal](images/Week%204/Validation%20Testing/case%204%20-%20uknown%20text/restored%20text.png)

### Kesimpulan

Pengujian ini memastikan sistem tetap stabil terhadap masukan yang berada di luar skenario utama.

---

# 13. Pengujian Validasi Kasus 5 — Pemulihan Kosong

## Tujuan

Memastikan proses pemulihan menangani masukan kosong dengan benar.

### Skenario

Pengguna menjalankan pemulihan tanpa memasukkan teks.

### Hasil yang Diharapkan

Sistem menolak pemrosesan dan memberikan respons validasi yang sesuai.

### Bukti

![Pemulihan kosong](images/Week%204/Validation%20Testing/case%205%20-%20empty%20redis/restored%20text.png)

### Kesimpulan

Validasi ini memastikan endpoint pemulihan memiliki perlindungan terhadap masukan kosong.

---

# 14. Ringkasan Jenis Pengujian

| Jenis Pengujian | Kasus | Fokus                 | BERHASIL/TIDAK BERHASIL |
| --------------- | ----: | --------------------- | ----------------------- |
| Fungsional      |     1 | Teks sederhana        | BERHASIL                |
| Fungsional      |     2 | Banyak entitas        | BERHASIL                |
| Fungsional      |     3 | Entitas duplikat      | BERHASIL                |
| Performa        |     1 | Dokumen klinis kecil  | BERHASIL                |
| Performa        |     2 | Dokumen klinis sedang | BERHASIL                |
| Performa        |     3 | Dokumen klinis besar  | BERHASIL                |
| Validasi        |     1 | Masukan kosong        | BERHASIL                |
| Validasi        |     2 | Teks normal           | BERHASIL                |
| Validasi        |     3 | Pemulihan tanpa token | BERHASIL                |
| Validasi        |     4 | Teks tidak dikenal    | BERHASIL                |
| Validasi        |     5 | Pemulihan kosong      | BERHASIL                |

---

# 15. Kesimpulan Pengujian

Berdasarkan rangkaian pengujian yang telah dilakukan, sistem diuji dari tiga sisi utama.

**Pertama, pengujian fungsional** memastikan fungsi utama sistem berjalan, mulai dari deteksi entitas, penyamaran, penyimpanan pemetaan, hingga pemulihan data.

**Kedua, pengujian performa** digunakan untuk melihat perubahan perilaku sistem ketika ukuran dokumen dan jumlah entitas meningkat dari skala kecil hingga besar.

**Ketiga, pengujian validasi** memastikan sistem dapat menangani kondisi masukan yang kosong, teks biasa, token yang tidak tersedia, teks yang tidak dikenal, serta proses pemulihan tanpa masukan.

Seluruh bukti visual pada dokumentasi ini berasal dari hasil pengujian yang disimpan pada direktori `images/Week 4/`. Dokumentasi tersebut dapat digunakan sebagai bukti pelaksanaan pengujian pada tahap akhir pengembangan Privacy Shield LLM.

---

# 16. Catatan

Dokumentasi ini berfokus pada **hasil dan bukti pengujian**, bukan pada penjelasan implementasi setiap fungsi di dalam kode sumber.

Untuk pengembangan lebih lanjut, hasil pengujian dapat dilengkapi dengan:

- waktu pemrosesan setiap skenario;
- jumlah entitas yang terdeteksi;
- jumlah entitas yang berhasil dipulihkan;
- tingkat keberhasilan deteksi;
- tingkat keberhasilan pemulihan;
- penggunaan memori;
- penggunaan CPU;
- perbandingan waktu pemrosesan antara skala kecil, sedang, dan besar.
