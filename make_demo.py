"""Make the demo image: run summarize.py for real and render its output.
Run:  python make_demo.py   # saves assets/demo.png
"""
import subprocess
import sys
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent
OUT = HERE / "assets" / "demo.png"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
TITLE = "text-summarizer-ai — terminal"
COMMAND = "python summarize.py"
ARGS = ['summarize.py']

def build_lines(output):
    return wrap_output(output)


def run_real_command():
    """Run the project for real and return its text output."""
    result = subprocess.run(
        [sys.executable] + ARGS, cwd=HERE,
        capture_output=True, text=True, timeout=300,
    )
    return (result.stdout or result.stderr).strip()

def wrap_output(text, width=86):
    """Wrap long lines so they fit inside the terminal window."""
    lines = []
    for raw in text.splitlines():
        if not raw.strip():
            lines.append("")
        else:
            lines.extend(textwrap.wrap(raw, width=width) or [""])
    return lines

def render(lines):
    """Draw a terminal window with the given lines and save the PNG."""
    font = ImageFont.truetype(FONT_PATH, 16)
    title_font = ImageFont.truetype(FONT_PATH, 15)
    line_height, pad_x, pad_y = 24, 28, 20
    width = 1200
    height = max(620, 44 + pad_y * 2 + len(lines) * line_height)
    img = Image.new("RGB", (width, height), "#0B1220")
    draw = ImageDraw.Draw(img)
    # Header bar with three window dots and the title.
    draw.rectangle([0, 0, width, 44], fill="#0B3C5D")
    for i, colour in enumerate(["#FF5F57", "#FEBC2E", "#28C840"]):
        x = 22 + i * 26
        draw.ellipse([x, 15, x + 14, 15 + 14], fill=colour)
    draw.text((110, 13), TITLE, font=title_font, fill="#F7F1E1")
    y = 44 + pad_y
    for line in lines:
        colour = "#E3A82B" if line.startswith("$") else "#F7F1E1"
        draw.text((pad_x, y), line, font=font, fill=colour)
        y += line_height
    OUT.parent.mkdir(exist_ok=True)
    img.save(OUT)
    print(f"Saved {OUT} ({OUT.stat().st_size} bytes)")

def main():
    output = run_real_command()
    lines = ["$ " + COMMAND, ""] + build_lines(output)
    render(lines[:26])

if __name__ == "__main__":
    main()
