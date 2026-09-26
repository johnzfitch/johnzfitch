<figure>
  <img src=".github/assets/header.svg" alt="Header">
</figure>
<p align="center">
  <a href="https://definitelynot.ai"><img src=".github/assets/buttons/definitelynot@2x.png" alt="definitelynot.ai" width="176" height="62"></a>&nbsp;
  <a href="https://internetuniverse.org"><img src=".github/assets/buttons/internetuniverse@2x.png" alt="Internet Universe" width="176" height="62"></a>&nbsp;
  <a href="https://math.berkeley.edu"><img src=".github/assets/buttons/berkeley-math@2x.png" alt="UC Berkeley Mathematics" width="176" height="62"></a>&nbsp;
  <a href="mailto:zack@internetuniverse.org"><img src=".github/assets/buttons/email@2x.png" alt="Email" width="176" height="62"></a>
</p>
<p align="center">
  <sub>SF Bay Area &ensp;&bull;&ensp; <a href="https://johnzfitch.github.io/johnzfitch">Git Page</a> &ensp;&bull;&ensp; All icons from <a href="https://github.com/johnzfitch/iconics">iconics</a></sub>
</p>

<!-- Link Reference Definitions (Layer 1: invisible metadata) -->

-----

## OpenAI Codex: the ghost in the machine

> [!IMPORTANT]
> A <ruby>pre-`main()`<rp>(</rp><rt>⁠#[ctor::ctor]</rt><rp>)</rp></ruby> constructor in Codex was stripping <var>LD_*</var> and <var>DYLD_*</var> from the environment, and every tool subprocess inherited the stripped copy. CUDA and MKL couldn't find their libraries, so work fell back to slow paths, <mark>11 to 300 times slower</mark>, on every supported OS, and nothing reported an error. OpenAI put a team on it for a week and didn't find a root cause, because their tools couldn't see code that ran before they loaded. I traced it to one commit, built a reproduction harness, and wrote it up. An OpenAI maintainer wrote the fix from my investigation, it shipped in <samp>rust-v0.80.0</samp>, and the release notes thank me by name. It had also been the main thing keeping Codex from spawning and controlling subagents that worked.

Proof: [Issue #8945](https://github.com/openai/codex/issues/8945)  |  [PR #8951](https://github.com/openai/codex/pull/8951)  |  [Release notes (<samp>rust-v0.80.0</samp>)](https://github.com/openai/codex/releases/tag/rust-v0.80.0)

<details>
<summary><b>The full investigation</b></summary>

<br>

### The ghost

In <time datetime="2025-10">October 2025</time>, OpenAI put together a team to look into slowdowns in <b>Codex</b> that nobody could explain. They spent a week on it and came up empty.

I called it a ghost because that's how it acted. `pre_main_hardening()` ran before `main()`, which meant it ran before any profiler attached and before logging started. It removed <var>LD_LIBRARY_PATH</var> and <var>DYLD_LIBRARY_PATH</var> from the process environment, handed control to `main()`, and left no trace. Users could see the variables set in their shell. Inside <samp>codex exec</samp>, they were empty.

-----

### Finding it

<b>Three days</b> after their announcement, I had the commit that introduced it ([PR #4521](https://github.com/openai/codex/pull/4521)) and a working theory. I sent both to <kbd>@tibo_openai</kbd>.

Knowing the commit didn't prove anything yet. I spent the next <b>2 months</b> building repro harnesses, benchmarking CUDA, Conda, MKL, and HPC setups, and lining up 15+ scattered user reports until the pattern was clear.

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
      <td>Emergency <var>PATH</var> fix lands <em>(didn't catch the root cause)</em></td>
    </tr>
    <tr>
      <td>Late Oct 2025</td>
      <td>OpenAI&rsquo;s team investigates, finds no root cause, and puts it down to a change in user behavior</td>
    </tr>
    <tr>
      <td><time datetime="2026-01-09">Jan 9, 2026</time></td>
      <td><ins>Fix merged from my investigation, credited in release notes</ins></td>
    </tr>
  </tbody>
</table>

#### Evidence

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

**What I put together:**

<dl>
  <dt><img src=".github/assets/icons/script.png" width="20" height="20" alt="">&ensp;Failure modes on each platform</dt>
  <dd>Reproduction steps and benchmarks that show the 11&ndash;300&times; slowdowns</dd>
  <dt><img src=".github/assets/icons/lightbulb.png" width="20" height="20" alt="">&ensp;Matching up the reports</dt>
  <dd>Matched 15+ scattered user reports over 3 months and followed the environment through <code>fork</code>/<code>exec</code></dd>
</dl>

  <img src=".github/assets/icons/script.png" width="20" height="20" alt=""> [Full technical write-up](https://github.com/user-attachments/files/24510983/GITHUB_ISSUE_DETAILED.md)<br>
  <img src=".github/assets/icons/lightbulb.png" width="20" height="20" alt=""> [How I investigated it](https://docs.google.com/document/d/1fDJc1e0itJdh0MXMFJtkRiBcxGEFtye6Xc6Ui7eMX4o/edit)

-----

### Why normal debugging missed it

Everything about it made it hard to see:

<dl>
  <dt>Ran before <code>main()</code></dt>
  <dd><code>#[ctor::ctor]</code> ran it before any logging or instrumentation was set up</dd>
  <dt>No noise</dt>
  <dd>No warning and no error. The variables were just gone</dd>
  <dt>Scattered symptoms</dt>
  <dd>It showed up as unrelated issues on different platforms and setups</dd>
  <dt>Blamed on users</dt>
  <dd>Everyone assumed they'd misconfigured something, since their shell looked fine</dd>
  <dt>Wrong place to look</dt>
  <dd>The team was debugging application code that runs after <code>main()</code></dd>
</dl>


> [!NOTE]
> Standard debugging tools don't see code that runs before `main()`. Profilers start at `main()`, and logging isn't set up yet. The constructor runs, changes the environment, and is gone.

-----

### What happened next

OpenAI confirmed it and merged a fix within 24 hours. The <samp>v0.80.0</samp> release notes credit the investigation:

> "Codex <abbr title="Command Line Interface">CLI</abbr> subprocesses again inherit env vars like <var>LD_LIBRARY_PATH</var>/<var>DYLD_LIBRARY_PATH</var> to avoid runtime issues. As explained in #8945, failure to pass along these environment variables to subprocesses that expect them (notably <abbr title="Graphics Processing Unit">GPU</abbr>-related ones), was causing 10×+ performance regressions! Special thanks to <kbd>@johnzfitch</kbd> for the detailed investigation and write-up in #8945."

**What works again:**

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

TL;DR: it was literally a ghost. It ran before <code>main()</code>, stripped the environment, and disappeared, leaving nothing behind but confused users reporting slowness.</details>

-----

## <img src=".github/assets/icons/toolbox.png" width="20" height="20" alt=""> Recent Work

<dl>
  <dt><a href="https://github.com/johnzfitch/claude-cowork-linux"><b>claude-cowork-linux</b></a> <sub>⭐419</sub></dt>
  <dd>Runs Claude Desktop's Cowork mode natively on Linux. Bubblewrap stands in for the VM, and the ASAR is unpacked on the host before any sandboxed code runs. My most-starred project.</dd>

  <dt><a href="https://github.com/johnzfitch/llmx"><b>llmx</b></a></dt>
  <dd>Codebase indexer that runs on your own machine. BM25 plus mdbr-leaf-ir embeddings (Burn), merged with reciprocal rank fusion, and deterministic chunking. Also runs in the browser on WebGPU/WASM at llm.cat.</dd>

  <dt><a href="https://github.com/johnzfitch/dota"><b>dota</b></a></dt>
  <dd>Post-quantum secrets manager with a terminal UI. v7 TC-HKEM hybrid (ML-KEM-768 + X25519), an Argon2id master key, and an AES-256-GCM encrypted JSON vault.</dd>

  <dt><a href="https://github.com/johnzfitch/claude-wiki"><b>claude-wiki</b></a> <sub>⭐23</sub></dt>
  <dd>Anthropic's Claude docs as 2000+ Markdown files in 24 categories, pulled from first-party sources and refreshed daily.</dd>

  <dt><a href="https://github.com/johnzfitch/pyghidra-lite"><b>pyghidra-lite</b></a> <sub>⭐36</sub></dt>
  <dd>MCP server for Ghidra that keeps token use low. Reads ELF, Mach-O, and PE binaries, with Swift, Objective-C, and Hermes support.</dd>

  <dt><a href="https://github.com/johnzfitch/raley-bot"><b>raley-bot</b></a></dt>
  <dd>Grocery shopping assistant built on a store's web API. It picks products, tracks prices, and clips coupons, from a CLI or as an MCP server.</dd>

  <dt><a href="https://github.com/johnzfitch/indepacer"><b>indepacer</b></a></dt>
  <dd>Python CLI for PACER. Searches federal cases and downloads dockets and documents through PCL and CM/ECF, with MFA and cost protection.</dd>

  <dt><a href="https://github.com/johnzfitch/claude-warden"><b>claude-warden</b></a> <sub>⭐60</sub></dt>
  <dd>Security hooks for Claude Code. Blocks SSRF probes, caps how many subagents can spawn, compresses MCP output, and sends every tool call to OTEL traces.</dd>
</dl>

-----

## <img src=".github/assets/icons/star.png" width="20" height="20" alt=""> Selected Work

<dl>
  <dt><a href="https://github.com/johnzfitch/claude-cowork-linux"><b>claude-cowork-linux</b></a> <sub>⭐419</sub></dt>
  <dd>Runs the official Claude Desktop app's Cowork mode natively on Linux. Bubblewrap stands in for the VM, and the ASAR is unpacked on the host before any sandboxed code runs.</dd>

  <dt><a href="https://github.com/johnzfitch/specho-v2"><b>specHO</b></a></dt>
  <dd>Detects <abbr title="Large Language Model">LLM</abbr> watermarks with phonetic and semantic analysis <em>(The Echo Rule)</em>. Live demo at <a href="https://definitelynot.ai">definitelynot.ai</a></dd>

  <dt><a href="https://github.com/johnzfitch/codex-patcher"><b>codex-patcher</b></a></dt>
  <dd>Patches Rust code automatically with byte-span replacement and tree-sitter, so LLM-written edits land where they're supposed to.</dd>

  <dt><a href="https://github.com/johnzfitch/htmx-docs"><b>htmx-docs</b></a></dt>
  <dd>HTMX docs in Markdown: the API reference, the Big Sky repos, and the relevant RFCs.</dd>

  <dt><a href="https://github.com/johnzfitch/filearchy"><b>filearchy</b></a></dt>
  <dd>Wayland file manager forked from COSMIC Files, with custom MIME icons, more archive formats, and terminal integration.</dd>

  <dt><a href="https://github.com/johnzfitch/nautilus-plus"><b>nautilus-plus</b></a></dt>
  <dd>Nautilus fork with sub-millisecond search, thumbnails for large animated files, and fixes that keep it from crashing.</dd>

  <dt><a href="https://github.com/johnzfitch/indepacer"><b>indepacer</b></a></dt>
  <dd>CLI for PACER: search federal cases and pull dockets and documents from federal court records.</dd>
</dl>

I self-host on bare metal (NixOS), with post-quantum crypto, my own authoritative <abbr title="Domain Name System">DNS</abbr>, and containers.

-----

## <img src=".github/assets/icons/globe.png" width="20" height="20" alt=""> Live Demos

<dl>
  <dt><a href="https://definitelynot.ai"><b>Cosmic Code Cleaner</b></a> @ definitelynot.ai</dt>
  <dd>Cleans up text you paste out of an LLM, using the vectorhit algorithm: curly quotes, invisible Unicode, look-alike punctuation, and indented blocks.</dd>

  <dt><a href="https://llm.cat"><b>LLMX Ingestor</b></a> @ llm.cat</dt>
  <dd>WebAssembly codebase indexer. Deterministic chunking and BM25 search for large folders, and your files never leave your machine.</dd>

  <dt><a href="https://internetuniverse.org"><b>LINTENIUM FIELD</b></a> @ internetuniverse.org</dt>
  <dd>A puzzle <abbr title="Alternate Reality Game">ARG</abbr> in a terminal: an interactive mystery with audio visualizations.</dd>

  <dt><a href="https://look.definitelynot.ai"><b>Observatory</b></a> @ look.definitelynot.ai</dt>
  <dd>Deepfake detection that runs 4 ML models in your browser on <abbr title="Web Graphics Processing Unit">WebGPU</abbr>.</dd>
</dl>

-----

## Featured

### <img src=".github/assets/icons/shield.png" width="20" height="20" alt=""> [dota](https://github.com/johnzfitch/dota): post-quantum secrets manager

**Defense of the Artifacts.** A secrets manager for secrets that have to stay secret for a long time. Today's encryption holds up fine, but someone can record encrypted data now and decrypt it later, once quantum computers can break it ("harvest now, decrypt later"). dota uses hybrid post-quantum encryption, so an attacker would have to break both the classical layer and the post-quantum one.

<table>
  <thead>
    <tr>
      <th width="140">Layer</th>
      <th>Implementation</th>
      <th>Why</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>Key Encapsulation</b></td>
      <td>ML-KEM-768 + X25519 hybrid</td>
      <td><abbr title="National Institute of Standards and Technology">NIST</abbr>-standardized lattice crypto plus a classical fallback. If one is broken, the other still protects you</td>
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
      <td>Unlocking needs the YubiKey or SoloKey. The master password alone can't decrypt anything</td>
    </tr>
  </tbody>
</table>

The <abbr title="Terminal User Interface">TUI</abbr> (Ratatui) has vim-style navigation, fuzzy search, a clipboard that clears itself, and <abbr title="Time-based One-Time Password">TOTP</abbr> codes for 2FA.

**Stack:** Rust &ensp;&bull;&ensp; pqcrypto (ML-KEM) &ensp;&bull;&ensp; x25519-dalek &ensp;&bull;&ensp; argon2 &ensp;&bull;&ensp; SQLCipher &ensp;&bull;&ensp; Ratatui

-----

### <img src=".github/assets/icons/search.png" width="20" height="20" alt=""> [llmx](https://github.com/johnzfitch/llmx): codebase indexer for local agents

**Live demo:** [llm.cat](https://llm.cat) (WebAssembly; it runs entirely in your browser and uploads nothing)

Indexes a codebase on your own machine, with real neural embeddings (<b>mdbr-leaf-ir</b>) running on <abbr title="Web Graphics Processing Unit">WebGPU</abbr>. There's no server and no API call, so your code stays put. Search combines BM25 keyword ranking with vector similarity through <abbr title="Reciprocal Rank Fusion">RRF</abbr>, so it finds exact matches and things that mean the same.

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
      <td><b>Embeddings</b></td>
      <td>mdbr-leaf-ir vectors on <abbr title="Web Graphics Processing Unit">WebGPU</abbr>. About 50ms per inference, same quality as running it on a server</td>
    </tr>
    <tr>
      <td><b>Hybrid search</b></td>
      <td>BM25 and vector similarity merged with <abbr title="Reciprocal Rank Fusion">RRF</abbr>, so exact matches and similar meaning both count</td>
    </tr>
    <tr>
      <td><b>Chunking</b></td>
      <td>Split by file type (functions, headings, JSON keys). The same input always gives the same chunks</td>
    </tr>
    <tr>
      <td><b>Exports</b></td>
      <td>An outline file (<samp>llm.md</samp>) with function names and heading breadcrumbs, so an agent can pull only the part it needs</td>
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

### <img src=".github/assets/icons/lock.png" width="20" height="20" alt=""> [claude-warden](https://github.com/johnzfitch/claude-warden): security hooks for Claude Code

Hooks for Claude Code that cut wasted tokens, hold security boundaries, and record what the agent did. I wrote them after months of using <abbr title="Large Language Model">LLM</abbr> coding agents every day and writing down how they failed.

**The problem:** out of the box, Claude Code can burn tokens on noisy command output, expose your internal network through <abbr title="Server-Side Request Forgery">SSRF</abbr>, spawn subagents without limit, and leave no record you can inspect.

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

- **[claude-wiki](https://github.com/johnzfitch/claude-wiki)** ⭐23: Anthropic's docs as a Markdown wiki, 2000+ files across 24 categories
- **[observatory](https://github.com/johnzfitch/observatory)**: deepfake detection with 4 ML models on WebGPU. Live at [look.definitelynot.ai](https://look.definitelynot.ai)
- **[specHO](https://github.com/johnzfitch/specho-v2)**: LLM watermark detection with phonetic and semantic analysis. Live at [definitelynot.ai](https://definitelynot.ai)
- **[burn-plugin](https://github.com/johnzfitch/burn-plugin)**: Claude Code plugin for the Burn deep learning framework
- **[raley-bot](https://github.com/johnzfitch/raley-bot)**: grocery assistant that gets past F5 bot detection, works out unit prices across bizarre measurements, clips coupons automatically, and runs as an MCP server for Claude Desktop

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
