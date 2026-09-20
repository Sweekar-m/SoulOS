import math
import re
from collections import Counter

from .catalog import INTENT_CATALOG


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _tfidf_vectors(documents: list[list[str]]) -> list[dict[str, float]]:
    df = Counter(token for doc in documents for token in set(doc))
    total = len(documents)
    vectors = []
    for doc in documents:
        counts = Counter(doc)
        length = max(len(doc), 1)
        vectors.append({
            token: (count / length) * math.log((total + 1) / (df[token] + 1))
            for token, count in counts.items()
        })
    return vectors


def cosine_similarity(left: dict[str, float], right: dict[str, float]) -> float:
    common = set(left) & set(right)
    dot = sum(left[k] * right[k] for k in common)
    left_norm = math.sqrt(sum(v * v for v in left.values()))
    right_norm = math.sqrt(sum(v * v for v in right.values()))
    if not left_norm or not right_norm:
        return 0.0
    return dot / (left_norm * right_norm)


class IntentClassifier:
    def __init__(self) -> None:
        self.intents = list(INTENT_CATALOG)
        self.examples = [example for intent in self.intents for example in INTENT_CATALOG[intent]]
        self.example_intents = [intent for intent in self.intents for _ in INTENT_CATALOG[intent]]
        self.document_vectors = _tfidf_vectors([_tokens(example) for example in self.examples])

    def predict(self, text: str) -> tuple[str, float]:
        query = _tokens(text)
        query_vector = _tfidf_vectors([query] + [_tokens(example) for example in self.examples])[0]
        scores: dict[str, float] = {}
        for vector, intent in zip(self.document_vectors, self.example_intents):
            score = cosine_similarity(query_vector, vector)
            scores[intent] = max(scores.get(intent, 0.0), score)
        if not scores:
            return "unknown", 0.0
        intent, confidence = max(scores.items(), key=lambda item: item[1])
        return intent, round(confidence, 4)
