# privacy-shield-llm

An automated HealthTech security pipeline that detects and redacts Protected Health Information (PHI) and Personally Identifiable Information (PII) before data is processed by Large Language Models (LLMs), enabling secure, privacy-preserving, and compliant AI applications.

## 1. Project Overview

**privacy-shield-llm** is a HealthTech security pipeline designed to reduce the risk of exposing sensitive PHI/PII to LLM-based applications.

The pipeline combines:

- FastAPI for the API layer
- Regex-based detection for structured PII
- spaCy and Microsoft Presidio for NLP-based entity detection
- Pseudonymization for sensitive entities
- Redis for token mapping and reverse mapping
- Docker for containerized deployment
- Automated testing and CI/CD for validation

The main processing flow is:

```text
Input Clinical Text
        |
        v
PII/PHI Detection
   |            |
 Regex          NLP
   |            |
   +-----+------+
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

## 2. System Overview

The system separates detection, transformation, mapping, and restoration into dedicated components.

### Detection Layer

Structured entities such as email addresses, phone numbers, dates, and IDs are detected using regular expressions.

NLP-based detection is used for contextual entities such as:

- Patient names
- Doctor names
- Organizations
- Addresses and locations
- Other context-dependent entities

### Pseudonymization Layer

Detected sensitive values can be replaced with stable tokens such as:

```text
John Doe       -> [PATIENT_001]
08123456789    -> [PHONE_001]
john@email.com -> [EMAIL_001]
```

### Redis Mapping Layer

Redis stores the relationship between original values and generated tokens so that the sanitized text can later be restored.

The mapping service supports:

```text
Original Entity -> Token
Token           -> Original Entity
```

### Reverse Mapping

After LLM processing, tokens in the response can be mapped back to their original values through Redis.

This keeps sensitive information separated from the LLM processing stage.

## 3. Docker Deployment

The project provides Docker configuration for running the application and Redis in containers.

Build the application image:

```bash
docker build -t privacy-shield-llm:latest .
```

Run the application container according to the project's Docker configuration.

For the Redis service, Docker Compose is provided.

## 4. Redis Setup

Redis is used as the persistent mapping store for pseudonymization and reverse mapping.

Start Redis:

```bash
docker compose up -d redis
```

Check the container:

```bash
docker compose ps
```

View Redis logs:

```bash
docker compose logs -f redis
```

Test the Redis connection:

```bash
docker exec -it privacy-shield-redis redis-cli ping
```

Expected result:

```text
PONG
```

Stop Redis:

```bash
docker compose stop redis
```

Remove the Redis container:

```bash
docker compose down
```

The Redis data is stored in the `redis_data` Docker volume.

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

Do not commit the real `.env` file or credentials to the repository.

Use `.env.example` when sharing the required configuration structure.

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

## 7. Security Considerations

The pipeline is designed around the principle of minimizing sensitive data exposure before LLM processing.

Key security considerations include:

- Detect PHI/PII before sending data to an LLM.
- Keep original sensitive values outside the LLM-facing text whenever possible.
- Use pseudonymous tokens instead of raw sensitive values.
- Store token mappings in Redis rather than exposing the mapping to the LLM.
- Protect Redis credentials through environment variables.
- Do not commit `.env` files containing secrets.
- Validate input and output data.
- Test duplicate entities to ensure mapping consistency.
- Test unknown tokens and missing mappings safely.
- Consider Redis persistence, access control, network isolation, and credential protection in production.

## 8. Threat Model

The project's security analysis is documented separately.

- [Threat Model — English](Threat-model-EN.md)

The threat model focuses specifically on security risks relevant to the HealthTech PHI/PII redaction pipeline, including sensitive-data exposure, unauthorized mapping access, LLM-related risks, Redis security, and pipeline integrity.

## 9. Documentation

Additional project documentation is maintained separately from the main README.

Important documentation includes:

- Threat Model — English
- System Validation & Performance Testing — English
- Development and learning notes

## 10. Project Information

**Project:** HealthTech — Automated PHI/PII Redaction Pipeline for LLMs

**Repository:** `privacy-shield-llm`

**Technology:** Python, FastAPI, spaCy, Microsoft Presidio, Redis, Docker

**Purpose:** Protect sensitive HealthTech data before it is processed by LLM-based applications.

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

### Week 4 — Integration & Deployment

**August 3 – August 9, 2026**

| Date      | Activity                                                                    | Commit                                                               |
| --------- | --------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| August 03 | Day 22 - Pseudonymization Engine                                            | `feat: implement pseudonymization engine for sensitive entities`     |
| August 04 | Day 23 - Redis Token Mapping Service                                        | `feat: implement Redis-based token mapping service`                  |
| August 05 | Day 24 - Reverse Mapping Integration                                        | `feat: integrate reverse mapping into LLM response pipeline`         |
| August 06 | Day 25 - System Validation & Performance Testing                            | `test: validate end-to-end pipeline performance and reverse mapping` |
| August 07 | Day 26 - Threat Modeling & Security Analysis for PHI/PII Redaction Pipeline | `docs: add HealthTech PII threat modeling`                           |
| August 08 | Day 27 - Project Documentation, Architecture & Security Report              | `docs: finalize project documentation`                               |
| August 09 | Day 28 - Documentation in Week 4                                            | `docs: documentation in Week 4`                                      |

## 12. Testing

Testing documentation is maintained separately for the English and Indonesian versions.

- [System Validation & Performance Testing — English](System%20Validation%20%26%20Performance%20Testing-EN.md)

The testing scope includes functional validation, duplicate entity mapping, clinical input testing, performance testing, reverse mapping, unknown tokens, empty input, and Redis mapping behavior.

---

**Project:** privacy-shield-llm  
**HealthTech Security Pipeline — PHI/PII Protection for LLM Applications V0.18.4**
