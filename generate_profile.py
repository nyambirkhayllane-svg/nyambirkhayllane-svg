"""Generate matching dark and light terminal-profile SVGs."""

from __future__ import annotations

import os
from dataclasses import dataclass
from html import escape
from pathlib import Path
from typing import Iterable


PORTRAIT_PATH = Path("portrait.txt")
SVG_WIDTH, SVG_HEIGHT = 800, 360
CONTENT_TOP, CONTENT_BOTTOM = 52, 344
PORTRAIT_X, PORTRAIT_FONT_SIZE, PORTRAIT_LINE_HEIGHT = 24, 7.0, 7.0
PANEL_X, VALUE_X = 390, 482
TEXT_FONT_SIZE, TEXT_LINE_HEIGHT = 12, 26


@dataclass(frozen=True)
class Profile:
    """Displayed profile data, optionally overridden with PROFILE_* variables."""

    name: str = "Khayllane Nyambir"
    username: str = "nyambirkhayllane-svg"
    role: str = "Software Developer"
    location: str = "Mozambique"
    email: str = "nyambirkhayllane@gmail.com"

    @classmethod
    def from_environment(cls) -> "Profile":
        defaults = cls()
        names = ("name", "username", "role", "location", "email")
        return cls(**{
            name: os.getenv(f"PROFILE_{name.upper()}", getattr(defaults, name)).strip()
            for name in names
        })


@dataclass(frozen=True)
class Theme:
    """Color tokens shared by every element in one SVG variant."""

    name: str
    background: str
    header: str
    primary: str
    portrait: str
    accent: str
    muted: str
    border: str


DARK = Theme("dark", "#0d1117", "#161b22", "#e6edf3", "#c9d1d9", "#58a6ff", "#8b949e", "#30363d")
LIGHT = Theme("light", "#ffffff", "#f6f8fa", "#24292f", "#24292f", "#0969da", "#57606a", "#d0d7de")
THEMES = (DARK, LIGHT)


def read_portrait(path: Path = PORTRAIT_PATH) -> list[str]:
    """Read a non-empty UTF-8 portrait while preserving leading spaces."""
    if not path.is_file():
        raise FileNotFoundError(f"Portrait not found: {path.resolve()}")
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or not any(line.strip() for line in lines):
        raise ValueError(f"Portrait is empty: {path.resolve()}")
    return lines


def validate_portrait(lines: Iterable[str], max_width: int = 60) -> None:
    """Reject portrait dimensions that cannot fit the shared card layout."""
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


def theme_css(theme: Theme) -> str:
    """Create compact class-based CSS from theme tokens."""
    return f"""
    .card{{fill:{theme.background};stroke:{theme.border};stroke-width:1}}
    .header{{fill:{theme.header}}}
    .portrait,.label,.value,.prompt,.muted{{font-family:ui-monospace,SFMono-Regular,Consolas,"Liberation Mono",monospace;white-space:pre}}
    .portrait{{fill:{theme.portrait};font-size:{PORTRAIT_FONT_SIZE}px}}
    .label,.value,.prompt{{font-size:{TEXT_FONT_SIZE}px}}
    .label,.prompt{{fill:{theme.accent};font-weight:600}}
    .value{{fill:{theme.primary}}}.muted{{fill:{theme.muted};font-size:10px}}
    .cursor{{fill:{theme.accent};animation:blink 1.1s steps(2,start) infinite}}
    @keyframes blink{{50%{{opacity:0}}}}
    @media (prefers-reduced-motion:reduce){{.cursor{{animation:none}}}}
    """


def create_svg(portrait_lines: list[str], profile: Profile, theme: Theme) -> str:
    """Render one theme using the shared layout and content."""
    validate_portrait(portrait_lines)
    fields = (
        ("name", profile.name),
        ("role", profile.role),
        ("location", profile.location),
        ("email", profile.email),
        ("github", f"github.com/{profile.username}"),
    )
    row_y = CONTENT_TOP + 94
    rows = []
    for label, value in fields:
        rows.append(
            f'<text class="label" x="{PANEL_X}" y="{row_y}">{label}</text>'
            f'<text class="value" x="{VALUE_X}" y="{row_y}">{escape(value)}</text>'
        )
        row_y += TEXT_LINE_HEIGHT

    terminal_user = profile.name.split(maxsplit=1)[0].lower()
    title = f"{terminal_user}@github:~"
    return "".join((
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}" preserveAspectRatio="xMidYMid meet" role="img" aria-labelledby="title desc">',
        f'<title id="title">{escape(profile.name)} terminal profile — {theme.name} theme</title>',
        '<desc id="desc">ASCII portrait beside professional profile details</desc>',
        f'<style>{theme_css(theme)}</style>',
        f'<defs><clipPath id="content"><rect x="12" y="42" width="776" height="306" rx="4"/></clipPath></defs>',
        f'<rect class="card" x=".5" y=".5" width="799" height="359" rx="10"/>',
        '<path class="header" d="M10 .5h780a9.5 9.5 0 0 1 9.5 9.5v35H.5V10A9.5 9.5 0 0 1 10 .5Z"/>',
        '<circle cx="18" cy="18" r="4.5" fill="#ff5f56"/><circle cx="34" cy="18" r="4.5" fill="#ffbd2e"/><circle cx="50" cy="18" r="4.5" fill="#27c93f"/>',
        f'<text class="muted" x="400" y="22" text-anchor="middle">{escape(title)}</text>',
        '<g clip-path="url(#content)">', portrait_markup(portrait_lines),
        f'<text class="prompt" x="{PANEL_X}" y="{CONTENT_TOP + 25}">$ whoami</text>',
        f'<text class="muted" x="{PANEL_X}" y="{CONTENT_TOP + 51}">{escape(profile.username)}</text>',
        "".join(rows),
        f'<text class="prompt" x="{PANEL_X}" y="{row_y + 18}">$</text>',
        f'<rect class="cursor" x="{PANEL_X + 17}" y="{row_y + 7}" width="7" height="14" rx="1"/>',
        '</g></svg>',
    ))


def write_svgs(portrait_lines: list[str], profile: Profile) -> list[Path]:
    """Write both themes and a dark-theme legacy compatibility artifact."""
    outputs = []
    for theme in THEMES:
        path = Path(f"{theme.name}.svg")
        path.write_text(create_svg(portrait_lines, profile, theme), encoding="utf-8")
        outputs.append(path)
    Path("profile.svg").write_text(create_svg(portrait_lines, profile, DARK), encoding="utf-8")
    return outputs


def main() -> int:
    outputs = write_svgs(read_portrait(), Profile.from_environment())
    print("Generated: " + ", ".join(str(path.resolve()) for path in outputs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
