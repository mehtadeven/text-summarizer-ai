"""
Extractive Text Summarizer
--------------------------
Summarises an article without any neural network:
1. Split the text into sentences
2. Score every word with TF-IDF (rare, meaningful words score higher)
3. A sentence's score = the total of its word scores
4. Return the top-scoring sentences, in their original order

It also prints the top keywords: the words with the highest TF-IDF
score in the whole document.

Run:  python summarize.py                       (summarises the sample article)
      python summarize.py my.txt                (summarises your own text file)
      python summarize.py my.txt --sentences 5  (asks for a 5-sentence summary)
"""

import argparse
import re
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
    try:
        matrix = tfidf.fit_transform(sentences)
    except ValueError:
        return sentences[:num_sentences]  # no usable words: take the first sentences
    scores = matrix.sum(axis=1).A1  # total TF-IDF weight per sentence
    top = sorted(range(len(sentences)), key=lambda i: scores[i], reverse=True)[:num_sentences]
    return [sentences[i] for i in sorted(top)]  # back to reading order


def top_keywords(text: str, num_keywords: int = 5) -> list[str]:
    if not text.strip():
        return []
    tfidf = TfidfVectorizer(stop_words="english")
    try:
        matrix = tfidf.fit_transform([text])
    except ValueError:
        return []  # only stop words, so no keywords to report
    scores = matrix.sum(axis=0).A1  # total TF-IDF weight per word
    words = tfidf.get_feature_names_out()
    top = sorted(range(len(words)), key=lambda i: scores[i], reverse=True)[:num_keywords]
    return [words[i] for i in top]


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarise a text file with TF-IDF.")
    parser.add_argument("file", nargs="?", help="text file to summarise (default: built-in sample)")
    parser.add_argument("--sentences", type=int, default=3,
                        help="number of sentences in the summary (default: 3)")
    args = parser.parse_args()

    text = Path(args.file).read_text() if args.file else SAMPLE
    print(f"SUMMARY ({args.sentences} sentences):\n")
    for s in summarize(text, args.sentences):
        print(f"- {s}")
    keywords = top_keywords(text)
    print("\nKeywords: " + (", ".join(keywords) if keywords else "none found"))


if __name__ == "__main__":
    main()
