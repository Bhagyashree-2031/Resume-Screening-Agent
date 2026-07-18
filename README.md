# 🤖 Resume Screening AI Agent

## 📌 Project Overview

The **Resume Screening AI Agent** is an AI-powered Applicant Tracking System (ATS) built with **Streamlit** that automates candidate screening by comparing multiple resumes against a Job Description (JD). The application combines **Natural Language Processing (NLP)**, **semantic similarity**, **skill matching**, and **AI-generated reasoning** to rank candidates and provide explainable hiring recommendations.

Designed with a modular architecture, the project supports recruiters and hiring teams by significantly reducing manual resume screening time while maintaining transparent and reproducible candidate evaluations.

---

# ✨ Features

* Upload a Job Description (.txt)
* Upload multiple resumes (PDF, DOCX, TXT)
* Extract candidate information including:

  * Name
  * Skills
  * Education
  * Experience
  * Projects
  * Certifications
* Semantic similarity using Sentence Transformers
* Skill matching against the Job Description
* Weighted candidate scoring (0–100)
* AI-generated strengths, weaknesses, missing skills, and recommendations using **Groq (Llama 3.3 70B)**
* Interactive Streamlit dashboard
* Candidate ranking with detailed reasoning
* Export ranked results to **CSV** and **JSON**
* Supports processing multiple resumes in a single run

---

# 🏗️ Architecture

The project follows a modular architecture for better maintainability and scalability.

| Module                   | Description                                          |
| ------------------------ | ---------------------------------------------------- |
| `app.py`                 | Streamlit frontend and application workflow          |
| `utils/parser.py`        | Resume parsing (PDF, DOCX, TXT)                      |
| `utils/extractor.py`     | Candidate information extraction and skill detection |
| `utils/scorer.py`        | Semantic similarity and weighted scoring             |
| `utils/groq_reasoner.py` | AI-generated reasoning using Groq                    |
| `utils/exporter.py`      | CSV and JSON export                                  |

---

# 🛠️ Tech Stack

* Python 3.11+
* Streamlit
* Sentence Transformers
* scikit-learn
* Groq API
* Llama 3.3 70B
* pdfplumber
* python-docx
* pandas
* NumPy
* python-dotenv

---

# 📂 Project Structure

```text
resume-screening-agent/
│
├── app.py
├── requirements.txt
├── README.md
├── TRADEOFFS.md
├── .env.example
├── .gitignore
│
├── utils/
│   ├── parser.py
│   ├── extractor.py
│   ├── scorer.py
│   ├── groq_reasoner.py
│   └── exporter.py
│
├── sample_data/
│   ├── jd_devops_engineer.txt
│   └── resumes/
│
├── output/
│   ├── ranking.csv
│   └── ranking.json
│
└── screenshots/
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/resume-screening-agent.git

cd resume-screening-agent
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Configure the Groq API

Create a `.env` file in the project root and add your Groq API key.

```env
GROQ_API_KEY=your_groq_api_key_here
```

> **Important:** Never commit your actual API key to GitHub. Use `.env.example` to provide a template.

---

# ▶️ Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your default browser.

Default URL:

```
http://localhost:8501
```

---

# 🚀 End-to-End Workflow

1. Launch the Streamlit application.
2. Upload a Job Description (.txt).
3. Upload one or more resumes (PDF, DOCX, or TXT).
4. The application extracts candidate information.
5. Semantic similarity between each resume and the Job Description is computed.
6. Technical skills are matched against the required skills.
7. Weighted scores are calculated.
8. Groq generates AI-powered candidate reasoning.
9. Candidates are ranked based on the final score.
10. Results can be exported as CSV and JSON.

---

# 📊 Scoring Method

Candidate ranking is based on a weighted scoring approach.

| Component           | Weight |
| ------------------- | ------ |
| Semantic Similarity | 60%    |
| Skill Match         | 25%    |
| Experience Match    | 10%    |
| Education Match     | 5%     |

### Semantic Similarity

The application uses the **all-MiniLM-L6-v2** Sentence Transformer model to generate embeddings for both the Job Description and resumes. Cosine similarity is then used to measure their semantic relevance.

### Skill Matching

A predefined engineering skill dictionary identifies matched and missing skills relative to the Job Description.

### AI Reasoning

Groq's **Llama 3.3 70B** model generates:

* Candidate strengths
* Weaknesses
* Missing skills
* Interview recommendation
* Ranking explanation

---

# 📥 Sample Inputs

Sample data is included to help reviewers reproduce the application.

```text
sample_data/
│
├── jd_devops_engineer.txt
│
└── resumes/
    ├── resume_01.pdf
    ├── resume_02.pdf
    ├── resume_03.txt
    ├── resume_04.txt
    └── resume_05.pdf
```

---

# 📤 Sample Outputs

After processing, the application generates:

```text
output/
│
├── ranking.csv
└── ranking.json
```

The Streamlit dashboard displays:

* Candidate Ranking
* Match Scores
* Matched Skills
* Missing Skills
* AI Recommendations
* Candidate Details

---

# 📸 Screenshots

<img width="1920" height="1080" alt="Screenshot (1)" src="https://github.com/user-attachments/assets/28640fe9-a1d0-44a0-8ea0-0522b13e03ca" />
<img width="1920" height="1080" alt="Screenshot (2)" src="https://github.com/user-attachments/assets/9909c7ed-e8c6-439c-9f9b-edbd2e2ecb38" />
<img width="1920" height="1080" alt="Screenshot (3)" src="https://github.com/user-attachments/assets/ff58090a-1242-4ca4-b54f-4f438efcf4c1" />
<img width="1920" height="1080" alt="Screenshot (4)" src="https://github.com/user-attachments/assets/4b651cfb-8821-40db-9afd-579b5cc2db87" />
<img width="1920" height="1080" alt="Screenshot (5)" src="https://github.com/user-attachments/assets/0633eedb-04fd-4057-8404-40f50de4f192" />
<img width="1920" height="1080" alt="Screenshot (6)" src="https://github.com/user-attachments/assets/ce63b043-59cd-43c2-9b60-04e6f525fafc" />
<img width="1920" height="1080" alt="Screenshot (7)" src="https://github.com/user-attachments/assets/66968394-05b5-4f38-8e23-2fd2bc0e054f" />

---

# 🎯 Design Choices

* Streamlit was selected for rapid development of an interactive dashboard.
* Sentence Transformers provide semantic understanding beyond keyword matching.
* Skill matching complements semantic similarity with explicit technical skill comparison.
* Groq (Llama 3.3 70B) generates explainable AI recommendations for recruiters.
* A modular architecture improves readability, maintainability, and scalability.

---

# 🔄 Limitations

* Scanned image-based PDFs are not fully supported without OCR.
* Resume parsing accuracy depends on document formatting.
* Skill detection relies on a predefined engineering skill dictionary.
* Scoring weights are fixed and may require tuning for different hiring scenarios.

---

# 🚀 Future Improvements

* OCR support for scanned resumes
* Multi-language resume parsing
* Configurable scoring weights
* Resume duplicate detection
* Candidate comparison dashboard
* Recruiter authentication
* Cloud deployment
* ATS integration
* Expanded engineering skill database
* Advanced analytics and reporting

---

# 📄 License

This project was developed for educational purposes and as part of an AI Agent Challenge. It is intended to demonstrate AI-powered resume screening, candidate ranking, and explainable recruitment workflows.
