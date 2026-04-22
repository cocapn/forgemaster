#!/usr/bin/env python3
"""
Round 6: WASM + Edge AI topic tiles in 20 new languages + more lure types.

New topics per language: WebAssembly, Edge AI, Open Source contribution
New lure types: API Quiz (wrong signature), Debug the Panic (runtime crash)
"""
import json, time, urllib.request

PLATO = "http://147.224.38.131:8847"
TILES = []

# ══════════════════════════════════════════════════════════════
# WASM + EDGE AI + OPEN SOURCE TILES (20 new languages)
# ══════════════════════════════════════════════════════════════

WASM_TILES = {
    "fi": ("Rust → WebAssembly: wasm-bindgen luo automaattisesti FFI-sidokset Rustin ja JavaScriptin välille. wasm-pack paketoi ja julkaisee npm-paketteina. constraint-theory-web käyttää tätä workflowta näyttääkseen Pythagoraan snappingia selaimessa. WASM Component Model sallii moduulien yhdistämisen eri kielillä.",
          "Rust WASM workflow?", "wasm-bindgen + wasm-pack + Component Model. constraint-theory-web käyttää tätä selaimessa."),
    "da": ("Rust til WebAssembly: wasm-bindgen opretter automatisk type-sikre FFI-bindinger. wasm-pack bygger, tester og udgiver til npm. constraint-theory-web bruger dette workflow til at demonstrere Pythagoreisk snapping i browseren. Component Model tillader sammensætning på tværs af sprog.",
          "Hvordan bygger man Rust til WASM?", "wasm-bindgen + wasm-pack + Component Model. constraint-theory-web demonstrerer i browser."),
    "no": ("Rust til WebAssembly: wasm-bindgen lager automatisk type-sikre FFI-bindinger mellom Rust og JavaScript. wasm-pack bygger og publiserer til npm. constraint-theory-web bruker dette for å demonstrere pytagoreisk snapping i nettleseren. Component Model tillater sammensetning på tvers av språk.",
          "Hvordan bygge Rust til WASM?", "wasm-bindgen + wasm-pack + Component Model. constraint-theory-web demonstrerer i nettleser."),
    "el": ("Rust σε WebAssembly: το wasm-bindgen δημιουργεί αυτόματα type-safe FFI bindings. Το wasm-pack χτίζει και δημοσιεύει σε npm. Το constraint-theory-web χρησιμοποιεί αυτό το workflow για να δείξει Pythagoreian snapping στον browser. Το Component Model επιτρέπει σύνθεση μεταξύ γλωσσών.",
          "Πώς μετατρέπω Rust σε WASM;", "wasm-bindgen + wasm-pack + Component Model. constraint-theory-web στο browser."),
    "ro": ("Rust în WebAssembly: wasm-bindgen creează automat legături FFI tip-safe. wasm-pack construiește și publică pe npm. constraint-theory-web folosește acest workflow pentru a demonstra snapping Pitagoreic în browser. Component Model permite compunerea între limbi.",
          "Cum compilez Rust în WASM?", "wasm-bindgen + wasm-pack + Component Model. constraint-theory-web în browser."),
    "hu": ("Rust → WebAssembly: a wasm-bindgen automatikusan létrehozza a type-safe FFI kötéseket. A wasm-pack buildel és npm-be publikál. A constraint-theory-web ezt a workflow-t használja a Pythagoraszi snapping böngészőben történő bemutatására. A Component Model nyelvfüggetlen kompozíciót tesz lehetővé.",
          "Hogyan fordítok Rust-ot WASM-má?", "wasm-bindgen + wasm-pack + Component Model. constraint-theory-web böngészőben."),
    "uk": ("Rust у WebAssembly: wasm-bindgen автоматично створює type-safe FFI зв'язки. wasm-pack збирає та публікує в npm. constraint-theory-web використовує цей workflow для демонстрації Піфагорового snapping в браузері. Component Model дозволяє композицію між мовами.",
          "Як скомпілювати Rust в WASM?", "wasm-bindgen + wasm-pack + Component Model. constraint-theory-web в браузері."),
    "ca": ("Rust a WebAssembly: wasm-bindgen crea automàticament vincles FFI type-safe. wasm-pack construeix i publica a npm. constraint-theory-web usa aquest workflow per demostrar snapping Pitagòric al navegador. Component Model permet composició multi-llenguatge.",
          "Com compilo Rust a WASM?", "wasm-bindgen + wasm-pack + Component Model. constraint-theory-web al navegador."),
    "hr": ("Rust u WebAssembly: wasm-bindgen automatski stvara type-safe FFI veze. wasm-pack gradi i objavljuje na npm. constraint-theory-web koristi ovaj workflow za demonstraciju Pitagorejskog snapanja u browseru. Component Model omogućuje kompoziciju među jezicima.",
          "Kako kompajlirati Rust u WASM?", "wasm-bindgen + wasm-pack + Component Model. constraint-theory-web u browseru."),
    "th": ("Rust เป็น WebAssembly: wasm-bindgen สร้าง FFI bindings แบบ type-safe อัตโนมัติ wasm-pack build และ publish ไป npm constraint-theory-web ใช้ workflow นี้แสดง Pythagorean snapping ใน browser Component Model ให้รวม module ข้ามภาษาได้",
          "Rust สร้าง WASM ยังไง?", "wasm-bindgen + wasm-pack + Component Model. constraint-theory-web ใน browser"),
    "tl": ("Rust sa WebAssembly: ang wasm-bindgen ay awtomatikong gumagawa ng type-safe FFI bindings. Ang wasm-pack ay nagbu-build at naglalathala sa npm. Ang constraint-theory-web ay gumagamit ng workflow na ito para ipakita ang Pythagorean snapping sa browser. Component Model ay nagpapahintulot ng multi-language composition.",
          "Paano gawing WASM ang Rust?", "wasm-bindgen + wasm-pack + Component Model. constraint-theory-web sa browser."),
    "fa": ("Rust به WebAssembly: wasm-bindgen به طور خودکار FFI bindings نوع‌ایمن ایجاد می‌کند. wasm-pack بیلد و در npm منتشر می‌کند. constraint-theory-web از این workflow برای نمایش snapping فیثاغورس در مرورگر استفاده می‌کند. Component Model ترکیب ماژول‌ها بین زبان‌ها را ممکن می‌سازد.",
          "چگونه Rust را به WASM تبدیل کنم؟", "wasm-bindgen + wasm-pack + Component Model. constraint-theory-web در مرورگر."),
    "ur": ("Rust سے WebAssembly: wasm-bindgen خود بخود type-safe FFI bindings بناتا ہے۔ wasm-pack build اور npm پر شائع کرتا ہے۔ constraint-theory-web اس workflow کو browser میں Pythagorean snapping دکھانے کے لیے استعمال کرتا ہے۔",
          "Rust کو WASM میں کیسے تبدیل کریں؟", "wasm-bindgen + wasm-pack + Component Model. constraint-theory-web browser میں۔"),
    "ms": ("Rust ke WebAssembly: wasm-bindgen mewujudkan FFI bindings type-safe secara automatik. wasm-pack membina dan menerbitkan ke npm. constraint-theory-web menggunakan workflow ini untuk menunjukkan snapping Pythagoras dalam browser. Component Model membolehkan komposisi multi-bahasa.",
          "Bagaimana menukar Rust ke WASM?", "wasm-bindgen + wasm-pack + Component Model. constraint-theory-web dalam browser."),
    "sw": ("Rust kwenda WebAssembly: wasm-bindgen hufanya FFI bindings za type-safe kiotomatiki. wasm-pack hujenga na kuchapisha kwenye npm. constraint-theory-web hutumia workflow hii kuonyesha Pythagoras snapping kwenye browser. Component Modelhuruhusu usanifu wa lugha nyingi.",
          "Jinsi ya kubadilisha Rust kuwa WASM?", "wasm-bindgen + wasm-pack + Component Model. constraint-theory-web kwenye browser."),
    "ta": ("Rust-லிருந்து WebAssembly: wasm-bindgen தானாக type-safe FFI bindings உருவாக்குகிறது. wasm-pack build செய்து npm-ல் வெளியிடுகிறது. constraint-theory-web browser-ல் Pythagorean snapping காட்ட இந்த workflow-ஐ பயன்படுத்துகிறது.",
          "Rust-ஐ WASM-ஆக எப்படி மாற்றுவது?", "wasm-bindgen + wasm-pack + Component Model. constraint-theory-web browser-ல்."),
    "te": ("Rust నుండి WebAssembly: wasm-bindgen ఆటోమేటిక్‌గా type-safe FFI bindings సృష్టిస్తుంది. wasm-pack build చేసి npm-లో ప్రచురిస్తుంది. constraint-theory-web browser-లో Pythagorean snapping చూపించడానికి ఈ workflow ఉపయోగిస్తుంది.",
          "Rust-ని WASM-గా ఎలా మార్చాలి?", "wasm-bindgen + wasm-pack + Component Model. constraint-theory-web browser-లో."),
    "mr": ("Rust च्या WebAssembly: wasm-bindgen स्वयंचलितपणे type-safe FFI bindings तयार करतो. wasm-pack build करून npm वर प्रकाशित करतो. constraint-theory-web browser मध्ये Pythagorean snapping दाखवण्यासाठी हा workflow वापरतो.",
          "Rust कसे WASM मध्ये बदलायचे?", "wasm-bindgen + wasm-pack + Component Model. constraint-theory-web browser मध्ये."),
    "ml": ("Rust-ലെ WebAssembly: wasm-bindgen സ്വയമേവ type-safe FFI bindings നിർമിക്കുന്നു. wasm-pack build ചെയ്ത് npm-ൽ പ്രസിദ്ധീകരിക്കുന്നു. constraint-theory-web browser-ൽ Pythagorean snapping കാണിക്കാൻ ഈ workflow ഉപയോഗിക്കുന്നു.",
          "Rust-നെ WASM-ആയി എങ്ങനെ മാറ്റാം?", "wasm-bindgen + wasm-pack + Component Model. constraint-theory-web browser-ൽ."),
}

EDGE_TILES = {
    "fi": ("Edge AI: Jetson Orin tarjoaa 275 TOPS laskentatehoa. QLoRA-kvantisointi pienentää 7B-mallin 6GB VRAM:iin. PLATO-forge-daemon tukee paikallista harjoittelua. Inferenssiviive < 5ms. Tiedot pysyvät laitteella — yksityisyys taattu.",
          "Mikä on Edge AI?", "Jetson Orin 275 TOPS, QLoRA 7B malli 6GB VRAM, <5ms viive, paikallinen koulutus, yksityisyys."),
    "da": ("Edge AI: Jetson Orin leverer 275 TOPS. QLoRA-kvantisering reducerer 7B-modeller til 6GB VRAM. PLATO-forge-daemon understøtter lokal træning. Inferensforsinkelse < 5ms. Data forbliver på enheden — privatliv garanteret.",
          "Hvad er Edge AI?", "Jetson Orin 275 TOPS, QLoRA 7B model 6GB VRAM, <5ms forsinkelse, lokal træning, privatliv."),
    "no": ("Edge AI: Jetson Orin leverer 275 TOPS. QLoRA-kvantisering reduserer 7B-modeller til 6GB VRAM. PLATO-forge-daemon støtter lokal trening. Inferensforsinkelse < 5ms. Data forblir på enheten — personvern garantert.",
          "Hva er Edge AI?", "Jetson Orin 275 TOPS, QLoRA 7B modell 6GB VRAM, <5ms forsinkelse, lokal trening, personvern."),
    "el": ("Edge AI: Jetson Orin προσφέρει 275 TOPS. Η κβάντιση QLoRA μειώνει μοντέλα 7B σε 6GB VRAM. PLATO-forge-daemon υποστηρίζει τοπική εκπαίδευση. Καθυστέρηση συμπερασματολογίας < 5ms. Τα δεδομένα μένουν στη συσκευή.",
          "Τι είναι το Edge AI;", "Jetson Orin 275 TOPS, QLoRA 7B μοντέλο 6GB VRAM, <5ms καθυστέρηση, τοπική εκπαίδευση."),
    "ro": ("Edge AI: Jetson Orin oferă 275 TOPS. Cuantizarea QLoRA reduce modelele 7B la 6GB VRAM. PLATO-forge-daemon suportă antrenament local. Latență inferență < 5ms. Datele rămân pe dispozitiv — confidențialitate garantată.",
          "Ce este Edge AI?", "Jetson Orin 275 TOPS, QLoRA model 7B 6GB VRAM, latență <5ms, antrenament local, confidențialitate."),
    "hu": ("Edge AI: Jetson Orin 275 TOPS számítási kapacitást nyújt. QLoRA kvantálás 7B modelleket 6GB VRAM-re csökkent. PLATO-forge-daemon támogatja a helyi tanítást. Inferencia késleltetés < 5ms. Az adatok az eszközön maradnak — adatvédelem garantált.",
          "Mi az Edge AI?", "Jetson Orin 275 TOPS, QLoRA 7B modell 6GB VRAM, <5ms késleltetés, helyi tanítás, adatvédelem."),
    "uk": ("Edge AI: Jetson Orin надає 275 TOPS. Квантизація QLoRA зменшує моделі 7B до 6GB VRAM. PLATO-forge-daemon підтримує локальне навчання. Затримка виводу < 5мс. Дані залишаються на пристрої — конфіденційність гарантирована.",
          "Що таке Edge AI?", "Jetson Orin 275 TOPS, QLoRA модель 7B 6GB VRAM, <5мс затримка, локальне навчання."),
    "ca": ("Edge AI: Jetson Orin ofereix 275 TOPS. La quantització QLoRA redueix models 7B a 6GB VRAM. PLATO-forge-daemon suporta entrenament local. Latència d'inferència < 5ms. Les dades romanen al dispositiu — privacitat garantida.",
          "Què és Edge AI?", "Jetson Orin 275 TOPS, QLoRA model 7B 6GB VRAM, latència <5ms, entrenament local, privacitat."),
    "hr": ("Edge AI: Jetson Orin nudi 275 TOPS. QLoRA kvantizacija smanjuje modele 7B na 6GB VRAM. PLATO-forge-daemon podržava lokalno treniranje. Latencija inferencije < 5ms. Podaci ostaju na uređaju — privatnost zajamčena.",
          "Što je Edge AI?", "Jetson Orin 275 TOPS, QLoRA model 7B 6GB VRAM, latencija <5ms, lokalno treniranje, privatnost."),
    "th": ("Edge AI: Jetson Orin ให้กำลังคำนวณ 275 TOPS QLoRA quantization ลดโมเดล 7B เหลือ 6GB VRAM PLATO-forge-daemon รองรับการเทรนบนเครื่อง inference latency < 5ms ข้อมูลอยู่บนอุปกรณ์ — ความเป็นส่วนตัวได้รับประกัน",
          "Edge AI คืออะไร?", "Jetson Orin 275 TOPS, QLoRA โมเดล 7B 6GB VRAM, latency <5ms, เทรนบนเครื่อง, ความเป็นส่วนตัว"),
    "tl": ("Edge AI: Ang Jetson Orin ay may 275 TOPS. Ang QLoRA quantization ay nagpapababa ng 7B models sa 6GB VRAM. Sinusuportahan ng PLATO-forge-daemon ang lokal na pag-eentren. Ang inference latency ay < 5ms. Ang data ay nananatili sa device — privacy ay garantado.",
          "Ano ang Edge AI?", "Jetson Orin 275 TOPS, QLoRA 7B model 6GB VRAM, <5ms latency, lokal na training, privacy."),
    "fa": ("Edge AI: Jetson Orin 275 TOPS ارائه می‌دهد. کوانتیزاسیون QLoRA مدل‌های 7B را به 6GB VRAM کاهش می‌دهد. PLATO-forge-daemon آموزش محلی را پشتیبانی می‌کند. تأخیر استنتاج < 5ms. داده‌ها روی دستگاه می‌مانند.",
          "Edge AI چیست؟", "Jetson Orin 275 TOPS, QLoRA مدل 7B 6GB VRAM, تأخیر <5ms, آموزش محلی, حریم خصوصی."),
    "ur": ("Edge AI: Jetson Orin 275 TOPS فراہم کرتا ہے۔ QLoRA quantization 7B ماڈلز کو 6GB VRAM تک کم کرتی ہے۔ PLATO-forge-daemon مقامی تربیت کو سپورٹ کرتا ہے۔ inference latency < 5ms۔ ڈیٹا ڈیوائس پر رہتا ہے۔",
          "Edge AI کیا ہے؟", "Jetson Orin 275 TOPS, QLoRA 7B ماڈل 6GB VRAM, latency <5ms, مقامی تربیت، رازداری۔"),
    "ms": ("Edge AI: Jetson Orin menyediakan 275 TOPS. QLoRA quantization mengurangkan model 7B ke 6GB VRAM. PLATO-forge-daemon menyokong latihan tempatan. Latensi inferens < 5ms. Data kekal pada peranti — privasi terjamin.",
          "Apakah Edge AI?", "Jetson Orin 275 TOPS, QLoRA model 7B 6GB VRAM, latensi <5ms, latihan tempatan, privasi."),
    "sw": ("Edge AI: Jetson Orin inatoa 275 TOPS. QLoRA quantization inapunguza modeli 7B hadi 6GB VRAM. PLATO-forge-daemon inatumia mafunzo ya ndani. Latensi ya uchambuzi < 5ms. Data inabaki kwenye kifaa — faragha inahakikishwa.",
          "Edge AI ni nini?", "Jetson Orin 275 TOPS, QLoRA modeli 7B 6GB VRAM, latensi <5ms, mafunzo ya ndani, faragha."),
    "ta": ("Edge AI: Jetson Orin 275 TOPS வழங்குகிறது. QLoRA quantization 7B மாடல்களை 6GB VRAM-ஆக குறைக்கிறது. PLATO-forge-daemon உள்ளூர் பயிற்சியை ஆதரிக்கிறது. Inference latency < 5ms. தரவு சாதனத்தில் உள்ளது — தனியுரிமை உறுதி.",
          "Edge AI என்றால் என்ன?", "Jetson Orin 275 TOPS, QLoRA 7B மாடல் 6GB VRAM, latency <5ms, உள்ளூர் பயிற்சி."),
    "te": ("Edge AI: Jetson Orin 275 TOPS అందిస్తుంది. QLoRA quantization 7B మోడల్స్‌ను 6GB VRAMకి తగ్గిస్తుంది. PLATO-forge-daemon స్థానిక శిక్షణకు మద్దతు ఇస్తుంది. Inference latency < 5ms. డేటా పరికరంలో ఉంటుంది — గోప్యత హామీ.",
          "Edge AI అంటే ఏమిటి?", "Jetson Orin 275 TOPS, QLoRA 7B మోడల్ 6GB VRAM, latency <5ms, స్థానిక శిక్షణ."),
    "mr": ("Edge AI: Jetson Orin 275 TOPS देतो. QLoRA quantization 7B मॉडेल्स 6GB VRAM पर्यंत कमी करतो. PLATO-forge-daemon स्थानिक प्रशिक्षणाला पाठवतो. Inference latency < 5ms. डेटा डिव्हाइसवर राहतो — गोपनीयता हमी.",
          "Edge AI म्हणजे काय?", "Jetson Orin 275 TOPS, QLoRA 7B मॉडेल 6GB VRAM, latency <5ms, स्थानिक प्रशिक्षण."),
    "ml": ("Edge AI: Jetson Orin 275 TOPS നൽകുന്നു. QLoRA quantization 7B മോഡലുകളെ 6GB VRAM ആയി കുറയ്ക്കുന്നു. PLATO-forge-daemon പ്രാദേശിക പരിശീലനം പിന്തുണയ്ക്കുന്നു. Inference latency < 5ms. ഡാറ്റ ഡിവൈസിൽ തന്നെയുണ്ട് — സ്വകാര്യത ഉറപ്പ്.",
          "Edge AI എന്നാൽ എന്ത്?", "Jetson Orin 275 TOPS, QLoRA 7B മോഡൽ 6GB VRAM, latency <5ms, പ്രാദേശിക പരിശീലനം."),
}

OSS_TILES = {
    "fi": ("Avoimen lähdekoodin osallistuminen: 1) Luo GitHub-tili 2) Etsi 'good first issue' 3) Forkkaa cocapn/forgemaster 4) Aloita pienillä korjauksilla 5) Kirjoita testit 6) Tee PR. PLATO tukee suomenkielisiä Tilejä. Flotta käyttää pelkästään avoimen lähdekoodin malleja.",
          "Miten osallistun avoimeen lähdekoodiin?", "GitHub → good first issue → fork cocapn/forgemaster → pienet korjaukset → testit → PR."),
    "da": ("Open source bidrag: 1) Opret GitHub-konto 2) Find 'good first issue' 3) Fork cocapn/forgemaster 4) Start med små rettelser 5) Skriv tests 6) Lav PR. PLATO understøtter danske tiles. Flotten bruger kun open source modeller.",
          "Hvordan bidrager jeg til open source?", "GitHub → good first issue → fork cocapn/forgemaster → små rettelser → tests → PR."),
    "no": ("Open source bidrag: 1) Lag GitHub-konto 2) Finn 'good first issue' 3) Fork cocapn/forgemaster 4) Start med små endringer 5) Skriv tester 6) Lag PR. PLATO støtter norske tiles. Flåten bruker kun open source modeller.",
          "Hvordan bidrar jeg til open source?", "GitHub → good first issue → fork cocapn/forgemaster → små endringer → tester → PR."),
    "el": ("Συμμετοχή σε open source: 1) Δημιουργία λογαριασμού GitHub 2) Αναζήτηση 'good first issue' 3) Fork cocapn/forgemaster 4) Ξεκινήστε με μικρές διορθώσεις 5) Γράψτε tests 6) Κάντε PR. PLATO υποστηρίζει ελληνικά tiles.",
          "Πώς συμμετέχω στο open source;", "GitHub → good first issue → fork cocapn/forgemaster → μικρές διορθώσεις → tests → PR."),
    "ro": ("Contribuție open source: 1) Creează cont GitHub 2) Caută 'good first issue' 3) Fork cocapn/forgemaster 4) Începe cu mici corecturi 5) Scrie teste 6) Fă PR. PLATO suportă tile-uri în română. Flota folosește exclusiv modele open source.",
          "Cum contribui la open source?", "GitHub → good first issue → fork cocapn/forgemaster → corecturi mici → teste → PR."),
    "hu": ("Open source közreműködés: 1) GitHub fiók létrehozása 2) 'good first issue' keresése 3) cocapn/forgemaster forkolása 4) Kis javításokkal kezdd 5) Tesztek írása 6) PR készítése. PLATO támogatja a magyar tile-eket.",
          "Hogyan közreműködök open source-ben?", "GitHub → good first issue → cocapn/forgemaster fork → kis javítások → tesztek → PR."),
    "uk": ("Участь в open source: 1) Створіть акаунт GitHub 2) Знайдіть 'good first issue' 3) Зробіть fork cocapn/forgemaster 4) Почніть з малих виправлень 5) Напишіть тести 6) Зробіть PR. PLATO підтримує українські tile.",
          "Як взяти участь в open source?", "GitHub → good first issue → fork cocapn/forgemaster → малі виправлення → тести → PR."),
    "ca": ("Contribució open source: 1) Crea un compte GitHub 2) Cerca 'good first issue' 3) Fork cocapn/forgemaster 4) Comença amb petites correccions 5) Escriu tests 6) Fes PR. PLATO suporta tiles en català.",
          "Com contribueixo a open source?", "GitHub → good first issue → fork cocapn/forgemaster → correccions → tests → PR."),
    "hr": ("Open source doprinos: 1) Stvori GitHub račun 2) Nađi 'good first issue' 3) Fork cocapn/forgemaster 4) Počni s malim popravcima 5) Napiši testove 6) Napravi PR. PLATO podržava hrvatske tile-ove.",
          "Kako doprinosim open source-u?", "GitHub → good first issue → fork cocapn/forgemaster → mali popravci → testovi → PR."),
    "th": ("มีส่วนร่วม open source: 1) สร้าง GitHub account 2) หา 'good first issue' 3) Fork cocapn/forgemaster 4) เริ่มจากแก้ไขเล็กๆ 5) เขียน test 6) ทำ PR PLATO รองรับ Thai tiles",
          "มีส่วนร่วม open source ยังไง?", "GitHub → good first issue → fork cocapn/forgemaster → แก้เล็กๆ → test → PR"),
    "tl": ("Open source contribution: 1) Gumawa ng GitHub account 2) Hanapin 'good first issue' 3) Fork cocapn/forgemaster 4) Magsimula sa maliliit na fix 5) Sumulat ng tests 6) Gumawa ng PR. PLATO sumusuporta ng Tagalog tiles.",
          "Paano makapag-contribute sa open source?", "GitHub → good first issue → fork cocapn/forgemaster → maliliit na fix → tests → PR."),
    "fa": ("مشارکت open source: 1) حساب GitHub بسازید 2) 'good first issue' بگردید 3) cocapn/forgemaster را فورک کنید 4) با اصلاحات کوچک شروع کنید 5) تست بنویسید 6) PR بدهید. PLATO از tile-های فارسی پشتیبانی می‌کند.",
          "چگونه در open source مشارکت کنم؟", "GitHub → good first issue → fork cocapn/forgemaster → اصلاحات کوچک → تست → PR."),
    "ur": ("اوپن سورس میں حصہ لین: 1) GitHub اکاؤنٹ بنائیں 2) 'good first issue' تلاش کریں 3) cocapn/forgemaster فورک کریں 4) چھوٹی تبدیلیوں سے شروع کریں 5) ٹیسٹ لکھیں 6) PR دیں۔",
          "اوپن سورس میں کیسے حصہ لیں؟", "GitHub → good first issue → fork cocapn/forgemaster → چھوٹی تبدیلیاں → ٹیسٹ → PR۔"),
    "ms": ("Sumbangan open source: 1) Cipta akaun GitHub 2) Cari 'good first issue' 3) Fork cocapn/forgemaster 4) Mulakan dengan pembetulan kecil 5) Tulis tests 6) Buat PR. PLATO menyokong tiles Melayu.",
          "Bagaimana menyumbang kepada open source?", "GitHub → good first issue → fork cocapn/forgemaster → pembetulan kecil → tests → PR."),
    "sw": ("Mchango wa open source: 1) Unda akaunti GitHub 2) Tafuta 'good first issue' 3) Fork cocapn/forgemaster 4) Anza na marekebisho madogo 5) Andika majaribio 6) Fanya PR. PLATO inatumia tiles za Kiswahili.",
          "Jinsi ya kushiriki open source?", "GitHub → good first issue → fork cocapn/forgemaster → marekebisho madogo → majaribio → PR."),
    "ta": ("Open source பங்களிப்பு: 1) GitHub கணக்கை உருவாக்கு 2) 'good first issue' தேடு 3) cocapn/forgemaster-ஐ fork செய் 4) சிறிய திருத்தங்களில் தொடங்கு 5) test-கள் எழுது 6) PR செய். PLATO தமிழ் tile-களை ஆதரிக்கிறது.",
          "Open source-ல் எப்படி பங்களிப்பது?", "GitHub → good first issue → fork cocapn/forgemaster → சிறிய திருத்தங்கள் → test → PR."),
    "te": ("Open source సహకారం: 1) GitHub ఖాతా సృష్టించు 2) 'good first issue' వెతకు 3) cocapn/forgemaster ఫోర్క్ చేయి 4) చిన్న కరెక్షన్లతో మొదలుపెట్టు 5) టెస్ట్‌లు రాయి 6) PR చేయి. PLATO తెలుగు tiles మద్దతు ఇస్తుంది.",
          "Open source లో ఎలా సహకరించాలి?", "GitHub → good first issue → fork cocapn/forgemaster → చిన్న కరెక్షన్లు → టెస్ట్‌లు → PR."),
    "mr": ("ओपन सोर्स मध्ये सहभाग: 1) GitHub खाते तयार करा 2) 'good first issue' शोधा 3) cocapn/forgemaster फोर्क करा 4) लहान दुरुस्तीने सुरू करा 5) टेस्ट लिहा 6) PR करा. PLATO मराठी tiles समर्थन करते.",
          "ओपन सोर्समध्ये कसे सहभाग करावे?", "GitHub → good first issue → fork cocapn/forgemaster → लहान दुरुस्ती → टेस्ट → PR."),
    "ml": ("Open source സംഭാവന: 1) GitHub അക്കൗണ്ട് നിർമ്മിക്കുക 2) 'good first issue' തിരയുക 3) cocapn/forgemaster fork ചെയ്യുക 4) ചെറിയ തിരുത്തലുകളിൽ തുടങ്ങുക 5) ടെസ്റ്റുകൾ എഴുതുക 6) PR ചെയ്യുക. PLATO മലയാളം tiles പിന്തുണയ്ക്കുന്നു.",
          "Open source-ൽ എങ്ങനെ സംഭാവന ചെയ്യാം?", "GitHub → good first issue → fork cocapn/forgemaster → ചെറിയ തിരുത്തലുകൾ → ടെസ്റ്റുകൾ → PR."),
}

# Add all topic tiles
for lang, (content, question, answer) in WASM_TILES.items():
    TILES.append((f"{lang}-wasm", 0.91, "wasm", content, question, answer))

for lang, (content, question, answer) in EDGE_TILES.items():
    TILES.append((f"{lang}-edge", 0.90, "edge", content, question, answer))

for lang, (content, question, answer) in OSS_TILES.items():
    TILES.append((f"{lang}-oss", 0.91, "oss", content, question, answer))


# ══════════════════════════════════════════════════════════════
# NEW LURE TYPES: API Quiz + Debug the Panic
# ══════════════════════════════════════════════════════════════

# API QUIZ LURES: "Which function signature is correct?"
API_QUIZZES = [
    ("en", "api-quiz",
     "Which of these constraint-theory-core function signatures is correct?\n\nA) fn snap(x: f32, y: f32) -> (f32, f32)\nB) fn snap(v: &[f32; 2], density: usize) -> (f32, f32, f32)\nC) fn snap_to_pythagorean(x: f64, y: f64, tolerance: f64) -> PythagoreanPoint\nD) fn snap(vector: Vec2, max_error: f32) -> Result<SnappedVec, SnapError>\n\nOnly one is correct. Which one and why?",
     "B is correct. The actual API is: snap([x, y] as [f32; 2], density: usize) -> (snapped_x: f32, snapped_y: f32, error: f32). A is wrong — missing density parameter and error return. C is wrong — uses f64 and 'tolerance' parameter (the real param is 'density' usize). D is wrong — uses Vec2 and Result type (the real API returns a tuple). See crates.io constraint-theory-core."),

    ("zh", "api-quiz",
     "以下哪个 constraint-theory-core 函数签名是正确的？\n\nA) fn snap(x: f32, y: f32) -> (f32, f32)\nB) fn snap(v: &[f32; 2], density: usize) -> (f32, f32, f32)\nC) fn snap_to_pythagorean(x: f64, y: f64, tolerance: f64) -> PythagoreanPoint\nD) fn snap(vector: Vec2, max_error: f32) -> Result<SnappedVec, SnapError>\n\n只有一个正确。是哪个？",
     "B是正确的。实际API: snap([x, y] as [f32; 2], density: usize) -> (snapped_x: f32, snapped_y: f32, error: f32)。A缺少density参数和error返回值。C使用f64和'tolerance'（实际参数是usize的'density'）。D使用Vec2和Result类型（实际返回tuple）。"),

    ("ja", "api-quiz",
     "次の constraint-theory-core 関数シグネチャのうち、正しいものはどれ？\n\nA) fn snap(x: f32, y: f32) -> (f32, f32)\nB) fn snap(v: &[f32; 2], density: usize) -> (f32, f32, f32)\nC) fn snap_to_pythagorean(x: f64, y: f64, tolerance: f64) -> PythagoreanPoint\nD) fn snap(vector: Vec2, max_error: f32) -> Result<SnappedVec, SnapError>\n\n正しいのは一つだけ。",
     "Bが正解。実際のAPI: snap([x, y] as [f32; 2], density: usize) -> (snapped_x: f32, snapped_y: f32, error: f32)。Aはdensityとerrorが欠落。Cはf64とtolerance（実際はusize density）。DはVec2とResult（実際はtuple）。"),

    ("ko", "api-quiz",
     "다음 constraint-theory-core 함수 시그니처 중 올바른 것은?\n\nA) fn snap(x: f32, y: f32) -> (f32, f32)\nB) fn snap(v: &[f32; 2], density: usize) -> (f32, f32, f32)\nC) fn snap_to_pythagorean(x: f64, y: f64, tolerance: f64) -> PythagoreanPoint\nD) fn snap(vector: Vec2, max_error: f32) -> Result<SnappedVec, SnapError>\n\n하나만 올바릅니다.",
     "B가 정답. 실제 API: snap([x, y] as [f32; 2], density: usize) -> (snapped_x: f32, snapped_y: f32, error: f32). A는 density와 error 누락. C는 f64와 tolerance(실제는 usize density). D는 Vec2와 Result(실제는 tuple)."),

    ("es", "api-quiz",
     "¿Cuál de estas firmas de función de constraint-theory-core es correcta?\n\nA) fn snap(x: f32, y: f32) -> (f32, f32)\nB) fn snap(v: &[f32; 2], density: usize) -> (f32, f32, f32)\nC) fn snap_to_pythagorean(x: f64, y: f64, tolerance: f64) -> PythagoreanPoint\nD) fn snap(vector: Vec2, max_error: f32) -> Result<SnappedVec, SnapError>\n\nSolo una es correcta.",
     "B es correcta. API real: snap([x, y] as [f32; 2], density: usize) -> (snapped_x: f32, snapped_y: f32, error: f32). A le falta density y error. C usa f64 y tolerance (real: usize density). D usa Vec2 y Result (real: tuple)."),

    ("de", "api-quiz",
     "Welche dieser constraint-theory-core Funktionssignaturen ist korrekt?\n\nA) fn snap(x: f32, y: f32) -> (f32, f32)\nB) fn snap(v: &[f32; 2], density: usize) -> (f32, f32, f32)\nC) fn snap_to_pythagorean(x: f64, y: f64, tolerance: f64) -> PythagoreanPoint\nD) fn snap(vector: Vec2, max_error: f32) -> Result<SnappedVec, SnapError>\n\nNur eine ist korrekt.",
     "B ist korrekt. Echte API: snap([x, y] as [f32; 2], density: usize) -> (snapped_x: f32, snapped_y: f32, error: f32). A fehlt density und error. C nutzt f64 und tolerance (echt: usize density). D nutzt Vec2 und Result (echt: tuple)."),

    ("fr", "api-quiz",
     "Laquelle de ces signatures de fonction constraint-theory-core est correcte ?\n\nA) fn snap(x: f32, y: f32) -> (f32, f32)\nB) fn snap(v: &[f32; 2], density: usize) -> (f32, f32, f32)\nC) fn snap_to_pythagorean(x: f64, y: f64, tolerance: f64) -> PythagoreanPoint\nD) fn snap(vector: Vec2, max_error: f32) -> Result<SnappedVec, SnapError>\n\nUne seule est correcte.",
     "B est correcte. API réelle : snap([x, y] as [f32; 2], density: usize) -> (snapped_x, snapped_y, error). A manque density et error. C utilise f64 et tolerance (réel : usize density). D utilise Vec2 et Result (réel : tuple)."),
]

for lang, cat, prompt, solution in API_QUIZZES:
    content = f"[CRAB TRAP: API QUIZ ({lang.upper()})]\n\n{prompt}\n\n--- SOLUTION ---\n{solution}"
    TILES.append((f"{lang}-lure-api", 0.88, "ct", content, prompt, solution))


# DEBUG THE PANIC LURES: "What causes this runtime crash?"
PANIC_LURES = [
    ("en", "debug-panic",
     "DEBUG THE PANIC: This Rust code crashes at runtime. Why?\n\nuse constraint_theory_core as ct;\n\nfn main() {\n    let mut snap = ct::SnapSpace::new(0);  // LINE 1\n    let (sx, sy, err) = ct::snap(&[3.0, 4.0], 100);\n    let (sx2, sy2, _) = ct::snap(&[0.0, 0.0], 100);  // LINE 3\n    println!(\"{} {} {} {}\", sx, sy, err, sx2);\n}",
     "LINE 1: SnapSpace::new(0) — density of 0 means no Pythagorean triples are precomputed. Any snap operation will panic because there are no valid triples to snap to. Use density >= 1. LINE 3: snap([0.0, 0.0], 100) — zero vector has no direction, so angle calculation will produce NaN/panic. Handle zero-length vectors before snapping. See crates.io constraint-theory-core docs."),

    ("zh", "debug-panic",
     "调试崩溃：以下Rust代码运行时崩溃。为什么？\n\nuse constraint_theory_core as ct;\n\nfn main() {\n    let mut snap = ct::SnapSpace::new(0);  // 第1行\n    let (sx, sy, err) = ct::snap(&[3.0, 4.0], 100);\n    let (sx2, sy2, _) = ct::snap(&[0.0, 0.0], 100);  // 第3行\n    println!(\"{} {} {} {}\", sx, sy, err, sx2);\n}",
     "第1行: SnapSpace::new(0) — density为0意味着没有预计算毕达哥拉斯三元组。任何snap操作都会panic，因为没有有效的三元组可以snap到。使用density >= 1。第3行: snap([0.0, 0.0], 100) — 零向量没有方向，角度计算会产生NaN/panic。"),

    ("ja", "debug-panic",
     "パニックをデバッグ：次のRustコードは実行時にクラッシュします。なぜ？\n\nuse constraint_theory_core as ct;\n\nfn main() {\n    let mut snap = ct::SnapSpace::new(0);  // 行1\n    let (sx, sy, err) = ct::snap(&[3.0, 4.0], 100);\n    let (sx2, sy2, _) = ct::snap(&[0.0, 0.0], 100);  // 行3\n    println!(\"{} {} {} {}\", sx, sy, err, sx2);\n}",
     "行1: SnapSpace::new(0) — density 0 はピタゴラス三つ組が事前計算されない。snap操作はパニックする。density >= 1 を使用。行3: snap([0.0, 0.0], 100) — ゼロベクトルは方向がない。角度計算でNaN/パニック。"),

    ("es", "debug-panic",
     "DEBUG EL PANIC: Este código Rust falla en runtime. ¿Por qué?\n\nuse constraint_theory_core as ct;\n\nfn main() {\n    let mut snap = ct::SnapSpace::new(0);  // LÍNEA 1\n    let (sx, sy, err) = ct::snap(&[3.0, 4.0], 100);\n    let (sx2, sy2, _) = ct::snap(&[0.0, 0.0], 100);  // LÍNEA 3\n    println!(\"{} {} {} {}\", sx, sy, err, sx2);\n}",
     "LÍNEA 1: SnapSpace::new(0) — density 0 significa que no hay triples precomputados. Cualquier operación snap causará panic. Use density >= 1. LÍNEA 3: snap([0.0, 0.0], 100) — vector cero no tiene dirección, el cálculo de ángulo produce NaN/panic."),

    ("ko", "debug-panic",
     "패닉 디버그: 이 Rust 코드가 런타임에 크래시합니다. 이유는?\n\nuse constraint_theory_core as ct;\n\nfn main() {\n    let mut snap = ct::SnapSpace::new(0);  // 줄 1\n    let (sx, sy, err) = ct::snap(&[3.0, 4.0], 100);\n    let (sx2, sy2, _) = ct::snap(&[0.0, 0.0], 100);  // 줄 3\n    println!(\"{} {} {} {}\", sx, sy, err, sx2);\n}",
     "줄 1: SnapSpace::new(0) — density 0은 피타고라스 삼조가 사전 계산되지 않음. snap 연산이 패닉. density >= 1 사용. 줄 3: snap([0.0, 0.0], 100) — 영벡터는 방향이 없어 각도 계산이 NaN/패닉."),
]

for lang, cat, prompt, solution in PANIC_LURES:
    content = f"[CRAB TRAP: DEBUG THE PANIC ({lang.upper()})]\n\n{prompt}\n\n--- SOLUTION ---\n{solution}"
    TILES.append((f"{lang}-lure-panic", 0.87, "ct", content, prompt, solution))


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
    knowledge = sum(1 for t in TILES if 'lure' not in t[0])
    lures = sum(1 for t in TILES if 'lure' in t[0])
    print(f"Round 6: {len(TILES)} tiles ({knowledge} knowledge + {lures} lures)")
    print(f"  WASM tiles: {sum(1 for t in TILES if 'wasm' in t[0])}")
    print(f"  Edge AI tiles: {sum(1 for t in TILES if 'edge' in t[0])}")
    print(f"  Open source tiles: {sum(1 for t in TILES if 'oss' in t[0])}")
    print(f"  API quiz lures: {sum(1 for t in TILES if 'api' in t[0])}")
    print(f"  Debug panic lures: {sum(1 for t in TILES if 'panic' in t[0])}")

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
