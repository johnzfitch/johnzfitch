<figure>
  <img src=".github/assets/header.svg" alt="Header">
</figure>
<p align="center">
  <a href="https://definitelynot.ai"><img src=".github/assets/buttons/definitelynot@2x.png" alt="definitelynot.ai" width="176" height="62"></a>&nbsp;
  <a href="https://internetuniverse.org"><img src=".github/assets/buttons/internetuniverse@2x.png" alt="Internet Universe" width="176" height="62"></a>&nbsp;
  <a href="https://math.berkeley.edu"><img src=".github/assets/buttons/berkeley-math@2x.png" alt="UC Berkeley Mathematics" width="176" height="62"></a>&nbsp;
  <a href="mailto:webmaster@internetuniverse.org"><img src=".github/assets/buttons/email@2x.png" alt="Email" width="176" height="62"></a>
</p>
<p align="center">
  <sub>SF Bay Area &ensp;&bull;&ensp; <a href="https://johnzfitch.github.io/johnzfitch">Git Page</a> &ensp;&bull;&ensp; All icons from <a href="https://github.com/johnzfitch/iconics">iconics</a></sub>
</p>

<!-- Link Reference Definitions (Layer 1: invisible metadata) -->

-----

## OpenAI Codex: Finding the Ghost in the Machine

> [!IMPORTANT]
> Solved a <ruby>pre-`main()`<rp>(</rp><rt>⁠#[ctor::ctor]</rt><rp>)</rp></ruby> environment stripping bug causing <mark>11–300× <abbr title="Graphics Processing Unit">GPU</abbr> slowdowns</mark> that eluded OpenAI's debugging team for months. This was the main blocker to Codex spawning and controlling effective subagents. The regression often times caused delayed cpu fallback or silent failures in ML-related tasks across all operating systems.

Proof: [Issue #8945](https://github.com/openai/codex/issues/8945)  |  [PR #8951](https://github.com/openai/codex/pull/8951)  |  [Release notes (<samp>rust-v0.80.0</samp>)](https://github.com/openai/codex/releases/tag/rust-v0.80.0)

<details>
<summary><b>Full Investigation Details</b></summary>

<br>

### The Ghost

In <time datetime="2025-10">October 2025</time>, OpenAI assembled a specialized debugging team to investigate mysterious slowdowns affecting <b>Codex</b>. After a week of intensive investigation: <b>nothing</b>.

The bug was literally a ghost — `pre_main_hardening()` executed before `main()`, stripped critical environment variables (<var>LD_LIBRARY_PATH</var>, <var>DYLD_LIBRARY_PATH</var>), and disappeared without a trace. Standard profilers saw nothing. Users saw variables in their shell, but inside <samp>codex exec</samp> they vanished.

-----

### The Hunt

Within <b>3 days</b> of their announcement, I identified the problematic commit [PR #4521](https://github.com/openai/codex/pull/4521) and contacted <kbd>@tibo_openai</kbd>.

But identification is not proof. I spent <b>2 months</b> building an undeniable case.

#### Timeline

<table>
  <thead>
    <tr>
      <th width="180">Date</th>
      <th>Event</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><time datetime="2025-09-30">Sept 30, 2025</time></td>
      <td><a href="https://github.com/openai/codex/pull/4521">PR #4521</a> merges, enabling <code>pre_main_hardening()</code> in release builds</td>
    </tr>
    <tr>
      <td><time datetime="2025-10-01">Oct 1, 2025</time></td>
      <td><samp>rust-v0.43.0</samp> ships <mark>(first affected release)</mark></td>
    </tr>
    <tr>
      <td><time datetime="2025-10-06">Oct 6, 2025</time></td>
      <td>First &ldquo;painfully slow&rdquo; regression reports</td>
    </tr>
    <tr>
      <td>Oct 1&ndash;29, 2025</td>
      <td>Spike in <var>env</var>/<var>PATH</var> inheritance issues across platforms</td>
    </tr>
    <tr>
      <td><time datetime="2025-10-29">Oct 29, 2025</time></td>
      <td>Emergency <var>PATH</var> fix lands <em>(did not catch root cause)</em></td>
    </tr>
    <tr>
      <td>Late Oct 2025</td>
      <td>OpenAI&rsquo;s specialized team investigates, declares there is no root cause, identifies issue as user behavior change</td>
    </tr>
    <tr>
      <td><time datetime="2026-01-09">Jan 9, 2026</time></td>
      <td><ins>My fix merged, credited in release notes</ins></td>
    </tr>
  </tbody>
</table>

#### Evidence Collected

<table>
  <thead>
    <tr>
      <th>Platform</th>
      <th>Issues</th>
      <th>Failure Mode</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>macOS</b></td>
      <td>#6012, #5679, #5339, #6243, #6218</td>
      <td><var>DYLD_*</var> stripping breaking dynamic linking</td>
    </tr>
    <tr>
      <td><b>Linux/<abbr title="Windows Subsystem for Linux 2">WSL2</abbr></b></td>
      <td>#4843, #3891, #6200, #5837, #6263</td>
      <td><var>LD_LIBRARY_PATH</var> stripping &rarr; silent <abbr title="Compute Unified Device Architecture">CUDA</abbr>/<abbr title="Math Kernel Library">MKL</abbr> degradation</td>
    </tr>
  </tbody>
</table>

**Compiled evidence packages:**

<dl>
  <dt><img src=".github/assets/icons/script.png" width="20" height="20" alt="">&ensp;Platform-specific failure modes</dt>
  <dd>Reproduction steps with quantifiable performance regressions (11&ndash;300&times;) and benchmarks</dd>
  <dt><img src=".github/assets/icons/lightbulb.png" width="20" height="20" alt="">&ensp;Pattern analysis</dt>
  <dd>Cross-referenced 15+ scattered user reports over 3 months, traced process environment inheritance through <code>fork</code>/<code>exec</code> boundaries</dd>
</dl>

  <img src=".github/assets/icons/script.png" width="20" height="20" alt=""> [Comprehensive Technical Analysis](https://github.com/user-attachments/files/24510983/GITHUB_ISSUE_DETAILED.md)<br>
  <img src=".github/assets/icons/lightbulb.png" width="20" height="20" alt=""> [Investigation Methodology](https://docs.google.com/document/d/1fDJc1e0itJdh0MXMFJtkRiBcxGEFtye6Xc6Ui7eMX4o/edit)

-----

### Why Conventional Debugging Failed

The bug was designed to be invisible:

<dl>
  <dt>Pre-main execution</dt>
  <dd>Used <code>#[ctor::ctor]</code> to run before <code>main()</code>, before any logging or instrumentation</dd>
  <dt>Silent stripping</dt>
  <dd>No warnings, no errors&thinsp;&mdash;&thinsp;just missing environment variables</dd>
  <dt>Distributed symptoms</dt>
  <dd>Appeared as unrelated issues across different platforms and configurations</dd>
  <dt>User attribution</dt>
  <dd>Everyone assumed they misconfigured something (shell looked fine)</dd>
  <dt>Wrong search space</dt>
  <dd>Team was debugging post-<code>main</code> application code</dd>
</dl>


> [!NOTE]
> Standard debugging tools cannot see pre-main execution. Profilers start at `main()`. Log hooks are not initialized yet. The code executes, modifies the environment, and vanishes.

-----

### The Impact

OpenAI confirmed and merged the fix within 24 hours, explicitly crediting the investigation in <samp>v0.80.0</samp> release notes:

> "Codex <abbr title="Command Line Interface">CLI</abbr> subprocesses again inherit env vars like <var>LD_LIBRARY_PATH</var>/<var>DYLD_LIBRARY_PATH</var> to avoid runtime issues. As explained in #8945, failure to pass along these environment variables to subprocesses that expect them (notably <abbr title="Graphics Processing Unit">GPU</abbr>-related ones), was causing 10×+ performance regressions! Special thanks to <kbd>@johnzfitch</kbd> for the detailed investigation and write-up in #8945."

**Restored:**

<table>
  <tbody>
    <tr>
      <td><ins><abbr title="Graphics Processing Unit">GPU</abbr> acceleration</ins></td>
      <td>Internal ML/AI dev teams</td>
    </tr>
    <tr>
      <td><ins><abbr title="Compute Unified Device Architecture">CUDA</abbr>/PyTorch</ins></td>
      <td>ML researchers</td>
    </tr>
    <tr>
      <td><ins><abbr title="Math Kernel Library">MKL</abbr>/NumPy</ins></td>
      <td>Scientific computing users</td>
    </tr>
    <tr>
      <td><ins>Conda environments</ins></td>
      <td>Cross-platform compatibility</td>
    </tr>
    <tr>
      <td><ins>Enterprise drivers</ins></td>
      <td>Database connectivity</td>
    </tr>
  </tbody>
</table>

When the tools are blind, the system lies, and everyone else has stopped looking for it..</details>

-----

## <img src=".github/assets/icons/toolbox.png" width="20" height="20" alt=""> Recent Work

<dl>
  <dt><a href="https://github.com/johnzfitch/claude-cowork-linux"><b>claude-cowork-linux</b></a> <sub>⭐287</sub></dt>
  <dd>Run Claude Desktop's Cowork mode natively on Linux by reverse-engineering macOS components for direct execution without a VM.</dd>

  <dt><a href="https://github.com/johnzfitch/dota"><b>dota</b></a></dt>
  <dd>Post-quantum secure secrets manager using hybrid ML-KEM-768 and X25519 encryption with a terminal UI for secure secret management.</dd>

  <dt><a href="https://github.com/johnzfitch/pyghidra-lite"><b>pyghidra-lite</b></a> <sub>⭐32</sub></dt>
  <dd>Token-efficient MCP server for Ghidra, enabling analysis of ELF, Mach-O, and PE binaries with Swift, Objective-C, and Hermes support.</dd>

  <dt><a href="https://github.com/johnzfitch/claude-wiki"><b>claude-wiki</b></a> <sub>⭐13</sub></dt>
  <dd>Comprehensive Markdown documentation mirror for Anthropic's Claude, featuring 2000+ articles on APIs, SDKs, agents, and integrations.</dd>

  <dt><a href="https://github.com/johnzfitch/claude-warden"><b>claude-warden</b></a> <sub>⭐58</sub></dt>
  <dd>Security hooks for Claude Code that optimize token usage, enforce budgets, and provide observability with OTEL tracing and SSRF protection.</dd>

  <dt><a href="https://github.com/johnzfitch/iconics"><b>iconics</b></a></dt>
  <dd>A semantic icon library leveraging SQLite for cataloging, offering intelligent search and markdown export for efficient project integration.</dd>

  <dt><a href="https://github.com/johnzfitch/llmx"><b>llmx</b></a></dt>
  <dd>Local-first codebase indexer utilizing BM25 and neural embeddings for efficient semantic search and chunk exports in-browser via WebGPU.</dd>

  <dt><a href="https://github.com/johnzfitch/arch-dependency-matrices"><b>arch-dependency-matrices</b></a></dt>
  <dd>Mathematical analysis of Arch Linux package dependencies using graph theory, spectral analysis, and linear algebra in Python.</dd>
</dl>

-----

## <img src=".github/assets/icons/star.png" width="20" height="20" alt=""> Selected Work

<dl>
  <dt><a href="https://github.com/johnzfitch/claude-cowork-linux"><b>claude-cowork-linux</b></a> <sub>⭐287</sub></dt>
  <dd>Run the official Claude Desktop app's Cowork mode natively on Linux with bubblewrap sandboxing — highest-adoption project in the portfolio</dd>

  <dt><a href="https://github.com/johnzfitch/specho-v2"><b>specHO</b></a></dt>
  <dd><abbr title="Large Language Model">LLM</abbr> watermark detection via phonetic/semantic analysis <em>(The Echo Rule)</em> — live demo at <a href="https://definitelynot.ai">definitelynot.ai</a></dd>

  <dt><a href="https://github.com/johnzfitch/codex-patcher"><b>codex-patcher</b></a></dt>
  <dd>Automated Rust code patching tool leveraging tree-sitter for syntax-aware modifications and reliable LLM-generated updates.</dd>

  <dt><a href="https://github.com/johnzfitch/htmx-docs"><b>htmx-docs</b></a></dt>
  <dd>Curated HTMX documentation in Markdown, including API references, Big Sky repos, and relevant RFCs, organized for easy access.</dd>

  <dt><a href="https://github.com/johnzfitch/filearchy"><b>filearchy</b></a></dt>
  <dd>Filearchy is a Wayland file manager forked from cosmic-files, enhancing workflows with custom MIME icons, extended archive support, and terminal integration.</dd>

  <dt><a href="https://github.com/johnzfitch/nautilus-plus"><b>nautilus-plus</b></a></dt>
  <dd>Enhanced Nautilus file manager with sub-millisecond search, large animated thumbnail support, and crash prevention features.</dd>

  <dt><a href="https://github.com/johnzfitch/indepacer"><b>indepacer</b></a></dt>
  <dd>CLI tool for querying PACER, enabling case searches, docket downloads, and document retrieval from federal court records.</dd>
</dl>

Self-hosting bare metal infrastructure (NixOS) with post-quantum cryptography, authoritative <abbr title="Domain Name System">DNS</abbr>, and containerized services.

-----

## <img src=".github/assets/icons/globe.png" width="20" height="20" alt=""> Live Demos

<dl>
  <dt><a href="https://definitelynot.ai"><b>Cosmic Code Cleaner</b></a> @ definitelynot.ai</dt>
  <dd>LLM paste sanitizer with vectorhit algorithm — fix curly quotes, invisible Unicode, confusable punctuation, dedent blocks</dd>

  <dt><a href="https://llm.cat"><b>LLMX Ingestor</b></a> @ llm.cat</dt>
  <dd>WebAssembly codebase indexer — private, deterministic chunking and BM25 search for large folders</dd>

  <dt><a href="https://internetuniverse.org"><b>LINTENIUM FIELD</b></a> @ internetuniverse.org</dt>
  <dd>Terminal-based <abbr title="Alternate Reality Game">ARG</abbr> experience — interactive mystery with audio visualizations</dd>

  <dt><a href="https://look.definitelynot.ai"><b>Observatory</b></a> @ look.definitelynot.ai</dt>
  <dd><abbr title="Web Graphics Processing Unit">WebGPU</abbr> deepfake detection running 4 ML models in browser</dd>
</dl>

-----

## Featured

### <img src=".github/assets/icons/shield.png" width="20" height="20" alt=""> [dota](https://github.com/johnzfitch/dota) — Post-Quantum Secrets Manager

**Defense of the Artifacts**: A secrets manager engineered for cryptographic longevity. While current encryption remains secure, "harvest now, decrypt later" attacks mean secrets stored today may be vulnerable to quantum computers within their lifetime. dota addresses this with hybrid post-quantum encryption that provides security against both classical and quantum adversaries.

<table>
  <thead>
    <tr>
      <th width="140">Layer</th>
      <th>Implementation</th>
      <th>Why It Matters</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>Key Encapsulation</b></td>
      <td>ML-KEM-768 + X25519 hybrid</td>
      <td><abbr title="National Institute of Standards and Technology">NIST</abbr>-standardized lattice crypto with classical fallback — if either is broken, the other protects</td>
    </tr>
    <tr>
      <td><b>Key Derivation</b></td>
      <td>Argon2id (memory-hard)</td>
      <td>Resists <abbr title="Graphics Processing Unit">GPU</abbr>/<abbr title="Application-Specific Integrated Circuit">ASIC</abbr> brute-force; tunable time/memory parameters</td>
    </tr>
    <tr>
      <td><b>Storage</b></td>
      <td>SQLCipher (AES-256-CBC)</td>
      <td>Encrypted at rest with authenticated pages; survives partial file corruption</td>
    </tr>
    <tr>
      <td><b>Hardware Auth</b></td>
      <td>HMAC-SHA1 challenge-response</td>
      <td>YubiKey/SoloKey required for unlock — no master password alone can decrypt</td>
    </tr>
  </tbody>
</table>

The <abbr title="Terminal User Interface">TUI</abbr> (Ratatui) provides vim-style navigation, fuzzy search across entries, secure clipboard integration with auto-clear, and <abbr title="Time-based One-Time Password">TOTP</abbr> generation for 2FA codes.

**Stack:** Rust &ensp;&bull;&ensp; pqcrypto (ML-KEM) &ensp;&bull;&ensp; x25519-dalek &ensp;&bull;&ensp; argon2 &ensp;&bull;&ensp; SQLCipher &ensp;&bull;&ensp; Ratatui

-----

### <img src=".github/assets/icons/search.png" width="20" height="20" alt=""> [llmx](https://github.com/johnzfitch/llmx) — Codebase Indexer for Local Agents

**Live Demo:** [llm.cat](https://llm.cat) (WebAssembly — runs entirely in browser, no upload)

Local-first codebase indexing with real neural embeddings (<b>Snowflake Arctic</b>) running via <abbr title="Web Graphics Processing Unit">WebGPU</abbr>. No server, no API calls, no data leaving your machine. Hybrid search combines BM25 keyword ranking with vector similarity using <abbr title="Reciprocal Rank Fusion">RRF</abbr> for best-of-both-worlds retrieval.

```bash
llmx index ~/projects/myapp           # Build trigram + BM25 index
llmx search "authentication middleware" --limit 20
llmx export --format md --max-tokens 8000   # Context-window-aware export
llmx serve --port 8080                # Local HTTP API for agents
```

<table>
  <thead>
    <tr>
      <th>Capability</th>
      <th>Implementation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>Neural Embeddings</b></td>
      <td>Snowflake Arctic vectors with <abbr title="Web Graphics Processing Unit">WebGPU</abbr> acceleration — ~50ms inference, same quality as server-side</td>
    </tr>
    <tr>
      <td><b>Hybrid Search</b></td>
      <td>BM25 + vector similarity fused via <abbr title="Reciprocal Rank Fusion">RRF</abbr> — handles exact matches and semantic similarity</td>
    </tr>
    <tr>
      <td><b>Smart Chunking</b></td>
      <td>Deterministic by file type: functions, headings, JSON keys — same input always yields identical chunks</td>
    </tr>
    <tr>
      <td><b>Semantic Exports</b></td>
      <td>Hierarchical outline format (<samp>llm.md</samp>) with function names and heading breadcrumbs for selective retrieval</td>
    </tr>
  </tbody>
</table>

<dl>
  <dt>Proof</dt>
  <dd><ruby>7,147 files<rp>(</rp><rt>Apple HIG corpus</rt><rp>)</rp></ruby> → <ruby>31 MB index<rp>(</rp><rt></rt><rp>)</rp></ruby> → <ruby>1,625 tokens<rp>(</rp><rt>99.98% savings</rt><rp>)</rp></ruby></dd>
  <dt>Stack</dt>
  <dd>Rust &ensp;&bull;&ensp; tantivy &ensp;&bull;&ensp; tree-sitter &ensp;&bull;&ensp; <abbr title="WebAssembly">WASM</abbr> &ensp;&bull;&ensp; WebGPU</dd>
</dl>

-----

### <img src=".github/assets/icons/lock.png" width="20" height="20" alt=""> [claude-warden](https://github.com/johnzfitch/claude-warden) — Security Hooks for Claude Code

A defense-in-depth hook system for Claude Code that addresses token efficiency, security boundaries, and observability. Born from months of production use identifying failure modes in <abbr title="Large Language Model">LLM</abbr> coding agents.

**The Problem:** Claude Code's default behavior can burn tokens on verbose command output, leak internal network topology via <abbr title="Server-Side Request Forgery">SSRF</abbr>, spawn unbounded subagents, and produce unobservable execution traces.

<table>
  <thead>
    <tr>
      <th width="160">Hook</th>
      <th>Threat Model</th>
      <th>Mitigation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><samp>quiet-overrides</samp></td>
      <td>Token exhaustion from <code>npm install</code>, <code>cargo build</code>, <code>git log</code></td>
      <td>Injects <code>-q</code>/<code>--silent</code>/<code>--quiet</code> flags; caps output at configurable byte limit</td>
    </tr>
    <tr>
      <td><samp>ssrf-protection</samp></td>
      <td>Agent fetching <code>http://169.254.169.254</code> (cloud metadata) or internal services</td>
      <td>Blocks RFC1918/link-local ranges; allowlist for legitimate internal APIs</td>
    </tr>
    <tr>
      <td><samp>mcp-compression</samp></td>
      <td><abbr title="Model Context Protocol">MCP</abbr> tool outputs flooding context window</td>
      <td>gzip + base64 for large payloads; configurable threshold</td>
    </tr>
    <tr>
      <td><samp>subagent-budget</samp></td>
      <td>Recursive agent spawning exhausting API quota</td>
      <td>Per-session spawn limits; depth tracking; cost estimation</td>
    </tr>
    <tr>
      <td><samp>otel-tracing</samp></td>
      <td>Black-box execution; no audit trail</td>
      <td>Exports spans to Grafana/Loki with tool calls, durations, token counts</td>
    </tr>
  </tbody>
</table>

```bash
# Example: warden blocks verbose npm and injects quiet flag
$ claude "install dependencies"
# [warden] Intercepted: npm install → npm install --silent
# [warden] Output capped at 4096 bytes (was 847KB)
```

**Stack:** Shell &ensp;&bull;&ensp; jq &ensp;&bull;&ensp; OpenTelemetry &ensp;&bull;&ensp; Prometheus &ensp;&bull;&ensp; Grafana/Loki

-----

## <img src=".github/assets/icons/ai-brain.png" width="20" height="20" alt=""> AI / ML / Agent Tooling

- **[claude-wiki](https://github.com/johnzfitch/claude-wiki)** ⭐13 — Comprehensive Anthropic documentation wiki — 749+ docs across 24 categories
- **[observatory](https://github.com/johnzfitch/observatory)** — WebGPU deepfake detection with 4 ML models — live: [look.definitelynot.ai](https://look.definitelynot.ai)
- **[specHO](https://github.com/johnzfitch/specho-v2)** — LLM watermark detection via phonetic/semantic analysis — live: [definitelynot.ai](https://definitelynot.ai)
- **[burn-plugin](https://github.com/johnzfitch/burn-plugin)** — Claude Code plugin for the Burn deep learning framework
- **[raley-bot](https://github.com/johnzfitch/raley-bot)** — Automated grocery assistant with F5 bot detection evasion, unit pricing across bizarre measurements, automatic coupon clipping, and MCP server for Claude Desktop

-----

## <img src=".github/assets/icons/server.png" width="20" height="20" alt=""> Infrastructure

**Primary server:** Dedicated bare-metal NixOS host <sub>(details available on request)</sub>

<table>
  <tbody>
    <tr>
      <th align="left" width="120">Security</th>
      <td>Post-quantum <abbr title="Secure Shell">SSH</abbr> &ensp;&bull;&ensp; Rosenpass <abbr title="Virtual Private Network">VPN</abbr> &ensp;&bull;&ensp; <samp>nftables</samp> firewall</td>
    </tr>
    <tr>
      <th align="left"><abbr title="Domain Name System">DNS</abbr></th>
      <td>Unbound resolver with <abbr title="Domain Name System Security Extensions">DNSSEC</abbr> &ensp;&bull;&ensp; ad/tracker blocking</td>
    </tr>
    <tr>
      <th align="left">Services</th>
      <td>FreshRSS &ensp;&bull;&ensp; Caddy (<abbr title="HTTP Secure">HTTPS</abbr>/<abbr title="HTTP version 3">HTTP/3</abbr>) &ensp;&bull;&ensp; cPanel/WHM &ensp;&bull;&ensp; Podman containers</td>
    </tr>
    <tr>
      <th align="left">Network</th>
      <td>Local 10<small>Gbps</small> &ensp;&bull;&ensp; Authoritative BIND9 with <abbr title="Request for Comments 2136">RFC&thinsp;2136</abbr> <abbr title="Automatic Certificate Management Environment">ACME</abbr></td>
    </tr>
  </tbody>
</table>

<p align="center">
  <a href="https://johnzfitch.github.io/johnzfitch/">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset=".github/assets/cards/typing-philosophy-dark.svg">
    <img alt="Philosophy" src=".github/assets/cards/typing-philosophy-light.svg" width="100%">
  </picture>
  </a>
</p>
