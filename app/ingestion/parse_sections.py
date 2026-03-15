import json
import re
from pathlib import Path

INPUT_DIR = Path("processed_data/pages")
OUTPUT_DIR = Path("processed_data/sections")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SECTION_PATTERN = re.compile(r"==+\s*(.*?)\s*==+")


def split_sections(text):

    matches = list(SECTION_PATTERN.finditer(text))

    if not matches:
        return [("Introduction", text)]

    sections = []

    # Intro before first section
    intro_end = matches[0].start()
    intro_text = text[:intro_end].strip()

    if intro_text:
        sections.append(("Introduction", intro_text))

    for i, match in enumerate(matches):

        title = match.group(1)

        start = match.end()

        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

        section_text = text[start:end].strip()

        if section_text:
            sections.append((title, section_text))

    return sections


def parse_sections():

    section_count = 0

    print("Parsing sections...")

    for file in INPUT_DIR.glob("*.json"):

        with open(file, "r", encoding="utf-8") as f:

            page = json.load(f)

            sections = split_sections(page["text"])

            for i, (section_title, section_text) in enumerate(sections):

                section = {
                    "section_id": f"{page['page_id']}_{i}",
                    "page_id": page["page_id"],
                    "title": page["title"],
                    "section_title": section_title,
                    "text": section_text
                }

                output_file = OUTPUT_DIR / f"section_{section_count}.json"

                with open(output_file, "w", encoding="utf-8") as out:
                    json.dump(section, out, ensure_ascii=False)

                section_count += 1

                if section_count % 1000 == 0:
                    print(f"Parsed {section_count} sections")

    print(f"Finished parsing {section_count} sections")


if __name__ == "__main__":
    parse_sections()