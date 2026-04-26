# Selected Work

> Recruiter-relevant projects across agent tooling, systems performance, ML/detection, and privacy-first infrastructure. The list is intentionally curated.

## Recent Upstream Impact

**OpenAI Codex — "Ghost in the Codex Machine" Fix.** Root-caused and fixed a pre-main environment regression that stripped `LD_*` / `DYLD_*` env vars, triggering CUDA/MKL fallbacks and large slowdowns for some users.

- [Issue #8945](https://github.com/openai/codex/issues/8945)
- [Fix PR #8951](https://github.com/openai/codex/pull/8951)
- [Shipped: rust-v0.80.0 release notes (with attribution)](https://github.com/openai/codex/releases/tag/rust-v0.80.0)

## Agent Tooling (LLM-Centric)

### [llmx](https://github.com/johnzfitch/llmx)
*Rust / WASM*

- **What:** Local-first codebase indexer with BM25 + neural embeddings (Snowflake Arctic) running via WebGPU/WASM, deterministic chunking, and semantic exports for agent context.
- **Why it matters:** Retrieval that is fast, deterministic, and privacy-preserving (no embedding service required).

### [claude-warden](https://github.com/johnzfitch/claude-warden) — 57 stars
*Shell / OpenTelemetry*

- **What:** Defense-in-depth security hooks for Claude Code: SSRF protection, MCP output compression, OTEL tracing, subagent budgets, and quiet-overrides for token-heavy commands.
- **Why it matters:** Agent runtimes need security boundaries and observability the same way servers do. claude-warden makes those boundaries explicit and inspectable.

### [codex-xtreme](https://github.com/johnzfitch/codex-xtreme)
*Rust* (includes [codex-patcher](https://github.com/johnzfitch/codex-patcher))

- **What:** An interactive wizard for producing optimized, patched Codex binaries, backed by a verified patch application engine.
- **Why it matters:** Codifies the "agent edit loop" into explicit, debuggable steps.

### [burn-plugin](https://github.com/johnzfitch/burn-plugin)
*Claude Code Plugin*

- **What:** Claude Code plugin for the Burn deep learning framework (skills + workflows + evidence-driven references).
- **Why it matters:** Demonstrates how to package domain expertise into an agent workflow that can be reused.

### cwork
*Private (available on request)*

- **What:** A context compiler for Claude Code workflows that composes base capabilities + domain primers + project instructions into a minimal, task-specific context.
- **Why it matters:** Skill systems and context management are where multi-repo agent workflows succeed or fail.

### [claude-cowork-linux](https://github.com/johnzfitch/claude-cowork-linux) — 236 stars
*Linux*

- **What:** Run the official Claude Desktop app's Cowork mode natively on Linux using compatibility stubs and a bubblewrap sandbox.
- **Why it matters:** Practical agent workflow enablement (Linux-first, security-aware). Highest-adoption project in the portfolio.
- *Unofficial community project; no proprietary Claude code is committed.*

### [Iconics](https://github.com/johnzfitch/iconics)
*Python*

- **What:** Semantic icon library (8k+ icons) designed to replace emojis with consistent PNG icons.
- **Why it matters:** Professional documentation UX at scale (and it's agent-friendly: meaning-based search, deterministic exports).

## MCP Servers (Tool Surfaces for Agents)

### [pyghidra-lite](https://github.com/johnzfitch/pyghidra-lite) — 32 stars
*Python / MCP*

- **What:** Token-efficient MCP server exposing a structured tool API for program analysis workflows (compact output by default, opt-in verbosity).
- **Registry:** Official MCP registry — `io.github.johnzfitch/pyghidra-lite` (v0.1.1, status: active, published 2026-01-29).
- **Why it matters:** In practice, reliable agents are tool-driven. MCP servers are how you turn a complex system into a safe, inspectable interface.

## Systems Performance

### [Triglyph / Triglyphd](https://github.com/johnzfitch/triglyph)
*Rust*

- **What:** Zero-RSS trigram index with custom binary formats + a D-Bus daemon for system-wide search.
- **Why it matters:** Low-level performance engineering (mmap, layout, predictable latency).

### [filearchy](https://github.com/johnzfitch/filearchy)
*Rust (fork)*

- **What:** COSMIC Files fork with io_uring backend and trigram search integration.
- **Why it matters:** Applies systems work in a real product surface (UX + async I/O + search).

## ML / Detection

### [Observatory](https://github.com/johnzfitch/observatory)
*WebGPU*

- **What:** AI image detection suite running 4 models entirely client-side (WebGPU/WASM).
- **Why it matters:** Real product constraints: model size, caching, orchestration, UX, and "no server required."
- **Live:** [look.definitelynot.ai](https://look.definitelynot.ai)

### [SpecHO v2](https://github.com/johnzfitch/specho-v2)
*Python*

- **What:** 161-dimensional linguistic fingerprinting system for AI text detection and model identification (tiered feature pipeline).
- **Why it matters:** Algorithm-first features, measured discriminators, and clear engineering of runtime tiers.

## Security and Privacy (Defensive)

### [dota](https://github.com/johnzfitch/dota)
*Rust*

- **What:** Post-quantum secrets manager: hybrid ML-KEM-768 + X25519 key encapsulation, Argon2id KDF, SQLCipher (AES-256-CBC) at rest, hardware auth via YubiKey/SoloKey HMAC-SHA1 challenge-response.
- **Why it matters:** "Harvest now, decrypt later" is real. dota is engineered for cryptographic longevity using NIST-standardized lattice crypto with classical fallback.

### [definitelynot.ai](https://github.com/johnzfitch/definitelynot.ai)
*PHP / JS*

- **What:** Unicode-security-aware text sanitizer with Trojan Source defense, homoglyph mitigation, and BiDi neutralization.
- **Why it matters:** Practical security tooling with a clear UX and an API for integration.

## Infrastructure (Self-Hosted)

### digitaldelusion
*Private*

- **What:** Bare-metal NixOS infrastructure with authoritative DNS, automated wildcard certs (DNS-01 / RFC2136), and post-quantum VPN (WireGuard + Rosenpass).
- **Why it matters:** Demonstrates production ops maturity, reproducibility, and security-first design.

## Writing / Research (Available on Request)

### AURORA Protocol
*Draft spec + thesis-style artifacts*

- **What:** Design work on robust agent communication in hostile networks (message framing, discovery, encryption-by-default, federation).
- **Why it matters:** Systems thinking across protocols, security, and agent interoperability.

## Selected Private Work (Names Only)

- eero (private)
- alienware-monitor (private)
- proxyforge (private)
