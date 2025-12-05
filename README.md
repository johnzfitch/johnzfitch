# John Zachary Fitch
**AI Product Engineer** | **UC Berkeley Mathematics**

---

I'm a software engineer with a background in mathematics from UC Berkeley. I'm focused on AI product engineering and maintaining a privacy-first infrastructure. I love working on enhancing existing projects and pushing the boundaries on what models can do locally. My work is typically centered around building tools that might expand human capability rather than those that could replace it. 

I maintain a [custom fork of omarchy](https://github.com/johnzfitch/omarchy) with 2,600+ lines of modifications tailored to my workflow. My [nautilus-plus](https://github.com/johnzfitch/nautilus-plus) (AUR: `nautilus-plus`) integrates with [search-cache](https://github.com/johnzfitch/search-cache), a Rust-based file search tool, delivering sub-millisecond search and user-configurable performance optimizations for GTK4 file management. I'm developing **The Echo Rule**—a methodology for detecting LLM-generated text through phonetic, structural, and semantic pattern recognition, implemented in [specHO](https://github.com/johnzfitch/specHO) and [definitelynot.ai](https://definitelynot.ai).

Maintain NixOS bare-metal infrastructure with post-quantum cryptography (ML-KEM SSH key exchange, WireGuard/Rosenpass hybrid VPN with Classic McEliece + Kyber-512), self-hosted authoritative DNS (BIND9 with RFC2136 ACME), containerized services via Podman, and declarative secrets management (agenix). Local 10Gbps network runs Unbound recursive DNS with DNSSEC validation.

**Philosophy:** Local-first computing. Privacy by default. AI as augmentation, not replacement.

---

## <img src=".github/assets/icons/radar.png" width="24" height="24"> The Echo Rule

LLMs echo their training data. That echo is detectable through pattern recognition:

| Signature | Detection Method |
|-----------|------------------|
| **Phonetic** | CMU phoneme analysis, Levenshtein distance on pronunciation |
| **Structural** | POS tag patterns, sentence construction habits |
| **Semantic** | Word2Vec cosine similarity, hedging language clusters |

---

## <img src=".github/assets/icons/chart.png" width="24" height="24"> Skills

<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/assets/charts/skills-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset=".github/assets/charts/skills-light.svg">
  <img alt="Technical Focus - Skills breakdown" src=".github/assets/charts/skills-light.svg">
</picture>

---

## <img src=".github/assets/icons/science.png" width="24" height="24"> Projects

### <img src=".github/assets/icons/security.png" width="24" height="24"> AI/ML

| Project | Description | Stack |
|---------|-------------|-------|
| [**specHO**](https://github.com/johnzfitch/specHO) | LLM watermark detection implementing the Echo Rule through phonetic, structural, and semantic analysis. Five-component pipeline. | Python, spaCy, Gensim |
| [**definitelynot.ai**](https://github.com/johnzfitch/definitelynot.ai) | Unicode security sanitizer defending against Trojan Source attacks, homoglyph spoofing, and BiDi exploits via 16-step pipeline. | PHP, JavaScript, ICU |
| [**marginium**](https://github.com/johnzfitch/marginium) | Multimodal generation framework providing LLMs with visual awareness of their output structure. | Python |
| [**gemini-cli**](https://github.com/johnzfitch/gemini-cli) | Privacy-enhanced fork of Google's Gemini CLI with telemetry disabled and custom Gogh color schemes. | TypeScript, Node.js |
| **aegis** *(private)* | Browser MCP server enabling Claude Code to interface with Floorp browser for web automation and research. | TypeScript, Playwright |

### <img src=".github/assets/icons/ram.png" width="24" height="24"> Systems

| Project | Description | Stack |
|---------|-------------|-------|
| [**search-cache**](https://github.com/johnzfitch/search-cache) | Fast file search tool using HashMap-based indexing with DashMap for concurrency and Rayon for parallel execution. Sub-millisecond search for 2.15M+ files. Available on AUR. | Rust |
| [**nautilus-plus**](https://github.com/johnzfitch/nautilus-plus) | Enhanced GNOME Files with user-configurable search blacklist, depth-limited search, and 512px thumbnails. Integrates with search-cache. Available on AUR as `nautilus-plus`. | C, GTK4 |
| [**cod3x**](https://github.com/johnzfitch/cod3x) | Terminal coding agent with 3D ASCII interface at 60fps and SQLite session persistence. | Rust, SQLite |
| **bitmail** *(private)* | Modern Bitmessage client with Python CLI and Rust TUI for decentralized encrypted messaging. | Python, Rust |

### <img src=".github/assets/icons/homelab.png" width="24" height="24"> Desktop

| Project | Description | Stack |
|---------|-------------|-------|
| [**omarchy**](https://github.com/johnzfitch/omarchy) | Custom fork of DHH's omarchy with 2,628+ lines of customization: waybar RSS ticker, NVIDIA config, ultra-compact Nautilus UI. | Hyprland, Shell |
| [**waybar-config**](https://github.com/johnzfitch/waybar-config) | RSS feed ticker connecting to self-hosted FreshRSS with hover-pause and smart click routing. | JSON, CSS, Shell |
| [**iconics**](https://github.com/johnzfitch/iconics) | Semantic icon library with 3,372 cataloged PNG icons and CLI tool for discovery and export. | Python |
| [**claude-desktop-arch**](https://github.com/johnzfitch/claude-desktop-arch) | Enable Claude Code preview in Claude Desktop on Arch Linux via 3-line platform detection patch. | JavaScript, Shell |
| [**gemini-sharp**](https://github.com/johnzfitch/gemini-sharp) | Single-file standalone Gemini CLI binaries with privacy enhancements and 15+ Gogh color themes. | C#, .NET |

### <img src=".github/assets/icons/automation.png" width="24" height="24"> Other

| Project | Description | Stack |
|---------|-------------|-------|
| [**qualcomm-x870e-linux-bug-patch**](https://github.com/johnzfitch/qualcomm-x870e-linux-bug-patch) | ACPI kernel fix for Qualcomm WCN7850 WiFi 7 on AMD X870E motherboards. | ACPI, Shell |
| [**arch-dependency-matrices**](https://github.com/johnzfitch/arch-dependency-matrices) | Mathematical analysis of 1,553 Arch Linux packages using graph theory, PageRank, and spectral analysis. | Python, NumPy |
| [**stranger-things-finale-theater-list**](https://github.com/johnzfitch/stranger-things-finale-theater-list) | Complete list of 490 theaters showing Stranger Things 5: The Finale (Dec 31, 2025 & Jan 1, 2026). | Markdown |
| [**wealth-for-me-not-for-thee**](https://github.com/johnzfitch/wealth-for-me-not-for-thee) | Wealth inequality visualizer game - scroll to comprehend the scale of billionaire wealth vs median income. | JavaScript, CSS |
| [**NetworkBatcher**](https://github.com/johnzfitch/NetworkBatcher) | Energy-efficient network request batching for iOS 26+ with intelligent coalescing and battery optimization. | Swift |
| [**Liberty-Links**](https://github.com/johnzfitch/Liberty-Links) | Curated collection of tracker-free, redirect-free links - privacy-respecting alternatives to common services. | Markdown |

### <img src=".github/assets/icons/lock.png" width="24" height="24"> Security Research

| Project | Description | Stack |
|---------|-------------|-------|
| **eero-reverse-engineering** *(private)* | Mesh WiFi router security analysis including API research, traffic capture tools, and protocol documentation. | Python, Wireshark |
| **proxyforge** *(private)* | Transparent MITM proxy for API traffic analysis with TLS interception and HAR export. | Python, mitmproxy |

---

## <img src=".github/assets/icons/server.png" width="24" height="24"> Infrastructure

### Primary Server (Tier.net - Dallas, TX)

| Component | Specification |
|-----------|---------------|
| CPU | Intel Xeon E3-1270v5 |
| Memory | 32GB RAM |
| Storage | 2x 1.8TB SSD (3.6TB total, btrfs) |
| OS | NixOS 24.05 |
| Security | Post-quantum SSH (sntrup761x25519), nftables |

### <img src=".github/assets/icons/wireless.png" width="24" height="24"> DNS

- **Unbound** recursive resolver - no third-party DNS
- DNSSEC validation, QNAME minimization
- Ad/tracker blocking (Steven Black, OISD, Hagezi Pro)

### <img src=".github/assets/icons/rss.png" width="24" height="24"> Self-Hosted

- **FreshRSS** at feed.internetuniverse.org (desktop integration)
- **Caddy** with automatic HTTPS/HTTP3
- **cPanel/WHM** for InternetUniverse.org and DefinitelyNot.ai

### <img src=".github/assets/icons/storage.png" width="24" height="24"> Infrastructure as Code

| Project | Description | Stack |
|---------|-------------|-------|
| *(redacted)* | NixOS bare-metal server config with post-quantum SSH (ML-KEM), Rosenpass VPN, and battle-hardened nftables. | Nix, agenix |
| **unbound-config** *(private)* | Recursive DNS resolver configuration with DNSSEC, QNAME minimization, and curated ad/tracker blocklists. | Unbound, Shell |

---

## <img src=".github/assets/icons/djinni.png" width="24" height="24"> Philosophy

AI should expand human capability, not replace workers. I call it **additive innovation**: build tools that make people better at their jobs, not tools that eliminate their jobs.

The best way to predict AI's impact is to build the tools that shape it.

---

## <img src=".github/assets/icons/mail.png" width="24" height="24"> Contact

**Location:** SF Bay Area or remote

**Email:** webmaster@internetuniverse.org

---

<sub>Icons curated by Master Orchestrator Agent from the [iconics](https://github.com/johnzfitch/iconics) library (3,372+ semantic icons). Multi-agent fact-checking ensured accuracy.</sub>
