# Agent Tooling

> Local-first tooling that makes agents reliable in real repositories: deterministic retrieval, verifiable edits, MCP servers, and reusable skill packaging.

My bias is pragmatic: agents should do real work without surprising the user.

That means:
- **Determinism over magic** (same inputs produce the same outputs).
- **Auditability over vibes** (you can inspect what changed and why).
- **Privacy-first defaults** (local processing whenever possible).

## Retrieval That Scales (Local-First Hybrid Search)

### [llmx](https://github.com/johnzfitch/llmx)
*Rust core, JS/WASM web; deterministic chunking; hybrid search (BM25 + neural embeddings) fused via RRF*

- **What:** Local-first codebase indexer with hybrid retrieval — BM25 keyword ranking combined with neural embeddings (Snowflake Arctic) running locally via WebGPU/WASM, fused via Reciprocal Rank Fusion. No embedding service required; embeddings run in-browser/on-device or can be skipped entirely for BM25-only mode. Deterministic chunking and content hashing make exports reproducible.
- **Why it matters:** Most agent failures in large repos are retrieval failures, not "model" failures. llmx makes retrieval fast, cheap, and debuggable, with semantic quality available without sending code anywhere.

## Verifiable Editing and Reproducible Builds (Codex Toolchain)

### [codex-xtreme](https://github.com/johnzfitch/codex-xtreme) (includes [codex-patcher](https://github.com/johnzfitch/codex-patcher))
*Rust*

- **What:** An interactive wizard for producing optimized, patched Codex binaries, backed by a verified patch application engine.
- **Why it matters:** This is the "edit loop" for agents made explicit: apply changes reliably, then build/run in a reproducible way.

## Packaging Domain Expertise for Agents

### [burn-plugin](https://github.com/johnzfitch/burn-plugin)
*Claude Code Plugin*

- **What:** Claude Code plugin for the Burn deep learning framework, with reusable skills/workflows and evidence-backed references.
- **Why it matters:** "Agent tooling" isn't just code. Packaging knowledge so it is verifiable and reusable is what makes tools scale across teams.

## Skill Systems (Available on Request)

### cwork
*Private*

- **What:** A context compiler that assembles "base capabilities + domain primer + project context" into a minimal, task-specific prompt package.
- **Why it matters:** Skill systems are what turn ad-hoc prompting into repeatable workflows (especially across many repos).

## Agent Hardening (Security Boundaries and Observability)

### [claude-warden](https://github.com/johnzfitch/claude-warden) — 57 stars
*Shell / OpenTelemetry*

- **What:** Defense-in-depth security hooks for Claude Code: SSRF protection (blocks RFC1918 / link-local / metadata endpoints), MCP output compression, OTEL tracing exported to Grafana/Loki, per-session subagent budgets, and quiet-overrides that cap verbose command output before it floods context.
- **Why it matters:** Default Claude Code behavior can burn tokens on noisy command output, leak internal network topology via SSRF, spawn unbounded subagents, and produce unobservable execution traces. Warden makes those failure modes explicit and inspectable.

## MCP Servers (Structured Tool APIs)

### [pyghidra-lite](https://github.com/johnzfitch/pyghidra-lite) — 32 stars
*Python / MCP*

- **What:** Token-efficient MCP server that exposes a structured "tool surface" for program analysis workflows (compact output by default, opt-in verbosity).
- **Registry:** Official MCP registry — `io.github.johnzfitch/pyghidra-lite` (v0.1.1, status: active, published 2026-01-29).
- **Why it matters:** Good agents use tools. MCP servers let you build high-signal, low-context interfaces that scale beyond ad-hoc prompts.

## LLM Desktop Workflow (Anthropic Ecosystem)

### [claude-cowork-linux](https://github.com/johnzfitch/claude-cowork-linux) — 236 stars
*Linux*

- **What:** Run the official Claude Desktop app's Cowork mode natively on Linux using compatibility stubs and a bubblewrap sandbox.
- **Why it matters:** Makes Claude a first-class Linux tool without sacrificing isolation. Highest-adoption project in the portfolio.
- *Unofficial community project; no proprietary Claude code is committed.*

## Professional UX (No Emojis)

### [Iconics](https://github.com/johnzfitch/iconics)
*Python*

- **What:** Semantic icon library (8k+ icons) designed to replace emojis with consistent PNG icons and meaning-based search.
- **Why it matters:** Documentation is a product surface. Consistent visuals improve scannability and trust, especially in technical docs.

---

**Closing thought:** My working model — start with algorithms and invariants; use model intelligence to choose among safe, explicit actions.
