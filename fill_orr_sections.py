"""
ORR Document Section Filler
----------------------------
Takes a .docx template and a .txt file (JSON format) and produces a new .docx
with JSON values inserted into the specified sections.

Usage:
    python fill_orr_sections.py --docx XYZ_ORR.docx --json reviewer_input.txt --output XYZ_ORR_filled.docx

The mapping between JSON keys and document sections is defined in SECTION_MAPPING below.
To adapt to new templates or additional sections, simply edit this mapping — no other
code changes are needed.
"""

import json
import argparse
from copy import deepcopy
from pathlib import Path
from docx import Document
from docx.oxml.ns import qn


# =============================================================================
# CONFIGURATION: Section Mapping
# =============================================================================
# Each entry maps a JSON key (from the txt file) to the heading text in the docx.
# The script finds the heading and replaces the placeholder paragraph(s) after it
# with the content from the JSON. The JSON value can be:
#   - A string (single paragraph)
#   - A list of strings (multiple paragraphs)
#
# To add/change sections:
#   1. Add the new key to your JSON txt file
#   2. Add a new entry here: "json_key": "Exact Heading Text In Document"
#
# The heading match is case-insensitive and uses 'startswith' to handle minor
# variations (e.g., trailing spaces, parentheticals).
# =============================================================================

SECTION_MAPPING = {
    "section_1_review": "ORR Section 1",
    "section_2_review": "ORR Section 2",
    "conclusion_review": "Conclusion",
}


def load_json_data(json_path: str) -> dict:
    """Load and parse the JSON txt file."""
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def insert_paragraph_after(paragraph, text, style=None):
    """Insert a new paragraph directly after the given paragraph in the document body."""
    new_para_element = deepcopy(paragraph._element)
    # Clear all runs/content from the cloned element
    for child in list(new_para_element):
        if child.tag == qn('w:r'):
            new_para_element.remove(child)
    # Add a single run with the desired text
    from docx.oxml import OxmlElement
    run_elem = OxmlElement('w:r')
    # Copy run properties from the original first run if available
    if paragraph.runs:
        orig_rpr = paragraph.runs[0]._element.find(qn('w:rPr'))
        if orig_rpr is not None:
            run_elem.append(deepcopy(orig_rpr))
    text_elem = OxmlElement('w:t')
    text_elem.set(qn('xml:space'), 'preserve')
    text_elem.text = text
    run_elem.append(text_elem)
    new_para_element.append(run_elem)

    paragraph._element.addnext(new_para_element)
    return new_para_element


def find_and_fill_sections(doc: Document, data: dict, mapping: dict) -> dict:
    """
    Walk through document paragraphs, find section headings defined in the mapping,
    and replace the placeholder paragraph after each heading with the corresponding
    JSON value. Supports multi-paragraph content (JSON list of strings).

    Returns a dict of {section_heading: bool} indicating which sections were filled.
    """
    results = {heading: False for heading in mapping.values()}
    paragraphs = doc.paragraphs

    for json_key, heading_prefix in mapping.items():
        if json_key not in data:
            print(f"  WARNING: Key '{json_key}' not found in JSON data. Skipping.")
            continue

        content = data[json_key]
        # Normalize to list of paragraphs
        if isinstance(content, str):
            content_paragraphs = [content]
        elif isinstance(content, list):
            content_paragraphs = content
        else:
            print(f"  WARNING: Value for '{json_key}' is not a string or list. Skipping.")
            continue

        heading_prefix_lower = heading_prefix.lower()

        for i, para in enumerate(paragraphs):
            if (
                para.style.name.startswith("Heading")
                and para.text.strip().lower().startswith(heading_prefix_lower)
            ):
                # Find the first non-empty paragraph after the heading (the placeholder)
                for j in range(i + 1, len(paragraphs)):
                    if paragraphs[j].text.strip():
                        placeholder_para = paragraphs[j]

                        # Set the first paragraph text on the placeholder itself
                        placeholder_para.text = ""
                        if placeholder_para.runs:
                            for run in placeholder_para.runs:
                                run.text = ""
                        # Clear existing runs at XML level and add fresh content
                        from docx.oxml import OxmlElement
                        for child in list(placeholder_para._element):
                            if child.tag == qn('w:r'):
                                placeholder_para._element.remove(child)
                        run_elem = OxmlElement('w:r')
                        text_elem = OxmlElement('w:t')
                        text_elem.set(qn('xml:space'), 'preserve')
                        text_elem.text = content_paragraphs[0]
                        run_elem.append(text_elem)
                        placeholder_para._element.append(run_elem)

                        # Insert additional paragraphs after the first one (in reverse
                        # order since each insert goes right after the placeholder)
                        current_para = placeholder_para
                        for extra_text in content_paragraphs[1:]:
                            insert_paragraph_after(current_para, extra_text)
                            # Move reference to the newly inserted element
                            current_para_element = current_para._element.getnext()
                            # Wrap in a temporary object for next iteration
                            class _ParaRef:
                                def __init__(self, elem, runs_source):
                                    self._element = elem
                                    self.runs = runs_source.runs
                            current_para = _ParaRef(current_para_element, placeholder_para)

                        results[heading_prefix] = True
                        break
                break

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Fill specific sections in a .docx template with data from a JSON .txt file."
    )
    parser.add_argument("--docx", required=True, help="Path to the input .docx template")
    parser.add_argument("--json", required=True, help="Path to the .txt file containing JSON data")
    parser.add_argument("--output", default=None, help="Path for the output .docx (default: <input>_filled.docx)")
    parser.add_argument(
        "--mapping-file",
        default=None,
        help="Optional path to a JSON file defining section mappings (overrides built-in SECTION_MAPPING)",
    )

    args = parser.parse_args()

    if args.output is None:
        stem = Path(args.docx).stem
        args.output = f"{stem}_filled.docx"

    print(f"Input document : {args.docx}")
    print(f"JSON data file : {args.json}")
    print(f"Output document: {args.output}")
    print()

    # Load mapping (from external file or built-in)
    if args.mapping_file:
        with open(args.mapping_file, "r", encoding="utf-8") as f:
            mapping = json.load(f)
        print(f"Using external mapping from: {args.mapping_file}")
    else:
        mapping = SECTION_MAPPING
        print("Using built-in SECTION_MAPPING")

    print(f"Sections to fill: {list(mapping.values())}")
    print()

    # Load data
    data = load_json_data(args.json)
    print(f"JSON keys found: {list(data.keys())}")
    print()

    # Load document
    doc = Document(args.docx)

    # Fill sections
    results = find_and_fill_sections(doc, data, mapping)

    # Report
    print("Results:")
    for section, filled in results.items():
        status = "FILLED" if filled else "NOT FOUND/SKIPPED"
        print(f"  {section}: {status}")
    print()

    # Save
    doc.save(args.output)
    print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()
