# ResumeIQ — AI Resume Analyzer & Job Match Engine

> **Semantic resume intelligence for better job targeting.**

ResumeIQ analyzes a resume against a target job description using **Transformer embeddings, cosine similarity, and an explainable skill-overlap layer**. Instead of treating keyword frequency as the whole story, it combines semantic alignment with explicit technical skill coverage.

![Python](https://img.shields.io/badge/Python-3.12-111827?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API-111827?style=flat-square&logo=fastapi&logoColor=white)
![NLP](https://img.shields.io/badge/NLP-Transformers-111827?style=flat-square)
![Docker](https://img.shields.io/badge/Docker-ready-111827?style=flat-square&logo=docker&logoColor=white)

## What it does

- Upload **PDF, DOCX, or TXT** resumes
- Extract resume text without persisting uploaded files
- Generate semantic representations with **all-MiniLM-L6-v2**
- Calculate resume ↔ job semantic similarity
- Extract technical skills with an auditable skill taxonomy
- Separate **matched skills** from **skill gaps**
- Combine semantic and skill signals into a transparent match score
- Generate concise, actionable resume recommendations
- Serve a responsive dashboard directly from FastAPI

## Architecture

```text
Resume (PDF/DOCX/TXT)
        │
        ▼
┌───────────────────┐
│   Text Extraction │
└─────────┬─────────┘
          │
          ▼
┌────────────────────────────┐
│ Transformer Embedding Model│
│    all-MiniLM-L6-v2        │
└────────────┬───────────────┘
             │
      ┌──────┴──────┐
      ▼             ▼
Semantic Score   Skill Engine
      │             │
      └──────┬──────┘
             ▼
       Match Intelligence
             │
             ▼
     Web Dashboard / JSON API
```

### Scoring

```
Final Match = 0.65 × Semantic Similarity
            + 0.35 × Skill Coverage
```

This is a heuristic product metric, **not a hiring prediction**. The weights are explicit so they can be tuned or replaced by a learned ranking model later.

## Run locally

```bash
git clone https://github.com/PriyanshuBhatt29/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer

python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
uvicorn backend.api:app --reload
```

Open **http://localhost:8000**.

The first analysis downloads the Sentence Transformers model and caches it locally.

## Docker

```bash
docker compose up --build
```

Then open **http://localhost:8000**.

## API

### Health
`GET /api/health`

### Analyze a resume
`POST /api/analyze`

Multipart fields:
- `resume`: PDF, DOCX, or TXT file
- `job_description`: target role description

### Analyze raw text
`POST /api/analyze-text`

```json
{
  "resume_text": "Python developer with experience in FastAPI...",
  "job_description": "Looking for a Python engineer with FastAPI..."
}
```

## Project structure

```text
AI-Resume-Analyzer/
├── backend/
│   ├── api.py
│   ├── config.py
│   ├── parsers.py
│   ├── scoring.py
│   └── skills.py
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── tests/
│   └── test_api.py
├── docs/
│   └── architecture.md
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Engineering notes

**Why embeddings?** A resume can describe the same capability using different language. Sentence-level embeddings provide a semantic signal that is less brittle than exact keyword matching.

**Why a separate skill layer?** Pure semantic similarity can hide concrete gaps. The explicit taxonomy makes the result inspectable and gives users actionable missing-skill information.

**Privacy:** The current application processes uploaded files in memory and does not implement persistent resume storage. In production, authentication, rate limiting, malware scanning, encrypted storage, and stricter CORS should be added.

## Roadmap

- [ ] Learned job-ranking model from labeled resume/job pairs
- [ ] Section-aware resume parsing
- [ ] Experience and seniority extraction
- [ ] Skill synonym graph and ontology
- [ ] Recruiter comparison workspace
- [ ] Evaluation dataset and model benchmarks
- [ ] Optional local embedding inference

## License

MIT

---

**Built as a practical AI engineering project — not just a UI demo.**
