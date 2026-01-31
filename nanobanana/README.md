# Nano Banana Prompts (README Highlight Cards)

This folder contains prompts intended for an image generator ("Nano Banana") to produce **GitHub README highlight cards** for the OpenAI Codex "Ghost Regression" fix.

## Goals

- Create a recruiter-friendly visual hook above the fold.
- Stay factual and evidence-backed (no invented claims).
- Avoid scary security phrasing and avoid brand logos.

## Output Specs (Recommended)

- Format: PNG
- Theme: dark
- Primary palette: `#134e4a`, `#0d9488`, `#2dd4bf`
- Sizes:
  - Split Bars card: 1280×640
  - Terminal Receipt card: 1200×600 (or 1600×900 if you want extra legibility)

## Usage

1. Feed one prompt file from `dev/johnzfitch/nanobanana/prompts/` into Nano Banana.
2. Save outputs into `dev/johnzfitch/.github/assets/cards/` with stable filenames, e.g.:
   - `codex-ghost-regression-split-bars.png`
   - `codex-ghost-regression-terminal-receipt.png`
3. Embed the chosen image into `dev/johnzfitch/README.md` once generated.

