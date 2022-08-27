from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

from src.domain.word_similarity.PredictionRequest import PredictionRequest
from src.domain.word_similarity.PredictionResponse import PredictionResponse
from src.domain.word_similarity.WordSimilarityResolver import WordSimilarityResolver


@dataclass(frozen=True)
class PredictionWordInputData:
    request: PredictionRequest


@dataclass(frozen=True)
class PredictionWordPayload:
    results: PredictionResponse


class PredictionWordSimilarityUseCase(metaclass=ABCMeta):
    @abstractmethod
    def handle(self, params: PredictionWordInputData) -> PredictionWordPayload:
        raise NotImplementedError


class PredictionWordSimilarityInteractor(PredictionWordSimilarityUseCase):
    def __init__(self, resolver: WordSimilarityResolver):
        self.resolver = resolver


    def handle(self, params: PredictionWordInputData) -> PredictionWordPayload:
