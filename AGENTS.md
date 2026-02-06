# AGENTS.md

## What This Repo Is
- GitHub profile README plus supporting assets (SVG cards, icons).
- Static portfolio site in `web/`, deployed via GitHub Pages.

## Commands
- `python3 scripts/gen_readme_assets.py` - regenerate `.github/assets/cards/*.svg` from `data/projects.toml`
- `nohup python3 -m http.server 5173 --bind 127.0.0.1 -d web >server.log 2>&1 & echo $! > server.pid` - preview the site locally

## Style Rules
- README: ASCII-only text, no emoji.
- Icons: prefer `.github/assets/icons/` (iconics-derived). Use 24x24 in Markdown/HTML.
- Privacy: no analytics, tracking pixels, or view counters.

## Key Files
- `README.md` - profile README
- `data/projects.toml` - authoritative project catalog
- `scripts/gen_readme_assets.py` - SVG card generator
- `.github/workflows/readme-dashboard.yml` - scheduled refresh + commit
- `.github/workflows/pages.yml` - deploy `web/` to GitHub Pages
