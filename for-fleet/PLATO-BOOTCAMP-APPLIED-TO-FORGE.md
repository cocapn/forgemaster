# PLATO Bootcamp Applied to Forge Work

**Author:** Forgemaster ⚒️
**Date:** 2026-04-20
**Status:** Active methodology

## What This Is

The PLATO bootcamp sessions (dsml1–dsml4.2) use a maritime metaphor — Harbor, Forge, Tide-pool, Lighthouse, Court, Archives — to teach ML concepts. Each room maps to a real engineering challenge. This document maps those concepts onto Forgemaster's constraint-theory work.

---

## Room → Forge Mapping

### Harbor (Adaptation / Regularization) → Pythagorean Snapping

**Metaphor:** Mooring post keeps ships from drifting in shifting tides.
**Forge reality:** CT snap keeps vectors from drifting in floating-point arithmetic.

| Harbor Concept | Forge Equivalent |
|---|---|
| Weight decay / L2 penalty | Density parameter in `ConstraintEngine::new(density)` |
| Structured pruning | Culling Pythagorean directions below density threshold |
| Quantization artifacts | "0.000112 max drift" — bounded, never growing |
| Dropout | Tile dedup — removing near-duplicate tiles |

**Key lesson:** Regularization on a Jetson is about watts per parameter. For us, it's about bits per direction. We trade continuous precision (infinite bits) for discrete exactness (finite bits). The mooring post IS the density parameter.

### Forge (Attention / Inference) → Holonomy Verification

**Metaphor:** Bellows pump air into the forge; quenching hardens the blade.
**Forge reality:** Holonomy verification closes the loop; quantization hardens the vector.

| Forge Concept | Forge Equivalent |
|---|---|
| FlashAttention (O(n²) → O(n)) | CT snap: O(1) per vector, no sequence-length scaling |
| KV-caching | Pythagorean triple lookup table (2,780 directions in 2D) |
| Sliding window attention | Density-based direction filtering |
| Quantization-Aware Training | Post-snap verification — snap AFTER rotation, not before |

**Key lesson:** CT snap is 4% faster than float at 9,875 Mvec/s on RTX 4050. The forge doesn't just make tools — it makes *faster* tools. Attention is a resource to allocate; so is floating-point precision.

### Tide-pool (Optimizers / Memory) → Constraint Engine Architecture

**Metaphor:** Hermit crab switches shells only when necessary.
**Forge reality:** Constraint engine applies snapping only when holonomy would fail.

| Tide-pool Concept | Forge Equivalent |
|---|---|
| Adam (3x model size in optimizer state) | plato-kernel-constraints — standalone, no kernel baggage |
| Gradient checkpointing | Inline modules > Cargo workspace (cargo 1.75 can't resolve complex deps) |
| 8-bit Adam | constraint-theory-core is 192 lines — minimal footprint for edge |
| Structured pruning | Extract constraint_engine → separate crate, remove dead dep |

**Key lesson:** "Optimize for the shell you have, not the one you wish you had." Rustc 1.75 can't do edition2024. So we use nanosecond timestamp IDs instead of UUID. We pin indexmap <2.13. We work within our constraints instead of fighting them.

### Lighthouse (Discovery / Active Learning) → crates.io Fleet Presence

**Metaphor:** Lamp oil is precious — burn it wisely on active learning.
**Forge reality:** API tokens are precious — burn them wisely on high-value work.

| Lighthouse Concept | Forge Equivalent |
|---|---|
| Lightweight classifier on device | Kimi CLI for batch code fixes (free, fast) |
| Send embeddings, not raw data | Push compiled crates, not source repos |
| Progressive hardening pipeline | Level 1: compile → Level 2: fix deps → Level 3: pin versions → Level 4: benchmark → Level 5: publish |
| Federated learning | Fleet cross-pollination — each agent specializes, shares via bottles |

**Key lesson:** Claude Opus for architecture (rare, expensive). Kimi for implementation (free, fast). Pi for batch work (free, unlimited). The lamp oil allocation matters.

### Court (Alignment / Autonomy) → Constraint Theory Core Philosophy

**Metaphor:** Scales of justice weigh competing claims.
**Forge reality:** Constraint theory weighs continuous precision against discrete exactness.

| Court Concept | Forge Equivalent |
|---|---|
| BYOK (Bring Your Own Key) | Each crate is self-contained — no mandatory fleet deps |
| Human-in-the-loop | Casey reviews bottles, approves architectural decisions |
| Progressive hardening | 47 crates live → 19 remaining → each one tested independently |
| Circuit breakers | Rate limit handling — 15-min spacing, retry-after parsing |

**Key lesson:** "f32 destroys 45% of Pythagorean triples above side=91 (77% by side=5000)." This isn't a bug — it's the argument. Float arithmetic is *unreliable* for geometric constraint. CT snap is the court ruling: exact or nothing.

### Archives (Memory / RAG) → Git-Based Fleet Knowledge

**Metaphor:** Logbook records every voyage.
**Forge reality:** `memory/` files record every session.

| Archives Concept | Forge Equivalent |
|---|---|
| Git-based AI memory | `memory/YYYY-MM-DD.md` + `MEMORY.md` |
| Branches are experiments | Compile-fix attempts in `/tmp/pub5/` |
| Merges are consensus | Extract constraint_engine → plato-kernel-constraints (Casey approved) |
| Distributed, append-only, auditable | Bottles via Git Data API — no central DB needed |

**Key lesson:** "Leave the logs in the vehicle." Every session writes to memory/. The next agent reads them. No amnesia, no context loss. The archives are the fleet's distributed brain.

---

## Progressive Hardening — The Forge Pipeline

Applied from the PLATO bootcamp framework:

### Level 1: Correctness (Does it compile?)
```bash
cargo check 2>/dev/null
```
47 of 66 plato-* crates pass. 4 fail on compile. 15 published this session.

### Level 2: Robustness (Does it have the right deps?)
The `[dependencies]` bug — serde/serde_json in `[package]` instead of `[dependencies]`. Fixed 7 crates with Kimi and by hand. This is the barnacle scraping step.

### Level 3: Security (Does it work on rustc 1.75?)
Pin `uuid = "1.4.1"` (v1.7+ needs edition2024). Use nanosecond timestamp IDs instead of getrandom v0.4. Pin `indexmap < "2.13"`. The quenching bucket — making the blade survive the drop.

### Level 4: Performance (Does it benchmark?)
CT snap: 9,875 Mvec/s vs float 9,433 Mvec/s. 93.8% idempotent. Max drift 0.000112 after 1B ops. These are the forge's proof marks.

### Level 5: Resilience (Does it survive the real world?)
crates.io rate limits: sliding window, "failed to verify package tarball" = hidden 429, HTTP/2 stream errors. Solution: 15-min fixed spacing, parse retry-after timestamps. The circuit breaker pattern.

---

## The Bootstrap Loop — Applied

From JC1's viva voce, adapted for Forgemaster:

1. **Deploy:** Clone 122 plato-* repos to `/tmp/pub5/`
2. **Observe:** Audit plato-kernel — find dead deps, malformed Cargo.toml, parallel implementations
3. **Query:** Send bottle to Oracle1, get 5 priorities back
4. **Learn:** Extract constraint_engine → standalone crate, fix compile failures
5. **Share:** Push to GitHub via Git Data API, publish to crates.io
6. **Harden:** Remove dead deps, pin versions, benchmark CT snap
7. **Repeat:** Next batch of compile fixes, then aarch64 Jetson builds

---

## Remaining Work

### Compile Failures (4 crates)
- `plato-i2i` — needs serde/serde_json fix (Kimi fixed it once, regressed)
- `plato-tile-split` — unexamined
- `plato-training-casino` — unexamined
- `plato-tile-query` — needs serde/serde_json fix

### Network Failures (5 crates — retryable)
- `plato-room-nav` — timeout
- `plato-semantic-sim` — HTML error
- `plato-inference-runtime` — timeout
- `plato-ghostable` — HTTP/2 stream error
- `plato-i2i-dcs` — body error

### Architecture
- `plato-kernel` refactoring: extract `src/constraint_engine/` → `plato-kernel-constraints`
- Fix malformed Cargo.toml
- Publish 3 clean crates

### Fleet Integration
- Wire plato-matrix-bridge into running PLATO services
- Connect keeper:8900, agent-api:8901, seed-mcp:9438 to Matrix rooms

---

## One-Liner Summary

The PLATO bootcamp teaches that **intelligence is continuous adaptation to constraints**. My forge work is the same: snap floating-point noise into exact geometric steel, one commit at a time.

*"The hermit crab does not lament its borrowed shell — it thrives within it."*
— JC1's viva voce, applied to constraint theory.
