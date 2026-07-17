# Terminal banner generator

The profile banner is built from two small Python programs:

1. `photo_to_ascii.py` converts a source photograph into `portrait.txt`.
2. `generate_profile.py` combines that portrait with `profile.json` and writes the SVG themes.

## Setup

```bash
python -m venv .venv
python -m pip install -r requirements.txt
```

Activate the environment using the command appropriate for your shell, then run:

```bash
python photo_to_ascii.py
python generate_profile.py
```

This produces:

- `dark.svg` for dark GitHub themes;
- `light.svg` for light GitHub themes;
- `profile.svg` as a backward-compatible dark-theme artifact.

## Profile configuration

Edit `profile.json` to change:

- personal profile fields;
- terminal commands and output;
- contact links;
- dark and light theme colors.

The fields `name`, `username`, `role`, `location`, and `email` can also be overridden temporarily with matching `PROFILE_*` environment variables.

## Portrait options

The default portrait is 56 characters wide. Useful options include:

```bash
python photo_to_ascii.py --width 56
python photo_to_ascii.py --crop LEFT TOP RIGHT BOTTOM
python photo_to_ascii.py --contrast 1.15
python photo_to_ascii.py --background-threshold 235
python photo_to_ascii.py --dither
python photo_to_ascii.py --palette "@%#*+=-:. "
```

Dithering is optional. It may preserve gradients and facial detail in some photographs, but the non-dithered output is often cleaner at small sizes.

Run `python photo_to_ascii.py --help` for every available option.

## Generated-file consistency

After changing `profile.json`, `portrait.txt`, or the generator, rerun:

```bash
python generate_profile.py
```

Commit the generator inputs and all three generated SVG files together so the README remains synchronized.
