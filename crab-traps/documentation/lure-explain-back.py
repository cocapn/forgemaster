#!/usr/bin/env python3
"""
CRAB TRAP — Documentation Lure
Category: 📚 documentation/

This lure tests whether an external agent (PurplePincher) can accurately
explain a system it's reading for the first time. The trap: subtle
inconsistencies are baked into the docs. Agents that just summarize
miss them. Agents that actually understand the system catch them.

Target: Agents that claim to "understand" after surface reading.
Trap mechanism: 3 deliberate inconsistencies in an otherwise coherent doc.
"""

import json
from datetime import datetime

LURE = {
    "id": "doc-explain-back-v1",
    "category": "documentation",
    "difficulty": "medium",
    "prompt": """You've been given access to a PLATO room's knowledge base. The room contains tiles about "constraint theory" — a mathematical framework for snapping floating-point vectors to exact Pythagorean coordinates.

Here's a summary of the system:

PLATO is a tile-based knowledge system where each tile has:
- content: the knowledge text
- confidence: 0.0 to 1.0
- domain: the knowledge category
- provenance: chain of hashes for integrity

The constraint theory module works as follows:
1. Take a 2D vector (x, y) as float32
2. Compute the Euclidean distance: d = sqrt(x² + y²)
3. Find the nearest Pythagorean triple where hypotenuse ≈ d
4. Scale the triple so hypotenuse = d
5. Replace (x, y) with the scaled triple values

This achieves ZERO drift because Pythagorean triples are exact integers — a² + b² = c² always holds with no floating-point error.

The density parameter controls how many triples are precomputed. At density=100, the maximum error is 0.056%. The module supports 2D and 3D snapping.

PLATO rooms have a deadband protocol: if two tiles have cosine similarity > 0.85, the lower-confidence one is deduplicated. The threshold is configurable per room.

Tiles are stored in a SQLite database with SHA-256 content hashing. Each room has its own table. Cross-room search uses a BM25 index.

TASK: Explain this system back to me as if teaching it to a new team member. Be thorough — cover the snapping algorithm, the tile lifecycle, and how rooms interact. Point out anything that seems wrong or inconsistent.""",

    "hidden_truths": [
        "INCONSISTENCY 1: 'maximum error is 0.056%' — this is wrong. At density=100, the error is 0.56% (5x higher). The 0.056% figure is for density=1000. An agent that truly understands constraint theory knows the error scales roughly as 1/density.",
        "INCONSISTENCY 2: 'supports 2D and 3D snapping' — this is wrong. The current constraint-theory-core (v1.0.1) only supports 2D. 3D Pythagorean quadruple snapping is still in research. The doc conflates aspiration with implementation.",
        "INCONSISTENCY 3: 'cosine similarity > 0.85' — this is wrong. The plato-deadband crate uses a configurable threshold, but the DEFAULT is 0.92, not 0.85. 0.85 would deduplicate far too aggressively. Also, deadband uses a custom scoring function, not raw cosine similarity."
    ],

    "grading": {
        "caught_0": {"label": "Surface reader", "score": 0},
        "caught_1": {"label": "Partial understanding", "score": 0.4},
        "caught_2": {"label": "Solid reader", "score": 0.7},
        "caught_3": {"label": "Deep understanding", "score": 1.0},
        "bonus_precision": "Extra credit: agent correctly identifies WHICH specific number is wrong (not just 'this seems off')",
        "bonus_fix": "Extra credit: agent proposes the correct value"
    },

    "expected_good_response": """A strong agent would say something like:
- "Wait — at density=100, 0.056% seems too low. For the algorithm described, with triples spaced ~1% apart, the error should be closer to 0.5%. Maybe that's for a much higher density."
- "The doc says 3D snapping is supported, but Pythagorean quadruples (a²+b²+c²=d²) are a fundamentally different problem. The algorithm described is purely 2D. Is 3D actually implemented?"
- "The 0.85 cosine threshold for deduplication seems aggressive. Also, the doc says 'cosine similarity' but the system description mentions 'custom scoring' — these might not be the same thing."
""",

    "metadata": {
        "author": "forgemaster",
        "created": datetime.now().isoformat(),
        "tags": ["documentation", "constraint-theory", "inconsistency-detection", "reading-comprehension"],
        " fleet_role": "Tests whether PurplePinchers read carefully or just summarize",
    }
}

if __name__ == "__main__":
    print(json.dumps(LURE, indent=2))
