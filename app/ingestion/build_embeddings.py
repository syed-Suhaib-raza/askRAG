import json
import numpy as np
import torch
from pathlib import Path
from sentence_transformers import SentenceTransformer
from tqdm import tqdm


# Input directories
PAGES_DIR = Path("processed_data/pages")
SECTIONS_DIR = Path("processed_data/sections_filtered")
CHUNKS_DIR = Path("processed_data/deduplicated_chunks")

# Output directories
BASE_EMBED_DIR = Path("processed_data/embeddings")

PAGE_EMBED_DIR = BASE_EMBED_DIR / "page_embeddings"
SECTION_EMBED_DIR = BASE_EMBED_DIR / "section_embeddings"
CHUNK_EMBED_DIR = BASE_EMBED_DIR / "chunk_embeddings"

PAGE_EMBED_DIR.mkdir(parents=True, exist_ok=True)
SECTION_EMBED_DIR.mkdir(parents=True, exist_ok=True)
CHUNK_EMBED_DIR.mkdir(parents=True, exist_ok=True)


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
BATCH_SIZE = 64


def load_model():

    device = "cuda" if torch.cuda.is_available() else "cpu"

    print(f"Loading embedding model on {device}...")

    model = SentenceTransformer(MODEL_NAME, device=device)

    return model


def embed_pages(model):

    texts = []
    metadata = []

    print("\nPreparing page texts...")

    for file in tqdm(list(PAGES_DIR.glob("*.json"))):

        with open(file, "r", encoding="utf-8") as f:
            page = json.load(f)

        text = f"Title: {page['title']}\n\n{page['text'][:2000]}"

        texts.append(text)

        metadata.append({
            "page_id": page["page_id"],
            "title": page["title"]
        })

    print("Embedding pages...")

    embeddings = model.encode(
        texts,
        batch_size=BATCH_SIZE,
        show_progress_bar=True
    )

    np.save(PAGE_EMBED_DIR / "page_embeddings.npy", embeddings)

    with open(PAGE_EMBED_DIR / "page_metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f)

    print(f"Saved {len(embeddings)} page embeddings")


def embed_sections(model):

    texts = []
    metadata = []

    print("\nPreparing section texts...")

    for file in tqdm(list(SECTIONS_DIR.glob("*.json"))):

        with open(file, "r", encoding="utf-8") as f:
            section = json.load(f)

        text = (
            f"Article: {section['title']}\n"
            f"Section: {section['section_title']}\n\n"
            f"{section['text']}"
        )

        texts.append(text)
        metadata.append(section)

    print("Embedding sections...")

    embeddings = model.encode(
        texts,
        batch_size=BATCH_SIZE,
        show_progress_bar=True
    )

    np.save(SECTION_EMBED_DIR / "section_embeddings.npy", embeddings)

    with open(SECTION_EMBED_DIR / "section_metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f)

    print(f"Saved {len(embeddings)} section embeddings")


def embed_chunks(model):

    texts = []
    metadata = []

    print("\nPreparing chunk texts...")

    for file in tqdm(list(CHUNKS_DIR.glob("*.json"))):

        with open(file, "r", encoding="utf-8") as f:
            chunk = json.load(f)

        texts.append(chunk["context"])
        metadata.append(chunk)

    print("Embedding chunks...")

    embeddings = model.encode(
        texts,
        batch_size=BATCH_SIZE,
        show_progress_bar=True
    )

    np.save(CHUNK_EMBED_DIR / "chunk_embeddings.npy", embeddings)

    with open(CHUNK_EMBED_DIR / "chunk_metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f)

    print(f"Saved {len(embeddings)} chunk embeddings")


def build_embeddings():

    model = load_model()

    embed_pages(model)
    embed_sections(model)
    embed_chunks(model)

    print("\nEmbedding pipeline complete.")


if __name__ == "__main__":
    build_embeddings()