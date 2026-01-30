# John Zachary Fitch

Agent tooling - systems performance - privacy-first infrastructure

SF Bay Area (open to remote)

Email: webmaster@internetuniverse.org
GitHub: https://github.com/johnzfitch
Website: https://definitelynot.ai

---

## Summary

Software engineer with a UC Berkeley mathematics background focused on building production-grade tools for AI agents and the systems they depend on: retrieval, verifiable edits, structured tool APIs, and privacy-first infrastructure. I work across Rust, Python, and the web, with an evidence-first style: measure, reproduce, fix, and ship.

---

## Recent Upstream Impact

### Ghost in the Codex Machine (OpenAI Codex)

I traced and fixed an "invisible" pre-main regression in OpenAI Codex that stripped `LD_*` / `DYLD_*` environment variables in release builds. For CUDA, Conda/MKL, and HPC-style environments, this caused critical libraries to disappear inside tool subprocesses, forcing slow fallback paths.

Proof:
- Issue: https://github.com/openai/codex/issues/8945
- Fix PR: https://github.com/openai/codex/pull/8951
- Credited in release notes: https://github.com/openai/codex/releases/tag/rust-v0.80.0

Representative measurements (vary by environment):
| Workload | Before | After | Speedup |
|---|---:|---:|---:|
| MKL/BLAS (10x 2000x2000 matmul) | 16.3s | 0.306s | 53x |
| CUDA workflows | 11x-300x slower | restored | varies |

What this demonstrates:
- Systems debugging under real-world constraints (pre-main execution, silent failures)
- Performance engineering with reproducible measurement
- Security tradeoff reasoning grounded in practical threat models
- Upstream collaboration: issue -> fix -> verification -> shipped release

---

## Selected Work (Public)

Codex toolchain:
- codex-xtreme: interactive wizard for optimized, patched Codex builds. https://github.com/johnzfitch/codex-xtreme
- codex-patcher: verified patch application engine (byte-span verification, tree-sitter matching). https://github.com/johnzfitch/codex-patcher

Agent retrieval:
- llmx: local-first codebase indexer with BM25 search + semantic chunk exports (Rust/WASM). https://github.com/johnzfitch/llmx

Tool surfaces:
- pyghidra-lite: token-efficient MCP server for tool-driven program analysis with controllable verbosity. https://github.com/johnzfitch/pyghidra-lite

Claude ecosystem:
- burn-plugin: Claude Code plugin + skills for the Burn deep learning framework (evidence-backed references and workflows). https://github.com/johnzfitch/burn-plugin
- claude-cowork-linux: run the official Claude Desktop app on Linux with bubblewrap sandboxing. https://github.com/johnzfitch/claude-cowork-linux

Detection and safety:
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
- Agent tooling: retrieval, deterministic chunking, patch safety, tool-driven workflows
- Systems performance: memory mapping, indexing, predictable latency
- Security and privacy: defensive design, minimized surface area, explicit threat models
- Infrastructure: NixOS, DNS, TLS automation, containerized services, operational reliability

---

## Infrastructure (Self-Hosted, Sanitized)

I operate production infrastructure on bare metal with a reliability-first and security-first posture:
- Dedicated server: Intel Xeon E3-1270v5, 32GB RAM, ~3.6TB SSD (btrfs), NixOS
- Network design: 6 public IPv4 addresses across two separate /24 subnets for redundancy
- DNS: authoritative BIND9 (recursion disabled), rate limiting, constrained zone transfers
- TLS: automated wildcard certificates via DNS-01 using RFC2136 dynamic updates (TSIG)
- Post-quantum layers: hybrid SSH key exchange + WireGuard VPN with Rosenpass PQ key exchange overlay
- Deployments: declarative configuration, atomic upgrades, rollbacks, encrypted secrets

---

## Education

UC Berkeley - Mathematics

---

## Selected Private Work (Names Only)

- digitaldelusion (NixOS infrastructure and DNS automation)
- cwork (context compiler / skill system for Claude Code workflows; available on request)
- eero (sanitized security work)
- alienware-monitor (sanitized)
- proxyforge (sanitized)

