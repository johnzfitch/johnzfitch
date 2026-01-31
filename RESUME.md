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

## Signature Open Source Impact (Jan 2026)

### OpenAI Codex: "Ghost in the Codex Machine" (Issue #8945, PR #8951)

I root-caused and fixed an "invisible" release-only regression in OpenAI Codex where a pre-main constructor ran before `main()` and stripped `LD_*` / `DYLD_*` environment variables. For CUDA, Conda/MKL, and HPC-style setups, this made critical dynamic libraries disappear inside tool subprocesses and forced slow fallback paths.

To map the true scope, I validated behavior across macOS, Windows, and Linux and reduced it to a minimal reproduction + benchmark-backed report.

Proof:
- Issue: https://github.com/openai/codex/issues/8945
- Fix PR: https://github.com/openai/codex/pull/8951
- Release notes call-out: https://github.com/openai/codex/releases/tag/rust-v0.80.0
- Changelog context: https://developers.openai.com/codex/changelog

Timeline:
- 2025-09-30: regression introduced (PR #4521)
- 2026-01-08: I opened issue #8945 with root cause + reproduction + benchmarks
- 2026-01-09: fix merged (PR #8951) and shipped in the rust-v0.80.0 release series

Representative measurements (vary by environment):
| Workload | Before | After | Speedup |
|---|---:|---:|---:|
| MKL/BLAS (repro harness) | ~2.71s | ~0.239s | 11.3x |
| CUDA workflows (library discovery / GPU fallback) | 100x-300x slower | restored | varies |

Release notes excerpt:
> "Special thanks to @johnzfitch for the detailed investigation and write-up in #8945."

What this demonstrates:
- Deep systems debugging (pre-main execution, release-only behavior, silent failures)
- Performance engineering with reproducible measurement
- Security tradeoff reasoning grounded in practical threat models
- Upstream collaboration: clear issue, fast repro, verified fix, shipped release

---

## Selected Work (Public)

Agent build and edit loop:
- codex-xtreme (includes codex-patcher): reproducible build + patch workflow for Codex binaries. https://github.com/johnzfitch/codex-xtreme

Local-first retrieval:
- llmx: codebase indexing with deterministic chunking + BM25 search + exports for agent context. https://github.com/johnzfitch/llmx

Tool surfaces (MCP):
- pyghidra-lite: token-efficient MCP server for tool-driven program analysis (compact by default, opt-in verbosity). https://github.com/johnzfitch/pyghidra-lite

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
- Hardware: Intel Xeon E3-1270v5, 32GB RAM, 2x 1.8TB SSD (btrfs), 10GbE
- Network design: 6 public IPv4 addresses across two separate /24 subnets for redundancy
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
