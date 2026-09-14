from dataclasses import dataclass


@dataclass
class RankedRecommendation:
    job_id: int
    similarity: float


class RankingService:

    def rank(
        self,
        recommendations: list[tuple[int, float]],
    ) -> list[RankedRecommendation]:

        ranked = sorted(
            recommendations,
            key=lambda item: item[1],
            reverse=True,
        )

        return [
            RankedRecommendation(
                job_id=job_id,
                similarity=similarity,
            )
            for job_id, similarity in ranked
        ]