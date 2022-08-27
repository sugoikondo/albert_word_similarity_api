from dataclasses import dataclass
from src.domain.word_similarity import WordSimilarity


@dataclass(frozen=True)
class SimilarityResult:
    word: str
    similar_words: list[WordSimilarity]
