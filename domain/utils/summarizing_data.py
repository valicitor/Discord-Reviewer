from typing import List
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from resources import MECHANIC_KEYWORDS
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer


class SummarizingData:
    def __init__(self):
        self.stop_words = set(stopwords.words("english"))

    def _compute_word_frequencies(self, text: str) -> Counter:
        words = [w.lower() for w in word_tokenize(text) if w.lower() not in self.stop_words]
        return Counter(words)

    def is_key_mechanic(self, sentence: str) -> bool:
        sentence_lower = sentence.lower()
        return any(keyword in sentence_lower for keyword in MECHANIC_KEYWORDS)

    def _score_sentence(self, sentence: str, word_freq: Counter) -> float:
        words = [w.lower() for w in word_tokenize(sentence) if w.lower() not in self.stop_words]
        if not words:
            return 0.0

        base_score = 0.0
        for w in words:
            freq_score = word_freq.get(w, 0)
            kw_data = MECHANIC_KEYWORDS.get(w)
            if kw_data:
                keyword_weight = kw_data.get("weight", 1.0)
            else:
                keyword_weight = 0.01  # default for non-keywords
            base_score += freq_score * keyword_weight

        base_score /= len(words)

        return base_score

    def _rank_sentences(self, sentences: List[str], word_freq: Counter) -> List[str]:
        scored = [(s, self._score_sentence(s, word_freq)) for s in sentences if s.strip()]
        scored.sort(key=lambda x: x[1], reverse=False)
        return [s for s, _ in scored]

    def summarize_text(self, text: str, sentence_count: int = 8, method="lsa") -> str:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))

        if method == "lsa":
            summarizer = LsaSummarizer()
        elif method == "lexrank":
            summarizer = LexRankSummarizer()
        else:
            raise ValueError("Unsupported method")

        summary_sentences = summarizer(parser.document, sentence_count)
        return " ".join(str(s) for s in summary_sentences)

    def summarize_bullet_points(self, micro_sentences: List[str], sentence_count: int = 6) -> List[str]:
        important_sentences = [s for s in micro_sentences if self.is_key_mechanic(s)]

        if not important_sentences:
            important_sentences = micro_sentences

        word_freq = self._compute_word_frequencies(" ".join(important_sentences))
        ranked_sentences = self._rank_sentences(important_sentences, word_freq)

        return ranked_sentences[:sentence_count]