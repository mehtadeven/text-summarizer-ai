# Contributing

Thanks for looking at this project. Small, clear improvements are welcome.

## Setup

```bash
git clone https://github.com/mehtadeven/text-summarizer-ai.git
cd text-summarizer-ai
python -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install pytest              # only needed to run the tests
```

## Run it

```bash
python summarize.py                      # built-in sample article
python summarize.py my.txt               # your own text file
python summarize.py my.txt --sentences 5 # longer summary
```

## Run the tests

```bash
python -m pytest tests/
```

Please make sure all tests pass before suggesting a change.

## Suggesting a change

- **Found a bug or have an idea?** Open an issue first and describe what
  you expected to happen and what actually happened.
- **Want to fix something yourself?** Fork the repo, make your change on a
  new branch, and open a pull request. Explain the change in one or two
  lines so it is easy to review.

## Code style

- Keep the code simple enough to explain out loud: clear names, short
  comments, no clever tricks.
- One change per pull request is easier to review than five at once.
- If you change behaviour, update the README and add or adjust a test.
