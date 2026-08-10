# Model Ancaman --- HealthTech: Automated PHI/PII Redaction Pipeline for LLMs

**Proyek:** HealthTech - Automated PHI/PII Redaction Pipeline for LLMs\
**Sistem:** Privacy Shield LLM\
**Cakupan:** Redaksi, pseudonimisasi, pemetaan token Redis, pemulihan,
API, masukan file, logging, dan batas integrasi LLM.

------------------------------------------------------------------------

## 1. Tujuan

Model ancaman ini mengidentifikasi aset, pelaku ancaman, batas
kepercayaan, permukaan serangan, ancaman keamanan, dan mitigasi yang
relevan dengan Privacy Shield LLM.

Tujuan keamanan utama:

> **Mencegah pengungkapan PHI/PII kepada pihak yang tidak berwenang
> sekaligus memungkinkan proses redaksi dan pemulihan dilakukan secara
> terkontrol.**

Analisis berdasarkan arsitektur yang telah diterapkan:

``` text
Front-End
    |
    v
FastAPI
    |
    +--> Regex Detection
    |      Email / Date / Phone / ID
    |
    +--> Presidio
    |
    v
RecognizerResult
    |
    v
Entity Processor
    |
    +--> Patient Detector
    +--> Doctor Detector
    +--> Address Detector
    |
    v
Resolver
    |
    v
Normalizer
    |
    v
Final Entities
    |
    v
Pseudonymizer
    |
    v
Mapping Service
    |
    v
Redis
    |
    v
Metrics Service
    |
    v
Response
```

Alur pemulihan:

``` text
Front-End
    |
    v
Restore API
    |
    v
restore_service
    |
    v
extract_tokens
    |
    v
Mapping Service
    |
    v
Redis
    |
    v
restored_mappings
    |
    v
Restore Text
    |
    v
Metrics Service
    |
    v
Response
```

------------------------------------------------------------------------

## 2. Aset yang Harus Dilindungi

  ID     Aset                   Contoh                             Sensitivitas
  ------ ---------------------- ---------------------------------- --------------
  A-01   Nama Pasien            `John Anderson`                    Kritis
  A-02   Nama Dokter            `Michael Johnson`                  Tinggi
  A-03   Alamat                 `25 Main Street, Boston`           Kritis
  A-04   Email                  `john@gmail.com`                   Tinggi
  A-05   Nomor Telepon          `+1 212-555-0187`                  Tinggi
  A-06   ID Pasien/Medis        `PAT-20260715`, `MRN-20260715`     Kritis
  A-07   Teks Klinis            Rekam medis pasien                 Kritis
  A-08   Token Pseudonimisasi   `[PATIENT_001]`                    Tinggi
  A-09   Pemetaan Token         `PATIENT_001 -> John Anderson`     Kritis
  A-10   Data Mapping Redis     Pemetaan asli/token                Kritis
  A-11   Request API            Request redaksi/pemulihan          Tinggi
  A-12   Log Aplikasi           Informasi pemrosesan/aktivitas     Tinggi
  A-13   Metrik                 Jumlah entitas/durasi pemrosesan   Sedang

### Aset Kritis: Pemetaan Token

Aset paling sensitif adalah hubungan antara token dan nilai aslinya:

``` text
PATIENT_001 -> John Anderson
```

Token teredaksi saja tidak secara langsung menampilkan nama pasien:

``` text
[PATIENT_001]
```

Namun, jika mapping diperoleh attacker, pseudonimisasi dapat dibalik.
Karena itu, Redis dan Mapping Service merupakan komponen keamanan
bernilai tinggi.

------------------------------------------------------------------------

## 3. Threat Actor

### TA-01 --- Attacker Eksternal

Mencoba berinteraksi dengan API tanpa otorisasi.

Tujuan yang mungkin:

-   mengirim masukan berbahaya;
-   menghabiskan sumber daya;
-   menyalahgunakan endpoint;
-   memperoleh PHI/PII.

### TA-02 --- Pengguna Aplikasi Tanpa Otorisasi

Pengguna yang dapat mengakses aplikasi tetapi tidak memiliki hak untuk
memulihkan data yang dilindungi.

### TA-03 --- Host atau Container Terkompromi

Attacker yang memperoleh akses ke host Docker, container aplikasi, atau
container Redis.

Tujuan yang mungkin:

-   membaca mapping Redis;
-   memperoleh credential;
-   memeriksa konfigurasi;
-   mengekstraksi data.

### TA-04 --- Konsumen Downstream Berbahaya atau Terkompromi

Sistem downstream atau integrasi LLM yang menerima teks klinis yang
telah diproses.

### TA-05 --- Insider

Pengguna internal yang memiliki akses resmi tetapi sengaja mengakses
mapping atau log sensitif.

------------------------------------------------------------------------

## 4. Batas Kepercayaan

### TB-01 --- Pengguna ↔ Front-End

**Risiko:** masukan berbahaya, penggunaan tanpa izin, atau pengiriman
data sensitif secara tidak sengaja.

### TB-02 --- Front-End ↔ FastAPI

**Risiko:** manipulasi request, akses API tanpa izin, request
berlebihan, dan penyalahgunaan endpoint.

### TB-03 --- Aplikasi ↔ Redis

**Risiko:** akses tanpa izin terhadap mapping PHI/PII yang dapat
dibalik.

Ini merupakan batas penyimpanan paling kritis.

### TB-04 --- Sistem Redaksi ↔ LLM Downstream

**Risiko:** PHI/PII yang tidak terdeteksi dapat melewati batas privasi.

------------------------------------------------------------------------

## 5. Permukaan Serangan

``` text
                    Front-End
                       |
                       v
                    FastAPI
                 /           \
                /             \
        /redact               /restore
           |                      |
           v                      v
    Detection Pipeline      Mapping Service
           |                      |
           +-----------> Redis <--+
                       |
                       v
                  Token Mapping
```

Permukaan serangan utama:

1.  Redact API.
2.  Restore API.
3.  Masukan teks klinis.
4.  Unggah file `.txt`.
5.  Redis.
6.  Token mapping.
7.  Log aplikasi.
8.  Lingkungan Docker/container.
9.  Konfigurasi dan credential.
10. Integrasi LLM downstream.

------------------------------------------------------------------------

## 6. Matriks Ancaman

  -----------------------------------------------------------------------------------------------
  ID          Ancaman                  Komponen        STRIDE        Dampak           Risiko
  ----------- ------------------------ --------------- ------------- ---------------- -----------
  T-01        Mapping Redis terekspos  Redis           Information   Pengungkapan     Kritis
                                                       Disclosure    PHI/PII          

  T-02        Restore tanpa izin       Restore API     Elevation of  Pemulihan        Kritis
                                                       Privilege /   PHI/PII asli     
                                                       Information                    
                                                       Disclosure                     

  T-03        Kegagalan deteksi        Regex /         Information   PHI/PII masuk    Kritis
                                       Presidio / NLP  Disclosure    downstream       

  T-04        Masukan berukuran besar  API / NLP       Denial of     Penggunaan       Tinggi
                                                       Service       sumber daya      
                                                                     berlebihan       

  T-05        Logging data sensitif    Log             Information   Kebocoran        Tinggi
                                                       Disclosure    PHI/PII sekunder 

  T-06        Mapping token bocor      Pseudonymizer / Information   Pseudonimisasi   Tinggi
                                       Mapping Service Disclosure    dapat dibalik    

  T-07        Redis persistence        Redis / Storage Information   Pemetaan         Kritis
              terekspos                                Disclosure    historis         
                                                                     terekspos        

  T-08        False positive           Entity          Tampering /   Modifikasi data  Sedang
                                       Processor       Integrity     tidak diperlukan 

  T-09        Penyalahgunaan endpoint  FastAPI         Spoofing /    Pemrosesan tanpa Tinggi
              API                                      Elevation of  izin             
                                                       Privilege                      

  T-10        Penyalahgunaan unggah    Front-End / API Denial of     Penyalahgunaan   Tinggi
              file                                     Service /     sumber daya      
                                                       Tampering                      

  T-11        Credential/konfigurasi   Docker /        Information   Kompromi         Kritis
              terekspos                Environment     Disclosure    infrastruktur    

  T-12        PHI/PII tersisa masuk    Batas LLM       Information   Pengungkapan     Kritis
              LLM                                      Disclosure    data sensitif    
  -----------------------------------------------------------------------------------------------

------------------------------------------------------------------------

## 7. Analisis Ancaman

### T-01 --- Mapping Redis Terekspos

Redis dapat berisi:

``` text
PATIENT_001 -> John Anderson
PATIENT_002 -> Sarah Williams
DOCTOR_001  -> Michael Johnson
ADDRESS_001 -> 25 Main Street
```

Akses Redis tanpa izin dapat membalik pseudonimisasi.

**Dampak:** Kritis.

**Kontrol arsitektur yang sudah ada:** Front-End tidak berkomunikasi
langsung dengan Redis; Mapping Service menjadi perantara.

**Kontrol yang direkomendasikan:**

-   Autentikasi dan otorisasi Redis.
-   Isolasi pada jaringan internal.
-   Jangan mengekspos Redis secara publik.
-   Lindungi credential.
-   Batasi akses administratif.
-   Pantau akses tanpa izin.
-   Gunakan enkripsi jika diperlukan.

### T-02 --- Restore Tanpa Otorisasi

Restore memang dirancang untuk mengembalikan nilai asli. Attacker dapat
mencoba:

``` text
[PATIENT_001]
[DOCTOR_001]
[ADDRESS_001]
```

untuk memperoleh PHI/PII asli.

**Dampak:** Kritis.

**Kontrol yang direkomendasikan:**

-   Autentikasi kuat.
-   Otorisasi restore.
-   Isolasi mapping berdasarkan user/session.
-   Audit logging.
-   Rate limiting.
-   Validasi token secara ketat.

### T-03 --- Kegagalan Deteksi

Detector dapat gagal mengenali:

``` text
Patient John Anderson
```

Jika nama tersebut terlewat, data dapat diteruskan ke LLM downstream.

**Dampak:** Kritis.

**Komponen terkait:** Regex, Presidio, Patient Detector, Doctor
Detector, Address Detector, Resolver, dan Normalizer.

**Kontrol yang direkomendasikan:**

-   Layered detection.
-   Pengujian false negative.
-   Pengujian format tidak biasa.
-   Pengujian nomor telepon/identifier internasional.
-   Monitoring cakupan deteksi.
-   Fail-safe untuk entitas yang tidak pasti.

### T-04 --- Masukan Berukuran Besar

Attacker dapat mengirim dokumen klinis besar secara berulang sehingga:

``` text
Regex -> Presidio -> NLP -> Resolver -> Normalizer -> Pseudonymizer -> Redis
```

menggunakan CPU, memory, dan waktu secara berlebihan.

**Dampak:** Tinggi.

**Kontrol yang direkomendasikan:**

-   Batas ukuran request/file.
-   Rate limiting.
-   Timeout.
-   Batas concurrency.
-   Monitoring sumber daya.
-   Penolakan request yang terlalu besar.

### T-05 --- Logging Data Sensitif

Aplikasi dapat melakukan redaksi dengan benar tetapi secara tidak
sengaja menyimpan teks asli ke log.

Contoh tidak aman:

``` text
Patient John Anderson
john@gmail.com
+1 212-555-0187
```

**Dampak:** Tinggi.

**Kontrol yang direkomendasikan:**

-   Jangan mencatat teks klinis mentah.
-   Jangan mencatat nilai entitas asli.
-   Sanitasi exception message.
-   Batasi akses log.
-   Tetapkan retensi log.
-   Audit perilaku logging.

### T-06 --- Pemetaan Token Bocor

Token:

``` text
[PATIENT_001]
[PATIENT_002]
```

menjadi sensitif ketika dikombinasikan dengan:

``` text
PATIENT_001 -> John Anderson
PATIENT_002 -> Sarah Williams
```

**Dampak:** Tinggi.

> **Pseudonimisasi adalah mekanisme perlindungan data, bukan pengganti
> access control.**

### T-07 --- Redis Persistence Terekspos

File persistence, backup, snapshot, atau volume Redis dapat mengekspos
mapping historis.

**Dampak:** Kritis.

**Kontrol yang direkomendasikan:**

-   Lindungi Redis persistence.
-   Amankan backup.
-   Batasi akses volume.
-   Enkripsi backup.
-   Tetapkan retensi/penghapusan.
-   Batasi akses host Docker.

### T-08 --- False Positive

Nilai normal dapat salah diklasifikasikan:

``` text
[ADDRESS_001]
```

**Dampak:** Sedang.

**Kontrol arsitektur yang sudah ada:** Resolver menangani
overlap/prioritas dan Normalizer mengelompokkan entitas.

**Kontrol yang direkomendasikan:**

-   Pengukuran precision/recall.
-   Penambahan kasus validasi.
-   Evaluasi confidence threshold.
-   Pengujian teks ambigu.

### T-09 --- Penyalahgunaan Endpoint API

Pemanggilan berulang atau tanpa izin terhadap:

``` text
POST /redact
POST /restore
```

dapat menyebabkan pemrosesan tanpa izin, resource exhaustion, atau
pengungkapan informasi.

**Dampak:** Tinggi.

**Kontrol yang direkomendasikan:**

-   Autentikasi.
-   Otorisasi.
-   Rate limiting.
-   Validasi request.
-   Audit logging.
-   CORS yang aman.
-   HTTPS pada deployment.

### T-10 --- Penyalahgunaan Unggah File

Fitur unggah `.txt` dapat disalahgunakan dengan file sangat besar,
rusak, atau dikirim berulang.

**Dampak:** Tinggi.

**Kontrol yang direkomendasikan:**

-   Validasi file.
-   Batas ukuran.
-   Timeout.
-   Pembersihan temporary file.
-   Penanganan nama file yang aman.
-   Rate limiting.

### T-11 --- Credential atau Konfigurasi Terekspos

Credential Redis, konfigurasi API, atau secret dapat bocor melalui
source code, `.env`, Git history, Docker, atau log.

**Dampak:** Kritis.

**Kontrol yang direkomendasikan:**

-   Environment variable atau secret manager.
-   `.gitignore` untuk secret lokal.
-   Rotasi credential.
-   Jangan commit production secret.
-   Batasi akses environment container.
-   Periksa Git history untuk secret.

### T-12 --- PHI/PII Tersisa Masuk ke LLM

Jika detection gagal:

``` text
Clinical Text
     |
     v
Redaction
     |
     X  <-- PHI/PII tidak terdeteksi
     |
     v
LLM
```

**Dampak:** Kritis.

**Kontrol yang direkomendasikan:**

-   Perlakukan redaksi sebagai security boundary.
-   Layered detection.
-   Validasi output akhir.
-   Fail-safe untuk entitas yang tidak pasti.
-   Data minimization.
-   Monitoring aliran data downstream.

------------------------------------------------------------------------

## 8. Pemetaan Kontrol Keamanan

  Kontrol                         Ancaman
  ------------------------------- -------------------------------------------
  Regex + Presidio + Custom NLP   T-03, T-08, T-12
  Resolver / priority handling    T-03, T-08
  Normalizer                      T-03, T-08
  Pseudonymization                T-03, T-06, T-12
  Mapping Service                 T-01, T-02, T-06
  Redis isolation                 T-01, T-07
  Input validation                T-04, T-10
  File validation                 T-10
  Metrics Service                 Mendukung monitoring dan analisis anomali
  Response schema                 Mengontrol struktur response API
  Validation testing              T-03, T-08, T-09, T-10

------------------------------------------------------------------------

## 9. Abuse Case

### Abuse Case 1 --- Akses Redis Langsung

``` text
Attacker
   |
   v
Redis
   |
   v
PATIENT_001 -> John Anderson
```

**Tujuan:** memperoleh PHI/PII asli.

### Abuse Case 2 --- Penyalahgunaan Restore

``` text
Attacker
   |
   v
/restore
   |
   v
[PATIENT_001]
   |
   v
Nama Pasien Asli
```

**Tujuan:** memulihkan data tanpa otorisasi.

### Abuse Case 3 --- Bypass Detection

``` text
Format PHI/PII yang dibuat khusus
          |
          v
Detector gagal
          |
          v
Informasi asli tetap berada di teks
```

**Tujuan:** melewati lapisan redaksi.

### Abuse Case 4 --- Resource Exhaustion

``` text
Attacker
   |
   v
Request besar / berulang
   |
   v
Regex + Presidio + NLP
   |
   v
CPU / Memory exhaustion
```

**Tujuan:** menurunkan ketersediaan layanan.

------------------------------------------------------------------------

## 10. Prioritas Risiko

### Prioritas 1 --- Perlindungan Mapping Redis

Redis menyimpan mapping yang dapat digunakan untuk membalik
pseudonimisasi.

### Prioritas 2 --- Otorisasi Restore

Restore memiliki kemampuan untuk mengembalikan PHI/PII asli.

### Prioritas 3 --- Kegagalan Deteksi

PHI/PII yang terlewat dapat melewati batas redaksi.

### Prioritas 4 --- Penyalahgunaan API dan Input

Pemrosesan NLP dapat membutuhkan sumber daya komputasi yang besar.

### Prioritas 5 --- Kebocoran Log dan Backup

Informasi sensitif dapat bocor di luar pipeline utama.

------------------------------------------------------------------------

## 11. Risiko Residual

Risiko residual terpenting adalah **ketidakpastian deteksi**.

Tidak ada regex, model NER, atau detector berbasis aturan yang dapat
menjamin seluruh kemungkinan representasi PHI/PII akan selalu dikenali.

``` text
Deteksi
    !=
Jaminan Privasi Mutlak
```

Privacy Shield LLM harus diperlakukan sebagai lapisan perlindungan
privasi dengan pendekatan defense-in-depth, bukan jaminan absolut bahwa
seluruh data sensitif selalu akan terdeteksi.

------------------------------------------------------------------------

## 12. Rekomendasi Keamanan

Untuk deployment production:

1.  Terapkan autentikasi dan otorisasi pada `/redact` dan `/restore`.
2.  Isolasi Redis dari akses jaringan publik.
3.  Lindungi credential Redis.
4.  Terapkan batas ukuran request dan file.
5.  Tambahkan rate limiting.
6.  Hindari logging teks klinis mentah.
7.  Lindungi Redis persistence dan backup.
8.  Validasi output redaksi sebelum dikirim downstream.
9.  Pisahkan mapping berdasarkan user/session jika digunakan banyak
    pengguna.
10. Gunakan HTTPS pada deployment.
11. Lakukan rotasi secret dan credential.
12. Pantau aktivitas yang berkaitan dengan keamanan.
13. Tetapkan kebijakan retensi dan penghapusan mapping sensitif.
14. Lanjutkan pengujian false negative dan false positive.

------------------------------------------------------------------------

## 13. Kesimpulan Model Ancaman

Hubungan keamanan paling kritis dalam Privacy Shield LLM adalah:

``` text
Pseudonymized Token
        |
        v
Token Mapping
        |
        v
Original PHI/PII
```

Arsitektur mengurangi paparan langsung dengan mengubah data sensitif
menjadi token:

``` text
John Anderson
      |
      v
[PATIENT_001]
```

Namun:

``` text
PATIENT_001 -> John Anderson
```

tetap harus dilindungi sebagai informasi yang sangat sensitif.

Area keamanan utama adalah:

-   Restore endpoint.
-   Redis mapping store.
-   Detection pipeline.
-   API input.
-   File upload.
-   Application logs.
-   Docker/configuration environment.
-   Batas integrasi LLM downstream.

Keamanan tidak dapat hanya bergantung pada pseudonimisasi. Sistem
membutuhkan defense-in-depth pada seluruh alur:

``` text
Input
  ↓
Detection
  ↓
Pseudonymization
  ↓
Mapping Storage
  ↓
API
  ↓
Restore
  ↓
Downstream LLM
```
