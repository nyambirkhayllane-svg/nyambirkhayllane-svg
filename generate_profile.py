from pathlib import Path
from html import escape


PORTRAIT_PATH = Path("portrait.txt")
OUTPUT_PATH = Path("profile.svg")

NAME = "Khayllane Nyambir"
USERNAME = "nyambirkhayllane-svg"
ROLE = "Developer"
LOCATION = "Seu país"
EMAIL = "seu-email@example.com"

BACKGROUND = "#0d1117"
TEXT_COLOR = "#c9d1d9"
ACCENT_COLOR = "#58a6ff"
MUTED_COLOR = "#8b949e"

FONT_SIZE = 14
LINE_HEIGHT = 18
WIDTH = 1000
PADDING = 30


def read_portrait() -> list[str]:
    if not PORTRAIT_PATH.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {PORTRAIT_PATH.resolve()}"
        )

    return PORTRAIT_PATH.read_text(encoding="utf-8").splitlines()


def create_svg(portrait_lines: list[str]) -> str:
    portrait_height = len(portrait_lines) * LINE_HEIGHT
    height = max(520, portrait_height + (PADDING * 2))

    svg_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{WIDTH}" height="{height}" '
            f'viewBox="0 0 {WIDTH} {height}">'
        ),
        "<style>",
        """
        .background {
            fill: #0d1117;
        }

        .terminal-text {
            font-family: Consolas, Monaco, "Courier New", monospace;
            font-size: 14px;
            white-space: pre;
        }

        .portrait {
            fill: #c9d1d9;
        }

        .label {
            fill: #58a6ff;
            font-weight: bold;
        }

        .value {
            fill: #c9d1d9;
        }

        .muted {
            fill: #8b949e;
        }

        .cursor {
            fill: #58a6ff;
            animation: blink 1s steps(2, start) infinite;
        }

        @keyframes blink {
            50% {
                opacity: 0;
            }
        }
        """,
        "</style>",
        (
            f'<rect class="background" width="{WIDTH}" '
            f'height="{height}" rx="12"/>'
        ),
    ]

    portrait_x = PADDING
    portrait_y = PADDING + FONT_SIZE

    for index, line in enumerate(portrait_lines):
        y = portrait_y + index * LINE_HEIGHT
        svg_lines.append(
            f'<text class="terminal-text portrait" '
            f'x="{portrait_x}" y="{y}">{escape(line)}</text>'
        )

    longest_line = max((len(line) for line in portrait_lines), default=0)
    info_x = min(620, PADDING + longest_line * 8 + 40)
    info_y = 90

    information = [
        ("user", USERNAME),
        ("name", NAME),
        ("role", ROLE),
        ("location", LOCATION),
        ("email", EMAIL),
        ("github", f"github.com/{USERNAME}"),
    ]

    svg_lines.append(
        f'<text class="terminal-text label" '
        f'x="{info_x}" y="{info_y}">{escape(USERNAME)}</text>'
    )

    svg_lines.append(
        f'<text class="terminal-text muted" '
        f'x="{info_x}" y="{info_y + LINE_HEIGHT}">'
        "--------------------------------"
        "</text>"
    )

    current_y = info_y + LINE_HEIGHT * 3

    for label, value in information:
        svg_lines.append(
            f'<text class="terminal-text label" '
            f'x="{info_x}" y="{current_y}">{escape(label)}:</text>'
        )

        svg_lines.append(
            f'<text class="terminal-text value" '
            f'x="{info_x + 100}" y="{current_y}">'
            f"{escape(value)}</text>"
        )

        current_y += LINE_HEIGHT * 2

    svg_lines.append(
        f'<text class="terminal-text label" '
        f'x="{info_x}" y="{current_y + 20}">$</text>'
    )

    svg_lines.append(
        f'<rect class="cursor" '
        f'x="{info_x + 18}" y="{current_y + 7}" '
        f'width="9" height="16"/>'
    )

    svg_lines.append("</svg>")

    return "\n".join(svg_lines)


def main() -> None:
    portrait_lines = read_portrait()
    svg = create_svg(portrait_lines)

    OUTPUT_PATH.write_text(svg, encoding="utf-8")

    print(f"SVG criado em: {OUTPUT_PATH.resolve()}")


if __name__ == "__main__":
    main()