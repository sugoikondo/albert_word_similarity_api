import struct

import numpy as np
import redis
from configs import REDIS_HOST, REDIS_PORT


class WordVectorCacheClient:
    """
    A client for caching & retrieving word vectors.
    """
    def __init__(self):
        self.redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

    def resolve(self, words: list[str]) -> np.ndarray:
        vectors = []
        for word in words:
            vectors.append(self.redis.get(word))
        return np.array(vectors)

    def store(self, data: dict[str, np.ndarray]):
        for key, value in data.items():
            self.redis.set(key, value)

    def __store_vector(self, word: str, vector: np.ndarray):
        height, width = vector.shape
        shape = struct.pack('>II', height, width)
        encoded = shape + vector.tobytes()

        self.redis.set(word, encoded)

    def __restore_vector(self, word: str) -> np.ndarray:
        encoded = self.redis.get(word)
        height, width = struct.unpack('>II', encoded[:8])
        vector = np.frombuffer(encoded, dtype=np.float32, offset=8).reshape(height, width)
        return vector
