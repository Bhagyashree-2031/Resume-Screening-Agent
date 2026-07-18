import logging
import re
from typing import Dict, List

logger = logging.getLogger(__name__)

SKILL_ALIASES = {
    "python": ["python", "py"],
    "react": ["react", "reactjs", "react.js"],
    "node": ["node", "nodejs", "node.js", "express"],
    "spring boot": ["spring boot", "springboot", "spring"],
    "sql": ["sql", "sql server", "mssql", "postgresql", "mysql"],
    "machine learning": ["machine learning", "ml"],
    "artificial intelligence": ["artificial intelligence", "ai"],
    "scikit-learn": ["scikit-learn", "scikit learn", "sklearn"],
    "rest api": ["rest api", "restful api", "apis", "api development"],
    "c++": ["c++", "cpp"],
    "c": ["c", "c language"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript", "ts"],
    "fastapi": ["fastapi", "fast api"],
    "django": ["django"],
    "flask": ["flask"],
    "docker": ["docker", "docker compose"],
    "kubernetes": ["kubernetes", "k8s"],
    "aws": ["aws", "amazon web services"],
    "azure": ["azure", "microsoft azure"],
    "gcp": ["gcp", "google cloud platform"],
    "git": ["git"],
    "github": ["github"],
    "gitlab": ["gitlab"],
    "linux": ["linux", "ubuntu"],
    "ci/cd": ["ci/cd", "continuous integration", "continuous deployment"],
    "jenkins": ["jenkins"],
    "terraform": ["terraform"],
    "ansible": ["ansible"],
    "bash": ["bash", "shell scripting"],
    "pytest": ["pytest", "pytests"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    "opencv": ["opencv"],
    "nlp": ["nlp", "natural language processing"],
    "computer vision": ["computer vision"],
    "spark": ["spark"],
    "hadoop": ["hadoop"],
    "airflow": ["airflow"],
    "dbt": ["dbt"],
    "tableau": ["tableau"],
    "excel": ["excel"],
    "power bi": ["power bi"],
    "snowflake": ["snowflake"],
    "microservices": ["microservices"],
    "system design": ["system design"],
    "distributed systems": ["distributed systems"],
    "agile": ["agile"],
    "scrum": ["scrum"],
    "streamlit": ["streamlit"],
    "html": ["html"],
    "css": ["css"],
    "mongodb": ["mongodb"],
    "redis": ["redis"],
    "postgresql": ["postgresql"],
    "mysql": ["mysql"],
    "elasticsearch": ["elasticsearch"],
    "kafka": ["kafka"],
    "rabbitmq": ["rabbitmq"],
    "graphql": ["graphql"],
    "unit testing": ["unit testing"],
    "testing": ["testing"],
    "selenium": ["selenium"],
    "jupyter": ["jupyter"],
    "data analysis": ["data analysis"],
    "data visualization": ["data visualization"],
    "statistics": ["statistics"],
    "matplotlib": ["matplotlib"],
    "seaborn": ["seaborn"],
    "plotly": ["plotly"],
    "pyspark": ["pyspark"],
    "scala": ["scala"],
    "kotlin": ["kotlin"],
    "go": ["go"],
    "rust": ["rust"],
    "php": ["php"],
    "csharp": ["csharp", ".net"],
    "dotnet": ["dotnet", ".net"],
    "aspnet": ["aspnet", "asp.net"],
    "spring": ["spring"],
    "hibernate": ["hibernate"],
    "jpa": ["jpa"],
    "oracle": ["oracle"],
    "sqlalchemy": ["sqlalchemy"],
    "pymongo": ["pymongo"],
    "celery": ["celery"],
    "devops": ["devops"],
    "prometheus": ["prometheus"],
    "grafana": ["grafana"],
    "openai": ["openai"],
    "groq": ["groq"],
    "langchain": ["langchain"],
    "llamaindex": ["llamaindex"],
    "transformers": ["transformers"],
    "spacy": ["spacy"],
    "torch": ["torch"],
}

COMMON_SKILLS = sorted(SKILL_ALIASES.keys())

HEADING_PATTERNS = [
    r"^contact$",
    r"^profile$",
    r"^summary$",
    r"^objective$",
    r"^skills$",
    r"^technical skills$",
    r"^experience$",
    r"^work experience$",
    r"^education$",
    r"^projects$",
    r"^certifications$",
    r"^achievements$",
    r"^internships$",
    r"^links$",
    r"^linkedin$",
    r"^github$",
    r"^location$",
    r"^about$",
    r"^references$",
]

NAME_REJECT_KEYWORDS = (
    "graduate",
    "graduated",
    "education",
    "university",
    "college",
    "school",
    "skills",
    "experience",
    "project",
    "projects",
    "certification",
    "certifications",
    "summary",
    "objective",
    "profile",
    "internship",
    "internships",
    "achievement",
    "achievements",
    "backend",
    "frontend",
    "developer",
    "engineer",
    "best",
    "practices",
    "practice",
    "science",
    "engineering",
    "technology",
    "management",
    "systems",
    "design",
)


def normalize_text(text: str) -> str:
    """Normalize whitespace and casing for stable matching."""
    return re.sub(r"\s+", " ", text or "").strip().lower()


def clean_line(line: str) -> str:
    """Clean a line for parsing and matching."""
    return re.sub(r"\s+", " ", line or "").strip()


def is_heading(line: str) -> bool:
    """Determine whether a line is likely a resume heading."""
    cleaned = clean_line(line).lower()
    if not cleaned:
        return True
    if len(cleaned.split()) > 8:
        return False
    if re.search(r"@|http|https|\d{3,}", cleaned):
        return False
    if cleaned in {"name", "phone", "email", "address", "portfolio", "resume", "summary", "objective"}:
        return True
    return any(re.fullmatch(pattern, cleaned) for pattern in HEADING_PATTERNS)


def _matches_alias(text: str, alias: str) -> bool:
    """Match a skill alias while tolerating punctuation and spacing differences."""
    if not alias:
        return False
    normalized_alias = re.sub(r"[^a-z0-9]+", " ", alias.lower()).strip()
    if not normalized_alias:
        return False
    normalized_text = re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()
    if not normalized_text:
        return False
    return re.search(r"(?<![a-z0-9])" + re.escape(normalized_alias) + r"(?![a-z0-9])", normalized_text) is not None


def extract_skills(text: str) -> List[str]:
    """Extract candidate skills using aliases, punctuation-tolerant matching, and common variants."""
    found_skills: List[str] = []

    for canonical_skill, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            if _matches_alias(text, alias):
                found_skills.append(canonical_skill)
                break

    return sorted(set(found_skills))


def is_probable_person_name(line: str) -> bool:
    """Determine whether a line is likely to be a person's name rather than resume content."""
    cleaned = clean_line(line)
    if not cleaned:
        return False
    if is_heading(cleaned):
        return False
    if len(cleaned.split()) > 4:
        return False
    if re.search(r"@|http|https|\d", cleaned):
        return False
    lowered = cleaned.lower()
    if any(keyword in lowered for keyword in NAME_REJECT_KEYWORDS):
        return False
    if len(cleaned.split()) < 2:
        return False
    if cleaned[0].islower():
        return False
    if re.fullmatch(r"[A-Z][A-Za-z'&.-]+(?:\s+[A-Z][A-Za-z'&.-]+){1,3}", cleaned):
        return True
    if re.fullmatch(r"[A-Z][A-Za-z'&.-]+(?:\s+[A-Za-z'&.-]+){1,3}", cleaned) and all(token[0].isupper() for token in cleaned.split()):
        return True
    return False


def extract_name(text: str) -> str:
    """Extract a real candidate name by preferring contact-block lines over summary content."""
    lines = [clean_line(line) for line in text.splitlines() if clean_line(line)]

    for line in lines[:15]:
        if is_probable_person_name(line):
            return line

    for line in lines[:15]:
        if is_heading(line):
            continue
        if len(line.split()) <= 4 and not re.search(r"@|http|https|\d", line):
            lowered = line.lower()
            if re.search(r"[A-Za-z]", line) and not any(keyword in lowered for keyword in NAME_REJECT_KEYWORDS):
                tokens = line.split()
                if len(tokens) >= 2 and all(token[0].isupper() for token in tokens if token):
                    return line

    return "Unknown Candidate"


def extract_email(text: str) -> str:
    """Extract an email address from the resume text."""
    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return match.group(0) if match else "N/A"


def extract_phone(text: str) -> str:
    """Extract a phone number from the resume text."""
    match = re.search(r"(?:\+\d{1,3}[-.\s]?)?(?:\(?\d{2,4}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}", text)
    return match.group(0) if match else "N/A"


def extract_linkedin(text: str) -> str:
    """Extract a LinkedIn profile URL if available."""
    match = re.search(r"https?://(?:www\.)?linkedin\.com/in/[^\s]+", text, re.IGNORECASE)
    return match.group(0) if match else "N/A"


def extract_github(text: str) -> str:
    """Extract a GitHub profile URL if available."""
    match = re.search(r"https?://(?:www\.)?github\.com/[^\s]+", text, re.IGNORECASE)
    return match.group(0) if match else "N/A"


def extract_location(text: str) -> str:
    """Extract a likely location string from the resume text."""
    lines = [clean_line(line) for line in text.splitlines() if clean_line(line)]
    for line in lines:
        if re.search(r"(india|bengaluru|bangalore|delhi|mumbai|pune|hyderabad|chennai|usa|canada|uk|germany|singapore|australia)", line, re.IGNORECASE):
            if not is_heading(line):
                return line
    return "N/A"


def extract_education(text: str) -> str:
    """Extract education details from the resume text."""
    lines = [clean_line(line) for line in text.splitlines() if clean_line(line)]
    education_lines = []
    for line in lines:
        if re.search(r"(b\.tech|btech|b\.e|be|bs|ba|bsc|master|msc|m\.sc|phd|ph\.d|bachelor|college|university|engineering|technology|information technology|computer science)", line.lower()):
            if not is_heading(line):
                education_lines.append(line)
    return " | ".join(education_lines[:8]) if education_lines else "N/A"


def extract_experience(text: str) -> str:
    """Extract experience-related details from the resume text."""
    lines = [clean_line(line) for line in text.splitlines() if clean_line(line)]
    experience_lines = []
    for line in lines:
        if re.search(r"(experience|worked|developer|engineer|intern|internship|software|sde|analyst|manager|lead|team|year|years|month|months)", line.lower()):
            if not is_heading(line):
                experience_lines.append(line)
    return " | ".join(experience_lines[:12]) if experience_lines else "N/A"


def extract_projects(text: str) -> List[str]:
    """Extract likely project lines from the resume text."""
    lines = [clean_line(line) for line in text.splitlines() if clean_line(line)]
    projects = []
    for line in lines:
        if re.search(r"(project|built|developed|implemented|designed|created|optimized|deployed)", line.lower()):
            if not is_heading(line):
                projects.append(line)
    return projects[:8]


def extract_certifications(text: str) -> List[str]:
    """Extract certifications and credentials from resume text."""
    lines = [clean_line(line) for line in text.splitlines() if clean_line(line)]
    certs = []
    for line in lines:
        if re.search(r"(certified|certificate|certification|aws|azure|docker|kubernetes|oracle|google|microsoft|ibm)", line.lower()):
            if not is_heading(line):
                certs.append(line)
    return certs[:8]


def extract_internships(text: str) -> List[str]:
    """Extract internship-related lines from a resume."""
    lines = [clean_line(line) for line in text.splitlines() if clean_line(line)]
    internships = []
    for line in lines:
        if re.search(r"(intern|internship)", line.lower()):
            if not is_heading(line):
                internships.append(line)
    return internships[:8]


def extract_achievements(text: str) -> List[str]:
    """Extract achievement-related lines from a resume."""
    lines = [clean_line(line) for line in text.splitlines() if clean_line(line)]
    achievements = []
    for line in lines:
        if re.search(r"(award|awarded|won|published|recognized|volunteer|leader|mentored|organized|contributed)", line.lower()):
            if not is_heading(line):
                achievements.append(line)
    return achievements[:8]


def extract_candidate_profile(text: str, filename: str) -> Dict[str, object]:
    """Create a structured candidate profile from parsed resume text."""
    try:
        profile = {
            "name": extract_name(text),
            "email": extract_email(text),
            "phone": extract_phone(text),
            "linkedin": extract_linkedin(text),
            "github": extract_github(text),
            "location": extract_location(text),
            "skills": extract_skills(text),
            "education": extract_education(text),
            "experience": extract_experience(text),
            "projects": extract_projects(text),
            "certifications": extract_certifications(text),
            "internships": extract_internships(text),
            "achievements": extract_achievements(text),
            "filename": filename,
        }
        return profile
    except Exception as exc:
        logger.exception("Failed to extract candidate profile for %s", filename)
        return {
            "name": "Unknown Candidate",
            "email": "N/A",
            "phone": "N/A",
            "linkedin": "N/A",
            "github": "N/A",
            "location": "N/A",
            "skills": [],
            "education": "N/A",
            "experience": "N/A",
            "projects": [],
            "certifications": [],
            "internships": [],
            "achievements": [],
            "filename": filename,
            "error": str(exc),
        }
