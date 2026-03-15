import os
import json
from tqdm import tqdm

PAGES_DIR = "processed_data/pages"
OUTPUT_DIR = "processed_data/page_index"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "page_index.json")


def load_pages():
    """
    Load all page files from processed_data/pages
    """
    pages = []

    for file in os.listdir(PAGES_DIR):
        if file.endswith(".json"):
            path = os.path.join(PAGES_DIR, file)

            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                pages.append(data)

    return pages


def build_index(pages):
    """
    Build page lookup index
    """
    page_index = {}

    for page in tqdm(pages, desc="Indexing pages"):

        page_id = page.get("page_id")
        title = page.get("title")

        page_index[page_id] = {
            "title": title,
            "file": f"{page_id}.json"
        }

    return page_index


def save_index(index):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)


def main():

    print("Loading pages...")
    pages = load_pages()

    print(f"{len(pages)} pages loaded")

    print("Building page index...")
    page_index = build_index(pages)

    print("Saving index...")
    save_index(page_index)

    print("Page index built successfully")


if __name__ == "__main__":
    main()