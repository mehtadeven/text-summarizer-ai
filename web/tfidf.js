// TF-IDF in plain JavaScript - a port of scikit-learn's TfidfVectorizer defaults
// (lowercase, token pattern \b\w\w+\b, smooth_idf=True, norm="l2"), so the
// browser demo scores text exactly like the Python version.
const Tfidf = (() => {
  // Python's \w is Unicode-aware: letters, numbers and underscore.
  const WORD = /[\p{L}\p{N}_]+/gu;

  function tokenize(text, stopWords) {
    const words = (String(text).toLowerCase().match(WORD) || []).filter((w) => w.length >= 2);
    return stopWords ? words.filter((w) => !stopWords.has(w)) : words;
  }

  // Code-point order, like Python's sorted() on strings.
  const byText = (a, b) => (a < b ? -1 : a > b ? 1 : 0);

  function vectorize(model, tokens) {
    const counts = new Map();
    for (const token of tokens) {
      const i = model.index.get(token);
      if (i !== undefined) counts.set(i, (counts.get(i) || 0) + 1);
    }
    const vector = new Map();
    let squared = 0;
    for (const [i, count] of counts) {
      const weight = count * model.idf[i];
      vector.set(i, weight);
      squared += weight * weight;
    }
    const norm = Math.sqrt(squared);
    if (norm > 0) for (const [i, weight] of vector) vector.set(i, weight / norm);
    return vector;
  }

  // Learn the vocabulary + IDF from `docs` and return one vector per doc.
  // Throws like scikit-learn when every word is a stop word.
  function fit(docs, stopWords) {
    const tokenized = docs.map((doc) => tokenize(doc, stopWords));
    const docFreq = new Map();
    for (const tokens of tokenized) {
      for (const token of new Set(tokens)) docFreq.set(token, (docFreq.get(token) || 0) + 1);
    }
    if (docFreq.size === 0) throw new Error("empty vocabulary; the text only contains stop words");
    const vocab = [...docFreq.keys()].sort(byText);
    const index = new Map(vocab.map((term, i) => [term, i]));
    const n = docs.length;
    // scikit-learn's smoothed idf: ln((1 + n) / (1 + df)) + 1
    const idf = vocab.map((term) => Math.log((1 + n) / (1 + docFreq.get(term))) + 1);
    const model = { vocab, index, idf, stopWords };
    model.rows = tokenized.map((tokens) => vectorize(model, tokens));
    return model;
  }

  function transform(model, text) {
    return vectorize(model, tokenize(text, model.stopWords));
  }

  // Cosine similarity of two l2-normalised vectors is their dot product.
  function dot(a, b) {
    const [small, big] = a.size <= b.size ? [a, b] : [b, a];
    let sum = 0;
    for (const [i, weight] of small) {
      const other = big.get(i);
      if (other !== undefined) sum += weight * other;
    }
    return sum;
  }

  // Indices sorted by score, highest first; ties keep their original order
  // (Python's sorted(..., reverse=True) is stable in the same way).
  function rankDesc(scores) {
    return scores.map((score, i) => [score, i]).sort((a, b) => b[0] - a[0] || a[1] - b[1]).map((p) => p[1]);
  }

  return { tokenize, fit, transform, dot, rankDesc };
})();

if (typeof module !== "undefined") module.exports = { Tfidf };
