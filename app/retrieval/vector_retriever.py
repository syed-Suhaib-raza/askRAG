import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer


class VectorRetriever:
    def __init__(
        self,
        index_path="processed_data/vector_index/faiss_index.bin",
        metadata_path="processed_data/embeddings/chunk_embeddings/chunk_metadata.json",
        model_name="sentence-transformers/all-MiniLM-L6-v2",
    ):
        self.index = faiss.read_index(index_path)

        with open(metadata_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

        self.model = SentenceTransformer(model_name)

    def retrieve(self, query, top_k=10):
        query_embedding = self.model.encode([query]).astype("float32")

        scores, indices = self.index.search(query_embedding, top_k)

        results = []

        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue

            chunk = self.metadata[int(idx)]

            results.append(
                {
                    "chunk_id": chunk["chunk_id"],
                    "score": float(score),
                    "text": chunk["text"],
                    "section_id": chunk["section_id"],
                    "page_id": chunk["page_id"],
                }
            )

        return results