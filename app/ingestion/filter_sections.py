import json
from pathlib import Path

INPUT_DIR = Path("processed_data/sections")
OUTPUT_DIR = Path("processed_data/sections_filtered")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

REMOVE_SECTIONS = {
    "references",
    "external links",
    "see also",
    "further reading",
    "bibliography",
    "sources",
    "notes",
    "citations"
}


def filter_sections():

    kept = 0
    removed = 0

    print("Filtering sections...")

    for file in INPUT_DIR.glob("*.json"):

        with open(file, "r", encoding="utf-8") as f:
            section = json.load(f)

        title = section["section_title"].lower()

        if title in REMOVE_SECTIONS:
            removed += 1
            continue

        if len(section["text"].strip()) < 200:
            removed += 1
            continue

        output_file = OUTPUT_DIR / file.name

        with open(output_file, "w", encoding="utf-8") as out:
            json.dump(section, out, ensure_ascii=False)

        kept += 1

        if kept % 1000 == 0:
            print(f"Kept {kept} sections")

    print(f"\nFinished filtering")
    print(f"Kept: {kept}")
    print(f"Removed: {removed}")


if __name__ == "__main__":
    filter_sections()