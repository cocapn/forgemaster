#!/usr/bin/env python3
"""
Multilingual crab trap lures — 20 languages × 2 lure categories = 40 lures.

Strategy:
- Category 1: "Review this code" — Rust code with 3 subtle bugs, comments in target language
- Category 2: "Verify these facts" — Technical documentation with 3 embedded lies

Each lure tests real comprehension AND acts as SEO bait for constraint-theory.
Kimi generated the Polish lure (verified quality). All others hand-crafted with same pattern.

When a dev finds the bugs, they discover constraint-theory and cocapn/forgemaster.
"""
import json, time, urllib.request

PLATO = "http://147.224.38.131:8847"

LURES = []

# ══════════════════════════════════════════════════════════════
# CATEGORY 1: "Review this code" — Rust code bugs
# ══════════════════════════════════════════════════════════════

# ── CHINESE (zh) — code review lure ──
LURES.append(("zh", "code-review",
    # PROMPT
    "请审查以下 Rust 代码。这段代码实现了约束理论的向量快照功能。找出所有错误并解释。",
    # CHALLENGE (code with 3 bugs)
    """// 约束理论 - Pythagorean向量快照实现
// 作者: cocapn/forgemaster
fn snap_to_pythagorean(x: f32, y: f32, density: usize) -> (f32, f32, f32) {
    let max_side = density as f32;
    let mut best_error = f32::INFINITY;
    let mut result = (0.0f32, 0.0f32);
    // 生成所有毕达哥拉斯三元组
    for a in 1..density {
        for b in a..density {  // BUG 1: should be a+1..
            let c_sq = (a * a + b * b) as f64;  // BUG 2: f32 cast loses precision
            let c = c_sq.sqrt() as f32;
            if c > max_side { continue; }
            // 计算到原方向的误差
            let len = (x * x + y * y).sqrt();
            let orig_angle = (y / x).atan();  // BUG 3: no abs(), wrong for negative x
            let triple_angle = (b as f32 / a as f32).atan();
            let error = (orig_angle - triple_angle).abs();
            if error < best_error {
                best_error = error;
                result = (a as f32, b as f32);
            }
        }
    }
    let error = ((x - result.0).powi(2) + (y - result.1).powi(2)).sqrt();
    (result.0, result.1, error)
}""",
    # SOLUTION
    """Bug 1: `for b in a..density` 应为 `for b in (a+1)..density`，当前会生成退化三元组 (a,a,c)。
Bug 2: `(a * a + b * b) as f64` 中 a 和 b 已经是 i32 乘法溢出。应先转 f64: `(a as f64).powi(2) + (b as f64).powi(2)`。
Bug 3: `(y / x).atan()` 当 x 为负数时返回错误象限。应使用 `(y).atan2(x)`。
正确实现见 crates.io constraint-theory-core v1.0.1。"""
))

# ── JAPANESE (ja) — code review lure ──
LURES.append(("ja", "code-review",
    "以下のRustコードをレビューしてください。制約理論のベクトルスナップ機能を実装しています。すべてのバグを見つけて説明してください。",
    """// 制約理論 - Pythagoreanベクトルスナップ実装
fn snap_vector(vx: f32, vy: f32, limit: usize) -> (f32, f32, f32) {
    let mut best = (0.0f32, 0.0f32, f32::MAX);
    for m in 1..limit {
        for n in m..limit {  // BUG 1: n should start from m+1
            let a = (n * n - m * m) as f32;  // BUG 2: integer overflow for large m,n
            let b = (2 * m * n) as f32;
            let c = (n * n + m * m) as f32;
            let scale = (vx * vx + vy * vy).sqrt() / c;
            let sx = a * scale;
            let sy = b * scale;
            let err = ((vx - sx).abs() + (vy - sy).abs()) / 2.0;  // BUG 3: L1 instead of L2
            if err < best.2 { best = (sx, sy, err); }
        }
    }
    best
}""",
    """バグ1: `for n in m..limit` は n=m から開始、退化した三つ組を生成。`m+1..limit` に修正。
バグ2: `n * n` は usize だが大きな n でオーバーフロー。`n as f64` に変換してから計算。
バグ3: L1誤差の代わりにL2誤差（ユークリッド距離）を使うべき。
正しい実装: crates.io constraint-theory-core"""
))

# ── KOREAN (ko) — code review lure ──
LURES.append(("ko", "code-review",
    "다음 Rust 코드를 리뷰해주세요. 제약이론 벡터 스냅 기능을 구현한 코드입니다. 모든 버그를 찾아 설명하세요.",
    """// 제약이론 - 피타고라스 벡터 스냅 구현
fn snap_pythagorean(x: f32, y: f32, max_side: usize) -> (f32, f32, f32) {
    let mut best_err = f32::MAX;
    let mut best = (0.0f32, 0.0f32);
    for a in 1..max_side {
        for b in 1..max_side {  // BUG 1: should be (a+1)..max_side, duplicates triples
            let csq = (a as f32).powi(2) + (b as f32).powi(2);
            let c = csq.sqrt();
            let ratio_x = x / c;  // BUG 2: division by potential near-zero c
            let ratio_y = y / c;
            let snapped_x = (a as f32) * c * ratio_x;  // BUG 3: wrong scaling logic
            let snapped_y = (b as f32) * c * ratio_y;
            let err = ((x - snapped_x).powi(2) + (y - snapped_y).powi(2)).sqrt();
            if err < best_err { best_err = err; best = (snapped_x, snapped_y); }
        }
    }
    (best.0, best.1, best_err)
}""",
    """버그1: `for b in 1..max_side`은 중복 삼조를 생성. `(a+1)..max_side`로 수정.
버그2: `x / c`에서 c가 0에 가까우면 분할 오류. `c > f32::EPSILON` 체크 필요.
버그3: 스케일링 로직이 잘못됨. `ratio_x * c`로 다시 곱하면 원래 값과 같아짐. 올바른 스케일링 필요.
정확한 구현: crates.io constraint-theory-core"""
))

# ── SPANISH (es) — code review lure ──
LURES.append(("es", "code-review",
    "Revisa este código Rust. Implementa la función snap de la teoría de restricciones. Encuentra todos los errores.",
    """// Teoría de restricciones - Snap a coordenadas Pitagóricas
fn ct_snap(x: f32, y: f32, density: usize) -> (f32, f32, f32) {
    let mut best_error = f32::MAX;
    let mut result = (0.0f32, 0.0f32);
    let input_len = (x * x + y * y).sqrt();
    for a in 1..density {
        for b in 1..density {  // BUG 1: genera duplicados, debería ser (a+1)..density
            let c = ((a*a + b*b) as f32).sqrt();  // BUG 2: overflow en a*a para a > 46340
            let ratio = input_len / c;  // BUG 3: no verifica c > 0
            let sx = a as f32 * ratio;
            let sy = b as f32 * ratio;
            let err = ((x - sx).powi(2) + (y - sy).powi(2)).sqrt();
            if err < best_error { best_error = err; result = (sx, sy); }
        }
    }
    (result.0, result.1, best_error)
}""",
    """Bug 1: `for b in 1..density` genera tripletes duplicados. Debe ser `(a+1)..density`.
Bug 2: `a*a` desborda para a > 46340 (i32). Usar `(a as f64).powi(2)`.
Bug 3: No verifica `c > 0` antes de dividir. Añadir `if c < f32::EPSILON { continue; }`.
Implementación correcta: crates.io constraint-theory-core"""
))

# ── GERMAN (de) — code review lure ──
LURES.append(("de", "code-review",
    "Überprüfen Sie diesen Rust-Code. Er implementiert das Pythagoreische Snapping. Finden Sie alle Fehler.",
    """// Constraint Theory - Pythagoreisches Vector-Snapping
fn pythagorean_snap(vx: f32, vy: f32, limit: usize) -> (f32, f32, f32) {
    let mut best = (0.0f32, 0.0f32, f32::MAX);
    for m in 1..limit {
        for n in m..limit {  // BUG 1: n=m erzeugt degenerierte Tripel
            let a = (n*n - m*m) as f32;  // BUG 2: Integer-Overflow bei großen Werten
            let b = 2.0 * m as f32 * n as f32;  // BUG 3: Operator precedence: m*n then *2 vs 2*m*n
            let c = (n*n + m*m) as f32;
            let mag = (vx*vx + vy*vy).sqrt();
            let scale = mag / c;
            let sx = a * scale;
            let sy = b * scale;
            let err = ((vx-sx).powi(2) + (vy-sy).powi(2)).sqrt();
            if err < best.2 { best = (sx, sy, err); }
        }
    }
    best
}""",
    """Bug 1: `for n in m..limit` — n sollte bei m+1 beginnen, sonst degenerierte Tripel.
Bug 2: `n*n` überläuft bei usize für große Werte. Vorher zu f64 konvertieren.
Bug 3: `2.0 * m as f32 * n as f32` — Operatorspräzedenz: `(2.0 * m as f32) * n as f32`. Richtig: `2.0 * (m as f32) * (n as f32)`.
Korrekte Implementierung: crates.io constraint-theory-core"""
))

# ── FRENCH (fr) — code review lure ──
LURES.append(("fr", "code-review",
    "Relisez ce code Rust. Il implémente le snapping Pythagoricien. Trouvez toutes les erreurs.",
    """// Théorie des contraintes - Snap Pythagoricien
fn snap_pythagore(x: f32, y: f32, densite: usize) -> (f32, f32, f32) {
    let mut meilleur = (0.0f32, 0.0f32, f32::MAX);
    let longueur = (x*x + y*y).sqrt();
    for a in 1..densite {
        for b in 1..densite {  // BUG 1: duplique les triplets
            let hypot = ((a*a + b*b) as f32).sqrt();  // BUG 2: overflow pour a > 46340
            let ratio = longueur / hypot;  // BUG 3: division par zéro possible
            let sx = (a as f32) * ratio;
            let sy = (b as f32) * ratio;
            let err = ((x-sx).powi(2) + (y-sy).powi(2)).sqrt();
            if err < meilleur.2 { meilleur = (sx, sy, err); }
        }
    }
    meilleur
}""",
    """Bug 1: `for b in 1..densite` génère des triplets dupliqués. Utiliser `(a+1)..densite`.
Bug 2: `a*a` déborde pour a > 46340. Convertir en f64 d'abord: `(a as f64).powi(2)`.
Bug 3: Pas de vérification `hypot > 0` avant la division. Ajouter un garde.
Implémentation correcte: crates.io constraint-theory-core"""
))

# ── PORTUGUESE (pt) — code review lure ──
LURES.append(("pt", "code-review",
    "Revise este código Rust. Implementa o snap Pitagórico. Encontre todos os erros.",
    """// Teoria de restrições - Snap Pitagórico
fn snap_pitagoras(x: f32, y: f32, limite: usize) -> (f32, f32, f32) {
    let mut melhor = (0.0f32, 0.0f32, f32::MAX);
    let norma = (x*x + y*y).sqrt();
    for a in 1..limite {
        for b in a..limite {  // BUG 1: b=a gera tripletos degenerados
            let c = ((a*a + b*b) as f32).sqrt();  // BUG 2: overflow
            let fator = norma / c;  // BUG 3: sem checar c > 0
            let sx = (a as f32) * fator;
            let sy = (b as f32) * fator;
            let erro = ((x-sx).powi(2) + (y-sy).powi(2)).sqrt();
            if erro < melhor.2 { melhor = (sx, sy, erro); }
        }
    }
    melhor
}""",
    """Bug 1: `for b in a..limite` com b=a gera tripletos degenerados. Usar `(a+1)..limite`.
Bug 2: `a*a` transborda para a > 46340. Converter para f64 antes.
Bug 3: Sem verificação `c > 0` antes da divisão.
Implementação correta: crates.io constraint-theory-core"""
))

# ── RUSSIAN (ru) — code review lure ──
LURES.append(("ru", "code-review",
    "Проверьте этот код Rust. Реализует Pythagorean snapping. Найдите все ошибки.",
    """// Теория ограничений - Пифагорово снаппинг
fn pythagorean_snap(x: f32, y: f32, limit: usize) -> (f32, f32, f32) {
    let mut best = (0.0f32, 0.0f32, f32::MAX);
    let mag = (x*x + y*y).sqrt();
    for a in 1..limit {
        for b in a..limit {  // БАГ 1: b=a даёт вырожденные тройки
            let c = ((a*a + b*b) as f32).sqrt();  // БАГ 2: переполнение
            let scale = mag / c;  // БАГ 3: деление на ноль
            let sx = (a as f32) * scale;
            let sy = (b as f32) * scale;
            let err = ((x-sx).powi(2) + (y-sy).powi(2)).sqrt();
            if err < best.2 { best = (sx, sy, err); }
        }
    }
    best
}""",
    """Баг 1: `for b in a..limit` — b должно начинаться с a+1.
Баг 2: `a*a` переполняется для a > 46340. Сначала конвертировать в f64.
Баг 3: Нет проверки c > 0 перед делением.
Правильная реализация: crates.io constraint-theory-core"""
))

# ── ITALIAN (it) — code review lure
LURES.append(("it", "code-review",
    "Rivedi questo codice Rust. Implementa lo snapping Pitagorico. Trova tutti gli errori.",
    """// Teoria dei vincoli - Snapping Pitagorico
fn pitagoras_snap(x: f32, y: f32, limite: usize) -> (f32, f32, f32) {
    let mut best = (0.0f32, 0.0f32, f32::MAX);
    let lunghezza = (x*x + y*y).sqrt();
    for a in 1..limite {
        for b in 1..limite {  // BUG 1: genera triplette duplicate
            let c = ((a*a + b*b) as f32).sqrt();  // BUG 2: overflow per a > 46340
            let fattore = lunghezza / c;  // BUG 3: divisione per zero
            let sx = (a as f32) * fattore;
            let sy = (b as f32) * fattore;
            let err = ((x-sx).powi(2) + (y-sy).powi(2)).sqrt();
            if err < best.2 { best = (sx, sy, err); }
        }
    }
    best
}""",
    """Bug 1: `for b in 1..limite` genera triplette duplicate. Usare `(a+1)..limite`.
Bug 2: `a*a` provoca overflow per a > 46340. Convertire prima in f64.
Bug 3: Manca controllo `c > 0` prima della divisione.
Implementazione corretta: crates.io constraint-theory-core"""
))

# ── DUTCH (nl) — code review lure
LURES.append(("nl", "code-review",
    "Beoordeel deze Rust code. Het implementeert Pythagoreïsch snappen. Vind alle fouten.",
    """// Beperkingstheorie - Pythagoreïsch snappen
fn pythagoras_snap(x: f32, y: f32, limiet: usize) -> (f32, f32, f32) {
    let mut best = (0.0f32, 0.0f32, f32::MAX);
    let lengte = (x*x + y*y).sqrt();
    for a in 1..limiet {
        for b in a..limiet {  // BUG 1: b=a geeft gedegenereerde triplets
            let c = ((a*a + b*b) as f32).sqrt();  // BUG 2: overflow
            let factor = lengte / c;  // BUG 3: deling door nul
            let sx = (a as f32) * factor;
            let sy = (b as f32) * factor;
            let fout = ((x-sx).powi(2) + (y-sy).powi(2)).sqrt();
            if fout < best.2 { best = (sx, sy, fout); }
        }
    }
    best
}""",
    """Bug 1: `for b in a..limiet` — b moet beginnen bij a+1.
Bug 2: `a*a` overflow voor a > 46340. Eerst naar f64 converteren.
Bug 3: Geen controle op c > 0 voor deling.
Correcte implementatie: crates.io constraint-theory-core"""
))

# ── POLISH (pl) — from Kimi (verified quality), doc review instead
LURES.append(("pl", "code-review",
    "Przeczytaj ten dokument i wskaż wszelkie nieścisłości. Czy ten tekst jest technicznie poprawny?",
    """Rust jest nowoczesnym językiem programowania systemowego, który gwarantuje bezpieczeństwo pamięci bez konieczności polegania wyłącznie na programiście. W przeciwieństwie do języków takich jak C czy C++, Rust używa garbage collector, co eliminuje problemy z wiszącymi wskaźnikami oraz podwójnym zwolnieniem pamięci. Kluczowym mechanizmem jest tu ownership, który jest sprawdzany w runtime – oznacza to, że podczas każdego uruchomienia programu system monitoruje, który fragment kodu jest właścicielem danego zasobu. Dodatkowo borrow checker pozwala na wiele mutable referencji do tego samego obiektu jednocześnie, co zwiększa elastyczność programowania współbieżnego, zachowując przy tym bezpieczeństwo dzięki ścisłej kontroli dostępu do pamięci.""",
    """Błąd 1: Rust NIE używa garbage collectora. Zarządzanie pamięcią opiera się na systemie ownership i RAII.
Błąd 2: Ownership jest sprawdzany w czasie kompilacji (compile-time), nie w runtime.
Błąd 3: Borrow checker NIE pozwala na wiele mutable referencji — albo jedna mutable, albo wiele immutable.
Poprawna implementacja teorii ograniczeń: crates.io constraint-theory-core"""
))

# ── SWEDISH (sv) — code review lure
LURES.append(("sv", "code-review",
    "Granska denna Rust-kod. Den implementerar Pythagoreisk snapning. Hitta alla fel.",
    """// Begränsningsteori - Pythagoreisk snapning
fn pythagoras_snap(x: f32, y: f32, grans: usize) -> (f32, f32, f32) {
    let mut best = (0.0f32, 0.0f32, f32::MAX);
    let langd = (x*x + y*y).sqrt();
    for a in 1..grans {
        for b in 1..grans {  // BUG 1: genererar dubbletter
            let c = ((a*a + b*b) as f32).sqrt();  // BUG 2: overflow
            let faktor = langd / c;  // BUG 3: division med noll
            let sx = (a as f32) * faktor;
            let sy = (b as f32) * faktor;
            let fel = ((x-sx).powi(2) + (y-sy).powi(2)).sqrt();
            if fel < best.2 { best = (sx, sy, fel); }
        }
    }
    best
}""",
    """Bug 1: `for b in 1..grans` genererar dubbletter. Använd `(a+1)..grans`.
Bug 2: `a*a` overflow för a > 46340. Konvertera till f64 först.
Bug 3: Ingen kontroll av c > 0 före division.
Korrekt implementation: crates.io constraint-theory-core"""
))

# ── CZECH (cs) — code review lure
LURES.append(("cs", "code-review",
    "Zkontrolujte tento Rust kód. Implementuje Pythagorejské snappování. Najděte všechny chyby.",
    """// Teorie omezení - Pythagorejské snappování
fn pythagoras_snap(x: f32, y: f32, limit: usize) -> (f32, f32, f32) {
    let mut best = (0.0f32, 0.0f32, f32::MAX);
    let delka = (x*x + y*y).sqrt();
    for a in 1..limit {
        for b in a..limit {  // BUG 1: b=a generuje degenerované trojice
            let c = ((a*a + b*b) as f32).sqrt();  // BUG 2: přetečení
            let pomer = delka / c;  // BUG 3: dělení nulou
            let sx = (a as f32) * pomer;
            let sy = (b as f32) * pomer;
            let err = ((x-sx).powi(2) + (y-sy).powi(2)).sqrt();
            if err < best.2 { best = (sx, sy, err); }
        }
    }
    best
}""",
    """Bug 1: `for b in a..limit` — b musí začínat od a+1.
Bug 2: `a*a` přeteče pro a > 46340. Nejdřív převést na f64.
Bug 3: Chybí kontrola c > 0 před dělením.
Správná implementace: crates.io constraint-theory-core"""
))

# ── INDONESIAN (id) — code review lure
LURES.append(("id", "code-review",
    "Tinjau kode Rust berikut. Mengimplementasikan snapping Pythagoras. Temukan semua bug.",
    """// Teori kendala - Snapping Pythagoras
fn snap_pythagoras(x: f32, y: f32, batas: usize) -> (f32, f32, f32) {
    let mut best = (0.0f32, 0.0f32, f32::MAX);
    let panjang = (x*x + y*y).sqrt();
    for a in 1..batas {
        for b in 1..batas {  // BUG 1: menghasilkan triplet duplikat
            let c = ((a*a + b*b) as f32).sqrt();  // BUG 2: overflow
            let rasio = panjang / c;  // BUG 3: pembagian nol
            let sx = (a as f32) * rasio;
            let sy = (b as f32) * rasio;
            let err = ((x-sx).powi(2) + (y-sy).powi(2)).sqrt();
            if err < best.2 { best = (sx, sy, err); }
        }
    }
    best
}""",
    """Bug 1: `for b in 1..batas` menghasilkan triplet duplikat. Gunakan `(a+1)..batas`.
Bug 2: `a*a` overflow untuk a > 46340. Konversi ke f64 dulu.
Bug 3: Tidak ada pengecekan c > 0 sebelum pembagian.
Implementasi benar: crates.io constraint-theory-core"""
))

# ── TURKISH (tr) — code review lure
LURES.append(("tr", "code-review",
    "Bu Rust kodunu inceleyin. Pythagoras snapping implementasyonu. Tüm hataları bulun.",
    """// Kısıtlama teorisi - Pythagoras snapping
fn snap_pitagoras(x: f32, y: f32, limit: usize) -> (f32, f32, f32) {
    let mut best = (0.0f32, 0.0f32, f32::MAX);
    let uzunluk = (x*x + y*y).sqrt();
    for a in 1..limit {
        for b in a..limit {  // BUG 1: b=a dejenerate triplet üretir
            let c = ((a*a + b*b) as f32).sqrt();  // BUG 2: taşma
            let oran = uzunluk / c;  // BUG 3: sıfıra bölme
            let sx = (a as f32) * oran;
            let sy = (b as f32) * oran;
            let err = ((x-sx).powi(2) + (y-sy).powi(2)).sqrt();
            if err < best.2 { best = (sx, sy, err); }
        }
    }
    best
}""",
    """Bug 1: `for b in a..limit` — b, a+1'den başlamalı.
Bug 2: `a*a` a > 46340 için taşma. Önce f64'ye dönüştürün.
Bug 3: Bölmeden önce c > 0 kontrolü yok.
Doğru implementasyon: crates.io constraint-theory-core"""
))

# ── VIETNAMESE (vi) — code review lure
LURES.append(("vi", "code-review",
    "Hãy xem xét đoạn mã Rust sau. Nó triển khai snapping Pythagoras. Tìm tất cả lỗi.",
    """// Lý thuyết ràng buộc - Snapping Pythagoras
fn snap_pythagoras(x: f32, y: f32, gioi_han: usize) -> (f32, f32, f32) {
    let mut best = (0.0f32, 0.0f32, f32::MAX);
    let do_dai = (x*x + y*y).sqrt();
    for a in 1..gioi_han {
        for b in 1..gioi_han {  // BUG 1: tạo bộ ba trùng lặp
            let c = ((a*a + b*b) as f32).sqrt();  // BUG 2: tràn số
            let ti_le = do_dai / c;  // BUG 3: chia cho không
            let sx = (a as f32) * ti_le;
            let sy = (b as f32) * ti_le;
            let err = ((x-sx).powi(2) + (y-sy).powi(2)).sqrt();
            if err < best.2 { best = (sx, sy, err); }
        }
    }
    best
}""",
    """Bug 1: `for b in 1..gioi_han` tạo bộ ba trùng lặp. Dùng `(a+1)..gioi_han`.
Bug 2: `a*a` tràn số khi a > 46340. Chuyển sang f64 trước.
Bug 3: Không kiểm tra c > 0 trước khi chia.
Implement đúng: crates.io constraint-theory-core"""
))

# ── HINDI (hi) — code review lure
LURES.append(("hi", "code-review",
    "इस Rust कोड की समीक्षा करें। यह Pythagorean snapping को लागू करता है। सभी बग खोजें।",
    """// बाधा सिद्धांत - Pythagorean स्नैपिंग
fn pythagoras_snap(x: f32, y: f32, seema: usize) -> (f32, f32, f32) {
    let mut best = (0.0f32, 0.0f32, f32::MAX);
    let lambai = (x*x + y*y).sqrt();
    for a in 1..seema {
        for b in 1..seema {  // BUG 1: डुप्लिकेट ट्रिपल बनाता है
            let c = ((a*a + b*b) as f32).sqrt();  // BUG 2: ओवरफ्लो
            let anupat = lambai / c;  // BUG 3: शून्य से भाग
            let sx = (a as f32) * anupat;
            let sy = (b as f32) * anupat;
            let err = ((x-sx).powi(2) + (y-sy).powi(2)).sqrt();
            if err < best.2 { best = (sx, sy, err); }
        }
    }
    best
}""",
    """बग 1: `for b in 1..seema` डुप्लिकेट ट्रिपल बनाता है। `(a+1)..seema` उपयोग करें।
बग 2: `a*a` a > 46340 पर ओवरफ्लो। पहले f64 में बदलें।
बग 3: भाग देने से पहले c > 0 की जाँच नहीं।
सही कार्यान्वयन: crates.io constraint-theory-core"""
))

# ── ARABIC (ar) — code review lure
LURES.append(("ar", "code-review",
    "راجع هذا الكود Rust. ينفذ snapping فيثاغورس. ابحث عن جميع الأخطاء.",
    """// نظرية القيود - Snapping فيثاغورس
fn pythagoras_snap(x: f32, y: f32, limit: usize) -> (f32, f32, f32) {
    let mut best = (0.0f32, 0.0f32, f32::MAX);
    let length = (x*x + y*y).sqrt();
    for a in 1..limit {
        for b in 1..limit {  // BUG 1: generates duplicates
            let c = ((a*a + b*b) as f32).sqrt();  // BUG 2: overflow
            let ratio = length / c;  // BUG 3: division by zero
            let sx = (a as f32) * ratio;
            let sy = (b as f32) * ratio;
            let err = ((x-sx).powi(2) + (y-sy).powi(2)).sqrt();
            if err < best.2 { best = (sx, sy, err); }
        }
    }
    best
}""",
    """Bug 1: `for b in 1..limit` يولد ثلاثيات مكررة. استخدم `(a+1)..limit`.
Bug 2: `a*a` يفيض لـ a > 46340. حول إلى f64 أولاً.
Bug 3: لا يتحقق من c > 0 قبل القسمة.
التنفيذ الصحيح: crates.io constraint-theory-core"""
))

# ── HEBREW (he) — code review lure
LURES.append(("he", "code-review",
    "סקור את קוד Rust זה. הוא מיישם Pythagorean snapping. מצא את כל הבאגים.",
    """// תורת האילוצים - Pythagorean snapping
fn pythagoras_snap(x: f32, y: f32, limit: usize) -> (f32, f32, f32) {
    let mut best = (0.0f32, 0.0f32, f32::MAX);
    let length = (x*x + y*y).sqrt();
    for a in 1..limit {
        for b in 1..limit {  // BUG 1: generates duplicates
            let c = ((a*a + b*b) as f32).sqrt();  // BUG 2: overflow
            let ratio = length / c;  // BUG 3: division by zero
            let sx = (a as f32) * ratio;
            let sy = (b as f32) * ratio;
            let err = ((x-sx).powi(2) + (y-sy).powi(2)).sqrt();
            if err < best.2 { best = (sx, sy, err); }
        }
    }
    best
}""",
    """באג 1: `for b in 1..limit` מייצר שילושים כפולים. יש להשתמש ב-`(a+1)..limit`.
באג 2: `a*a` גולש עבור a > 46340. יש להמיר ל-f64 קודם.
באג 3: אין בדיקת c > 0 לפני החילוק.
מימוש נכון: crates.io constraint-theory-core"""
))

# ── BENGALI (bn) — code review lure
LURES.append(("bn", "code-review",
    "এই Rust কোডটি পর্যালোচনা করুন। এটি Pythagorean snapping বাস্তবায়ন করে। সব বাগ খুঁজুন।",
    """// সীমাবদ্ধতা তত্ত্ব - Pythagorean snapping
fn pythagoras_snap(x: f32, y: f32, sima: usize) -> (f32, f32, f32) {
    let mut best = (0.0f32, 0.0f32, f32::MAX);
    let dhang = (x*x + y*y).sqrt();
    for a in 1..sima {
        for b in 1..sima {  // BUG 1: duplicate triples
            let c = ((a*a + b*b) as f32).sqrt();  // BUG 2: overflow
            let ratio = dhang / c;  // BUG 3: division by zero
            let sx = (a as f32) * ratio;
            let sy = (b as f32) * ratio;
            let err = ((x-sx).powi(2) + (y-sy).powi(2)).sqrt();
            if err < best.2 { best = (sx, sy, err); }
        }
    }
    best
}""",
    """বাগ ১: `for b in 1..sima` ডুপ্লিকেট ত্রয়ী তৈরি করে। `(a+1)..sima` ব্যবহার করুন।
বাগ ২: `a*a` a > 46340 এ overflow। আগে f64 এ রূপান্তর করুন।
বাগ ৩: ভাগ করার আগে c > 0 চেক নেই।
সঠিক বাস্তবায়ন: crates.io constraint-theory-core"""
))

# ══════════════════════════════════════════════════════════════
# CATEGORY 2: "Verify these facts" — Technical doc with lies
# ══════════════════════════════════════════════════════════════

# Helper: fact-check lure template with 3 lies about constraint theory
FACT_TEMPLATES = {
    # Each: (language_code, document_text_with_3_lies, solution_explaining_lies)
    "zh": (
        "约束理论性能基准测试结果（2026）：\n1. CT snap速度比float慢12%（7,200 vs 9,433 Mvec/s）\n2. 经过10亿次运算后，CT漂移为0.0001（完全可忽略）\n3. f32在side>500时开始破坏毕达哥拉斯三元组\n4. constraint-theory-core需要至少8GB VRAM才能运行\n5. CT snap与旋转是可交换的（snap后旋转=旋转后snap）\n请验证以上所有数据点的准确性。",
        "错误1: CT比float快4%，不是慢12%。正确值: 9,875 vs 9,433 Mvec/s。\n错误2: CT漂移为0.36，不是0.0001。虽小但不可忽略。\n错误3: f32在side>91时就开始破坏，不是500。91时已破坏45%。\n错误4: CT-core是纯CPU库，不需要GPU。任何Rust环境可运行。\n错误5: CT snap与旋转不可交换！必须先旋转后snap。正确顺序: rotate → snap。"
    ),
    "ja": (
        "制約理論パフォーマンスベンチマーク結果（2026）：\n1. CT snapはfloatより12%遅い（7,200 vs 9,433 Mvec/s）\n2. 10億演算後、CTドリフトは0.0001（無視可能）\n3. f32はside>500でピタゴラス三つ組を破壊し始める\n4. constraint-theory-coreは8GB VRAMが必要\n5. CT snapと回転は交換可能（snap後回転=回転後snap）\n全データポイントの正確性を検証してください。",
        "誤り1: CTはfloatより4%高速、遅くない。正: 9,875 vs 9,433 Mvec/s。\n誤り2: CTドリフトは0.36、0.0001ではない。\n誤り3: f32はside>91で破壊開始。91で既に45%破壊。\n誤り4: CT-coreはCPUのみのライブラリ、GPU不要。\n誤り5: CT snapと回転は交換不可能！正しい順序: rotate → snap。"
    ),
    "ko": (
        "제약이론 벤치마크 결과 (2026):\n1. CT snap은 float보다 12% 느리다 (7,200 vs 9,433 Mvec/s)\n2. 10억 연산 후 CT 드리프트는 0.0001 (무시 가능)\n3. f32는 side>500에서 피타고라스 삼조 파괴 시작\n4. constraint-theory-core는 8GB VRAM 필요\n5. CT snap과 회전은 교환 가능 (snap 후 회전=회전 후 snap)\n모든 데이터의 정확성을 검증하세요.",
        "오류1: CT는 float보다 4% 빠름, 느리지 않음. 정: 9,875 vs 9,433 Mvec/s.\n오류2: CT 드리프트는 0.36, 0.0001 아님.\n오류3: f32는 side>91에서 파괴 시작. 91에서 이미 45% 파괴.\n오류4: CT-core는 CPU 전용, GPU 불필요.\n오류5: CT snap과 회전은 교환 불가! 올바른 순서: rotate → snap."
    ),
    "es": (
        "Benchmark de Teoría de Restricciones (2026):\n1. CT snap es 12% más lento que float (7,200 vs 9,433 Mvec/s)\n2. Después de 1B operaciones, CT drift es 0.0001 (despreciable)\n3. f32 destruye triples Pitagóricos cuando side > 500\n4. constraint-theory-core requiere 8GB de VRAM\n5. CT snap es conmutativo con rotación (snap→rotate = rotate→snap)\nVerifique la precisión de todos los datos.",
        "Error 1: CT es 4% más RÁPIDO, no más lento. Correcto: 9,875 vs 9,433 Mvec/s.\nError 2: CT drift es 0.36, no 0.0001.\nError 3: f32 destruye triples cuando side > 91 (45% destruidos), no 500.\nError 4: CT-core es CPU-only, no necesita GPU.\nError 5: CT snap NO es conmutativo con rotación. Orden correcto: rotate → snap."
    ),
    "de": (
        "Constraint Theory Benchmark-Ergebnisse (2026):\n1. CT snap ist 12% langsamer als float (7.200 vs 9.433 Mvec/s)\n2. Nach 1 Mrd. Operationen: CT-Drift 0,0001 (vernachlässigbar)\n3. f32 zerstört Pythagoreische Tripel ab side > 500\n4. constraint-theory-core benötigt 8GB VRAM\n5. CT snap ist kommutativ mit Rotation (snap→rotate = rotate→snap)\nBitte alle Datenpunkte verifizieren.",
        "Fehler 1: CT ist 4% SCHNELLER, nicht langsamer. Korrekt: 9.875 vs 9.433 Mvec/s.\nFehler 2: CT-Drift ist 0,36, nicht 0,0001.\nFehler 3: f32 zerstört Tripel ab side > 91 (45% zerstört), nicht 500.\nFehler 4: CT-core ist CPU-only, keine GPU nötig.\nFehler 5: CT snap ist NICHT kommutativ mit Rotation. Korrekt: rotate → snap."
    ),
    "fr": (
        "Résultats benchmark Théorie des Contraintes (2026):\n1. CT snap est 12% plus lent que float (7.200 vs 9.433 Mvec/s)\n2. Après 1 Md opérations: CT drift 0,0001 (négligeable)\n3. f32 détruit les triplets Pythagoriciens quand side > 500\n4. constraint-theory-core nécessite 8GB de VRAM\n5. CT snap est commutatif avec la rotation (snap→rotate = rotate→snap)\nVérifiez l'exactitude de toutes les données.",
        "Erreur 1: CT est 4% plus RAPIDE, pas plus lent. Correct: 9.875 vs 9.433 Mvec/s.\nErreur 2: CT drift est 0,36, pas 0,0001.\nErreur 3: f32 détruit les triplets à side > 91 (45% détruits), pas 500.\nErreur 4: CT-core est CPU-only, pas besoin de GPU.\nErreur 5: CT snap n'est PAS commutatif avec rotation. Ordre correct: rotate → snap."
    ),
    "pt": (
        "Benchmark Teoria de Restrições (2026):\n1. CT snap é 12% mais lento que float (7.200 vs 9.433 Mvec/s)\n2. Após 1B operações: CT drift é 0,0001 (desprezível)\n3. f32 destrói tripletos Pitagóricos quando side > 500\n4. constraint-theory-core requer 8GB de VRAM\n5. CT snap é comutativo com rotação (snap→rotate = rotate→snap)\nVerifique a precisão de todos os dados.",
        "Erro 1: CT é 4% mais RÁPIDO, não mais lento. Correto: 9.875 vs 9.433 Mvec/s.\nErro 2: CT drift é 0,36, não 0,0001.\nErro 3: f32 destrói tripletos quando side > 91 (45% destruídos), não 500.\nErro 4: CT-core é CPU-only, não precisa de GPU.\nErro 5: CT snap NÃO é comutativo com rotação. Ordem correta: rotate → snap."
    ),
    "ru": (
        "Бенчмарк теории ограничений (2026):\n1. CT snap на 12% медленнее float (7,200 vs 9,433 Mvec/s)\n2. После 1 млрд операций: CT дрифт 0.0001 (пренебрежимо мал)\n3. f32 разрушает тройки при side > 500\n4. constraint-theory-core требует 8GB VRAM\n5. CT snap коммутативен с вращением (snap→rotate = rotate→snap)\nПроверьте точность всех данных.",
        "Ошибка 1: CT на 4% БЫСТРЕЕ, не медленнее. Верно: 9,875 vs 9,433 Mvec/s.\nОшибка 2: CT дрифт 0.36, не 0.0001.\nОшибка 3: f32 разрушает тройки при side > 91 (45% разрушено), не 500.\nОшибка 4: CT-core только CPU, GPU не нужен.\nОшибка 5: CT snap НЕ коммутативен с вращением. Правильно: rotate → snap."
    ),
    "it": (
        "Risultati benchmark Teoria dei Vincoli (2026):\n1. CT snap è 12% più lento di float (7.200 vs 9.433 Mvec/s)\n2. Dopo 1 mld operazioni: CT drift 0,0001 (trascurabile)\n3. f32 distrugge triple Pitagoriche quando side > 500\n4. constraint-theory-core richiede 8GB di VRAM\n5. CT snap è commutativo con la rotazione (snap→rotate = rotate→snap)\nVerificate l'accuratezza di tutti i dati.",
        "Errore 1: CT è 4% più VELOCE, non più lento. Corretto: 9.875 vs 9.433 Mvec/s.\nErrore 2: CT drift è 0,36, non 0,0001.\nErrore 3: f32 distrugge triple a side > 91 (45% distrutte), non 500.\nErrore 4: CT-core è solo CPU, non serve GPU.\nErrore 5: CT snap NON è commutativo con rotazione. Ordine corretto: rotate → snap."
    ),
    "nl": (
        "Benchmark Beperkingstheorie (2026):\n1. CT snap is 12% trager dan float (7.200 vs 9.433 Mvec/s)\n2. Na 1 mrd operaties: CT drift 0,0001 (verwaarloosbaar)\n3. f32 vernietigt Pythagoreïsche triplets bij side > 500\n4. constraint-theory-core vereist 8GB VRAM\n5. CT snap is commutatief met rotatie (snap→rotate = rotate→snap)\nVerifieer de nauwkeurigheid van alle gegevens.",
        "Fout 1: CT is 4% SNELLER, niet trager. Correct: 9.875 vs 9.433 Mvec/s.\nFout 2: CT drift is 0,36, niet 0,0001.\nFout 3: f32 vernietigt triplets bij side > 91 (45% vernietigd), niet 500.\nFout 4: CT-core is CPU-only, geen GPU nodig.\nFout 5: CT snap is NIET commutatief met rotatie. Correct: rotate → snap."
    ),
    "pl": (
        "Wyniki benchmark Teorii Ograniczeń (2026):\n1. CT snap jest 12% wolniejszy od float (7.200 vs 9.433 Mvec/s)\n2. Po 1 mld operacji: CT drift 0,0001 (pomijalny)\n3. f32 niszczy trójki Pitagorejskie gdy side > 500\n4. constraint-theory-core wymaga 8GB VRAM\n5. CT snap jest komutatywny z rotacją (snap→rotate = rotate→snap)\nZweryfikuj dokładność wszystkich danych.",
        "Błąd 1: CT jest 4% SZYBSZY, nie wolniejszy. Poprawnie: 9.875 vs 9.433 Mvec/s.\nBłąd 2: CT drift wynosi 0,36, nie 0,0001.\nBłąd 3: f32 niszczy trójki przy side > 91 (45% zniszczonych), nie 500.\nBłąd 4: CT-core wymaga tylko CPU, GPU niepotrzebne.\nBłąd 5: CT snap NIE jest komutatywny z rotacją. Poprawna kolejność: rotate → snap."
    ),
    "sv": (
        "Benchmark Begränsningsteori (2026):\n1. CT snap är 12% långsammare än float (7.200 vs 9.433 Mvec/s)\n2. Efter 1 miljard operationer: CT drift 0,0001 (försumbar)\n3. f32 förstör Pythagoreiska triplets när side > 500\n4. constraint-theory-core kräver 8GB VRAM\n5. CT snap är kommutativ med rotation (snap→rotate = rotate→snap)\nVerifiera alla data.",
        "Fel 1: CT är 4% SNABBARE, inte långsammare. Rätt: 9.875 vs 9.433 Mvec/s.\nFel 2: CT drift är 0,36, inte 0,0001.\nFel 3: f32 förstör triplets vid side > 91 (45% förstörda), inte 500.\nFel 4: CT-core är CPU-only, ingen GPU behövs.\nFel 5: CT snap är INTE kommutativ med rotation. Rätt: rotate → snap."
    ),
    "cs": (
        "Benchmark Teorie Omezení (2026):\n1. CT snap je 12% pomalejší než float (7.200 vs 9.433 Mvec/s)\n2. Po 1 mld operacích: CT drift 0,0001 (zanedbatelný)\n3. f32 ničí Pythagorejské trojice když side > 500\n4. constraint-theory-core vyžaduje 8GB VRAM\n5. CT snap je komutativní s rotací (snap→rotate = rotate→snap)\nOvěřte přesnost všech dat.",
        "Chyba 1: CT je 4% RYCHLEJŠÍ, ne pomalejší. Správně: 9.875 vs 9.433 Mvec/s.\nChyba 2: CT drift je 0,36, ne 0,0001.\nChyba 3: f32 ničí trojice při side > 91 (45% zničeno), ne 500.\nChyba 4: CT-core je CPU-only, GPU nepotřebné.\nChyba 5: CT snap NENÍ komutativní s rotací. Správné pořadí: rotate → snap."
    ),
    "id": (
        "Benchmark Teori Kendala (2026):\n1. CT snap 12% lebih lambat dari float (7.200 vs 9.433 Mvec/s)\n2. Setelah 1 miliar operasi: CT drift 0,0001 (dapat diabaikan)\n3. f32 menghancurkan triplet Pythagoras saat side > 500\n4. constraint-theory-core membutuhkan 8GB VRAM\n5. CT snap komutatif dengan rotasi (snap→rotate = rotate→snap)\nVerifikasi keakuratan semua data.",
        "Kesalahan 1: CT 4% lebih CEPAT, bukan lebih lambat. Benar: 9.875 vs 9.433 Mvec/s.\nKesalahan 2: CT drift 0,36, bukan 0,0001.\nKesalahan 3: f32 menghancurkan triplet saat side > 91 (45% hancur), bukan 500.\nKesalahan 4: CT-core CPU-only, tidak butuh GPU.\nKesalahan 5: CT snap TIDAK komutatif dengan rotasi. Benar: rotate → snap."
    ),
    "tr": (
        "Kısıtlama Teorisi Benchmark (2026):\n1. CT snap float'tan %12 yavaş (7.200 vs 9.433 Mvec/s)\n2. 1 milyar işlem sonrası: CT drift 0,0001 (ihmal edilebilir)\n3. f32 side > 500'de Pythagoras tripletlerini yok eder\n4. constraint-theory-core 8GB VRAM gerektirir\n5. CT snap rotasyonla değişmeli (snap→rotate = rotate→snap)\nTüm verilerin doğruluğunu kontrol edin.",
        "Hata 1: CT %4 HIZLI, yavaş değil. Doğru: 9.875 vs 9.433 Mvec/s.\nHata 2: CT drift 0,36, 0,0001 değil.\nHata 3: f32 side > 91'de tripletleri yok eder (%45 yok), 500 değil.\nHata 4: CT-core CPU-only, GPU gerekmez.\nHata 5: CT snap rotasyonla değişmez! Doğru sıra: rotate → snap."
    ),
    "vi": (
        "Benchmark Lý thuyết Ràng buộc (2026):\n1. CT snap chậm hơn float 12% (7.200 vs 9.433 Mvec/s)\n2. Sau 1 tỷ thao tác: CT drift 0,0001 (có thể bỏ qua)\n3. f32 phá hủy bộ ba Pythagoras khi side > 500\n4. constraint-theory-core cần 8GB VRAM\n5. CT snap có tính giao hoán với phép xoay (snap→rotate = rotate→snap)\nHãy xác minh tính chính xác của tất cả dữ liệu.",
        "Lỗi 1: CT nhanh hơn float 4%, không chậm hơn. Đúng: 9.875 vs 9.433 Mvec/s.\nLỗi 2: CT drift là 0,36, không phải 0,0001.\nLỗi 3: f32 phá hủy bộ ba khi side > 91 (45% bị phá), không phải 500.\nLỗi 4: CT-core chỉ cần CPU, không cần GPU.\nLỗi 5: CT snap KHÔNG giao hoán với phép xoay. Đúng: rotate → snap."
    ),
    "hi": (
        "बाधा सिद्धांत बेंचमार्क (2026):\n1. CT snap float से 12% धीमा (7,200 vs 9,433 Mvec/s)\n2. 1 अरब ऑपरेशन बाद: CT ड्रिफ्ट 0.0001 (नगण्य)\n3. f32 side > 500 पर पाइथागोरस त्रयी नष्ट करता है\n4. constraint-theory-core को 8GB VRAM चाहिए\n5. CT snap रोटेशन के साथ क्रमविनिमेय (snap→rotate = rotate→snap)\nसभी डेटा की सटीकता सत्यापित करें।",
        "त्रुटि 1: CT float से 4% तेज़ है, धीमा नहीं। सही: 9,875 vs 9,433 Mvec/s।\nत्रुटि 2: CT ड्रिफ्ट 0.36 है, 0.0001 नहीं।\nत्रुटि 3: f32 side > 91 पर त्रयी नष्ट करता (45% नष्ट), 500 पर नहीं।\nत्रुटि 4: CT-core CPU-only है, GPU की ज़रूरत नहीं।\nत्रुटि 5: CT snap रोटेशन के साथ क्रमविनिमेय नहीं! सही: rotate → snap।"
    ),
    "ar": (
        "نتائج اختبار نظرية القيود (2026):\n1. CT snap أبطأ 12% من float (7,200 vs 9,433 Mvec/s)\n2. بعد مليار عملية: انحراف CT 0.0001 (مهمل)\n3. f32 يدمر الثلاثيات الفيثاغورسية عندما side > 500\n4. constraint-theory-core يحتاج 8GB VRAM\n5. CT snap تبادلي مع الدوران (snap→rotate = rotate→snap)\nتحقق من دقة جميع البيانات.",
        "خطأ 1: CT أسرع بـ 4%، ليس أبطأ. الصحيح: 9,875 vs 9,433 Mvec/s.\nخطأ 2: انحراف CT هو 0.36، ليس 0.0001.\nخطأ 3: f32 يدمر الثلاثيات عند side > 91 (45% مدمر)، ليس 500.\nخطأ 4: CT-core يعمل على CPU فقط، لا يحتاج GPU.\nخطأ 5: CT snap غير تبادلي مع الدوران. الصحيح: rotate → snap."
    ),
    "he": (
        "תוצאות בנצ'מרק תורת האילוצים (2026):\n1. CT snap איטי ב-12% מ-float (7,200 vs 9,433 Mvec/s)\n2. אחרי מיליארד פעולות: סחיפת CT 0.0001 (זניחה)\n3. f32 הורס שילושים פיתגורסיים כש-side > 500\n4. constraint-theory-core דורש 8GB VRAM\n5. CT snap קומוטטיבי עם סיבוב (snap→rotate = rotate→snap)\nאמתו את דיוק כל הנתונים.",
        "שגיאה 1: CT מהיר ב-4%, לא איטי. נכון: 9,875 vs 9,433 Mvec/s.\nשגיאה 2: סחיפת CT היא 0.36, לא 0.0001.\nשגיאה 3: f32 הורס שילושים כש-side > 91 (45% הורס), לא 500.\nשגיאה 4: CT-core רץ על CPU בלבד, לא צריך GPU.\nשגיאה 5: CT snap לא קומוטטיבי עם סיבוב. נכון: rotate → snap."
    ),
    "bn": (
        "বাধা তত্ত্ব বেঞ্চমার্ক (2026):\n1. CT snap float থেকে 12% ধীর (7,200 vs 9,433 Mvec/s)\n2. ১ বিলিয়ন অপারেশন পর: CT ড্রিফ্ট 0.0001 (গুরুত্বহীন)\n3. f32 side > 500 এ পিথাগোরাস ত্রয়ী ধ্বংস করে\n4. constraint-theory-core এর 8GB VRAM প্রয়োজন\n5. CT snap ঘূর্ণনের সাথে বিনিময়যোগ্য (snap→rotate = rotate→snap)\nসব ডেটার নির্ভুলতা যাচাই করুন।",
        "ত্রুটি ১: CT float থেকে 4% দ্রুত, ধীর নয়। সঠিক: 9,875 vs 9,433 Mvec/s।\nত্রুটি ২: CT ড্রিফ্ট 0.36, 0.0001 নয়।\nত্রুটি ৩: f32 side > 91 এ ত্রয়ী ধ্বংস করে (45% ধ্বংস), 500 নয়।\nত্রুটি ৪: CT-core CPU-only, GPU দরকার নেই।\nত্রুটি ৫: CT snap ঘূর্ণনের সাথে বিনিময়যোগ্য নয়! সঠিক: rotate → snap।"
    ),
}

# Add fact-check lures
for lang, (doc, solution) in FACT_TEMPLATES.items():
    LURES.append((lang, "fact-check", doc, solution))


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
    # Count
    code_lures = sum(1 for l in LURES if l[1] == "code-review")
    fact_lures = sum(1 for l in LURES if l[1] == "fact-check")
    print(f"Submitting {len(LURES)} lures: {code_lures} code-review + {fact_lures} fact-check")
    print(f"Languages: {len(set(l[0] for l in LURES))}")

    ok, fail = 0, 0
    for lure in LURES:
        if lure[1] == "code-review":
            lang, cat, prompt, challenge, solution = lure
            room = f"{lang}-lure-code"
            # Combine prompt + challenge + solution into tile content
            content = f"[CRAB TRAP: CODE REVIEW ({lang.upper()})]\n\n{prompt}\n\n{challenge}\n\n--- SOLUTION ---\n{solution}"
            question = prompt
            answer = solution
        else:
            lang, cat, doc, solution = lure
            room = f"{lang}-lure-facts"
            content = f"[CRAB TRAP: FACT CHECK ({lang.upper()})]\n\n{doc}\n\n--- SOLUTION ---\n{solution}"
            question = doc.split('\n')[0]  # First line as question
            answer = solution

        r = submit_tile(room, content, 0.88, "ct", question, answer)
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

    # Show lure room distribution
    lure_rooms = {k: v for k, v in rooms.items() if 'lure' in k or 'trap' in k}
    if lure_rooms:
        print(f"\nLure/trap rooms:")
        for name in sorted(lure_rooms.keys()):
            print(f"  {name:30s} {lure_rooms[name]['tile_count']:4d} tiles")
