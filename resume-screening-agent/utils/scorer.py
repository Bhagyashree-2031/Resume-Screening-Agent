import re
from typing import Dict, List, Tuple

try:
    from sentence_transformers import SentenceTransformer, util
except Exception:  # pragma: no cover - environment fallback
    SentenceTransformer = None
    util = None

MODEL_NAME = "all-MiniLM-L6-v2"
MODEL = SentenceTransformer(MODEL_NAME) if SentenceTransformer is not None else None

STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "to",
    "of",
    "in",
    "on",
    "a",
    "an",
    "is",
    "are",
    "be",
    "this",
    "that",
    "these",
    "those",
    "from",
    "as",
    "or",
    "by",
    "at",
    "using",
    "experience",
    "developer",
    "developer",
    "role",
    "skills",
}


def normalize_skill_name(skill: str) -> str:
    """Normalize a skill string for consistent matching."""
    return re.sub(r"\s+", " ", skill.strip().lower())


def _lexical_overlap(job_description: str, resume_text: str) -> float:
    """Compute a conservative lexical overlap score between the job description and resume text."""
    def tokens(text: str) -> set[str]:
        return {
            normalize_skill_name(token)
            for token in re.findall(r"[a-z0-9]+", text.lower())
            if normalize_skill_name(token) not in STOPWORDS and len(normalize_skill_name(token)) > 2
        }

    job_tokens = tokens(job_description)
    resume_tokens = tokens(resume_text)
    if not job_tokens:
        return 0.0
    return len(job_tokens & resume_tokens) / len(job_tokens)


def compute_similarity(job_description: str, resume_text: str) -> float:
    """Compute a blended semantic and lexical similarity score."""
    lexical_similarity = _lexical_overlap(job_description, resume_text)
    if not resume_text.strip():
        return 0.0
    if MODEL is None or util is None:
        return round(max(0.0, min(1.0, lexical_similarity)), 4)
    try:
        embeddings = MODEL.encode([job_description, resume_text], convert_to_tensor=True)
        semantic_similarity = util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()
        semantic_similarity = max(0.0, min(1.0, semantic_similarity))
        return round(max(0.0, min(1.0, (semantic_similarity * 0.7) + (lexical_similarity * 0.3))), 4)
    except Exception:
        return round(max(0.0, min(1.0, lexical_similarity)), 4)


def calculate_skill_match(job_skills: List[str], candidate_skills: List[str]) -> Tuple[List[str], List[str], float]:
    """Match skills between the job description and resume profile."""
    normalized_job = {normalize_skill_name(skill) for skill in job_skills}
    normalized_candidate = {normalize_skill_name(skill) for skill in candidate_skills}

    matched = sorted(normalized_job & normalized_candidate)
    missing = sorted(normalized_job - normalized_candidate)
    ratio = (len(matched) / len(normalized_job)) if normalized_job else 0.0
    return matched, missing, ratio


def extract_job_skills(job_description: str) -> List[str]:
    """Extract skills from a job description using a shared skill dictionary."""
    from utils.extractor import COMMON_SKILLS

    normalized_text = re.sub(r"\s+", " ", job_description.lower())
    matched_skills = []
    for skill in COMMON_SKILLS:
        if re.search(r"\b" + re.escape(skill) + r"\b", normalized_text):
            matched_skills.append(skill)
    return matched_skills


def _experience_score(profile: Dict[str, object]) -> float:
    """Convert extracted experience text into a realistic contribution to the overall score."""
    experience_text = str(profile.get("experience", "") or "")
    if not experience_text or experience_text == "N/A":
        return 0.0
    lowered = experience_text.lower()
    if re.search(r"(\d+(?:\.\d+)?)\s*(?:\+\s*)?(years?|yrs?)", lowered):
        years = float(re.search(r"(\d+(?:\.\d+)?)\s*(?:\+\s*)?(years?|yrs?)", lowered).group(1))
        if years >= 5:
            return 1.0
        if years >= 3:
            return 0.8
        if years >= 1:
            return 0.6
        return 0.4
    if re.search(r"\b(senior|lead|principal|staff)\b", lowered):
        return 0.9
    if re.search(r"\b(intern|junior|associate)\b", lowered):
        return 0.35
    return 0.6


def _education_score(profile: Dict[str, object]) -> float:
    """Convert extracted education text into a realistic contribution to the overall score."""
    education_text = str(profile.get("education", "") or "")
    if not education_text or education_text == "N/A":
        return 0.0
    lowered = education_text.lower()
    if re.search(r"\b(phd|doctorate)\b", lowered):
        return 1.0
    if re.search(r"\b(master|m\.tech|mtech|msc|ms|mba)\b", lowered):
        return 0.9
    if re.search(r"\b(b\.tech|btech|be|bs|bachelor|engineering|computer science|information technology)\b", lowered):
        return 0.75
    return 0.5


def score_resume_against_jd(job_description: str, profile: Dict[str, object]) -> Dict[str, object]:
    """Compute the final weighted score for a candidate using a realistic ATS formula."""
    job_skills = extract_job_skills(job_description)
    candidate_skills = list(profile.get("skills", []) or [])

    matched_skills, missing_skills, skill_ratio = calculate_skill_match(job_skills, candidate_skills)
    resume_text = " ".join(
        [
            str(profile.get("experience", "")),
            str(profile.get("education", "")),
            " ".join(profile.get("projects", [])),
            " ".join(profile.get("achievements", [])),
            " ".join(candidate_skills),
        ]
    )
    similarity = compute_similarity(job_description, resume_text)
    experience_score = _experience_score(profile)
    education_score = _education_score(profile)

    final_score = round(
        similarity * 25 + skill_ratio * 40 + experience_score * 20 + education_score * 15,
        2,
    )

    final_score = max(0.0, min(95.0, final_score))

    return {
        "score": final_score,
        "similarity": round(similarity, 4),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "experience_score": round(experience_score, 2),
        "education_score": round(education_score, 2),
        "job_skills": job_skills,
    }
