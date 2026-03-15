import json
from pathlib import Path

INPUT_DIR = Path("processed_data/sections_filtered")
OUTPUT_DIR = Path("processed_data/chunks")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CHUNK_SIZE = 200
CHUNK_OVERLAP = 50


def build_context(section, chunk_text):
    """
    Add contextual information to improve embedding quality
    """

    context = (
        f"Article: {section['title']}\n"
        f"Section: {section['section_title']}\n\n"
        f"{chunk_text}"
    )

    return context


def split_chunks(text):
    """
    Split text into overlapping chunks
    """

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + CHUNK_SIZE

        chunk_words = words[start:end]

        chunk = " ".join(chunk_words)

        chunks.append(chunk)

        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


def build_chunks():

    chunk_count = 0

    print("Chunking sections with contextual metadata...")

    for file in INPUT_DIR.glob("*.json"):

        with open(file, "r", encoding="utf-8") as f:
            section = json.load(f)

        text_chunks = split_chunks(section["text"])

        for i, chunk in enumerate(text_chunks):

            context = build_context(section, chunk)

            chunk_data = {
                "chunk_id": f"{section['section_id']}_{i}",
                "page_id": section["page_id"],
                "section_id": section["section_id"],
                "title": section["title"],
                "section_title": section["section_title"],
                "text": chunk,
                "context": context
            }

            output_file = OUTPUT_DIR / f"chunk_{chunk_count}.json"

            with open(output_file, "w", encoding="utf-8") as out:
                json.dump(chunk_data, out, ensure_ascii=False)

            chunk_count += 1

            if chunk_count % 1000 == 0:
                print(f"Created {chunk_count} chunks")

    print(f"\nFinished creating {chunk_count} chunks")


if __name__ == "__main__":
    build_chunks()