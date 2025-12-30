# John Zachary Fitch
**Full-Stack Engineer** | **Security Researcher** | **UC Berkeley Mathematics**

<img src=".github/assets/icons/linkedin.png" width="20" height="20"> [LinkedIn](https://www.linkedin.com/in/john-fitch-600726193/) | <img src=".github/assets/icons/globe.png" width="20" height="20"> [DefinitelyNot.ai](https://definitelynot.ai) | <img src=".github/assets/icons/mail.png" width="20" height="20"> webmaster@internetuniverse.org

---

Software engineer with UC Berkeley mathematics background specializing in systems programming, security research, and AI/ML applications. I build production tools across the full stack—from WebGPU-accelerated browser applications to Rust CLI tools to bare-metal NixOS infrastructure.

**What I ship:**
- **[Observatory](https://look.definitelynot.ai)** - WebGPU deepfake detection running 4 ML models in-browser *(live demo)*
- **[specHO](https://github.com/johnzfitch/specHO)** - LLM watermark detection via phonetic/semantic analysis *(The Echo Rule)*
- **[filearchy](https://github.com/johnzfitch/filearchy)** - COSMIC Files fork with sub-10ms trigram search *(Rust)*
- **[nautilus-plus](https://github.com/johnzfitch/nautilus-plus)** - Enhanced GNOME Files with sub-millisecond search *(AUR)*
- **[indepacer](https://github.com/johnzfitch/indepacer)** - PACER CLI for federal court research *(PyPI: pacersdk)*

Self-hosting 32GB bare-metal infrastructure (NixOS) with post-quantum cryptography (ML-KEM, Rosenpass VPN), authoritative DNS, and containerized services.

**Philosophy:** AI as augmentation, not replacement. Privacy by default. Ship tools that make people better at their jobs.

---

## <img src=".github/assets/icons/star.png" width="24" height="24"> Featured

### <img src=".github/assets/icons/observatory-eye.png" width="20" height="20"> Observatory - WebGPU Deepfake Detection
**Live Demo:** [look.definitelynot.ai](https://look.definitelynot.ai)

Browser-based AI image detection running 4 specialized ML models (ViT, Swin Transformer) through WebGPU. Zero server-side processing—all inference happens client-side with 672MB of ONNX models.

| Model | Accuracy | Architecture |
|-------|----------|--------------|
| dima806_ai_real | 98.2% | Vision Transformer |
| SMOGY | 98.2% | Swin Transformer |
| Deep-Fake-Detector-v2 | 92.1% | ViT-Base |
| umm_maybe | 94.2% | Vision Transformer |

**Stack:** JavaScript (ES6), Transformers.js, ONNX, WebGPU/WASM
**Design:** 2006 "Purist" UI aesthetic - no frameworks, pure web standards

---

### <img src=".github/assets/icons/console.png" width="20" height="20"> indepacer - Federal Court Records CLI
PACER automation for legal research with MFA support, local caching, and intelligent document linking.

```bash
pacer pcl cases -t "Apple v. Samsung"         # Search cases nationwide
pacer download docket 1:18-cv-08434 nysd      # Download full docket
pacer grep "motion to dismiss"                # Search local archive
```

Features context system for workflow efficiency, cost confirmation prompts (PACER charges per page), and batch operations. Separate `pacersdk` SDK published to PyPI.

**Stack:** Python, Click, Rich terminal UI, TOTP authentication

---

### <img src=".github/assets/icons/shield.png" width="20" height="20"> aegis - Intelligent Browser Security
Browser automation with risk-based safety controls, human behavior simulation for anti-bot detection, and container isolation for privacy.

**Danger Slider:** 5-level control from PARANOID (approve every action) to AUTOPILOT (time-limited auto-approve). Cursor movements use Bezier curves and Fitts's Law for realistic timing.

**Stack:** TypeScript, Playwright, Firefox/Floorp integration, WebSocket MCP

---

### <img src=".github/assets/icons/radar.png" width="20" height="20"> The Echo Rule - LLM Detection Methodology
LLMs echo their training data. That echo is detectable through pattern recognition:

| Signature | Detection Method |
|-----------|------------------|
| **Phonetic** | CMU phoneme analysis, Levenshtein distance |
| **Structural** | POS tag patterns, sentence construction |
| **Semantic** | Word2Vec cosine similarity, hedging clusters |

Implemented in [specHO](https://github.com/johnzfitch/specHO) with 98.6% preprocessor test pass rate. Live demo at [definitelynot.ai](https://definitelynot.ai).

---

## <img src=".github/assets/icons/chart.png" width="24" height="24"> Skills

<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/assets/charts/skills-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset=".github/assets/charts/skills-light.svg">
  <img alt="Technical Focus - Skills breakdown" src=".github/assets/charts/skills-light.svg">
</picture>

**Core:** Rust · Python · TypeScript · C · Nix · Shell

---

## <img src=".github/assets/icons/folder.png" width="24" height="24"> Projects

### <img src=".github/assets/icons/ai-brain.png" width="24" height="24"> AI/ML

| Project | Description | Stack |
|---------|-------------|-------|
| [**observatory**](https://github.com/johnzfitch/observatory) | WebGPU deepfake detection, 4 ML models client-side · [live](https://look.definitelynot.ai) | JS, Transformers.js, ONNX |
| [**specHO**](https://github.com/johnzfitch/specHO) | LLM watermark detection via Echo Rule (phonetic/semantic) | Python, spaCy, Gensim |
| [**definitelynot.ai**](https://github.com/johnzfitch/definitelynot.ai) | Unicode security: Trojan Source, homoglyph, BiDi defense | PHP, JavaScript, ICU |
| [**marginium**](https://github.com/johnzfitch/marginium) | Multimodal generation with LLM visual output awareness | Python |
| [**gemini-cli**](https://github.com/johnzfitch/gemini-cli) | Privacy-enhanced Gemini CLI fork, telemetry disabled | TypeScript, Node.js |

### <img src=".github/assets/icons/lock.png" width="24" height="24"> Security Research

| Project | Description | Stack |
|---------|-------------|-------|
| **aegis** *(private)* | Browser automation, anti-bot detection (Bezier/Fitts's Law) | TypeScript, Playwright |
| **eero** *(private)* | Mesh WiFi router security analysis, HackerOne prep | Python, Wireshark |
| **blizzarchy** *(private)* | Battle.net OAuth analysis, telemetry RE | Rust, Python, Ghidra |
| [**featherarchy**](https://github.com/johnzfitch/featherarchy) | Security-hardened Monero wallet fork | C++, Qt6 |
| **alienware-monitor** *(private)* | Dell monitor firmware RE, GSFW decoder | Python, Ghidra |
| **proxyforge** *(private)* | Transparent MITM proxy, TLS interception | Python, mitmproxy |

### <img src=".github/assets/icons/script.png" width="24" height="24"> Systems Programming

| Project | Description | Stack |
|---------|-------------|-------|
| [**filearchy**](https://github.com/johnzfitch/filearchy) | COSMIC Files fork with embedded trigram search engine | Rust, libcosmic |
| ↳ [triglyph](https://github.com/johnzfitch/triglyph) | Zero-RSS trigram index library (mmap, ~0 bytes resident) | Rust, memmap2 |
| ↳ [triglyphd](https://github.com/johnzfitch/triglyphd) | D-Bus daemon for system-wide search | Rust, zbus |
| [**nautilus-plus**](https://github.com/johnzfitch/nautilus-plus) | Enhanced GNOME Files with 512px thumbnails, search-cache | C, GTK4 |
| ↳ [search-cache](https://github.com/johnzfitch/search-cache) | HashMap-based file indexing, sub-ms search for 2.15M+ files | Rust, DashMap |
| [**cod3x**](https://github.com/johnzfitch/cod3x) | Terminal coding agent with 3D ASCII interface at 60fps | Rust, SQLite |
| **bitmail** *(private)* | Modern Bitmessage client with Python CLI and Rust TUI | Python, Rust |

### <img src=".github/assets/icons/console.png" width="24" height="24"> CLI Tools

| Project | Description | Stack |
|---------|-------------|-------|
| [**indepacer**](https://github.com/johnzfitch/indepacer) | PACER CLI for federal court research, MFA, cost protection | Python, Click, Rich |
| [**iconics**](https://github.com/johnzfitch/iconics) | Semantic icon library (3,372 PNGs), CLI discovery/export | Python |
| [**gemini-sharp**](https://github.com/johnzfitch/gemini-sharp) | Single-file Gemini CLI binaries, 15+ color themes | C#, .NET |

### <img src=".github/assets/icons/cinema-display.png" width="24" height="24"> Desktop/Linux

| Project | Description | Stack |
|---------|-------------|-------|
| [**omarchy**](https://github.com/johnzfitch/omarchy) | DHH's omarchy fork: waybar RSS, NVIDIA config, compact UI | Hyprland, Shell |
| [**waybar-config**](https://github.com/johnzfitch/waybar-config) | RSS ticker for self-hosted FreshRSS, hover-pause | JSON, CSS, Shell |
| [**claude-desktop-arch**](https://github.com/johnzfitch/claude-desktop-arch) | Claude Code preview patch for Arch Linux | JavaScript, Shell |
| [**qualcomm-x870e-linux-bug-patch**](https://github.com/johnzfitch/qualcomm-x870e-linux-bug-patch) | WiFi 7 firmware fix for WCN7850 on X870E | Python, ACPI |
| [**arch-dependency-matrices**](https://github.com/johnzfitch/arch-dependency-matrices) | Graph theory analysis of 1,553 Arch packages | Python, NumPy |

### <img src=".github/assets/icons/smartphone.png" width="24" height="24"> Web/Mobile

| Project | Description | Stack |
|---------|-------------|-------|
| [**NetworkBatcher**](https://github.com/johnzfitch/NetworkBatcher) | Energy-efficient network batching for iOS 26+ | Swift |
| [**Liberty-Links**](https://github.com/johnzfitch/Liberty-Links) | Tracker-free, privacy-respecting link alternatives | Markdown |

---

## <img src=".github/assets/icons/server.png" width="24" height="24"> Infrastructure

**Primary Server:** Intel Xeon E3-1270v5 | 32GB RAM | 3.6TB SSD (btrfs) | NixOS 24.05

| Service | Technology |
|---------|------------|
| **Security** | Post-quantum SSH (sntrup761x25519), Rosenpass VPN (ML-KEM + Kyber-512), nftables firewall |
| **DNS** | Unbound recursive resolver with DNSSEC, ad/tracker blocking, no third-party DNS |
| **Services** | FreshRSS, Caddy (HTTPS/HTTP3), cPanel/WHM, Podman containers |
| **Network** | Local 10Gbps, authoritative BIND9 with RFC2136 ACME |

**Infrastructure as Code:**

| Project | Description | Stack |
|---------|-------------|-------|
| **NixOS Server** *(private)* | Bare-metal config: post-quantum SSH, Rosenpass VPN, BIND9 | Nix, agenix |
| **unbound-config** *(private)* | Recursive DNS with DNSSEC, ad/tracker blocking | Unbound, Shell |

---

## <img src=".github/assets/icons/compass.png" width="24" height="24"> Philosophy

AI should expand human capability, not replace workers. I call it **additive innovation**: build tools that make people better at their jobs, not tools that eliminate their jobs.

The best way to predict AI's impact is to build the tools that shape it.

---

<p align="center">
<sub>SF Bay Area · Open to remote · Icons from <a href="https://github.com/johnzfitch/iconics">iconics</a></sub>
</p>
