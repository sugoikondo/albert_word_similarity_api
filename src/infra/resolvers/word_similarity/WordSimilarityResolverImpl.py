import logging
import torch
import os.path
import numpy as np
import pandas as pd
from transformers import AlbertTokenizer, AlbertForPreTraining

from src.domain.word_similarity.PredictionConfig import PredictionConfig
from src.domain.word_similarity.PredictionRequest import PredictionRequest
from src.domain.word_similarity.PredictionResponse import PredictionResponse
from src.domain.word_similarity.SimilarityResult import SimilarityResult
from src.domain.word_similarity.WordSimilarity import WordSimilarity
from src.domain.word_similarity.WordSimilarityResolver import WordSimilarityResolver


def similarity(v1: np.ndarray, v2: np.ndarray) -> float:
    n1 = np.linalg.norm(v1)
    n2 = np.linalg.norm(v2)
    return np.dot(v1, v2) / n1 / n2


class WordSimilarityResolverImpl(WordSimilarityResolver):
    def __init__(self):
        logging.info('loading pretrained models...')
        self.tokenizer = AlbertTokenizer.from_pretrained('ALINEAR/albert-japanese-v2')
        self.model = AlbertForPreTraining.from_pretrained('ALINEAR/albert-japanese-v2')
        logging.info('model loaded successfully')

    def resolve(self, request: PredictionRequest, config: PredictionConfig) -> PredictionResponse:
        # 先に candidates 全てのベクトル表現を取得する
        candidate_vectors: pd.DataFrame = pd.DataFrame(columns=['word', 'vector'])
        for candidate in request.candidates:
            input_ids = torch.tensor(self.tokenizer.encode(candidate.strip(), add_special_tokens=True)).unsqueeze(0)
            word_vector = torch.mean(self.model(input_ids, output_hidden_states=True).hidden_states[12], 1)
            candidate_vectors = candidate_vectors.append(
                {
                    'word': candidate.strip(),
                    'vector': pd.DataFrame(word_vector.detach().numpy())
                }, ignore_index=True
            )

        # 次に候補者たちとの diff をそれぞれ取得する
        results: list[SimilarityResult] = []
        for word in request.target_words:
            input_ids = torch.tensor(self.tokenizer.encode(word, add_special_tokens=True)).unsqueeze(0)
            tgt_word_vector_dict = torch.mean(
                self.model(input_ids, output_hidden_states=True).hidden_states[12], 1
            ).detach().numpy()

            similar_words: list[WordSimilarity] = []
            for idx in candidate_vectors.index:
                candidate_word = candidate_vectors.loc[idx, 'word']
                candidate_vector_df = candidate_vectors.loc[idx, 'vector']
                sim = similarity(np.array(tgt_word_vector_dict), np.array(candidate_vector_df).flatten())[0].item()

                similar_words.append(WordSimilarity(candidate_word, sim))

            similar_words.sort(key=lambda x: x.similarity, reverse=True)
            results.append(
                SimilarityResult(
                    word=word,
                    similar_words=similar_words
                )
            )

        return PredictionResponse(results=results)
