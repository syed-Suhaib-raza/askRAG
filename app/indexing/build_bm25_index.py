import os
import json
import pickle
from tqdm import tqdm
from rank_bm25 import BM25Okapi


PAGES_DIR = "processed_data/pages"
SECTIONS_DIR = "processed_data/sections_filtered"
OUTPUT_DIR = "processed_data/bm25_index"


def tokenize(text):
    return text.lower().split()


def load_documents(directory, text_field="text"):

    documents = []
    ids = []

    files = os.listdir(directory)

    for file in tqdm(files, desc=f"Loading {directory}"):

        if not file.endswith(".json"):
            continue

        path = os.path.join(directory, file)

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        text = data.get(text_field, "")

        tokens = tokenize(text)

        documents.append(tokens)

        if "page_id" in data:
            ids.append(data["page_id"])
        elif "section_id" in data:
            ids.append(data["section_id"])

    return documents, ids


def build_bm25(documents):

    bm25 = BM25Okapi(documents)

    return bm25


def save_index(index, ids, name):

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    index_path = os.path.join(OUTPUT_DIR, f"{name}.pkl")
    ids_path = os.path.join(OUTPUT_DIR, f"{name}_ids.pkl")

    with open(index_path, "wb") as f:
        pickle.dump(index, f)

    with open(ids_path, "wb") as f:
        pickle.dump(ids, f)


def main():

    print("Building page BM25 index...")

    page_docs, page_ids = load_documents(PAGES_DIR)
    page_bm25 = build_bm25(page_docs)

    save_index(page_bm25, page_ids, "page_bm25")

    print("Page BM25 built")

    print("Building section BM25 index...")

    section_docs, section_ids = load_documents(SECTIONS_DIR)
    section_bm25 = build_bm25(section_docs)

    save_index(section_bm25, section_ids, "section_bm25")

    print("Section BM25 built")


if __name__ == "__main__":
    main()