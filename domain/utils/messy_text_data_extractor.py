import re
from typing import List, Dict, Any, Tuple


class MessyTextDataExtractor:

    def __init__(self, min_header_len: int = 2, max_header_words: int = 8):
        self.min_header_len = min_header_len
        self.max_header_words = max_header_words

    def split_inline_subheader(self,
                               seg: str) -> Tuple[str | None, str | None]:
        if ":" in seg:
            first, rest = seg.split(":", 1)
            first, rest = first.strip(), rest.strip()
            if len(first.split()) <= self.max_header_words:
                return first + ":", rest
        return None, None

    def classify_segment(
            self, seg: str) -> Tuple[str | None, str | None, str | None]:
        seg = seg.strip()
        if not seg:
            return "EMPTY", None, None

        # Inline subheader check
        subheader, rest = self.split_inline_subheader(seg)
        if subheader and rest:
            return "INLINE_SUBHEADER", subheader, rest

        word_count = len(seg.split())
        ends_with_punct = seg[-1] in ".!?"

        # Short = more likely header/subheader
        if word_count <= self.max_header_words:
            if seg.isupper():
                return "HEADER", seg, None
            if seg.endswith(":") or re.match(r"^\d+(\.\d+)*[\)\.]?\s", seg):
                return "SUBHEADER", seg, None
            if not ends_with_punct:
                return "HEADER", seg, None

        # Default = content
        return "CONTENT", seg, None

    def build_hierarchy(self, segments: List[str]) -> List[Dict[str, Any]]:
        hierarchy = []
        current_section = None
        current_subsection = None

        for seg in segments:
            label, head_text, rest = self.classify_segment(seg)

            if label == "INLINE_SUBHEADER":
                if current_section is None:
                    # Top-level inline header
                    current_section = {
                        "header": head_text,
                        "subsections": [],
                        "content": []
                    }
                    if rest:
                        current_section["content"].append(rest)
                    hierarchy.append(current_section)
                    current_subsection = None
                else:
                    # Nested inline subheader
                    current_subsection = {
                        "subheader": head_text,
                        "content": []
                    }
                    if rest:
                        current_subsection["content"].append(rest)
                    current_section["subsections"].append(current_subsection)

            elif label == "HEADER":
                current_section = {
                    "header": head_text,
                    "subsections": [],
                    "content": []
                }
                hierarchy.append(current_section)
                current_subsection = None

            elif label == "SUBHEADER":
                if current_section is None:
                    current_section = {
                        "header": head_text,
                        "subsections": [],
                        "content": []
                    }
                    hierarchy.append(current_section)
                else:
                    current_subsection = {
                        "subheader": head_text,
                        "content": []
                    }
                    current_section["subsections"].append(current_subsection)

            elif label == "CONTENT":
                if current_subsection:
                    current_subsection["content"].append(head_text)
                elif current_section:
                    current_section["content"].append(head_text)
                else:
                    hierarchy.append({"content": [head_text]})

        return hierarchy

    def merge_inline_headers(self, hierarchy) -> List[Dict[str, Any]]:
        new_hierarchy = []
        i = 0

        while i < len(hierarchy):
            section = hierarchy[i]

            header = section.get("header")
            content = section.get("content", [])
            subsections = section.get("subsections", [])

            # Look for a key-value pair pattern: two consecutive headers
            if (i + 1 < len(hierarchy)
                and header is not None and not content and not subsections
                and hierarchy[i + 1].get("header") is not None
                and not hierarchy[i + 1].get("content", [])
                and not hierarchy[i + 1].get("subsections", [])):

                key = header
                value = hierarchy[i + 1]["header"]

                # If the "value" looks like a proper header/title, promote it
                if value.isupper() and len(value.split()) <= self.max_header_words:
                    new_hierarchy.append({
                        "header": value,
                        "subsections": [],
                        "table": [{key: value}]
                    })
                else:
                    # Otherwise, append as a table row to the previous section
                    if new_hierarchy and "table" in new_hierarchy[-1]:
                        new_hierarchy[-1]["table"].append({key: value})
                    elif new_hierarchy:
                        new_hierarchy[-1].setdefault("table", []).append({key: value})
                    else:
                        new_hierarchy.append({
                            "header": None,
                            "table": [{key: value}]
                        })

                i += 2  # Skip both key and value
                continue

            # Recurse into subsections if they exist
            if subsections:
                section["subsections"] = self.merge_inline_headers(subsections)

            new_hierarchy.append(section)
            i += 1

        return new_hierarchy
