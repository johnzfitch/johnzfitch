#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
import tomllib
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Project:
    id: str
    title: str
    desc: str
    tags: list[str]
    repo: str | None
    demo: str | None
    private: bool


@dataclass(frozen=True)
class Category:
    id: str
    title: str
    icon: str | None
    projects: list[Project]


@dataclass(frozen=True)
class RepoStats:
    stars: int
    pushed_at: datetime


def _die(msg: str) -> None:
    raise SystemExit(msg)


def _require_ascii(label: str, value: str) -> None:
    try:
        value.encode("ascii")
    except UnicodeEncodeError as exc:
        _die(f"Non-ASCII in {label}: {value!r} ({exc})")


def _esc(s: str) -> str:
    # Basic XML escape for text nodes.
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def _read_toml(path: Path) -> dict[str, Any]:
    with path.open("rb") as f:
        data = tomllib.load(f)
    if not isinstance(data, dict):
        _die(f"Invalid TOML root: {path}")
    return data


def _load_catalog(path: Path) -> list[Category]:
    data = _read_toml(path)
    categories_raw = data.get("categories")
    if not isinstance(categories_raw, list) or not categories_raw:
        _die(f"Expected [[categories]] in {path}")

    categories: list[Category] = []
    for c in categories_raw:
        if not isinstance(c, dict):
            _die(f"Invalid category entry in {path}: {c!r}")

        cid = str(c.get("id", "")).strip()
        title = str(c.get("title", "")).strip()
        icon = c.get("icon")
        icon_s = str(icon).strip() if icon else None

        if not cid or not title:
            _die(f"Category missing id/title in {path}: {c!r}")
        _require_ascii(f"category.id {cid}", cid)
        _require_ascii(f"category.title {cid}", title)

        projects_raw = c.get("projects", [])
        if not isinstance(projects_raw, list):
            _die(f"Invalid projects list for category {cid} in {path}")

        projects: list[Project] = []
        for p in projects_raw:
            if not isinstance(p, dict):
                _die(f"Invalid project entry in category {cid}: {p!r}")

            pid = str(p.get("id", "")).strip()
            ptitle = str(p.get("title", "")).strip()
            desc = str(p.get("desc", "")).strip()

            repo = p.get("repo")
            repo_s = str(repo).strip() if repo else None

            demo = p.get("demo")
            demo_s = str(demo).strip() if demo else None

            private = bool(p.get("private", False))

            tags_raw = p.get("tags", [])
            if not isinstance(tags_raw, list):
                _die(f"Invalid tags for project {pid} in category {cid}")
            tags = [str(t).strip() for t in tags_raw if str(t).strip()]

            if not pid or not ptitle or not desc:
                _die(f"Project missing required fields in category {cid}: {p!r}")

            _require_ascii(f"project.id {pid}", pid)
            _require_ascii(f"project.title {pid}", ptitle)
            _require_ascii(f"project.desc {pid}", desc)
            for t in tags:
                _require_ascii(f"project.tag {pid}", t)

            projects.append(
                Project(
                    id=pid,
                    title=ptitle,
                    desc=desc,
                    tags=tags,
                    repo=repo_s,
                    demo=demo_s,
                    private=private,
                )
            )

        categories.append(Category(id=cid, title=title, icon=icon_s, projects=projects))

    return categories


def _http_json(url: str, token: str | None) -> dict[str, Any]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "johnzfitch-readme-dashboard",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read().decode("utf-8")
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise ValueError(f"Unexpected JSON type from {url}")
    return payload


def _fetch_repo_stats(repo: str, token: str | None) -> RepoStats | None:
    if "/" not in repo:
        return None

    url = f"https://api.github.com/repos/{repo}"
    try:
        payload = _http_json(url, token)
    except urllib.error.HTTPError as exc:
        # Running without a token can hit rate limits; don't fail the whole build.
        if exc.code in (403, 404):
            return None
        return None
    except Exception:
        return None

    stars = int(payload.get("stargazers_count", 0))
    pushed_at_raw = str(payload.get("pushed_at", "")).strip()
    if not pushed_at_raw:
        return None

    pushed_at = datetime.fromisoformat(pushed_at_raw.replace("Z", "+00:00")).astimezone(
        timezone.utc
    )
    return RepoStats(stars=stars, pushed_at=pushed_at)


def _format_k(n: int) -> str:
    if n < 1000:
        return str(n)
    if n < 10_000:
        return f"{n/1000:.1f}k"
    if n < 1_000_000:
        return f"{n//1000}k"
    return f"{n/1_000_000:.1f}m"


def _split_into_columns(categories: list[Category]) -> tuple[list[Category], list[Category]]:
    # Greedy balance by total blocks (category header + project rows).
    cats_sorted = sorted(categories, key=lambda c: len(c.projects), reverse=True)
    cols: list[list[Category]] = [[], []]
    load = [0, 0]

    for c in cats_sorted:
        idx = 0 if load[0] <= load[1] else 1
        cols[idx].append(c)
        load[idx] += 1 + len(c.projects)

    # Preserve original ordering within each column.
    order = {c.id: i for i, c in enumerate(categories)}
    for col in cols:
        col.sort(key=lambda c: order.get(c.id, 0))

    return cols[0], cols[1]


def _svg_text(x: float, y: float, text: str, cls: str, anchor: str | None = None) -> str:
    anchor_attr = f' text-anchor="{anchor}"' if anchor else ""
    return f'<text x="{x}" y="{y}" class="{cls}"{anchor_attr}>{_esc(text)}</text>'


def _render_project_dashboard_svg(
    *,
    categories: list[Category],
    repo_stats: dict[str, RepoStats],
    icon_data: dict[str, str],
    variant: str,
    layout: str,
) -> str:
    if variant not in ("light", "dark"):
        _die(f"Invalid variant: {variant}")
    if layout not in ("desktop", "mobile"):
        _die(f"Invalid layout: {layout}")

    if variant == "light":
        bg0 = "#f8fafc"
        bg1 = "#ffffff"
        border = "#cbd5e1"
        text = "#0f172a"
        muted = "#334155"
        subtle = "#64748b"
        accent0 = "#0ea5e9"
        accent1 = "#14b8a6"
    else:
        bg0 = "#050816"
        bg1 = "#0b1227"
        border = "#26324a"
        text = "#e2e8f0"
        muted = "#cbd5e1"
        subtle = "#94a3b8"
        accent0 = "#22d3ee"
        accent1 = "#34d399"

    if layout == "desktop":
        width = 1200
        pad = 28
        gap_col = 28
        col_w = (width - pad * 2 - gap_col) / 2
        col_left, col_right = _split_into_columns(categories)
        columns = [col_left, col_right]
    else:
        width = 920
        pad = 28
        gap_col = 0
        col_w = width - pad * 2
        columns = [categories]

    title_h = 70
    cat_h = 34
    proj_h = 46
    gap_y = 10

    def column_height(col: list[Category]) -> int:
        h = 0
        for c in col:
            h += cat_h + gap_y
            h += len(c.projects) * proj_h
            h += gap_y
        return h

    content_h = max(column_height(col) for col in columns)
    height = int(pad * 2 + title_h + content_h + 6)

    total_stars = sum(s.stars for s in repo_stats.values())
    last_push_dt = max((s.pushed_at for s in repo_stats.values()), default=None)
    last_push = last_push_dt.strftime("%Y-%m-%d") if last_push_dt else "unknown"

    parts: list[str] = []
    title_text = _svg_text(pad, pad + 34, "PROJECT DASHBOARD", "title")
    meta_text = _svg_text(
        pad,
        pad + 56,
        f"Signal: {_format_k(total_stars)} stars | Last push: {last_push} | Layout: {layout}",
        "meta",
    )
    parts.append(
        (
            """<svg xmlns="http://www.w3.org/2000/svg" width="%(width)d" height="%(height)d" viewBox="0 0 %(width)d %(height)d" role="img" aria-labelledby="title desc">
  <title id="title">Project dashboard</title>
  <desc id="desc">Projects grouped by category with live repo stats.</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="%(bg0)s" />
      <stop offset="1" stop-color="%(bg1)s" />
    </linearGradient>
    <linearGradient id="hdr" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="%(accent0)s" stop-opacity="0.95" />
      <stop offset="1" stop-color="%(accent1)s" stop-opacity="0.95" />
    </linearGradient>
    <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M 24 0 L 0 0 0 24" fill="none" stroke="%(border)s" stroke-width="1" opacity="0.22" />
    </pattern>
    <filter id="soft" x="-20%%" y="-20%%" width="140%%" height="140%%">
      <feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#000" flood-opacity="0.22" />
    </filter>
    <style><![CDATA[
      .title { font: 800 28px ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial; fill: %(text)s; }
      .meta { font: 600 13px ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial; fill: %(subtle)s; }
      .cat { font: 800 14px ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial; fill: #001018; letter-spacing: 0.10em; }
      .name { font: 800 15px ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; fill: %(text)s; }
      .desc { font: 600 12px ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial; fill: %(muted)s; }
      .stats { font: 800 12px ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; fill: %(subtle)s; }
    ]]></style>
  </defs>

  <rect x="0" y="0" width="%(width)d" height="%(height)d" rx="18" fill="url(#bg)" />
  <rect x="0" y="0" width="%(width)d" height="%(height)d" rx="18" fill="url(#grid)" />
  <rect x="%(pad)d" y="%(pad)d" width="%(inner_w)d" height="%(inner_h)d" rx="16" fill="none" stroke="%(border)s" stroke-width="2" />

  <g filter="url(#soft)">
    <rect x="%(pad)d" y="%(pad)d" width="%(inner_w)d" height="%(title_h)d" rx="14" fill="none" />
  </g>

  %(title_text)s
  %(meta_text)s
"""
            % {
                "width": width,
                "height": height,
                "bg0": bg0,
                "bg1": bg1,
                "border": border,
                "text": text,
                "muted": muted,
                "subtle": subtle,
                "accent0": accent0,
                "accent1": accent1,
                "pad": pad,
                "inner_w": int(width - pad * 2),
                "inner_h": int(height - pad * 2),
                "title_h": title_h,
                "title_text": title_text,
                "meta_text": meta_text,
            }
        )
    )

    def render_column(col: list[Category], x0: float, y0: float) -> None:
        y = y0
        for cat in col:
            parts.append(
                f'<rect x="{x0}" y="{y}" width="{col_w}" height="{cat_h}" rx="10" fill="url(#hdr)" opacity="0.92" />'
            )
            icon_href = icon_data.get(cat.icon or "")
            text_x = x0 + 14
            if icon_href:
                parts.append(
                    f'<image x="{x0 + 10}" y="{y + 5}" width="24" height="24" href="{icon_href}" />'
                )
                text_x = x0 + 44
            parts.append(_svg_text(text_x, y + 22, cat.title.upper(), "cat"))
            y += cat_h + gap_y

            for proj in cat.projects:
                is_private = proj.private or not proj.repo

                stats = repo_stats.get(proj.repo or "") if proj.repo else None
                stars_s = _format_k(stats.stars) if stats else "--"
                pushed_s = stats.pushed_at.strftime("%Y-%m-%d") if stats else "----"

                right = f"{stars_s}* {pushed_s}" if not is_private else "private"

                name = proj.title
                if is_private:
                    name = f"{name} [private]"

                name_y = y + 17
                desc_y = y + 36
                parts.append(_svg_text(x0 + 12, name_y, name, "name"))
                parts.append(_svg_text(x0 + col_w - 12, name_y, right, "stats", anchor="end"))

                desc = proj.desc
                if proj.tags:
                    desc = f"{desc} ({', '.join(proj.tags)})"

                max_len = 92 if layout == "desktop" else 110
                if len(desc) > max_len:
                    desc = desc[: max_len - 3].rstrip() + "..."

                parts.append(_svg_text(x0 + 12, desc_y, desc, "desc"))
                parts.append(
                    f'<line x1="{x0 + 10}" y1="{y + proj_h}" x2="{x0 + col_w - 10}" y2="{y + proj_h}" stroke="{border}" stroke-width="1" opacity="0.35" />'
                )

                y += proj_h

            y += gap_y

    y_start = pad + title_h + 10
    if layout == "desktop":
        x_left = pad
        x_right = pad + col_w + gap_col
        render_column(columns[0], x_left, y_start)
        render_column(columns[1], x_right, y_start)
    else:
        render_column(columns[0], pad, y_start)

    parts.append("</svg>\n")

    svg = "\n".join(parts)
    _require_ascii(f"project dashboard svg ({variant},{layout})", svg)
    return svg


def _render_typing_philosophy_svg(*, variant: str) -> str:
    if variant not in ("light", "dark"):
        _die(f"Invalid variant: {variant}")

    if variant == "light":
        text = "#0f172a"
        subtle = "#334155"
        caret = "#14b8a6"
    else:
        text = "#e2e8f0"
        subtle = "#94a3b8"
        caret = "#34d399"

    width = 1200
    height = 70
    phrase = "The best way to predict AI's impact is to build tools that shape it."
    _require_ascii("philosophy", phrase)

    # Typing effect is a blinking caret; text is always visible as fallback.
    svg = (
        """<svg xmlns="http://www.w3.org/2000/svg" width="%(width)d" height="%(height)d" viewBox="0 0 %(width)d %(height)d" role="img" aria-labelledby="title desc">
  <title id="title">Philosophy</title>
  <desc id="desc">%(phrase)s</desc>
  <defs>
    <style><![CDATA[
      .t { font: 800 26px ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; fill: %(text)s; }
      .s { font: 700 13px ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial; fill: %(subtle)s; }
      .caret { animation: blink 1s step-end infinite; fill: %(caret)s; }
      @keyframes blink { 50%% { opacity: 0; } }
    ]]></style>
  </defs>

  <rect x="0" y="0" width="%(width)d" height="%(height)d" rx="14" fill="none" />
  <text x="24" y="42" class="t">%(phrase)s</text>
  <rect x="1140" y="18" width="12" height="30" rx="2" class="caret" />
  <text x="24" y="62" class="s">Evidence-first systems, security, and tooling.</text>
</svg>
"""
        % {
            "width": width,
            "height": height,
            "phrase": _esc(phrase),
            "text": text,
            "subtle": subtle,
            "caret": caret,
        }
    )

    _require_ascii(f"typing svg ({variant})", svg)
    return svg


def _render_portal_badge_svg(*, variant: str, total_stars: int, last_push: str) -> str:
    if variant not in ("light", "dark"):
        _die(f"Invalid variant: {variant}")

    bg = "#050816" if variant == "dark" else "#0b1227"
    border = "#26324a" if variant == "dark" else "#1f2a44"
    text = "#e2e8f0"
    subtle = "#cbd5e1"
    accent0 = "#22d3ee"
    accent1 = "#34d399"

    width = 1200
    height = 120

    line1 = "PORTAL BADGE"
    line2 = "CLICK TO ENTER: PORTFOLIO"
    line3 = f"SIGNAL: {_format_k(total_stars)} stars | LAST PUSH: {last_push} | NO TRACKING"

    for label, val in [("line1", line1), ("line2", line2), ("line3", line3)]:
        _require_ascii(label, val)

    svg = (
        """<svg xmlns="http://www.w3.org/2000/svg" width="%(width)d" height="%(height)d" viewBox="0 0 %(width)d %(height)d" role="img" aria-labelledby="title desc">
  <title id="title">Portal badge</title>
  <desc id="desc">A clickable portal badge linking to the portfolio site.</desc>
  <defs>
    <linearGradient id="glow" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="%(accent0)s" stop-opacity="0.95" />
      <stop offset="1" stop-color="%(accent1)s" stop-opacity="0.95" />
    </linearGradient>
    <filter id="soft" x="-20%%" y="-20%%" width="140%%" height="140%%">
      <feDropShadow dx="0" dy="0" stdDeviation="10" flood-color="%(accent0)s" flood-opacity="0.35" />
    </filter>
    <pattern id="scan" width="6" height="6" patternUnits="userSpaceOnUse">
      <rect x="0" y="0" width="6" height="1" fill="#ffffff" opacity="0.08" />
    </pattern>
    <style><![CDATA[
      .h { font: 900 20px ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; fill: %(text)s; letter-spacing: 0.12em; }
      .b { font: 900 18px ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; fill: %(text)s; }
      .s { font: 800 12px ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; fill: %(subtle)s; }
      .caret { animation: blink 1s step-end infinite; fill: url(#glow); }
      @keyframes blink { 50%% { opacity: 0; } }
    ]]></style>
  </defs>

  <rect x="0" y="0" width="%(width)d" height="%(height)d" rx="18" fill="%(bg)s" stroke="%(border)s" stroke-width="2" />
  <rect x="0" y="0" width="%(width)d" height="%(height)d" rx="18" fill="url(#scan)" />

  <g filter="url(#soft)">
    <rect x="18" y="18" width="10" height="84" rx="5" fill="url(#glow)" />
  </g>

  <text x="48" y="44" class="h">%(line1)s</text>
  <text x="48" y="72" class="b">%(line2)s</text>
  <text x="48" y="96" class="s">%(line3)s</text>

  <rect x="1138" y="30" width="14" height="30" rx="2" class="caret" />
</svg>
"""
        % {
            "width": width,
            "height": height,
            "bg": bg,
            "border": border,
            "text": text,
            "subtle": subtle,
            "accent0": accent0,
            "accent1": accent1,
            "line1": _esc(line1),
            "line2": _esc(line2),
            "line3": _esc(line3),
        }
    )

    _require_ascii(f"portal badge svg ({variant})", svg)
    return svg


def _write_if_changed(path: Path, content: str) -> bool:
    existing = None
    if path.exists():
        existing = path.read_text(encoding="utf-8")
    if existing == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def _load_png_data_uri(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    raw = path.read_bytes()
    b64 = base64.b64encode(raw).decode("ascii")
    return f"data:image/png;base64,{b64}"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description="Generate SVG assets for README (project dashboard + portal badge)."
    )
    ap.add_argument(
        "--catalog",
        default="data/projects.toml",
        help="Path to data/projects.toml",
    )
    ap.add_argument(
        "--out",
        default=".github/assets/cards",
        help="Output directory for SVG assets",
    )
    ap.add_argument(
        "--no-fetch",
        action="store_true",
        help="Do not call GitHub API; omit live repo stats.",
    )
    args = ap.parse_args(argv)

    repo_root = Path(__file__).resolve().parents[1]
    catalog_path = (repo_root / args.catalog).resolve()
    out_dir = (repo_root / args.out).resolve()

    categories = _load_catalog(catalog_path)
    icon_dir = repo_root / ".github" / "assets" / "icons"
    icon_data: dict[str, str] = {}
    for c in categories:
        if not c.icon:
            continue
        if c.icon in icon_data:
            continue
        data_uri = _load_png_data_uri(icon_dir / c.icon)
        if data_uri:
            icon_data[c.icon] = data_uri

    token = (
        os.environ.get("GITHUB_TOKEN")
        or os.environ.get("GH_TOKEN")
        or os.environ.get("GITHUB_API_TOKEN")
    )

    repos: list[str] = []
    for c in categories:
        for p in c.projects:
            if p.repo and not p.private:
                repos.append(p.repo)

    repo_stats: dict[str, RepoStats] = {}
    if not args.no_fetch:
        for i, repo in enumerate(repos):
            stats = _fetch_repo_stats(repo, token)
            if stats:
                repo_stats[repo] = stats

            # Be polite to unauthenticated rate limits.
            if not token:
                time.sleep(0.4)
            elif i and i % 10 == 0:
                time.sleep(0.1)

    total_stars = sum(s.stars for s in repo_stats.values())
    last_push_dt = max((s.pushed_at for s in repo_stats.values()), default=None)
    last_push = last_push_dt.strftime("%Y-%m-%d") if last_push_dt else "unknown"

    outputs: dict[str, str] = {}
    for variant in ("light", "dark"):
        outputs[f"typing-philosophy-{variant}.svg"] = _render_typing_philosophy_svg(
            variant=variant
        )
        outputs[f"portal-badge-{variant}.svg"] = _render_portal_badge_svg(
            variant=variant,
            total_stars=total_stars,
            last_push=last_push,
        )
        for layout in ("desktop", "mobile"):
            outputs[f"projects-{layout}-{variant}.svg"] = _render_project_dashboard_svg(
                categories=categories,
                repo_stats=repo_stats,
                icon_data=icon_data,
                variant=variant,
                layout=layout,
            )

    changed = False
    for name, content in outputs.items():
        changed |= _write_if_changed(out_dir / name, content)

    print(f"Assets: {out_dir} ({'changed' if changed else 'no changes'})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
