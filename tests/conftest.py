import sys
from pathlib import Path

# Make summarize.py (in the project root) importable from the tests.
sys.path.insert(0, str(Path(__file__).parent.parent))
