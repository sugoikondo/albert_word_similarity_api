from dataclasses import dataclass

from src.domain.word_similarity.SimilarityResult import SimilarityResult


@dataclass(frozen=True)
class PredictionResponse:
    results: list[SimilarityResult]
