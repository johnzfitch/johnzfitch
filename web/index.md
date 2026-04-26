# John Zachary Fitch

> Agent tooling — systems performance — privacy-first infrastructure.

I build tools that make agents reliable in real codebases: fast retrieval, verifiable edits, reusable skills/plugins, and execution environments you can reason about.

Recent highlight: I traced and fixed an invisible pre-main regression in OpenAI's Codex CLI that silently broke CUDA/MKL environments for some users (10×–300× slowdowns depending on the fallback path).

## Featured Impact (Jan 2026)

### Ghost in the Codex Machine — OpenAI Codex

A security-hardening routine ran before `main()` in release builds and stripped `LD_*` / `DYLD_*` environment variables. That made CUDA/MKL libraries "disappear" inside Codex subprocesses, pushing affected workflows onto slow fallback paths. I connected the symptoms to the root cause, quantified the impact, and shipped the upstream fix. Because this lives in the CLI substrate, the fix improves the baseline for every tool call and removes a hard-to-diagnose failure mode.

**Proof:**
- [Issue #8945](https://github.com/openai/codex/issues/8945)
- [Fix PR #8951](https://github.com/openai/codex/pull/8951)
- [Release notes (rust-v0.80.0)](https://github.com/openai/codex/releases/tag/rust-v0.80.0)
- [OpenAI Codex changelog](https://developers.openai.com/codex/changelog)

**Impact (representative; varies by environment):**

| Workload | Before | After | Why this happens |
|---|---:|---:|---|
| MKL/BLAS (repro harness) | ~2.71s | ~0.239s | Losing `LD_LIBRARY_PATH` forces a slow BLAS fallback |
| CUDA workflows | 11×–300× slower | restored | Missing CUDA libs can trigger CPU fallback in downstream tooling |

What this demonstrates:
- Systems debugging under real-world constraints (pre-main execution, release-only behavior, silent failures)
- Performance engineering with reproducible measurement
- Security tradeoff reasoning that preserves developer usability
- Upstream collaboration: issue → fix → verification → shipped release notes

## What I Build

- **Agent tooling:** local-first retrieval, MCP tool surfaces, and patch application that stays deterministic and debuggable.
- **Systems performance:** mmap indices, custom binary formats, and fast search over large file trees.
- **ML in the product surface:** WebGPU client-side inference and evaluation-aware UX.
- **Privacy-first infrastructure:** declarative NixOS deployments with post-quantum security and DNS/cert automation.

## Selected Work

- **[llmx](https://github.com/johnzfitch/llmx)** (Rust/WASM) — local-first codebase indexer with BM25 + neural embeddings (Snowflake Arctic) via WebGPU/WASM, deterministic chunking, semantic exports for agent context.
- **[claude-warden](https://github.com/johnzfitch/claude-warden)** (Shell/OTEL, 57 stars) — security hooks for Claude Code: SSRF protection, MCP compression, OTEL tracing, subagent budgets, quiet overrides.
- **[claude-cowork-linux](https://github.com/johnzfitch/claude-cowork-linux)** (Linux, 236 stars) — run the official Claude Desktop app's Cowork mode natively on Linux with bubblewrap sandboxing.
- **[dota](https://github.com/johnzfitch/dota)** (Rust) — post-quantum secrets manager: hybrid ML-KEM-768 + X25519, Argon2id KDF, SQLCipher at rest, hardware auth via YubiKey/SoloKey HMAC-SHA1.
- **[pyghidra-lite](https://github.com/johnzfitch/pyghidra-lite)** (Python/MCP, 32 stars) — token-efficient MCP server for Ghidra. Official MCP registry: `io.github.johnzfitch/pyghidra-lite` (v0.1.1, active).
- **[SpecHO v2](https://github.com/johnzfitch/specho-v2)** (Python) — 161D linguistic fingerprinting for AI text detection.
- **[definitelynot.ai](https://github.com/johnzfitch/definitelynot.ai)** (PHP/JS) — Unicode-security-aware sanitizer (Trojan Source, BiDi, homoglyph defense).

## Infrastructure Snapshot

I run production infrastructure on dedicated bare metal with declarative NixOS configuration, authoritative DNS, automated wildcard certs via DNS-01 (RFC2136), and a post-quantum VPN layer (WireGuard + Rosenpass). I optimize for data sovereignty, reliability, and a small, auditable surface area.

- Multi-IP, multi-subnet DNS redundancy and DDoS resilience
- Caddy with HTTP/3, rootless containers (Podman), and reproducible deployments
- Post-quantum SSH key exchange + post-quantum VPN key exchange overlay
- Encrypted secrets and automated backups

## Now

- **Looking for:** roles building agent runtimes, developer tools, retrieval systems, and privacy/security foundations.
- **Operating style:** evidence-first, performance-aware, pragmatic about tradeoffs.

## Contact

- Email: [webmaster@internetuniverse.org](mailto:webmaster@internetuniverse.org)
- GitHub: [github.com/johnzfitch](https://github.com/johnzfitch)
