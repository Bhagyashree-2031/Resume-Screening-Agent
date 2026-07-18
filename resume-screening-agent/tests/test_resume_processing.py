import unittest

from utils.extractor import extract_candidate_profile, extract_skills
from utils.scorer import score_resume_against_jd


class ResumeProcessingTests(unittest.TestCase):
    def test_extract_name_prefers_person_name(self):
        resume_text = """
        John Doe
        john.doe@example.com
        +1 555 123 4567
        Computer Science and Engineering graduate with strong backend experience.
        """
        profile = extract_candidate_profile(resume_text, "john_doe.pdf")
        self.assertEqual(profile["name"], "John Doe")

    def test_extract_skills_captures_common_tech_stack(self):
        resume_text = """
        Worked with Python, FastAPI, Docker, AWS, SQL, and REST APIs in backend systems.
        """
        skills = extract_skills(resume_text)
        self.assertIn("python", skills)
        self.assertIn("fastapi", skills)
        self.assertIn("docker", skills)
        self.assertIn("aws", skills)
        self.assertIn("sql", skills)

    def test_extract_name_avoids_summary_and_section_text(self):
        resume_text = """
        John Doe
        john.doe@example.com
        +1 555 123 4567
        Computer Science and Engineering graduate with strong backend experience.
        Pre-University College
        """
        profile = extract_candidate_profile(resume_text, "john_doe.pdf")
        self.assertEqual(profile["name"], "John Doe")

    def test_scoring_ranks_matching_resume_highly(self):
        profile = {
            "skills": ["python", "fastapi", "docker", "aws", "sql"],
            "experience": "3 years of backend development and API engineering",
            "education": "B.Tech in Computer Science",
            "projects": ["Built Python backend services and deployed to AWS"],
            "achievements": ["Improved API performance and reliability"],
        }
        job_description = """
        Senior Python Developer with FastAPI, Docker, AWS, SQL, and REST API experience.
        """
        score_data = score_resume_against_jd(job_description, profile)
        self.assertGreater(score_data["score"], 70)
        self.assertLess(score_data["score"], 100)


if __name__ == "__main__":
    unittest.main()
