from dataclasses import dataclass


@dataclass(frozen=True)
class PredictionConfig:
    top_n: int
