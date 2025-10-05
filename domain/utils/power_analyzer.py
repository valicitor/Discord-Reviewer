import re
from typing import List, Tuple
from resources import MECHANIC_KEYWORDS, NEGATION_WORDS

class PowerAnalyzer:
    def __init__(self, mechanic_keywords: dict = MECHANIC_KEYWORDS):
        self.mechanic_keywords = mechanic_keywords
        self.axis_names = sorted(
            {axis for kw_data in mechanic_keywords.values() for axis in kw_data["axes"]}
        )
        # Simple stopword list
        self.stop_words = set([
            "the", "a", "an", "and", "or", "is", "of", "to", "in", "on", "with", "for", "by", "as", "at"
        ])
        self.negation_words = set(NEGATION_WORDS)

    def preprocess(self, text: str) -> List[str]:
        # Lowercase, remove punctuation, split into tokens
        text = re.sub(r"[^\w\s]", " ", text.lower())
        tokens = text.split()
        tokens = [t for t in tokens if t not in self.stop_words]
        return tokens

    def generate_ngrams(self, tokens: List[str], n: int = 3) -> List[str]:
        ngrams_list = []
        for i in range(len(tokens)):
            for size in range(1, n+1):
                if i + size <= len(tokens):
                    ngram = "_".join(tokens[i:i+size])
                    ngrams_list.append(ngram)
        return ngrams_list

    def analyze(self, ability_text: str) -> List[Tuple[str, float]]:
        sentences = re.split(r"[.!?]\s*", ability_text)
        axis_scores = {axis: 0.0 for axis in self.axis_names}
        NEGATION_WINDOW = 3

        for sent in sentences:
            tokens = self.preprocess(sent)
            ngram_tokens = self.generate_ngrams(tokens, n=3)
            i = 0
            while i < len(ngram_tokens):
                match_found = False
                for kw, kw_data in sorted(self.mechanic_keywords.items(), key=lambda x: -len(x[0].split())):
                    kw_key = kw.replace(" ", "_")
                    if ngram_tokens[i] == kw_key:
                        weight = kw_data["weight"]
                        # negation check
                        window_start = max(0, i-NEGATION_WINDOW)
                        if any(t in self.negation_words for t in ngram_tokens[window_start:i]):
                            weight *= -1
                        for axis in kw_data["axes"]:
                            axis_scores[axis] += weight
                        i += 1
                        match_found = True
                        break
                if not match_found:
                    i += 1

        # normalize 0-10
        max_score = max(axis_scores.values()) or 1.0
        for axis in axis_scores:
            axis_scores[axis] = round(min(10.0, axis_scores[axis] / max_score * 10), 1)

        return [(axis, axis_scores[axis]) for axis in self.axis_names]