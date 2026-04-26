# Ghost in the Codex Machine

> Fixing an "invisible" pre-main regression in OpenAI Codex that silently broke CUDA/MKL environments.

## Executive Summary

This was a performance regression that didn't look like a performance regression.

In release builds, a pre-main hardening routine executed before `main()` and stripped `LD_*` / `DYLD_*` environment variables. For a subset of users (CUDA, Conda/MKL, HPC, custom library layouts), that meant critical dynamic libraries could no longer be discovered inside Codex subprocesses. The downstream effect was dramatic: slow fallback BLAS, CPU fallback for GPU workflows, timeouts, and "Codex feels slow" reports that were difficult to attribute to a single root cause.

I traced the behavior back to the introducing change, wrote a reproduction + benchmark-backed issue, and shipped the upstream fix. The fix is called out in the rust-v0.80.0 release notes with attribution.

## Primary Links (Proof)

- [Issue #8945](https://github.com/openai/codex/issues/8945)
- [Fix PR #8951](https://github.com/openai/codex/pull/8951)
- [Release notes (rust-v0.80.0)](https://github.com/openai/codex/releases/tag/rust-v0.80.0)
- [OpenAI Codex changelog](https://developers.openai.com/codex/changelog)

**Related context:** the PR that introduced always-on pre-main hardening — [PR #4521](https://github.com/openai/codex/pull/4521).

## Timeline (Key Dates)

| Date | Event |
|---|---|
| 2025-09-30 | PR #4521 merges (process hardening executes pre-main in CLI release builds) |
| 2025-10-01 | First affected release ships (rust-v0.43.0) |
| 2025-10-31 | "Ghosts in the Codex Machine" investigation published (concludes there is no single conclusive large issue) |
| 2026-01-08 | I open Issue #8945 with root cause + reproduction + benchmarks |
| 2026-01-09 | Fix merged in PR #8951 |
| 2026-01-09+ | Fix shipped in rust-v0.80.0 (release notes call-out) |

## The Problem (What Users Experienced)

When Codex runs tools (Python, Node, build systems, CLIs), it does so by spawning subprocesses. For dev workflows, the correct baseline is simple: subprocesses should inherit the developer's environment unless a specific policy says otherwise.

When `LD_LIBRARY_PATH` / `DYLD_LIBRARY_PATH` disappears, the failure mode is often not a clean error. Instead, the dynamic linker "finds something else," and performance collapses:

- BLAS libraries fall back to unaccelerated implementations.
- CUDA tooling may fall back to CPU execution.
- Some enterprise/custom libraries fail to load entirely.

## Root Cause (Why This Was a "Ghost")

The stripping happened before `main()` and before most instrumentation/logging was initialized:

- Implemented as a pre-main constructor in release builds (`#[ctor::ctor]`-style behavior).
- Silent by default (no warning when variables were removed).
- Reproduced only on specific environment layouts (non-RPATH installs, legacy Conda, HPC module stacks, custom vendor libraries).
- Users could see `LD_LIBRARY_PATH` set correctly in their shell, but inside `codex exec` it was empty.

## Evidence and Reproduction (How I Proved It)

I approached this like a systems regression:

- Correlated the introducing change with a cluster of "environment disappeared" reports.
- Wrote a minimal reproduction that directly inspects env vars inside Codex tool calls.
- Used benchmarks that isolate library fallback behavior (e.g., matrix multiplication and CUDA library loading).
- Documented results in a way upstream could validate quickly.

## Fix (What Shipped Upstream)

Security hardening is valuable, but in a developer CLI it must not silently rewrite the user's execution environment.

My proposed posture was "opt-in maximum hardening." Upstream shipped a pragmatic equivalent:

- Remove pre-main hardening from the Codex CLI to restore environment inheritance for subprocesses.
- Keep pre-main hardening in the responses API proxy (where it is more appropriate).

Release notes excerpt:

> "Special thanks to @johnzfitch for the detailed investigation and write-up in #8945."

## Measured Impact (Representative)

Performance varies by workload and environment. The key point is the failure mode: stripping env vars can force slow, silent fallbacks.

| Workload | Before | After | Speedup |
|---|---:|---:|---:|
| MKL/BLAS (repro harness) | ~2.71s | ~0.239s | 11.3× |
| CUDA workflows (library discovery / GPU fallback) | 100×–300× slower | restored | varies |

## Why This Matters (Beyond One Bug)

This is the kind of engineering failure that only shows up in real-world environments:

- **Subprocess correctness is a product feature** — tools must behave the same "inside Codex" as they do in the user's terminal.
- **Security controls must be explicit, not surprising.**
- **Performance regressions can hide inside "correct" behavior** when the system silently falls back.
- **Substrate bugs distort everything built on top** — tooling, orchestration, higher-level features all pay the tax.

## What This Demonstrates

- Deep systems debugging (pre-main execution, env inheritance, dynamic linking).
- Performance engineering with hard evidence.
- Security tradeoff reasoning grounded in practical threat models.
- High-quality upstream collaboration: clear issue, reproducible repro, verified fix, shipped release.

## What I Would Add Next (Engineering Hygiene)

- Integration tests asserting env-var inheritance for subprocess execution.
- A documented "secure mode" switch with explicit tradeoffs.
- A debug command to dump the effective execution environment (for users and support).
