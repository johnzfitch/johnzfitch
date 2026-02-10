![Header](.github/assets/header.svg)
<p align="center">
  <a href="https://definitelynot.ai"><img src=".github/assets/buttons/definitelynot@2x.png" alt="definitelynot.ai" width="176" height="62"></a>&nbsp;
  <a href="https://internetuniverse.org"><img src=".github/assets/buttons/internetuniverse@2x.png" alt="Internet Universe" width="176" height="62"></a>&nbsp;
  <a href="https://math.berkeley.edu"><img src=".github/assets/buttons/berkeley-math@2x.png" alt="UC Berkeley Mathematics" width="176" height="62"></a>
  <a href="mailto:webmaster@internetuniverse.org"><img src=".github/assets/buttons/email@2x.png" alt="Email" width="176" height="62"></a>
</p>
<p align="center">
  <a href="https://johnzfitch.github.io/johnzfitch/">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset=".github/assets/cards/typing-philosophy-dark.svg">
    <img alt="Philosophy" src=".github/assets/cards/typing-philosophy-light.svg" width="100%">
  </picture></p>

---

## OpenAI Codex: Finding the Ghost in the Machine

**TL;DR**: Solved a pre-`main()` environment stripping bug causing 11-300x GPU slowdowns that eluded OpenAI's debugging team for months. This was the main blocker to Codex spawning effective subagents, and also explains why OpenAI wasn't able to use Codex in-house until February 2026. 

Proof: [Issue #8945](https://github.com/openai/codex/issues/8945) | [PR #8951](https://github.com/openai/codex/pull/8951) | [Release notes (rust-v0.80.0)](https://github.com/openai/codex/releases/tag/rust-v0.80.0)

<details>
<summary><b>Full Investigation Details</b></summary>

<br>

### The Ghost

In October 2025, OpenAI assembled a specialized debugging team to investigate mysterious slowdowns affecting **Codex**. After a week of intensive investigation: **nothing**.

The bug was literally a ghost - `pre_main_hardening()` executed before `main()`, stripped critical environment variables (`LD_LIBRARY_PATH`, `DYLD_LIBRARY_PATH`), and disappeared without a trace. Standard profilers saw nothing. Users saw variables in their shell, but inside `codex exec` they vanished.

---

### The Hunt

Within **3 days** of their announcement, I identified the problematic commit [PR #4521](https://github.com/openai/codex/pull/4521) and contacted @tibo_openai.

But identification is not proof. I spent **2 months** building an undeniable case.

#### Timeline

- **Sept 30, 2025** - PR #4521 merges, enabling `pre_main_hardening()` in release builds
- **Oct 1, 2025** - `rust-v0.43.0` ships (first affected release)
- **Oct 6, 2025** - First "painfully slow" regression reports
- **Oct 1-29, 2025** - Spike in env/PATH inheritance issues across platforms
- **Oct 29, 2025** - Emergency PATH fix lands (did not catch root cause)
- **Late Oct 2025** - OpenAI's specialized team investigates, declares there is no root cause, identifies issue as user behavior change
- **Jan 9, 2026** - My fix merged, credited in release notes

#### Evidence Collected

| Platform | Issues | Failure Mode |
|----------|--------|--------------|
| **macOS** | #6012, #5679, #5339, #6243, #6218 | `DYLD_*` stripping breaking dynamic linking |
| **Linux/WSL2** | #4843, #3891, #6200, #5837, #6263 | `LD_LIBRARY_PATH` stripping -> silent CUDA/MKL degradation |

**Compiled evidence packages:**

- Platform-specific failure modes and reproduction steps
- Quantifiable performance regressions (11-300x) with benchmarks
- Pattern analysis across 15+ scattered user reports over 3 months
- Process environment inheritance trace through fork/exec boundaries

- <img src=".github/assets/icons/script.png" width="24" height="24" alt=""> [Comprehensive Technical Analysis](https://github.com/user-attachments/files/24510983/GITHUB_ISSUE_DETAILED.md)
- <img src=".github/assets/icons/lightbulb.png" width="24" height="24" alt=""> [Investigation Methodology](https://docs.google.com/document/d/1fDJc1e0itJdh0MXMFJtkRiBcxGEFtye6Xc6Ui7eMX4o/edit)

---

### Why Conventional Debugging Failed

The bug was designed to be invisible:

- **Pre-main execution** - Used `#[ctor::ctor]` to run before `main()`, before any logging/instrumentation
- **Silent stripping** - No warnings, no errors, just missing environment variables
- **Distributed symptoms** - Appeared as unrelated issues across different platforms/configs
- **User attribution** - Everyone assumed they misconfigured something (shell looked fine)
- **Wrong search space** - Team was debugging post-main application code

Standard debugging tools cannot see pre-main execution. Profilers start at `main()`. Log hooks are not initialized yet. The code executes, modifies the environment, and vanishes.

---

### The Impact

OpenAI confirmed and merged the fix within 24 hours, explicitly crediting the investigation in v0.80.0 release notes:

> "Codex CLI subprocesses again inherit env vars like LD_LIBRARY_PATH/DYLD_LIBRARY_PATH to avoid runtime issues. As explained in #8945, failure to pass along these environment variables to subprocesses that expect them (notably GPU-related ones), was causing 10x+ performance regressions! Special thanks to @johnzfitch for the detailed investigation and write-up in #8945."

**Restored:**

- GPU acceleration for internal ML/AI dev teams
- CUDA/PyTorch functionality for ML researchers
- MKL/NumPy performance for scientific computing users
- Conda environment compatibility
- Enterprise database driver support

When the tools are blind, the system lies, and everyone else has stopped looking for it. This is the type of problem I love solving. 

</details>

---

## Selected Work

- **[Observatory](https://look.definitelynot.ai)** - WebGPU deepfake detection running 4 ML models in browser (live demo)
- **[specHO](https://github.com/johnzfitch/specHO)** - LLM watermark detection via phonetic/semantic analysis (The Echo Rule)
- **[filearchy](https://github.com/johnzfitch/filearchy)** - COSMIC Files fork with sub-10ms trigram search (Rust)
- **[nautilus-plus](https://github.com/johnzfitch/nautilus-plus)** - Enhanced GNOME Files with sub-ms search (AUR)
- **[indepacer](https://github.com/johnzfitch/indepacer)** - PACER CLI for federal court research (PyPI: pacersdk)

Self-hosting bare metal infrastructure (NixOS) with post-quantum cryptography, authoritative DNS, and containerized services.

---

## Featured

### <img src=".github/assets/icons/observatory-eye.png" width="24" height="24" alt=""> Observatory - WebGPU Deepfake Detection

**Live Demo:** [look.definitelynot.ai](https://look.definitelynot.ai)

Browser-based AI image detection running 4 specialized ML models (ViT, Swin Transformer) through WebGPU. Zero server-side processing; all inference happens client-side with 672MB of ONNX models.

| Model | Accuracy | Architecture |
|-------|----------|--------------|
| dima806_ai_real | 98.2% | Vision Transformer |
| SMOGY | 98.2% | Swin Transformer |
| Deep-Fake-Detector-v2 | 92.1% | ViT-Base |
| umm_maybe | 94.2% | Vision Transformer |

**Stack:** JavaScript (ES6), Transformers.js, ONNX, WebGPU/WASM

---

### <img src=".github/assets/icons/folder.png" width="24" height="24" alt=""> iconics - Semantic Icon Library

3,372+ PNG icons with semantic CLI discovery. Find the right icon by meaning, not filename.

```bash
icon suggest security       # -> lock, shield, key, firewall...
icon suggest data           # -> chart, database, folder...
icon use lock shield        # Export to ./icons/
```

**Features:** Fuzzy search, theme variants, batch export, markdown integration
**Stack:** Python, FuzzyWuzzy, PIL

---

### <img src=".github/assets/icons/script.png" width="24" height="24" alt=""> filearchy + triglyph - Sub-10ms File Search

COSMIC Files fork with embedded trigram search engine. Memory-mapped indices achieve sub-millisecond searches across 2.15M+ files with near-zero resident memory.

```text
filearchy/
|-- triglyph/      # Trigram library (mmap)
`-- triglyphd/     # D-Bus daemon for system-wide search
```

**Performance:** 2.15M files indexed, sub-10ms query time, 156MB index on disk
**Stack:** Rust, libcosmic, memmap2, zbus

---

### <img src=".github/assets/icons/radar.png" width="24" height="24" alt=""> The Echo Rule - LLM Detection Methodology

LLMs echo their training data. That echo is detectable through pattern recognition:

| Signature | Detection Method |
|-----------|------------------|
| **Phonetic** | CMU phoneme analysis, Levenshtein distance |
| **Structural** | POS tag patterns, sentence construction |
| **Semantic** | Word2Vec cosine similarity, hedging clusters |

Implemented in [specHO](https://github.com/johnzfitch/specHO) with 98.6% preprocessor test pass rate. Live demo at [definitelynot.ai](https://definitelynot.ai).

---

## <img src=".github/assets/icons/chart.png" width="24" height="24" alt=""> Skills

<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/assets/charts/skills-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset=".github/assets/charts/skills-light.svg">
  <img alt="Technical focus - skills breakdown" src=".github/assets/charts/skills-light.svg">
</picture>

**Core:** Rust | Python | TypeScript | C | Nix | Shell

---

## <img src=".github/assets/icons/folder.png" width="24" height="24" alt=""> Project Dashboard

<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 600px)" srcset=".github/assets/cards/projects-mobile-dark.svg">
  <source media="(prefers-color-scheme: light) and (max-width: 600px)" srcset=".github/assets/cards/projects-mobile-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset=".github/assets/cards/projects-desktop-dark.svg">
  <img alt="Projects grouped by category" src=".github/assets/cards/projects-desktop-light.svg">
</picture>

<details>
<summary><b>Text project index (copyable)</b></summary>

### AI / ML
- [observatory](https://github.com/johnzfitch/observatory) - WebGPU deepfake detection (live: https://look.definitelynot.ai)
- [specHO](https://github.com/johnzfitch/specHO) - LLM watermark detection (Echo Rule)
- [definitelynot.ai](https://github.com/johnzfitch/definitelynot.ai) - Unicode security defenses
- [marginium](https://github.com/johnzfitch/marginium) - Multimodal generation tooling
- [gemini-cli](https://github.com/johnzfitch/gemini-cli) - Privacy-enhanced Gemini CLI fork

### Security Research
- eero (private) - Mesh WiFi router security analysis
- blizzarchy (private) - OAuth analysis and telemetry RE
- [featherarchy](https://github.com/johnzfitch/featherarchy) - Security-hardened Monero wallet fork
- alienware-monitor (private) - Firmware RE
- proxyforge (private) - Transparent MITM proxy

### Systems Programming
- [filearchy](https://github.com/johnzfitch/filearchy) - COSMIC Files fork with trigram search
- [triglyph](https://github.com/johnzfitch/triglyph) - Trigram index library
- [triglyphd](https://github.com/johnzfitch/triglyphd) - D-Bus search daemon
- [nautilus-plus](https://github.com/johnzfitch/nautilus-plus) - Enhanced GNOME Files
- [search-cache](https://github.com/johnzfitch/search-cache) - Sub-ms search cache/index
- [cod3x](https://github.com/johnzfitch/cod3x) - Terminal coding agent
- bitmail (private) - Bitmessage client

### CLI Tools
- [indepacer](https://github.com/johnzfitch/indepacer) - PACER CLI
- [iconics](https://github.com/johnzfitch/iconics) - Semantic icon library
- [gemini-sharp](https://github.com/johnzfitch/gemini-sharp) - Single-file Gemini CLI binaries

### Desktop / Linux
- [omarchy](https://github.com/johnzfitch/omarchy) - Omarchy fork
- [waybar-config](https://github.com/johnzfitch/waybar-config) - Waybar RSS ticker
- [claude-desktop-arch](https://github.com/johnzfitch/claude-desktop-arch) - Claude patch for Arch
- [qualcomm-x870e-linux-bug-patch](https://github.com/johnzfitch/qualcomm-x870e-linux-bug-patch) - WiFi 7 firmware fix
- [arch-dependency-matrices](https://github.com/johnzfitch/arch-dependency-matrices) - Graph theory analysis

### Web / Mobile
- [NetworkBatcher](https://github.com/johnzfitch/NetworkBatcher) - Network batching for iOS
- [Liberty-Links](https://github.com/johnzfitch/Liberty-Links) - Privacy-respecting link alternatives

### Infrastructure
- NixOS Server (private) - Post-quantum SSH, Rosenpass VPN, authoritative DNS
- unbound-config (private) - Recursive DNS with DNSSEC and ad blocking

</details>

---

## <img src=".github/assets/icons/server.png" width="24" height="24" alt=""> Infrastructure

**Primary server:** Dedicated bare-metal NixOS host (details available on request)

- Security: Post-quantum SSH, Rosenpass VPN, nftables firewall
- DNS: Unbound resolver with DNSSEC, ad/tracker blocking
- Services: FreshRSS, Caddy (HTTPS/HTTP3), cPanel/WHM, Podman containers
- Network: Local 10Gbps, authoritative BIND9 with RFC2136 ACME

<details>
<summary><b>Infrastructure matrix</b></summary>

| Service | Technology |
|---------|------------|
| **Security** | Post-quantum SSH, Rosenpass VPN, nftables firewall |
| **DNS** | Unbound resolver with DNSSEC, ad/tracker blocking |
| **Services** | FreshRSS, Caddy (HTTPS/HTTP3), cPanel/WHM, Podman containers |
| **Network** | Local 10Gbps, authoritative BIND9 with RFC2136 ACME |

</details>

---

<p align="center">
  <sub>SF Bay Area | Open to remote | Icons from <a href="https://github.com/johnzfitch/iconics">iconics</a></sub>
</p>
