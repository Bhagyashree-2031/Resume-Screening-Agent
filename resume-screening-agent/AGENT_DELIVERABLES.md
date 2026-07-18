# Agent-Specific Deliverables

## Resume Screening Agent (Intermediate)

This project implements an AI-powered Resume Screening Agent that ranks multiple candidate resumes against a given Job Description (JD) using Natural Language Processing (NLP), semantic similarity, skill matching, and AI-generated reasoning.

---

# Deliverables

## 1. Job Description (JD)

A sample Job Description is included in the repository.

**Location**

```text
sample_data/
└── jd_devops_engineer.txt
```

The JD is uploaded through the Streamlit interface and serves as the reference for candidate evaluation.

---

## 2. Sample Resume Folder

The repository contains sample resumes for demonstration and testing.

**Supported Formats**

- PDF
- DOCX
- TXT

**Location**

```text
sample_data/
└── resumes/
```

The application supports processing multiple resumes in a single run and is designed to handle 10 or more resumes.

---

## 3. Ranked Output

After processing, the application generates ranked candidate results.

### CSV Output

```text
output/
└── ranking.csv
```

### JSON Output

```text
output/
└── ranking.json
```

Each ranked result includes:

- Candidate Name
- Match Score
- Matched Skills
- Missing Skills
- Recommendation
- AI-generated Reasoning
- Rank

The same information is also displayed in the Streamlit dashboard.

---

## 4. Scoring Method

Candidate ranking is calculated using a weighted scoring approach.

| Component | Weight |
|-----------|--------|
| Semantic Similarity | 60% |
| Skill Match | 25% |
| Experience Match | 10% |
| Education Match | 5% |

### Semantic Similarity

The application uses the Sentence Transformer model:

```text
all-MiniLM-L6-v2
```

Cosine similarity is computed between the Job Description and each resume.

### Skill Matching

A predefined engineering skill dictionary is used to identify matched and missing technical skills.

### AI Reasoning

The Groq API using the **Llama 3.3 70B** model generates:

- Strengths
- Weaknesses
- Missing Skills
- Recommendation
- Reason for Ranking

---

# Expected Workflow

1. Upload a Job Description (.txt)
2. Upload multiple resumes (PDF, DOCX, or TXT)
3. Extract candidate information
4. Compute semantic similarity
5. Perform skill matching
6. Calculate weighted scores
7. Rank candidates
8. Generate AI-powered reasoning
9. Export ranked results as CSV and JSON

---

# Deliverable Checklist

- ✅ Job Description (JD)
- ✅ Sample Resume Folder
- ✅ PDF, DOCX, and TXT Resume Support
- ✅ Resume Parsing
- ✅ Candidate Information Extraction
- ✅ NLP Semantic Similarity
- ✅ Skill Matching
- ✅ Candidate Ranking
- ✅ AI-generated Recommendations
- ✅ Ranked CSV Export
- ✅ Ranked JSON Export
- ✅ Streamlit Dashboard
- ✅ Multiple Resume Processing

---

This project fulfills the required deliverables for the **Resume Screening Agent (Intermediate)** challenge by providing an end-to-end workflow for intelligent resume screening, candidate ranking, AI-assisted evaluation, and exportable results.