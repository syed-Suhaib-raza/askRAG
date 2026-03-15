import json
import hashlib
from pathlib import Path

INPUT_DIR = Path("processed_data/chunks")
OUTPUT_DIR = Path("processed_data/deduplicated_chunks")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def hash_text(text):
    """
    Create a stable hash for chunk text
    """
    return hashlib.md5(text.strip().encode("utf-8")).hexdigest()


def deduplicate_chunks():

    seen_hashes = set()

    kept = 0
    removed = 0

    print("Deduplicating chunks...")

    for file in INPUT_DIR.glob("*.json"):

        with open(file, "r", encoding="utf-8") as f:
            chunk = json.load(f)

        text_hash = hash_text(chunk["text"])

        if text_hash in seen_hashes:
            removed += 1
            continue

        seen_hashes.add(text_hash)

        output_file = OUTPUT_DIR / file.name

        with open(output_file, "w", encoding="utf-8") as out:
            json.dump(chunk, out, ensure_ascii=False)

        kept += 1

        if kept % 1000 == 0:
            print(f"Kept {kept} chunks")

    print("\nDeduplication complete")
    print(f"Chunks kept: {kept}")
    print(f"Chunks removed: {removed}")


if __name__ == "__main__":
    deduplicate_chunks()