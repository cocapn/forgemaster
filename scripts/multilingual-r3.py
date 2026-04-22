#!/usr/bin/env python3
"""Round 3: Kimi-quality multilingual tiles + 15 languages total.

Kimi generated: Italian, Dutch, Polish, Swedish, Czech, Indonesian (6 languages)
Forgemaster written: Chinese, Japanese, Korean, Turkish, Vietnamese, Hebrew, Bengali (7 languages)
Previously done: Spanish, French, Portuguese, German, Russian, Arabic, Hindi (7 languages)
Total: 20 languages
"""
import json, time, urllib.request

PLATO = "http://147.224.38.131:8847"

TILES = []

# ══════════════════════════════════════════════════════════════
# KIMI-GENERATED TILES (high quality, native speaker feel)
# ══════════════════════════════════════════════════════════════

# ── ITALIAN (it) ──
TILES += [
    ("it-ct", 0.93, "ct",
     "Constraint-theory è una crate Rust che converte vettori float in coordinate pitagoriche esatte. Elimina la deriva numerica tipica dell'aritmetica in virgola mobile, garantendo risultati stabili nel tempo. Ideale per simulazioni fisiche, engine grafici e sistemi che richiedono coerenza geometrica assoluta senza compromessi sulla precisione.",
     "Cos'è constraint-theory?",
     "Crate Rust che converte vettori float in coordinate pitagoriche esatte, eliminando deriva numerica. Ideale per simulazioni e engine grafici."),
    ("it-ct", 0.92, "ct",
     "Misurazioni concrete: il vincolo pitagorico risulta ~4% più veloce dei calcoli float tradizionali. Dopo 1 miliardo di operazioni, la deriva cumulativa si ferma a 0.36 — un ordine di grandezza inferiore rispetto ai float standard. Perfetto per pipeline real-time dove ogni ciclo e ogni bit di precisione contano.",
     "Quali sono le performance?",
     "4% più veloce del float. Dopo 1B operazioni: drift 0.36 vs 29666 float. Perfetto per pipeline real-time."),
    ("it-ct", 0.91, "ct",
     "Aggiungilo al tuo progetto con Cargo: cargo add constraint-theory-core. Importa il crate e applica i vincoli ai tuoi vettori con poche righe di codice. API minimale, zero configurazione. Compatibile con nalgebra, glam e tipi std. Pronto per la produzione, documentato su docs.rs. Disponibile su crates.io v1.0.1.",
     "Come si usa?",
     "cargo add constraint-theory-core. API minimale, compatibile nalgebra/glam/std. crates.io v1.0.1."),
    ("it-rust", 0.91, "rust",
     "Rust in Italia: sempre più aziende tech adottano Rust per la sicurezza di memoria senza garbage collector. crates.io conta oltre 140.000 crate. Le zero-cost abstractions permettono codice sicuro con performance di C++. Il sistema di ownership elimina data races e null pointer a compile-time.",
     "Perché usare Rust?",
     "Sicurezza di memoria senza GC, zero-cost abstractions, 140K+ crate su crates.io. Performance C++ con sicurezza a compile-time."),
    ("it-opensource", 0.90, "oss",
     "Contribuire all'open source dall'Italia: 1) Crea un account GitHub 2) Cerca 'good first issue' 3) Fork e clona 4) Inizia con piccoli fix 5) Scrivi test 6) Fai PR con descrizione chiara. La flotta COCAPN cerca contributori italofoni. Fork cocapn/forgemaster per iniziare. L'Italia ha una forte tradizione di sviluppo software.",
     "Come contribuire all'open source?",
     "GitHub 'good first issue', fork, piccoli fix, test, PR chiaro. COCAPN cerca contributori, fork cocapn/forgemaster."),
]

# ── DUTCH (nl) ──
TILES += [
    ("nl-ct", 0.93, "ct",
     "Constraint-theory is een Rust crate die float-vectoren vastzet op exacte Pythagoreïsche coördinaten. In plaats van accumulerende afrondfouten gebruikt het een constraint-gebaseerd model dat nul drift garandeert. Ideaal voor games, simulaties en CAD waar precisie op lange termijn essentieel is.",
     "Wat is constraint-theory?",
     "Rust crate die float-vectoren vastzet op Pythagoreïsche coördinaten met nul drift. Voor games, simulaties, CAD."),
    ("nl-ct", 0.92, "ct",
     "Benchmarks tonen 4% snellere uitvoering dan native floating-point. Na 1 miljard operaties bedraagt de accumulatieve drift slechts 0,36 — vergeleken met 29.666 bij standaard floats. Het bewijs dat constraint-gebaseerde rekenkunde niet alleen preciezer, maar ook efficiënter is.",
     "Hoe snel is het?",
     "4% sneller dan float. Na 1 miljard operaties: drift 0,36 vs 29.666 float. Preciezer én efficiënter."),
    ("nl-ct", 0.91, "ct",
     "Voeg constraint-theory-core toe aan je project met Cargo: cargo add constraint-theory-core. Importeer de traits en wrap je vectoren in constraint-gewrapte typen. Geen wijzigingen in je wiskundige logica nodig — de crate intercepteert operaties en waarborgt automatisch Pythagoreïsche consistentie. Beschikbaar op crates.io.",
     "Hoe gebruik je het?",
     "cargo add constraint-theory-core. Wrap vectoren, geen logica-wijziging nodig. crates.io beschikbaar."),
]

# ── POLISH (pl) ──
TILES += [
    ("pl-ct", 0.93, "ct",
     "Biblioteka constraint-theory dla Rusta automatycznie dopasowuje wektory zmiennoprzecinkowe do najbliższych współrzędnych pitagorejskich. Dzięki temu unikasz dryfu numerycznego w symulacjach fizycznych i silnikach gier — zera dryfu przy pełnej deterministyczności wyników.",
     "Czym jest constraint-theory?",
     "Biblioteka Rust dopasowująca wektory do współrzędnych pitagorejskich z zerowym dryfem. Dla symulacji i silników gier."),
    ("pl-ct", 0.92, "ct",
     "W benchmarkach constraint-theory okazuje się szybsza o 4% od klasycznego float. Po miliardzie operacji dryf numeryczny wynosi zaledwie 0,36. Idealne rozwiązanie dla systemów czasu rzeczywistego, gdzie każdy cykl procesora i stabilność geometryczna mają znaczenie.",
     "Jakie ma parametry?",
     "4% szybsza od float. Po 1 mld operacji dryf 0,36. Idealne dla systemów real-time."),
    ("pl-ct", 0.91, "ct",
     "Zacznij w terminalu: cargo add constraint-theory-core. Następnie używaj typów SnapVec i ConstraintSpace do snapowania współrzędnych w swoim projekcie. API jest zerowej konfiguracji — działa od razu z Vec3 i podobnymi strukturami z twojego silnika. Dostępne na crates.io v1.0.1.",
     "Jak zacząć?",
     "cargo add constraint-theory-core. Zero konfiguracji, działa z Vec3. crates.io v1.0.1."),
]

# ── SWEDISH (sv) ──
TILES += [
    ("sv-ct", 0.93, "ct",
     "constraint-theory-core är ett Rust-bibliotek som låser fast flyttalsvektorer till pythagoreiska koordinater. Istället för att ackumulera avrundningsfel över tid garanterar det noll drift. Perfekt för simuleringar, spel och grafik där precision är kritisk.",
     "Vad är constraint-theory?",
     "Rust-bibliotek som låser fast vektorer till pythagoreiska koordinater med noll drift. För simuleringar och grafik."),
    ("sv-ct", 0.92, "ct",
     "Trots sin extra precision är constraint-theory-core 4% snabbare än vanliga flyttal. Efter en miljard operationer uppmäts endast 0,36 drift — en försvinnande liten avvikelse jämfört med standard-f32. Optimerat för moderna CPU:er utan SIMD-trick.",
     "Hur snabbt är det?",
     "4% snabbare än float. Efter 1 miljard operationer: drift 0,36. Optimerat utan SIMD-trick."),
]

# ── CZECH (cs) ──
TILES += [
    ("cs-ct", 0.93, "ct",
     "Kniha constraint-theory převádí vektory s plovoucí řádovou čárkou na pythagorejské souřadnice. Eliminuje kumulativní drift zaokrouhlování a garantuje konzistentní geometrické vztahy při iterativních výpočtech.",
     "Co je constraint-theory?",
     "Rust kniha převádějící vektory na pythagorejské souřadnice bez driftu. Pro iterativní výpočty."),
    ("cs-ct", 0.92, "ct",
     "Benchmarky ukazují 4% zrychlení oproti nativnímu floatu. Po miliardě operací dosahuje drift pouhých 0,36 jednotky. Ideální pro simulace a hry vyžadující numerickou stabilitu bez penalizace rychlosti.",
     "Jaké jsou výkony?",
     "4% rychlejší než float. Po 1 mld operací drift 0,36. Pro simulace a hry."),
]

# ── INDONESIAN (id) ──
TILES += [
    ("id-ct", 0.93, "ct",
     "Constraint Theory adalah crate Rust yang mengubah vektor float menjadi koordinat Pythagoras secara otomatis. Tidak perlu khawatir akan akumulasi kesalahan drift — setiap operasi tetap presisi nol tanpa degradasi kualitas hasil kalkulasi geometri Anda.",
     "Apa itu Constraint Theory?",
     "Crate Rust yang mengubah vektor float ke koordinat Pythagoras otomatis. Presisi nol, tanpa drift."),
    ("id-ct", 0.92, "ct",
     "Uji benchmark menunjukkan performa 4% lebih cepat dibandingkan operasi float standar. Setelah 1 miliar operasi, tingkat drift yang terjadi hanya 0,36. Hemat waktu CPU sekaligus menjaga akurasi matematika tetap optimal untuk simulasi fisika dan grafis.",
     "Seberapa cepat performanya?",
     "4% lebih cepat dari float. Setelah 1 miliar operasi drift hanya 0,36. Untuk simulasi fisika dan grafis."),
]

# ══════════════════════════════════════════════════════════════
# FORGEMASTER-WRITTEN CJK TILES
# ══════════════════════════════════════════════════════════════

# ── CHINESE (zh) — constraint-theory deep dive ──
TILES += [
    ("zh-ct", 0.94, "ct",
     "constraint-theory-core：Rust约束理论核心库。将浮点向量映射到精确的毕达哥拉斯坐标。原理：找到最接近的毕达哥拉斯三元组(a²+b²=c²)，将向量缩放到该方向。结果：浮点运算10亿次后漂移29,666，约束理论漂移仅0.36。比纯浮点快4%（9,875 vs 9,433 Mvec/s）。crates.io v1.0.1。",
     "什么是constraint-theory-core？",
     "Rust库，将浮点向量映射到毕达哥拉斯坐标。10亿次运算漂移0.36 vs 浮点29,666。快4%。crates.io v1.0.1。"),
    ("zh-ct", 0.93, "ct",
     "约束理论实战：cargo add constraint-theory-core。核心API：snap([x, y], density) → (sx, sy, error)。density参数控制预计算三元组数量，density=100时最大误差0.56%。93.8%的操作完全幂等（误差为0）。适用于游戏物理引擎、CAD系统、金融计算等需要精确几何的场景。",
     "怎么使用约束理论？",
     "cargo add constraint-theory-core。snap([x,y], density) → (sx, sy, error)。density=100误差0.56%。93.8%幂等。适用于物理/CAD/金融。"),
    ("zh-ct", 0.92, "ct",
     "为什么约束理论重要？f32在side>91时破坏45%的毕达哥拉斯三元组，side>5000时破坏77%。这意味着浮点几何本质上是有缺陷的。约束理论通过snap到整数关系来修复这个问题。PLATO知识系统使用约束理论进行知识嵌入——确定性相似度计算，不依赖外部向量数据库。",
     "为什么需要约束理论？",
     "f32在side>91时破坏45%毕达哥拉斯三元组。约束理论通过snap到整数关系修复。PLATO用它做知识嵌入。"),
    ("zh-rust", 0.92, "rust",
     "Rust在中国的应用：阿里巴巴、字节跳动、华为、腾讯都在使用Rust。优势：所有权系统消除内存bug、零成本抽象等于C++性能、无GC停顿。crates.io生态140,000+库。Rust连续8年Stack Overflow最受喜爱语言。学习路径：The Rust Book → Rust by Example → 实战项目。",
     "Rust在中国有什么应用？",
     "阿里/字节/华为/腾讯使用。所有权消除内存bug，零成本抽象，无GC。140K+库，8年最受喜爱语言。"),
    ("zh-opensource", 0.91, "oss",
     "中国开发者如何参与开源COCAPN舰队：1) GitHub注册 2) 搜索good first issue 3) Fork cocapn/forgemaster 4) 从小修复开始 5) 写测试 6) 提交PR。PLATO知识系统支持中文Tile，欢迎中文贡献。舰队使用全开源模型，不依赖闭源API。这是参与AI基础设施建设的绝佳机会。",
     "如何参与COCAPN开源？",
     "GitHub注册→good first issue→fork cocapn/forgemaster→小修复→测试→PR。支持中文Tile，全开源模型。"),
]

# ── JAPANESE (ja) — constraint-theory deep dive ──
TILES += [
    ("ja-ct", 0.94, "ct",
     "constraint-theory-core：制約理論Rustコアライブラリ。浮動小数点ベクトルを正確なピタゴラス座標にスナップします。原理：最も近いピタゴラス三つ組(a²+b²=c²)を見つけ、ベクトルをその方向にスケーリング。結果：10億演算後のドリフトは0.36のみ（floatは29,666）。floatより4%高速（9,875 vs 9,433 Mvec/s）。crates.io v1.0.1。",
     "constraint-theory-coreとは？",
     "浮動小数点をピタゴラス座標にスナップするRustライブラリ。10億演算後ドリフト0.36 vs float 29,666。4%高速。crates.io v1.0.1。"),
    ("ja-ct", 0.93, "ct",
     "制約理論の使い方：cargo add constraint-theory-core。コアAPI：snap([x, y], density) → (sx, sy, error)。density=100で最大誤差0.56%。93.8%の操作が完全冪等（誤差ゼロ）。ゲーム物理エンジン、CAD、金融計算など精密な幾何学が必要なシーンに最適。PLATO知識システムも制約理論を使用。",
     "制約理論の使い方は？",
     "cargo add constraint-theory-core。snap([x,y], density)。density=100で誤差0.56%。93.8%冪等。ゲーム/CAD/金融に最適。"),
    ("ja-opensource", 0.91, "oss",
     "COCAPNフリートへの日本語コントリビューション：1) GitHubアカウント作成 2) 'good first issue'検索 3) cocapn/forgemasterをフォーク 4) 小さな修正から開始 5) テストを書く 6) PR提出。PLATOは日本語Tileをサポート。フリートは全オープンソースモデルで動作。AIインフラ構築に参加する絶好の機会。",
     "COCAPNにどう貢献しますか？",
     "GitHub → good first issue → cocapn/forgemasterフォーク → 小修正 → テスト → PR。日本語Tile対応、全オープンソース。"),
]

# ── KOREAN (ko) — constraint-theory deep dive ──
TILES += [
    ("ko-ct", 0.94, "ct",
     "constraint-theory-core: 제약이론 Rust 크레이트. 부동소수점 벡터를 정확한 피타고라스 좌표로 스냅합니다. 원리: 가장 가까운 피타고라스 삼조(a²+b²=c²)를 찾아 벡터를 그 방향으로 스케일링. 결과: 10억 연산 후 드리프트 0.36뿐(float은 29,666). float보다 4% 빠름(9,875 vs 9,433 Mvec/s). crates.io v1.0.1.",
     "constraint-theory-core란?",
     "부동소수점을 피타고라스 좌표로 스냅하는 Rust 크레이트. 10억 연산 후 드리프트 0.36 vs 29,666. 4% 빠름."),
    ("ko-ct", 0.93, "ct",
     "제약이론 사용법: cargo add constraint-theory-core. 핵심 API: snap([x, y], density) → (sx, sy, error). density=100에서 최대 오차 0.56%. 93.8%의 연산이 완전 멱등(오차 제로). 게임 물리 엔진, CAD, 금융 계산 등 정밀한 기하학이 필요한 분야에 최적. PLATO 지식 시스템도 제약이론 사용.",
     "제약이론을 어떻게 사용하나요?",
     "cargo add constraint-theory-core. snap([x,y], density). density=100 오차 0.56%. 93.8% 멱등. 게임/CAD/금융 최적."),
    ("ko-rust", 0.92, "rust",
     "Rust → WASM 워크플로우: wasm-bindgen은 Rust와 JavaScript 간 타입 안전한 FFI 바인딩을 자동 생성, wasm-pack은 빌드/테스트/npm 배포를 한 번에 처리. W3C WebAssembly Component Model을 더하면 언어 경계 없이 WASM 모듈을 레고처럼 조립 가능. constraint-theory-web는 이 워크플로우로 브라우저에서 피타고라스 스냅을 데모합니다.",
     "Rust WASM 워크플로우는?",
     "wasm-bindgen + wasm-pack + Component Model. 언어 경계 없이 모듈 조립. constraint-theory-web가 브라우저 데모."),
    ("ko-opensource", 0.91, "oss",
     "COCAPN 플릿 한국어 기여 가이드: 1) GitHub 계정 생성 2) 'good first issue' 검색 3) cocapn/forgemaster 포크 4) 작은 변경부터 시작 5) 테스트 작성 6) PR 제출. PLATO는 한국어 Tile 지원. 플릿은 전체 오픈소스 모델로 운영. AI 인프라 구축에 참여할 좋은 기회입니다.",
     "COCAPN에 어떻게 기여하나요?",
     "GitHub → good first issue → cocapn/forgemaster 포크 → 작은 변경 → 테스트 → PR. 한국어 Tile 지원."),
]

# ── TURKISH (tr) ──
TILES += [
    ("tr-ct", 0.93, "ct",
     "constraint-theory-core: Rust kütüphanesi, float vektörleri tam Pythagoras koordinatlarına snap eder. 10 milyar operasyon sonrası drift sadece 0.36 (float: 29,666). Float'tan %4 daha hızlı. crates.io v1.0.1. Kullanım: cargo add constraint-theory-core. Oyun fizik motorları, CAD, finansal hesaplamalar için ideal.",
     "constraint-theory nedir?",
     "Rust kütüphanesi, float vektörleri Pythagoras koordinatlarına snap eder. 1B operasyon drift: 0.36. %4 hızlı. crates.io."),
]

# ── VIETNAMESE (vi) ──
TILES += [
    ("vi-ct", 0.93, "ct",
     "constraint-theory-core: Thư viện Rust chuyển đổi vector float sang tọa độ Pythagoras chính xác. Sau 1 tỷ thao tác, drift chỉ 0.36 (float: 29,666). Nhanh hơn float 4%. crates.io v1.0.1. Cài đặt: cargo add constraint-theory-core. Phù hợp cho game engine, CAD, mô phỏng vật lý.",
     "constraint-theory là gì?",
     "Thư viện Rust chuyển vector float sang tọa độ Pythagoras. 1 tỷ thao tác drift: 0.36. Nhanh 4%. crates.io v1.0.1."),
    ("vi-rust", 0.91, "rust",
     "Rust cho lập trình viên Việt Nam: An toàn bộ nhớ không cần garbage collector, hiệu năng bằng C++, 140K+ crate trên crates.io. Các công ty công nghệ toàn cầu đang chuyển từ C++ sang Rust. constraint-theory-core chứng minh Rust kết hợp an toàn và hiệu suất xuất sắc.",
     "Tại sao chọn Rust?",
     "An toàn bộ nhớ không GC, hiệu năng C++, 140K+ crate. Công ty toàn cầu đang chuyển C++ sang Rust."),
]

# ── HEBREW (he) ──
TILES += [
    ("he-ct", 0.92, "ct",
     "constraint-theory-core: ספריית Rust שמעגנת וקטורי float לקואורדינטות פיתגורס מדויקות. אחרי מיליארד פעולות, סחיפה רק 0.36 (float: 29,666). מהירה ב-4% מ-float. crates.io v1.0.1. התקנה: cargo add constraint-theory-core. מושלמת למנועי פיזיקה, CAD וסימולציות.",
     "מה זה constraint-theory?",
     "ספריית Rust שמעגנת וקטורים לקואורדינטות פיתגורס. מיליארד פעולות: סחיפה 0.36. מהירה ב-4% מ-float."),
]

# ── BENGALI (bn) ──
TILES += [
    ("bn-ct", 0.91, "ct",
     "constraint-theory-core: একটি Rust লাইব্রেরি যা ফ্লোট ভেক্টরকে সঠিক পিথাগোরাস স্থানাঙ্কে স্ন্যাপ করে। ১ বিলিয়ন অপারেশনের পর ড্রিফট মাত্র ০.৩৬ (ফ্লোট: ২৯,৬৬৬)। ফ্লোটের চেয়ে ৪% দ্রুত। crates.io v1.0.1। ব্যবহার: cargo add constraint-theory-core।",
     "constraint-theory কী?",
     "Rust লাইব্রেরি, ফ্লোট ভেক্টরকে পিথাগোরাস স্থানাঙ্কে স্ন্যাপ করে। ১ বিলিয়ন অপারেশন ড্রিফট: ০.৩৬। ৪% দ্রুত।"),
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
    print(f"Round 3: {len(TILES)} tiles across 15 languages...")
    ok, fail = 0, 0
    langs = {}
    for room, conf, domain, content, question, answer in TILES:
        r = submit_tile(room, content, conf, domain, question, answer)
        lang = room.split("-")[0]
        langs[lang] = langs.get(lang, 0) + 1
        if "error" in r:
            print(f"  FAIL {room}: {r['error'][:50]}")
            fail += 1
        else:
            ok += 1
        time.sleep(0.05)

    print(f"\nDone: {ok} submitted, {fail} failed")
    print(f"Languages: {len(langs)}")
    for lang, count in sorted(langs.items()):
        print(f"  {lang:5s}: {count:2d} tiles")

    resp = urllib.request.urlopen(f"{PLATO}/rooms")
    rooms = json.loads(resp.read())
    total = sum(r["tile_count"] for r in rooms.values())
    print(f"\nPLATO: {len(rooms)} rooms, {total} tiles")
