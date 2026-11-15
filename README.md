# 📝 Text Summarizer AI


![Banner](assets/banner.svg)
![Python](https://img.shields.io/badge/Python-3.10+-blue) ![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange) ![NLP](https://img.shields.io/badge/area-NLP-purple) ![Status](https://img.shields.io/badge/status-working-brightgreen)

Paste in a long article, get back its **3 most important sentences** — an extractive summarizer built with TF-IDF, no neural network and no API key needed.

## 📄 Sample output

Input: a 12-sentence article about learning AI. Output:

> - Instead of only reading textbooks, students can now build small projects that solve real problems.
> - Each project looks simple, but together they teach the core ideas of machine learning: data, features, models, and evaluation.
> - The best way to learn AI is not to watch videos about it, but to build with it.

## ⚙️ How it works

1. Split the text into sentences
2. Score every word with **TF-IDF** — rare, meaningful words weigh more than "the" and "is"
3. Each sentence's score = the sum of its word scores
4. Return the top sentences **in their original order**, so the summary still reads naturally

## 🚀 Run it

```bash
pip install -r requirements.txt
python summarize.py            # summarises the built-in sample article
python summarize.py my.txt     # summarises your own text file
```

## 🧠 What I learned

- Extractive vs abstractive summarization (picking sentences vs writing new ones)
- How TF-IDF quietly powers search, recommendations, and chatbots too
- Testing scoring variants: my first version over-penalised long sentences and picked the weakest ones — the simple total score won

## 🔮 Next steps

- [ ] Let the user choose the summary length
- [ ] Add TextRank (graph-based) scoring and compare
- [ ] Build a paste-and-summarise web page

---
Built by [Mehta Deven](https://github.com/mehtadeven) — IT student learning ML/AI in public.
