# John Zachary Fitch

Agent tooling | systems performance | privacy-first infrastructure

SF Bay Area (open to remote)

- Email: webmaster@internetuniverse.org
- GitHub: https://github.com/johnzfitch
- Website: https://definitelynot.ai
- Live demo: https://look.definitelynot.ai

---

## Summary

I build production-grade tooling for agents and the substrate they depend on: deterministic retrieval, verifiable edits, structured tool APIs, and execution environments you can reason about. I work across Rust, Python, and web platforms with an evidence-first style: measure, reproduce, fix, and ship.

---

## Highlights (Jan 2026)

### OpenAI Codex: Revealing the "Ghost in the Codex Machine" (Issue [#8945](https://github.com/openai/codex/issues/8945), PR [#8951](https://github.com/openai/codex/pull/8951))

I investigated and helped fix an "invisible" regression in OpenAI Codex where a pre-main constructor ran before `main()` and stripped `LD_*` / `DYLD_*` environment variables. For GPU workloads such as CUDA, Conda/MKL, HPC-style setups, this was a hard regression that made critical dynamic libraries disappear inside tool subprocesses and forced slow fallback, infinite hangs, or silent failure. Every child process, including subagents, inherited this stripped environment. Those children (Python/Conda/NumPy/PyTorch, often glibc-linked) can genuinely depend on LD_LIBRARY_PATH for CUDA/MKL/non-RPATH setups. 

The fix shipped upstream with the help of maintainers and was given a special credit within 0.80 release notes.

Release notes excerpt:
> "Special thanks to @johnzfitch for the detailed investigation and write-up in #8945."

To map the true scope, I validated behavior across macOS, Windows, and Linux and reduced it to a minimal reproduction + benchmark-backed report.

Proof:
- Issue: https://github.com/openai/codex/issues/8945
- Fix PR: https://github.com/openai/codex/pull/8951
- Release notes: https://github.com/openai/codex/releases/tag/rust-v0.80.0
- Changelog: [https://developers.openai.com/codex/changelog](https://developers.openai.com/codex/changelog#github-release-275597320)

Timeline:
- 2025-09-30: regression introduced (PR #4521)
- 2025-10-31: OpenAI concludes [internal investigation](https://docs.google.com/document/d/1fDJc1e0itJdh0MXMFJtkRiBcxGEFtye6Xc6Ui7eMX4o/edit?usp=sharing)
- 2026-01-08: I opened issue #8945 with root cause + reproduction + benchmarks
- 2026-01-09: fix merged (PR #8951) and shipped in the rust-v0.80.0 release series

Representative measurements (vary by environment):
| Workload | Before | After | Speedup |
|---|---:|---:|---:|
| MKL/BLAS (repro harness) | ~2.71s | ~0.239s | 11.3x |
| CUDA workflows (library discovery / GPU fallback) | 100x-300x slower | restored | varies |

---

## Selected Work (Public)

Agent build and edit loop:
- codex-xtreme (includes codex-patcher): reproducible build + patch workflow for Codex binaries. https://github.com/johnzfitch/codex-xtreme

Local-first retrieval:
- llmx: codebase indexing with deterministic chunking + BM25 search + exports for agent context. https://github.com/johnzfitch/llmx

Tool surfaces (MCP):
- pyghidra-lite: token-efficient MCP server for tool-driven program analysis (compact by default, opt-in verbosity). Official MCP registry: `io.github.johnzfitch/pyghidra-lite` (v0.1.1, active, published 2026-01-29). Repo: https://github.com/johnzfitch/pyghidra-lite

Agent skills and plugins (Anthropic ecosystem):
- burn-plugin: Claude Code plugin + reusable skills for the Burn deep learning framework (evidence-backed workflows). https://github.com/johnzfitch/burn-plugin
- claude-cowork-linux: run the official Claude Desktop app on Linux with bubblewrap sandboxing. https://github.com/johnzfitch/claude-cowork-linux

ML/detection and safety:
- Observatory: client-side AI image detection (WebGPU/WASM). Live: https://look.definitelynot.ai Repo: https://github.com/johnzfitch/observatory
- SpecHO v2: 161D linguistic fingerprinting for AI text detection and model identification (tiered runtime). https://github.com/johnzfitch/specho-v2
- definitelynot.ai: Unicode-security-aware sanitizer (Trojan Source, BiDi, homoglyph defense). https://github.com/johnzfitch/definitelynot.ai

Documentation UX:
- Iconics: semantic icon library (8k+ icons) for professional docs (no emojis). https://github.com/johnzfitch/iconics

---

## Core Skills

Languages:
- Rust (systems, CLIs, correctness-oriented tooling)
- Python (tooling, automation, reproducible experiments)
- JavaScript/TypeScript (web tooling, WASM/WebGPU integration)
- Nix (reproducible systems, deployment as code)

Domains:
- Agent tooling: retrieval, deterministic chunking, verifiable patching, structured tool APIs (MCP)
- Systems performance: mmap, indexing, predictable latency, subprocess correctness
- Security and privacy: defensive design, minimized surface area, explicit threat models
- Infrastructure: NixOS, DNS, TLS automation, containerized services, operational reliability

---

## Infrastructure (Self-Hosted, Sanitized)

I operate production infrastructure on bare metal with a reliability-first and security-first posture:
- Hardware: dedicated bare-metal host (details available on request)
- Network design: multi-IP, multi-subnet redundancy for failure isolation (details available on request)
- DNS: authoritative BIND9 (recursion disabled), rate limiting, constrained zone transfers
- TLS: automated wildcard certificates via DNS-01 using RFC2136 dynamic updates (TSIG)
- Post-quantum layers: hybrid SSH key exchange + WireGuard VPN with Rosenpass PQ key exchange overlay
- Deployments: declarative configuration, atomic upgrades, rollbacks, encrypted secrets and backups

---

## Education

UC Berkeley - Mathematics 

---

## Selected Private Work (Names Only)

- digitaldelusion (NixOS infrastructure and DNS automation)
- cwork (context compiler / skill system for Claude Code workflows; available on request)
- eero (sanitized)
- alienware-monitor (sanitized)
- proxyforge (sanitized)
