from dependencies.llm import get_llm_provider
from services.llm_service import (
    JobExplanationContext,
    LLMService,
)


provider = get_llm_provider()

service = LLMService(
    llm_provider=provider,
)

context = JobExplanationContext(
    candidate_profile="""
Java Backend Developer with experience in Java, Spring Boot,
PostgreSQL, REST APIs, JPA, and Docker.
""",
    job_title="Java Backend Developer",
    company_name="Example Technologies",
    job_description="""
We are looking for a Java Backend Developer to build REST APIs
using Java and Spring Boot. Experience with PostgreSQL and JPA
is preferred.
""",
    match_score=87.0
)

explanation = service.generate_job_explanation(context)

print(explanation)