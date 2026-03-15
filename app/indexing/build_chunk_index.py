import os
import json
from tqdm import tqdm

CHUNKS_DIR = "processed_data/deduplicated_chunks"
OUTPUT_DIR = "processed_data/chunk_index"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "chunk_index.json")


def load_chunks():
    """
    Load chunk metadata from deduplicated chunks
    """
    chunks = []

    for file in os.listdir(CHUNKS_DIR):
        if file.endswith(".json"):

            path = os.path.join(CHUNKS_DIR, file)

            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                chunks.append(data)

    return chunks


def build_index(chunks):
    """
    Build chunk index mapping vector ids to chunk metadata
    """

    chunk_index = {}

    for vector_id, chunk in enumerate(tqdm(chunks, desc="Indexing chunks")):

        chunk_id = chunk.get("chunk_id")
        section_id = chunk.get("section_id")
        page_id = chunk.get("page_id")

        chunk_index[vector_id] = {
            "chunk_id": chunk_id,
            "section_id": section_id,
            "page_id": page_id,
            "file": f"{chunk_id}.json"
        }

    return chunk_index


def save_index(index):

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)


def main():

    print("Loading chunks...")
    chunks = load_chunks()

    print(f"{len(chunks)} chunks loaded")

    print("Building chunk index...")
    chunk_index = build_index(chunks)

    print("Saving chunk index...")
    save_index(chunk_index)

    print("Chunk index built successfully")


if __name__ == "__main__":
    main()