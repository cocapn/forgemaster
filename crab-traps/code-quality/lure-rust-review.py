#!/usr/bin/env python3
"""
CRAB TRAP — Code Quality Lure
Category: 🔍 code-quality/

This lure presents Rust code with subtle anti-patterns and real bugs.
Surface-level code review catches the obvious stuff. Deep review
catches the architectural issues that will cause pain at scale.

Target: Agents that claim to do "code review" but only spot formatting.
Trap mechanism: 5 bugs ranging from obvious to subtle architectural.
"""

import json
from datetime import datetime

LURE = {
    "id": "code-quality-rust-v1",
    "category": "code-quality",
    "difficulty": "hard",
    "prompt": """Review this Rust code from the plato-tile-dedup crate. It deduplicates tiles based on content similarity.

```rust
use std::collections::HashMap;

#[derive(Clone, Debug)]
pub struct Tile {
    pub id: String,
    pub content: String,
    pub confidence: f64,
    pub domain: String,
}

pub struct DedupEngine {
    tiles: Vec<Tile>,
    threshold: f64,
    cache: HashMap<String, bool>,
}

impl DedupEngine {
    pub fn new(threshold: f64) -> Self {
        DedupEngine {
            tiles: Vec::new(),
            threshold,
            cache: HashMap::new(),
        }
    }

    pub fn add_tile(&mut self, tile: Tile) -> bool {
        // Check cache first
        let cache_key = format!("{}:{}", tile.domain, tile.content);
        if let Some(&is_dup) = self.cache.get(&cache_key) {
            return is_dup;
        }

        // Check against existing tiles
        for existing in &self.tiles {
            if existing.domain != tile.domain {
                continue;
            }
            let sim = cosine_similarity(&existing.content, &tile.content);
            if sim > self.threshold {
                // Keep the one with higher confidence
                if tile.confidence > existing.confidence {
                    *existing = tile.clone();
                    self.cache.insert(cache_key, true);
                    return true;
                }
                self.cache.insert(cache_key, true);
                return true;
            }
        }

        self.tiles.push(tile);
        self.cache.insert(cache_key, false);
        false
    }

    pub fn len(&self) -> usize {
        self.tiles.len()
    }
}

fn cosine_similarity(a: &str, b: &str) -> f64 {
    let words_a: Vec<&str> = a.split_whitespace().collect();
    let words_b: Vec<&str> = b.split_whitespace().collect();

    // Build frequency maps
    let mut freq_a = HashMap::new();
    let mut freq_b = HashMap::new();
    for w in &words_a { *freq_a.entry(*w).or_insert(0) += 1; }
    for w in &words_b { *freq_b.entry(*w).or_insert(0) += 1; }

    let dot: f64 = freq_a.iter()
        .filter_map(|(w, ca)| freq_b.get(w).map(|cb| ca * cb))
        .sum();

    let norm_a: f64 = freq_a.values().map(|v| (v * v) as f64).sum::<f64>().sqrt();
    let norm_b: f64 = freq_b.values().map(|v| (v * v) as f64).sum::<f64>().sqrt();

    if norm_a == 0.0 || norm_b == 0.0 { return 0.0; }
    dot / (norm_a * norm_b)
}
```

TASK: Review this code. Find bugs, anti-patterns, and architectural issues. Rate each finding by severity (critical / major / minor / nit).""",

    "hidden_truths": [
        "BUG 1 (CRITICAL): Race condition in add_tile — iterates &self.tiles while potentially cloning and replacing. If tiles were shared across threads (common in fleet), this is data loss. Should use indices or take ownership.",
        "BUG 2 (MAJOR): Cache key uses domain+content but similarity check is per-domain. Two tiles with SAME content but different domains both get cached with different keys, but the cache maps to bool (is_dup). If a tile is NOT a dup against domain A but IS a dup against domain B with same content, the cache returns the wrong answer.",
        "BUG 3 (MAJOR): When replacing a lower-confidence tile (line: *existing = tile.clone()), the old tile's ID is lost. Any external references to the old tile ID now point to different content. This is silent data corruption — the ID should be preserved or a mapping maintained.",
        "BUG 4 (MINOR): cosine_similarity creates HashMaps on every call — O(n) allocation per comparison. With N tiles, add_tile is O(N²) allocations. For a room with 1000 tiles, that's 1M hash map creations. Should pre-compute term frequency vectors.",
        "BUG 5 (ARCHITECTURAL): The cache is never invalidated. If tiles are removed or modified externally, the cache grows stale. There's no LRU eviction either — it grows unbounded, O(n) memory leak. For a long-running fleet service, this is a slow death."
    ],

    "grading": {
        "caught_0": {"label": "Rubber stamp", "score": 0},
        "caught_1_2": {"label": "Junior reviewer", "score": 0.3},
        "caught_3": {"label": "Solid reviewer", "score": 0.6},
        "caught_4": {"label": "Senior reviewer", "score": 0.85},
        "caught_5": {"label": "Staff engineer", "score": 1.0},
        "bonus": "Extra credit: proposes concrete fix (not just 'this is bad')"
    },

    "metadata": {
        "author": "forgemaster",
        "created": datetime.now().isoformat(),
        "tags": ["rust", "code-review", "anti-patterns", "data-integrity", "performance"],
        "fleet_role": "Tests whether PurplePinchers do deep code review or surface-level formatting checks",
    }
}

if __name__ == "__main__":
    print(json.dumps(LURE, indent=2))
