from abc import abstractmethod, ABCMeta

from src.domain.word_similarity.PredictionRequest import PredictionRequest
from src.domain.word_similarity.PredictionResponse import PredictionResponse


class WordSimilarityResolver(metaclass=ABCMeta):
    @abstractmethod
    def resolve(self, request: PredictionRequest) -> PredictionResponse:
        raise NotImplementedError
