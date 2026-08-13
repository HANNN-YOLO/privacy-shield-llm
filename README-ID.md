# privacy-shield-llm

Pipeline keamanan HealthTech otomatis yang dirancang untuk mendeteksi, melakukan pseudonymization, redaction, mapping, dan restoration terhadap Protected Health Information (PHI) dan Personally Identifiable Information (PII) dari teks klinis melalui pipeline pemrosesan yang terstruktur dan terukur.

Sistem ini menggabungkan deteksi berbasis rule, pengenalan entitas berbasis NLP, pemrosesan entitas, pseudonymization, mapping token berbasis Redis, restoration, serta metrik pemrosesan untuk menyediakan workflow perlindungan PHI/PII yang aman dan dapat diaudit.

---

## 1. Gambaran Umum Project

**privacy-shield-llm** merupakan pipeline keamanan HealthTech yang dirancang untuk mengurangi risiko tereksposnya data sensitif PHI/PII selama proses pemrosesan teks klinis.

Pipeline memisahkan workflow pemrosesan ke dalam beberapa tahapan khusus:

- FastAPI sebagai API layer
- Regex-based detection untuk PII terstruktur
- Microsoft Presidio untuk pengenalan entitas berbasis NLP
- RecognizerResult processing untuk memproses entitas yang terdeteksi
- Entity Processor untuk klasifikasi PHI/PII berdasarkan konteks
- Resolver untuk resolusi entitas
- Normalizer untuk normalisasi entitas
- Pseudonymization untuk entitas sensitif
- `redact_service` sebagai proses utama redaction
- `mapping_service` untuk penyimpanan dan pengambilan token/key
- Redis sebagai persistent mapping storage
- `restore_service` untuk mengembalikan entitas yang telah dimapping
- Metrics untuk pengukuran waktu pemrosesan dan hasil deteksi
- Docker untuk deployment berbasis container
- Automated testing dan CI/CD untuk validasi

Sistem terdiri dari dua alur pemrosesan utama:

1. **Redact Flow**
2. **Restore Flow**

### Redact Flow

Proses redaction dimulai dari Front-End dan melewati structured detection, NLP recognition, entity processing, normalization, pseudonymization, hingga akhirnya diproses oleh `redact_service`.

```text
                    Input (Front-End)
                           |
                           v
                   Regex Detection
               (EMAIL, DATE, PHONE, ID)
                           |
                           v
                        Presidio
                           |
                           v
                   RecognizerResult
                           |
                           v
                   Entity Processor
            (PATIENT, DOCTOR, ADDRESS, CONTEXT)
                           |
                           v
                       Resolver
                           |
                           v
                      Normalizer
                           |
                           v
                  Pseudonymization
                           |
                           v
                    redact_service
                       /       \
                      /         \
                     v           v
                 Metric    mapping_service
                                |
                                v
                           Redis Storage
```

`redact_service` bertindak sebagai titik pemrosesan utama setelah tahap pseudonymization.

Service ini menghasilkan dua jalur pemrosesan:

- **Metric Path** — mencatat waktu pemrosesan, informasi deteksi PII/PHI, dan metrik yang berkaitan dengan response.
- **Mapping Path** — mengirim key/token yang dihasilkan ke `mapping_service`, yang kemudian menyimpan mapping tersebut di Redis.

### Restore Flow

Proses restore mengambil mapping yang diperlukan dari Redis sebelum mengembalikan entitas yang telah dipseudonymize.

```text
                    Input (Front-End)
                           |
                           v
                   mapping_service
                      (GET KEYS)
                           |
                           v
                         Metric
             (Processing Time & PII/PHI Detection)
                           |
                           v
                    restore_service
                           |
                           v
                        Response
```

Restore Flow menggunakan mapping yang sebelumnya disimpan oleh workflow redaction untuk mengembalikan nilai yang sesuai sebelum response diberikan.

---

## 2. Gambaran Sistem

Sistem memisahkan proses detection, entity processing, transformation, mapping, restoration, dan metrics ke dalam beberapa komponen khusus.

### Detection Layer

Detection layer mengidentifikasi PHI/PII terstruktur dan berbasis konteks dari teks klinis yang masuk.

#### Regex Detection

Regular expression digunakan untuk structured identifiers seperti:

- Email
- Nomor telepon
- Tanggal
- Nomor identitas

Alur awal detection adalah:

```text
                    Input Text
                        |
                        v
                Regex Detection
                        |
                        +---- EMAIL
                        +---- DATE
                        +---- PHONE
                        +---- ID
```

Regex detection menyediakan lapisan awal yang deterministic untuk mendeteksi PII terstruktur.

#### Presidio Detection

Setelah tahap Regex Detection, teks diproses menggunakan Microsoft Presidio untuk melakukan pengenalan entitas berbasis NLP.

```text
                Clinical Text
                        |
                        v
                    Presidio
                        |
                        v
                RecognizerResult
```

Presidio bertanggung jawab untuk mengidentifikasi entitas berbasis konteks yang tidak dapat dideteksi secara reliable hanya menggunakan regular expression sederhana.

### RecognizerResult

Hasil detection yang dihasilkan oleh Presidio diproses dalam bentuk `RecognizerResult`.

Hasil tersebut menyediakan informasi yang diperlukan oleh tahap berikutnya untuk melakukan pemrosesan entitas lebih lanjut.

### Entity Processor

Entity Processor memproses output dari `RecognizerResult` dan mengubah entitas yang terdeteksi menjadi kategori internal yang telah distandarkan berdasarkan predefined medical rules.

Logika mapping yang digunakan adalah:

- `PERSON` → dikonversi menjadi `PATIENT` atau `DOCTOR` berdasarkan contextual role inference
- `LOCATION`, `LOC`, `FAC`, `GPE` → dikonversi menjadi `ADDRESS`
- `CONTEXT` → apabila teks yang terdeteksi merepresentasikan kondisi medis atau nama penyakit, nilai asli dipertahankan tanpa dilakukan anonymization

Tahap ini memastikan bahwa output NLP yang masih bersifat umum dapat diubah menjadi healthcare entity yang sesuai dengan domain, sekaligus mempertahankan konteks medis yang relevan.

### Resolver

Resolver memproses dan merekonsiliasi informasi entitas yang berasal dari beberapa sumber detection, yaitu Regex dan `RecognizerResult` + Entity Processor, kemudian menentukan entitas final sebelum masuk ke tahap normalization.

Logika pengambilan keputusan adalah:

- **Regex vs RecognizerResult conflict** → entitas dari Regex memiliki prioritas
- **RecognizerResult vs Entity Processor conflict** → output Entity Processor memiliki prioritas
- **Final fallback condition** → apabila tidak terdapat aturan conflict resolution yang berlaku, sistem menggunakan `RecognizerResult` asli

```text
                RecognizerResult
                        |
                        v
                Entity Processor
                        |
                        v
                    Resolver
```

### Normalizer

Normalizer melakukan standardisasi terhadap informasi entitas yang telah diselesaikan oleh Resolver sebelum masuk ke tahap pseudonymization.

```text
                     Resolver
                        |
                        v
                   Normalizer
                        |
                        v
                Pseudonymization
```

Tahap ini memastikan informasi entitas telah dipersiapkan secara konsisten sebelum menghasilkan representasi pseudonymous.

---

### Pseudonymization Layer

Entitas sensitif yang telah terdeteksi diubah menjadi nilai pseudonymous sehingga nilai aslinya tidak langsung terekspos.

Contoh:

```text
John Doe        -> [PATIENT_001]
08123456789     -> [PHONE_001]
john@email.com  -> [EMAIL_001]
123456789       -> [ID_001]
```

Nilai yang telah dipseudonymize kemudian diteruskan ke `redact_service`.

```text
                Detected Entity
                        |
                        v
                Pseudonymization
                        |
                        v
                redact_service
```

Proses pseudonymization mempertahankan kemampuan untuk melakukan restoration terhadap nilai yang telah dimapping melalui mapping service dan restore service.

---

### Redact Service

`redact_service` bertanggung jawab menangani proses redaction akhir setelah entity detection, processing, resolution, normalization, dan pseudonymization selesai dilakukan.

Service ini menyediakan dua jalur pemrosesan:

```text
                    redact_service
                    /             \
                   /               \
                  v                 v
              Metric          mapping_service
                                   |
                                   v
                                Redis
```

#### Metric Path

Komponen Metric mencatat informasi yang berkaitan dengan proses redaction, termasuk:

- Waktu pemrosesan redaction
- Waktu pemrosesan detection
- Informasi PII/PHI yang terdeteksi
- Informasi pemrosesan response

Hal ini memungkinkan sistem untuk mengukur dan mengevaluasi performa pipeline redaction.

#### Mapping Path

Mapping path mengirim mapping entitas yang telah dipseudonymize ke `mapping_service`.

```text
                Pseudonymized Entity
                        |
                        v
                mapping_service
                        |
                        v
                      Redis
```

---

### Redis Mapping Layer

Redis digunakan sebagai persistent mapping storage untuk kebutuhan pseudonymization dan restoration.

Mapping service menyimpan hubungan antara key/token yang dihasilkan dengan nilai aslinya.

Secara konseptual:

```text
                    KEY / TOKEN
                        |
                        v
                Original Value
```

Mapping service bertanggung jawab untuk menyimpan dan mengambil mapping tersebut.

Proses mapping adalah:

```text
                redact_service
                        |
                        v
                mapping_service
                        |
                        v
                    SAVE KEYS
                        |
                        v
                      Redis
```

Pada proses restoration, mapping service mengambil key yang diperlukan:

```text
                    Front-End
                        |
                        v
                mapping_service
                        |
                        v
                     GET KEYS
                        |
                        v
                      Redis
```

---

### Flow Reverse Mapping

Reverse Mapping merupakan proses untuk mengambil kembali nilai asli berdasarkan pseudonymized key/token yang diterima dari Front-End.

Berbeda dengan Redact Flow yang membuat dan menyimpan mapping, Reverse Mapping menggunakan mapping yang sudah tersedia di Redis untuk melakukan lookup terhadap nilai asli.

Alur Reverse Mapping adalah:

```text
                    Input (Front-End)
                           |
                           v
                   mapping_service
                  (GET KEY / TOKEN)
                           |
                           v
                     Redis Lookup
                           |
                           v
                    Reverse Mapping
                           |
                           v
                    restore_service
                           |
                           v
                         Metric
             (Processing Time & PII/PHI Detection)
                           |
                           v
                        Response
```

Proses Reverse Mapping dimulai ketika Front-End mengirim pseudonymized key/token.

`mapping_service` menerima key/token tersebut dan melakukan lookup ke Redis untuk mendapatkan nilai asli yang sebelumnya disimpan pada saat Redact Flow.

Contoh:

```text
                    Input
               [PATIENT_001]
                       |
                       v
               mapping_service
                       |
                       v
                 Redis Lookup
                       |
                       v
          [PATIENT_001] -> "John Doe"
                       |
                       v
              Reverse Mapping
                       |
                       v
               restore_service
                       |
                       v
               Output: John Doe
```

Dengan demikian, alur hubungan antara Redact Flow dan Reverse Mapping adalah:

```text
                    REDACT FLOW
                         |
                         v
                Pseudonymization
                         |
                         v
                   mapping_service
                  (SAVE KEY / TOKEN)
                         |
                         v
                       Redis
                         |
                         |
                    Stored Mapping
                         |
                         |
                         v
              REVERSE MAPPING FLOW
                         |
                         v
                  mapping_service
                  (GET KEY/TOKEN)
                         |
                         v
                  Redis Lookup
                         |
                         v
                 Original Value
                         |
                         v
                 restore_service
                         |
                         v
                      Response
```

Dalam desain ini, `mapping_service` bertanggung jawab untuk menyimpan token mapping selama Redact Flow dan mengambilnya kembali selama Reverse Mapping Flow, sehingga terdapat hubungan satu-ke-satu yang konsisten antara pseudonymized token dan nilai PHI/PII aslinya.

Pada implementasi ini, Reverse Mapping tidak membutuhkan integrasi LLM. Reverse Mapping merupakan mekanisme direct mapping lookup yang mengambil nilai asli berdasarkan pseudonymized key/token.

### Metrics

Metrics terintegrasi pada workflow redaction maupun restoration.

Untuk proses redaction:

```text
                redact_service
                        |
                        v
                      Metric
```

Untuk proses restoration:

```text
                mapping_service
                        |
                        v
                restore_service
                        |
                        v
                     Metric
```

Sistem Metric digunakan untuk mengukur:

- Waktu pemrosesan
- Detection processing
- Informasi deteksi PII/PHI
- Response processing

Pengukuran tersebut mendukung validasi sistem dan evaluasi performa pipeline.

---

## 3. Deployment Docker

Project menyediakan konfigurasi Docker untuk menjalankan aplikasi dan Redis di dalam container.

Build application image:

```bash
docker build -t privacy-shield-llm:latest .
```

Jalankan application container sesuai dengan konfigurasi Docker pada project.

Untuk service Redis, Docker Compose telah disediakan.

---

## 4. Setup Redis

Redis digunakan sebagai mapping storage untuk kebutuhan pseudonymization dan restoration.

### Menjalankan Redis

```bash
docker compose up -d redis
```

### Memeriksa Container

```bash
docker compose ps
```

### Melihat Log Redis

```bash
docker compose logs -f redis
```

### Menguji Koneksi Redis

```bash
docker exec -it privacy-shield-redis redis-cli ping
```

Hasil yang diharapkan:

```text
PONG
```

### Menghentikan Redis

```bash
docker compose stop redis
```

### Menghapus Container Redis

```bash
docker compose down
```

Data Redis disimpan di dalam Docker volume `redis_data`.

---

## 5. Konfigurasi Environment

Nilai konfigurasi sensitif dimuat melalui environment variables.

Contoh:

```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
```

Untuk eksekusi menggunakan container, environment variables dapat diberikan melalui Docker Compose.

> **Catatan Keamanan:** Jangan melakukan commit file `.env` asli atau credentials ke repository.

Gunakan `.env.example` ketika membagikan struktur konfigurasi yang diperlukan.

---

## 6. Struktur Project

Struktur project secara sederhana adalah:

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

Struktur implementasi dapat berkembang seiring dengan perkembangan project.

---

## 7. Pertimbangan Keamanan

Pipeline dirancang dengan pendekatan meminimalkan exposure terhadap PHI/PII sensitif selama proses pemrosesan teks klinis.

Pertimbangan keamanan utama meliputi:

- Mendeteksi PHI/PII sebelum data sensitif diproses lebih lanjut.
- Menggunakan Regex untuk structured PII detection.
- Menggunakan NLP-based recognition untuk contextual entities.
- Memproses entity yang terdeteksi melalui dedicated entity-processing stages.
- Menggunakan pseudonymous token sebagai pengganti nilai sensitif secara langsung.
- Menyimpan mapping information secara terpisah di Redis.
- Membatasi akses terhadap Redis credentials melalui environment variables.
- Tidak melakukan commit file `.env` yang berisi secrets.
- Melakukan validasi terhadap input dan output data.
- Menguji duplicate entities untuk memastikan konsistensi mapping.
- Menguji unknown token dan missing mapping secara aman.
- Mengukur waktu pemrosesan redaction dan restoration.
- Mempertimbangkan Redis persistence, access control, network isolation, dan credential protection pada production.
- Tidak mengekspos PHI/PII asli di source code, documentation, testing data, screenshots, atau repository commits.

---

## 8. Threat Model

Analisis keamanan project didokumentasikan secara terpisah.

- [Threat Model — Indonesian](Threat-model-ID.md)

Threat model berfokus pada risiko keamanan yang relevan terhadap pipeline redaction PHI/PII HealthTech, termasuk:

- Sensitive-data exposure
- Unauthorized mapping access
- PHI/PII detection bypass
- Incorrect entity classification
- Mapping security
- Redis security
- Data restoration risks
- Pipeline integrity
- Sensitive-data leakage melalui logs atau documentation

---

## 9. Dokumentasi

Dokumentasi tambahan project dikelola secara terpisah dari README utama.

Dokumentasi penting meliputi:

- Threat Model — Indonesian
- System Validation & Performance Testing — Indonesian
- Development and learning notes

Dokumentasi mencakup architecture, security considerations, testing, performance measurements, dan development process project.

---

## 10. Informasi Project

**Project:** HealthTech — Automated PHI/PII Redaction Pipeline

**Repository:** `privacy-shield-llm`

**Technology:** Python, FastAPI, Regex, Microsoft Presidio, Redis, Docker

**Core Components:** Regex Detection, Presidio, RecognizerResult, Entity Processor, Resolver, Normalizer, Pseudonymization, Redact Service, Mapping Service, Restore Service, dan Metrics

**Purpose:** Mendeteksi, melakukan pseudonymization, redaction, mapping, dan restoration terhadap PHI/PII sensitif melalui security pipeline yang terstruktur dan terukur.

---

## 11. Jadwal Pengembangan

### Persiapan Bootcamp

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

---

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

---

### Week 3 — NLP Detection

**July 27 – August 2, 2026**

| Tanggal   | Aktivitas                                                   | Commit                                                                            |
| --------- | ----------------------------------------------------------- | --------------------------------------------------------------------------------- |
| July 27   | Day 15 - NLP & NER Research                                 | `docs: add NLP and named entity recognition learning notes`                       |
| July 28   | Day 16 - spaCy Integration                                  | `feat: integrate spaCy named entity recognition`                                  |
| July 29   | Day 17 - Microsoft Presidio Integration                     | `feat: integrate Microsoft Presidio analyzer engine`                              |
| July 30   | Day 18 - Person Entity Detection                            | `feat: implement patient and doctor name detection`                               |
| July 31   | Day 19 - Address Entity Detection                           | `feat: implement address and location entity detection`                           |
| August 01 | Day 20 - Context-Aware Detection                            | `feat: improve contextual entity recognition for medical terms`                   |
| August 02 | Day 21 - NLP Pipeline Integration & Documentation in Week 3 | `feat: integrate NLP detection into redaction pipeline & documentation in week 3` |

---

### Week 4 — Integration & Deployment

**August 3 – August 9, 2026**

| Tanggal   | Aktivitas                                                                   | Commit                                                                  |
| --------- | --------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| August 03 | Day 22 - Pseudonymization Engine                                            | `feat: implement pseudonymization engine for sensitive entities`        |
| August 04 | Day 23 - Redis Token Mapping Service                                        | `feat: implement Redis-based token mapping service`                     |
| August 05 | Day 24 - Restore Mapping Integration                                        | `feat: integrate mapping retrieval into restore pipeline`               |
| August 06 | Day 25 - System Validation & Performance Testing                            | `test: validate end-to-end pipeline performance and restore processing` |
| August 07 | Day 26 - Threat Modeling & Security Analysis for PHI/PII Redaction Pipeline | `docs: add HealthTech PII threat modeling`                              |
| August 08 | Day 27 - Project Documentation, Architecture & Security Report              | `docs: finalize project documentation`                                  |
| August 09 | Day 28 - Documentation in Week 4                                            | `docs: documentation in Week 4`                                         |

---

## 12. Testing

Dokumentasi testing dikelola secara terpisah untuk versi English dan Indonesian.

- [System Validation & Performance Testing — Indonesian](System%20Validation%20%26%20Performance%20Testing-ID.md)

Testing mencakup:

- Regex detection validation
- Presidio entity detection
- RecognizerResult processing
- Entity Processor validation
- Resolver validation
- Normalizer validation
- Pseudonymization validation
- Duplicate entity mapping
- Clinical input testing
- Redaction processing time
- PII/PHI detection metrics
- Mapping service validation
- Redis mapping behavior
- Mapping key retrieval
- Restore processing
- Unknown tokens
- Missing mappings
- Empty input
- Response validation
- End-to-end redaction dan restoration workflow

---

## 🔐 Security Features

- PHI/PII detection
- Regex-based structured detection
- NLP-based contextual entity detection
- Patient and doctor name detection
- Address and location detection
- Context-aware medical entity detection
- Pseudonymization
- Redis-based token mapping
- Reverse mapping
- Docker containerization
- CI/CD automation
- Threat modeling
- System validation and performance testing

---

## 📦 Project Deliverables

- FastAPI backend
- Front-End interface
- Regex detection modules
- Email detection
- Phone detection
- Date detection
- ID detection
- Microsoft Presidio integration
- RecognizerResult processing
- Entity Processor
- Resolver
- Normalizer
- Pseudonymization engine
- Redact Service
- Mapping Service
- Redis token/key mapping
- Restore Service
- Metrics and processing-time measurement
- Docker configuration
- Docker Compose configuration
- GitHub Actions CI/CD
- Docker Hub image
- Threat Model
- Architecture documentation
- Testing documentation
- Security report

---

## 🔮 Future Improvements

- Advanced contextual PHI/PII detection
- Improved entity resolution
- Improved entity normalization
- More comprehensive PHI/PII recognizers
- Advanced pseudonymization strategies
- Mapping expiration policies
- Redis security hardening
- Role-Based Access Control (RBAC)
- Audit logging
- Advanced performance monitoring
- Monitoring and alerting
- Kubernetes deployment
- Cloud deployment
- Additional security validation and compliance analysis

---

## 👥 Contributors

| Member   | Responsibility                          |
| -------- | --------------------------------------- |
| Member 1 | FastAPI & API Layer                     |
| Member 2 | Regex Detection                         |
| Member 3 | NLP Detection                           |
| Member 4 | Token Mapping, Integration & Deployment |

---

# License

Project ini dikembangkan untuk **tujuan edukasi** sebagai bagian dari **Infotact Technical Internship Program — Advanced Cybersecurity Project**.

Project ditujukan untuk kebutuhan edukasi, development, testing, dan demonstrasi cybersecurity engineering.

Implementasi berfokus pada perlindungan PHI/PII dalam HealthTech melalui detection, pseudonymization, mapping, redaction, restoration, dan performance measurement.

**Project:** `privacy-shield-llm`

**Project:** HealthTech — Automated PHI/PII Redaction Pipeline

**Version:** `V0.19.9`

Copyright © 2026.

Project ini tidak dimaksudkan untuk dianggap sebagai software medical, privacy, compliance, atau security yang siap digunakan pada production tanpa security assessment, testing, validation, dan compliance review yang sesuai.
