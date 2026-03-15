import os
import json
from tqdm import tqdm

SECTIONS_DIR = "processed_data/sections_filtered"
OUTPUT_DIR = "processed_data/section_index"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "section_index.json")


def load_sections():
    """
    Load all section files from processed_data/sections
    """
    sections = []

    for file in os.listdir(SECTIONS_DIR):
        if file.endswith(".json"):
            path = os.path.join(SECTIONS_DIR, file)

            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                sections.append(data)

    return sections


def build_index(sections):
    """
    Build section lookup index
    """
    section_index = {}

    for section in tqdm(sections, desc="Indexing sections"):

        section_id = section.get("section_id")
        page_id = section.get("page_id")
        title = section.get("title")

        section_index[section_id] = {
            "page_id": page_id,
            "title": title,
            "file": f"{section_id}.json"
        }

    return section_index


def save_index(index):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)


def main():

    print("Loading sections...")
    sections = load_sections()

    print(f"{len(sections)} sections loaded")

    print("Building section index...")
    section_index = build_index(sections)

    print("Saving section index...")
    save_index(section_index)

    print("Section index built successfully")


if __name__ == "__main__":
    main()