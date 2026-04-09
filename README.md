# Discord Wordle Emojis Generator

Generate Wordle-style PNG emoji tiles for Discord.

## What It Generates

- `gray_A` to `gray_Z`
- `white_A` to `white_Z`
- `green_A` to `green_Z`
- `yellow_A` to `yellow_Z`
- `gray_square`
- `white_square`

## Features

- Optional rounded tiles
- Optional subtle tile border
- Optional light text shadow
- Custom tile size
- Optional custom TTF font

## Requirements

- Python 3.10+
- Pillow (see `requirements.txt`)

## Quick Start

```bash
python -m pip install -r requirements.txt
python generate_discord_wordle_emojis.py --rounded --border --shadow
```

This generates files into `wordle_emojis` by default.

## Usage Examples

Default rounded output with border and shadow:

```bash
python generate_discord_wordle_emojis.py --rounded --border --shadow
```

Custom size:

```bash
python generate_discord_wordle_emojis.py --rounded --border --shadow --size 256
```

Custom font:

```bash
python generate_discord_wordle_emojis.py --rounded --border --shadow --font "/path/to/font.ttf"
```

Custom output folder:

```bash
python generate_discord_wordle_emojis.py --out generated_custom
```

## Showcase Files In This Repo

This repository intentionally keeps only a small showcase set in `generated_rounded_128`:

- `gray_A.png`
- `green_A.png`
- `yellow_A.png`
- `white_A.png`
- `gray_square.png`
- `white_square.png`

Generate the full set locally using the script.
