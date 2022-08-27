from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from containers import Container
from src.domain.word_similarity.PredictionConfig import PredictionConfig
from src.domain.word_similarity.PredictionRequest import PredictionRequest
from src.domain.word_similarity.WordSimilarityResolver import WordSimilarityResolver

router = APIRouter()


@router.get("/healthcheck")
@inject
async def fixed_prediction(
        word_similarity_resolver: WordSimilarityResolver = Depends(Provide(Container.word_similarity_resolver)),
):
    # Run the inference once to make sure the model is loaded onto memory.
    request = PredictionRequest(target_words=["銀行"], candidates=["現金"])
    config = PredictionConfig(top_n=1)
    word_similarity_resolver.resolve(request, config)
    return {"OK"}


class PredictionRequest(BaseModel):
    target_words: list[str]
    candidates: list[str]
    top_n: int = 5


class WordSimilarity(BaseModel):
    word: str
    similarity: float


class SimilarityResult(BaseModel):
    word: str
    similar_words: list[WordSimilarity]


class PredictionResponse(BaseModel):
    results: list[SimilarityResult]


@router.post("/word_similarity", response_model=PredictionResponse)
@inject
async def predict_word_similarity(
        request: PredictionRequest,
        word_similarity_resolver: WordSimilarityResolver = Depends(Provide(Container.word_similarity_resolver)),
):
    prediction_request = PredictionRequest(
        target_words=request.target_words,
        candidates=request.candidates
    )
    prediction_config = PredictionConfig(top_n=request.top_n)
    result = word_similarity_resolver.resolve(prediction_request, prediction_config)
    return result
