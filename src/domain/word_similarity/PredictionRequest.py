from dataclasses import dataclass


@dataclass
class PredictionRequest:
    target_words: list[str]
    candidates: list[str]
