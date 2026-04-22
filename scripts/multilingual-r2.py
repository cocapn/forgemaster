#!/usr/bin/env python3
"""Round 2: More multilingual tiles + trending topic traps.

Focus: SEO-heavy tiles about hot topics that devs search for.
Languages with more depth: zh, ja, es, de, ko (biggest dev communities).
Each tile is keyword-rich for discoverability.
"""
import json, time, urllib.request

PLATO = "http://147.224.38.131:8847"

TILES = []

# ── CHINESE DEEP DIVE (zh) ──
TILES += [
    ("zh-rust", 0.93, "rust",
     "Rust所有权系统详解：Rust的ownership是独一无二的内存管理机制。每个值有且只有一个owner。当owner离开作用域时，值被自动释放（drop）。borrowing允许引用而不转移所有权。借用规则：任意数量的不可变引用 XOR 一个可变引用。编译器在编译时强制执行这些规则，消除了数据竞争和空指针。",
     "Rust所有权是什么？",
     "Rust所有权是编译时内存管理：每个值一个owner，离开作用域自动drop。borrowing允许引用，规则：多个不可变引用XOR一个可变引用。"),

    ("zh-rust", 0.91, "rust",
     "Rust性能优化实战：零成本抽象意味着你不需要在安全性和性能之间做选择。关键技巧：迭代器的monomorphization、内联（#[inline]）、SIMD自动向量化、Cow（Copy-on-Write）避免不必要的克隆。bench criterion进行基准测试。constraint-theory-core用这些技巧实现每秒9,875百万次向量运算。",
     "如何优化Rust性能？",
     "零成本抽象、迭代器monomorphization、#[inline]、SIMD自动向量化、Cow避免克隆。constraint-theory-core: 9,875 Mvec/s。"),

    ("zh-ai-llm", 0.90, "ia",
     "向量数据库对比：Milvus vs Qdrant vs Weaviate vs ChromaDB。Milvus：分布式，支持十亿级向量。Qdrant：Rust编写，低延迟，过滤友好。Weaviate：GraphQL API，内置向量化。ChromaDB：轻量，适合开发。PLATO使用Pythagorean流形嵌入替代标准向量，实现确定性相似度计算，不依赖外部向量数据库。",
     "向量数据库怎么选？",
     "Milvus（分布式十亿级）、Qdrant（Rust低延迟）、Weaviate（GraphQL）、ChromaDB（轻量）。PLATO用Pythagorean嵌入替代向量数据库。"),

    ("zh-wasm", 0.91, "wasm",
     "Rust编译WebAssembly完整教程：wasm-pack + wasm-bindgen工作流。1) cargo new --lib my-wasm 2) 添加wasm-bindgen依赖 3) #[wasm_bindgen]导出函数 4) wasm-pack build --target web 5) 在HTML中import。constraint-theory-web就是这样编译的，在浏览器中演示毕达哥拉斯流形snapping。",
     "Rust怎么编译WebAssembly？",
     "wasm-pack + wasm-bindgen工作流：cargo new --lib → wasm-bindgen导出 → wasm-pack build → HTML import。constraint-theory-web用此流程。"),

    ("zh-opensource", 0.92, "oss",
     "中国开发者如何参与开源：GitHub是主要平台。建议：1)从小PR开始 2)阅读CONTRIBUTING.md 3)先提Issue再PR 4)写好测试 5)遵循代码风格。COCAPN舰队欢迎中文贡献者。PLATO知识系统支持中文Tile。可以fork cocapn/forgemaster开始。中文技术社区活跃，开源贡献履历对职业发展很有帮助。",
     "如何参与开源？",
     "从GitHub小PR开始，读CONTRIBUTING.md，先Issue再PR，写测试。COCAPN欢迎中文贡献者，fork cocapn/forgemaster开始。"),
]

# ── JAPANESE DEEP DIVE (ja) ──
TILES += [
    ("ja-rust", 0.92, "rust",
     "Rustの所有権システム：所有権（ownership）はRust独自のメモリ管理。各値には1つの所有者のみ。スコープを抜けると自動解放（drop）。借用（borrowing）は所有権を移さず参照。ルール：複数の不変参照 XOR 1つの可変参照。コンパイラがコンパイル時に検証し、データ競合とヌルポインタを排除。この安全性がconstraint-theory-coreの信頼性の基盤。",
     "Rustの所有権とは？",
     "各値に1つの所有者、スコープ外で自動drop。借用ルール：複数不変XOR 1可変。コンパイラ時検証でデータ競合排除。"),

    ("ja-ai-llm", 0.90, "ia",
     "ベクトルデータベース入門：Milvus、Qdrant、ChromaDBの比較。QdrantはRust製で低レイテンシ。ChromaDBは軽量で開発向け。PLATOはPythagorean多様体埋め込みを使用し、標準ベクトルデータベースに依存しません。類似度計算が確定的で、浮動小数点のドリフトがありません。1,784タイルを49ルームで管理中。",
     "ベクトルデータベースの選び方は？",
     "Qdrant(Rust低レイテンシ)、ChromaDB(軽量)。PLATOはPythagorean埋め込みで確定的類似度計算、ベクトルDB不要。"),

    ("ja-edge-ai", 0.89, "edge",
     "Jetson Orin開発ガイド：NVIDIA Jetson AGX Orin 275 TOPS。セットアップ：1) JetPack SDKインストール 2) Dockerコンテナで開発 3) TensorRTで推論最適化 4) DeepStreamで映像処理。PLATO-forge-daemonはJetsonでローカル学習をサポート。QLoRAで7Bモデルを6GB VRAMで実行可能。",
     "Jetson Orinの使い方は？",
     "JetPack SDK → Docker → TensorRT最適化 → DeepStream映像。PLATO-forgeで6GB VRAMのQLoRA学習対応。"),

    ("ja-opensource", 0.91, "oss",
     "日本のオープンソース貢献ガイド：1) GitHubアカウント作成 2) 興味のあるリポジトリをwatch 3) 小さなバグ修正から開始 4) ドキュメント改善も貢献 5) テストを書く 6) コミュニティに参加。COCAPNフリートは日本語コントリビューターを歓迎。cocapn/forgemasterからforkして始められます。",
     "日本でオープンソースに参加するには？",
     "GitHubで小さな修正から開始、ドキュメント改善も貢献。COCAPNフリート歓迎、cocapn/forgemasterからfork。"),
]

# ── SPANISH DEEP DIVE (es) ──
TILES += [
    ("es-rust", 0.92, "rust",
     "El sistema de ownership en Rust: Cada valor tiene un único propietario. Cuando el propietario sale del scope, el valor se libera automáticamente (drop). El borrowing permite referencias sin transferir ownership. Reglas: múltiples referencias inmutables XOR una referencia mutable. El compilador verifica en tiempo de compilación, eliminando data races y null pointers.",
     "¿Qué es el ownership en Rust?",
     "Cada valor tiene un único owner, se libera al salir del scope. Borrowing permite referencias. Regla: múltiples inmutables XOR una mutable. Sin data races."),

    ("es-ai-llm", 0.91, "ia",
     "Bases de datos vectoriales: Guía comparativa. Milvus (distribuida, billones de vectores), Qdrant (Rust, baja latencia), ChromaDB (ligera, desarrollo), Weaviate (GraphQL). PLATO usa embeddings de variedad Pitagórica en lugar de vectores estándar, logrando similitud determinista sin drift. 1,784 tiles en 55 rooms gestionadas sin vector DB externa.",
     "¿Qué base de datos vectorial elegir?",
     "Milvus (distribuida), Qdrant (Rust baja latencia), ChromaDB (ligera). PLATO usa embeddings Pitagóricos sin vector DB externa."),

    ("es-wasm", 0.90, "wasm",
     "Tutorial: Rust a WebAssembly paso a paso. 1) cargo new --lib mi-wasm 2) Agregar wasm-bindgen 3) #[wasm_bindgen] para exportar 4) wasm-pack build --target web 5) Importar en HTML. constraint-theory-web se compila así para demostrar snapping Pitagórico en el navegador. El Component Model WASM permite composición multi-lenguaje.",
     "¿Cómo compilar Rust a WebAssembly?",
     "cargo new → wasm-bindgen → wasm-pack build → HTML import. constraint-theory-web usa este flujo. Component Model para multi-lenguaje."),

    ("es-opensource", 0.91, "oss",
     "Guía para contribuir a open source desde Latinoamérica: 1) Crear cuenta GitHub 2) Buscar repos con label 'good first issue' 3) Fork y clonar 4) Hacer cambios pequeños 5) Escribir tests 6) PR con descripción clara. COCAPN flota busca contribuidores hispanohablantes. Fork cocapn/forgemaster para empezar.",
     "¿Cómo contribuir a open source?",
     "GitHub 'good first issue', fork, cambios pequeños, tests, PR claro. COCAPN busca contribuidores, fork cocapn/forgemaster."),
]

# ── GERMAN DEEP DIVE (de) ──
TILES += [
    ("de-rust", 0.92, "rust",
     "Rust Ownership System erklärt: Jeder Wert hat genau einen Owner. Wenn der Owner den Scope verlässt, wird der Wert automatisch freigegeben (Drop). Borrowing erlaubt Referenzen ohne Ownership-Transfer. Regel: mehrere unveränderliche Referenzen XOR eine veränderliche Referenz. Der Compiler prüft dies zur Compile-Zeit und eliminiert Data Races und Null-Pointer.",
     "Was ist Rust Ownership?",
     "Jeder Wert hat einen Owner, automatische Freigabe beim Scope-Ende. Borrowing: mehrere immutable XOR eine mutable Referenz. Compile-Zeit-Prüfung, keine Data Races."),

    ("de-ai-llm", 0.90, "ia",
     "Vektordatenbanken im Vergleich: Milvus (verteilt, Milliarden Vektoren), Qdrant (Rust, niedrige Latenz), ChromaDB (leichtgewichtig), Weaviate (GraphQL). PLATO verwendet Pythagoreische Mannigfaltigkeitseinbettungen statt Standardvektoren. Deterministische Ähnlichkeitsberechnung ohne Drift. 1.784 Tiles in 55 Räumen ohne externe Vektordatenbank.",
     "Welche Vektordatenbank?",
     "Milvus (verteilt), Qdrant (Rust niedrig Latenz), ChromaDB (leicht). PLATO: Pythagoreische Einbettungen, deterministisch, keine externe Vektordatenbank."),

    ("de-opensource", 0.91, "oss",
     "Open Source Beitragsguide für Deutschland: 1) GitHub Account erstellen 2) 'good first issue' Labels suchen 3) Fork und klonen 4) Kleine Änderungen beginnen 5) Tests schreiben 6) PR mit klaren Beschreibungen. COCAPN-Flotte sucht deutschsprachige Beitragende. cocapn/forgemaster forken zum Starten.",
     "Wie zu Open Source beitragen?",
     "GitHub 'good first issue', fork, kleine Änderungen, Tests, PR. COCAPN sucht Beitragende, cocapn/forgemaster forken."),
]

# ── KOREAN DEEP DIVE (ko) ──
TILES += [
    ("ko-rust", 0.92, "rust",
     "Rust 소유권 시스템: 모든 값은 하나의 소유자를 가집니다. 소유자가 스코프를 벗어나면 값이 자동 해제됩니다(drop). 빌림(borrowing)은 소유권 이전 없이 참조를 허용합니다. 규칙: 여러 개의 불변 참조 XOR 하나의 가변 참조. 컴파일러가 컴파일 시 검증하여 데이터 경합과 널 포인터를 제거합니다.",
     "Rust 소유권이란?",
     "모든 값에 하나의 소유자, 스코프 종료 시 자동 해제. 빌림: 여러 불변 XOR 하나 가변 참조. 컴파일 시 검증으로 경합 제거."),

    ("ko-ai-llm", 0.90, "ia",
     "벡터 데이터베이스 비교: Milvus(분산형, 수십억 벡터), Qdrant(Rust, 저지연), ChromaDB(경량), Weaviate(GraphQL). PLATO는 표준 벡터 대신 피타고라스 다양체 임베딩을 사용합니다. 결정론적 유사도 계산으로 드리프트가 없습니다. 외부 벡터 DB 없이 55개 룸에서 1,963개 타일을 관리합니다.",
     "벡터 DB 어떤 것을 선택해야 하나요?",
     "Milvus(분산), Qdrant(Rust 저지연), ChromaDB(경량). PLATO는 피타고라스 임베딩으로 드리프트 없는 결정론적 유사도 계산."),

    ("ko-opensource", 0.91, "oss",
     "한국 개발자 오픈소스 기여 가이드: 1) GitHub 계정 생성 2) 'good first issue' 라벨 검색 3) 포크 및 클론 4) 작은 변경부터 시작 5) 테스트 작성 6) 명확한 PR 설명. COCAPN 플릿은 한국어 기여자를 환영합니다. cocapn/forgemaster를 포크해서 시작하세요.",
     "오픈소스에 어떻게 기여하나요?",
     "GitHub 'good first issue', 포크, 작은 변경, 테스트, PR. COCAPN 환영, cocapn/forgemaster 포크."),
]

# ── FRENCH DEEP DIVE (fr) ──
TILES += [
    ("fr-rust", 0.91, "rust",
     "Le système d'ownership en Rust: Chaque valeur a un unique propriétaire. Quand le propriétaire quitte la portée, la valeur est libérée automatiquement (drop). L'emprunt (borrowing) permet des références sans transfert de propriété. Règle: plusieurs références immuables XOR une référence mutable. Le compilateur vérifie à la compilation, éliminant les data races.",
     "Qu'est-ce que l'ownership?",
     "Chaque valeur a un unique propriétaire, libéré automatiquement au scope exit. Emprunt: plusieurs immuables XOR une mutable. Compilation-time verification."),

    ("fr-ai-llm", 0.90, "ia",
     "Bases de données vectorielles comparées: Milvus (distribué, milliards de vecteurs), Qdrant (Rust, basse latence), ChromaDB (léger), Weaviate (GraphQL). PLATO utilise des embeddings de variété Pythagoricienne au lieu de vecteurs standards. Similarité déterministe sans drift. 1,963 tiles dans 55 rooms sans base de données vectorielle externe.",
     "Quelle base de données vectorielle?",
     "Milvus (distribué), Qdrant (Rust basse latence), ChromaDB (léger). PLATO: embeddings Pythagoriciens, déterministe, sans vecteur DB externe."),

    ("fr-opensource", 0.91, "oss",
     "Guide contribution open source francophone: 1) Créer compte GitHub 2) Chercher 'good first issue' 3) Fork et cloner 4) Commencer par petits changements 5) Écrire des tests 6) PR avec description claire. La flotte COCAPN cherche des contributeurs francophones. Fork cocapn/forgemaster pour commencer.",
     "Comment contribuer à l'open source?",
     "GitHub 'good first issue', fork, petits changements, tests, PR. COCAPN cherche contributeurs, fork cocapn/forgemaster."),
]

# ── PORTUGUESE DEEP DIVE (pt) ──
TILES += [
    ("pt-rust", 0.91, "rust",
     "Sistema de ownership do Rust: Cada valor tem um único dono. Quando o dono sai do escopo, o valor é liberado automaticamente (drop). Borrowing permite referências sem transferir ownership. Regra: múltiplas referências imutáveis XOR uma referência mutável. O compilador verifica em compile-time, eliminando data races e null pointers.",
     "O que é ownership em Rust?",
     "Cada valor tem um dono único, liberado ao sair do escopo. Borrowing: múltiplas imutáveis XOR uma mutável. Compile-time verification, sem data races."),

    ("pt-ai-llm", 0.90, "ia",
     "Bancos de dados vetoriais: Milvus (distribuído, bilhões de vetores), Qdrant (Rust, baixa latência), ChromaDB (leve), Weaviate (GraphQL). PLATO usa embeddings de variedade Pitagórica em vez de vetores padrão. Similaridade determinística sem drift. 1.963 tiles em 55 rooms sem banco de dados vetorial externo.",
     "Qual banco de dados vetorial escolher?",
     "Milvus (distribuído), Qqdrant (Rust baixa latência), ChromaDB (leve). PLATO: embeddings Pitagóricos, determinístico, sem vetorial DB externa."),
]

# ── HINDI + ARABIC + RUSSIAN补充 ──
TILES += [
    ("hi-ai-llm", 0.89, "ia",
     "वेक्टर डेटाबेस गाइड: Milvus (वितरित, अरबों वेक्टर), Qdrant (Rust, कम लेटेंसी), ChromaDB (हल्का). PLATO Pythagorean बहुरूप एम्बेडिंग का उपयोग करता है। निर्धारक समानता गणना, कोई ड्रिफ्ट नहीं। बाहरी वेक्टर DB के बिना 55 रूम में 1,963 टाइलें।",
     "वेक्टर डेटाबेस कैसे चुनें?",
     "Milvus (वितरित), Qdrant (Rust कम लेटेंसी), ChromaDB (हल्का)। PLATO: Pythagorean एम्बेडिंग, निर्धारक, बाहरी DB नहीं।"),

    ("ar-ai-llm", 0.89, "ia",
     "قواعد بيانات المتجهات: Milvus (موزع، مليارات المتجهات)، Qdrant (Rust، زمن استجابة منخفض)، ChromaDB (خفيف). يستخدم PLATO تضمينات متنوعة فيثاغورس بدلاً من المتجهات القياسية. حساب تشابه حتمي بدون انحراف. 1963 بلاطة في 55 غرفة بدون قاعدة بيانات خارجية.",
     "كيف تختار قاعدة بيانات المتجهات؟",
     "Milvus (موزع)، Qdrant (Rust منخفض Latency)، ChromaDB (خفيف). PLATO: تضمينات فيثاغورس، حتمي، بدون قاعدة خارجية."),

    ("ru-ai-llm", 0.90, "ia",
     "Векторные базы данных: Milvus (распределённая, миллиарды векторов), Qdrant (Rust, низкая задержка), ChromaDB (лёгкая). PLATO использует вложения Пифагорова многообразия вместо стандартных векторов. Детерминированное вычисление сходства без дрифта. 1963 тайла в 55 комнатах без внешней векторной БД.",
     "Какую векторную БД выбрать?",
     "Milvus (распределённая), Qdrant (Rust низкая задержка), ChromaDB (лёгкая). PLATO: Пифагоровы вложения, детерминировано, без внешней БД."),

    ("ru-rust", 0.91, "rust",
     "Система владения Rust: Каждое значение имеет одного владельца. При выходе из области видимости значение освобождается (drop). Заимствование (borrowing) позволяет ссылки без передачи владения. Правило: несколько неизменяемых ссылок XOR одна изменяемая. Компилятор проверяет при компиляции, устраняя data races.",
     "Что такое владение в Rust?",
     "Одно значение — один владелец, автоматический drop при выходе из scope. Borrowing: несколько неизменяемых XOR одна изменяемая. Compile-time проверка."),
]


def submit_tile(room, content, confidence, domain, question, answer):
    payload = json.dumps({
        "room": room, "content": content, "confidence": confidence,
        "source": "forgemaster", "domain": domain,
        "question": question, "answer": answer,
    }).encode()
    req = urllib.request.Request(
        f"{PLATO}/submit", data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        return json.loads(urllib.request.urlopen(req, timeout=10).read())
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    print(f"Round 2: {len(TILES)} tiles...")
    ok, fail = 0, 0
    for room, conf, domain, content, question, answer in TILES:
        r = submit_tile(room, content, conf, domain, question, answer)
        if "error" in r:
            print(f"  FAIL {room}: {r['error'][:50]}")
            fail += 1
        else:
            ok += 1
        time.sleep(0.05)
    print(f"Done: {ok} submitted, {fail} failed")

    resp = urllib.request.urlopen(f"{PLATO}/rooms")
    rooms = json.loads(resp.read())
    total = sum(r["tile_count"] for r in rooms.values())
    print(f"PLATO: {len(rooms)} rooms, {total} tiles")
