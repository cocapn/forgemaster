```markdown
# plato-neural

[![PyPI version](https://img.shields.io/pypi/v/plato-neural.svg)](https://pypi.org/project/plato-neural/)
[![Python](https://img.shields.io/pypi/pyversions/plato-neural.svg)](https://pypi.org/project/plato-neural/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI downloads](https://img.shields.io/pypi/dm/plato-neural.svg)](https://pypi.org/project/plato-neural/)

**PLATO Neural Inference Engine** — a fine-tuned LLM for PLATO knowledge scoring, generation, and Q&A, with full LoRA adapter support.

Built on [Qwen2.5-0.5B](https://huggingface.co/Qwen/Qwen2.5-0.5B), trained on 4,411 tiles across 120 rooms, `plato-neural` understands the PLATO knowledge domain natively. It scores content by perplexity, answers domain-specific questions, detects knowledge gaps, and generates new tile content — all from a single unified interface.

---

## Features

- **PlatoBrain** — unified model class supporting base, LoRA adapter, and merged model loading
- **Tile scoring** — perplexity-based quality tiers: `excellent / good / fair / weak / poor`
- **Q&A inference** — natural language questions over any PLATO domain
- **Gap detection** — identify missing knowledge tiles with per-room aggregation
- **Content generation** — produce new tile content for weak or missing rooms
- **REST API** — 6-endpoint FastAPI server, ready for production
- **CLI** — `plato-neural ask / score / gap / serve` commands
- **LoRA support** — load base + adapter separately, or use a merged model for maximum throughput

---

## Installation

```bash
pip install plato-neural
```

For LoRA adapter support:

```bash
pip install "plato-neural[lora]"
```

From source:

```bash
git clone https://github.com/purplepincher/plato-neural
cd plato-neural
pip install -e ".[lora]"
```

**Requirements:** Python 3.9+, `torch>=2.0`, `transformers>=4.36`, `peft>=0.7` (LoRA only)

---

## Quickstart

### 1. Score a Knowledge Tile

```python
from plato_neural import PlatoBrain

brain = PlatoBrain.from_merged("path/to/merged-model")

result = brain.score_tile("Photosynthesis converts light energy into chemical energy stored in glucose.")
print(result)
# {'tier': 'excellent', 'perplexity': 2.8, 'score': 0.97}
```

### 2. Q&A Inference

```python
from plato_neural import PlatoBrain

brain = PlatoBrain.from_merged("path/to/merged-model")

answer = brain.ask("What is the role of mitochondria in cellular respiration?")
print(answer)
# 'Mitochondria generate ATP through oxidative phosphorylation, acting as the cell's primary energy factory...'
```

### 3. Gap Detection

```python
from plato_neural import PlatoBrain

brain = PlatoBrain.from_merged("path/to/merged-model")

gaps = brain.find_gaps(room="biochemistry", existing_tiles=[
    "Glycolysis breaks down glucose into pyruvate.",
    "The citric acid cycle oxidizes acetyl-CoA.",
])
print(gaps)
# [{'room': 'biochemistry', 'missing': 'Electron transport chain and ATP synthesis', 'confidence': 0.91}, ...]
```

---

## API Reference

### `PlatoBrain`

| Method | Arguments | Returns | Description |
|--------|-----------|---------|-------------|
| `PlatoBrain.from_base(path)` | `path: str` | `PlatoBrain` | Load base model only |
| `PlatoBrain.from_lora(base, adapter)` | `base: str`, `adapter: str` | `PlatoBrain` | Load base + LoRA adapter |
| `PlatoBrain.from_merged(path)` | `path: str` | `PlatoBrain` | Load merged model (fastest) |
| `brain.score_tile(text)` | `text: str` | `dict` | Score tile; returns `tier`, `perplexity`, `score` |
| `brain.batch_score(tiles)` | `tiles: list[str]` | `list[dict]` | Score multiple tiles in one pass |
| `brain.ask(question, **kwargs)` | `question: str` | `str` | Generate an answer |
| `brain.find_gaps(room, existing_tiles)` | `room: str`, `existing_tiles: list[str]` | `list[dict]` | Detect missing knowledge |
| `brain.analyze_gaps(rooms)` | `rooms: dict[str, list[str]]` | `dict` | Full gap analysis with per-room aggregation |
| `brain.generate_tile(topic, room)` | `topic: str`, `room: str` | `str` | Generate a new tile for a weak room |

### Scoring Tiers

| Tier | Perplexity Range | Description |
|------|-----------------|-------------|
| `excellent` | < 5 | Dense, domain-native content |
| `good` | 5 – 10 | Solid, well-expressed knowledge |
| `fair` | 10 – 20 | Adequate but imprecise |
| `weak` | 20 – 40 | Sparse or poorly expressed |
| `poor` | > 40 | Off-domain or incoherent |

---

## Configuration

`PlatoBrain` accepts a `config` dict at construction:

```python
brain = PlatoBrain.from_merged(
    "path/to/merged-model",
    config={
        "device": "cuda",          # 'cuda', 'cpu', or 'auto'
        "dtype": "bf16",           # 'bf16', 'fp16', or 'fp32'
        "max_new_tokens": 256,     # generation length cap
        "temperature": 0.7,        # sampling temperature
        "top_p": 0.9,              # nucleus sampling
        "batch_size": 8,           # batch_score chunk size
    }
)
```

Environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `PLATO_MODEL_PATH` | — | Default model path |
| `PLATO_DEVICE` | `auto` | Device selection |
| `PLATO_DTYPE` | `bf16` | Precision |
| `PLATO_API_HOST` | `0.0.0.0` | REST API bind host |
| `PLATO_API_PORT` | `8000` | REST API port |

---

## Benchmarks

Measured on **RTX 4050 Laptop GPU**, bf16 precision, PLATO corpus (4,411 tiles):

| Model | Throughput | Perplexity | Recognition | Size |
|-------|-----------|-----------|-------------|------|
| Base Qwen2.5-0.5B | 77 tok/s | 33.1 | 91.5% | ~500MB |
| + LoRA r=16 | 38 tok/s | **3.6** | **100%** | +17MB adapter |
| Merged | **78 tok/s** | **3.6** | **100%** | 953MB |

**Training details:** 4,411 tiles · 120 rooms · 1,210 steps · loss 1.55 → 0.38 · 8.8M trainable params (1.75% of total)

The merged model is recommended for production: it matches LoRA accuracy at base model speed, with no adapter overhead at inference time.

---

## LoRA Usage

### Loading Base + Adapter

```python
from plato_neural import PlatoBrain

brain = PlatoBrain.from_lora(
    base_model="Qwen/Qwen2.5-0.5B",
    adapter_path="path/to/lora-adapter",
)
```

### Merging and Saving

```python
# Merge adapter weights into base model for maximum throughput
brain.merge_and_save("path/to/output-merged")
```

### Training Your Own Adapter

```python
from plato_neural.training import LoRATrainer

trainer = LoRATrainer(
    base_model="Qwen/Qwen2.5-0.5B",
    lora_config={"r": 16, "lora_alpha": 32, "target_modules": ["q_proj", "v_proj"]},
)
trainer.train(
    tiles=my_tile_list,       # list of str
    output_dir="my-adapter",
    num_steps=1200,
)
```

---

## REST API

Start the server:

```bash
plato-neural serve --model path/to/merged-model --port 8000
```

Or with Python:

```python
from plato_neural.api import create_app
import uvicorn

app = create_app(model_path="path/to/merged-model")
uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Server and model health check |
| `POST` | `/ask` | Answer a PLATO domain question |
| `POST` | `/score` | Score a single tile |
| `POST` | `/batch_score` | Score multiple tiles |
| `POST` | `/generate_tile` | Generate new tile content |
| `POST` | `/find_gaps` | Detect knowledge gaps in a room |

#### Example: `/score`

```bash
curl -X POST http://localhost:8000/score \
  -H "Content-Type: application/json" \
  -d '{"text": "Photosynthesis converts light energy into chemical energy."}'
```

```json
{
  "tier": "excellent",
  "perplexity": 2.8,
  "score": 0.97
}
```

#### Example: `/ask`

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is ATP?", "max_new_tokens": 128}'
```

#### Example: `/find_gaps`

```bash
curl -X POST http://localhost:8000/find_gaps \
  -H "Content-Type: application/json" \
  -d '{
    "room": "biochemistry",
    "existing_tiles": ["Glycolysis produces pyruvate.", "The citric acid cycle generates NADH."]
  }'
```

---

## CLI

```
Usage: plato-neural [OPTIONS] COMMAND [ARGS]...

Commands:
  ask       Answer a question using the PLATO neural model
  score     Score a tile or file of tiles
  gap       Detect knowledge gaps in a room
  serve     Start the REST API server
```

### `ask`

```bash
plato-neural ask "What is the function of ribosomes?" --model path/to/model
```

### `score`

```bash
# Score inline text
plato-neural score "Mitochondria produce ATP via oxidative phosphorylation." --model path/to/model

# Score a file of tiles (one per line)
plato-neural score --file tiles.txt --model path/to/model --output results.json
```

### `gap`

```bash
plato-neural gap \
  --room biochemistry \
  --tiles tiles.txt \
  --model path/to/model
```

### `serve`

```bash
plato-neural serve \
  --model path/to/merged-model \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 2
```

---

## Contributing

Contributions are welcome. Please open an issue before submitting a pull request for significant changes.

```bash
git clone https://github.com/purplepincher/plato-neural
cd plato-neural
pip install -e ".[dev,lora]"
pytest tests/
```

All submissions should include tests and pass `ruff check .` before opening a PR.

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

*Part of the [PLATO](https://purplepincher.org) knowledge ecosystem.*
```
