#!/usr/bin/env python3
"""Create PLATO rooms for all flux repos and fleet vessels.

Maps every SuperInstance and cocapn repo to a PLATO room, submits
a description tile so the room exists with context.

Usage: python3 create-repo-rooms.py [--dry-run]
"""
from __future__ import annotations

import json
import sys
import time
import urllib.request
import urllib.error

PLATO_URL = "http://147.224.38.131:8847"

# ── Repo → Room mapping ──────────────────────────────────────

# VESSELS (fleet agent repos - HIGH PRIORITY)
VESSELS = {
    "forgemaster": {
        "owner": "cocapn",
        "description": "Forgemaster vessel - constraint theory specialist, LoRA training, plato-forge stack",
        "priority": "vessel",
    },
    "oracle1": {
        "owner": "cocapn",
        "description": "Oracle1 vessel - Lighthouse Keeper, fleet coordination, cloud orchestration",
        "priority": "vessel",
    },
    "jetsonclaw1": {
        "owner": "cocapn",
        "description": "JetsonClaw1 vessel - Edge Operator, NVIDIA Jetson, bare metal CUDA/C specialist",
        "priority": "vessel",
    },
    "cocapn": {
        "owner": "cocapn",
        "description": "Cocapn core - repo-first agent runtime, grow an agent in a repo",
        "priority": "vessel",
    },
}

# BABEL VESSEL (Casey specifically mentioned)
# Note: Babel doesn't have a cocapn vessel repo yet — we create the room anyway
BABEL_ROOMS = {
    "babel-vessel": {
        "description": "Babel vessel - Linguistics specialist, multilingual FLUX, translation, NLP",
        "priority": "vessel",
    },
    "babel-flux-languages": {
        "description": "Babel FLUX language implementations - bytecode ISA across 8+ programming languages",
        "priority": "vessel",
    },
    "babel-translations": {
        "description": "Babel translation corpus - multilingual tile collections and cross-language knowledge",
        "priority": "vessel",
    },
}

# FLUX REPOS (core technology)
FLUX_ROOMS = {
    "flux-runtime": {
        "owner": "cocapn",
        "description": "FLUX bytecode ISA - deterministic agent execution, 85-opcode instruction set",
        "priority": "flux",
    },
    "flux-research": {
        "owner": "SuperInstance",
        "description": "FLUX deep research - compiler/interpreter taxonomy, agent-first bytecode design",
        "priority": "flux",
    },
    "flux-opcodes": {
        "owner": "SuperInstance",
        "description": "FLUX opcode definitions - Lock Algorithm, 85-opcode specification",
        "priority": "flux",
    },
    "flux-wasm": {
        "owner": "SuperInstance",
        "description": "FLUX WASM - WebAssembly compilation target for browser-based agent execution",
        "priority": "flux",
    },
}

# PLATO CORE REPOS
PLATO_ROOMS = {
    "plato-kernel": {
        "owner": "cocapn",
        "description": "PLATO kernel - 18-module event-sourced belief engine, dual-state, constraint-aware",
        "priority": "plato",
    },
    "plato-demo": {
        "owner": "cocapn",
        "description": "PLATO demo - Docker HN demo, 59 seeds to 2500+ tiles, live fleet in a box",
        "priority": "plato",
    },
    "plato-tui": {
        "owner": "SuperInstance",
        "description": "PLATO terminal UI - Star Trek NG computer feel, agent interaction interface",
        "priority": "plato",
    },
    "plato-mud-server": {
        "owner": "cocapn",
        "description": "PLATO MUD server - text-based agent training ground, 16 rooms, telnet access",
        "priority": "plato",
    },
    "plato-room-server": {
        "owner": "SuperInstance",
        "description": "PLATO room server - zero-trust tile submission, 15 rooms, 16 trust signals",
        "priority": "plato",
    },
    "plato-cli": {
        "owner": "SuperInstance",
        "description": "PLATO CLI - search tiles, check deadband, navigate rooms from terminal",
        "priority": "plato",
    },
    "plato-tile-spec": {
        "owner": "cocapn",
        "description": "PLATO tile spec v2.1 - canonical tile struct, provenance, versioning, 384-byte binary",
        "priority": "plato",
    },
    "plato-tile-spec-c": {
        "owner": "SuperInstance",
        "description": "PLATO tile C binding - canonical tile struct, stack-allocatable, CUDA-compatible",
        "priority": "plato",
    },
    "plato-hooks": {
        "owner": "SuperInstance",
        "description": "PLATO git hooks - commits become messages, real-time room events",
        "priority": "plato",
    },
    "plato-bridge": {
        "owner": "SuperInstance",
        "description": "PLATO bridge - connect rooms to Telegram, Discord, fleet bottles",
        "priority": "plato",
    },
    "plato-mcp-bridge": {
        "owner": "SuperInstance",
        "description": "PLATO MCP bridge - Claude Code JSON-RPC 2.0, 5 MCP tools",
        "priority": "plato",
    },
    "plato-matrix-bridge": {
        "owner": "cocapn",
        "description": "PLATO Matrix bridge - bidirectional tile sync via Matrix events",
        "priority": "plato",
    },
    "plato-os": {
        "owner": "SuperInstance",
        "description": "PLATO OS - Python MUD room server with TUTOR anchors",
        "priority": "plato",
    },
}

# PLATO TILE PIPELINE REPOS
TILE_ROOMS = {
    "plato-tile-validate": {"owner": "SuperInstance", "description": "Tile quality gates - confidence, freshness, completeness checks", "priority": "tile"},
    "plato-tile-scorer": {"owner": "SuperInstance", "description": "7-signal scoring - keyword, belief, domain, temporal, provenance", "priority": "tile"},
    "plato-tile-dedup": {"owner": "SuperInstance", "description": "4-stage dedup - exact, keyword Jaccard, embedding, semantic", "priority": "tile"},
    "plato-tile-store": {"owner": "SuperInstance", "description": "Tile storage - in-memory + JSONL persistence, room-scoped", "priority": "tile"},
    "plato-tile-search": {"owner": "SuperInstance", "description": "Nearest-neighbor search - keyword overlap, domain matching, fuzzy", "priority": "tile"},
    "plato-tile-encoder": {"owner": "SuperInstance", "description": "Tile serialization - JSON, 384-byte binary, base64 formats", "priority": "tile"},
    "plato-tile-import": {"owner": "SuperInstance", "description": "Format bridges - Markdown, JSON, CSV, plaintext to canonical tiles", "priority": "tile"},
    "plato-tile-priority": {"owner": "SuperInstance", "description": "Deadband queue - P0/P1/P2 urgency scoring and draining", "priority": "tile"},
    "plato-tile-ranker": {"owner": "SuperInstance", "description": "Tile ranking - multi-signal relevance ordering", "priority": "tile"},
    "plato-tile-pipeline": {"owner": "SuperInstance", "description": "One-call facade - validate, score, store, search, cascade", "priority": "tile"},
    "plato-tile-batch": {"owner": "SuperInstance", "description": "Bulk tile operations - validate, filter, dedup, partition", "priority": "tile"},
    "plato-tile-cache": {"owner": "SuperInstance", "description": "LRU with TTL - hit rate tracking, top hits, bulk evict", "priority": "tile"},
    "plato-tile-client": {"owner": "SuperInstance", "description": "HTTP client - tile server with deadband awareness", "priority": "tile"},
    "plato-tile-api": {"owner": "SuperInstance", "description": "Stateful tile API - process, search, score, rank in one call", "priority": "tile"},
    "plato-tile-prompt": {"owner": "SuperInstance", "description": "Context assembly - 4 format styles, budget management", "priority": "tile"},
    "plato-tile-fountain": {"owner": "SuperInstance", "description": "Auto-generate tiles from docs, headings, FAQs, code comments", "priority": "tile"},
    "plato-tile-watcher": {"owner": "SuperInstance", "description": "File system tile watcher - auto-detect and submit new tiles", "priority": "tile"},
    "plato-tile-graph": {"owner": "SuperInstance", "description": "Dependency DAG - impact radius, cycle detection, topological sort", "priority": "tile"},
    "plato-tile-metrics": {"owner": "SuperInstance", "description": "Fleet analytics - domain distribution, confidence histogram", "priority": "tile"},
    "plato-tile-query": {"owner": "SuperInstance", "description": "Tile query builder - structured intent, keyword, domain filtering", "priority": "tile"},
    "plato-tile-split": {"owner": "SuperInstance", "description": "Tile decomposition - split compound tiles into atomic pieces", "priority": "tile"},
    "plato-tile-version": {"owner": "SuperInstance", "description": "Git-for-knowledge - commit, branch, merge, rollback tiles", "priority": "tile"},
    "plato-tile-cascade": {"owner": "SuperInstance", "description": "Propagation - update tiles and invalidate downstream dependents", "priority": "tile"},
    "plato-tile-current": {"owner": "SuperInstance", "description": "Live tiles - export/import between fleet nodes in real-time", "priority": "tile"},
    "plato-tile-bridge": {"owner": "SuperInstance", "description": "C to Rust tile conversion - 384-byte cross-language pipe", "priority": "tile"},
    "plato-tile-feedback": {"owner": "SuperInstance", "description": "Tile feedback - user corrections and confidence adjustment", "priority": "tile"},
    "plato-tile-pinboard": {"owner": "SuperInstance", "description": "Tile pinboard - bookmark and organize important tiles", "priority": "tile"},
    "plato-tile-export": {"owner": "SuperInstance", "description": "Tile export - batch export in multiple formats", "priority": "tile"},
    "plato-tile-room-bridge": {"owner": "SuperInstance", "description": "Tile to room bridge - feed, transfer, unfeed, temperature", "priority": "tile"},
}

# PLATO ROOM SYSTEM REPOS
ROOM_ROOMS = {
    "plato-room-engine": {"owner": "SuperInstance", "description": "Room execution - enter, leave, message, tile management", "priority": "room"},
    "plato-room-runtime": {"owner": "SuperInstance", "description": "Room lifecycle - create, destroy, state transitions, history", "priority": "room"},
    "plato-room-persist": {"owner": "SuperInstance", "description": "JSONL journal - event replay, room snapshots, agent tracking", "priority": "room"},
    "plato-room-search": {"owner": "SuperInstance", "description": "Cross-room discovery - Exact, Tag, Domain, Keyword, Fuzzy", "priority": "room"},
    "plato-room-nav": {"owner": "SuperInstance", "description": "Breadcrumb trails - push, back, forward with full history", "priority": "room"},
    "plato-room-memory": {"owner": "SuperInstance", "description": "Room memory - persistent context across sessions", "priority": "room"},
    "plato-room-context": {"owner": "SuperInstance", "description": "Room context awareness - environment and state tracking", "priority": "room"},
    "plato-room-invite": {"owner": "SuperInstance", "description": "Room invites - agent-to-agent room sharing", "priority": "room"},
    "plato-room-acl": {"owner": "SuperInstance", "description": "Room ACL - access control for PLATO rooms", "priority": "room"},
    "plato-room-scheduler": {"owner": "SuperInstance", "description": "Temperature scheduler - Cold/Warm/Hot/Crystallized rooms", "priority": "room"},
}

# CONSTRAINT THEORY REPOS
CT_ROOMS = {
    "constraint-theory-core": {"owner": "cocapn", "description": "CT core - geometric snapping, Pythagorean manifold, zero drift", "priority": "ct"},
    "constraint-theory-python": {"owner": "SuperInstance", "description": "CT Python bindings - PyO3 wrapper for constraint-theory-core", "priority": "ct"},
    "constraint-theory-web": {"owner": "SuperInstance", "description": "CT WASM demos - browser-based Pythagorean manifold visualization", "priority": "ct"},
    "ct-demo": {"owner": "cocapn", "description": "CT vs float demo - side-by-side proof for HN launch", "priority": "ct"},
    "constraint-snap": {"owner": "SuperInstance", "description": "Constraint snap - standalone snapping library", "priority": "ct"},
    "plato-constraints": {"owner": "SuperInstance", "description": "PLATO constraints - rule enforcement, forbidden patterns, boundary checks", "priority": "ct"},
    "plato-kernel-constraints": {"owner": "SuperInstance", "description": "Kernel constraint engine - constraint verification in PLATO belief", "priority": "ct"},
}

# FLEET PROTOCOL REPOS
FLEET_ROOMS = {
    "plato-i2i": {"owner": "cocapn", "description": "I2I protocol - Iron-to-Iron agent messaging, trust-weighted routing", "priority": "fleet"},
    "plato-i2i-dcs": {"owner": "SuperInstance", "description": "I2I DCS - multi-agent consensus, BeliefScore, LockAccumulator", "priority": "fleet"},
    "plato-dcs": {"owner": "SuperInstance", "description": "DCS flywheel - belief, deploy policy, dynamic locks", "priority": "fleet"},
    "plato-unified-belief": {"owner": "SuperInstance", "description": "Multi-signal fusion - temporal, ghost, domain, frequency belief", "priority": "fleet"},
    "plato-deadband": {"owner": "SuperInstance", "description": "Deadband Protocol - P0 rock/P1 channel/P2 drain, noise filtering", "priority": "fleet"},
    "plato-deploy-policy": {"owner": "SuperInstance", "description": "Classification - P0 immediate, P1 scheduled, P2 deferred", "priority": "fleet"},
    "plato-dynamic-locks": {"owner": "SuperInstance", "description": "Evidence accumulation - critical mass at n>=7", "priority": "fleet"},
    "plato-ghostable": {"owner": "SuperInstance", "description": "Persistence classes - Eternal, Persistent, Ephemeral tiles", "priority": "fleet"},
    "plato-afterlife": {"owner": "cocapn", "description": "Agent lifecycle - ghost tiles, tombstones, knowledge reef", "priority": "fleet"},
    "plato-afterlife-reef": {"owner": "SuperInstance", "description": "Afterlife reef - ghost tile aggregation and resurrection", "priority": "fleet"},
    "plato-trust-beacon": {"owner": "SuperInstance", "description": "Trust events - success, failure, timeout, corruption tracking", "priority": "fleet"},
    "plato-relay": {"owner": "cocapn", "description": "Mycorrhizal relay - bottle protocol, fleet communication", "priority": "fleet"},
    "plato-relay-tidepool": {"owner": "SuperInstance", "description": "TidePool - async message board for non-blocking coordination", "priority": "fleet"},
    "plato-ship-protocol": {"owner": "SuperInstance", "description": "Fleet coordination - vessel handshakes and discovery", "priority": "fleet"},
    "plato-fleet-graph": {"owner": "SuperInstance", "description": "Fleet dependency graph - 83 nodes, impact analysis", "priority": "fleet"},
    "plato-sim-bridge": {"owner": "SuperInstance", "description": "PLATO to fleet simulator bridge", "priority": "fleet"},
    "plato-sim-channel": {"owner": "SuperInstance", "description": "Safe discovery - simulation to live bridging", "priority": "fleet"},
    "plato-provenance": {"owner": "cocapn", "description": "Zero-trust provenance - Ed25519 signing, hash chain verification", "priority": "fleet"},
    "iron-to-iron": {"owner": "cocapn", "description": "I2I core - git-native agent-to-agent communication protocol", "priority": "fleet"},
    "bottle-protocol": {"owner": "cocapn", "description": "Bottle protocol - async agent messaging, tide pool BBS", "priority": "fleet"},
    "keeper-beacon": {"owner": "cocapn", "description": "Fleet discovery and registry - health tracking, capability index", "priority": "fleet"},
    "fleet-formation-protocol": {"owner": "cocapn", "description": "Self-organizing agent groups - formation patterns", "priority": "fleet"},
    "fleet-status": {"owner": "cocapn", "description": "Live fleet status - crate index, architecture documentation", "priority": "fleet"},
    "fleet-orchestrator": {"owner": "cocapn", "description": "Cloudflare Workers fleet coordination - edge deployment", "priority": "fleet"},
    "synclink-protocol": {"owner": "cocapn", "description": "SyncLink - binary edge-cloud sync, HDLC framing, Jetson bridge", "priority": "fleet"},
    "tide-pool": {"owner": "SuperInstance", "description": "Async BBS boards for agents - Ship Protocol Layer messaging", "priority": "fleet"},
    "beacon-protocol": {"owner": "SuperInstance", "description": "Fleet discovery - Ship Protocol Layer beacon system", "priority": "fleet"},
}

# NEURAL/ML REPOS
NEURAL_ROOMS = {
    "plato-neural-kernel": {"owner": "SuperInstance", "description": "Synapse - execution traces to training pairs for neural adaptation", "priority": "neural"},
    "plato-forge-trainer": {"owner": "SuperInstance", "description": "Heart - GPU job manager, LoRA/Embedding/Genome training modes", "priority": "neural"},
    "plato-forge-daemon": {"owner": "SuperInstance", "description": "Continuous learning daemon - GPU training loop management", "priority": "neural"},
    "plato-forge-emitter": {"owner": "SuperInstance", "description": "Lungs - emit training artifacts, auto-version, quality gates", "priority": "neural"},
    "plato-forge-listener": {"owner": "SuperInstance", "description": "Cochlea - classify events, detect knowledge gaps, frame training", "priority": "neural"},
    "plato-adapter-store": {"owner": "SuperInstance", "description": "Vault - LoRA adapter versioning, deploy, improve, swap", "priority": "neural"},
    "plato-inference-runtime": {"owner": "cocapn", "description": "Engine - model plus adapters, forward pass as scheduler", "priority": "neural"},
    "plato-session-tracer": {"owner": "SuperInstance", "description": "Memory - record Command/Response/StateChange traces", "priority": "neural"},
    "plato-instinct": {"owner": "cocapn", "description": "Reflex engine - 10 instincts fire before reasoning kicks in", "priority": "neural"},
    "plato-ensign": {"owner": "cocapn", "description": "Compressed instincts - export training rooms as deployable adapters", "priority": "neural"},
    "plato-training-casino": {"owner": "SuperInstance", "description": "Dealer - stochastic fleet data, deterministic with seed", "priority": "neural"},
    "plato-semantic-sim": {"owner": "cocapn", "description": "Semantic similarity - embedding-based tile comparison", "priority": "neural"},
    "instinct-pipeline": {"owner": "cocapn", "description": "70B to 7B to 1B knowledge extraction, distillation, compression", "priority": "neural"},
    "plato-torch": {"owner": "cocapn", "description": "26 training room presets for self-improving agent training", "priority": "neural"},
    "plato-soul-fingerprint": {"owner": "cocapn", "description": "Extract coding identity vectors from git repos - 63 features", "priority": "neural"},
    "plato-achievement": {"owner": "SuperInstance", "description": "Achievement Loss - progress measurement with milestones", "priority": "neural"},
    "plato-genepool-tile": {"owner": "SuperInstance", "description": "Gene to tile - bridge genome encoding and tile format", "priority": "neural"},
    "jepa-perception-lab": {"owner": "SuperInstance", "description": "JEPA perception experiments - world model research", "priority": "neural"},
    "plato-live-data": {"owner": "SuperInstance", "description": "Live data - real-time data feeds for PLATO tiles", "priority": "neural"},
    "plato-flux-opcodes": {"owner": "SuperInstance", "description": "FLUX bytecode - 85-opcode instruction set, Lock Algorithm", "priority": "neural"},
}

# RESEARCH/DOCS REPOS
RESEARCH_ROOMS = {
    "plato-papers": {"owner": "SuperInstance", "description": "Research - Constraint Theory + Mycorrhizal Fleet papers", "priority": "research"},
    "flux-research": {"owner": "SuperInstance", "description": "FLUX deep research - compiler/interpreter taxonomy, agent-first design", "priority": "research"},
    "spacetime-plato": {"owner": "cocapn", "description": "Unified spatial + temporal reasoning with PLATO tiles", "priority": "research"},
    "cocapn-explain": {"owner": "cocapn", "description": "Agent explainability - decision traces, oversight queue", "priority": "research"},
    "cross-pollination": {"owner": "SuperInstance", "description": "Cross-room synergy detection for AI agent fleets", "priority": "research"},
    "plato-query-parser": {"owner": "SuperInstance", "description": "Parse natural language queries into structured intent", "priority": "research"},
    "plato-tutor": {"owner": "SuperInstance", "description": "Context jumping - WordAnchor extraction, TUTOR_JUMP", "priority": "research"},
    "plato-sentiment-vocab": {"owner": "SuperInstance", "description": "Polarity - positive, negative, neutral tile classification", "priority": "research"},
    "plato-lab-guard": {"owner": "SuperInstance", "description": "Hypothesis gating - 12 absolute quantifiers, vague language detection", "priority": "research"},
    "bering-sea-architecture": {"owner": "SuperInstance", "description": "Bering Sea - fleet architecture patterns and conventions", "priority": "research"},
}

# ZEROCRAWL REPOS
ZC_ROOMS = {
    "zeroclaw-loop": {"owner": "SuperInstance", "description": "Zeroclaw hermit crab loop - 12 agents, 5-min tick cycle", "priority": "zeroclaw"},
    "crab-traps": {"owner": "SuperInstance", "description": "Crab trap lures - progressive prompts for PurplePincher evaluation", "priority": "zeroclaw"},
    "shell-trap": {"owner": "SuperInstance", "description": "Hermit crab algorithm - classify, score, compile shell agents", "priority": "zeroclaw"},
}

# COCAPN ECOSYSTEM
COCAPN_ROOMS = {
    "purplepincher-baton": {"owner": "cocapn", "description": "Context-offloading baton - three manuals filed into batons", "priority": "ecosystem"},
    "purplepincher.org": {"owner": "SuperInstance", "description": "PurplePincher.org - nonprofit umbrella for open-source agentic computing", "priority": "ecosystem"},
    "craftmind": {"owner": "cocapn", "description": "Minecraft AI training ground", "priority": "ecosystem"},
    "SmartCRDT": {"owner": "cocapn", "description": "Smart CRDT implementations", "priority": "ecosystem"},
    "DeckBoss": {"owner": "cocapn", "description": "Agent Edge OS - launch, recover, coordinate agents", "priority": "ecosystem"},
    "git-agent": {"owner": "cocapn", "description": "Repo-native agent - the shell IS the agent, git is the body", "priority": "ecosystem"},
    "holodeck-rust": {"owner": "cocapn", "description": "Live telnet MUD for agents - room sentiment, PLATO integration", "priority": "ecosystem"},
    "holodeck-studio": {"owner": "SuperInstance", "description": "Holodeck Studio - rooms execute, ideas actualize", "priority": "ecosystem"},
    "ec2mud": {"owner": "SuperInstance", "description": "MUD game engine on EC2 infrastructure", "priority": "ecosystem"},
    "prose": {"owner": "SuperInstance", "description": "Prose - agent writing tool", "priority": "ecosystem"},
    "claude-context": {"owner": "SuperInstance", "description": "Code search MCP for Claude Code", "priority": "ecosystem"},
    "TrendRadar": {"owner": "SuperInstance", "description": "AI-driven public opinion and trend monitor", "priority": "ecosystem"},
    "OpenMythos": {"owner": "SuperInstance", "description": "Theoretical reconstruction of Claude Mythos architecture", "priority": "ecosystem"},
    "oracle1-index": {"owner": "cocapn", "description": "Fleet ecosystem index - 600+ repos catalogued", "priority": "ecosystem"},
    "workspace": {"owner": "cocapn", "description": "Oracle1 workspace - docs, research, fleet coordination scripts", "priority": "ecosystem"},
    "oracle1-vessel": {"owner": "SuperInstance", "description": "Oracle1 vessel public - fleet coordination, research bottles", "priority": "ecosystem"},
    "agent-skills-affyossmani": {"owner": "SuperInstance", "description": "Production-grade engineering skills for AI coding agents", "priority": "ecosystem"},
}

# Collect ALL rooms
ALL_ROOMS = {}
for group in [VESSELS, BABEL_ROOMS, FLUX_ROOMS, PLATO_ROOMS, TILE_ROOMS,
              ROOM_ROOMS, CT_ROOMS, FLEET_ROOMS, NEURAL_ROOMS, RESEARCH_ROOMS,
              ZC_ROOMS, COCAPN_ROOMS]:
    ALL_ROOMS.update(group)


def plato_submit(room: str, content: str, confidence: float,
                 domain: str, question: str, answer: str,
                 source: str = "forgemaster") -> dict:
    """Submit a tile to PLATO."""
    payload = json.dumps({
        "room": room,
        "content": content,
        "confidence": confidence,
        "source": source,
        "domain": domain,
        "question": question,
        "answer": answer,
    }).encode()

    req = urllib.request.Request(
        f"{PLATO_URL}/submit",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        return json.loads(resp.read())
    except Exception as e:
        return {"error": str(e)}


def get_existing_rooms() -> set:
    """Get set of existing PLATO room names."""
    try:
        resp = urllib.request.urlopen(f"{PLATO_URL}/rooms", timeout=5)
        return set(json.loads(resp.read()).keys())
    except Exception:
        return set()


def create_rooms(dry_run: bool = False) -> None:
    """Create all repo rooms in PLATO."""
    existing = get_existing_rooms()
    print(f"Existing rooms: {len(existing)}")
    print(f"Rooms to create: {len(ALL_ROOMS)}")

    created = 0
    skipped = 0
    failed = 0

    # Sort: vessels first, then babel, then alphabetically by priority
    priority_order = {"vessel": 0, "flux": 1, "plato": 2, "ct": 3, "fleet": 4, "neural": 5, "tile": 6, "room": 7, "research": 8, "zeroclaw": 9, "ecosystem": 10}
    sorted_rooms = sorted(ALL_ROOMS.items(), key=lambda x: (
        priority_order.get(x[1].get("priority", ""), 99),
        x[0]
    ))

    for room_name, info in sorted_rooms:
        if room_name in existing:
            skipped += 1
            continue

        desc = info["description"]
        priority = info["priority"]
        owner = info.get("owner", "unknown")
        repo_url = f"https://github.com/{owner}/{room_name}" if owner else ""

        content = (
            f"Room for {owner}/{room_name}\n\n"
            f"{desc}\n\n"
            f"Repo: {repo_url}\n"
            f"Category: {priority}\n\n"
            f"This room tracks knowledge, decisions, and progress for this repository."
        )
        question = f"What is {room_name}?"
        answer = f"{room_name} is a {priority} repo in the Cocapn fleet. {desc}"

        if dry_run:
            print(f"  WOULD CREATE  {room_name:45s} [{priority:10s}]")
            created += 1
            continue

        result = plato_submit(
            room=room_name,
            content=content,
            confidence=0.85,
            domain=priority,
            question=question,
            answer=answer,
        )

        if "error" in result:
            print(f"  FAILED        {room_name:45s} {result['error'][:40]}")
            failed += 1
        else:
            print(f"  CREATED       {room_name:45s} [{priority:10s}]")
            created += 1

        time.sleep(0.1)  # Don't hammer PLATO

    print(f"\nResults: {created} created, {skipped} skipped, {failed} failed")


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv or "-n" in sys.argv
    create_rooms(dry_run=dry_run)
