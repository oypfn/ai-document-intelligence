# AI Document Intelligence

A document-processing API foundation for secure PDF ingestion and structured text extraction. The project is intentionally built around a clear boundary between deterministic document processing and future AI features.

## Current milestone

- FastAPI service with health endpoint.
- PDF-only upload endpoint with a 10 MB request limit.
- PDF signature validation, encrypted-file rejection and page-wise text extraction.
- Automated API tests and GitHub Actions quality workflow.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Open `/docs` for the interactive API reference. Run checks with `ruff check .` and `pytest`.

## Security and scope

Files are processed in memory and are not persisted. This is a prototype foundation, not a production document vault. Authentication, tenant isolation, malware scanning, encrypted object storage, retention controls, OCR, embeddings, semantic retrieval and LLM providers remain planned work. Never upload confidential documents to a public demo.

## Roadmap

- [x] Health endpoint and PDF extraction
- [x] File type and size guardrails
- [x] API tests and CI
- [ ] OCR for scanned documents
- [ ] Background processing and status tracking
- [ ] Embeddings and semantic search
- [ ] Auth, tenant isolation and secure storage
- [ ] Evaluation set for extraction quality
