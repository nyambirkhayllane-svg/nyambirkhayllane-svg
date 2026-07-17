"""Generate matching dark and light terminal-profile SVGs."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from html import escape
from pathlib import Path
from typing import Any, Iterable


CONFIG_PATH = Path("profile.json")
PORTRAIT_PATH = Path("portrait.txt")
SVG_WIDTH, SVG_HEIGHT = 800, 360
CONTENT_TOP, CONTENT_BOTTOM = 52, 344
PORTRAIT_X, PORTRAIT_FONT_SIZE, PORTRAIT_LINE_HEIGHT = 24, 7.0, 7.0
PANEL_X, TEXT_FONT_SIZE = 390, 11


@dataclass(frozen=True)
class Profile:
    name: str
    username: str
    role: str
    location: str
    email: str


@dataclass(frozen=True)
class Theme:
    name: str
    background: str
    header: str
    primary: str
    portrait: str
    accent: str
    muted: str
    border: str


@dataclass(frozen=True)
class Settings:
    profile: Profile
    terminal: tuple[tuple[str, str], ...]
    links: dict[str, str]
    themes: tuple[Theme, ...]


def require_mapping(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        raise ValueError(f"Configuration field '{key}' must be an object")
    return value


def load_settings(path: Path = CONFIG_PATH) -> Settings:
    """Load and validate changeable profile content from JSON."""
    if not path.is_file():
        raise FileNotFoundError(f"Configuration not found: {path.resolve()}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON in {path}: {error}") from error
    if not isinstance(data, dict):
        raise ValueError("Profile configuration must be a JSON object")

    profile_data = require_mapping(data, "profile")
    profile_fields = ("name", "username", "role", "location", "email")
    profile_values = {}
    for field in profile_fields:
        value = os.getenv(f"PROFILE_{field.upper()}", str(profile_data.get(field, ""))).strip()
        if not value:
            raise ValueError(f"Profile field '{field}' cannot be empty")
        profile_values[field] = value

    terminal_data = data.get("terminal")
    if not isinstance(terminal_data, list) or not terminal_data:
        raise ValueError("Configuration field 'terminal' must be a non-empty list")
    terminal = []
    for index, entry in enumerate(terminal_data):
        if not isinstance(entry, list) or len(entry) != 2 or not all(isinstance(item, str) and item for item in entry):
            raise ValueError(f"Terminal entry {index} must contain a command and output")
        terminal.append((entry[0], entry[1]))

    theme_data = require_mapping(data, "themes")
    color_fields = ("background", "header", "primary", "portrait", "accent", "muted", "border")
    themes = []
    for name in ("dark", "light"):
        colors = require_mapping(theme_data, name)
        missing = [field for field in color_fields if not isinstance(colors.get(field), str)]
        if missing:
            raise ValueError(f"Theme '{name}' is missing: {', '.join(missing)}")
        themes.append(Theme(name=name, **{field: colors[field] for field in color_fields}))

    links = require_mapping(data, "links")
    return Settings(Profile(**profile_values), tuple(terminal), {str(k): str(v) for k, v in links.items()}, tuple(themes))


def read_portrait(path: Path = PORTRAIT_PATH) -> list[str]:
    if not path.is_file():
        raise FileNotFoundError(f"Portrait not found: {path.resolve()}")
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or not any(line.strip() for line in lines):
        raise ValueError(f"Portrait is empty: {path.resolve()}")
    return lines


def validate_portrait(lines: Iterable[str], max_width: int = 60) -> None:
    rows = list(lines)
    width = max(map(len, rows), default=0)
    final_baseline = CONTENT_TOP + 10 + (len(rows) - 1) * PORTRAIT_LINE_HEIGHT
    if width > max_width:
        raise ValueError(f"Portrait is {width} characters wide; maximum is {max_width}")
    if final_baseline > CONTENT_BOTTOM:
        raise ValueError(f"Portrait has {len(rows)} rows and exceeds the card height")


def portrait_markup(lines: list[str]) -> str:
    rows = "".join(
        f'<tspan x="{PORTRAIT_X}" dy="{0 if index == 0 else PORTRAIT_LINE_HEIGHT}">'
        f'{escape(line.rstrip())}</tspan>'
        for index, line in enumerate(lines)
    )
    return f'<text class="portrait" x="{PORTRAIT_X}" y="{CONTENT_TOP + 10}">{rows}</text>'


def terminal_markup(entries: tuple[tuple[str, str], ...]) -> str:
    """Render a compact shell transcript with consistent command spacing."""
    y = CONTENT_TOP + 18
    markup = []
    for command, output in entries:
        markup.append(f'<text class="prompt" x="{PANEL_X}" y="{y}">$ {escape(command)}</text>')
        markup.append(f'<text class="value" x="{PANEL_X}" y="{y + 18}">{escape(output)}</text>')
        y += 54
    cursor_y = min(y - 11, CONTENT_BOTTOM - 14)
    markup.append(f'<text class="prompt" x="{PANEL_X}" y="{cursor_y + 11}">$</text>')
    markup.append(f'<rect class="cursor" x="{PANEL_X + 17}" y="{cursor_y}" width="7" height="14" rx="1"/>')
    return "".join(markup)


def theme_css(theme: Theme) -> str:
    return f"""
    .card{{fill:{theme.background};stroke:{theme.border};stroke-width:1}}
    .header{{fill:{theme.header}}}
    .portrait,.value,.prompt,.muted{{font-family:ui-monospace,SFMono-Regular,Consolas,"Liberation Mono",monospace;white-space:pre}}
    .portrait{{fill:{theme.portrait};font-size:{PORTRAIT_FONT_SIZE}px}}
    .value,.prompt{{font-size:{TEXT_FONT_SIZE}px}}
    .prompt{{fill:{theme.accent};font-weight:600}}.value{{fill:{theme.primary}}}
    .muted{{fill:{theme.muted};font-size:10px}}
    .cursor{{fill:{theme.accent};animation:blink 1.1s steps(2,start) infinite}}
    @keyframes blink{{50%{{opacity:0}}}}
    @media (prefers-reduced-motion:reduce){{.cursor{{animation:none}}}}
    """


def create_svg(portrait_lines: list[str], settings: Settings, theme: Theme) -> str:
    validate_portrait(portrait_lines)
    terminal_user = settings.profile.name.split(maxsplit=1)[0].lower()
    title = f"{terminal_user}@github:~"
    return "".join((
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}" preserveAspectRatio="xMidYMid meet" role="img" aria-labelledby="title desc">',
        f'<title id="title">{escape(settings.profile.name)} terminal profile — {theme.name} theme</title>',
        '<desc id="desc">ASCII portrait and a terminal session describing current work and learning</desc>',
        f'<style>{theme_css(theme)}</style>',
        '<defs><clipPath id="content"><rect x="12" y="42" width="776" height="306" rx="4"/></clipPath></defs>',
        '<rect class="card" x=".5" y=".5" width="799" height="359" rx="10"/>',
        '<path class="header" d="M10 .5h780a9.5 9.5 0 0 1 9.5 9.5v35H.5V10A9.5 9.5 0 0 1 10 .5Z"/>',
        '<circle cx="18" cy="18" r="4.5" fill="#ff5f56"/><circle cx="34" cy="18" r="4.5" fill="#ffbd2e"/><circle cx="50" cy="18" r="4.5" fill="#27c93f"/>',
        f'<text class="muted" x="400" y="22" text-anchor="middle">{escape(title)}</text>',
        '<g clip-path="url(#content)">', portrait_markup(portrait_lines),
        terminal_markup(settings.terminal), '</g></svg>',
    ))


def write_svgs(portrait_lines: list[str], settings: Settings) -> list[Path]:
    outputs = []
    for theme in settings.themes:
        path = Path(f"{theme.name}.svg")
        path.write_text(create_svg(portrait_lines, settings, theme), encoding="utf-8")
        outputs.append(path)
    dark = next(theme for theme in settings.themes if theme.name == "dark")
    Path("profile.svg").write_text(create_svg(portrait_lines, settings, dark), encoding="utf-8")
    return outputs


def main() -> int:
    outputs = write_svgs(read_portrait(), load_settings())
    print("Generated: " + ", ".join(str(path.resolve()) for path in outputs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
