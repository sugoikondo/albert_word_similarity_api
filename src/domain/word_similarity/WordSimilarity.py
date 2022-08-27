from dataclasses import dataclass


@dataclass(frozen=True)
class WordSimilarity:
    word: str
    similarity: float
