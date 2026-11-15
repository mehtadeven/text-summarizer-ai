"""
Extractive Text Summarizer
--------------------------
Summarises an article without any neural network:
1. Split the text into sentences
2. Score every word with TF-IDF (rare, meaningful words score higher)
3. A sentence's score = the sum of its word scores, normalised by length
4. Return the top-scoring sentences, in their original order

Run:  python summarize.py          (summarises the sample article)
      python summarize.py my.txt   (summarises your own text file)
"""

import re
import sys
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer

SAMPLE = """Artificial intelligence is changing how students learn. Instead of only
reading textbooks, students can now build small projects that solve real problems.
A spam classifier teaches how machines understand text. A digit recognizer shows
how computers see images. A recommendation system explains the idea behind the
suggestions on streaming platforms. Each project looks simple, but together they
teach the core ideas of machine learning: data, features, models, and evaluation.
The best way to learn AI is not to watch videos about it, but to build with it.
Students who build in public also create proof of their skills. A GitHub profile
full of working projects says more than a certificate. That is why learning by
building is becoming the most trusted path into an AI career."""


def split_sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.replace("\n", " ")) if s.strip()]


def summarize(text: str, num_sentences: int = 3) -> list[str]:
    sentences = split_sentences(text)
    if len(sentences) <= num_sentences:
        return sentences
    tfidf = TfidfVectorizer(stop_words="english")
    matrix = tfidf.fit_transform(sentences)
    scores = matrix.sum(axis=1).A1  # total TF-IDF weight per sentence
    top = sorted(range(len(sentences)), key=lambda i: scores[i], reverse=True)[:num_sentences]
    return [sentences[i] for i in sorted(top)]  # back to reading order


def main() -> None:
    text = Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else SAMPLE
    print("SUMMARY (3 sentences):\n")
    for s in summarize(text, 3):
        print(f"- {s}")


if __name__ == "__main__":
    main()
