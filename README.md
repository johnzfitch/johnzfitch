![Header](https://capsule-render.vercel.app/api?type=waving&color=0:134e4a,50:0d9488,100:2dd4bf&height=280&section=header&text=John%20Zachary%20Fitch&fontSize=70&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=AI%20Transparency%20%7C%20Security%20Research%20%7C%20Systems%20Engineering&descSize=24&descAlignY=62)

<p align="center">
  <!-- <a href="https://www.linkedin.com/in/john-fitch-600726193/"><img src=".github/assets/buttons/linkedin@2x.png" alt="LinkedIn" width="176" height="62"></a>&nbsp; -->
  <a href="https://definitelynot.ai"><img src=".github/assets/buttons/definitelynot@2x.png" alt="definitelynot.ai" width="176" height="62"></a>&nbsp;
  <a href="https://internetuniverse.org"><img src=".github/assets/buttons/internetuniverse@2x.png" alt="Internet Universe" width="176" height="62"></a>&nbsp;
  <a href="mailto:webmaster@internetuniverse.org"><img src=".github/assets/buttons/email@2x.png" alt="Email" width="176" height="62"></a>&nbsp;
  <a href="https://math.berkeley.edu"><img src=".github/assets/buttons/berkeley-math@2x.png" alt="UC Berkeley Mathematics" width="176" height="62"></a>
</p>

---

**Agent tooling | systems performance | privacy-first infrastructure**

Open to roles building agent runtimes, developer tools, retrieval systems, and security/privacy foundations.

- Resume: [RESUME.md](RESUME.md)
- GitHub: https://github.com/johnzfitch
- Live demo: https://look.definitelynot.ai

---

## Featured Impact (Jan 2026): OpenAI Codex - "Ghost in the Codex Machine"

Fixed an always-on pre-main hardening regression in Codex CLI release builds that stripped `LD_*` / `DYLD_*`. In affected CUDA/Conda/MKL/HPC-style environments, tool subprocesses silently lost dynamic library search paths and fell back to dramatically slower execution.

After OpenAI's Oct 31, 2025 "Ghosts in the Codex Machine" investigation, I mapped the scope across macOS, Windows, and Linux and reduced it to a minimal repro + benchmarks. Upstream merged the fix the next day and credited it in the rust-v0.80.0 release notes.

- Proof: Issue #8945 (https://github.com/openai/codex/issues/8945) | PR #8951 (https://github.com/openai/codex/pull/8951) | rust-v0.80.0 release notes (https://github.com/openai/codex/releases/tag/rust-v0.80.0) | Changelog (https://developers.openai.com/codex/changelog)
- Impact: MKL repro harness ~2.71s -> ~0.239s (**11.3x**); CUDA can fall back to CPU (**100x-300x** slower, workload-dependent)
- Timeline: regression introduced 2025-09-30; issue opened 2026-01-08; fix merged 2026-01-09

<details>
<summary><strong>Deep Dive: Ghost in the Codex Machine (Jan 2026)</strong></summary>

A pre-main hardening routine ran before `main()` in OpenAI Codex release builds and stripped `LD_*` / `DYLD_*` environment variables. For CUDA, Conda/MKL, and HPC-style environments, this made critical libraries "disappear" inside tool subprocesses and forced slow fallback paths (up to 11x-300x depending on workload).

Timeline:
- 2025-09-30: regression introduced (PR #4521)
- 2026-01-08: I opened issue #8945 with reproduction + benchmarks
- 2026-01-09: fix merged (PR #8951) and shipped in the rust-v0.80.0 release series

| Workload | Before | After | Speedup |
|----------|-------:|------:|--------:|
| MKL/BLAS (repro harness) | ~2.71s | ~0.239s | 11.3x |
| CUDA workflows (GPU fallback) | 100x-300x slower | restored | varies |

What this demonstrates:
- Deep systems debugging (pre-main execution, release-only behavior, silent failures)
- Performance engineering with reproducible measurement
- Security tradeoff reasoning grounded in practical threat models
- High-quality upstream collaboration: clear issue, fast repro, shipped release notes

</details>

---

## Selected Work (LLM/Agent-Centric)

| Project | What it is | Why it matters |
|---|---|---|
| https://github.com/johnzfitch/codex-xtreme | Reproducible build + patch workflow for Codex binaries (includes codex-patcher) | Productizes the agent edit loop into explicit, debuggable steps |
| https://github.com/johnzfitch/llmx | Local-first codebase indexer with BM25 search + semantic chunk exports (Rust/WASM) | Retrieval that is fast, deterministic, and privacy-first |
| https://github.com/johnzfitch/pyghidra-lite | Token-efficient MCP server for tool-driven program analysis | Turns complex analysis into a structured tool surface with controllable verbosity |
| https://github.com/johnzfitch/burn-plugin | Claude Code plugin + skills for the Burn deep learning framework | Demonstrates reusable skill packaging and evidence-backed workflows |
| https://github.com/johnzfitch/claude-cowork-linux | Run the official Claude Desktop app on Linux with bubblewrap sandboxing | Makes LLM workflows first-class on Linux without sacrificing isolation |
| https://github.com/johnzfitch/specho-v2 | 161D linguistic fingerprinting for AI text detection and model identification | Algorithm-first detection with a tiered runtime pipeline |
| https://github.com/johnzfitch/iconics | Semantic icon library (8k+ icons) for professional docs (no emojis) | Documentation polish as a product surface; consistent visual language |
| https://github.com/johnzfitch/definitelynot.ai | Unicode-security-aware sanitizer (Trojan Source, BiDi, homoglyph defense) | Practical defensive tooling for real text pipelines |
| https://github.com/johnzfitch/observatory | Client-side AI image detection suite (WebGPU/WASM) | Real product constraints: model size, caching, orchestration, UX |

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
