from dataclasses import dataclass


@dataclass
class PredictionConfig:
    top_n: int
