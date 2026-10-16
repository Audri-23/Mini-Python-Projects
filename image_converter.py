"""
Image Format Converter
----------------------
Convert JPG, JPEG, PNG, and WebP images, resize them, and process batches.

Dependency:
    python -m pip install Pillow

Run:
    python image_converter.py

The program saves results in a separate output folder and never modifies
the original image files.
"""

from pathlib import Path
from datetime import datetime

try:
    from PIL import Image, ImageOps
except ImportError:
    print("Pillow is not installed.")
    print("Install it with: python -m pip install Pillow")
    raise SystemExit(1)


SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
FORMAT_EXTENSIONS = {
    "JPG": ".jpg",
    "PNG": ".png",
    "WEBP": ".webp",
}
RESAMPLE = getattr(Image, "Resampling", Image).LANCZOS


def readable_size(size_bytes):
    """Return a human-readable file size."""
    size = float(size_bytes)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024 or unit == "GB":
            return f"{size:.1f} {unit}" if unit != "B" else f"{int(size)} B"
        size /= 1024
    return f"{size:.1f} GB"


def ask_choice(prompt, choices):
    """Ask until the user enters one of the allowed choices."""
    choices_text = "/".join(choices)
    while True:
        answer = input(f"{prompt} ({choices_text}): ").strip().upper()
        if answer in choices:
            return answer
        print(f"Please enter one of: {choices_text}")


def ask_positive_integer(prompt):
    """Ask for a positive whole number, or allow the user to skip."""
    while True:
        answer = input(prompt).strip()
        if not answer:
            return None
        try:
            number = int(answer)
            if number > 0:
                return number
        except ValueError:
            pass
        print("Enter a positive whole number, or press Enter to skip.")


def collect_images():
    """Collect image paths from individual files or a directory."""
    print("\nEnter image file paths one at a time.")
    print("You can also enter a folder path to include its supported images.")
    print("Press Enter on an empty line when you are finished.\n")

    found = []
    while True:
        raw_path = input("File or folder path: ").strip().strip('"').strip("'")
        if not raw_path:
            break

        path = Path(raw_path).expanduser()
        if not path.exists():
            print("That path does not exist. Try again.")
            continue

        if path.is_file():
            if path.suffix.lower() in SUPPORTED_EXTENSIONS:
                found.append(path)
            else:
                print("Unsupported file type. Use JPG, PNG, or WebP.")
        elif path.is_dir():
            folder_images = sorted(
                p for p in path.iterdir()
                if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
            )
            if folder_images:
                found.extend(folder_images)
                print(f"Added {len(folder_images)} image(s) from that folder.")
            else:
                print("No supported images found directly inside that folder.")
                print("(Subfolders are not scanned.)")

    # Remove duplicate paths while keeping the original order.
    unique = []
    seen = set()
    for path in found:
        resolved = path.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(path)

    return unique


def make_unique_path(path):
    """Avoid overwriting a previous output file."""
    if not path.exists():
        return path

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    candidate = path.with_name(f"{path.stem}_{timestamp}{path.suffix}")
    counter = 2
    while candidate.exists():
        candidate = path.with_name(
            f"{path.stem}_{timestamp}_{counter}{path.suffix}"
        )
        counter += 1
    return candidate


def convert_image(source, output_dir, output_format, width, height, quality):
    """Convert and optionally resize one image. Returns output path and sizes."""
    with Image.open(source) as original:
        # Apply camera orientation information before resizing.
        image = ImageOps.exif_transpose(original)
        image.load()

        original_dimensions = image.size

        # Resize to fit within the requested dimensions while preserving ratio.
        if width or height:
            max_width = width or image.width
            max_height = height or image.height
            image.thumbnail((max_width, max_height), RESAMPLE)

        # JPG does not support transparency. Put transparent pixels on white.
        if output_format == "JPG":
            has_transparency = (
                image.mode in ("RGBA", "LA")
                or (image.mode == "P" and "transparency" in image.info)
            )
            if has_transparency:
                rgba = image.convert("RGBA")
                background = Image.new("RGB", rgba.size, (255, 255, 255))
                background.paste(rgba, mask=rgba.getchannel("A"))
                image = background
            elif image.mode != "RGB":
                image = image.convert("RGB")
        elif output_format == "PNG":
            if image.mode not in ("RGB", "RGBA", "L", "LA", "I", "I;16"):
                image = image.convert("RGBA" if "transparency" in image.info else "RGB")
        elif output_format == "WEBP":
            if image.mode not in ("RGB", "RGBA"):
                image = image.convert("RGBA" if "transparency" in image.info else "RGB")

        extension = FORMAT_EXTENSIONS[output_format]
        destination = make_unique_path(output_dir / f"{source.stem}{extension}")

        save_options = {}
        if output_format in ("JPG", "WEBP"):
            save_options["quality"] = quality
        if output_format == "PNG":
            save_options["optimize"] = True

        pillow_format = "JPEG" if output_format == "JPG" else output_format
        image.save(destination, format=pillow_format, **save_options)

    return destination, source.stat().st_size, destination.stat().st_size, original_dimensions


def main():
    print("=" * 54)
    print("             IMAGE FORMAT CONVERTER")
    print("=" * 54)
    print("Supported formats: JPG, PNG, WebP")
    print("Original images will not be changed.\n")

    images = collect_images()
    if not images:
        print("\nNo images selected. Nothing to do.")
        return

    print(f"\nSelected {len(images)} image(s).")
    output_format = ask_choice(
        "Choose the output format", ["JPG", "PNG", "WEBP"]
    )

    print("\nOptional resizing")
    print("Enter a maximum width and/or height in pixels.")
    print("The image keeps its original proportions; it will not be stretched.")
    width = ask_positive_integer("Maximum width (Enter to skip): ")
    height = ask_positive_integer("Maximum height (Enter to skip): ")

    quality = 90
    if output_format in ("JPG", "WEBP"):
        while True:
            answer = input("Output quality 1-100 [default 90]: ").strip()
            if not answer:
                break
            try:
                quality = int(answer)
                if 1 <= quality <= 100:
                    break
            except ValueError:
                pass
            print("Enter a whole number from 1 to 100, or press Enter for 90.")

    default_output = Path.cwd() / "converted_images"
    raw_output = input(
        f"\nOutput folder [{default_output}]: "
    ).strip().strip('"').strip("'")
    output_dir = Path(raw_output).expanduser() if raw_output else default_output

    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        print(f"Could not create output folder: {error}")
        return

    print("\nConverting images...\n")
    successes = 0
    failures = 0
    total_before = 0
    total_after = 0

    for source in images:
        try:
            destination, before, after, old_dimensions = convert_image(
                source, output_dir, output_format, width, height, quality
            )
            with Image.open(destination) as result:
                new_dimensions = result.size

            successes += 1
            total_before += before
            total_after += after
            print(f"[OK] {source.name}")
            print(f"     {old_dimensions[0]}x{old_dimensions[1]} -> "
                  f"{new_dimensions[0]}x{new_dimensions[1]}")
            print(f"     {readable_size(before)} -> {readable_size(after)}")
            print(f"     Saved: {destination}")
        except (OSError, ValueError) as error:
            failures += 1
            print(f"[FAILED] {source}: {error}")
        print()

    print("=" * 54)
    print("CONVERSION SUMMARY")
    print("=" * 54)
    print(f"Successful: {successes}")
    print(f"Failed:     {failures}")
    if successes:
        difference = total_before - total_after
        print(f"Input size:  {readable_size(total_before)}")
        print(f"Output size: {readable_size(total_after)}")
        if difference > 0:
            print(f"Size saved:  {readable_size(difference)}")
        elif difference < 0:
            print(f"Size increase: {readable_size(-difference)}")
        else:
            print("Total file size stayed the same.")
        print(f"\nOutput folder: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
