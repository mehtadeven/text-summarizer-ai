![Text Summarizer AI](assets/banner.svg)

# Text Summarizer AI

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white) ![NLP](https://img.shields.io/badge/Area-NLP-purple) ![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?logo=scikitlearn&logoColor=white) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE) ![Stars](https://img.shields.io/github/stars/mehtadeven/text-summarizer-ai?style=social)

An **extractive summarizer**: paste a long article and receive its most important sentences, verbatim and in reading order. No neural network, no API key — just well-applied TF-IDF.

## Sample output

Input: a 10-sentence article on learning AI. Output:

> - Instead of only reading textbooks, students can now build small projects that solve real problems.
> - Each project looks simple, but together they teach the core ideas of machine learning: data, features, models, and evaluation.
> - The best way to learn AI is not to watch videos about it, but to build with it.
>
> Keywords: build, students, ai, learn, learning

## How it works

![Pipeline](assets/flow.svg)

Sentences are scored by the summed TF-IDF weight of their words: sentences dense in rare, meaningful terms outrank filler. The top three are then restored to their original order so the summary reads naturally. During development, three scoring variants were benchmarked; a length-penalised variant consistently selected the weakest sentences, so the straightforward total score — verified against the sample — is what ships.

## Quick start

```bash
pip install -r requirements.txt
python summarize.py                      # summarise the built-in sample article
python summarize.py my.txt               # summarise any text file
python summarize.py my.txt --sentences 5 # choose the summary length (default: 3)
```

Every run also prints a **Keywords** line: the five words with the highest
TF-IDF score in the document, so you can see what the text is mainly about
at a glance.

## Tests

```bash
pip install pytest
python -m pytest tests/
```

## What this project demonstrates

- Extractive vs abstractive summarization
- TF-IDF as a reusable relevance signal (search, recommenders, chatbots)
- Empirical scoring choices: variants tested, not guessed

## Roadmap

- TextRank (graph-based) scoring comparison
- Paste-and-summarise web page

## Contributing

Contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) for setup, how to run the tests, and how to suggest a change.

---

**Author:** [Mehta Deven](https://github.com/mehtadeven) — IT student at SAL College of Engineering, Ahmedabad, building a public portfolio in Python, Machine Learning and AI.
**Portfolio:** [mehtadeven.github.io/portfolio](https://mehtadeven.github.io/portfolio/)

## Licence

MIT — see [LICENSE](LICENSE) for the full text.
