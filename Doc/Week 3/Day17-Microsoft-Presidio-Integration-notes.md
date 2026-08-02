Today, I will write code to integrate Microsoft Presidio for NLP purposes.

Conceptually, Microsoft Presidio is an open-source framework from Microsoft designed to detect and analyze Personally Identifiable Information (PII), as well as perform redaction or anonymization. PII encompasses personal information—such as hospital medical data—that requires protection because it contains patient details, visit records, physician data, and the like.

The first step is to download the Microsoft Presidio libraries by running the commands `pip install presidio-analyzer` and `pip install presidio-anonymizer`.
For the second step, I am implementing Presidio solely on the back-end. At this stage, I only require the log analysis results and am not yet integrating it into the main pipeline, as my current focus is on understanding how to obtain those analysis results for the subsequent implementation phase. so if want see my proof so acces in images section, in Week 3 section
