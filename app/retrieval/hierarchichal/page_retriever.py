import json
import numpy as np
from sentence_transformers import SentenceTransformer


class PageRetriever:

    def __init__(
        self,
        index_path="processed_data/embeddings/page_embeddings/page_metadata.json",
        embedding_path="processed_data/embeddings/page_embeddings/page_embeddings.npy",
        model_name="sentence-transformers/all-MiniLM-L6-v2",
    ):

        with open(index_path, "r", encoding="utf-8") as f:
            self.pages = json.load(f)

        self.embeddings = np.load(embedding_path)

        self.model = SentenceTransformer(model_name)

        print("pages:", len(self.pages))
        print("embeddings:", self.embeddings.shape)


    def retrieve(self, query, top_k=5):

        query_embedding = self.model.encode(query)
        query_embedding = np.array(query_embedding).reshape(-1)

        scores = np.dot(self.embeddings, query_embedding).flatten()

        top_ids = np.argsort(scores)[::-1][:top_k]

        results = []

        for idx in top_ids:

            idx = int(idx)

            metadata = self.pages[idx]

            results.append(
                {
                    "page_id": metadata["page_id"],   # wikipedia id
                    "title": metadata["title"],
                    "score": float(scores[idx]),
                }
            )

        return results