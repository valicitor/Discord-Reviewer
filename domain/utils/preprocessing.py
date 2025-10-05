import re
from typing import List
import nltk
from domain.utils.data_normalization import DataNormalization
from resources import FILLER_PHRASES, MECHANIC_KEYWORDS, VALID_VERBS

class Preprocessing:
    def __init__(self, min_words_per_sentence: int = 3, max_sentence_length: int = 25):
        self.min_words = min_words_per_sentence
        self.max_length = max_sentence_length
        self.normalizer = DataNormalization()
        self.conj_splitter = re.compile(r'\s+(?:and|but|or|however|because|although|if|when|while)\s+', re.IGNORECASE)

    def clean_content(self, content: str) -> str:
        if not content:
            return ""

        # Remove obvious headers and formatting artifacts
        content = re.sub(r'\b(name|ability type|multiplier|consequence|extra effect|description)+(?:s)?\s*(?:[:\-\=\-\>\n\.])*\s*\b', 
                        '', content, flags=re.IGNORECASE | re.MULTILINE)

        # Clean up common filler phrases
        for phrase in FILLER_PHRASES:
            content = re.sub(phrase, '', content, flags=re.IGNORECASE)

        content = self.normalizer.normalize_whitespace(content)
        content = self.normalizer.normalize_case(content)
        
        return content

    def split_into_meaningful_chunks(self, text: str) -> List[str]:
        if not text or len(text.split()) < self.min_words:
            return []

        # Use nltk for sentence tokenization
        try:
            sentences = nltk.sent_tokenize(text)
        except:
            # Fallback: split on punctuation
            sentences = re.split(r'[\.\!\?\:\;\(\)\|\[\]]+', text)
            sentences = [s.strip() for s in sentences if s.strip()]

        chunks = []

        for sentence in sentences:
            words = sentence.split()

            # Skip very short fragments
            if len(words) < self.min_words:
                continue

            # Split long sentences on conjunctions
            if len(words) > self.max_length:
                for chunk in self.conj_splitter.split(sentence):
                    chunk = chunk.strip()
                    if chunk and len(chunk.split()) >= self.min_words:
                        chunks.append(chunk)
            else:
                chunks.append(sentence.strip())

        return chunks


    def is_meaningful_chunk(self, chunk: str) -> bool:
        words = chunk.lower().split()

        if len(words) < self.min_words:
            return False

        # Skip all-caps headers
        if chunk.upper() == chunk and len(words) < 5:
            return False

        # Look for action indicators
        action_indicators = {
            'creates', 'uses', 'attacks', 'moves', 'leaves', 'reveals', 
            'forces', 'phases', 'render', 'immune', 'cannot', 'depletes',
            'risks', 'exploit', 'prepare', 'reposition', 'interact', 'focus',
            'increases', 'decreases', 'affects', 'causes', 'prevents',
            'allows', 'requires', 'becomes', 'makes', 'takes', 'gives',
            'maintaining', 'detach', 'pass', 'touch', 'work', 'reduced'
        }

        chunk_lower = chunk.lower()
        has_action = any(indicator in chunk_lower for indicator in action_indicators)
        has_verbs = any(word in VALID_VERBS for word in words)
        has_mechanics = any(keyword in chunk_lower for keyword in MECHANIC_KEYWORDS)

        return has_action or has_verbs or has_mechanics or len(words) >= 4

    def preprocess_chunks(self, all_chunks: List[str]) -> List[str]:
        if not all_chunks:
            return all_chunks

        meaningful_chunks = [c for c in all_chunks if self.is_meaningful_chunk(c)]
        return meaningful_chunks

    def preprocess(self, text: str) -> List[str]:
        all_chunks = []

        if not text or not text.strip():
            return all_chunks

        cleaned = self.clean_content(text)
        all_chunks = self.split_into_meaningful_chunks(cleaned)

        return self.preprocess_chunks(all_chunks)
        
    def aggressive_pass(self, meaningful_chunks: List[str]) -> List[str]:
        if not meaningful_chunks:
            return []

        # Deduplicate and limit output for aggressive processing
        unique_chunks = []
        seen_content = set()

        for chunk in meaningful_chunks:
            chunk_simple = re.sub(r'[^\w\s]', '', chunk.lower())
            words = frozenset(w for w in chunk_simple.split() if len(w) > 2)

            if words and words not in seen_content and len(words) >= 3:
                unique_chunks.append(chunk)
                seen_content.add(words)

        return unique_chunks