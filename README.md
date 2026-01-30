# John Zachary Fitch

**Agent tooling - systems performance - privacy-first infrastructure**

Open to roles building agent runtimes, developer tools, retrieval systems, and security/privacy foundations.

- Resume: [RESUME.md](RESUME.md)
- Email: webmaster@internetuniverse.org
- GitHub: https://github.com/johnzfitch
- Website: https://definitelynot.ai

| Proof | Link |
|---|---|
| Ghost bug fix (OpenAI Codex) | https://github.com/openai/codex/issues/8945 and https://github.com/openai/codex/pull/8951 |
| Credited in release notes | https://github.com/openai/codex/releases/tag/rust-v0.80.0 |
| Changelog context | https://developers.openai.com/codex/changelog |
| Live demo | https://look.definitelynot.ai |

---

## Ghost in the Codex Machine (Jan 2026)

A pre-main security-hardening routine in OpenAI Codex release builds stripped `LD_*` / `DYLD_*` environment variables before `main()` ran. For CUDA, Conda/MKL, and HPC users, this caused critical libraries to "disappear" inside subprocesses, forcing slow fallback paths (10x-300x slowdowns). I traced the root cause, wrote a reproduction with benchmarks, and shipped the upstream fix.

| Workload | Before | After | Speedup |
|----------|-------:|------:|--------:|
| MKL/BLAS (10x 2000x2000 matmul) | 16.3s | 0.306s | 53x |
| CUDA workflows | 11x-300x slower | restored | varies |

What this demonstrates:
- Systems debugging under real-world constraints (pre-main execution, release-only behavior, silent failures)
- Performance engineering with reproducible measurement
- Security tradeoff reasoning grounded in practical threat models
- High-quality upstream collaboration: issue -> fix -> verification -> shipped release notes

---

## Selected Work (LLM/Agent-Centric)

| Project | What it is | Why it matters |
|---|---|---|
| https://github.com/johnzfitch/codex-xtreme | Build wizard for optimized, patched Codex binaries (powered by codex-patcher) | Productizes the "agent edit loop" into reproducible build + patch workflows |
| https://github.com/johnzfitch/llmx | Local-first codebase indexer with BM25 search + semantic chunk exports (Rust/WASM) | Retrieval that is fast, deterministic, and privacy-first |
| https://github.com/johnzfitch/pyghidra-lite | Token-efficient MCP server for tool-driven program analysis | Turns complex analysis into a structured tool surface with controllable verbosity |
| https://github.com/johnzfitch/burn-plugin | Claude Code plugin + skills for the Burn deep learning framework | Demonstrates reusable skill packaging and evidence-backed workflows |
| https://github.com/johnzfitch/claude-cowork-linux | Run the official Claude Desktop app on Linux with bubblewrap sandboxing | Makes LLM workflows first-class on Linux without sacrificing isolation |
| https://github.com/johnzfitch/specho-v2 | 161D linguistic fingerprinting for AI text detection and model identification | Algorithm-first detection with a tiered runtime pipeline |
| https://github.com/johnzfitch/iconics | Semantic icon library (8k+ icons) for professional docs (no emojis) | Documentation polish as a product surface; consistent visual language |
| https://github.com/johnzfitch/definitelynot.ai | Unicode-security-aware sanitizer (Trojan Source, BiDi, homoglyph defense) | Practical defensive tooling for real text pipelines |

---

## Infrastructure

Self-hosted bare-metal NixOS with:
- Declarative configuration (flakes, atomic upgrades, rollbacks)
- Authoritative DNS and automated wildcard certs (DNS-01 / RFC2136)
- Post-quantum security layers (hybrid SSH KEX, WireGuard + Rosenpass)

---

## Private Work (Names Only)

- digitaldelusion (NixOS infrastructure)
- cwork (context compiler / skill system for Claude Code workflows; available on request)
- eero
- alienware-monitor
- proxyforge

---

## Education

UC Berkeley - Mathematics

---

## Contact

- Email: webmaster@internetuniverse.org
- GitHub: https://github.com/johnzfitch
- Website: https://definitelynot.ai

---

<sub>SF Bay Area / Open to remote</sub>
