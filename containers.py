from dependency_injector import containers, providers

from src.infra.resolvers.word_similarity.WordSimilarityResolverImpl import WordSimilarityResolverImpl


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["endpoints"])

    # infra
    word_similarity_resolver = providers.ThreadSafeSingleton(WordSimilarityResolverImpl)
