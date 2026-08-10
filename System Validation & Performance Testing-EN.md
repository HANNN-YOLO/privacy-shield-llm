# Privacy Shield LLM Testing Documentation

## 1. Testing Objectives

This documentation contains the testing results for **Privacy Shield LLM**, specifically covering the following processes:

- sensitive data detection;
- sensitive data redaction;
- token mapping storage in Redis;
- original data restoration;
- invalid input handling;
- testing with various levels of clinical data complexity;
- system performance measurement.

The testing was conducted to ensure that the system is not only capable of performing data redaction, but also able to maintain the relationship between **original data → token → original data** throughout the restoration process.

---

# 2. Testing Evidence Structure

Testing evidence is stored in the following directory:

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

This documentation uses the images within this structure as visual evidence of the testing results.

---

# 3. Functional Testing

## 3.1 Case 1 — Simple Text

### Objective

To ensure that the system can process simple clinical text containing several types of sensitive data.

### Scenario

The input text contains data such as:

- patient name;
- doctor name;
- date;
- address;
- email address;
- phone number;
- patient identification number.

### Expected Results

The system should:

1. accept the input text;
2. detect sensitive entities;
3. generate a token for each entity;
4. display the redacted text;
5. store the token mapping in Redis;
6. restore the original data through the restoration process.

### Evidence

**Redaction Result:**

![Simple case redaction result](images/Week%204/Functional%20Testing/case%201%20-%20simple/redacted%20text.png)

**Redis Evidence:**

![Simple case Redis evidence](images/Week%204/Functional%20Testing/case%201%20-%20simple/redis%20server.png)

**Restoration Result:**

![Simple case restoration result](images/Week%204/Functional%20Testing/case%201%20-%20simple/restored%20text.png)

### Conclusion

The simple case serves as a basic test to ensure that the complete primary workflow operates correctly, from detection through restoration.

---

# 4. Functional Testing Case 2 — Multiple Entities

## 4.1 Objective

This test is used to ensure that the system can handle text containing a larger number of sensitive entities within a single input.

### Scenario

The clinical text contains multiple patients, doctors, addresses, dates, identification numbers, email addresses, and phone numbers.

### Expected Results

The system should be able to:

- detect multiple entities;
- assign different tokens to each entity;
- preserve the entity types;
- store all mappings in Redis;
- perform restoration without data loss.

### Evidence

**Redaction Result:**

![Multiple entity case redaction result](images/Week%204/Functional%20Testing/case%202%20-%20mixed%20entity/redacted%20text.png)

**Redis Evidence:**

![Multiple entity case Redis evidence](images/Week%204/Functional%20Testing/case%202%20-%20mixed%20entity/redis%20server.png)

**Restoration Result:**

![Multiple entity case restoration result](images/Week%204/Functional%20Testing/case%202%20-%20mixed%20entity/restored%20text.png)

### Conclusion

This case validates that the system does not only work with one or two entities, but can also handle multiple entities within a single clinical document.

---

# 5. Functional Testing Case 3 — Duplicate Entities

## 5.1 Objective

This test focuses on entities that appear more than once.

### Scenario

The same personal data or multiple identical data entries appear repeatedly within the clinical text.

For example:

```text
Patient John Anderson visited the hospital.
The patient John Anderson was examined by the doctor.
John Anderson returned for a follow-up examination.
```

### Items Being Verified

This test ensures that:

- the system does not lose any occurrence of an entity;
- each occurrence is handled correctly;
- Redis mappings remain consistent;
- the restoration process produces the expected data.

### Evidence

**Redaction Result:**

![Duplicate entity redaction result](images/Week%204/Functional%20Testing/case%203%20-%20duplicate%20entity/redacted%20text.png)

**Redis Evidence:**

![Duplicate entity Redis evidence](images/Week%204/Functional%20Testing/case%203%20-%20duplicate%20entity/redis%20server.png)

**Restoration Result:**

![Duplicate entity restoration result](images/Week%204/Functional%20Testing/case%203%20-%20duplicate%20entity/restored%20text.png)

### Conclusion

This case ensures that the pseudonymization and mapping mechanisms do not encounter conflicts when an entity appears repeatedly.

---

# 6. Performance Testing

Performance testing is used to determine how the system responds as the size of the clinical text increases.

The testing is divided into three scales:

1. small;
2. medium;
3. large.

---

## 6.1 Case 1 — Small Clinical Document

### Objective

To measure the processing time when the system receives a clinical document containing a relatively small amount of text and a limited number of entities.

### Observed Parameters

- processing time;
- number of entities;
- redaction result;
- restoration result;
- Redis mapping.

### Redaction Evidence

![Small clinical document performance result](images/Week%204/Performance%20Testing/case%201%20-%20small%20clinical/redacted%20text.png)

### Redis Evidence

![Small clinical document Redis evidence](images/Week%204/Performance%20Testing/case%201%20-%20small%20clinical/redis%20server.png)

### Restoration Evidence

![Small clinical document restoration result](images/Week%204/Performance%20Testing/case%201%20-%20small%20clinical/restored%20text.png)

---

# 7. Performance Testing Case 2 — Medium Clinical Document

## Objective

To determine the system's capability when the amount of text and number of entities increase compared to the small clinical document case.

### Redaction Evidence

![Medium clinical document performance result](images/Week%204/Performance%20Testing/case%202%20-%20medium%20clinical/redacted%20text.png)

### Redis Evidence

![Medium clinical document Redis evidence](images/Week%204/Performance%20Testing/case%202%20-%20medium%20clinical/redis%20server.png)

### Restoration Evidence

![Medium clinical document restoration result](images/Week%204/Performance%20Testing/case%202%20-%20medium%20clinical/restored%20text.png)

### Conclusion

This case is used to compare changes in processing time as the data workload increases.

---

# 8. Performance Testing Case 3 — Large Clinical Document

## Objective

To test the system using a large clinical text containing a higher number of entities.

### Redaction Evidence

![Large clinical document performance result](images/Week%204/Performance%20Testing/case%203%20-%20Large%20clinical/redacted%20text.png)

### Redis Evidence — Part 1

![Large clinical document Redis evidence part 1](images/Week%204/Performance%20Testing/case%203%20-%20Large%20clinical/redis%20server%20part%201.png)

### Redis Evidence — Part 2

![Large clinical document Redis evidence part 2](images/Week%204/Performance%20Testing/case%203%20-%20Large%20clinical/redis%20server%20part%202.png)

### Restoration Evidence

![Large clinical document restoration result](images/Week%204/Performance%20Testing/case%203%20-%20Large%20clinical/restored%20text.png)

### Conclusion

This case represents the largest workload test in the testing series. It is used to determine whether the system remains capable of performing redaction, mapping, and restoration when the amount of data increases significantly.

---

# 9. Validation Testing

Validation testing is used to ensure that the system provides the correct response under both normal and invalid input conditions.

---

## 9.1 Case 1 — Empty Input

### Objective

To ensure that the system does not process empty input.

### Scenario

The user presses the redaction button without entering any clinical text.

### Expected Results

The system should reject the process and notify the user that the input cannot be empty.

### Evidence

![Empty input validation](images/Week%204/Validation%20Testing/case%201%20-%20empty%20input/null%20redacted.png)

![Empty input restoration validation](images/Week%204/Validation%20Testing/case%201%20-%20empty%20input/null%20restored.png)

### Conclusion

Empty input validation ensures that the system does not perform unnecessary processing on empty data.

---

# 10. Validation Testing Case 2 — Normal Text

## Objective

To ensure that the system can accept text that does not contain sensitive entities.

### Scenario

The user provides normal text without personal or medical information that needs to be redacted.

### Expected Results

The system should still be able to process the input without generating unnecessary tokens.

### Evidence

![Normal text validation](images/Week%204/Validation%20Testing/case%202%20-%20normal%20text/redacrted%20text.png)

### Conclusion

This case ensures that the system does not unnecessarily redact the entire input text.

---

# 11. Validation Testing Case 3 — Restoration Without Token

## Objective

To ensure that the system can handle the restoration process when the provided text does not contain a token registered in Redis.

### Scenario

The user enters text that does not contain a valid pseudonymization token.

### Expected Results

The system must not generate fake data or perform arbitrary substitutions.

### Evidence

![Restoration without token](images/Week%204/Validation%20Testing/case%203%20-%20restore%20no%20token/restored%20text.png)

### Conclusion

This test ensures that the restoration mechanism does not perform substitutions on unknown tokens.

---

# 12. Validation Testing Case 4 — Unknown Text

## Objective

To test the system's behavior when receiving text that does not match the typical clinical document patterns used by the system.

### Expected Results

The system should continue to provide a stable response without experiencing a processing failure.

### Evidence

![Unknown text validation](images/Week%204/Validation%20Testing/case%204%20-%20uknown%20text/restored%20text.png)

### Conclusion

This test ensures that the system remains stable when handling input outside the primary expected scenarios.

---

# 13. Validation Testing Case 5 — Empty Restoration

## Objective

To ensure that the restoration process correctly handles empty input.

### Scenario

The user executes the restoration process without entering any text.

### Expected Results

The system should reject the process and provide an appropriate validation response.

### Evidence

![Empty restoration](images/Week%204/Validation%20Testing/case%205%20-%20empty%20redis/restored%20text.png)

### Conclusion

This validation ensures that the restoration endpoint is protected against empty input.

---

# 14. Testing Summary

| ID    | Category    | Test Case        | Evidence                     | Expected Result                              | Result |
| ----- | ----------- | ---------------- | ---------------------------- | -------------------------------------------- | ------ |
| FT-01 | Functional  | Simple Entity    | Redacted, Restored, Redis    | Entity is pseudonymized and restored         | PASSED |
| FT-02 | Functional  | Mixed Entity     | Redacted, Restored, Redis    | Multiple entity types are processed          | PASSED |
| FT-03 | Functional  | Duplicate Entity | Redacted, Restored, Redis    | Repeated entities use consistent mapping     | PASSED |
| PT-01 | Performance | Small Clinical   | Redacted, Restored, Redis    | Pipeline works with small input              | PASSED |
| PT-02 | Performance | Medium Clinical  | Redacted, Restored, Redis    | Pipeline remains stable with increased input | PASSED |
| PT-03 | Performance | Large Clinical   | Redacted, Restored, Redis ×2 | Pipeline handles large input and mappings    | PASSED |
| VT-01 | Validation  | Empty Input      | Null Redacted, Null Restored | Empty input is handled safely                | PASSED |
| VT-02 | Validation  | Normal Text      | Redacted                     | Normal text is not unnecessarily modified    | PASSED |
| VT-03 | Validation  | Restore No Token | Restored                     | Restore handles text without tokens          | PASSED |
| VT-04 | Validation  | Unknown Token    | Restored                     | Unknown mapping is handled safely            | PASSED |
| VT-05 | Validation  | Empty Redis      | Restored                     | Missing Redis mapping is handled safely      | PASSED |

---

# 15. Testing Conclusion

Based on the testing series that was conducted, the system was evaluated from three primary perspectives.

**First, functional testing** ensures that the system's core functionality operates correctly, starting from entity detection, redaction, and mapping storage through to data restoration.

**Second, performance testing** is used to observe changes in system behavior as the document size and number of entities increase from small to large scales.

**Third, validation testing** ensures that the system can properly handle empty input, normal text, unavailable tokens, unknown text, and restoration requests without input.

All visual evidence in this documentation originates from the testing results stored in the `images/Week 4/` directory. This documentation can be used as evidence of testing performed during the final stage of Privacy Shield LLM development.

---

# 16. Notes

This documentation focuses on **testing results and evidence**, rather than explaining the implementation of each function within the source code.

For further development, the testing results can be enhanced with:

- processing time for each scenario;
- number of detected entities;
- number of successfully restored entities;
- detection success rate;
- restoration success rate;
- memory usage;
- CPU usage;
- processing time comparison between small, medium, and large workloads.
