import json

from providers.llm.base import LLMProvider
from repositories.resume_parsed_data_repository import ResumeParsedDataRepository
from schemas.resume_profile import ResumeProfile
from services.resume_experience_service import ResumeExperienceService

class ResumeParsingService:

    def __init__(
            self,
            llm_provider: LLMProvider,
            experience_service: ResumeExperienceService,
            parsed_data_repository: ResumeParsedDataRepository,
    ):
        self.llm_provider = llm_provider
        self.experience_service = experience_service
        self.parsed_data_repository = parsed_data_repository

    def parse(
        self,
        resume_text: str,
    ) -> ResumeProfile:

        prompt = f"""
        You are a resume parsing assistant.

        Extract structured information from the resume below.

        Resume:
        {resume_text}

        Return ONLY valid JSON.

        The JSON must contain exactly these fields:
        {{
            "full_name": null,
            "current_job_title": null,
            "years_of_experience": null,
            "technical_skills": [],
            "professional_summary": null,
            "experience": []
        }}

        Each experience entry must contain exactly these fields:
        {{
            "company": null,
            "job_title": null,
            "start_date": null,
            "end_date": null
        }}

        Rules:

        GENERAL:
        - Use only information explicitly present in the resume.
        - Do not invent information.
        - If information is unavailable, use null or an empty list.
        - Do not use markdown.
        - Do not wrap the JSON in ```.

        PERSONAL INFORMATION:
        - The first person's name appearing in the resume header should be used as full_name.
        - Do not return null for full_name if a person's name is clearly present in the resume.
        - curren-t_job_title must represent the person's current or most recent professional job title.
        
        EXPERIENCE:
- Extract every professional employment entry from the resume.
- An employment entry consists of:
  1. A job title with its employment date range.
  2. The company name on the following line when the resume structure places it there.
- The job title and date range may appear on the same line.
- The company name may appear on the immediately following line.
- Treat the job-title/date line and the following company line as ONE experience entry.
- For example:
  "Software Developer Trainee Nov 2025 – Present"
  followed by
  "DFIVE Technologies Pvt. Ltd., Bengaluru"
  must produce:
  {{
      "company": "DFIVE Technologies Pvt. Ltd.",
      "job_title": "Software Developer Trainee",
      "start_date": "Nov 2025",
      "end_date": "Present"
  }}
- Another example:
  "Technical Apprentice Nov 2021 – Nov 2022"
  followed by
  "Bharat Electronics Limited (BEL), Bengaluru"
  must produce:
  {{
      "company": "Bharat Electronics Limited (BEL)",
      "job_title": "Technical Apprentice",
      "start_date": "Nov 2021",
      "end_date": "Nov 2022"
  }}
- Extract both start_date and end_date whenever they are explicitly present.
- Never drop an explicitly present end date.
- Use "Present" when the resume explicitly indicates that the employment is ongoing.
- Remove only the location portion from the company name when it is clearly separated by a comma.
- Do not include education, projects, or certifications as experience.
- Never create an experience entry when company, job_title, and start_date are all missing.
- If an experience entry cannot be reliably identified, omit it rather than inventing values.
- Do not calculate years_of_experience.
- Always return years_of_experience as null.
        
        TECHNICAL SKILLS:
        - technical_skills must be a flat list of individual skills.
        - Extract specific programming languages, frameworks, libraries, databases, technologies, technical concepts, platforms, and technical tools explicitly mentioned.
        - Split category-based skill sections into individual skills.
        - For example, if the resume contains "Backend: Java, Spring Boot, REST APIs", return:
          ["Java", "Spring Boot", "REST APIs"]
        - Do not include category labels such as "Backend", "Frontend", "Databases", or "Programming".
        - Do not return an entire category line as one skill.
        - Do not include soft skills.
        - Do not invent skills that are not explicitly mentioned.

        PROFESSIONAL SUMMARY:
        - Create a concise professional summary using only information explicitly present in the resume.
        - Do not add qualifications or experience that are not present.

        Return only the JSON object.
        """

        response = self.llm_provider.generate(prompt)

        data = json.loads(response)

        profile = ResumeProfile.model_validate(data)

        profile.years_of_experience = self.experience_service.calculate_years(
            profile.experience
        )

        return profile

    def parse_and_save(
            self,
            resume_id: int,
    ) -> ResumeProfile | None:

        parsed_data = self.parsed_data_repository.find_by_resume_id(
            resume_id
        )

        if parsed_data is None:
            return None

        resume_text = parsed_data.cleaned_text

        if not resume_text:
            return None

        profile = self.parse(resume_text)

        parsed_json = profile.model_dump_json()

        self.parsed_data_repository.update_parsed_json(
            resume_id=resume_id,
            parsed_json=parsed_json,
        )

        return profile