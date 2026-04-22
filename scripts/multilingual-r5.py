#!/usr/bin/env python3
"""
Round 5: Lures for all 30 new languages + WASM/Edge AI tiles + more lure types.

New lure types:
- "Which crate?" lures: identify the right Rust crate for a problem
- "API quiz" lures: which function signature is correct?
- "Debug the panic" lures: find what causes the runtime crash
"""
import json, time, urllib.request

PLATO = "http://147.224.38.131:8847"
TILES = []

# ══════════════════════════════════════════════════════════════
# LURES FOR NEW LANGUAGES (code-review type, adapted per language)
# ══════════════════════════════════════════════════════════════

CODE_LURE_PROMPTS = {
    "fi": ("Tarkista tämä Rust-koodi. Se toteuttaa Pythagoraan snapping. Etsi kaikki virheet.",
           "Bug 1: `for b in 1..limit` luo duplikaatteja. Käytä `(a+1)..limit`.\nBug 2: `a*a` ylivuoto a > 46340. Muuta f64:ksi ensin.\nBug 3: Ei tarkistusta c > 0 ennen jakamista."),
    "da": ("Gennemgå denne Rust-kode. Den implementerer Pythagoreisk snapning. Find alle fejl.",
           "Bug 1: `for b in 1..limit` skaber duplikater. Brug `(a+1)..limit`.\nBug 2: `a*a` overflow for a > 46340. Konverter til f64 først.\nBug 3: Ingen kontrol af c > 0 før division."),
    "no": ("Gjennomgå denne Rust-koden. Den implementerer pytagoreisk snapping. Finn alle feil.",
           "Bug 1: `for b in 1..limit` lager duplikater. Bruk `(a+1)..limit`.\nBug 2: `a*a` overflow for a > 46340. Konverter til f64 først.\nBug 3: Ingen sjekk av c > 0 før divisjon."),
    "el": ("Ελέγξτε αυτόν τον κώδικα Rust. Υλοποιεί Pythagoreian snapping. Βρείτε όλα τα σφάλματα.",
           "Bug 1: `for b in 1..limit` δημιουργεί διπλότυπα. Χρησιμοποιήστε `(a+1)..limit`.\nBug 2: `a*a` overflow για a > 46340. Μετατρέψτε σε f64 πρώτα.\nBug 3: Χωρίς έλεγχο c > 0 πριν τη διαίρεση."),
    "ro": ("Revizuiți acest cod Rust. Implementează snapping Pitagoreic. Găsiți toate erorile.",
           "Bug 1: `for b in 1..limit` generează duplicate. Folosiți `(a+1)..limit`.\nBug 2: `a*a` overflow pentru a > 46340. Convertiți la f64 mai întâi.\nBug 3: Fără verificare c > 0 înainte de împărțire."),
    "hu": ("Ellenőrizze ezt a Rust kódot. Pythagoraszi snapping-et valósít meg. Találja meg az összes hibát.",
           "Bug 1: `for b in 1..limit` duplikátumokat hoz létre. Használja `(a+1)..limit`.\nBug 2: `a*a` túlcsordulás a > 46340 esetén. Konvertáljon f64-re először.\nBug 3: Nincs c > 0 ellenőrzés osztás előtt."),
    "uk": ("Перевірте цей код Rust. Реалізує Піфагорове зчеплення. Знайдіть усі помилки.",
           "Помилка 1: `for b in 1..limit` створює дублікати. Використовуйте `(a+1)..limit`.\nПомилка 2: `a*a` переповнення для a > 46340. Перетворіть на f64 спочатку.\nПомилка 3: Немає перевірки c > 0 перед діленням."),
    "ca": ("Reviseu aquest codi Rust. Implementa snapping Pitagòric. Trobeu tots els errors.",
           "Bug 1: `for b in 1..limit` genera duplicats. Utilitzeu `(a+1)..limit`.\nBug 2: `a*a` overflow per a > 46340. Convertiu a f64 primer.\nBug 3: Sense verificació c > 0 abans de la divisió."),
    "hr": ("Pregledajte ovaj Rust kod. Implementira Pitagorejsko snapanje. Pronađite sve greške.",
           "Bug 1: `for b in 1..limit` stvara duplikate. Koristite `(a+1)..limit`.\nBug 2: `a*a` overflow za a > 46340. Pretvorite u f64 prvo.\nBug 3: Nema provjere c > 0 prije dijeljenja."),
    "th": ("ตรวจสอบโค้ด Rust นี้ มัน implement Pythagorean snapping อยู่ หา bug ทั้งหมด",
           "Bug 1: `for b in 1..limit` สร้างค่าซ้ำ ใช้ `(a+1)..limit`\nBug 2: `a*a` overflow เมื่อ a > 46340 แปลงเป็น f64 ก่อน\nBug 3: ไม่มีการตรวจสอบ c > 0 ก่อนหาร"),
    "tl": ("Suriin ang Rust code na ito. Nag-iimplement ng Pythagorean snapping. Hanapin ang lahat ng bug.",
           "Bug 1: `for b in 1..limit` gumagawa ng duplicate. Gamitin `(a+1)..limit`.\nBug 2: `a*a` overflow para sa a > 46340. I-convert muna sa f64.\nBug 3: Walang check ng c > 0 bago mag-divide."),
    "fa": ("این کد Rust را بررسی کنید. Pythagorean snapping را پیاده‌سازی می‌کند. همه باگ‌ها را پیدا کنید.",
           "باگ ۱: `for b in 1..limit` مقادیر تکراری ایجاد می‌کند. از `(a+1)..limit` استفاده کنید.\nباگ ۲: `a*a` برای a > 46340 سرریز می‌شود. ابتدا به f64 تبدیل کنید.\nباگ ۳: بدون بررسی c > 0 قبل از تقسیم."),
    "ur": ("اس Rust کوڈ کا جائزہ لیں۔ Pythagorean snapping لاگو کرتا ہے۔ تمام bugs تلاش کریں۔",
           "Bug 1: `for b in 1..limit` نقلیں بناتا ہے۔ `(a+1)..limit` استعمال کریں۔\nBug 2: `a*a` a > 46340 پر overflow۔ پہلے f64 میں تبدیل کریں۔\nBug 3: c > 0 کی جانچ بغیر تقسیم۔"),
    "ms": ("Semak kod Rust ini. Ia melaksanakan Pythagorean snapping. Cari semua bug.",
           "Bug 1: `for b in 1..limit` menghasilkan duplikat. Guna `(a+1)..limit`.\nBug 2: `a*a` overflow untuk a > 46340. Tukar ke f64 dahulu.\nBug 3: Tiada semakan c > 0 sebelum pembahagian."),
    "sw": ("Kagua msimbo huu wa Rust. Unatekeleza Pythagorean snapping. Tafuta bug zote.",
           "Bug 1: `for b in 1..limit` hufanya nakala. Tumia `(a+1)..limit`.\nBug 2: `a*a` overflow kwa a > 46340. Badilisha kuwa f64 kwanza.\nBug 3: Hakuna uchambuzi wa c > 0 kabla ya kugawa."),
    "ta": ("இந்த Rust குறியீட்டை சரிபார்க்கவும். Pythagorean snapping செயல்படுத்துகிறது. அனைத்து bug-களையும் கண்டறியவும்.",
           "Bug 1: `for b in 1..limit` நகல்களை உருவாக்குகிறது. `(a+1)..limit` பயன்படுத்தவும்.\nBug 2: `a*a` a > 46340-க்கு overflow. முதலில் f64-ஆக மாற்றவும்.\nBug 3: c > 0 சரிபார்ப்பு இல்லை."),
    "te": ("ఈ Rust కోడ్‌ను తనిఖీ చేయండి. Pythagorean snapping అమలు చేస్తుంది. అన్ని bugలను కనుగొనండి.",
           "Bug 1: `for b in 1..limit` నకిళ్లు సృష్టిస్తుంది. `(a+1)..limit` ఉపయోగించండి.\nBug 2: `a*a` a > 46340 కి overflow. ముందుగా f64 గా మార్చండి.\nBug 3: c > 0 తనిఖీ లేదు."),
    "mr": ("हा Rust कोड तपासा. Pythagorean snapping लागू करतो. सर्व बग शोधा.",
           "बग १: `for b in 1..limit` डुप्लिकेट्स तयार करतो. `(a+1)..limit` वापरा.\nबग २: `a*a` a > 46340 साठी overflow. आधी f64 मध्ये बदला.\nबग ३: c > 0 तपासणी नाही."),
    "ml": ("ഈ Rust കോഡ് പരിശോധിക്കുക. Pythagorean snapping നടപ്പിലാക്കുന്നു. എല്ലാ ബഗ്ഗുകളും കണ്ടെത്തുക.",
           "ബഗ് 1: `for b in 1..limit` ഡൂപ്ലിക്കേറ്റുകൾ ഉണ്ടാക്കുന്നു. `(a+1)..limit` ഉപയോഗിക്കുക.\nബഗ് 2: `a*a` a > 46340 ന് overflow. ആദ്യം f64 ആയി മാറ്റുക.\nബഗ് 3: c > 0 പരിശോധന ഇല്ല."),
}

# Standard buggy code template (same code, different language prompts)
BUGGY_CODE = """fn snap_pythagorean(x: f32, y: f32, limit: usize) -> (f32, f32, f32) {
    let mut best = (0.0f32, 0.0f32, f32::MAX);
    let mag = (x*x + y*y).sqrt();
    for a in 1..limit {
        for b in 1..limit {  // BUG 1
            let c = ((a*a + b*b) as f32).sqrt();  // BUG 2
            let scale = mag / c;  // BUG 3
            let sx = (a as f32) * scale;
            let sy = (b as f32) * scale;
            let err = ((x-sx).powi(2) + (y-sy).powi(2)).sqrt();
            if err < best.2 { best = (sx, sy, err); }
        }
    }
    best
}"""

for lang, (prompt, solution) in CODE_LURE_PROMPTS.items():
    content = f"[CRAB TRAP: CODE REVIEW ({lang.upper()})]\n\n{prompt}\n\n{BUGGY_CODE}\n\n--- SOLUTION ---\n{solution}"
    TILES.append((f"{lang}-lure-code", 0.87, "ct", content, prompt, solution))

# ══════════════════════════════════════════════════════════════
# FACT-CHECK LURES FOR NEW LANGUAGES
# ══════════════════════════════════════════════════════════════

FACT_LURES = {
    "fi": ("constraint-theory suorituskyky (2026):\n1. CT snap on 12% hitaampi kuin float\n2. CT drift 1B ops jälkeen: 0.0001\n3. f32 tuhoaa Pythagoraan triplets kun side > 500\n4. Vaatii 8GB VRAM\n5. CT snap on kommutatiivinen rotaation kanssa\nTarkista kaikki tiedot.",
           "Väärin 1: CT on 4% NOPEAMPI (9,875 vs 9,433 Mvec/s).\nVäärin 2: Drift on 0.36, ei 0.0001.\nVäärin 3: f32 tuhoaa kun side > 91 (45%), ei 500.\nVäärin 4: CPU-only, ei GPU tarvita.\nVäärin 5: Ei kommutatiivinen! Oikea: rotate → snap."),
    "da": ("constraint-theory benchmark (2026):\n1. CT snap er 12% langsommere end float\n2. CT drift efter 1B operationer: 0.0001\n3. f32 ødelægger Pythagoreiske triplets ved side > 500\n4. Kræver 8GB VRAM\n5. CT snap er kommutativ med rotation\nVerificer alle data.",
           "Forkert 1: CT er 4% HURTIGERE (9.875 vs 9.433 Mvec/s).\nForkert 2: Drift er 0.36, ikke 0.0001.\nForkert 3: f32 ødelægger ved side > 91 (45%), ikke 500.\nForkert 4: CPU-only, ingen GPU nødvendig.\nForkert 5: Ikke kommutativ! Rigtigt: rotate → snap."),
    "no": ("constraint-theory benchmark (2026):\n1. CT snap er 12% tregere enn float\n2. CT drift etter 1B operasjoner: 0.0001\n3. f32 ødelegger pytagoreiske triplets ved side > 500\n4. Krever 8GB VRAM\n5. CT snap er kommutativ med rotasjon\nVerifiser alle data.",
           "Feil 1: CT er 4% RASKERE (9.875 vs 9.433 Mvec/s).\nFeil 2: Drift er 0.36, ikke 0.0001.\nFeil 3: f32 ødelegger ved side > 91 (45%), ikke 500.\nFeil 4: CPU-only, ingen GPU nødvendig.\nFeil 5: Ikke kommutativ! Riktig: rotate → snap."),
    "el": ("Αποτελέσματα constraint-theory (2026):\n1. CT snap είναι 12% πιο αργό από float\n2. CT drift μετά από 1B πράξεις: 0.0001\n3. f32 καταστρέφει Pythagόρειες τριάδες όταν side > 500\n4. Απαιτεί 8GB VRAM\n5. CT snap είναι αντιμεταθετικό με περιστροφή\nΕπαληθεύστε όλα τα δεδομένα.",
           "Λάθος 1: CT είναι 4% ΠΙΟ ΓΡΗΓΟΡΟ (9.875 vs 9.433 Mvec/s).\nΛάθος 2: Drift είναι 0.36, όχι 0.0001.\nΛάθος 3: f32 καταστρέφει σε side > 91 (45%), όχι 500.\nΛάθος 4: CPU-only, δεν χρειάζεται GPU.\nΛάθος 5: Δεν είναι αντιμεταθετικό! Σωστό: rotate → snap."),
    "ro": ("Benchmark constraint-theory (2026):\n1. CT snap este cu 12% mai lent decât float\n2. CT drift după 1B operații: 0.0001\n3. f32 distruge triplete Pitagoreice la side > 500\n4. Necesită 8GB VRAM\n5. CT snap este comutativ cu rotația\nVerificați toate datele.",
           "Greșit 1: CT este cu 4% MAI RAPID (9.875 vs 9.433 Mvec/s).\nGreșit 2: Drift este 0.36, nu 0.0001.\nGreșit 3: f32 distruge la side > 91 (45%), nu 500.\nGreșit 4: CPU-only, nu necesită GPU.\nGreșit 5: Nu este comutativ! Corect: rotate → snap."),
    "hu": ("constraint-theory benchmark (2026):\n1. CT snap 12%-kal lassabb mint a float\n2. CT drift 1Mrd művelet után: 0.0001\n3. f32 megsemmisíti a Pythagoraszi hármasokat side > 500-nál\n4. 8GB VRAM szükséges\n5. CT snap kommutatív a forgatással\nEllenőrizze az adatokat.",
           "Hiba 1: CT 4%-kal GYORSABB (9.875 vs 9.433 Mvec/s).\nHiba 2: Drift 0.36, nem 0.0001.\nHiba 3: f32 side > 91-nél pusztít (45%), nem 500-nál.\nHiba 4: CPU-only, GPU nem szükséges.\nHiba 5: Nem kommutatív! Helyes: rotate → snap."),
    "uk": ("Бенчмарк constraint-theory (2026):\n1. CT snap на 12% повільніший за float\n2. CT дрейф після 1 млрд операцій: 0.0001\n3. f32 руйнує трійки при side > 500\n4. Потрібно 8GB VRAM\n5. CT snap комутативний з обертанням\nПеревірте всі дані.",
           "Помилка 1: CT на 4% ШВИДШИЙ (9.875 vs 9.433 Mvec/s).\nПомилка 2: Дрейф 0.36, не 0.0001.\nПомилка 3: f32 руйнує при side > 91 (45%), не 500.\nПомилка 4: CPU-only, GPU не потрібен.\nПомилка 5: Не комутативний! Правильно: rotate → snap."),
    "ca": ("Benchmark constraint-theory (2026):\n1. CT snap és 12% més lent que float\n2. CT drift després de 1B operacions: 0.0001\n3. f32 destrueix triplets Pitagòrics a side > 500\n4. Requereix 8GB VRAM\n5. CT snap és commutatiu amb la rotació\nVerifiqueu totes les dades.",
           "Error 1: CT és 4% MÉS RÀPID (9.875 vs 9.433 Mvec/s).\nError 2: Drift és 0.36, no 0.0001.\nError 3: f32 destrueix a side > 91 (45%), no 500.\nError 4: CPU-only, no cal GPU.\nError 5: No és commutatiu! Correcte: rotate → snap."),
    "hr": ("Benchmark constraint-theory (2026):\n1. CT snap je 12% sporiji od float\n2. CT drift nakon 1M operacija: 0.0001\n3. f32 uništava Pitagorejske trojke pri side > 500\n4. Zahtijeva 8GB VRAM\n5. CT snap je komutativan s rotacijom\nProvjerite sve podatke.",
           "Pogreška 1: CT je 4% BRŽI (9.875 vs 9.433 Mvec/s).\nPogreška 2: Drift je 0.36, ne 0.0001.\nPogreška 3: f32 uništava pri side > 91 (45%), ne 500.\nPogreška 4: CPU-only, GPU nije potreban.\nPogreška 5: Nije komutativan! Ispravno: rotate → snap."),
    "th": ("benchmark constraint-theory (2026):\n1. CT snap ช้ากว่า float 12%\n2. CT drift หลัง 1B ops: 0.0001\n3. f32 ทำลาย Pythagorean triples เมื่อ side > 500\n4. ต้องการ VRAM 8GB\n5. CT snap สลับกันกับการหมุนได้\nตรวจสอบข้อมูลทั้งหมด",
           "ผิด 1: CT เร็วกว่า float 4% (9,875 vs 9,433 Mvec/s)\nผิด 2: drift คือ 0.36 ไม่ใช่ 0.0001\nผิด 3: f32 ทำลายเมื่อ side > 91 (45%) ไม่ใช่ 500\nผิด 4: CPU-only ไม่ต้องการ GPU\nผิด 5: ไม่สลับกันได้! ถูกต้อง: rotate → snap"),
    "tl": ("benchmark constraint-theory (2026):\n1. CT snap ay 12% mas mabagal kaysa float\n2. CT drift pagkatapos ng 1B ops: 0.0001\n3. f32 sumisira sa Pythagorean triples kapag side > 500\n4. Kailangan ng 8GB VRAM\n5. CT snap ay commutative sa rotation\nI-verify ang lahat ng data.",
           "Mali 1: CT ay 4% MAS MABILIS (9,875 vs 9,433 Mvec/s).\nMali 2: Drift ay 0.36, hindi 0.0001.\nMali 3: f32 sumisira sa side > 91 (45%), hindi 500.\nMali 4: CPU-only, hindi kailangan ng GPU.\nMali 5: Hindi commutative! Tama: rotate → snap."),
    "fa": ("بنچمارک constraint-theory (2026):\n1. CT snap 12% کندتر از float است\n2. CT drift بعد از 1 میلیارد عملیات: 0.0001\n3. f32 سه‌تایی‌های فیثاغورس را وقتی side > 500 نابود می‌کند\n4. 8GB VRAM لازم است\n5. CT snap با دوران جابجایی‌پذیر است\nهمه داده‌ها را تأیید کنید.",
           "خطای ۱: CT 4% سریع‌تر است (9,875 vs 9,433 Mvec/s).\nخطای ۲: انحراف 0.36 است، نه 0.0001.\nخطای ۳: f32 وقتی side > 91 نابود می‌کند (45%)، نه 500.\nخطای ۴: فقط CPU، GPU لازم نیست.\nخطای ۵: جابجایی‌پذیر نیست! صحیح: rotate → snap."),
    "ur": ("بینچمارک constraint-theory (2026):\n1. CT snap فلوٹ سے 12% سست ہے\n2. CT drift 1 ارب آپریشنز کے بعد: 0.0001\n3. f32 Pythagorean triples کو side > 500 پر تباہ کرتا ہے\n4. 8GB VRAM ضروری ہے\n5. CT snap گھومنے کے ساتھ تبدیل ہوتا ہے\nتمام ڈیٹا کی تصدیق کریں۔",
           "غلط 1: CT 4% تیز تر ہے (9,875 vs 9,433 Mvec/s)۔\nغلط 2: drift 0.36 ہے، 0.0001 نہیں۔\nغلط 3: f32 side > 91 پر تباہ کرتا ہے (45%)، 500 پر نہیں۔\nغلط 4: CPU-only، GPU ضروری نہیں۔\nغلط 5: تبدیل نہیں ہوتا! درست: rotate → snap۔"),
    "ms": ("benchmark constraint-theory (2026):\n1. CT snap 12% lebih perlahan dari float\n2. CT drift selepas 1B operasi: 0.0001\n3. f32 memusnahkan triplet Pythagoras bila side > 500\n4. Memerlukan 8GB VRAM\n5. CT snap adalah komutatif dengan putaran\nSahkan semua data.",
           "Salah 1: CT 4% LEBIH PANTAS (9,875 vs 9,433 Mvec/s).\nSalah 2: Drift ialah 0.36, bukan 0.0001.\nSalah 3: f32 memusnahkan pada side > 91 (45%), bukan 500.\nSalah 4: CPU-only, tidak perlu GPU.\nSalah 5: Bukan komutatif! Betul: rotate → snap."),
    "sw": ("benchmark constraint-theory (2026):\n1. CT snap ni 12% polepole kuliko float\n2. CT drift baada ya 1B shughuli: 0.0001\n3. f64 inaharibu Pythagoras triplets wakati side > 500\n4. Inahitaji 8GB VRAM\n5. CT snap ni komutative na mzunguko\nThibitisha data zote.",
           "Potofu 1: CT ni 4% HARAKA ZAIDI (9,875 vs 9,433 Mvec/s).\nPotofu 2: Drift ni 0.36, si 0.0001.\nPotofu 3: f32 inaharibu wakati side > 91 (45%), si 500.\nPotofu 4: CPU-only, haina hitaji GPU.\nPotofu 5: Sio komutative! Sahihi: rotate → snap."),
    "ta": ("constraint-theory பெஞ்ச்மார்க் (2026):\n1. CT snap float-ஐ விட 12% மெதுவானது\n2. 1B செயல்பாடுகளுக்குப் பிறகு CT drift: 0.0001\n3. f32 Pythagorean மும்மைகளை side > 500-ல் அழிக்கிறது\n4. 8GB VRAM தேவை\n5. CT snap சுழற்சியுடன் பரிமாற்றம் செய்யலாம்\nஅனைத்து தரவையும் சரிபார்க்கவும்.",
           "தவறு 1: CT 4% வேகமானது (9,875 vs 9,433 Mvec/s).\nதவறு 2: Drift 0.36, 0.0001 அல்ல.\nதவறு 3: f32 side > 91-ல் அழிக்கிறது (45%), 500 அல்ல.\nதவறு 4: CPU-only, GPU தேவையில்லை.\nதவறு 5: பரிமாற்றம் செய்ய முடியாது! சரி: rotate → snap."),
    "te": ("constraint-theory బెంచ్‌మార్క్ (2026):\n1. CT snap float కంటే 12% నెమ్మదిగా ఉంటుంది\n2. 1B ఆపరేషన్ల తర్వాత CT drift: 0.0001\n3. f32 Pythagorean ట్రిపుల్స్‌ను side > 500 వద్ద నాశనం చేస్తుంది\n4. 8GB VRAM అవసరం\n5. CT snap రొటేషన్‌తో మార్పిడి చేయగలదు\nఅన్ని డేటాను ధృవీకరించండి.",
           "తప్పు 1: CT 4% వేగవంతమైనది (9,875 vs 9,433 Mvec/s).\nతప్పు 2: Drift 0.36, 0.0001 కాదు.\nతప్పు 3: f32 side > 91 వద్ద నాశనం (45%), 500 కాదు.\nతప్పు 4: CPU-only, GPU అవసరం లేదు.\nతప్పు 5: మార్పిడి చేయలేదు! సరైనది: rotate → snap."),
    "mr": ("constraint-theory बेंचमार्क (2026):\n1. CT snap float पेक्षा 12% हळू आहे\n2. 1B ऑपरेशन्स नंतर CT drift: 0.0001\n3. f32 Pythagorean त्रयी side > 500 वर नष्ट करतो\n4. 8GB VRAM आवश्यक\n5. CT snap रोटेशनसोबत बदलता येतो\nसर्व डेटा सत्यापित करा.",
           "चूक 1: CT 4% जास्त जलद (9,875 vs 9,433 Mvec/s).\nचूक 2: Drift 0.36 आहे, 0.0001 नाही.\nचूक 3: f32 side > 91 वर नष्ट करतो (45%), 500 वर नाही.\nचूक 4: CPU-only, GPU लागत नाही.\nचूक 5: बदलता येत नाही! बरोबर: rotate → snap."),
    "ml": ("constraint-theory ബെഞ്ച്മാർക്ക് (2026):\n1. CT snap float-നെക്കാൾ 12% മന്ദമാണ്\n2. 1B പ്രവർത്തനങ്ങൾക്ക് ശേഷം CT drift: 0.0001\n3. f32 Pythagorean ട്രിപ്പിളുകൾ side > 500-ൽ നശിപ്പിക്കുന്നു\n4. 8GB VRAM ആവശ്യമാണ്\n5. CT snap റൊട്ടേഷനുമായി കൈമാറ്റം ചെയ്യാം\nഎല്ലാ ഡാറ്റയും തിരസ്കരിക്കുക.",
           "തെറ്റ് 1: CT 4% വേഗതയേറിയതാണ് (9,875 vs 9,433 Mvec/s).\nതെറ്റ് 2: Drift 0.36 ആണ്, 0.0001 അല്ല.\nതെറ്റ് 3: f32 side > 91-ൽ നശിപ്പിക്കുന്നു (45%), 500 അല്ല.\nതെറ്റ് 4: CPU-only, GPU ആവശ്യമില്ല.\nതെറ്റ് 5: കൈമാറ്റം ചെയ്യാൻ കഴിയില്ല! ശരി: rotate → snap."),
}

for lang, (doc, solution) in FACT_LURES.items():
    content = f"[CRAB TRAP: FACT CHECK ({lang.upper()})]\n\n{doc}\n\n--- SOLUTION ---\n{solution}"
    TILES.append((f"{lang}-lure-facts", 0.87, "ct", content, doc.split('\n')[0], solution))


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
    print(f"Round 5: {len(TILES)} tiles")
    print(f"  Code review lures: {sum(1 for t in TILES if 'lure-code' in t[0])}")
    print(f"  Fact check lures: {sum(1 for t in TILES if 'lure-facts' in t[0])}")
    print(f"  Languages: {len(set(t[0].split('-')[0] for t in TILES))}")

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
