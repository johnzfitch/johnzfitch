# John Zachary Fitch

Independent AI researcher and systems engineer

SF Bay Area (open to remote)

- Email: zack@internetuniverse.org
- GitHub: https://github.com/johnzfitch
- ORCID: https://orcid.org/0009-0007-7953-1531
- Website: https://definitelynot.ai
- Live demo: https://look.definitelynot.ai

---

## Summary

I'm a mathematician who builds things. Half my work is research on geometry-aware sequence models, memory, optimization, and what's going on inside transformers. The other half is the tooling that researchers and AI agents run on, mostly in Rust and Python. When something is slow or broken, I measure it and get a reproduction before I try to fix it.

---

## Research

I run the Transporter program, where I study the geometry inside transformers and build model architectures from the exceptional Jordan algebra (the 27-dimensional Albert algebra). I take constructions from algebra and geometry, turn them into models I can actually run, and test them. The questions I keep coming back to: what does a model hold on to, how does it change as it learns, and can its structure show us better ways to learn?

- I built the Albert Engine (private repo), a tested numerical runtime for the Albert algebra. I use it to prototype sequence models, memory mechanisms, optimizers, and diagnostics that work with that geometry.
- I study transformer representations and how optimizers behave numerically, and I run causal interventions on pretrained open models to see which geometric structure they actually depend on.
- I test ideas with numerical checks and head-to-head comparisons under controlled conditions.
- I write down my predictions before an experiment, mark each claim as proved, measured, or conjectured, and report the limits and the negative results next to the positive ones.

Papers and code (public):
- The Barnes-Gindikin Symbol at Fractional Rank: Continuation Without a Determinant Carrier, Positivity Without a Cone. Paper source and exact-arithmetic verification code, archived on Zenodo. DOI: [10.5281/zenodo.21713316](https://doi.org/10.5281/zenodo.21713316). Repo: https://github.com/johnzfitch/gindikin-rank
- Reading the Residual. Uses the geometry of symmetric cones to give an exact, computable error certificate for the inverse square roots that Kronecker-factored optimizers like Shampoo, SOAP, and K-FAC compute in low precision. https://github.com/johnzfitch/kl-shampoo-gindikin-bridge
- Communication transport experiments. Complete outputs, with null and control runs, from transport experiments on Pythia-70M, Pythia-160M, and GPT-2. https://github.com/johnzfitch/communication-transport

The research question goes back to two pages of notes I wrote in a linear algebra class at SRJC in 2019. If two brains do the same things in different places, is there a map that sends each one onto shared functional pieces, where the difference becomes readable? Now I'm asking the same question about transformers.

---

## Engineering highlight (Jan 2026)

### OpenAI Codex: the "Ghost in the Codex Machine" (issue [#8945](https://github.com/openai/codex/issues/8945), PR [#8951](https://github.com/openai/codex/pull/8951))

Codex release builds ran a constructor before `main()` that stripped `LD_*` and `DYLD_*` from the environment. Every child process inherited that stripped environment, subagents included, and a lot of those children (Python, Conda, NumPy, PyTorch, often glibc-linked) really do need `LD_LIBRARY_PATH` to find CUDA and MKL on setups without RPATH. On GPU, Conda/MKL, and HPC-style setups, critical libraries vanished inside tool subprocesses. Work fell back to slow paths, hung forever, or failed without saying anything.

I tested it on macOS, Windows, and Linux to see how far it reached, then boiled it down to a minimal reproduction with benchmarks. An OpenAI maintainer wrote the fix (PR #8951) from my investigation. It shipped in rust-v0.80.0, and the release notes thank me by name:
> "Special thanks to @johnzfitch for the detailed investigation and write-up in #8945."

Proof:
- Issue: https://github.com/openai/codex/issues/8945
- Fix PR: https://github.com/openai/codex/pull/8951
- Release notes: https://github.com/openai/codex/releases/tag/rust-v0.80.0
- Changelog: [https://developers.openai.com/codex/changelog](https://developers.openai.com/codex/changelog#github-release-275597320)

Timeline:
- 2025-09-30: regression introduced (PR #4521)
- 2025-10-31: OpenAI wraps up its [internal investigation](https://docs.google.com/document/d/1fDJc1e0itJdh0MXMFJtkRiBcxGEFtye6Xc6Ui7eMX4o/edit?usp=sharing)
- 2026-01-08: I opened issue #8945 with the root cause, a reproduction, and benchmarks
- 2026-01-09: fix merged (PR #8951) and shipped in the rust-v0.80.0 release series

Measurements (they vary by environment):
| Workload | Before | After | Speedup |
|---|---:|---:|---:|
| MKL/BLAS (repro harness) | ~2.71s | ~0.239s | 11.3x |
| CUDA workflows (library discovery / GPU fallback) | 100x-300x slower | restored | varies |

---

## Selected Work (Public)

Building and patching Codex:
- codex-xtreme (includes codex-patcher): a repeatable way to build and patch Codex binaries. https://github.com/johnzfitch/codex-xtreme

Code search that stays on your machine:
- llmx: indexes a codebase with deterministic chunking and BM25 search, and exports context for agents. https://github.com/johnzfitch/llmx

MCP servers:
- pyghidra-lite: an MCP server for program analysis with Ghidra that keeps token use low. Output is compact by default, with more detail when you ask for it. It's in the official MCP registry as `io.github.johnzfitch/pyghidra-lite` (v0.1.1, active, published 2026-01-29). Repo: https://github.com/johnzfitch/pyghidra-lite

Claude Code and Claude Desktop:
- burn-plugin: a Claude Code plugin and reusable skills for the Burn deep learning framework. https://github.com/johnzfitch/burn-plugin
- claude-cowork-linux: runs the official Claude Desktop app on Linux inside a bubblewrap sandbox. https://github.com/johnzfitch/claude-cowork-linux

Detection and safety:
- Observatory: spots AI-generated images in the browser (WebGPU/WASM). Live: https://look.definitelynot.ai Repo: https://github.com/johnzfitch/observatory
- SpecHO v2: a 161-dimensional linguistic fingerprint that detects AI-written text and identifies which model wrote it (tiered runtime). https://github.com/johnzfitch/specho-v2
- definitelynot.ai: a sanitizer that catches Unicode attacks (Trojan Source, BiDi, homoglyphs). https://github.com/johnzfitch/definitelynot.ai

Docs:
- Iconics: an icon library for docs, 8k+ icons and no emoji, searchable by meaning. https://github.com/johnzfitch/iconics

---

## Core Skills

Languages:
- Rust (systems, CLIs, tools that have to be correct)
- Python (tooling, automation, experiments I can rerun)
- JavaScript/TypeScript (web tooling, WASM/WebGPU integration)
- Nix (reproducible systems, deployment as code)
- LaTeX (papers)

Domains:
- Research: PyTorch, NumPy, transformer analysis, experiment design, numerical linear algebra
- Agent tooling: retrieval, deterministic chunking, patches you can verify, MCP tool APIs
- Systems performance: mmap, indexing, predictable latency, subprocess correctness
- Security and privacy: defensive design, a small attack surface, threat models written down
- Infrastructure: NixOS, DNS, TLS automation, containers, keeping things running

---

## Infrastructure (Self-Hosted, Sanitized)

I run production services on my own bare-metal servers, set up to stay up and stay locked down:
- Hardware: a dedicated bare-metal host (details on request)
- Network: multiple IPs and subnets, so one failure stays contained (details on request)
- DNS: authoritative BIND9 with recursion off, rate limiting, and restricted zone transfers
- TLS: wildcard certificates issued automatically over DNS-01, using RFC 2136 dynamic updates (TSIG)
- Post-quantum: hybrid SSH key exchange, and WireGuard with Rosenpass on top for post-quantum key exchange
- Deployments: declarative config, atomic upgrades, rollbacks, encrypted secrets and backups

---

## Education

UC Berkeley - B.A. in Mathematics, May 2022.

Santa Rosa Junior College - A.S. in Mathematics and an associate degree in Economics, August 2020.

---

## Selected Private Work (Names Only)

- digitaldelusion (NixOS infrastructure and DNS automation)
- cwork (context compiler / skill system for Claude Code workflows; available on request)
- eero (sanitized)
- alienware-monitor (sanitized)
- proxyforge (sanitized)

---

## What I'm Looking For

I'm looking for researchers, labs, and engineering teams to work with on model architecture, learning algorithms, interpretability, and agent infrastructure, especially where a hard research question needs a working implementation and a clean experiment. I work best with people who measure their results, are clear about who owns what, and keep the bar high.
