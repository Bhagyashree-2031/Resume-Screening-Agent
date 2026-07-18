# Tradeoffs and Design Decisions

## Overview

This project was designed to balance accuracy, simplicity, performance, and ease of use within the limited development time of a 24-hour challenge.

---

# Design Choices

## Resume Parsing

The application supports PDF, DOCX, and TXT resumes.

A lightweight parsing approach was selected to provide fast processing while supporting common resume formats.

---

## Semantic Similarity

Semantic similarity is computed using the Sentence Transformer model:

```
all-MiniLM-L6-v2
```

This model offers a good balance between speed, memory usage, and semantic understanding.

---

## Skill Matching

A predefined software engineering skill dictionary is used to compare candidate skills against the Job Description.

This improves ranking by considering both semantic similarity and explicit skill overlap.

---

## AI Reasoning

The application uses the Groq API with:

```
Llama 3.3 70B
```

The model generates:

- Candidate strengths
- Weaknesses
- Missing skills
- Interview recommendation
- Ranking explanation

This provides human-readable insights in addition to numerical scores.

---

# Tradeoffs

## Resume Parsing

The parser is optimized for standard resume layouts.

Highly customized resume formats may reduce extraction accuracy.

---

## Scanned PDFs

The current implementation assumes resumes contain selectable text.

Scanned image-based PDFs are not fully supported because OCR is not integrated.

---

## Skill Detection

Skill matching primarily relies on a curated dictionary and extracted resume text.

Rare technologies or unusual naming conventions may not always be recognized.

---

## Scoring

The scoring model combines semantic similarity, skill matching, education, and experience using predefined weights.

Different organizations may prefer different weighting strategies depending on hiring priorities.

---

## Performance

Embedding generation is optimized for multiple resumes, but processing time increases as the number and size of resumes grow.

---

# Future Improvements

Given additional development time, the following enhancements would be implemented:

- OCR support for scanned resumes
- Larger and configurable skill database
- Better experience extraction
- Multi-language resume support
- Resume duplicate detection
- Candidate comparison dashboard
- Recruiter feedback loop
- Adaptive scoring weights
- Cloud deployment
- Authentication and user management

---

# Conclusion

The current implementation provides a complete end-to-end AI Resume Screening Agent that fulfills the challenge requirements while maintaining a clean architecture, reliable ranking workflow, and an intuitive user interface. The design emphasizes reproducibility, modularity, and ease of evaluation while leaving room for future enhancements.