#!/usr/bin/env python3
"""Patch federated-nexus.py to use real SHA-256 vectors."""
import sys

path = '/home/ubuntu/.openclaw/workspace/scripts/federated-nexus.py'
with open(path) as f:
    content = f.read()

# 1. Add import
content = content.replace(
    'import json, time, hashlib, math, random, threading',
    'import json, time, hashlib, math, random, threading\nfrom nexus_vectors import tile_to_vector'
)

# 2. Replace global_model init
content = content.replace(
    'self.global_model = [random.gauss(0, 0.1) for _ in range(32)]',
    'self.global_model = tile_to_vector("fleet-global-model-v1", 32)'
)

# 3. Replace client registration vector
content = content.replace(
    '"vector": [random.gauss(0, 0.1) for _ in range(dim)]',
    '"vector": tile_to_vector(f"client:{client_id}", dim)'
)

with open(path, 'w') as f:
    f.write(content)

print("Patched federated-nexus.py successfully")
