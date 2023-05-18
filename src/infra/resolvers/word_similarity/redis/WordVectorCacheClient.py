import asyncio
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

    async def resolve(self, words: list[str]) -> np.ndarray:
        vectors = []
        for word in words:
            vectors.append(self.__restore_vector(word))
        return np.array(vectors)

    async def store(self, data: dict[str, np.ndarray]):
        request_list = []
        for key, value in data.items():
            request_list.append(self.__store_vector(key, value))

        await asyncio.gather(*request_list)
        return

    async def __store_vector(self, word: str, vector: np.ndarray):
        height, width = vector.shape
        shape = struct.pack('>II', height, width)
        encoded = shape + vector.tobytes()

        self.redis.set(word, encoded)

    async def __restore_vector(self, word: str) -> np.ndarray:
        encoded = self.redis.get(word)
        height, width = struct.unpack('>II', encoded[:8])
        vector = np.frombuffer(encoded, dtype=np.float32, offset=8).reshape(height, width)
        return vector
