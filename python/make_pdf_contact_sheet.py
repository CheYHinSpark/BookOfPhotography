from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "tmp" / "pdfs"
OUTPUT = SOURCE_DIR / "contact-sheet.png"


def main():
    source_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else SOURCE_DIR
    output = Path(sys.argv[2]) if len(sys.argv) > 2 else OUTPUT
    pattern = sys.argv[3] if len(sys.argv) > 3 else "page-*.png"
    pages = sorted(source_dir.glob(pattern))
    if not pages:
        raise SystemExit("No rendered PDF pages found.")

    columns = 4
    thumb_width = 280
    label_height = 34
    gutter = 22
    with Image.open(pages[0]) as sample:
        ratio = sample.height / sample.width
    thumb_height = round(thumb_width * ratio)
    rows = (len(pages) + columns - 1) // columns

    canvas_width = gutter + columns * (thumb_width + gutter)
    canvas_height = gutter + rows * (thumb_height + label_height + gutter)
    canvas = Image.new("RGB", (canvas_width, canvas_height), "#dfe7ee")
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default(size=20)

    for index, path in enumerate(pages):
        row, column = divmod(index, columns)
        x = gutter + column * (thumb_width + gutter)
        y = gutter + row * (thumb_height + label_height + gutter)
        with Image.open(path) as page:
            thumb = page.convert("RGB").resize((thumb_width, thumb_height), Image.Resampling.LANCZOS)
        canvas.paste(thumb, (x, y))
        draw.rectangle((x, y, x + thumb_width - 1, y + thumb_height - 1), outline="#8aa0b3", width=2)
        draw.text((x, y + thumb_height + 6), path.stem, fill="#243b53", font=font)

    canvas.save(output, optimize=True)


if __name__ == "__main__":
    main()
