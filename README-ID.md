# privacy-shield-llm

Pipeline keamanan HealthTech otomatis yang mendeteksi dan melakukan redaksi terhadap Protected Health Information (PHI) dan Personally Identifiable Information (PII) sebelum data diproses oleh Large Language Models (LLMs), sehingga mendukung aplikasi AI yang aman, menjaga privasi, dan memenuhi kebutuhan kepatuhan.

## 1. Gambaran Umum Proyek

**privacy-shield-llm** adalah pipeline keamanan HealthTech yang dirancang untuk mengurangi risiko tereksposnya data PHI/PII sensitif ke aplikasi berbasis LLM.

Pipeline menggabungkan:

- FastAPI untuk lapisan API
- Regex untuk mendeteksi PII terstruktur
- spaCy dan Microsoft Presidio untuk deteksi entitas berbasis NLP
- Pseudonymization untuk entitas sensitif
- Redis untuk token mapping dan reverse mapping
- Docker untuk deployment berbasis container
- Automated testing dan CI/CD untuk validasi

Alur utama sistem:

```text
Clinical Text
    |
    v
Deteksi PII/PHI
   |          |
 Regex       NLP
   |          |
   +----+-----+
        |
        v
Pseudonymization / Redaction
        |
        v
Sanitized Text
        |
        v
LLM Processing
        |
        v
Reverse Mapping
        |
        v
Restored Response
```

## 2. Gambaran Sistem

Sistem memisahkan proses deteksi, transformasi, mapping, dan restoration ke dalam komponen yang berbeda.

### Detection Layer

Entitas terstruktur seperti email, nomor telepon, tanggal, dan ID dideteksi menggunakan regular expression.

Deteksi berbasis NLP digunakan untuk entitas yang membutuhkan konteks, seperti:

- Nama pasien
- Nama dokter
- Organisasi
- Alamat dan lokasi
- Entitas lain yang bergantung pada konteks

### Pseudonymization Layer

Data sensitif yang terdeteksi dapat diganti dengan token yang stabil, misalnya:

```text
John Doe       -> [PATIENT_001]
08123456789    -> [PHONE_001]
john@email.com -> [EMAIL_001]
```

### Redis Mapping Layer

Redis menyimpan hubungan antara nilai asli dan token yang dihasilkan sehingga teks yang telah disanitasi dapat dikembalikan jika diperlukan.

Mapping mendukung:

```text
Original Entity -> Token
Token           -> Original Entity
```

### Reverse Mapping

Setelah proses LLM selesai, token pada response dapat dikembalikan ke nilai aslinya menggunakan Redis.

Dengan demikian, informasi sensitif tetap dipisahkan dari tahap pemrosesan LLM.

## 3. Docker Deployment

Project menyediakan konfigurasi Docker untuk menjalankan aplikasi dan Redis menggunakan container.

Build image aplikasi:

```bash
docker build -t privacy-shield-llm:latest .
```

Jalankan application container sesuai konfigurasi Docker project.

Untuk Redis, project menyediakan Docker Compose.

## 4. Redis Setup

Redis digunakan sebagai penyimpanan mapping untuk proses pseudonymization dan reverse mapping.

Jalankan Redis:

```bash
docker compose up -d redis
```

Periksa container:

```bash
docker compose ps
```

Lihat log Redis:

```bash
docker compose logs -f redis
```

Tes koneksi Redis:

```bash
docker exec -it privacy-shield-redis redis-cli ping
```

Hasil yang diharapkan:

```text
PONG
```

Hentikan Redis:

```bash
docker compose stop redis
```

Hapus container:

```bash
docker compose down
```

Data Redis disimpan di Docker volume `redis_data`.

## 5. Konfigurasi Environment

Konfigurasi sensitif dimuat melalui environment variables.

Contoh:

```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
```

Untuk menjalankan project menggunakan container, environment variables dapat diberikan melalui Docker Compose.

Jangan commit file `.env` asli atau credential ke repository.

Gunakan `.env.example` jika ingin membagikan struktur konfigurasi yang dibutuhkan.

## 6. Struktur Project

Struktur sederhana project:

```text
privacy-shield-llm/
├── .github/
│   └── workflows/
├── Back-End/
│   ├── app/
│   │   ├── providers/
│   │   ├── routes/
│   │   ├── rules/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── static/
│   │   ├── test/
│   │   └── utils/
│   └── main.py
├── Front-End/
├── Doc/
├── images/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── Threat-model-EN.md
├── Threat-model-ID.md
├── README.md
└── README-ID.md
```

Struktur implementasi dapat berubah seiring perkembangan project.

## 7. Pertimbangan Keamanan

Pipeline dirancang berdasarkan prinsip meminimalkan paparan data sensitif sebelum data diproses oleh LLM.

Pertimbangan keamanan utama:

- Deteksi PHI/PII sebelum data dikirim ke LLM.
- Usahakan nilai sensitif asli tidak masuk ke teks yang diproses LLM.
- Gunakan token pseudonymous sebagai pengganti nilai sensitif.
- Simpan mapping token di Redis dan jangan mengekspos mapping tersebut ke LLM.
- Lindungi credential Redis menggunakan environment variables.
- Jangan commit file `.env` yang berisi secret.
- Lakukan validasi terhadap input dan output.
- Uji entity yang sama secara berulang untuk memastikan mapping tetap konsisten.
- Uji unknown token dan mapping yang hilang agar dapat ditangani dengan aman.
- Untuk production, pertimbangkan persistence Redis, access control, network isolation, dan perlindungan credential.

## 8. Threat Model

Analisis keamanan project disimpan secara terpisah.

- [Threat Model — Indonesia](Threat-model-ID.md)

Threat model berfokus pada risiko keamanan yang berkaitan dengan pipeline redaction PHI/PII HealthTech, termasuk kebocoran data sensitif, akses mapping tanpa izin, risiko yang berkaitan dengan LLM, keamanan Redis, dan integritas pipeline.

## 9. Dokumentasi

Dokumentasi tambahan project disimpan secara terpisah dari README utama.

Dokumentasi utama meliputi:

- Threat Model — Indonesia
- System Validation & Performance Testing — Indonesia
- Development and learning notes

## 10. Informasi Project

**Project:** HealthTech — Automated PHI/PII Redaction Pipeline for LLMs

**Repository:** `privacy-shield-llm`

**Technology:** Python, FastAPI, spaCy, Microsoft Presidio, Redis, Docker

**Purpose:** Melindungi data sensitif HealthTech sebelum diproses oleh aplikasi berbasis LLM.

## 11. Jadwal Pengembangan

### Bootcamp Preparation

| Tanggal       | Aktivitas         |
| ------------- | ----------------- |
| June 06, 2026 | On Boarding       |
| July 13, 2026 | Division of Tasks |

### Week 1 — FastAPI Server

**July 13 – July 20, 2026**

| Tanggal | Aktivitas                                                                                        | Commit                                                                                  |
| ------- | ------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------- |
| July 13 | Day 1 - API Architecture Research & REST API Fundamentals                                        | `docs: add FastAPI architecture and REST API learning notes`                            |
| July 14 | Day 2 - FastAPI Project Initialization                                                           | `feat: initialize FastAPI project structure and development environment`                |
| July 15 | Day 3 - API Endpoint Development                                                                 | `feat: implement root and redact API endpoints`                                         |
| July 16 | Day 4 - Request & Response Processing                                                            | `feat: add JSON request parsing and response handling`                                  |
| July 17 | Day 5 - API Validation & Error Handling                                                          | `feat: implement request validation and error handling`                                 |
| July 18 | Day 6 - Building Front-End, Refactor Back-End, Connected Between Front-End & Back-End using CORS | `refactor: organize project into routes schemas and services`                           |
| July 19 | Day 7 - API Testing & Documentation in Week 1                                                    | `test: verify API endpoints and update Postman documentation & documentation in Week 1` |

### Week 2 — Regex Detection

**July 20 – July 27, 2026**

| Tanggal | Aktivitas                                        | Commit                                                                                           |
| ------- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| July 20 | Day 8 - Fundamental Regex Pattern Research       | `docs: add regex learning examples and validation patterns`                                      |
| July 21 | Day 9 - Email Detection Module                   | `feat: implement email detection using regex`                                                    |
| July 22 | Day 10 - Phone Detection Module                  | `feat: implement phone number detection using regex`                                             |
| July 23 | Day 11 - Date Detection Module                   | `feat: implement date detection using regex`                                                     |
| July 24 | Day 12 - Identity Detection Module               | `feat: implement patient ID and SSN detection`                                                   |
| July 25 | Day 13 - Regex Detection Pipeline                | `feat: integrate regex detectors into detection pipeline`                                        |
| July 26 | Day 14 - Regex Testing & Documentation in Week 2 | `test: validate regex detection pipeline with sample clinical notes and documentation in week 2` |

### Week 3 — NLP Detection

**July 27 – August 2, 2026**

| Tanggal  | Aktivitas                                                   | Commit                                                                            |
| -------- | ----------------------------------------------------------- | --------------------------------------------------------------------------------- |
| July 27  | Day 15 - NLP & NER Research                                 | `docs: add NLP and named entity recognition learning notes`                       |
| July 28  | Day 16 - spaCy Integration                                  | `feat: integrate spaCy named entity recognition`                                  |
| July 29  | Day 17 - Microsoft Presidio Integration                     | `feat: integrate Microsoft Presidio analyzer engine`                              |
| July 30  | Day 18 - Person Entity Detection                            | `feat: implement patient and doctor name detection`                               |
| July 31  | Day 19 - Address Entity Detection                           | `feat: implement address and location entity detection`                           |
| August 1 | Day 20 - Context-Aware Detection                            | `feat: improve contextual entity recognition for medical terms`                   |
| August 2 | Day 21 - NLP Pipeline Integration & Documentation in Week 3 | `feat: integrate NLP detection into redaction pipeline & documentation in week 3` |

### Week 4 — Integration & Deployment

**August 3 – August 9, 2026**

| Tanggal  | Aktivitas                                                                   | Commit                                                               |
| -------- | --------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| August 3 | Day 22 - Pseudonymization Engine                                            | `feat: implement pseudonymization engine for sensitive entities`     |
| August 4 | Day 23 - Redis Token Mapping Service                                        | `feat: implement Redis-based token mapping service`                  |
| August 5 | Day 24 - Reverse Mapping Integration                                        | `feat: integrate reverse mapping into LLM response pipeline`         |
| August 6 | Day 25 - System Validation & Performance Testing                            | `test: validate end-to-end pipeline performance and reverse mapping` |
| August 7 | Day 26 - Threat Modeling & Security Analysis for PHI/PII Redaction Pipeline | `docs: add HealthTech PII threat modeling`                           |
| August 8 | Day 27 - Project Documentation, Architecture & Security Report              | `docs: finalize project documentation`                               |

<!--
| July 04, 2026 | Day 28 | Final Documentation & Project Integration | -->

## 12. Testing

Dokumentasi testing disimpan secara terpisah untuk versi English dan Indonesia.

- [System Validation & Performance Testing — Indonesia](System%20Validation%20%26%20Performance%20Testing-ID.md)

Testing mencakup functional validation, duplicate entity mapping, clinical input testing, performance testing, reverse mapping, unknown tokens, empty input, dan Redis mapping behavior.

---

**Project:** privacy-shield-llm  
**HealthTech Security Pipeline — PHI/PII Protection for LLM Applications**
