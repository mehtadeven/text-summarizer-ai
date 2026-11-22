"""
Generate the README result chart for the Text Summarizer.

Scores every sentence of the built-in sample article with TF-IDF
(the same scoring summarize.py uses) and saves a bar chart to
assets/result.png. The 3 gold bars are the summary sentences.

Run:  python generate_charts.py
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer

from summarize import SAMPLE, split_sentences

NAVY = "#0B3C5D"
GOLD = "#E3A82B"
CREAM = "#F7F1E1"
OUT = Path(__file__).parent / "assets" / "result.png"


def sentence_scores(text: str):
    """Return the TF-IDF score of every sentence, like summarize()."""
    sentences = split_sentences(text)
    matrix = TfidfVectorizer(stop_words="english").fit_transform(sentences)
    return sentences, matrix.sum(axis=1).A1  # total word weight per sentence


def main() -> None:
    sentences, scores = sentence_scores(SAMPLE)
    # The summary = the 3 highest-scoring sentences.
    top_three = sorted(range(len(sentences)), key=lambda i: scores[i], reverse=True)[:3]
    for i, (sentence, score) in enumerate(zip(sentences, scores), 1):
        mark = " <- in summary" if (i - 1) in top_three else ""
        print(f"S{i}: {score:.2f}{mark}  {sentence[:60]}...")

    labels = [f"S{i}" for i in range(1, len(sentences) + 1)]
    colours = [GOLD if i in top_three else NAVY for i in range(len(sentences))]

    fig, ax = plt.subplots(figsize=(9, 4.6))
    fig.patch.set_facecolor(CREAM)
    ax.set_facecolor(CREAM)
    bars = ax.bar(labels, scores, color=colours, width=0.6)
    for bar, score in zip(bars, scores):
        ax.text(bar.get_x() + bar.get_width() / 2, score + 0.08,
                f"{score:.1f}", ha="center", fontsize=9, fontweight="bold")
    ax.set_ylabel("Sentence score (summed TF-IDF)")
    ax.set_xlabel("Sentence in the sample article (gold = picked for the 3-sentence summary)")
    ax.set_title("Text Summarizer — how each sentence scores",
                 fontsize=12, fontweight="bold", color=NAVY)
    plt.tight_layout()
    OUT.parent.mkdir(exist_ok=True)
    plt.savefig(OUT, dpi=150)
    print(f"Chart saved to {OUT}")


if __name__ == "__main__":
    main()
