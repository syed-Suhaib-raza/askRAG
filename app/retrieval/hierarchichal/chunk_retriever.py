from ..vector_retriever import VectorRetriever


class ChunkRetriever:
    def __init__(self):
        self.vector = VectorRetriever()

    def retrieve(self, query, section_ids, top_k=10):

        results = self.vector.retrieve(query, top_k * 3)

        filtered = []

        for r in results:
            if r["section_id"] in section_ids:
                filtered.append(r)

        return filtered[:top_k]