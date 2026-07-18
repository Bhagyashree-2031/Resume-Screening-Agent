import json
import os
import re
from typing import Dict

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def _fallback_reasoning(job_description: str, profile: Dict[str, object], score_data: Dict[str, object]) -> Dict[str, str]:
    """Provide deterministic reasoning when Groq is unavailable."""
    score = float(score_data.get("score", 0) or 0)
    matched_skills = list(score_data.get("matched_skills", []) or [])
    missing_skills = list(score_data.get("missing_skills", []) or [])

    if score >= 80:
        recommendation = "Strong hire — advance to interview"
        reason_for_ranking = "High alignment with the job description and strong skill overlap."
    elif score >= 65:
        recommendation = "Good fit — shortlist for review"
        reason_for_ranking = "Solid match with relevant experience and a meaningful share of the requested skills."
    elif score >= 50:
        recommendation = "Moderate fit — review manually"
        reason_for_ranking = "Partial alignment with the role; some requested skills or experience areas are missing."
    else:
        recommendation = "Weak fit — not a priority shortlist"
        reason_for_ranking = "The profile shows limited overlap with the role requirements."

    return {
        "strengths": ["Matched skills: " + ", ".join(matched_skills[:5])] if matched_skills else ["Profile contains relevant experience"],
        "weaknesses": ["Missing skills: " + ", ".join(missing_skills[:5])] if missing_skills else ["No major gaps detected"],
        "missing_skills": missing_skills,
        "recommendation": recommendation,
        "reason_for_ranking": reason_for_ranking,
    }


def _clean_json_payload(content: str) -> str:
    """Strip markdown fences and extra text before JSON parsing."""
    cleaned = content.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned


def generate_reasoning(job_description: str, profile: Dict[str, object], score_data: Dict[str, object]) -> Dict[str, str]:
    """Generate structured AI reasoning for a candidate using Groq."""
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        return _fallback_reasoning(job_description, profile, score_data)

    client = Groq(api_key=api_key)
    prompt = f"""
    You are an expert hiring analyst.
    Job Description:
    {job_description}

    Candidate Profile:
    Name: {profile.get('name', 'Unknown')}
    Skills: {', '.join(profile.get('skills', []))}
    Experience: {profile.get('experience', 'N/A')}
    Education: {profile.get('education', 'N/A')}

    Score Summary:
    Overall Score: {score_data.get('score', 0)}
    Similarity: {score_data.get('similarity', 0)}
    Matched Skills: {', '.join(score_data.get('matched_skills', []))}
    Missing Skills: {', '.join(score_data.get('missing_skills', []))}

    Return ONLY VALID JSON with this schema:
    {{"strengths":[], "weaknesses":[], "missing_skills":[], "recommendation":"", "reason_for_ranking":""}}
    Keep it concise and useful for hiring decisions.
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful hiring assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        content = response.choices[0].message.content or "{}"
        parsed = json.loads(_clean_json_payload(content))
        return {
            "strengths": parsed.get("strengths", []),
            "weaknesses": parsed.get("weaknesses", []),
            "missing_skills": parsed.get("missing_skills", []),
            "recommendation": parsed.get("recommendation", "Review manually"),
            "reason_for_ranking": parsed.get("reason_for_ranking", "Insufficient data"),
        }
    except (json.JSONDecodeError, TypeError, ValueError):
        return _fallback_reasoning(job_description, profile, score_data)
    except Exception as exc:
        return _fallback_reasoning(job_description, profile, score_data)
