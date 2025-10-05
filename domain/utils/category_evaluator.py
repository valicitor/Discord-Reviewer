import math
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk import pos_tag, ngrams
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from resources import MECHANIC_KEYWORDS

class CategoryEvaluator:
    def __init__(self, categories: list[dict[str, str]], mechanic_keywords: dict = MECHANIC_KEYWORDS):
        self.categories = categories
        self.prompts = [c["prompt"] for c in categories]
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words("english"))

        # Flatten keywords for boosting: lowercase -> numeric weight
        self.mechanic_keywords = {kw.lower(): data for kw, data in mechanic_keywords.items()}

        # Preprocess prompts
        self.preprocessed_prompts = [" ".join(self.preprocess(p)) for p in self.prompts]
        self.prompt_tokens_list = [self.preprocess(p) for p in self.prompts]

        # Fit vectorizer on prompts
        self.prompt_tfidf_matrix = self.vectorizer.fit_transform(self.preprocessed_prompts)

    def preprocess(self, text: str) -> list[str]:
        """Tokenize, lemmatize, and keep meaningful POS (nouns, verbs, adjectives)"""
        tokens = word_tokenize(text.lower())
        tokens = [self.lemmatizer.lemmatize(t) for t in tokens if t.isalnum() and t not in self.stop_words]
        tagged = pos_tag(tokens)
        important_tokens = [t for t, pos in tagged if pos.startswith(("N", "V", "J"))]  # nouns, verbs, adjectives
        # Add bigrams
        bigrams = ["_".join(gram) for gram in ngrams(important_tokens, 2)]
        return important_tokens + bigrams

    def evaluate(self, submission: str, chunk_size: int = 150) -> list[tuple[str, float]]:
        submission_tokens = self.preprocess(submission)
        if not submission_tokens:
            submission_tokens = ["dummy"]

        # Split submission into chunks
        chunks = [
            submission_tokens[i:i + chunk_size]
            for i in range(0, len(submission_tokens), chunk_size)
        ]
        if not chunks:
            chunks = [["dummy"]]

        preprocessed_chunks = [" ".join(chunk) for chunk in chunks]

        max_similarities = []
        for i, prompt_tokens in enumerate(self.prompt_tokens_list):
            prompt_text = self.preprocessed_prompts[i]
            chunk_sims = []

            for chunk_text, chunk_tokens in zip(preprocessed_chunks, chunks):
                tfidf_matrix = self.vectorizer.transform([chunk_text, prompt_text])
                sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0, 0]

                # Weighted mechanic keyword boost
                overlap = 0
                for w in chunk_tokens:
                    if w in self.mechanic_keywords and w in prompt_tokens:
                        kw_data = self.mechanic_keywords[w]
                        weight = kw_data.get("weight", 0)
                        overlap += weight

                boost_factor = 0.1 * min(len(chunk_tokens) / 100, 5.0)
                sim += overlap * boost_factor

                chunk_sims.append(sim)

            max_similarities.append(max(chunk_sims))

        # Convert raw scores to confidence percentages using sigmoid
        def sigmoid(x, center=0.5, steepness=10):
            return 100 / (1 + math.exp(-steepness * (x - center)))

        confidence_scores = [sigmoid(score) for score in max_similarities]

        # Get top 3 categories with confidence percentages
        top_indices = np.argsort(confidence_scores)[-3:][::-1]
        top_categories = [(self.categories[i]["tier_name"], float(confidence_scores[i])) for i in top_indices]

        return top_categories