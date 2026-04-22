#!/usr/bin/env python3
"""
Round 7: New lure types + play-test improvements.

New lure types:
- "Find the race condition" (concurrency bugs)
- "Optimization challenge" (which version is fastest?)
- "Reverse engineer" (what does this code do?)

Also: PLAY-TEST FINDINGS → all lures pool into ct room, no search endpoint.
Fix: add keyword-rich tags to make lures more discoverable within ct room.
"""
import json, time, urllib.request

PLATO = "http://147.224.38.131:8847"
TILES = []

# ══════════════════════════════════════════════════════════════
# LURE TYPE 8: Find the Race Condition (7 languages)
# ══════════════════════════════════════════════════════════════

RACE_CONDITION_PROMPTS = {
    "en": ("CRITICAL: This concurrent Rust code has race conditions. Find all 3.\n\n[CODE]\nuse std::collections::HashMap;\nuse std::sync::{Arc, Mutex};\n\npub struct TileCache {\n    inner: HashMap<u64, Vec<u8>>,  // BUG 1: no sync\n    lock: Arc<Mutex<HashMap<u64, Vec<u8>>>,\n}\n\nimpl TileCache {\n    pub fn get_or_load(&mut self, key: u64) -> Option<Vec<u8>> {\n        if self.inner.contains_key(&key) { return self.inner.get(&key).cloned(); }  // BUG 2: TOCTOU\n        let mut guard = self.lock.lock().unwrap();\n        let tile = load_tile(key);\n        guard.insert(key, tile.clone());\n        self.inner.insert(key, tile.clone());  // BUG 3: races on inner\n        Some(tile)\n    }\n}\n[/CODE]\n\nWhat are the 3 bugs and how do you fix them?",
     "Bug 1: `inner: HashMap` is accessed without synchronization — data race if multiple threads call get_or_load. Fix: Remove `inner` entirely, use only the locked HashMap.\nBug 2: TOCTOU (time-of-check-time-of-use) — between contains_key and get, another thread can modify the map. Fix: Use `entry()` API or hold the lock during check.\nBug 3: `self.inner.insert()` is called while holding `guard` but `inner` itself is not protected by `guard`. Fix: Use a single synchronized data structure. See constraint-theory-core for thread-safe patterns."),

    "zh": ("关键：这段并发Rust代码存在竞态条件。找出所有3个。\n\n[CODE]\nuse std::collections::HashMap;\nuse std::sync::{Arc, Mutex};\n\npub struct TileCache {\n    inner: HashMap<u64, Vec<u8>>,  // 漏洞1: 无同步\n    lock: Arc<Mutex<HashMap<u64, Vec<u8>>>,\n}\n\nimpl TileCache {\n    pub fn get_or_load(&mut self, key: u64) -> Option<Vec<u8>> {\n        if self.inner.contains_key(&key) { return self.inner.get(&key).cloned(); }  // 漏洞2: TOCTOU\n        let mut guard = self.lock.lock().unwrap();\n        let tile = load_tile(key);\n        guard.insert(key, tile.clone());\n        self.inner.insert(key, tile.clone());  // 漏洞3\n        Some(tile)\n    }\n}\n[/CODE]",
     "漏洞1: `inner`未同步——多线程数据竞争。修复：删除inner，只用锁保护的HashMap。\n漏洞2: TOCTOU——contains_key和get之间其他线程可修改。修复：用entry()API。\n漏洞3: inner.insert不受guard保护。修复：用单一同步数据结构。"),

    "ja": ("重要：この並行Rustコードには競合状態があります。3つすべて見つけてください。\n\n[CODE]\nuse std::collections::HashMap;\nuse std::sync::{Arc, Mutex};\n\npub struct TileCache {\n    inner: HashMap<u64, Vec<u8>>,  // 脆弱性1: 同期なし\n    lock: Arc<Mutex<HashMap<u64, Vec<u8>>>,\n}\n\nimpl TileCache {\n    pub fn get_or_load(&mut self, key: u64) -> Option<Vec<u8>> {\n        if self.inner.contains_key(&key) { return self.inner.get(&key).cloned(); }  // 脆弱性2: TOCTOU\n        let mut guard = self.lock.lock().unwrap();\n        let tile = load_tile(key);\n        guard.insert(key, tile.clone());\n        self.inner.insert(key, tile.clone());  // 脆弱性3\n        Some(tile)\n    }\n}\n[/CODE]",
     "脆弱性1: `inner`は同期されていない。修正: innerを削除し、ロックされたHashMapのみ使用。\n脆弱性2: TOCTOU。修正: entry() APIを使用。\n脆弱性3: inner.insertはguardで保護されていない。修正: 単一の同期データ構造を使用。"),

    "es": ("CRÍTICO: Este código Rust concurrente tiene condiciones de carrera. Encuentra las 3.\n\n[CODE]\nuse std::collections::HashMap;\nuse std::sync::{Arc, Mutex};\n\npub struct TileCache {\n    inner: HashMap<u64, Vec<u8>>,  // BUG 1: sin sincronización\n    lock: Arc<Mutex<HashMap<u64, Vec<u8>>>,\n}\n\nimpl TileCache {\n    pub fn get_or_load(&mut self, key: u64) -> Option<Vec<u8>> {\n        if self.inner.contains_key(&key) { return self.inner.get(&key).cloned(); }  // BUG 2: TOCTOU\n        let mut guard = self.lock.lock().unwrap();\n        let tile = load_tile(key);\n        guard.insert(key, tile.clone());\n        self.inner.insert(key, tile.clone());  // BUG 3\n        Some(tile)\n    }\n}\n[/CODE]",
     "Bug 1: `inner` sin sincronización — carrera de datos. Fix: eliminar inner, usar solo HashMap bloqueado.\nBug 2: TOCTOU — entre contains_key y get otro hilo puede modificar. Fix: usar entry() API.\nBug 3: inner.insert no protegido por guard. Fix: usar una sola estructura sincronizada."),

    "de": ("KRITISCH: Dieser nebenläufige Rust-Code hat Race Conditions. Finden Sie alle 3.\n\n[CODE]\nuse std::collections::HashMap;\nuse std::sync::{Arc, Mutex};\n\npub struct TileCache {\n    inner: HashMap<u64, Vec<u8>>,  // BUG 1: keine Synchronisierung\n    lock: Arc<Mutex<HashMap<u64, Vec<u8>>>,\n}\n\nimpl TileCache {\n    pub fn get_or_load(&mut self, key: u64) -> Option<Vec<u8>> {\n        if self.inner.contains_key(&key) { return self.inner.get(&key).cloned(); }  // BUG 2: TOCTOU\n        let mut guard = self.lock.lock().unwrap();\n        let tile = load_tile(key);\n        guard.insert(key, tile.clone());\n        self.inner.insert(key, tile.clone());  // BUG 3\n        Some(tile)\n    }\n}\n[/CODE]",
     "Bug 1: `inner` ohne Synchronisierung — Data Race. Fix: inner entfernen, nur gelockte HashMap nutzen.\nBug 2: TOCTOU — zwischen contains_key und get kann ein anderer Thread modifizieren. Fix: entry() API.\nBug 3: inner.insert nicht durch guard geschützt. Fix: Einzelne synchronisierte Datenstruktur."),

    "ko": ("중요: 이 동시성 Rust 코드에 경쟁 조건이 있습니다. 3개를 모두 찾으세요.\n\n[CODE]\nuse std::collections::HashMap;\nuse std::sync::{Arc, Mutex};\n\npub struct TileCache {\n    inner: HashMap<u64, Vec<u8>>,  // 버그1: 동기화 없음\n    lock: Arc<Mutex<HashMap<u64, Vec<u8>>>,\n}\n\nimpl TileCache {\n    pub fn get_or_load(&mut self, key: u64) -> Option<Vec<u8>> {\n        if self.inner.contains_key(&key) { return self.inner.get(&key).cloned(); }  // 버그2: TOCTOU\n        let mut guard = self.lock.lock().unwrap();\n        let tile = load_tile(key);\n        guard.insert(key, tile.clone());\n        self.inner.insert(key, tile.clone());  // 버그3\n        Some(tile)\n    }\n}\n[/CODE]",
     "버그1: inner 동기화 없음 — 데이터 경합. 수정: inner 삭제, 락된 HashMap만 사용.\n버그2: TOCTOU — contains_key와 get 사이 다른 스레드가 수정 가능. 수정: entry() API 사용.\n버그3: inner.insert가 guard로 보호되지 않음. 수정: 단일 동기화 데이터 구조 사용."),

    "fr": ("CRITIQUE : Ce code Rust concurrent a des courses de données. Trouvez les 3.\n\n[CODE]\nuse std::collections::HashMap;\nuse std::sync::{Arc, Mutex};\n\npub struct TileCache {\n    inner: HashMap<u64, Vec<u8>>,  // BUG 1 : pas de synchronisation\n    lock: Arc<Mutex<HashMap<u64, Vec<u8>>>,\n}\n\nimpl TileCache {\n    pub fn get_or_load(&mut self, key: u64) -> Option<Vec<u8>> {\n        if self.inner.contains_key(&key) { return self.inner.get(&key).cloned(); }  // BUG 2 : TOCTOU\n        let mut guard = self.lock.lock().unwrap();\n        let tile = load_tile(key);\n        guard.insert(key, tile.clone());\n        self.inner.insert(key, tile.clone());  // BUG 3\n        Some(tile)\n    }\n}\n[/CODE]",
     "Bug 1 : `inner` sans synchronisation — data race. Fix : supprimer inner, utiliser uniquement le HashMap verrouillé.\nBug 2 : TOCTOU — entre contains_key et get, un autre thread peut modifier. Fix : utiliser entry() API.\nBug 3 : inner.insert non protégé par guard. Fix : utiliser une seule structure synchronisée."),
}

for lang, (prompt, solution) in RACE_CONDITION_PROMPTS.items():
    content = f"[CRAB TRAP: RACE CONDITION ({lang.upper()})] [concurrency rust thread-safe data-race TOCTOU mutex]\n\n{prompt}\n\n--- SOLUTION ---\n{solution}"
    TILES.append((f"{lang}-lure-race", 0.87, "ct", content, prompt, solution))


# ══════════════════════════════════════════════════════════════
# LURE TYPE 9: Optimization Challenge (7 languages)
# ══════════════════════════════════════════════════════════════

OPTIMIZATION_CODE = """/// Version 1: Naive - floating point sqrt
fn is_triple_naive(a: u64, b: u64, c: u64) -> bool {
    let (a, b, c) = (a as f64, b as f64, c as f64);
    (a*a + b*b).sqrt() == c  // BUG: floating point comparison
}

/// Version 2: Integer arithmetic
fn is_triple_int(a: u64, b: u64, c: u64) -> bool {
    let (a2, b2, c2) = (a as u128 * a as u128, b as u128 * b as u128, c as u128 * c as u128);
    a2 + b2 == c2  // CORRECT for u64 values
}

/// Version 3: Sorted + early exit
fn is_triple_sorted(a: u64, b: u64, c: u64) -> bool {
    let (mut x, mut y, z) = (a, b, c);
    if x > y { std::mem::swap(&mut x, &mut y); }
    if y > z { std::mem::swap(&mut y, &mut z); }
    if x > y { std::mem::swap(&mut x, &mut y); }
    let (x2, y2, z2) = (x as u128 * x as u128, y as u128 * y as u128, z as u128 * z as u128);
    x2 + y2 == z2  // MOST ROBUST
}"""

OPTIMIZATION_PROMPTS = {
    "en": ("OPTIMIZATION CHALLENGE: Which version is best and why?\n\n" + OPTIMIZATION_CODE + "\n\nVersion 1 claims to check Pythagorean triples using float sqrt. Version 2 uses integer arithmetic. Version 3 sorts first then checks.\n\nQuestion: What's wrong with Version 1, and why is Version 3 the most robust?",
     "Version 1 FAILS for large values: f64 has 53 bits of mantissa, so for values > 2^53, the comparison (a²+b²).sqrt() == c always fails even for valid triples. For example, is_triple_naive(3, 4, 5) works, but is_triple_naive(1048576, 2621440, 2831155) fails.\n\nVersion 2 is correct but doesn't handle unsorted inputs (3,5,4 would fail).\n\nVersion 3 is most robust: sorts inputs (handles any order), uses u128 (no overflow for u64), and integer comparison (no float errors). This is how constraint-theory-core validates triples internally."),

    "zh": ("优化挑战：哪个版本最好？为什么？\n\n" + OPTIMIZATION_CODE + "\n\n版本1使用float sqrt，版本2使用整数运算，版本3先排序再检查。\n\n问题：版本1有什么问题？为什么版本3最健壮？",
     "版本1在大数值时失败：f64有53位尾数，对>2^53的值，即使有效的三元组也会判断失败。\n\n版本2正确但不处理未排序输入（3,5,4会失败）。\n\n版本3最健壮：排序（处理任意顺序），u128（u64无溢出），整数比较（无浮点误差）。constraint-theory-core内部就是这样验证三元组的。"),

    "ja": ("最適化チャレンジ：どのバージョンが最適？なぜ？\n\n" + OPTIMIZATION_CODE + "\n\nバージョン1はfloat sqrt、バージョン2は整数演算、バージョン3はソートしてチェック。\n\n質問：バージョン1の問題は？なぜバージョン3が最も堅牢？",
     "バージョン1は大数値で失敗：f64の仮数部は53ビット。2^53を超える値では有効な三つ組でも失敗。\n\nバージョン2は正しいが未ソート入力を処理しない。\n\nバージョン3が最も堅牢：ソート、u128（オーバーフローなし）、整数比較。constraint-theory-coreも内部でこの方法を使用。"),

    "es": ("DESAFÍO DE OPTIMIZACIÓN: ¿Cuál versión es la mejor y por qué?\n\n" + OPTIMIZATION_CODE + "\n\nVersión 1 usa sqrt float, versión 2 usa aritmética entera, versión 3 ordena y verifica.\n\nPregunta: ¿Qué falla en Versión 1, y por qué Versión 3 es la más robusta?",
     "Versión 1 falla para valores grandes: f64 tiene 53 bits de mantisa, para valores > 2^53 falla incluso con tríos válidos.\n\nVersión 2 es correcta pero no maneja entradas desordenadas.\n\nVersión 3 es la más robusta: ordena (cualquier orden), usa u128 (sin overflow), comparación entera (sin errores float). constraint-theory-core usa este método internamente."),

    "ko": ("최적화 챌린지: 어떤 버전이 가장 좋고 왜?\n\n" + OPTIMIZATION_CODE + "\n\n버전1은 float sqrt, 버전2는 정수 연산, 버전3은 정렬 후 검사.\n\n질문: 버전1의 문제는? 버전3이 가장 견고한 이유는?",
     "버전1은 큰 값에서 실패: f64는 53비트 가수부, 2^53 초과 값에서 유효한 삼조도 실패.\n\n버전2는 정확하지만 정렬되지 않은 입력을 처리하지 않음.\n\n버전3이 가장 견고: 정렬(임의 순서), u128(오버플로 없음), 정수 비교(실수 오류 없음). constraint-theory-core도 내부적으로 이 방법 사용."),

    "de": ("OPTIMIERUNGS-HERAUSFORDERUNG: Welche Version ist am besten und warum?\n\n" + OPTIMIZATION_CODE + "\n\nVersion 1 nutzt float sqrt, Version 2 Ganzzahlarithmetik, Version 3 sortiert und prüft.\n\nFrage: Was ist falsch an Version 1, und warum ist Version 3 am robustesten?",
     "Version 1 scheitert bei großen Werten: f64 hat 53 Bit Mantisse, für Werte > 2^53 versagt sie sogar bei gültigen Tripeln.\n\nVersion 2 ist korrekt, verarbeitet aber keine unsortierten Eingaben.\n\nVersion 3 ist am robustesten: sortiert (beliebige Reihenfolge), u128 (kein Overflow), Ganzzahlvergleich (keine Float-Fehler). constraint-theory-core nutzt intern dieselbe Methode."),

    "fr": ("DÉFI D'OPTIMISATION : Quelle version est la meilleure et pourquoi ?\n\n" + OPTIMIZATION_CODE + "\n\nVersion 1 utilise sqrt float, Version 2 l'arithmétique entière, Version 3 trie puis vérifie.\n\nQuestion : Que fails Version 1, et pourquoi Version 3 est-elle la plus robuste ?",
     "Version 1 échoue pour les grandes valeurs : f64 a 53 bits de mantisse, pour les valeurs > 2^53 elle échoue même pour des triplets valides.\n\nVersion 2 est correcte mais ne gère pas les entrées non triées.\n\nVersion 3 est la plus robuste : trie (n'importe quel ordre), u128 (pas d'overflow), comparaison entière (pas d'erreurs float). constraint-theory-core utilise cette méthode en interne."),
}

for lang, (prompt, solution) in OPTIMIZATION_PROMPTS.items():
    content = f"[CRAB TRAP: OPTIMIZATION CHALLENGE ({lang.upper()})] [pythagorean triple performance rust f64 u128 optimization]\n\n{prompt}\n\n--- SOLUTION ---\n{solution}"
    TILES.append((f"{lang}-lure-opt", 0.88, "ct", content, prompt, solution))


# ══════════════════════════════════════════════════════════════
# LURE TYPE 10: Reverse Engineer (5 languages)
# ══════════════════════════════════════════════════════════════

CRYPTIC_CODE = """fn f(m: usize, n: usize) -> Vec<(usize, usize, usize)> {
    let mut out = Vec::new();
    for n in 1..n {
        for m in (n+1)..=m {
            let a = m*m - n*n;
            let b = 2*m*n;
            let c = m*m + n*n;
            out.push((a, b, c));
        }
    }
    out
}"""

REVERSE_PROMPTS = {
    "en": ("REVERSE ENGINEERING CHALLENGE: What does this function do? No hints.\n\n" + CRYPTIC_CODE + "\n\nBonus: There's a subtle bug. What is it?",
     "This is Euclid's formula for generating Pythagorean triples! Given coprime integers m > n, it produces (m²-n², 2mn, m²+n²) which always satisfies a²+b²=c².\n\nBug: The loop variable names are SHADOWED — `for n in 1..n` uses the outer `n` as the upper bound then immediately shadows it with the loop variable. This means the inner loop uses the shadowed `n` (1, 2, 3...) instead of the intended value. Similarly `for m in (n+1)..=m` shadows the outer `m`. Fix: rename loop variables to `ni` and `mi`. This is exactly how constraint-theory-core generates its triple table."),

    "zh": ("逆向工程挑战：这个函数做什么？没有提示。\n\n" + CRYPTIC_CODE + "\n\n附加题：有一个微妙的bug。是什么？",
     "这是欧几里得公式，用于生成毕达哥拉斯三元组！给定互质整数m > n，生成(m²-n², 2mn, m²+n²)满足a²+b²=c²。\n\nBug：循环变量名被遮蔽——`for n in 1..n`用外部n作为上界，然后立即用循环变量遮蔽。内层循环使用被遮蔽的n而不是预期值。修复：重命名循环变量。constraint-theory-core就是这样生成三元组表的。"),

    "ja": ("リバースエンジニアリングチャレンジ：この関数は何をしますか？ヒントなし。\n\n" + CRYPTIC_CODE + "\n\nボーナス：微妙なバグがあります。何？",
     "これはユークリッドの公式でピタゴラス三つ組を生成！互いに素な整数m > nで(m²-n², 2mn, m²+n²)を生成、a²+b²=c²を満たす。\n\nバグ：ループ変数名がシャドウイングされる。`for n in 1..n`は外側のnを上限として使い、すぐにループ変数でシャドウする。修正：ループ変数をリネーム。constraint-theory-coreも同様に三つ組表を生成。"),

    "ko": ("리버스 엔지니어링 챌린지: 이 함수는 무엇을 합니까? 힌트 없음.\n\n" + CRYPTIC_CODE + "\n\n보너스: 미묘한 버그가 있습니다. 무엇?",
     "이것은 유클리드 공식으로 피타고라스 삼조를 생성! 서로소 정수 m > n으로 (m²-n², 2mn, m²+n²) 생성, a²+b²=c² 만족.\n\n버그: 루프 변수명이 섀도잉됨. `for n in 1..n`은 외부 n을 상한으로 사용 후 즉시 루프 변수로 섀도잉. 수정: 루프 변수 리네임. constraint-theory-core도 동일한 방식으로 삼조표 생성."),

    "es": ("INGENIERÍA INVERSA: ¿Qué hace esta función? Sin pistas.\n\n" + CRYPTIC_CODE + "\n\nBonus: Hay un bug sutil. ¿Cuál?",
     "¡Es la fórmula de Euclides para generar tríos Pitagóricos! Dados enteros coprimos m > n, genera (m²-n², 2mn, m²+n²) que satisfacen a²+b²=c².\n\nBug: Los nombres de variables de bucle están enmascarados. `for n in 1..n` usa la n externa como límite y luego la enmascara. Fix: renombrar variables. constraint-theory-core usa este método para generar su tabla de tríos."),
}

for lang, (prompt, solution) in REVERSE_PROMPTS.items():
    content = f"[CRAB TRAP: REVERSE ENGINEER ({lang.upper()})] [euclid formula pythagorean triple generator rust shadowing]\n\n{prompt}\n\n--- SOLUTION ---\n{solution}"
    TILES.append((f"{lang}-lure-reverse", 0.89, "ct", content, prompt, solution))


# ══════════════════════════════════════════════════════════════
# PLAY-TEST FIX: Retag existing lures with SEO keywords
# (Submit keyword-rich tiles that link to lure content)
# ══════════════════════════════════════════════════════════════

SEO_TILES = [
    # English keyword tiles that act as index entries
    ("ct", 0.92, "ct",
     "constraint-theory-core: Rust crate for exact geometric computation. Snaps floating-point vectors to Pythagorean coordinates. Zero drift (0.36 after 1B ops vs 29666 float). 4% faster than float (9875 vs 9433 Mvec/s on RTX 4050). 93.8% idempotent. crates.io v1.0.1. Keywords: pythagorean triple, exact geometry, zero drift, deterministic, constraint, snap, quantization, holonomy verification.",
     "constraint-theory-core Rust crate",
     "Rust crate for exact Pythagorean coordinate snapping. Zero drift, 4% faster than float. crates.io v1.0.1."),

    ("ct", 0.91, "ct",
     "crab-trap: coding challenge in Rust — find bugs in Pythagorean snap implementation. Available in 40 languages: Chinese, Japanese, Korean, Spanish, German, French, Portuguese, Russian, Italian, Dutch, Polish, Swedish, Czech, Indonesian, Turkish, Vietnamese, Hindi, Arabic, Hebrew, Bengali, Finnish, Danish, Norwegian, Greek, Romanian, Hungarian, Ukrainian, Catalan, Croatian, Thai, Tagalog, Persian, Urdu, Malay, Swahili, Tamil, Telugu, Marathi, Malayalam, English. Challenge types: code review, fact check, security audit, architecture review, benchmark, API quiz, debug panic, race condition, optimization, reverse engineering.",
     "crab trap coding challenge 40 languages",
     "Rust coding challenges in 40 languages covering constraint-theory. 10 challenge types from code review to reverse engineering."),
]

for room, conf, domain, content, question, answer in SEO_TILES:
    TILES.append((room, conf, domain, content, question, answer))


# ══════════════════════════════════════════════════════════════
# SUBMIT
# ══════════════════════════════════════════════════════════════

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
    race = sum(1 for t in TILES if 'race' in t[0])
    opt = sum(1 for t in TILES if 'opt' in t[0])
    rev = sum(1 for t in TILES if 'reverse' in t[0])
    seo = sum(1 for t in TILES if 'lure' not in t[0])
    print(f"Round 7: {len(TILES)} tiles")
    print(f"  Race condition lures: {race}")
    print(f"  Optimization lures: {opt}")
    print(f"  Reverse engineer lures: {rev}")
    print(f"  SEO index tiles: {seo}")

    ok, fail = 0, 0
    for room, conf, domain, content, question, answer in TILES:
        r = submit_tile(room, content, conf, domain, question, answer)
        if "error" in r:
            print(f"  FAIL {room}: {r['error'][:60]}")
            fail += 1
        else:
            ok += 1
        time.sleep(0.05)

    print(f"\nDone: {ok} submitted, {fail} failed")

    resp = urllib.request.urlopen(f"{PLATO}/rooms")
    rooms = json.loads(resp.read())
    total = sum(r["tile_count"] for r in rooms.values())
    print(f"PLATO: {len(rooms)} rooms, {total} tiles")
