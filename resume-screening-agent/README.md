# Resume Screening AI Agent

## Project Overview

The Resume Screening AI Agent is a production-style Streamlit application that ranks multiple resumes against a job description using NLP similarity and skill matching. It is designed for junior AI research associates and emphasizes modular architecture, clean code, and explainable results.

## Features

- Upload one job description in TXT format
- Upload multiple resumes in PDF, DOCX, or TXT format
- Extract candidate information such as name, skills, education, experience, projects, and certifications
- Compute semantic similarity using SentenceTransformers
- Match candidate skills against a predefined engineering skill dictionary
- Generate weighted ranking scores out of 100
- Produce AI-generated reasoning using Groq
- Export results as CSV and JSON

## Architecture

The project follows a modular structure:

- app.py: Streamlit frontend and orchestration logic
- utils/parser.py: file parsing for TXT, PDF, and DOCX
- utils/extractor.py: candidate profile extraction and skill detection
- utils/scorer.py: NLP similarity and weighted scoring
- utils/groq_reasoner.py: Groq-based reasoning generation
- utils/exporter.py: CSV and JSON export


## Tech Stack

- Python 3.11+
- Streamlit
- Sentence Transformers
- scikit-learn
- Groq API
- Llama 3.3 70B
- pdfplumber
- python-docx
- pandas
- NumPy

## Folder Structure

```text
resume-screening-agent/
app.py
requirements.txt
README.md
.env.example
.gitignore
utils/
parser.py
extractor.py
scorer.py
groq_reasoner.py
exporter.py
sample_data/
jd.txt
resumes/
output/
ranking.csv
ranking.json
```

## Installation

1. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

## Requirements

The project uses:

- streamlit
- sentence-transformers
- scikit-learn
- groq
- pdfplumber
- python-docx
- pandas
- python-dotenv

## Groq API Setup

1. Create a `.env` file from `.env.example`
2. Add your Groq API key:

```text
GROQ_API_KEY=Your API key
```

## How to Run

```bash
streamlit run app.py
```

## Screenshots Placeholder

- Add screenshots of the upload screen and ranking results here.

## Future Improvements

- Support advanced resume parsing with named entity recognition
- Add recruiter feedback and interview recommendations
- Improve skill matching with ontology-based expansion
- Add more polished analytics dashboards

## License

This project is intended for educational and assessment purposes.
