import json
import numpy as np
from sentence_transformers import SentenceTransformer


class SectionRetriever:

    def __init__(
        self,
        index_path="processed_data/embeddings/section_embeddings/section_metadata.json",
        embedding_path="processed_data/embeddings/section_embeddings/section_embeddings.npy",
        model_name="sentence-transformers/all-MiniLM-L6-v2",
    ):

        with open(index_path, "r", encoding="utf-8") as f:
            self.sections = json.load(f)

        self.embeddings = np.load(embedding_path)

        self.model = SentenceTransformer(model_name)

        # sanity check
        print("sections:", len(self.sections))
        print("embeddings:", self.embeddings.shape)


    def retrieve(self, query, page_ids, top_k=5):

        # handle both formats (ids or page dicts)
            if isinstance(page_ids[0], dict):
                page_ids = {p["page_id"] for p in page_ids}
            else:
                page_ids = set(page_ids)

            query_embedding = self.model.encode([query])[0]

            query_embedding = query_embedding / np.linalg.norm(query_embedding)
            embeddings = self.embeddings / np.linalg.norm(self.embeddings, axis=1, keepdims=True)

            scores = np.dot(embeddings, query_embedding)

            ranked = np.argsort(scores)[::-1]

            results = []

            for idx in ranked:

                idx = int(idx)

                if idx >= len(self.sections):
                    continue

                section = self.sections[idx]

                if section["page_id"] in page_ids:

                    results.append(
                        {
                            "section_id": section["section_id"],
                            "page_id": section["page_id"],
                            "title": section["title"],
                            "score": float(scores[idx]),
                        }
                    )

                if len(results) >= top_k:
                    break

            return results