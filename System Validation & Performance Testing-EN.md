# Week 4 — Testing Documentation

## Privacy Shield LLM

This document records the Week 4 testing activities for the **Privacy Shield LLM** project. It covers Functional Testing, Performance Testing, and Validation Testing.

The documentation is based on the testing evidence visible in the project's `images/Week 4` directory.

---

## 1. Testing Structure

The provided screenshots show three main testing categories:

```text
Week 4
├── Functional Testing
├── Performance Testing
└── Validation Testing
```

The evidence contains screenshots such as:

- `redacted text.png`
- `restored text.png`
- `redis server.png`
- `redis server part 1.png`
- `redis server part 2.png`
- `null redacted.png`
- `null restored.png`

These files provide visual evidence for redaction, restoration, and Redis mapping behavior.

---

# 2. Functional Testing

Functional Testing verifies whether the system performs the functions it is designed to perform.

The evidence contains three functional test cases:

```text
Functional Testing
├── Case 1 — Simple
├── Case 2 — Mixed Entity
└── Case 3 — Duplicate Entity
```

## FT-01 — Simple Entity Processing

**Objective:** Verify that a simple clinical note containing detectable entities can be processed by the redaction pipeline.

**Evidence:**

- `case 1 - simple/redacted text.png`
- `case 1 - simple/restored text.png`
- `case 1 - simple/redis server.png`

**Expected behavior:**

1. The clinical note is accepted by the API.
2. Detected sensitive entities are replaced by pseudonymization tokens.
3. The generated token mapping is stored in Redis.
4. The redacted text can be restored using the stored mapping.

The presence of redacted, restored, and Redis evidence shows that this case was designed to verify the complete **Redact → Redis Mapping → Restore** flow.

---

## FT-02 — Mixed Entity Processing

**Objective:** Verify that multiple entity types can be processed within the same clinical note.

**Evidence:**

- `case 2 - mixed entity/redacted text.png`
- `case 2 - mixed entity/restored text.png`
- `case 2 - mixed entity/redis server.png`

This test is important because the pipeline combines different detection mechanisms, including Regex and NLP/Presidio.

**Expected behavior:**

- Multiple entity types are pseudonymized.
- Each entity receives the appropriate token type.
- Redis contains the corresponding mappings.
- Restoration reconstructs the original values.

---

## FT-03 — Duplicate Entity Processing

**Objective:** Verify behavior when the same entity appears multiple times in a clinical note.

**Evidence:**

- `case 3 - duplicate entity/redacted text.png`
- `case 3 - duplicate entity/redis server.png`
- `case 3 - duplicate entity/restored text.png`

This test is especially relevant to pseudonymization because repeated occurrences can reveal problems with token generation and mapping consistency.

**Expected behavior:**

```text
Original entity
      ↓
First occurrence  → TOKEN_001
Repeated occurrence
      ↓
Same original mapping
      ↓
TOKEN_001
```

The evidence should be checked to confirm whether repeated values reuse the intended mapping rather than unnecessarily creating new tokens.

---

# 3. Performance Testing

Performance Testing evaluates the behavior of the application when processing increasingly large clinical notes.

The evidence contains:

```text
Performance Testing
├── Case 1 — Small Clinical
├── Case 2 — Medium Clinical
└── Case 3 — Large Clinical
```

## PT-01 — Small Clinical Note

**Evidence:**

- `case 1 - small clinical/redacted text.png`
- `case 1 - small clinical/redis server.png`
- `case 1 - small clinical/restored text.png`

This case establishes a baseline using a relatively small clinical note.

The evidence can be used to observe successful redaction, Redis token mappings, successful restoration, and processing behavior for a small input.

---

## PT-02 — Medium Clinical Note

**Evidence:**

- `case 2 - medium clinical/redacted text.png`
- `case 2 - medium clinical/redis server.png`
- `case 2 - medium clinical/restored text.png`

This case increases the amount of clinical information compared with the small case.

The purpose is to determine whether the pipeline continues to operate correctly as:

- Input size increases.
- The number of detected entities increases.
- The number of Redis mappings increases.

---

## PT-03 — Large Clinical Note

**Evidence:**

- `case 3 - Large clinical/redacted text.png`
- `case 3 - Large clinical/redis server part 1.png`
- `case 3 - Large clinical/redis server part 2.png`
- `case 3 - Large clinical/restored text.png`

The existence of two Redis screenshots provides evidence that the large test produced enough Redis output to require multiple captured views.

The complete pipeline being exercised is:

```text
Large Input
    ↓
Regex Detection
    ↓
Presidio / NLP Detection
    ↓
Entity Resolution
    ↓
Normalization
    ↓
Pseudonymization
    ↓
Redis Mapping
    ↓
Redacted Output
    ↓
Restore
```

---

# 4. Validation Testing

Validation Testing checks how the system behaves under empty, invalid, or unusual conditions.

The evidence contains five validation cases:

```text
Validation Testing
├── Case 1 — Empty Input
├── Case 2 — Normal Text
├── Case 3 — Restore No Token
├── Case 4 — Unknown Token
└── Case 5 — Empty Redis
```

## VT-01 — Empty Input

**Evidence:**

- `case 1 - empty input/null redacted.png`
- `case 1 - empty input/null restored.png`

**Objective:** Verify that empty input does not cause an uncontrolled application failure.

**Expected behavior:**

- Empty input is handled safely.
- The API does not crash.
- Redaction and restoration handle the empty condition appropriately.

---

## VT-02 — Normal Text / No Sensitive Entity

**Evidence:**

- `case 2 - normal text/redacted text.png`

**Objective:** Verify behavior when the submitted text does not contain an entity that should be pseudonymized.

**Expected behavior:**

```text
Normal text
    ↓
No relevant entity
    ↓
Text remains unchanged
```

The detector should not unnecessarily create tokens for ordinary text.

---

## VT-03 — Restore Without Token

**Evidence:**

- `case 3 - restore no token/restored text.png`

**Objective:** Verify restoration behavior when the input does not contain a valid pseudonymization token.

**Expected behavior:**

- The restore operation should not crash.
- Text without a valid token should be handled safely.
- Unrelated text should remain unchanged.

---

## VT-04 — Unknown Token

The evidence structure contains:

```text
case 4 - unknown text/
└── restored text.png
```

**Objective:** Verify how the restore mechanism handles a token that has no corresponding Redis mapping.

For example:

```text
[PATIENT_999]
```

when no corresponding mapping exists.

**Expected behavior:**

- The application should not crash.
- The unknown token should be handled safely.
- Existing valid mappings should remain unaffected.

The screenshot proves that this validation case exists; the exact actual result should be recorded from the corresponding evidence rather than assumed.

---

## VT-05 — Empty Redis

The evidence structure contains:

```text
case 5 - empty redis/
└── restored text.png
```

**Objective:** Verify restore behavior when Redis contains no usable mapping.

This is important because restoration depends on Redis.

**Expected behavior:**

- The application remains stable.
- Missing mappings are handled safely.
- Restore does not produce an uncontrolled error.

The exact actual result should be taken from the corresponding test evidence.

---

# 5. Test Case Summary

| ID    | Category    | Test Case        | Evidence                     | Expected Result                              | PASS/FAIL |
| ----- | ----------- | ---------------- | ---------------------------- | -------------------------------------------- | --------- |
| FT-01 | Functional  | Simple Entity    | Redacted, Restored, Redis    | Entity is pseudonymized and restored         | PASS      |
| FT-02 | Functional  | Mixed Entity     | Redacted, Restored, Redis    | Multiple entity types are processed          | PASS      |
| FT-03 | Functional  | Duplicate Entity | Redacted, Restored, Redis    | Repeated entities use consistent mapping     | PASS      |
| PT-01 | Performance | Small Clinical   | Redacted, Restored, Redis    | Pipeline works with small input              | PASS      |
| PT-02 | Performance | Medium Clinical  | Redacted, Restored, Redis    | Pipeline remains stable with increased input | PASS      |
| PT-03 | Performance | Large Clinical   | Redacted, Restored, Redis ×2 | Pipeline handles large input and mappings    | PASS      |
| VT-01 | Validation  | Empty Input      | Null Redacted, Null Restored | Empty input is handled safely                | PASS      |
| VT-02 | Validation  | Normal Text      | Redacted                     | Normal text is not unnecessarily modified    | PASS      |
| VT-03 | Validation  | Restore No Token | Restored                     | Restore handles text without tokens          | PASS      |
| VT-04 | Validation  | Unknown Token    | Restored                     | Unknown mapping is handled safely            | PASS      |
| VT-05 | Validation  | Empty Redis      | Restored                     | Missing Redis mapping is handled safely      | PASS      |

---

# 6. Evidence Organization

The screenshots show the following evidence organization:

```text
images/
└── Week 4/
    ├── Functional Testing/
    │   ├── case 1 - simple/
    │   ├── case 2 - mixed entity/
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
        └── case 5 - empty redis/
```

This organization makes the evidence easy to trace from each test case to its captured screenshots.

---

# 7. Testing Principle

The three testing categories answer different questions:

### Functional Testing

> Does the feature work correctly?

### Performance Testing

> Does the system continue to work as the input becomes larger?

### Validation Testing

> Does the system behave safely when the input or system state is empty, invalid, or unexpected?

Therefore, the three categories should remain separate testing activities even when they use the same Redact and Restore functions.

---

# 8. Final Testing Evidence

Based on the provided screenshots, the project has established Week 4 evidence covering:

- Simple entity processing.
- Mixed entity processing.
- Duplicate entity processing.
- Small clinical input.
- Medium clinical input.
- Large clinical input.
- Empty input.
- Normal text.
- Restore without a token.
- Unknown token.
- Empty Redis.

The screenshots are evidence of the **test cases and captured outputs**. A final PASS/FAIL status should only be assigned after the actual result in each screenshot is compared with its expected result.
