import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import pandas as pd


def export_results(results: List[Dict], output_dir: Path) -> Dict[str, Path]:
    """Export ranked results to CSV and JSON files with ATS-friendly fields."""
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / "ranking.csv"
    json_path = output_dir / "ranking.json"
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    rows = []
    for item in results:
        reasoning = item.get("reasoning", {}) or {}
        rows.append(
            {
                "Rank": item.get("rank", 0),
                "Candidate": item.get("candidate", "Unknown"),
                "Email": item.get("email", "N/A"),
                "Phone": item.get("phone", "N/A"),
                "Score": item.get("score", 0),
                "Similarity": item.get("similarity", 0),
                "Matched Skills": ", ".join(item.get("matched_skills", [])),
                "Missing Skills": ", ".join(item.get("missing_skills", [])),
                "Education": item.get("education", "N/A"),
                "Experience": item.get("experience", "N/A"),
                "Projects": " | ".join(item.get("projects", [])[:5]),
                "Certifications": " | ".join(item.get("certifications", [])[:5]),
                "Recommendation": item.get("recommendation", "Review manually"),
                "Reason": reasoning.get("reason_for_ranking", "N/A"),
                "Timestamp": timestamp,
            }
        )

    dataframe = pd.DataFrame(rows)
    dataframe.to_csv(csv_path, index=False)

    export_payload = []
    for item in results:
        export_payload.append(
            {
                "rank": item.get("rank", 0),
                "candidate": item.get("candidate", "Unknown"),
                "email": item.get("email", "N/A"),
                "phone": item.get("phone", "N/A"),
                "score": item.get("score", 0),
                "similarity": item.get("similarity", 0),
                "matched_skills": item.get("matched_skills", []),
                "missing_skills": item.get("missing_skills", []),
                "education": item.get("education", "N/A"),
                "experience": item.get("experience", "N/A"),
                "projects": item.get("projects", []),
                "certifications": item.get("certifications", []),
                "recommendation": item.get("recommendation", "Review manually"),
                "reason": (item.get("reasoning") or {}).get("reason_for_ranking", "N/A"),
                "timestamp": timestamp,
            }
        )

    with json_path.open("w", encoding="utf-8") as file_handle:
        json.dump(export_payload, file_handle, indent=2, ensure_ascii=False)

    return {"csv": csv_path, "json": json_path}
