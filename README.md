# Bulk Certificate Generator

A backend API for generating certificates in bulk using FastAPI, SQLAlchemy, SQLite, and ReportLab.

The system accepts a list of recipients, creates a generation job, processes certificates in the background, tracks generation progress, handles individual failures, and provides APIs to retrieve generated certificates.

---

## Features

- Bulk certificate generation
- REST API built with FastAPI
- Request validation using Pydantic
- SQLite relational database
- SQLAlchemy ORM
- Background certificate processing
- PDF certificate generation using ReportLab
- Job status and progress tracking
- Individual certificate status tracking
- Individual failure handling
- Certificate download API
- Automated tests using Pytest
- Interactive API documentation with Swagger/OpenAPI

---

## Tech Stack

- Python 3.12
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- ReportLab
- Pytest
- Uvicorn

---

## Project Structure

```text
bulk-certificate-generator/
│
├── app/
│   ├── main.py
│   ├── database.py
│   │
│   ├── models/
│   │   ├── job.py
│   │   └── certificate.py
│   │
│   ├── schemas/
│   │   └── job.py
│   │
│   └── services/
│       ├── certificate_generator.py
│       └── job_processor.py
│
├── generated/
├── tests/
│   ├── test_api.py
│   ├── test_certificate.py
│   └── test_failure.py
│
├── requirements.txt
├── README.md
└── .gitignore