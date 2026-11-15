"""Basic tests for the summarizer. Run with: python -m pytest tests/"""

import subprocess
import sys
from pathlib import Path

from summarize import SAMPLE, split_sentences, summarize, top_keywords

PROJECT_ROOT = Path(__file__).parent.parent


def test_summary_is_shorter_than_input():
    total = len(split_sentences(SAMPLE))
    result = summarize(SAMPLE)
    assert 0 < len(result) < total


def test_sentences_option_gives_exact_count():
    assert len(summarize(SAMPLE, 2)) == 2
    assert len(summarize(SAMPLE, 5)) == 5


def test_summary_sentences_come_from_the_text():
    for sentence in summarize(SAMPLE, 3):
        assert sentence in split_sentences(SAMPLE)


def test_keywords_are_five_words_from_the_text():
    keywords = top_keywords(SAMPLE)
    assert len(keywords) == 5
    for word in keywords:
        assert word in SAMPLE.lower()


def test_empty_and_tiny_input_is_handled():
    assert summarize("") == []
    assert top_keywords("") == []
    assert summarize("Just one sentence.") == ["Just one sentence."]
    assert summarize("One. Two.", 3) == ["One.", "Two."]


def test_cli_sentences_flag_and_keywords_line():
    run = subprocess.run(
        [sys.executable, "summarize.py", "--sentences", "2"],
        cwd=PROJECT_ROOT, capture_output=True, text=True,
    )
    assert run.returncode == 0
    assert "SUMMARY (2 sentences)" in run.stdout
    assert run.stdout.count("\n- ") == 2  # exactly two summary bullets
    assert "Keywords:" in run.stdout
