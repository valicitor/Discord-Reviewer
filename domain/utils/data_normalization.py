import re
import unicodedata
from resources import HEADER_FOOTER_PHRASES

class DataNormalization:
    def __init__(self):
        pass

    def remove_headers_footers(self, text: str) -> str:
        if not text:
            return ""

        for phrase in HEADER_FOOTER_PHRASES:
            words = phrase.split()
            pattern = r'\s*'.join(re.escape(word) + r'.*?' for word in words)
            text = re.sub(pattern, ' ', text, flags=re.IGNORECASE | re.DOTALL)

        return text

    def remove_discord_markdown(self, text: str) -> str:
        # Remove Markdown bold/italic formatting
        text = re.sub(r'\*\*', '', text)
        text = re.sub(r'__', '', text)
        text = re.sub(r'\*', '', text)
        text = re.sub(r'`', '', text)

        # Remove # and > symbols, but keep the text
        text = re.sub(r'[>#|]', '', text)

        return text

    def remove_unicode_artifacts(self, text: str) -> str:
        if not text:
            return ""

        # Normalize the text (NFKC) to simplify some Unicode forms
        text = unicodedata.normalize('NFKC', text)

        # Remove emojis and pictographs
        emoji_pattern = re.compile(
            "["
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F700-\U0001F77F"  # alchemical symbols
            "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
            "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
            "\U0001F900-\U0001F9FF"  # Supplemental Symbols & Pictographs
            "\U0001FA00-\U0001FA6F"  # Chess Symbols, Symbols & Pictographs Extended-A
            "\U0001FA70-\U0001FAFF"  # Symbols & Pictographs Extended-B
            "\u2600-\u26FF"          # Misc symbols
            "\u2700-\u27BF"          # Dingbats
            "]+", flags=re.UNICODE
        )
        text = emoji_pattern.sub("", text)

        # Remove box-drawing and block elements
        text = re.sub(r'[\u2580-\u259F\u25A0-\u25FF]', '', text)

        # Remove zero-width characters (invisible formatting marks)
        text = re.sub(r'[\u200B-\u200D\uFEFF]', '', text)

        text = re.sub(r'[《》]', '', text)

        return text.strip()

    def preserve_sentence_structure(self, text: str) -> str:
        if not text:
            return ""

        # Replace each line break with a period and space
        return text.replace('\n', '. ').replace('\r', '. ')

    def normalize_whitespace(self, text: str) -> str:
        if not text:
            return ""

        # Collapse "...." into "."
        text = re.sub(r'\.{2,}', '.', text)

        # Remove stray " . " (or multiple spaced periods)
        text = re.sub(r'(\s*\.\s*){2,}', '. ', text)

        # Normalize spacing around colons
        text = re.sub(r'\s*:\s*', ': ', text)

        # Fix decimals (x1.5 not x1 5)
        text = re.sub(r'(\d+)\.\s*(\d+)', r'\1.\2', text)

        # Ensure one space after sentence-ending periods
        text = re.sub(r'\.\s*([A-Za-z])', r'. \1', text)

        # Ensure single spaces after commas/semicolons/etc.
        text = re.sub(r'\s*([,!?;])\s*', r'\1 ', text)

        # Collapse any leftover whitespace
        text = re.sub(r'\s+', ' ', text)

        # Strip leading/trailing junk
        return text.strip()

    def normalize_case(self, text: str) -> str:
        if not text:
            return ""

        # Simple lowercase approach
        text = text.lower()

        # Capitalize first letter
        if text:
            text = text[0].upper() + text[1:]

        # Capitalize sentences
        text = re.sub(r'([.!?]\s+)([a-z])', 
                     lambda match: match.group(1) + match.group(2).upper(), text)

        return text

    def normalize(self, text: str) -> str:
        if not text or not text.strip():
            return ""

        steps = [
            self.preserve_sentence_structure,
            self.remove_headers_footers,
            self.remove_unicode_artifacts,
            self.normalize_whitespace,
            self.normalize_case
        ]

        normalized_text = text
        for step in steps:
            normalized_text = step(normalized_text)
            if not normalized_text:
                return ""

        return normalized_text