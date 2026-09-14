from dataclasses import dataclass

from providers.llm.base import LLMProvider


@dataclass
class JobExplanationContext:
    candidate_profile: str
    job_title: str
    company_name: str
    job_description: str
    match_score: float


class LLMService:

    def __init__(self, llm_provider: LLMProvider):
        self.llm_provider = llm_provider

    def generate_job_explanation(
        self,
        context: JobExplanationContext,
    ) -> str:

        prompt = f"""
        You are a job recommendation assistant.

        Explain the existing match between a candidate and a job.

        Candidate profile:
        {context.candidate_profile}

        Job title:
        {context.job_title}

        Company:
        {context.company_name}

        Job description:
        {context.job_description}

        Match score:
        {context.match_score}

        Instructions:
        - Use only information explicitly provided above.
        - Do not invent skills, experience, requirements, or qualifications.
        - Do not recalculate or reinterpret the match score.
        - Mention specific candidate skills that are relevant to the job.
        - If a required skill is not present in the candidate profile, do not assume the candidate has it.
        - Keep the explanation concise.
        - Do not use bullet points.
        - Return only the explanation.
        """

        return self.llm_provider.generate(prompt)