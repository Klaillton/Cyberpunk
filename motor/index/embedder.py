from __future__ import annotations

import math
import re
from collections import Counter
from typing import Protocol

import numpy as np

_TOKEN_RE = re.compile(r"[a-z0-9áàâãéêíóôõúç]+", re.IGNORECASE)


class Embedder(Protocol):
    dimension: int

    def fit(self, texts: list[str]) -> None: ...

    def embed(self, texts: list[str]) -> np.ndarray: ...


def _tokenize(text: str) -> list[str]:
    return [token.lower() for token in _TOKEN_RE.findall(text)]


def _normalize_rows(matrix: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return matrix / norms


class TfidfEmbedder:
    """Embedder leve sem dependências extras — adequado para CI e Raspberry Pi."""

    def __init__(self) -> None:
        self.vocabulary: dict[str, int] = {}
        self.idf: np.ndarray | None = None
        self.dimension = 0

    def fit(self, texts: list[str]) -> None:
        if not texts:
            self.vocabulary = {}
            self.idf = np.zeros(0, dtype=np.float32)
            self.dimension = 0
            return

        doc_freq: Counter[str] = Counter()
        for text in texts:
            tokens = set(_tokenize(text))
            for token in tokens:
                doc_freq[token] += 1

        self.vocabulary = {token: idx for idx, token in enumerate(sorted(doc_freq))}
        self.dimension = len(self.vocabulary)
        total_docs = len(texts)
        self.idf = np.array(
            [math.log((1 + total_docs) / (1 + doc_freq[token])) + 1.0 for token in sorted(doc_freq)],
            dtype=np.float32,
        )

    def embed(self, texts: list[str]) -> np.ndarray:
        if self.idf is None or self.dimension == 0:
            return np.zeros((len(texts), 0), dtype=np.float32)

        matrix = np.zeros((len(texts), self.dimension), dtype=np.float32)
        for row_idx, text in enumerate(texts):
            counts = Counter(_tokenize(text))
            if not counts:
                continue
            max_tf = max(counts.values())
            for token, count in counts.items():
                col = self.vocabulary.get(token)
                if col is None:
                    continue
                tf = 0.5 + 0.5 * (count / max_tf)
                matrix[row_idx, col] = tf * float(self.idf[col])
        return _normalize_rows(matrix)


def create_embedder() -> Embedder:
    try:
        from motor.index.minilm_embedder import MiniLmEmbedder

        return MiniLmEmbedder()
    except Exception:
        return TfidfEmbedder()