import json
from pathlib import Path

INPUT_DIR = Path("data/extracted_articles")
OUTPUT_DIR = Path("processed_data/pages")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def parse_pages():

    page_count = 0

    print("Parsing pages...")

    for file in INPUT_DIR.glob("*.jsonl"):

        with open(file, "r", encoding="utf-8") as f:

            for line in f:

                article = json.loads(line)

                page = {
                    "page_id": article["id"],
                    "title": article["title"],
                    "text": article["text"],
                    "length": len(article["text"])
                }

                output_file = OUTPUT_DIR / f"page_{page_count}.json"

                with open(output_file, "w", encoding="utf-8") as out:
                    json.dump(page, out, ensure_ascii=False)

                page_count += 1

                if page_count % 1000 == 0:
                    print(f"Parsed {page_count} pages")

    print(f"Finished parsing {page_count} pages")


if __name__ == "__main__":
    parse_pages()