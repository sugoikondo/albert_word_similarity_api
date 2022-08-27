from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

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
    request = PredictionRequest(target_words=["銀行"], candidates=["現金", "リース資産"])
    config = PredictionConfig(top_n=2)
    result = word_similarity_resolver.resolve(request, config)

    print(result)
    return {"Hello": "World"}

