# Architecture Notes

## Request flow

1. Browser submits a resume and target job description.
2. FastAPI validates the request.
3. `parsers.py` extracts plain text from PDF, DOCX, or TXT.
4. `scoring.py` creates normalized embeddings with `all-MiniLM-L6-v2`.
5. Cosine similarity becomes the semantic component.
6. `skills.py` performs deterministic skill extraction against a documented taxonomy.
7. Matched and missing skills are computed as set intersection/difference.
8. The API combines semantic and skill signals into the final product score.
9. The frontend renders score, coverage, gaps, and recommendations.

## Design principles

- **Explainability:** every score has visible components.
- **Separation of concerns:** parsing, extraction, scoring, and presentation are independent.
- **Privacy by default:** no database or persistent upload directory.
- **Deployment simplicity:** one FastAPI service serves the API and dashboard.
- **Replaceable ML layer:** the matcher can later be swapped for a fine-tuned ranking model.
