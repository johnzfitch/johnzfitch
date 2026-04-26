# Resume — John Zachary Fitch

> Agent tooling | systems performance | privacy-first infrastructure

I build production-grade tooling for agents and the substrate they depend on: deterministic retrieval, verifiable edits, structured tool APIs, and execution environments you can reason about. I work across Rust, Python, and web platforms with an evidence-first style: measure, reproduce, fix, and ship.

## Recent Highlight (Jan 2026)

**OpenAI Codex — Ghost in the Codex Machine**

Investigated and helped fix an "invisible" release-only regression where a pre-main constructor stripped `LD_*` / `DYLD_*` environment variables, breaking CUDA/MKL library discovery inside tool subprocesses. Shipped upstream with release-notes credit.

- [Issue #8945](https://github.com/openai/codex/issues/8945) / [Fix PR #8951](https://github.com/openai/codex/pull/8951)
- [Shipped + credited in rust-v0.80.0](https://github.com/openai/codex/releases/tag/rust-v0.80.0)

Representative impact:
- MKL/BLAS (repro harness): ~2.71s → ~0.239s (11.3×)
- CUDA workflows: restored expected library discovery to avoid CPU fallback in affected setups.

> "Special thanks to @johnzfitch for the detailed investigation and write-up in #8945."

## How I Work

- Construct from first principles rather than refine existing forms.
- Recover overlooked work — revisit ideas and approaches that didn't take the first time, with current tools.
- Probe working systems for hidden assumptions; rebuild the parts that don't hold up.
- Operate well in complex, debated, high-ambiguity spaces.
- Find a useful subspace inside a team early; manage well under crisis and time pressure.

## Core Skills

- **Rust** — performance-critical systems, CLI tools, data structures, correctness-oriented engineering.
- **Python** — tooling, analysis pipelines, automation, reproducible experiments.
- **Web** — WebGPU/WASM applications, client-side ML inference, offline-first UX.
- **Systems** — Linux, NixOS, DNS, TLS automation, containerized services, security hardening.
- **Agent integration** — MCP servers, skill/plugin packaging, tool-driven workflows.

## Selected Projects (Public)

- **[llmx](https://github.com/johnzfitch/llmx)** (Rust core, JS/WASM web; live: [llm.cat](https://llm.cat)) — local-only codebase indexer built on Burn-ml and mdbr-leaf-ir; hybrid search (BM25 + neural embeddings) fused via RRF; deterministic chunking with content hashing.
- **[claude-warden](https://github.com/johnzfitch/claude-warden)** (Shell/OTEL, 57 stars) — security hooks and budget system for Claude Code, with a built-in web viewer for extensive OTEL traces.
- **[claude-cowork-linux](https://github.com/johnzfitch/claude-cowork-linux)** (Linux, 236 stars) — native Linux port of Claude Desktop, security-first: treat the host OS as the VM (no Mac VM layer), wrap in bubblewrap, and handle the ASAR from outside the sandbox rather than hooking in; strips dispatch/channels, preserves Cowork/Code/Chat.
- **[dota](https://github.com/johnzfitch/dota)** (Rust) — post-quantum secrets manager: hybrid ML-KEM-768 + X25519, Argon2id KDF, SQLCipher at rest, YubiKey/SoloKey HMAC-SHA1 hardware auth.
- **[pyghidra-lite](https://github.com/johnzfitch/pyghidra-lite)** (Python/MCP, 32 stars) — token-efficient MCP server for Ghidra. Official MCP registry: `io.github.johnzfitch/pyghidra-lite` (v0.1.1).
- **[codex-xtreme](https://github.com/johnzfitch/codex-xtreme)** (Rust) — optimized, patched Codex builds (includes [codex-patcher](https://github.com/johnzfitch/codex-patcher)).
- **[burn-plugin](https://github.com/johnzfitch/burn-plugin)** — Claude Code plugin + skills for the Burn deep learning framework.
- **[Observatory](https://look.definitelynot.ai)** (WebGPU) — client-side AI image detection (live).
- **[SpecHO v2](https://github.com/johnzfitch/specho-v2)** (Python) — 161D linguistic fingerprinting for AI text detection.
- **[definitelynot.ai](https://github.com/johnzfitch/definitelynot.ai)** (PHP/JS) — Unicode-security-aware sanitizer + API.
- **[Iconics](https://github.com/johnzfitch/iconics)** (Python) — semantic icon library for professional docs (8k+ icons).

## Operating Background

Owner-operator of a regulated chemical-manufacturing business for 10 years; FDA and CPSC oversight, hazardous-substance handling. Sustained a multi-year PMTA process under non-committal regulatory guidance, including FOIA-driven information gathering. Mission: help adults worldwide quit smoking cigarettes. Declined paths that diverged from that mission even when commercially favorable; wound down on deliberate terms in the company's strongest revenue year.

What this established:
- Tolerance for prolonged regulatory ambiguity without losing direction.
- Operating discipline at production scale: manufacturing, compliance, hiring, crisis response.
- Over a decade under public scrutiny — grounded in the work, confident defending it on the record, practiced at navigating it responsibly.

## Infrastructure (Self-Hosted)

I operate production infrastructure on bare metal with:
- Declarative NixOS configuration (reproducible, atomic upgrades, rollbacks).
- Authoritative DNS and automated wildcard certificates (DNS-01 / RFC2136).
- Post-quantum security layers (hybrid SSH KEX, WireGuard + Rosenpass).

## Education

UC Berkeley — Mathematics. Withdrew during the 2020 lockdowns under a granted automatic readmission.

## What I'm Looking For

Roles building agent runtimes and developer tools, retrieval systems, and security/privacy foundations. I work best on teams that value measurable results, clear ownership, and high engineering standards.

## Contact

- Email: [webmaster@internetuniverse.org](mailto:webmaster@internetuniverse.org)
- GitHub: [github.com/johnzfitch](https://github.com/johnzfitch)
- PDF: [resume.pdf](resume.pdf)
