"""Convert a photograph into the ASCII portrait used by the profile card."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from PIL import Image, ImageEnhance, ImageFilter, ImageOps, UnidentifiedImageError


DEFAULT_IMAGE_PATH = Path("photo.jpg")
DEFAULT_OUTPUT_PATH = Path("portrait.txt")
DEFAULT_PALETTE = "@%#*+=-:. "


@dataclass(frozen=True)
class AsciiConfig:
    """Settings for predictable, reusable portrait conversion."""

    width: int = 56
    palette: str = DEFAULT_PALETTE
    character_aspect: float = 0.52
    crop: tuple[int, int, int, int] | None = None
    contrast: float = 1.08
    sharpen: bool = True
    background_threshold: int | None = None
    dither: bool = False

    def validate(self) -> None:
        if self.width <= 0:
            raise ValueError("ASCII width must be greater than zero")
        if len(self.palette) < 2:
            raise ValueError("ASCII palette must contain at least two characters")
        if not 0 < self.character_aspect <= 1:
            raise ValueError("Character aspect ratio must be between 0 and 1")
        if self.contrast <= 0:
            raise ValueError("Contrast must be greater than zero")
        if self.background_threshold is not None and not 0 <= self.background_threshold <= 255:
            raise ValueError("Background threshold must be between 0 and 255")


def load_image(path: Path, crop: tuple[int, int, int, int] | None = None) -> Image.Image:
    """Load an image safely and return a detached RGB copy."""
    if not path.is_file():
        raise FileNotFoundError(f"Source image not found: {path.resolve()}")
    try:
        with Image.open(path) as source:
            image = ImageOps.exif_transpose(source).convert("RGB")
    except (UnidentifiedImageError, OSError) as error:
        raise ValueError(f"Unable to read image {path.resolve()}: {error}") from error

    if crop is not None:
        left, top, right, bottom = crop
        if left < 0 or top < 0 or right > image.width or bottom > image.height:
            raise ValueError(f"Crop {crop} exceeds image bounds {image.size}")
        if right <= left or bottom <= top:
            raise ValueError("Crop must satisfy right > left and bottom > top")
        image = image.crop(crop)
    return image


def prepare_image(image: Image.Image, config: AsciiConfig) -> Image.Image:
    """Normalize tone, optionally enhance detail, and resize for text cells."""
    config.validate()
    grayscale = ImageOps.grayscale(image)
    grayscale = ImageOps.autocontrast(grayscale, cutoff=1)
    grayscale = ImageEnhance.Contrast(grayscale).enhance(config.contrast)
    if config.sharpen:
        grayscale = grayscale.filter(ImageFilter.UnsharpMask(radius=1, percent=125, threshold=3))
    if config.background_threshold is not None:
        threshold = config.background_threshold
        grayscale = grayscale.point(lambda value: 255 if value >= threshold else value)

    height = max(1, round(grayscale.height / grayscale.width * config.width * config.character_aspect))
    return grayscale.resize((config.width, height), Image.Resampling.LANCZOS)


def image_to_lines(image: Image.Image, palette: str) -> list[str]:
    """Map grayscale pixels to ordered characters, one string per image row."""
    if image.mode != "L":
        raise ValueError("ASCII conversion expects a grayscale image")
    last_index = len(palette) - 1
    characters = [
        palette[pixel * last_index // 255]
        for pixel in image.get_flattened_data()
    ]
    return [
        "".join(characters[start:start + image.width]).rstrip()
        for start in range(0, len(characters), image.width)
    ]


def dither_image(image: Image.Image, levels: int) -> Image.Image:
    """Apply optional Floyd–Steinberg dithering using the palette density."""
    if levels < 2:
        raise ValueError("Dithering requires at least two palette characters")
    return image.quantize(
        colors=levels,
        method=Image.Quantize.MAXCOVERAGE,
        dither=Image.Dither.FLOYDSTEINBERG,
    ).convert("L")


def convert_image(input_path: Path, output_path: Path, config: AsciiConfig) -> list[str]:
    """Run the complete conversion and write UTF-8 portrait text."""
    prepared = prepare_image(load_image(input_path, config.crop), config)
    if config.dither:
        prepared = dither_image(prepared, len(config.palette))
    lines = image_to_lines(prepared, config.palette)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return lines


def parse_crop(values: Sequence[int] | None) -> tuple[int, int, int, int] | None:
    if values is None:
        return None
    left, top, right, bottom = values
    return left, top, right, bottom


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_IMAGE_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--width", type=int, default=56, help="portrait width in characters")
    parser.add_argument("--palette", default=DEFAULT_PALETTE, help="characters from darkest to lightest")
    parser.add_argument("--aspect", type=float, default=0.52, help="monospace character aspect compensation")
    parser.add_argument("--crop", type=int, nargs=4, metavar=("LEFT", "TOP", "RIGHT", "BOTTOM"))
    parser.add_argument("--contrast", type=float, default=1.08)
    parser.add_argument("--no-sharpen", action="store_true", help="disable subtle detail enhancement")
    parser.add_argument("--background-threshold", type=int, help="make pixels at or above this level blank")
    parser.add_argument("--dither", action="store_true", help="use Floyd–Steinberg dithering for tonal detail")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = AsciiConfig(
        width=args.width,
        palette=args.palette,
        character_aspect=args.aspect,
        crop=parse_crop(args.crop),
        contrast=args.contrast,
        sharpen=not args.no_sharpen,
        background_threshold=args.background_threshold,
        dither=args.dither,
    )
    try:
        lines = convert_image(args.input, args.output, config)
    except (FileNotFoundError, ValueError) as error:
        raise SystemExit(f"error: {error}") from error
    print(f"ASCII portrait created: {args.output.resolve()} ({config.width}×{len(lines)} characters)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
