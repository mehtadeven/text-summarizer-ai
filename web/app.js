// Text Summarizer - browser version of summarize.py.
// 1. split the text into sentences  2. score words with TF-IDF
// 3. a sentence's score = the sum of its word scores
// 4. keep the top sentences, in their original order.

const STOPS = new Set(SKLEARN_STOP_WORDS);

// summarize.split_sentences
function splitSentences(text) {
  return String(text)
    .replace(/\n/g, " ")
    .split(/(?<=[.!?])\s+/)
    .map((s) => s.trim())
    .filter(Boolean);
}

// Score every sentence (total TF-IDF weight). Returns null if no usable words.
function sentenceScores(sentences) {
  try {
    const model = Tfidf.fit(sentences, STOPS);
    return model.rows.map((row) => [...row.values()].reduce((a, b) => a + b, 0));
  } catch {
    return null;
  }
}

// summarize.summarize -> indices of the chosen sentences, in reading order
function summarizeIndices(sentences, numSentences = 3) {
  if (sentences.length <= numSentences) return sentences.map((_, i) => i);
  const scores = sentenceScores(sentences);
  if (!scores) return sentences.slice(0, numSentences).map((_, i) => i);
  return Tfidf.rankDesc(scores).slice(0, numSentences).sort((a, b) => a - b);
}

function summarize(text, numSentences = 3) {
  const sentences = splitSentences(text);
  return summarizeIndices(sentences, numSentences).map((i) => sentences[i]);
}

// Python's round(x, digits): rounds the exact binary value, ties go to the even digit
// (round(3.25, 1) == 3.2), so the numbers here match the Python output exactly.
function pyRound(x, digits = 1) {
  const exact = Math.abs(x).toFixed(30);
  const [whole, frac] = exact.split(".");
  const kept = whole + frac.slice(0, digits);
  const rest = frac.slice(digits).replace(/0+$/, "");
  let n = BigInt(kept);
  if (rest > "5" || (rest === "5" && n % 2n === 1n)) n += 1n;
  return (Math.sign(x) || 1) * Number(n) / 10 ** digits;
}

// summarize.text_stats
function textStats(text) {
  const sentences = splitSentences(text);
  const words = String(text).split(/\s+/).filter(Boolean).length;
  return {
    words,
    sentences: sentences.length,
    words_per_sentence: sentences.length ? pyRound(words / sentences.length, 1) : 0,
  };
}

// summarize.top_keywords
function topKeywords(text, numKeywords = 5) {
  if (!String(text).trim()) return [];
  let model;
  try {
    model = Tfidf.fit([text], STOPS);
  } catch {
    return [];
  }
  const row = model.rows[0];
  const scores = model.vocab.map((_, i) => row.get(i) || 0);
  return Tfidf.rankDesc(scores).slice(0, numKeywords).map((i) => model.vocab[i]);
}

// ---- Page wiring (browser only) ----
if (typeof document !== "undefined") {
  const $ = (id) => document.getElementById(id);
  const input = $("text");
  const slider = $("count");

  function render() {
    const text = input.value;
    const sentences = splitSentences(text);
    slider.max = Math.max(1, sentences.length);
    if (+slider.value > sentences.length) slider.value = Math.max(1, sentences.length);
    const n = +slider.value;
    $("count-label").textContent = `${n} sentence${n === 1 ? "" : "s"}`;

    const stats = textStats(text);
    $("stat-words").textContent = stats.words;
    $("stat-sentences").textContent = stats.sentences;
    $("stat-wps").textContent = stats.words_per_sentence;

    const chosen = new Set(summarizeIndices(sentences, n));
    const summaryWords = [...chosen].reduce((sum, i) => sum + sentences[i].split(/\s+/).filter(Boolean).length, 0);
    $("stat-kept").textContent = stats.words ? Math.round((100 * summaryWords) / stats.words) + "%" : "–";

    const list = $("summary");
    list.innerHTML = "";
    if (!sentences.length) list.innerHTML = '<li class="empty">Paste some text to summarise.</li>';
    for (const i of [...chosen].sort((a, b) => a - b)) {
      const li = document.createElement("li");
      li.textContent = sentences[i];
      list.appendChild(li);
    }

    // The original text with the chosen sentences highlighted, and each sentence's score.
    const scores = sentenceScores(sentences) || sentences.map(() => 0);
    const best = Math.max(...scores, 1e-9);
    const view = $("highlight");
    view.innerHTML = "";
    sentences.forEach((sentence, i) => {
      const span = document.createElement("span");
      span.className = "sent" + (chosen.has(i) ? " picked" : "");
      span.style.setProperty("--w", (scores[i] / best).toFixed(3));
      span.title = `score ${scores[i].toFixed(3)}`;
      span.textContent = sentence + " ";
      view.appendChild(span);
    });

    const keywords = $("keywords");
    keywords.innerHTML = "";
    const words = topKeywords(text);
    if (!words.length) keywords.innerHTML = '<span class="empty">none found</span>';
    for (const word of words) {
      const chip = document.createElement("span");
      chip.className = "chip info";
      chip.textContent = word;
      keywords.appendChild(chip);
    }
  }

  input.addEventListener("input", render);
  slider.addEventListener("input", render);
  $("sample").addEventListener("click", () => {
    input.value = SAMPLE_TEXT;
    slider.value = 3;
    render();
  });
  $("clear").addEventListener("click", () => {
    input.value = "";
    render();
    input.focus();
  });

  input.value = SAMPLE_TEXT;
  render();
}

if (typeof module !== "undefined") {
  module.exports = { splitSentences, summarize, summarizeIndices, textStats, topKeywords };
}
