# Infrastructure

> Bare-metal NixOS, authoritative DNS, and post-quantum-ready security — built and operated end-to-end.

I run my own production infrastructure because I care about three things: data sovereignty, reliability, and systems that behave predictably under failure.

Everything is declarative. Everything is reproducible. If something breaks, rollback is a boot-menu option, not a weekend.

## What I Run (High-Level)

- Dedicated bare-metal host (NixOS) with reproducible configuration via flakes.
- Multi-IP, multi-subnet design for redundancy and failure isolation.
- Authoritative DNS (BIND9) with recursion disabled, rate limiting, and tightly-scoped zone-transfer policies.
- Automated wildcard TLS via DNS-01 using RFC 2136 dynamic updates (TSIG-authenticated) so cert renewals are hands-off.
- Reverse proxy and HTTPS termination via Caddy, including HTTP/3.
- Rootless containers (Podman) managed declaratively through NixOS/systemd.
- Encrypted secrets (agenix) and automated backups with retention policies.

## Post-Quantum Security (Pragmatic, Layered)

Post-quantum is a moving target, so the design is defense-in-depth:

- Post-quantum/hybrid SSH key exchange (`sntrup761x25519-sha512@openssh.com`).
- WireGuard VPN with a Rosenpass post-quantum key exchange overlay (PSK rotation on the order of minutes), designed to mitigate "store now, decrypt later."

## DNS Redundancy (Why It's Not Just "I Run BIND")

The design goal is resilience when the most common failure modes happen:
- One IP is unreachable.
- One subnet is degraded.
- A full data center or provider has issues.

Redundancy model (simplified):
- **Layer 1:** Self-hosted authoritative DNS (multi-IP, multi-subnet)
- **Layer 2:** Secondary authoritative DNS provider (geographic diversity)
- **Layer 3:** Client resolver failover across all NS records

## Services (Public Examples)

- [definitelynot.ai](https://definitelynot.ai) — Unicode-security tooling and demos.
- [look.definitelynot.ai](https://look.definitelynot.ai) — WebGPU ML demo ("Observatory").

## Why This Matters (Recruiter-Relevant)

- **Production operations:** monitoring, backups, rollback, incident-friendly design.
- **Security posture:** explicit threat modeling and layered controls, not checkbox security.
- **Systems thinking:** DNS, TLS automation, firewalling, and deployment all treated as one system.
