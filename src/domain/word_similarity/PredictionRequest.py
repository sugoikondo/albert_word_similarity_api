from dataclasses import dataclass


@dataclass(frozen=True)
class PredictionRequest:
    target_words: list[str]
    candidates: list[str]
