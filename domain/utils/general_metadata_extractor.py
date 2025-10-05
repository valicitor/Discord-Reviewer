import re
from typing import Dict, List, Tuple
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


class GeneralMetadataExtractor:
    def __init__(self, section_patterns: Dict[str, List[str]], n_clusters: int = 5):
        self.n_clusters = n_clusters
        self.section_patterns = section_patterns

    def extract_structured_fields(self, text: str) -> Tuple[Dict[str, List[str]], str]:
        """Extracts structured fields using regex and returns the remaining free text."""
        sections: Dict[str, List[str]] = {k: [] for k in self.section_patterns.keys()}
        matched_spans = []

        for section, patterns in self.section_patterns.items():
            for pat in patterns:
                for m in re.finditer(pat, text, re.IGNORECASE | re.MULTILINE):
                    val = m.group(1)
                    if val is not None and val.strip():
                        sections[section].append(val.strip())
                        matched_spans.append((m.start(), m.end()))

        # Remove matched spans from text
        remaining_text = ''
        last_idx = 0
        for start, end in sorted(matched_spans):
            remaining_text += text[last_idx:start]
            last_idx = end
        remaining_text += text[last_idx:]

        return sections, remaining_text

    def cluster_free_text(self, free_text: str) -> Dict[str, List[str]]:
        """Tokenizes sentences and clusters them into semantic sections."""
        sections = {}
        sentences = sent_tokenize(free_text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if not sentences:
            return sections

        if len(sentences) == 1:
            sections['other_cluster_0'] = sentences
            return sections

        vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        X = vectorizer.fit_transform(sentences)

        n_clusters = min(self.n_clusters, len(sentences))
        kmeans = KMeans(n_clusters=n_clusters, n_init=5, random_state=0)
        labels = kmeans.fit_predict(X)

        clusters = {i: [] for i in range(n_clusters)}
        for label, sentence in zip(labels, sentences):
            clusters[label].append(sentence)

        for i, cluster_sentences in clusters.items():
            cluster_key = f'other_cluster_{i}'
            sections[cluster_key] = cluster_sentences

        return sections

    def extract(self, text: str) -> Dict[str, List[str]]:
        """Full extraction combining structured regex and semantic clustering."""
        sections, free_text = self.extract_structured_fields(text)
        free_sections = self.cluster_free_text(free_text)

        # Merge both
        for k, v in free_sections.items():
            if k in sections:
                sections[k].extend(v)
            else:
                sections[k] = v

        return sections
