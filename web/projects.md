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
- **Why it matters:** Surfaces only the chunks the agent actually needs. Hybrid keyword + semantic retrieval, channeled through the host machine — no remote embedding service, no telemetry, no code leaving the workstation. Agents fight blind in large repos without it.

### [claude-warden](https://github.com/johnzfitch/claude-warden) — 57 stars
*Shell / OpenTelemetry*

- **What:** Defense-in-depth security hooks for Claude Code: SSRF protection, MCP output compression, OTEL tracing, subagent budgets, and quiet-overrides for token-heavy commands.
- **Why it matters:** Secures the agent's operating boundary. Imposes hard limits on network access, subagent nesting, and console output to prevent excessive token consumption and local network exposure. Outbound tracing ensures all model actions are fully auditable.

### [codex-xtreme](https://github.com/johnzfitch/codex-xtreme)
*Rust* (includes [codex-patcher](https://github.com/johnzfitch/codex-patcher))

- **What:** An interactive wizard for producing optimized, patched Codex binaries, backed by a verified patch application engine.
- **Why it matters:** Enables custom Codex builds with verified patch application. Every modification is fully auditable, and no changes go unverified before compilation. The "agent edit-test-build" loop becomes a robust, reviewable software process.

### [burn-plugin](https://github.com/johnzfitch/burn-plugin)
*Claude Code Plugin*

- **What:** Claude Code plugin for the Burn deep learning framework (skills + workflows + evidence-driven references).
- **Why it matters:** Packages deep-learning domain expertise into a portable toolchain plugin. Any developer or agent can leverage the same pre-verified workflows and references, eliminating the need to repeatedly read and parse complex source libraries.

### cwork
*Private (available on request)*

- **What:** A context compiler for Claude Code workflows that composes base capabilities + domain primers + project instructions into a minimal, task-specific context.
- **Why it matters:** Dynamically constructs minimal, high-relevance prompt contexts for each task: base capabilities + domain primer + project context, distilled to the exact minimum needed. This transforms ad-hoc prompt engineering into a reliable, repeatable software step.

### [claude-cowork-linux](https://github.com/johnzfitch/claude-cowork-linux) — 236 stars
*Linux*

- **What:** Run the official Claude Desktop app's Cowork mode natively on Linux using compatibility stubs and a bubblewrap sandbox.
- **Why it matters:** Makes Claude Desktop a first-class Linux application without sacrificing isolation. Avoids a virtual machine layer by sandboxing the application via bubblewrap directly on the host.
- *Unofficial community project; no proprietary Claude code is committed.*

### [Iconics](https://github.com/johnzfitch/iconics)
*Python*

- **What:** Semantic icon library (8k+ icons) designed to replace emojis with consistent PNG icons.
- **Why it matters:** Eight thousand glyphs catalogued by meaning, not by mood. Search by what an icon does; exports are deterministic, so the same query always yields the same icon. Replaces informal emojis with professional, clean iconography.

## MCP Servers (Tool Surfaces for Agents)

### [pyghidra-lite](https://github.com/johnzfitch/pyghidra-lite) — 32 stars
*Python / MCP*

- **What:** Token-efficient MCP server exposing a structured tool API for program analysis workflows (compact output by default, opt-in verbosity).
- **Registry:** Official MCP registry — `io.github.johnzfitch/pyghidra-lite` (v0.1.1, status: active, published 2026-01-29).
- **Why it matters:** Compacts Ghidra's highly verbose output into a token-efficient form so that binary analysis workflows fit comfortably within model context limits. Listed in the official MCP registry for easy integration.

## Systems Performance

### [Triglyph / Triglyphd](https://github.com/johnzfitch/triglyph)
*Rust*

- **What:** Zero-RSS trigram index with custom binary formats + a D-Bus daemon for system-wide search.
- **Why it matters:** Zero-RSS trigram index. Memory-mapped, layout-tuned, daemonized over D-Bus. Costs nothing while idle; answers in milliseconds when called.

### [filearchy](https://github.com/johnzfitch/filearchy)
*Rust (fork)*

- **What:** COSMIC Files fork with io_uring backend and trigram search integration.
- **Why it matters:** COSMIC Files reforged with an io_uring engine and trigram search welded into the panel. Async I/O straight from the kernel; instant filesystem queries from the navigation bar — no spinner, no remote indexer.

## ML / Detection

### [Observatory](https://github.com/johnzfitch/observatory)
*WebGPU*

- **What:** AI image detection suite running 4 models entirely client-side (WebGPU/WASM).
- **Why it matters:** Runs four detection models simultaneously in-browser via WebGPU. Local-first execution ensures privacy and zero latency, allowing users to verify synthetic imagery without uploading files to a remote server.
- **Live:** [look.definitelynot.ai](https://look.definitelynot.ai)

### [SpecHO v2](https://github.com/johnzfitch/specho-v2)
*Python*

- **What:** 161-dimensional linguistic fingerprinting system for AI text detection and model identification (tiered feature pipeline).
- **Why it matters:** Probes 161 linguistic dimensions in tiered passes — only as deep as the verdict requires. Detects AI-authored text and identifies the model behind it without lighting up the whole pipeline for a coin flip.

## Security and Privacy (Defensive)

### [dota](https://github.com/johnzfitch/dota)
*Rust*

- **What:** Post-quantum secrets manager: hybrid ML-KEM-768 + X25519 key encapsulation, Argon2id KDF, SQLCipher (AES-256-CBC) at rest, hardware auth via YubiKey/SoloKey HMAC-SHA1 challenge-response.
- **Why it matters:** Implements post-quantum security for local secrets. Hybrid encryption (ML-KEM-768 + X25519) secures credentials against future decryption risks, with hardware-backed multi-factor authentication (HMAC-SHA1 challenge-response) enforcing physical presence.

### [definitelynot.ai](https://github.com/johnzfitch/definitelynot.ai)
*PHP / JS*

- **What:** Unicode-security-aware text sanitizer with Trojan Source defense, homoglyph mitigation, and BiDi neutralization.
- **Why it matters:** Sanitizes adversarial unicode sequences from incoming text to defend against Trojan Source, BiDi smuggling, and homoglyph attacks before the input is processed or interpreted.

## Infrastructure (Self-Hosted)

### digitaldelusion
*Private*

- **What:** Bare-metal NixOS infrastructure with authoritative DNS, automated wildcard certs (DNS-01 / RFC2136), and post-quantum VPN (WireGuard + Rosenpass).
- **Why it matters:** A fully declarative, bare-metal NixOS infrastructure. Features automated wildcard certificates, authoritative DNS, and VPN tunnels with rapid key rotation, ensuring robust, reproducible, and easily recoverable system deployments.

## Writing / Research (Available on Request)

### AURORA Protocol
*Draft spec + thesis-style artifacts*

- **What:** Design work on robust agent communication in hostile networks (message framing, discovery, encryption-by-default, federation).
- **Why it matters:** Draft spec for agent-to-agent communication in hostile networks. Encryption-by-default, federation-aware, framing built to survive adversarial intermediaries.

## Selected Private Work (Names Only)

- eero (private)
- alienware-monitor (private)
- proxyforge (private)
