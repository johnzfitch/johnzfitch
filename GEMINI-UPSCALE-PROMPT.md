# Gemini CLI Icon Upscaling Prompt for Nano Banana MCP

## Usage

```bash
gemini-cli --mcp nano-banana < GEMINI-UPSCALE-PROMPT.md
```

---

## Prompt

You are an AI image enhancement specialist. I need you to upscale and enhance the following 25 icons for crisp 16x16 pixel display on GitHub READMEs.

**Global Requirements:**
- Output: 16x16 PNG with transparency preserved
- Style: Maintain original artistic intent while maximizing clarity at small size
- Edges: Apply intelligent edge sharpening without artifacts
- Colors: Preserve or enhance color depth for small display
- Anti-aliasing: Apply subtle anti-aliasing for smooth edges

---

## Icon-Specific Enhancement Instructions

### Fantasy Archon Pack (High Detail - Need Careful Downscaling)

| Icon | Enhancement Notes |
|------|-------------------|
| `archon-archon-pack-phoenix-emoji-character-fantasy.png` | **HEADER ICON** - Most important. Preserve fiery colors (orange/red gradient). Emphasize wing silhouette. Needs to be instantly recognizable as phoenix at 16x16. |
| `archon-archon-pack-sorceress-emoji-character-fantasy.png` | Preserve staff detail and flowing robes. Purple/mystical color scheme. For "Bio/About" section. |
| `archon-archon-pack-djinni-emoji-character-fantasy.png` | Blue/smoke aesthetic. Preserve ethereal quality. For "Philosophy" section. |
| `archon-archon-pack-basilisk-emoji-character-fantasy.png` | Green serpentine creature. Emphasize eyes/head shape. For "Security" section. |
| `archon-archon-pack-golem-emoji-character-fantasy.png` | Earth tones, stone texture. Blocky silhouette. For "Automation" section. |
| `archon-archon-pack-manticore-emoji-character-fantasy.png` | Hybrid creature - lion/scorpion. Preserve distinctive features. For "Complex Systems" section. |

### Technical/Scientific Icons

| Icon | Enhancement Notes |
|------|-------------------|
| `chart-data-analytics.png` | Clean lines for chart bars/axes. High contrast colors. For "Skills Distribution" section. |
| `Network radar.png` | Circular radar sweep pattern. Green on dark or vice versa. For "AI Detection / Echo Rule" section. |
| `icatch21-science1-ui-set-icon.png` | Atom or molecular structure. Clean geometric shapes. For "Systems Programming" section. |
| `icatch21-science2-ui-set-icon.png` | Laboratory flask/beaker. Preserve liquid color gradient. For "Research" section. |
| `gort-hardware-ram-device-tool.png` | Retro RAM stick. Emphasize chip pattern. For "Memory/Performance" section. |
| `System monitoring.png` | Dashboard/gauges aesthetic. Multiple indicators visible. For "Monitoring" section. |

### Infrastructure Icons

| Icon | Enhancement Notes |
|------|-------------------|
| `monitor_24x24.png` | **DOWNSAMPLE from 24x24** - Clean monitor silhouette. Screen should be visible. For "Linux Desktop" section. |
| `puzzle-system-fileserver-files-folder.png` | Server tower shape. Retro puzzle aesthetic. For "Infrastructure" section. |
| `Hard disk.png` | Classic HDD shape. Metallic sheen if possible. For "Storage" section. |
| `wireless.png` | Signal wave arcs. Clear broadcast pattern. For "DNS/Networking" section. |
| `Brick house.png` | House silhouette with brick texture hint. Warm colors. For "Home Lab" section. |

### Communication & UI Icons

| Icon | Enhancement Notes |
|------|-------------------|
| `internet-news-network-web-button.png` | News/RSS aesthetic. Globe or paper icon. For "RSS/Feeds" section. |
| `icatch21-magic1-ui-set-icon.png` | Magic wand with sparkles. For "Philosophy/Creative" section. |
| `icatch21-letter1-ui-set-icon.png` | Envelope shape. Classic mail icon. For "Contact" section. |
| `handshake_24x24.png` | **DOWNSAMPLE from 24x24** - Two hands meeting. Professional collaboration. For "Looking For" section. |
| `scroll_list_24x24.png` | **DOWNSAMPLE from 24x24** - Ancient scroll with text lines. For "Documentation" section. |

### Performance & Nature Icons

| Icon | Enhancement Notes |
|------|-------------------|
| `icatch21-fire1-ui-set-icon.png` | Flame shape. Orange/red gradient. For "Performance/Speed" section. |
| `tree.png` | Tree silhouette. Green canopy, brown trunk. For "Open Source" section. |
| `icatch21-plug1-ui-set-icon.png` | Electrical plug. Two-prong shape visible. For "Integration/APIs" section. |

---

## Output Format

For each icon, output:
- Filename: `[original-name]-enhanced-16x16.png`
- Format: PNG with alpha channel
- Dimensions: Exactly 16x16 pixels
- Color depth: 32-bit RGBA

---

## Priority Order

Process in this order (most important first):
1. `archon-archon-pack-phoenix-emoji-character-fantasy.png` (HEADER - critical)
2. `chart-data-analytics.png` (Skills section)
3. `Network radar.png` (Echo Rule section)
4. Fantasy pack remaining (sorceress, djinni, basilisk, golem, manticore)
5. Infrastructure icons
6. Communication icons
7. Performance/nature icons

---

## Quality Verification

After enhancement, each icon should:
- [ ] Be recognizable at 16x16 without squinting
- [ ] Have no muddy or blurred edges
- [ ] Maintain transparency where original had it
- [ ] Preserve the semantic meaning of the original
- [ ] Look professional on both light and dark GitHub themes

---

**Total Icons: 25**
**Output Directory: /home/zack/dev/johnzfitch/icons/enhanced/**
