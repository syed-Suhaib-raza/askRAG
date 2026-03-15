import pickle


class BM25Retriever:
    def __init__(
        self,
        bm25_path="processed_data/bm25_index/page_bm25.pkl",
        ids_path="processed_data/bm25_index/page_bm25_ids.pkl",
        metadata_path="processed_data/pages/page_index.json",
    ):

        with open(bm25_path, "rb") as f:
            self.bm25 = pickle.load(f)

        with open(ids_path, "rb") as f:
            self.ids = pickle.load(f)

        import json
        with open(metadata_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

    def retrieve(self, query, top_k=10):

        tokenized_query = query.split()

        scores = self.bm25.get_scores(tokenized_query)

        ranked = sorted(
            list(enumerate(scores)),
            key=lambda x: x[1],
            reverse=True
        )[:top_k]

        results = []

        for idx, score in ranked:

            page_id = self.ids[idx]
            page = self.metadata[page_id]

            results.append(
                {
                    "page_id": page_id,
                    "title": page["title"],
                    "score": float(score)
                }
            )

        return results