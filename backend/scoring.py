import re

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from .config import settings
from .skills import extract_skills


class ResumeMatcher:
    def __init__(self) -> None:
        self.model = SentenceTransformer(settings.model_name)

    def embed(self, text: str) -> np.ndarray:
        return self.model.encode([text], normalize_embeddings=True)[0]

    def analyze(self, resume: str, job_description: str) -> dict:
        resume = resume[: settings.max_text_length]
        job_description = job_description[: settings.max_text_length]

        resume_vector = self.embed(resume)
        job_vector = self.embed(job_description)
        semantic_similarity = float(cosine_similarity([resume_vector], [job_vector])[0][0])
        semantic_score = round(max(0, min(100, semantic_similarity * 100)), 1)

        resume_skills = extract_skills(resume)
        job_skills = extract_skills(job_description)
        resume_set, job_set = set(resume_skills), set(job_skills)
        matched = sorted(resume_set & job_set)
        missing = sorted(job_set - resume_set)
        skill_score = round((len(matched) / len(job_set) * 100), 1) if job_set else 0.0

        final_score = round((semantic_score * 0.65) + (skill_score * 0.35), 1)

        return {
            "match_score": final_score,
            "semantic_score": semantic_score,
            "skill_score": skill_score,
            "matched_skills": matched,
            "missing_skills": missing,
            "resume_skills": sorted(resume_set),
            "job_skills": sorted(job_set),
            "recommendations": self._recommendations(missing, resume, job_description),
        }

    @staticmethod
    def _recommendations(missing: list[str], resume: str, job: str) -> list[str]:
        suggestions = []
        if missing:
            suggestions.append(
                f"Strengthen evidence for {', '.join(missing[:5])} in projects, experience, or skills."
            )
        if not re.search(r"\b(results?|impact|increased|reduced|improved|achieved)\b", resume, re.I):
            suggestions.append("Add measurable outcomes to project and experience bullets.")
        if len(resume.split()) < 250:
            suggestions.append("Add concise context around your strongest projects and technical contributions.")
        if not suggestions:
            suggestions.append("Keep tailoring keywords and quantified impact to the target role.")
        return suggestions[:3]


_matcher: ResumeMatcher | None = None


def get_matcher() -> ResumeMatcher:
    global _matcher
    if _matcher is None:
        _matcher = ResumeMatcher()
    return _matcher
