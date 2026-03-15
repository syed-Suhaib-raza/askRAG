import bz2
import json
from pathlib import Path
import mwxml

DUMP_PATH = "data/wikipedia_dump/enwiki-latest-pages-articles.xml.bz2"
OUTPUT_DIR = Path("data/extracted_articles")

MAX_ARTICLES = 10000
ARTICLES_PER_FILE = 500


def extract_wikipedia():

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    article_count = 0
    file_index = 0
    buffer = []

    print("Starting Wikipedia extraction...")

    with bz2.open(DUMP_PATH) as dump_file:
        dump = mwxml.Dump.from_file(dump_file)

        for page in dump:

            # Only main namespace (actual articles)
            if page.namespace != 0:
                continue

            # Skip redirects
            if page.redirect:
                continue

            revision = next(page, None)
            if revision is None:
                continue

            text = revision.text
            if not text or len(text.strip()) < 200:
                continue

            article = {
                "id": page.id,
                "title": page.title,
                "text": text
            }

            buffer.append(article)
            article_count += 1

            # Write batch
            if len(buffer) >= ARTICLES_PER_FILE:
                output_file = OUTPUT_DIR / f"articles_{file_index}.jsonl"

                with open(output_file, "w", encoding="utf-8") as f:
                    for a in buffer:
                        f.write(json.dumps(a, ensure_ascii=False) + "\n")

                print(f"Saved {output_file} | Total articles: {article_count}")

                buffer = []
                file_index += 1

            # Stop at 10k
            if article_count >= MAX_ARTICLES:
                break

    print(f"\nFinished extracting {article_count} articles.")


if __name__ == "__main__":
    extract_wikipedia()