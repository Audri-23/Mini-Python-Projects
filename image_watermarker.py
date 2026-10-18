"""
Image Watermarker
-----------------
Batch-stamp a text or logo watermark onto photos.

Features
  * Text OR logo (transparent PNG) watermarks
  * 9 fixed positions + a tiled diagonal pattern
  * Adjustable opacity, size (relative to image width), rotation and colour
  * Auto-contrast shadow so text stays readable on any background
  * Fixes sideways phone photos (EXIF rotation) automatically
  * Handles JPG, PNG, WebP, BMP and TIFF - originals are never touched

Usage
  Interactive (just answer the prompts):
      python image_watermarker.py

  Command line (skips the prompts):
      python image_watermarker.py -i photos/ -t "(c) Audri 2026" -p bottom-right
      python image_watermarker.py -i photo.jpg -l logo.png -p center --opacity 40
      python image_watermarker.py -i photos/ -t "SAMPLE" -p tiled --color gray
"""

import argparse
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache
from pathlib import Path


# --------------------------------------------------------------------------- #
# Auto-install Pillow on first run (same style as the other scripts in the repo)
# --------------------------------------------------------------------------- #
def ensure_pillow():
    try:
        import PIL  # noqa: F401
    except ImportError:
        print("Pillow not found. Installing it now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])


ensure_pillow()

from PIL import Image, ImageColor, ImageDraw, ImageFont, ImageOps  # noqa: E402

# Avoid crashes on consoles that can't print some characters (e.g. old Windows).
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

RESAMPLE = getattr(Image, "Resampling", Image)  # Pillow 9.1+ vs older versions

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}
OUTPUT_SUFFIX = "_watermarked"
DEFAULT_OUTPUT_DIR = "watermarked_images"

# (key, label, vertical, horizontal)
POSITIONS = [
    ("top-left", "Top left", "top", "left"),
    ("top-center", "Top center", "top", "center"),
    ("top-right", "Top right", "top", "right"),
    ("middle-left", "Middle left", "middle", "left"),
    ("center", "Center", "middle", "center"),
    ("middle-right", "Middle right", "middle", "right"),
    ("bottom-left", "Bottom left", "bottom", "left"),
    ("bottom-center", "Bottom center", "bottom", "center"),
    ("bottom-right", "Bottom right", "bottom", "right"),
]
TILED = "tiled"
POSITION_KEYS = [p[0] for p in POSITIONS] + [TILED]

FONT_CANDIDATES = [
    "arialbd.ttf", "Arial Bold.ttf", "arial.ttf", "Arial.ttf", "segoeuib.ttf",
    "DejaVuSans-Bold.ttf", "DejaVuSans.ttf", "LiberationSans-Bold.ttf",
    "FreeSansBold.ttf", "Helvetica.ttc",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
]


# --------------------------------------------------------------------------- #
# Settings
# --------------------------------------------------------------------------- #
@dataclass
class Settings:
    mode: str                      # "text" or "logo"
    text: str = ""
    logo_path: Path | None = None
    position: str = "bottom-right"
    opacity: float = 0.5           # 0.0 - 1.0
    size_pct: float = 25.0         # watermark width as % of image width
    angle: float = 0.0             # degrees, counter-clockwise
    color: tuple = (255, 255, 255)
    font_path: str | None = None
    shadow: bool = True


# --------------------------------------------------------------------------- #
# Watermark building blocks
# --------------------------------------------------------------------------- #
@lru_cache(maxsize=64)
def load_font(font_path, size):
    """Load a scalable font, trying the user's font, then common system fonts."""
    candidates = ([font_path] if font_path else []) + FONT_CANDIDATES
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    try:
        return ImageFont.load_default(size=size)  # Pillow 10.1+
    except TypeError:
        return ImageFont.load_default()


def contrasting_shadow(rgb):
    """Dark shadow for light text, light shadow for dark text."""
    luminance = 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]
    return (0, 0, 0) if luminance >= 110 else (255, 255, 255)


def make_text_stamp(settings, target_width):
    """Render the watermark text into its own transparent image."""
    probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))

    # Measure at a reference size, then scale so the text hits the target width.
    ref_font = load_font(settings.font_path, 100)
    left, top, right, bottom = probe.textbbox((0, 0), settings.text, font=ref_font)
    size = max(8, int(100 * target_width / max(1, right - left)))

    font = load_font(settings.font_path, size)
    left, top, right, bottom = probe.textbbox((0, 0), settings.text, font=font)
    text_w, text_h = right - left, bottom - top

    offset = max(1, size // 25) if settings.shadow else 0
    pad = offset + 2
    canvas = Image.new("RGBA", (text_w + 2 * pad + offset, text_h + 2 * pad + offset), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    if settings.shadow:
        shadow_rgb = contrasting_shadow(settings.color)
        draw.text((pad - left + offset, pad - top + offset), settings.text,
                  font=font, fill=shadow_rgb + (200,))
    draw.text((pad - left, pad - top), settings.text, font=font, fill=settings.color + (255,))
    return canvas


def make_logo_stamp(logo, target_width):
    """Resize the logo (keeping its aspect ratio) to the target width."""
    target_width = max(10, int(target_width))
    target_height = max(1, int(logo.height * target_width / logo.width))
    return logo.resize((target_width, target_height), RESAMPLE.LANCZOS)


def apply_opacity(stamp, opacity):
    """Scale the stamp's alpha channel so it becomes semi-transparent."""
    alpha = stamp.getchannel("A").point(lambda v: int(v * opacity))
    stamp.putalpha(alpha)
    return stamp


def fit_inside(stamp, max_w, max_h):
    """Shrink the stamp if it would be bigger than the available space."""
    scale = min(max_w / stamp.width, max_h / stamp.height, 1.0)
    if scale < 1.0:
        new_size = (max(1, int(stamp.width * scale)), max(1, int(stamp.height * scale)))
        stamp = stamp.resize(new_size, RESAMPLE.LANCZOS)
    return stamp


def composite_at(layer, stamp, x, y):
    """alpha_composite that safely handles stamps hanging off the image edges."""
    src_x, src_y = max(0, -x), max(0, -y)
    dest_x, dest_y = max(0, x), max(0, y)
    width = min(stamp.width - src_x, layer.width - dest_x)
    height = min(stamp.height - src_y, layer.height - dest_y)
    if width <= 0 or height <= 0:
        return
    piece = stamp.crop((src_x, src_y, src_x + width, src_y + height))
    layer.alpha_composite(piece, (dest_x, dest_y))


def place_single(layer, stamp, position, margin):
    """Stamp once at one of the nine preset positions."""
    W, H = layer.size
    entry = next(p for p in POSITIONS if p[0] == position)
    _, _, vertical, horizontal = entry

    x = {"left": margin, "center": (W - stamp.width) // 2,
         "right": W - stamp.width - margin}[horizontal]
    y = {"top": margin, "middle": (H - stamp.height) // 2,
         "bottom": H - stamp.height - margin}[vertical]
    composite_at(layer, stamp, x, y)


def place_tiled(layer, stamp):
    """Repeat the stamp across the whole image in a staggered grid."""
    W, H = layer.size
    step_x = max(1, int(stamp.width * 1.5))
    step_y = max(1, int(stamp.height * 1.5))
    y, row = -(stamp.height // 2), 0
    while y < H:
        x = -(stamp.width // 2) - (step_x // 2 if row % 2 else 0)
        while x < W:
            composite_at(layer, stamp, x, y)
            x += step_x
        y += step_y
        row += 1


def build_stamp(settings, logo, image_width, image_height):
    """Create the ready-to-paste (sized, rotated, transparent) watermark."""
    target_width = max(20, image_width * settings.size_pct / 100)
    if settings.mode == "logo":
        stamp = make_logo_stamp(logo, target_width)
    else:
        stamp = make_text_stamp(settings, target_width)

    stamp = apply_opacity(stamp, settings.opacity)
    if settings.angle:
        stamp = stamp.rotate(settings.angle, resample=RESAMPLE.BICUBIC, expand=True)
    return stamp


# --------------------------------------------------------------------------- #
# Per-image processing
# --------------------------------------------------------------------------- #
def save_image(img_rgba, dest, has_alpha, icc_profile):
    """Save in the same format as the input, handling transparency rules."""
    ext = dest.suffix.lower()
    if ext in (".jpg", ".jpeg"):
        img_rgba.convert("RGB").save(dest, "JPEG", quality=95, optimize=True,
                                     icc_profile=icc_profile)
    elif ext == ".png":
        out = img_rgba if has_alpha else img_rgba.convert("RGB")
        out.save(dest, "PNG", optimize=True, icc_profile=icc_profile)
    elif ext == ".webp":
        out = img_rgba if has_alpha else img_rgba.convert("RGB")
        out.save(dest, "WEBP", quality=95, icc_profile=icc_profile)
    else:  # .bmp, .tif, .tiff
        img_rgba.convert("RGB").save(dest)


def watermark_image(src, dest, settings, logo):
    with Image.open(src) as opened:
        img = ImageOps.exif_transpose(opened)  # fix sideways phone photos
        icc_profile = img.info.get("icc_profile")
        has_alpha = img.mode in ("RGBA", "LA", "PA") or "transparency" in img.info
        base = img.convert("RGBA")

    W, H = base.size
    margin = max(10, int(W * 0.02))
    stamp = build_stamp(settings, logo, W, H)

    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    if settings.position == TILED:
        place_tiled(layer, stamp)
    else:
        stamp = fit_inside(stamp, W - 2 * margin, H - 2 * margin)
        place_single(layer, stamp, settings.position, margin)

    result = Image.alpha_composite(base, layer)
    save_image(result, dest, has_alpha, icc_profile)


def collect_images(path):
    if path.is_file():
        return [path] if path.suffix.lower() in SUPPORTED_EXTENSIONS else []
    return sorted(p for p in path.iterdir()
                  if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS)


def run_batch(input_path, output_dir, settings):
    images = collect_images(input_path)
    if not images:
        print("\nNo supported images found "
              f"({', '.join(sorted(SUPPORTED_EXTENSIONS))}).")
        return

    logo = None
    if settings.mode == "logo":
        logo = Image.open(settings.logo_path).convert("RGBA")

    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"\nFound {len(images)} image(s). Saving to: {output_dir.resolve()}\n")

    done, failed, skipped = 0, [], 0
    started = time.time()
    for index, src in enumerate(images, start=1):
        # Don't re-watermark our own output if input and output share a folder.
        if src.stem.endswith(OUTPUT_SUFFIX) and src.parent.resolve() == output_dir.resolve():
            skipped += 1
            continue
        dest = output_dir / f"{src.stem}{OUTPUT_SUFFIX}{src.suffix.lower()}"
        try:
            watermark_image(src, dest, settings, logo)
            done += 1
            print(f"  [{index}/{len(images)}] {src.name} -> OK")
        except Exception as error:  # keep going if one file is broken
            failed.append((src.name, error))
            print(f"  [{index}/{len(images)}] {src.name} -> FAILED ({error})")

    print("\n" + "-" * 50)
    print(f"Done in {time.time() - started:.1f}s  |  watermarked: {done}"
          f"  |  failed: {len(failed)}" + (f"  |  skipped: {skipped}" if skipped else ""))
    print(f"Output folder: {output_dir.resolve()}")


# --------------------------------------------------------------------------- #
# Input helpers
# --------------------------------------------------------------------------- #
def clean_path(raw):
    """Handle quotes from drag-and-drop paths and ~ shortcuts."""
    return Path(raw.strip().strip('"').strip("'")).expanduser()


def parse_color(value):
    try:
        return ImageColor.getrgb(value.strip())[:3]
    except ValueError:
        return None


def ask(prompt, default=None):
    suffix = f" [{default}]" if default is not None else ""
    while True:
        value = input(f"{prompt}{suffix}: ").strip()
        if value:
            return value
        if default is not None:
            return str(default)
        print("  Please enter a value.")


def ask_number(prompt, default, low, high):
    while True:
        raw = ask(prompt, default).rstrip("%")
        try:
            number = float(raw)
        except ValueError:
            print("  Please enter a number.")
            continue
        if low <= number <= high:
            return number
        print(f"  Please enter a value between {low:g} and {high:g}.")


def ask_yes_no(prompt, default=True):
    hint = "Y/n" if default else "y/N"
    while True:
        value = input(f"{prompt} ({hint}): ").strip().lower()
        if not value:
            return default
        if value in ("y", "yes"):
            return True
        if value in ("n", "no"):
            return False
        print("  Please answer y or n.")


def ask_existing_path(prompt, want_dir_ok=True):
    while True:
        path = clean_path(ask(prompt))
        if path.exists() and (path.is_file() or want_dir_ok):
            return path
        print("  That path doesn't exist (or isn't a file). Try again.")


def default_size(mode, position):
    if mode == "logo":
        return 12.0 if position == TILED else 20.0
    return 20.0 if position == TILED else 30.0


def default_angle(position):
    return 30.0 if position == TILED else 0.0


# --------------------------------------------------------------------------- #
# Interactive mode
# --------------------------------------------------------------------------- #
def interactive():
    print("=" * 50)
    print("  IMAGE WATERMARKER")
    print("=" * 50)

    input_path = ask_existing_path("Image file or folder path")
    if not collect_images(input_path):
        print("No supported images found there. Exiting.")
        return None

    print("\nWatermark type:\n  1) Text\n  2) Logo (PNG with transparent background)")
    mode = "logo" if ask("Choose", "1") == "2" else "text"

    settings = Settings(mode=mode)
    if mode == "text":
        settings.text = ask("Watermark text", f"\u00a9 {datetime.now().year}")
    else:
        settings.logo_path = ask_existing_path("Logo file path", want_dir_ok=False)
        try:
            Image.open(settings.logo_path).verify()
        except Exception:
            print("That file isn't a readable image. Exiting.")
            return None

    print("\nPosition:")
    for number, (_, label, _, _) in enumerate(POSITIONS, start=1):
        print(f"  {number}) {label}")
    print(f"  10) Tiled diagonal pattern (hardest to crop out)")
    while True:
        choice = ask("Choose", "9")
        if choice.isdigit() and 1 <= int(choice) <= 10:
            settings.position = POSITION_KEYS[int(choice) - 1]
            break
        print("  Please pick a number from 1 to 10.")

    settings.opacity = ask_number("Opacity % (1 = faint, 100 = solid)", 50, 1, 100) / 100
    settings.size_pct = ask_number("Size as % of image width",
                                   default_size(mode, settings.position), 1, 100)
    settings.angle = ask_number("Rotation in degrees (0 = straight)",
                                default_angle(settings.position), -180, 180)

    if mode == "text":
        while True:
            color = parse_color(ask("Text colour (name like 'white' or hex like #FFCC00)", "white"))
            if color:
                settings.color = color
                break
            print("  Couldn't understand that colour. Try 'white', 'black' or '#RRGGBB'.")
        font = input("Font file path (.ttf) [Enter = automatic]: ").strip()
        if font:
            font_path = clean_path(font)
            if font_path.is_file():
                settings.font_path = str(font_path)
            else:
                print("  Font not found - using an automatic font instead.")
        settings.shadow = ask_yes_no("Add a shadow for readability?", True)

    output_dir = clean_path(ask("Output folder", DEFAULT_OUTPUT_DIR))
    return input_path, output_dir, settings


# --------------------------------------------------------------------------- #
# Command-line mode
# --------------------------------------------------------------------------- #
def build_parser():
    parser = argparse.ArgumentParser(
        description="Batch-stamp a text or logo watermark onto images.")
    parser.add_argument("-i", "--input", help="image file or folder (omit for interactive mode)")
    parser.add_argument("-o", "--output", default=DEFAULT_OUTPUT_DIR,
                        help=f"output folder (default: {DEFAULT_OUTPUT_DIR})")
    parser.add_argument("-t", "--text", help="watermark text")
    parser.add_argument("-l", "--logo", help="logo image path (PNG with transparency works best)")
    parser.add_argument("-p", "--position", default="bottom-right", choices=POSITION_KEYS,
                        help="where to place it (default: bottom-right)")
    parser.add_argument("--opacity", type=float, default=50, help="1-100 (default: 50)")
    parser.add_argument("--size", type=float, help="watermark width as %% of image width")
    parser.add_argument("--angle", type=float, help="rotation in degrees (tiled default: 30)")
    parser.add_argument("--color", default="white", help="text colour name or hex (default: white)")
    parser.add_argument("--font", help="path to a .ttf font file")
    parser.add_argument("--no-shadow", action="store_true", help="disable the text shadow")
    return parser


def from_args(args, parser):
    input_path = clean_path(args.input)
    if not input_path.exists():
        parser.error(f"input path not found: {input_path}")
    if bool(args.text) == bool(args.logo):
        parser.error("provide exactly one of --text or --logo")
    if not 1 <= args.opacity <= 100:
        parser.error("--opacity must be between 1 and 100")

    mode = "logo" if args.logo else "text"
    settings = Settings(mode=mode, position=args.position, opacity=args.opacity / 100)
    settings.size_pct = args.size if args.size else default_size(mode, args.position)
    settings.angle = args.angle if args.angle is not None else default_angle(args.position)
    if not 1 <= settings.size_pct <= 100:
        parser.error("--size must be between 1 and 100")

    if mode == "logo":
        settings.logo_path = clean_path(args.logo)
        if not settings.logo_path.is_file():
            parser.error(f"logo not found: {settings.logo_path}")
    else:
        settings.text = args.text
        color = parse_color(args.color)
        if not color:
            parser.error(f"unknown colour: {args.color}")
        settings.color = color
        settings.shadow = not args.no_shadow
        if args.font:
            if not clean_path(args.font).is_file():
                parser.error(f"font not found: {args.font}")
            settings.font_path = str(clean_path(args.font))

    return input_path, clean_path(args.output), settings


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #
def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.input:
            config = from_args(args, parser)
        else:
            config = interactive()
        if config:
            run_batch(*config)
    except KeyboardInterrupt:
        print("\nCancelled.")


if __name__ == "__main__":
    main()
