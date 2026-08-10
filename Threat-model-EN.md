# Threat Model --- HealthTech: Automated PHI/PII Redaction Pipeline for LLMs

**Project:** HealthTech - Automated PHI/PII Redaction Pipeline for LLMs\
**System:** Privacy Shield LLM\
**Scope:** Redaction, pseudonymization, Redis token mapping,
restoration, API, file input, logging, and downstream LLM boundary.

------------------------------------------------------------------------

## 1. Objective

This threat model identifies the assets, threat actors, trust
boundaries, attack surfaces, security threats, and mitigations relevant
to Privacy Shield LLM.

The primary security objective is:

> **Prevent unauthorized disclosure of PHI/PII while allowing authorized
> redaction and controlled restoration.**

The analysis is based on the implemented architecture:

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

The restore path is:

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

## 2. Protected Assets

  ---------------------------------------------------------------------------------------
  ID                Asset              Example                          Sensitivity
  ----------------- ------------------ -------------------------------- -----------------
  A-01              Patient Name       `John Anderson`                  Critical

  A-02              Doctor Name        `Michael Johnson`                High

  A-03              Address            `25 Main Street, Boston`         Critical

  A-04              Email              `john@gmail.com`                 High

  A-05              Phone              `+1 212-555-0187`                High

  A-06              Patient/Medical ID `PAT-20260715`, `MRN-20260715`   Critical

  A-07              Clinical Text      Patient medical record           Critical

  A-08              Pseudonymization   `[PATIENT_001]`                  High
                    Token                                               

  A-09              Token Mapping      `PATIENT_001 -> John Anderson`   Critical

  A-10              Redis Mapping Data Original/token mappings          Critical

  A-11              API Requests       Redact/restore requests          High

  A-12              Application Logs   Processing/activity information  High

  A-13              Metrics            Entity count/processing duration Medium
  ---------------------------------------------------------------------------------------

### Critical Asset: Token Mapping

The most sensitive asset is the relationship between a token and its
original value:

``` text
PATIENT_001 -> John Anderson
```

The redacted token alone does not directly expose the patient's name:

``` text
[PATIENT_001]
```

However, access to the mapping makes pseudonymization reversible.
Therefore, Redis and the Mapping Service are high-value security
components.

------------------------------------------------------------------------

## 3. Threat Actors

### TA-01 --- External Attacker

Attempts to interact with the API without authorization.

Potential goals:

-   submit malicious input;
-   exhaust resources;
-   abuse endpoints;
-   obtain PHI/PII.

### TA-02 --- Unauthorized Application User

A user who can access the application but is not authorized to restore
protected data.

### TA-03 --- Compromised Host or Container

An attacker who obtains access to the Docker host, application
container, or Redis container.

Potential goals:

-   read Redis mappings;
-   obtain credentials;
-   inspect configuration;
-   extract stored data.

### TA-04 --- Malicious or Compromised Downstream Consumer

A downstream service or LLM integration that receives processed clinical
text.

### TA-05 --- Insider

A legitimate infrastructure/application user who intentionally accesses
sensitive mappings or logs.

------------------------------------------------------------------------

## 4. Trust Boundaries

### TB-01 --- User ↔ Front-End

**Risk:** malicious input, unauthorized use, accidental sensitive-data
submission.

### TB-02 --- Front-End ↔ FastAPI

**Risk:** request manipulation, unauthorized API access, excessive
requests, endpoint abuse.

### TB-03 --- Application ↔ Redis

**Risk:** unauthorized access to reversible PHI/PII mappings.

This is the most critical storage boundary.

### TB-04 --- Redaction System ↔ Downstream LLM

**Risk:** PHI/PII missed by detection may cross the privacy boundary.

------------------------------------------------------------------------

## 5. Attack Surface

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

Primary attack surfaces:

1.  Redact API.
2.  Restore API.
3.  Clinical text input.
4.  `.txt` file upload.
5.  Redis.
6.  Token mappings.
7.  Application logs.
8.  Docker/container environment.
9.  Configuration and credentials.
10. Downstream LLM integration.

------------------------------------------------------------------------

## 6. Threat Matrix

  ---------------------------------------------------------------------------------------------------
  ID          Threat                     Component       STRIDE        Impact             Risk
  ----------- -------------------------- --------------- ------------- ------------------ -----------
  T-01        Redis mapping exposure     Redis           Information   PHI/PII disclosure Critical
                                                         Disclosure                       

  T-02        Unauthorized restore       Restore API     Elevation of  Original PHI/PII   Critical
                                                         Privilege /   recovery           
                                                         Information                      
                                                         Disclosure                       

  T-03        Detection failure          Regex /         Information   PHI/PII reaches    Critical
                                         Presidio / NLP  Disclosure    downstream         

  T-04        Malicious large input      API / NLP       Denial of     Resource           High
                                                         Service       exhaustion         

  T-05        Sensitive logging          Logs            Information   Secondary PHI/PII  High
                                                         Disclosure    exposure           

  T-06        Token mapping leakage      Pseudonymizer / Information   Pseudonymization   High
                                         Mapping Service Disclosure    reversal           

  T-07        Redis persistence exposure Redis / Storage Information   Historical mapping Critical
                                                         Disclosure    disclosure         

  T-08        False positive             Entity          Tampering /   Unnecessary data   Medium
                                         Processor       Integrity     modification       

  T-09        API endpoint abuse         FastAPI         Spoofing /    Unauthorized       High
                                                         Elevation of  processing         
                                                         Privilege                        

  T-10        File upload abuse          Front-End / API Denial of     Resource abuse     High
                                                         Service /                        
                                                         Tampering                        

  T-11        Credential/configuration   Docker /        Information   Infrastructure     Critical
              exposure                   Environment     Disclosure    compromise         

  T-12        Residual PHI/PII reaches   LLM boundary    Information   Sensitive-data     Critical
              LLM                                        Disclosure    disclosure         
  ---------------------------------------------------------------------------------------------------

------------------------------------------------------------------------

## 7. Detailed Threats

### T-01 --- Redis Mapping Exposure

**Scenario:** Redis contains mappings such as:

``` text
PATIENT_001 -> John Anderson
PATIENT_002 -> Sarah Williams
DOCTOR_001  -> Michael Johnson
ADDRESS_001 -> 25 Main Street
```

Unauthorized Redis access can reverse pseudonymization.

**Impact:** Critical.

**Existing architectural control:** The Front-End does not communicate
directly with Redis; the Mapping Service mediates mapping operations.

**Recommended controls:**

-   Redis authentication and authorization.
-   Internal-network isolation.
-   No public Redis exposure.
-   Credential protection.
-   Restricted administrative access.
-   Monitoring of unauthorized access.
-   Encryption where appropriate.

### T-02 --- Unauthorized Restore

The restore endpoint intentionally returns original values. An attacker
may submit:

``` text
[PATIENT_001]
[DOCTOR_001]
[ADDRESS_001]
```

and attempt to recover original PHI/PII.

**Impact:** Critical.

**Recommended controls:**

-   Strong authentication.
-   Authorization for restore.
-   User/session mapping isolation.
-   Audit logging.
-   Rate limiting.
-   Strict token validation.

### T-03 --- Detection Failure

A detector may fail to recognize an entity:

``` text
Patient John Anderson
```

If the name is missed, it may reach a downstream LLM.

**Impact:** Critical.

**Relevant controls:** Regex, Presidio, Patient Detector, Doctor
Detector, Address Detector, Resolver, and Normalizer.

**Recommended controls:**

-   Layered detection.
-   False-negative testing.
-   Unusual-format testing.
-   International phone/identifier testing.
-   Detection coverage monitoring.
-   Fail-safe handling for uncertain entities.

### T-04 --- Malicious Large Input

An attacker repeatedly submits large clinical documents, causing:

``` text
Regex -> Presidio -> NLP -> Resolver -> Normalizer -> Pseudonymizer -> Redis
```

to consume excessive CPU, memory, or processing time.

**Impact:** High.

**Recommended controls:**

-   Request/file-size limits.
-   Rate limiting.
-   Timeouts.
-   Concurrency limits.
-   Resource monitoring.
-   Rejection of excessively large requests.

### T-05 --- Sensitive Logging

The application may redact the response correctly while accidentally
logging original clinical data.

Unsafe example:

``` text
Patient John Anderson
john@gmail.com
+1 212-555-0187
```

**Impact:** High.

**Recommended controls:**

-   Never log raw clinical text.
-   Do not log original entity values.
-   Sanitize exception messages.
-   Restrict log access.
-   Define log retention.
-   Audit logging behavior.

### T-06 --- Token Mapping Leakage

Tokens such as:

``` text
[PATIENT_001]
[PATIENT_002]
```

become sensitive when combined with their mappings:

``` text
PATIENT_001 -> John Anderson
PATIENT_002 -> Sarah Williams
```

**Impact:** High.

> **Pseudonymization is a data-protection mechanism, not a replacement
> for access control.**

### T-07 --- Redis Persistence Exposure

Redis persistence files, backups, snapshots, or container volumes may
expose historical mappings.

**Impact:** Critical.

**Recommended controls:**

-   Protect Redis persistence.
-   Secure backups.
-   Restrict volume access.
-   Encrypt backups.
-   Define retention/deletion policies.
-   Restrict Docker-host access.

### T-08 --- False Positive

A normal value may incorrectly become:

``` text
[ADDRESS_001]
```

or another token.

**Impact:** Medium.

**Existing architectural control:** Resolver overlap/priority handling
and Normalizer grouping.

**Recommended controls:**

-   Precision/recall measurement.
-   More validation cases.
-   Confidence-threshold review.
-   Ambiguous-text testing.

### T-09 --- API Endpoint Abuse

Repeated or unauthorized calls to:

``` text
POST /redact
POST /restore
```

may cause unauthorized processing, resource exhaustion, or information
disclosure.

**Impact:** High.

**Recommended controls:**

-   Authentication.
-   Authorization.
-   Rate limiting.
-   Request validation.
-   Audit logging.
-   Secure CORS configuration.
-   HTTPS in deployment.

### T-10 --- File Upload Abuse

The `.txt` upload feature may be abused with extremely large, malformed,
or repeated files.

**Impact:** High.

**Recommended controls:**

-   Strict file validation.
-   File-size limits.
-   Timeouts.
-   Temporary-file cleanup.
-   Safe filename handling.
-   Rate limiting.

### T-11 --- Credential or Configuration Exposure

Redis credentials, API settings, or other secrets may be exposed through
source code, `.env`, Git history, Docker configuration, or logs.

**Impact:** Critical.

**Recommended controls:**

-   Environment variables or secret management.
-   `.gitignore` for local secrets.
-   Credential rotation.
-   No production secrets in Git.
-   Restricted container-environment access.
-   Git-history secret review.

### T-12 --- Residual PHI/PII Reaches the LLM

If detection fails:

``` text
Clinical Text
     |
     v
Redaction
     |
     X  <-- PHI/PII missed
     |
     v
LLM
```

**Impact:** Critical.

**Recommended controls:**

-   Treat redaction as a security boundary.
-   Layered detection.
-   Final-output validation.
-   Fail-safe handling for uncertain entities.
-   Data minimization.
-   Downstream-flow monitoring.

------------------------------------------------------------------------

## 8. Security Control Mapping

  Control                         Threats Addressed
  ------------------------------- -----------------------------------------
  Regex + Presidio + Custom NLP   T-03, T-08, T-12
  Resolver / priority handling    T-03, T-08
  Normalizer                      T-03, T-08
  Pseudonymization                T-03, T-06, T-12
  Mapping Service                 T-01, T-02, T-06
  Redis isolation                 T-01, T-07
  Input validation                T-04, T-10
  File validation                 T-10
  Metrics Service                 Monitoring and anomaly analysis support
  Response schemas                Controlled API responses
  Validation testing              T-03, T-08, T-09, T-10

------------------------------------------------------------------------

## 9. Abuse Cases

### Abuse Case 1 --- Direct Redis Access

``` text
Attacker
   |
   v
Redis
   |
   v
PATIENT_001 -> John Anderson
```

**Goal:** obtain original PHI/PII.

### Abuse Case 2 --- Restore Abuse

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
Original Patient Name
```

**Goal:** recover protected information without authorization.

### Abuse Case 3 --- Detection Bypass

``` text
Crafted PHI/PII format
          |
          v
Detector fails
          |
          v
Original information remains
```

**Goal:** bypass the redaction layer.

### Abuse Case 4 --- Resource Exhaustion

``` text
Attacker
   |
   v
Large / repeated requests
   |
   v
Regex + Presidio + NLP
   |
   v
CPU / Memory exhaustion
```

**Goal:** reduce service availability.

------------------------------------------------------------------------

## 10. Risk Prioritization

### Priority 1 --- Redis Mapping Protection

Redis contains reversible mappings and therefore represents the
highest-value storage component.

### Priority 2 --- Restore Authorization

Restore is intentionally capable of returning original PHI/PII.

### Priority 3 --- Detection Failure

Missed PHI/PII can cross the redaction boundary.

### Priority 4 --- API and Input Abuse

NLP processing can be computationally expensive.

### Priority 5 --- Logging and Backup Exposure

Sensitive information may leak outside the main processing pipeline.

------------------------------------------------------------------------

## 11. Residual Risk

The most important residual risk is **detection uncertainty**.

No regex, NER model, or rule-based detector can guarantee recognition of
every possible representation of PHI/PII.

``` text
Detection
    !=
Absolute Privacy Guarantee
```

Privacy Shield LLM should therefore be treated as a defense-in-depth
privacy layer rather than an absolute guarantee that every sensitive
value will always be detected.

------------------------------------------------------------------------

## 12. Security Recommendations

For production deployment:

1.  Authenticate and authorize `/redact` and `/restore`.
2.  Isolate Redis from public network access.
3.  Protect Redis credentials.
4.  Enforce request and file-size limits.
5.  Add API rate limiting.
6.  Avoid logging raw clinical text.
7.  Protect Redis persistence and backups.
8.  Validate final redacted output before downstream transmission.
9.  Isolate mappings by user/session when multiple users are supported.
10. Use HTTPS in deployment environments.
11. Rotate secrets and credentials.
12. Monitor security-relevant events.
13. Establish retention and deletion policies for sensitive mappings.
14. Continue false-negative and false-positive testing.

------------------------------------------------------------------------

## 13. Threat Model Conclusion

The most critical security relationship in Privacy Shield LLM is:

``` text
Pseudonymized Token
        |
        v
Token Mapping
        |
        v
Original PHI/PII
```

The architecture reduces direct exposure by transforming sensitive
information into tokens before downstream processing:

``` text
John Anderson
      |
      v
[PATIENT_001]
```

However:

``` text
PATIENT_001 -> John Anderson
```

must itself be protected as highly sensitive information.

The primary security areas are therefore:

-   Restore endpoint.
-   Redis mapping store.
-   Detection pipeline.
-   API input layer.
-   File upload layer.
-   Application logs.
-   Docker/configuration environment.
-   Downstream LLM boundary.

Security cannot depend on pseudonymization alone. The system requires
defense in depth across:

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
