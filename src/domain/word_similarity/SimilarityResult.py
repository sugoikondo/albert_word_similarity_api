from dataclasses import dataclass
from src.domain.word_similarity import WordSimilarity


@dataclass
class SimilarityResult:
    word: str
    similar_words: list[WordSimilarity]
