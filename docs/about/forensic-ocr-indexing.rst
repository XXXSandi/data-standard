.. _forensic-ocr-indexing:

Forensic OCR and harvest indexing tool
======================================

Overview
--------

Many organisations need to turn scanned corporate filings, disclosures, or case files into structured, searchable information. A forensic optical character recognition (OCR) and harvest indexing tool helps convert these paper or image-based sources into usable data that can be linked to Beneficial Ownership Data Standard (BODS) statements.

Goals
-----

* Extract ownership and control details from scanned or image-based records.
* Normalise and index extracted data so investigators can search across filings and case evidence.
* Produce machine-readable BODS-aligned outputs that can be shared or merged with other registries.
* Maintain provenance metadata so each extracted fact can be traced back to the page, file, or source image.

Workflow outline
----------------

1. **Ingest and triage**: Accept scanned PDFs, image bundles, or zipped case files and register them for processing.
2. **OCR and layout analysis**: Run OCR tuned for forms and stamped documents; capture bounding boxes to preserve layout context for later verification.
3. **Field harvesting**: Use templates, regular expressions, or machine learning models to pull entity names, registration numbers, addresses, officer details, and relationship language from the OCR output.
4. **Entity resolution**: Match harvested identifiers and names against existing BODS entity and person statements to reduce duplication; flag low-confidence matches for human review.
5. **BODS mapping**: Transform harvested fields into draft :any:`Entity <schema-entity>`, :any:`Person <schema-person>`, and :any:`Relationship <schema-relationship>` statements, attaching supporting statement-level annotations for provenance.
6. **Indexing and search**: Store harvested fields, confidence scores, and source locations in a search index so investigators can pivot by entity, person, jurisdiction, or document reference.
7. **Quality assurance**: Provide reviewers with side-by-side OCR snippets and source images so they can correct fields before export.
8. **Export and integration**: Output validated statements as BODS JSON packages, alongside citation metadata and audit logs, ready for downstream sharing or loading into registry systems.

Operational considerations
-------------------------

* **Auditability**: Every harvested fact should carry a traceable link to the original document page, region, and processing timestamp.
* **Security**: Enforce access controls and redact sensitive personal data that is not required for publication; log reviewer actions for compliance.
* **Extensibility**: Keep harvesting templates and extraction rules versioned so they can evolve with new filing formats without code changes.
* **Performance**: Use batching and asynchronous OCR processing for large historical backfiles; prioritise recent filings for rapid turnaround.

Alignment with BODS
-------------------

* Use :any:`source statements <schema-statement>` and annotations to embed provenance for every harvested field.
* Capture jurisdiction and registration numbers to improve matching with external datasets.
* Preserve historical versions of statements so investigators can see how declared ownership has changed across successive filings.
* Include placeholders when information must be withheld or redacted, to keep packages consistent with BODS completeness requirements.
