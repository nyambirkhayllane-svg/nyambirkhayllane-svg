from pathlib import Path

from PIL import Image, ImageOps


IMAGE_PATH = Path("photo.jpg")
OUTPUT_PATH = Path("portrait.txt")

ASCII_CHARS = "@%#*+=-:. "


def resize_image(image: Image.Image, new_width: int = 80) -> Image.Image:
    width, height = image.size
    aspect_ratio = height / width

    new_height = int(aspect_ratio * new_width * 0.55)

    return image.resize((new_width, new_height))


def pixels_to_ascii(image: Image.Image) -> str:
    pixels = image.getdata()

    characters = [
        ASCII_CHARS[pixel * len(ASCII_CHARS) // 256]
        for pixel in pixels
    ]

    return "".join(characters)


def main() -> None:
    if not IMAGE_PATH.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {IMAGE_PATH.resolve()}"
        )

    image = Image.open(IMAGE_PATH)
    image = ImageOps.grayscale(image)
    image = ImageOps.autocontrast(image)
    image = resize_image(image)

    ascii_data = pixels_to_ascii(image)

    width = image.width

    ascii_lines = [
        ascii_data[index:index + width]
        for index in range(0, len(ascii_data), width)
    ]

    result = "\n".join(ascii_lines)

    OUTPUT_PATH.write_text(result, encoding="utf-8")

    print(f"Arte ASCII criada em: {OUTPUT_PATH.resolve()}")


if __name__ == "__main__":
    main()