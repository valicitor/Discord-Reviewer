from domain import DataNormalization, ExtractingData, MessyTextDataExtractor, VerificationToken
from config import VERIFICATION_SECRET 


class ClusterManager:

    def __init__(self, bot):
        self.bot = bot

    async def extract_and_cluster(
            self, ctx, submission) -> tuple[str, str, dict[str, list[dict[str, str]]] | None]:
        extractor = ExtractingData(self.bot)
        list_content, source, url, error = await extractor.extract_content(
            submission, ctx)

        if error:
            return None
        
        token = VerificationToken(VERIFICATION_SECRET).generate("".join(list_content) if list_content else "")

        normalizer = DataNormalization()
        clustered_data: dict[str, list[dict[str, str]]] = {}
        if list_content:
            if isinstance(list_content, str):
                list_content = [list_content]

            idx: int = 0
            for c in list_content:
                clean_content = normalizer.remove_discord_markdown(c)
                clean_content = normalizer.remove_headers_footers(
                    clean_content)
                clean_content = normalizer.remove_unicode_artifacts(
                    clean_content)

                segments: list[str] = [
                    line.strip() for line in clean_content.splitlines()
                    if line and line.strip()
                ]

                messyTextDataExtractor = MessyTextDataExtractor(1, 5)
                raw_hierarchy = messyTextDataExtractor.build_hierarchy(
                    segments)
                cleaned_hierarchy = messyTextDataExtractor.merge_inline_headers(
                    raw_hierarchy)

                clustered_data[f"post_{idx}"] = cleaned_hierarchy
                idx += 1

        return source, token, clustered_data

    async def find_fields(
        self,
        data: dict,
        field_names: list[str] = [],
        post_key: str = "post_0"
    ) -> list[str] | None:
        if not data or not field_names:
            return None

        found_sections: list[str] = []
        fallback_sections: list[str] = []
        post_sections = data.get(post_key, [])

        for section in post_sections:
            header = section.get("header", "").strip()
            header_lower = header.lower()

            for field_name in field_names:
                field_name_lower = field_name.strip().lower()

                # Case 1: Header contains the field name
                if field_name_lower in header_lower:
                    if section.get("content"):
                        found_sections.extend(section["content"])
                    elif section.get("table"):
                        # Pull out values from tables if header matches
                        for row in section["table"]:
                            for k, v in row.items():
                                found_sections.append(f"{k}: {v}")
                    else:
                        fallback_sections.append(header)

                # Case 2: Look inside subsections
                for subsection in section.get("subsections", []):
                    subheader = subsection.get("subheader", "").strip()
                    subheader_lower = subheader.lower()

                    if field_name_lower in subheader_lower:
                        if subsection.get("content"):
                            found_sections.extend(subsection["content"])
                        elif subsection.get("table"):
                            for row in subsection["table"]:
                                for k, v in row.items():
                                    found_sections.append(f"{k}: {v}")
                        else:
                            fallback_sections.append(subheader)

                # Case 3: Look inside tables directly for key matches
                if section.get("table"):
                    for row in section["table"]:
                        for k, v in row.items():
                            if field_name_lower == k.strip().lower():
                                found_sections.append(str(v))

        # Return content if found, else fallback headers/subheaders, else None
        return found_sections or fallback_sections or None

    async def extract_starting_abilities(
        self,
        data: dict,
        post_key: str = "post_0"
    ) -> tuple[dict, list[dict]]:

        if not data or post_key not in data:
            return data, []

        post_sections = data[post_key]
        abilities = []
        cleaned_sections = []
        i = 0

        while i < len(post_sections):
            section = post_sections[i]

            # Look for an ABILITY NAME header followed by a DESCRIPTION section
            if section.get("header", "").strip().lower() == "ability name":
                ability = {}

                # Peek ahead for description
                if i + 1 < len(post_sections) and post_sections[i + 1].get("header", "").strip().lower() == "description":
                    desc_section = post_sections[i + 1]
                    for subsection in desc_section.get("subsections", []):
                        key = subsection.get("subheader", "").replace(":", "").strip().lower()
                        val = " ".join(subsection.get("content", [])).strip()
                        ability[key] = val
                    abilities.append(ability)
                    i += 2  # Skip both ABILITY NAME and DESCRIPTION
                    continue

            # Otherwise, keep section
            cleaned_sections.append(section)
            i += 1

        # Replace with cleaned data
        cleaned_data = dict(data)
        cleaned_data[post_key] = cleaned_sections
        return cleaned_data, abilities