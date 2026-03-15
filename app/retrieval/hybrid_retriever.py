from .vector_retriever import VectorRetriever
from .bm25_page_retriever import BM25Retriever


class HybridRetriever:
    def __init__(self):
        self.vector = VectorRetriever()
        self.bm25 = BM25Retriever()

    def retrieve(self, query, top_k=10):

        vector_results = self.vector.retrieve(query, top_k)
        bm25_results = self.bm25.retrieve(query, top_k)

        scores = {}

        for r in vector_results:
            scores[r["chunk_id"]] = scores.get(r["chunk_id"], 0) + r["score"]

        for r in bm25_results:
            scores[r["chunk_id"]] = scores.get(r["chunk_id"], 0) + r["score"]

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        final = []

        for chunk_id, score in ranked[:top_k]:

            for r in vector_results + bm25_results:
                if r["chunk_id"] == chunk_id:
                    final.append(r)
                    break

        return final