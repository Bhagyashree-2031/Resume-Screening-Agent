import os
import sys
from pathlib import Path
from typing import List

import streamlit as st
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent
sys.path.append(str(ROOT_DIR))
load_dotenv(ROOT_DIR / ".env")

from utils.parser import load_text_from_file
from utils.extractor import extract_candidate_profile
from utils.scorer import score_resume_against_jd
from utils.groq_reasoner import generate_reasoning
from utils.exporter import export_results


st.set_page_config(page_title="Resume Screening Agent", page_icon="📄", layout="wide")


@st.cache_data(show_spinner=False)
def load_sample_jd() -> str:
    """Load a sample job description for demo use."""
    sample_path = ROOT_DIR / "sample_data" / "jd.txt"
    if sample_path.exists():
        return sample_path.read_text(encoding="utf-8")
    return """
    Senior Python Developer
    Build scalable backend systems using Python, FastAPI, Docker, AWS, and SQL.
    Experience with REST APIs, CI/CD, and machine learning pipelines is a plus.
    """


def _get_score_color(score: float) -> str:
    """Return a color label based on the candidate score."""
    if score >= 90:
        return "🟢 Strong Match"
    if score >= 70:
        return "🔵 Good Match"
    if score >= 50:
        return "🟠 Moderate Match"
    return "🔴 Low Match"


def _get_groq_status() -> tuple[str, str]:
    """Return the Groq configuration state and guidance text."""
    groq_api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not groq_api_key:
        return "not configured", "Add GROQ_API_KEY to .env to enable AI reasoning."

    placeholder_values = {
        "",
        "changeme",
        "your_groq_api_key_here",
        "your-api-key-here",
        "your_groq_api_key",
        "your_groq_api_key_here"
    }
    normalized = groq_api_key.lower()
    if normalized in placeholder_values or normalized.startswith("your") or normalized.startswith("<"):
        return "not configured", "Replace the placeholder GROQ_API_KEY in .env with a real key to enable AI reasoning."

    return "configured", "Groq AI reasoning is enabled."


def main() -> None:
    """Render the Streamlit ATS dashboard and orchestrate resume screening."""
    st.title("Resume Screening Agent")
    st.caption("Applicant Tracking System for ranking and reviewing candidate resumes")

    groq_status, groq_message = _get_groq_status()

    with st.sidebar:
        st.header("Configuration")
        if groq_status == "configured":
            st.success("Groq API status: configured")
        else:
            st.warning("Groq API status: not configured")
            st.caption(groq_message)
        st.text_input("Model", value="llama-3.3-70b-versatile", disabled=True)
        st.caption("Upload a job description and as many resumes as you have. Ten or more is recommended for a fuller run.")

        jd_file = st.file_uploader("Upload Job Description (.txt)", type=["txt"])
        resume_files = st.file_uploader(
            "Upload Resumes (PDF, DOCX, TXT)",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True,
        )
        analyze_button = st.button("Analyze Candidates", type="primary")

    if st.session_state.get("results") and not analyze_button:
        render_results(st.session_state.results)
        return

    if analyze_button:
        if not jd_file:
            jd_text = load_sample_jd()
        else:
            jd_text = jd_file.read().decode("utf-8", errors="ignore")

        if not resume_files:
            st.error("Please upload at least one resume.")
            return

        if len(resume_files) < 10:
            st.info("You uploaded fewer than 10 resumes. The app will still process them, but 10+ resumes are recommended for a fuller ranking run.")

        with st.spinner("Processing candidates..."):
            progress_bar = st.progress(0)
            processed_results = []

            for index, uploaded_file in enumerate(resume_files, start=1):
                try:
                    text = load_text_from_file(uploaded_file)
                    profile = extract_candidate_profile(text, uploaded_file.name)
                    score_data = score_resume_against_jd(jd_text, profile)
                    reasoning = generate_reasoning(jd_text, profile, score_data)

                    processed_results.append(
                        {
                            "candidate": profile.get("name", uploaded_file.name),
                            "score": score_data.get("score", 0),
                            "similarity": score_data.get("similarity", 0),
                            "matched_skills": score_data.get("matched_skills", []),
                            "missing_skills": score_data.get("missing_skills", []),
                            "experience": profile.get("experience", "N/A"),
                            "education": profile.get("education", "N/A"),
                            "email": profile.get("email", "N/A"),
                            "phone": profile.get("phone", "N/A"),
                            "linkedin": profile.get("linkedin", "N/A"),
                            "github": profile.get("github", "N/A"),
                            "location": profile.get("location", "N/A"),
                            "skills": profile.get("skills", []),
                            "projects": profile.get("projects", []),
                            "certifications": profile.get("certifications", []),
                            "internships": profile.get("internships", []),
                            "achievements": profile.get("achievements", []),
                            "recommendation": reasoning.get("recommendation", "Review manually"),
                            "reasoning": reasoning,
                            "raw_profile": profile,
                        }
                    )
                except Exception as exc:
                    st.warning(f"Skipped {uploaded_file.name}: {exc}")

                progress_bar.progress(index / len(resume_files))

            ranked_results = sorted(processed_results, key=lambda item: item["score"], reverse=True)
            for rank, item in enumerate(ranked_results, start=1):
                item["rank"] = rank

            export_results(ranked_results, ROOT_DIR / "output")
            st.session_state.results = ranked_results

        render_results(st.session_state.results)


def render_results(results: List[dict]) -> None:
    """Render the ATS-style results dashboard."""
    st.subheader("Candidate Ranking")

    if not results:
        st.info("No results to show yet.")
        return

    display_df = []
    for item in results:
        display_df.append(
            {
                "Rank": item.get("rank", 0),
                "Candidate": item.get("candidate", "Unknown"),
                "Score": round(item.get("score", 0), 2),
                "Similarity": round(item.get("similarity", 0), 2),
                "Matched Skills": ", ".join(item.get("matched_skills", [])[:8]),
                "Missing Skills": ", ".join(item.get("missing_skills", [])[:8]),
                "Experience": item.get("experience", "N/A"),
                "Education": item.get("education", "N/A"),
                "Recommendation": item.get("recommendation", "Review manually"),
            }
        )

    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    metrics_col1.metric("Average Score", f"{sum(item.get('score', 0) for item in results) / len(results):.1f}%")
    metrics_col2.metric("Highest Score", f"{max(item.get('score', 0) for item in results):.1f}%")
    metrics_col3.metric("Lowest Score", f"{min(item.get('score', 0) for item in results):.1f}%")
    metrics_col4.metric("Total Candidates", len(results))

    st.markdown("### 🏆 Top 3 Candidates")
    top_three = results[:3]
    cards = st.columns(3)
    for card, item in zip(cards, top_three):
        with card:
            st.markdown(f"### {item.get('candidate', 'Unknown')}")
            st.metric("Match Score", f"{round(item.get('score', 0), 1)}%")
            st.caption(_get_score_color(item.get("score", 0)))
            st.write("**Matched Skills:**")
            for skill in item.get("matched_skills", [])[:6]:
                st.markdown(f"<span style='background:#d1fae5;color:#065f46;padding:2px 8px;border-radius:999px;font-size:12px;'>● {skill}</span>", unsafe_allow_html=True)
            st.write("**Missing Skills:**")
            for skill in item.get("missing_skills", [])[:6]:
                st.markdown(f"<span style='background:#fee2e2;color:#991b1b;padding:2px 8px;border-radius:999px;font-size:12px;'>● {skill}</span>", unsafe_allow_html=True)
            st.write("**Recommendation:**", item.get("recommendation", "Review manually"))

    st.markdown("### 📋 Candidate Table")
    st.dataframe(display_df, use_container_width=True)

    st.markdown("### 🔎 Candidate Details")
    for item in results:
        profile = item.get("raw_profile") or {}
        with st.expander(f"{item.get('candidate', 'Unknown')} — {round(item.get('score', 0), 1)}%"):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write("**Candidate Name:**", item.get("candidate", "Unknown"))
                st.write("**Email:**", profile.get("email", "N/A"))
                st.write("**Phone:**", profile.get("phone", "N/A"))
                st.write("**Education:**", item.get("education", "N/A"))
                st.write("**Experience:**", item.get("experience", "N/A"))
                st.write("**Projects:**", "; ".join(profile.get("projects", [])[:5]) or "N/A")
                st.write("**Certifications:**", "; ".join(profile.get("certifications", [])[:5]) or "N/A")
                st.write("**Recommendation:**", item.get("recommendation", "Review manually"))
                st.write("**Reason:**", (item.get("reasoning") or {}).get("reason_for_ranking", "N/A"))
            with col2:
                st.write("**Skills:**", ", ".join(profile.get("skills", [])[:15]) or "N/A")
                st.write("**Matched Skills:**", ", ".join(item.get("matched_skills", [])[:10]))
                st.write("**Missing Skills:**", ", ".join(item.get("missing_skills", [])[:10]))
                st.write("**LinkedIn:**", profile.get("linkedin", "N/A"))
                st.write("**GitHub:**", profile.get("github", "N/A"))

    st.download_button(
        label="Download CSV",
        data=open(ROOT_DIR / "output" / "ranking.csv", "rb").read(),
        file_name="ranking.csv",
        mime="text/csv",
    )
    st.download_button(
        label="Download JSON",
        data=open(ROOT_DIR / "output" / "ranking.json", "rb").read(),
        file_name="ranking.json",
        mime="application/json",
    )


if __name__ == "__main__":
    main()
