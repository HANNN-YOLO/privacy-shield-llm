# privacy-shield-llm

An automated HealthTech security pipeline designed to detect, pseudonymize, redact, map, and restore Protected Health Information (PHI) and Personally Identifiable Information (PII) from clinical text through a structured and measurable processing pipeline.

The system combines rule-based detection, NLP-based entity recognition, entity processing, pseudonymization, Redis-based token mapping, restoration, and processing metrics to provide a secure and auditable PHI/PII protection workflow.

---

## 1. Project Overview

**privacy-shield-llm** is a HealthTech security pipeline designed to reduce the risk of exposing sensitive PHI/PII during clinical text processing.

The pipeline separates the processing workflow into several dedicated stages:

- FastAPI for the API layer
- Regex-based detection for structured PII
- Microsoft Presidio for NLP-based entity recognition
- RecognizerResult processing for detected entities
- Entity Processor for contextual PHI/PII classification
- Resolver for entity resolution
- Normalizer for entity normalization
- Pseudonymization for sensitive entities
- `redact_service` for the main redaction process
- `mapping_service` for token/key storage and retrieval
- Redis for persistent mapping storage
- `restore_service` for restoring mapped entities
- Metrics for processing-time and detection measurements
- Docker for containerized deployment
- Automated testing and CI/CD for validation

The system consists of two primary processing flows:

1. **Redact Flow**
2. **Restore Flow**

### Redact Flow

The redaction process starts from the Front-End and passes through structured detection, NLP recognition, entity processing, normalization, pseudonymization, and finally the redaction service.

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
                       / \
                      /   \
                     v     v
                Metric   mapping_service
                                |
                                v
                           Redis Storage
```

The `redact_service` acts as the central processing point after pseudonymization.

It produces two processing paths:

- **Metric Path** — records processing time, PII/PHI detection information, and response-related metrics.
- **Mapping Path** — sends generated keys/tokens to `mapping_service`, which stores the mapping in Redis.

### Restore Flow

The restore process retrieves the required mapping from Redis before restoring the pseudonymized entities.

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

The restore process uses the mapping stored by the redaction workflow to restore the corresponding values before returning the response.

---

## 2. System Overview

The system separates detection, entity processing, transformation, mapping, restoration, and metrics into dedicated components.

### Detection Layer

The detection layer identifies structured and contextual PHI/PII from incoming clinical text.

#### Regex Detection

Regular expressions are used for structured identifiers such as:

- Email addresses
- Phone numbers
- Dates
- Identification numbers

The initial detection flow is:

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

Regex detection provides a deterministic first layer for structured PII.

#### Presidio Detection

After the Regex Detection stage, the text is processed by Microsoft Presidio for NLP-based entity recognition.

```text
                Clinical Text
                        |
                        v
                    Presidio
                        |
                        v
                RecognizerResult
```

Presidio is responsible for identifying contextual entities that cannot reliably be detected using simple regular expressions.

### RecognizerResult

The detection result generated by Presidio is processed as `RecognizerResult`.

These results provide the information required by the next stage of the pipeline for further entity processing.

### Entity Processor

The Entity Processor processes the output from `RecognizerResult` and converts detected entities into standardized internal categories based on predefined medical rules.

The mapping logic is as follows:

- `PERSON` → converted into `PATIENT` or `DOCTOR` depending on contextual role inference
- `LOCATION`, `LOC`, `FAC`, `GPE` → converted into `ADDRESS`
- `CONTEXT` → if the detected text represents a medical condition or disease name, the original value is preserved without anonymization

This stage ensures that raw NLP outputs are normalized into domain-specific healthcare entities while preserving medically relevant context.

### Resolver

The Resolver processes and reconciles entity information coming from multiple detection sources (Regex and RecognizerResult + Entity Processor) and determines the final entity selection before normalization.

The decision logic is defined as:

- **Regex vs RecognizerResult conflict** → Regex entity takes priority
- **RecognizerResult vs Entity Processor conflict** → Entity Processor output takes priority
- **Final fallback condition** → if no conflict resolution rule applies, the system defaults to the original `RecognizerResult`

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

The Normalizer standardizes the resolved entity information before it enters the pseudonymization stage.

```text
                     Resolver
                        |
                        v
                   Normalizer
                        |
                        v
                Pseudonymization
```

This ensures that the entity information is prepared consistently before generating pseudonymous representations.

---

### Pseudonymization Layer

Detected sensitive entities are transformed into pseudonymous values instead of exposing their original values directly.

Example:

```text
John Doe        -> [PATIENT_001]
08123456789     -> [PHONE_001]
john@email.com  -> [EMAIL_001]
123456789       -> [ID_001]
```

The pseudonymized values are then passed to the `redact_service`.

```text
                Detected Entity
                        |
                        v
                Pseudonymization
                        |
                        v
                redact_service
```

The pseudonymization process preserves the ability to restore mapped values through the dedicated mapping and restore services.

---

### Redact Service

The `redact_service` is responsible for handling the final redaction process after entity detection, processing, resolution, normalization, and pseudonymization.

The service provides two processing paths:

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

The Metric component records information related to the redaction process, including:

- Redaction processing time
- Detection processing time
- Detected PII/PHI information
- Response-related processing information

This allows the system to measure and evaluate the performance of the redaction pipeline.

#### Mapping Path

The mapping path sends pseudonymized entity mappings to the `mapping_service`.

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

Redis is used as the persistent mapping storage for pseudonymized entities.

The mapping service stores the relationship between generated keys/tokens and their corresponding values.

Conceptually:

```text
                    KEY / TOKEN
                        |
                        v
                Original Value
```

The mapping service is responsible for storing and retrieving these mappings.

The mapping process is:

```text
                redact_service
                        |
                        v
                mapping_service
                        |
                        v
                      Redis
```

During restoration, the mapping service retrieves the required keys:

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

Flow Reverse Mapping

The reverse mapping process accepts a pseudonymized key/token from the Front-End and performs a lookup through mapping_service, which is responsible for retrieving the original value from Redis based on the stored token mapping generated during the Redact Flow.

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

The Flow Reverse Mapping works by using the pseudonymized key/token as the lookup reference to retrieve the original value that was previously stored during the mapping stage in the Redact Flow.

For example:

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
        Output:John Doe
```

Thus, the flow of the relationship between Redact Flow and Reverse Mapping is:

```text
                    REDACT FLOW
                         |
                         v
                Pseudonymization
                         |
                         v
                mapping_service
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

In this design, mapping_service is responsible for storing token mappings during Redact Flow and retrieving them during Reverse Mapping Flow, ensuring a consistent one-to-one relationship between pseudonymized tokens and their original PHI/PII values.

In this implementation, Reverse Mapping does not require LLM integration. It is a direct mapping lookup mechanism that retrieves the original value associated with a pseudonymized key/token.

### Metrics

Metrics are integrated into both the redaction and restoration workflows.

For the redaction process:

```text
                redact_service
                        |
                        v
                      Metric
```

For the restoration process:

```text
                mapping_service
                        |
                        v
                restore_service
                        |
                        v
                     Metric
```

The metric system is used to measure:

- Processing time
- Detection processing
- PII/PHI detection information
- Response processing

These measurements support system validation and performance evaluation.

---

## 3. Docker Deployment

The project provides Docker configuration for running the application and Redis in containers.

Build the application image:

```bash
docker build -t privacy-shield-llm:latest .
```

Run the application container according to the project's Docker configuration.

For the Redis service, Docker Compose is provided.

---

## 4. Redis Setup

Redis is used as the mapping storage for pseudonymization and restoration.

### Start Redis

```bash
docker compose up -d redis
```

### Check the Container

```bash
docker compose ps
```

### View Redis Logs

```bash
docker compose logs -f redis
```

### Test the Redis Connection

```bash
docker exec -it privacy-shield-redis redis-cli ping
```

Expected result:

```text
PONG
```

### Stop Redis

```bash
docker compose stop redis
```

### Remove the Redis Container

```bash
docker compose down
```

The Redis data is stored in the `redis_data` Docker volume.

---

## 5. Environment Configuration

Sensitive configuration values are loaded through environment variables.

Example:

```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
```

For containerized execution, the environment variables can be supplied through Docker Compose.

> **Security Note:** Do not commit the real `.env` file or credentials to the repository.

Use `.env.example` when sharing the required configuration structure.

---

## 6. Project Structure

A simplified project structure is:

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

The exact implementation may evolve as the project progresses.

---

## 7. Security Considerations

The pipeline is designed around minimizing the exposure of sensitive PHI/PII during clinical text processing.

Key security considerations include:

- Detect PHI/PII before sensitive data is processed further.
- Use Regex for structured PII detection.
- Use NLP-based recognition for contextual entities.
- Process detected entities through dedicated entity-processing stages.
- Use pseudonymous tokens instead of directly exposing sensitive values.
- Store mapping information separately in Redis.
- Restrict access to Redis credentials through environment variables.
- Do not commit `.env` files containing secrets.
- Validate input and output data.
- Test duplicate entities to ensure mapping consistency.
- Test unknown tokens and missing mappings safely.
- Measure redaction and restoration processing time.
- Consider Redis persistence, access control, network isolation, and credential protection in production.
- Do not expose real PHI/PII in source code, documentation, testing data, screenshots, or repository commits.

---

## 8. Threat Model

The project's security analysis is documented separately.

- [Threat Model — English](Threat-model-EN.md)

The threat model focuses on security risks relevant to the HealthTech PHI/PII redaction pipeline, including:

- Sensitive-data exposure
- Unauthorized mapping access
- PHI/PII detection bypass
- Incorrect entity classification
- Mapping security
- Redis security
- Data restoration risks
- Pipeline integrity
- Sensitive-data leakage through logs or documentation

---

## 9. Documentation

Additional project documentation is maintained separately from the main README.

Important documentation includes:

- Threat Model — English
- System Validation & Performance Testing — English
- Development and learning notes

The documentation covers the architecture, security considerations, testing, performance measurements, and development process of the project.

---

## 10. Project Information

**Project:** HealthTech — Automated PHI/PII Redaction Pipeline

**Repository:** `privacy-shield-llm`

**Technology:** Python, FastAPI, Regex, Microsoft Presidio, Redis, Docker

**Core Components:** Regex Detection, Presidio, RecognizerResult, Entity Processor, Resolver, Normalizer, Pseudonymization, Redact Service, Mapping Service, Restore Service, and Metrics

**Purpose:** Detect, pseudonymize, redact, map, and restore sensitive PHI/PII through a structured and measurable security pipeline.

---

## 11. Development Schedule

### Bootcamp Preparation

| Date          | Activity          |
| ------------- | ----------------- |
| June 06, 2026 | On Boarding       |
| July 13, 2026 | Division of Tasks |

### Week 1 — FastAPI Server

**July 13 – July 20, 2026**

| Date    | Activity                                                                                         | Commit                                                                                  |
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

| Date    | Activity                                         | Commit                                                                                           |
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

| Date      | Activity                                                    | Commit                                                                            |
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

| Date      | Activity                                                                    | Commit                                                                  |
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

Testing documentation is maintained separately for the English and Indonesian versions.

- [System Validation & Performance Testing — English](System%20Validation%20%26%20Performance%20Testing-EN.md)

The testing scope includes:

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
- End-to-end redaction and restoration workflow

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

This project is developed for **educational purposes** as part of the **Infotact Technical Internship Program — Advanced Cybersecurity Project**.

The project is intended for educational, development, testing, and cybersecurity engineering demonstration purposes.

The implementation focuses on HealthTech PHI/PII protection through detection, pseudonymization, mapping, redaction, restoration, and performance measurement.

**Project:** `privacy-shield-llm`

**Project:** HealthTech — Automated PHI/PII Redaction Pipeline

**Version:** `V0.18.8`

Copyright © 2026.

This project is not intended to be considered production-ready medical, privacy, compliance, or security software without appropriate security assessment, testing, validation, and compliance review.
