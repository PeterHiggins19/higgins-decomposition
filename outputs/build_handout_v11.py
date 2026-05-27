"""Build the v11 (2-side) operationalization handout in all six UN-6 locales.

v11 adds **side 2** carrying the operations + symbols reference, per reviewer
request. Side 2 contains:

  Block A — CoDa core operations (closure, CLR, ILR-Helmert, Aitchison
            distance, perturbation, power scaling, geometric mean)
  Block B — Hˢ supplementary operations (Helmsman, Power Share, Activation
            Coefficient, Aitchison-step, Shannon entropy, K_eff, TV/L2 drift)
  Block C — CNQ quaternion operations (q ∈ S³, log, Hamilton product,
            conjugate, sandwich, metric involution, SLERP, CHSH coherence)
  Block D — Closure constraints across domains (acoustic 6.02 dB / electricity
            100% / geochemistry / GDP / ERB loudness)
  Block E — Apparatus at a glance (CoDa community / CNT / CNQ / HCI-AUDIO /
            HUF) — who reads what
  Block F — Symbols legend (one-line strip)

Math symbols and English operation names are constant across all six locales
(standard mathematical publishing convention worldwide). Section headings and
brief one-line descriptions are localized per locale.

Two-page handout, side 1 unchanged from v10. Outputs to repo CODA-Association/.
"""
import base64, io, qrcode
from weasyprint import HTML

# ── Import shared content from v10 builder ──────────────────────────────────
import importlib.util, sys
spec = importlib.util.spec_from_file_location(
    "build_handout_un6",
    "/sessions/epic-gracious-lovelace/mnt/outputs/build_handout_un6.py")
v10 = importlib.util.module_from_spec(spec)
# We need just the LOCALES dict + QR_B64; importing the module runs the build
# block as a side effect. Instead, parse the file and exec only the LOCALES.
src = open(spec.origin).read()

# Extract LOCALES dict and QR_B64 by exec-ing the top of the file up to the
# "─── HTML template" marker.
cut = src.index("# ─── HTML template")
exec(src[:cut], globals())   # populates LOCALES, QR_B64, REPO_URL

# ── Page-2 localized strings ────────────────────────────────────────────────
# Section headings and column labels per locale. Math/operation names stay in
# English (international math-publishing convention).

P2 = {
"en": dict(
    h_title="Side 2 — Operations, symbols, and the apparatus map",
    h_intro="Compact reference for the operations performed by CoDa methods, what Hˢ adds on top, what CNQ adds in the quaternion view, where the closure comes from in each domain, and which apparatus reads what.",
    h_coda="CoDa core operations (the foundation Aitchison gave the field in 1986)",
    h_hs="Hˢ supplementary operations (what the standard adds)",
    h_cnq="CNQ quaternion operations (the phase readout on S³)",
    h_closure="Closure constraints across domains (the budget the partition apportions)",
    h_appar="Apparatus at a glance — who reads what",
    h_tt="HUF-STD-002 Tensor Train — pipeline order, link, mode, rank",
    h_sym="Symbols legend",
    c_op="Operation", c_sym="Symbol", c_formula="Formula / definition",
    c_dom="Domain", c_bud="Budget", c_clos="Closure constraint",
    c_app="Apparatus", c_reads="Reads", c_out="Output",
    c_order="Order", c_link="Link", c_mode="Mode (input → output)", c_rank="Rank",
    flow_label="Flow:",
    hash_note="Each link emits SHA-256; chain reproducible from raw input to final artifact in one command.",
    closing="Same input, same output, always. The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line. The AI follows the same protocol.",
),
"fr": dict(
    h_title="Verso — Opérations, symboles et carte de l'appareil",
    h_intro="Référence compacte des opérations effectuées par les méthodes CoDa, de ce qu'Hˢ ajoute par-dessus, de ce que CNQ ajoute dans la vue quaternion, d'où vient la fermeture dans chaque domaine, et quel appareil lit quoi.",
    h_coda="Opérations centrales CoDa (la fondation qu'Aitchison a donnée au domaine en 1986)",
    h_hs="Opérations supplémentaires Hˢ (ce que le standard ajoute)",
    h_cnq="Opérations quaternioniques CNQ (la lecture de phase sur S³)",
    h_closure="Contraintes de fermeture par domaine (le budget que la partition répartit)",
    h_appar="Appareil en un coup d'œil — qui lit quoi",
    h_tt="Train tensoriel HUF-STD-002 — ordre, lien, mode et rang du pipeline",
    h_sym="Légende des symboles",
    c_op="Opération", c_sym="Symbole", c_formula="Formule / définition",
    c_dom="Domaine", c_bud="Budget", c_clos="Contrainte de fermeture",
    c_app="Appareil", c_reads="Lit", c_out="Sortie",
    c_order="Ordre", c_link="Lien", c_mode="Mode (entrée → sortie)", c_rank="Rang",
    flow_label="Flux :",
    hash_note="Chaque lien émet SHA-256 ; chaîne reproductible de l'entrée brute à l'artefact final en une seule commande.",
    closing="Même entrée, même sortie, toujours. L'instrument lit. L'expert décide. Les hachages portent les reçus. Le vocabulaire tient la ligne. L'IA suit le même protocole.",
),
"es": dict(
    h_title="Reverso — Operaciones, símbolos y mapa del instrumento",
    h_intro="Referencia compacta de las operaciones realizadas por los métodos CoDa, lo que Hˢ añade encima, lo que CNQ añade en la vista quaterniónica, de dónde viene la clausura en cada dominio, y qué instrumento lee qué.",
    h_coda="Operaciones nucleares CoDa (la base que Aitchison dio al campo en 1986)",
    h_hs="Operaciones suplementarias Hˢ (lo que añade el estándar)",
    h_cnq="Operaciones quaterniónicas CNQ (la lectura de fase en S³)",
    h_closure="Restricciones de clausura por dominio (el presupuesto que reparte la partición)",
    h_appar="El instrumento de un vistazo — quién lee qué",
    h_tt="Tren tensorial HUF-STD-002 — orden, enlace, modo y rango del pipeline",
    h_sym="Leyenda de símbolos",
    c_op="Operación", c_sym="Símbolo", c_formula="Fórmula / definición",
    c_dom="Dominio", c_bud="Presupuesto", c_clos="Restricción de clausura",
    c_app="Instrumento", c_reads="Lee", c_out="Salida",
    c_order="Orden", c_link="Enlace", c_mode="Modo (entrada → salida)", c_rank="Rango",
    flow_label="Flujo:",
    hash_note="Cada enlace emite SHA-256; cadena reproducible desde la entrada bruta hasta el artefacto final en un solo comando.",
    closing="Misma entrada, misma salida, siempre. El instrumento lee. El experto decide. Los hashes llevan los recibos. El vocabulario sostiene la línea. La IA sigue el mismo protocolo.",
),
"ru": dict(
    h_title="Сторона 2 — Операции, символы и карта прибора",
    h_intro="Компактный справочник операций методов CoDa, того, что Hˢ добавляет сверху, что добавляет CNQ в кватернионном представлении, откуда берётся замыкание в каждой области и какой прибор что считывает.",
    h_coda="Базовые операции CoDa (основание, которое Aitchison дал области в 1986 г.)",
    h_hs="Дополнительные операции Hˢ (то, что добавляет стандарт)",
    h_cnq="Кватернионные операции CNQ (считывание фазы на S³)",
    h_closure="Ограничения замыкания по областям (бюджет, который распределяет разбиение)",
    h_appar="Прибор с одного взгляда — кто что считывает",
    h_tt="Тензорный поезд HUF-STD-002 — порядок, звено, режим и ранг конвейера",
    h_sym="Легенда символов",
    c_op="Операция", c_sym="Символ", c_formula="Формула / определение",
    c_dom="Область", c_bud="Бюджет", c_clos="Ограничение замыкания",
    c_app="Прибор", c_reads="Читает", c_out="Выход",
    c_order="Порядок", c_link="Звено", c_mode="Режим (вход → выход)", c_rank="Ранг",
    flow_label="Поток:",
    hash_note="Каждое звено выдаёт SHA-256; цепочка воспроизводима от исходного ввода до финального артефакта одной командой.",
    closing="Тот же вход — тот же выход, всегда. Инструмент читает. Эксперт решает. Хэши несут квитанции. Словарь держит линию. ИИ следует тому же протоколу.",
),
"zh": dict(
    h_title="第 2 面 — 操作、符号与仪器图谱",
    h_intro="CoDa 方法所执行的操作、H<sup>s</sup> 在其上添加的内容、CNQ 在四元数视图下添加的内容、每个领域闭包的来源，以及哪个仪器读取什么 — 紧凑参考。",
    h_coda="CoDa 核心操作（Aitchison 于 1986 年为本领域奠基）",
    h_hs="H<sup>s</sup> 补充操作（标准在其上添加的内容）",
    h_cnq="CNQ 四元数操作（S³ 上的相位读取）",
    h_closure="跨领域闭包约束（分割所分配的预算）",
    h_appar="仪器一览 — 谁读什么",
    h_tt="HUF-STD-002 张量链 — 流程顺序、环节、模式、秩",
    h_sym="符号图例",
    c_op="操作", c_sym="符号", c_formula="公式 / 定义",
    c_dom="领域", c_bud="预算", c_clos="闭包约束",
    c_app="仪器", c_reads="读取", c_out="输出",
    c_order="顺序", c_link="环节", c_mode="模式（输入 → 输出）", c_rank="秩",
    flow_label="流程：",
    hash_note="每个环节发出 SHA-256；从原始输入到最终成果可由一条命令完整复现。",
    closing="同输入同输出，始终如一。仪器读取。专家判定。哈希承载凭证。词汇守住底线。AI 遵循同一协议。",
),
"ar": dict(
    h_title="الوجه الثاني — العمليات والرموز وخريطة الجهاز",
    h_intro="مرجع مضغوط للعمليات التي تنفذها أساليب CoDa، وما يضيفه H<sup>s</sup> فوقها، وما يضيفه CNQ في رؤية الكواتيرنيون، ومن أين يأتي الإغلاق في كل مجال، وأي جهاز يقرأ ماذا.",
    h_coda="عمليات CoDa الأساسية (الأساس الذي قدّمه Aitchison للحقل عام 1986)",
    h_hs="عمليات H<sup>s</sup> التكميلية (ما يضيفه المعيار)",
    h_cnq="عمليات الكواتيرنيون CNQ (قراءة الطور على S³)",
    h_closure="قيود الإغلاق عبر المجالات (الميزانية التي يوزّعها التقسيم)",
    h_appar="الجهاز بنظرة واحدة — من يقرأ ماذا",
    h_tt="قطار HUF-STD-002 الموتري — الترتيب والرابط والنمط والرتبة في خط الأنابيب",
    h_sym="مفتاح الرموز",
    c_op="العملية", c_sym="الرمز", c_formula="الصيغة / التعريف",
    c_dom="المجال", c_bud="الميزانية", c_clos="قيد الإغلاق",
    c_app="الجهاز", c_reads="يقرأ", c_out="المخرج",
    c_order="الترتيب", c_link="الرابط", c_mode="النمط (مدخل → مخرج)", c_rank="الرتبة",
    flow_label="التدفق:",
    hash_note="كل رابط يصدر SHA-256؛ السلسلة قابلة للتكرار من المدخلات الخام إلى المنتج النهائي بأمر واحد.",
    closing="نفس المُدخل ونفس المُخرج دائمًا. الأداة تقرأ. الخبير يقرر. الهاشات تحمل الإيصالات. المصطلحات تحفظ الخط. ويتبع الذكاء الاصطناعي البروتوكول نفسه.",
),
}

# ── Page-2 row content (universal — math doesn't translate) ─────────────────

ROWS_CODA = [
    ("Closure",         "C(x)",              "x / Σᵢ xᵢ"),
    ("Geometric mean",  "g(x)",              "(∏ᵢ xᵢ)^(1/D)"),
    ("CLR (centred log-ratio)", "clrᵢ(x)",   "log(xᵢ) − (1/D) Σⱼ log(xⱼ)"),
    ("ILR (Helmert)",   "η(x)",              "Vᵀ · clr(x),   V·Vᵀ = I"),
    ("Aitchison distance", "d_Ait(x,y)",     "‖clr(x) − clr(y)‖₂"),
    ("Perturbation",    "x ⊕ y",             "C(x ⊙ y)   — additive on the simplex"),
    ("Power scaling",   "α ⊙ x",             "C(x^α)   — scalar action on the simplex"),
]

ROWS_HS = [
    ("Helmsman index",     "σ(t)",           "argmaxᵢ |clrᵢ(t+1) − clrᵢ(t)|"),
    ("Aitchison-step",     "‖Δclr(t)‖",      "‖clr(t+1) − clr(t)‖₂"),
    ("Power Share",        "πⱼ(t)",          "(Δclrⱼ)² / Σₖ (Δclrₖ)²,   Σ πⱼ = 1"),
    ("Activation Coefficient", "αⱼ(t)",      "πⱼ(t) / ρⱼ(t)   (when ρⱼ ≥ 10⁻³)"),
    ("Shannon entropy",    "H(t)",           "−Σⱼ ρⱼ ln ρⱼ"),
    ("Effective carriers", "K_eff(t)",       "exp(H(t))"),
    ("L2 drift",           "L2(p,q)",        "√Σᵢ (pᵢ − qᵢ)²"),
    ("TV distance",        "TV(p,q)",        "(1/2) Σᵢ |pᵢ − qᵢ|"),
]

ROWS_CNQ = [
    ("Phase quaternion",       "q(t)",         "∈ S³ ≅ SU(2)"),
    ("Quaternion conjugate",   "q*",           "(a, −b, −c, −d)"),
    ("Hamilton product",       "(p·q)_k",      "non-commutative quaternion multiplication"),
    ("Quaternion sandwich",    "v'",           "q · v · q*   (rotation of 3-vector)"),
    ("Quaternion log",         "log(q)",       "(atan2(|v|, a) / |v|) · v"),
    ("Metric involution",      "M²",           "= I   ⟺   (q*)* = q"),
    ("SLERP (spherical interp)", "slerp(q₁,q₂,α)", "sin((1−α)Ω)/sinΩ · q₁ + sin(αΩ)/sinΩ · q₂"),
    ("CHSH joint coherence",   "S",            "E(a,b) + E(a,b') + E(a',b) − E(a',b')"),
]

ROWS_CLOSURE = [
    ("Acoustic (BTL)",      "c = 20·log₁₀(2) ≈ 6.02 dB",     "Σ Gᵢ = c   (4π → 2π baffle-step)"),
    ("Electrical mix",      "100 % generation",               "Σ pᵢ = 1   (coal+gas+hydro+nuclear+solar+wind+oil+other)"),
    ("Geochemistry",        "100 % weight",                   "Σ wᵢ = 1   (major-element oxide fraction)"),
    ("Macro-economic",      "100 % GDP",                      "Σ pᵢ = 1   (sectoral share)"),
    ("ERB loudness (HCI-AUDIO)", "100 % perceptual",         "Σⱼ Σ_drivers = 1   (40 bands × 4 drivers)"),
]

ROWS_APPAR = [
    ("CoDa community",          "static partition / one timestep",      "log-ratio biplot, distance matrix"),
    ("CNT — tensor engine",     "trajectory amplitude / per-timestep",  "simplex coords, Helmsman, Power Share, navigation"),
    ("CNQ — quaternion engine", "phase trajectory / S³ rotation rates", "quaternion path, CHSH, twin-quaternion factoring"),
    ("HCI-AUDIO",               "4-way listening-position field",       "ERB band × driver matrix, phase quaternions"),
    ("HUF (umbrella)",          "governance",                            "HUF-STD-001 (Publication), -002 (Tensor Train I/O), -003 (Linear Algebra Foundations)"),
]

# Tensor-Train rows (new 2026-05-26 — reviewer noted 1/3 page free on side 2; Peter
# approved adding pipeline order/link/mode/rank from huf-gov/standards/
# HUF_TENSOR_TRAIN_IO_STANDARD.json the_tensor_train_v1_0.links[]. Stimulates CoDa-
# community interaction: the pipeline complements the apparatus map above.)
ROWS_TT = [
    ("Order 0",   "Adapter",                       "raw → CSV (T × D)",                            "D = 2 … 9+"),
    ("Order 1",   "CNT — closure + Helmert-ILR",   "(T, D) → (T, D − 1)",                          "D − 1"),
    ("Order 2",   "CNT — per-step viewpoints",     "(T, D − 1) → (T, K)",                          "K = 5 metrics"),
    ("Order 3",   "CNT — depth tower + IR class",  "(T, K) → scalar block",                        "regime label"),
    ("Order 2-3", "CNQ — quaternion path",         "CNT JSON → (T, 4) at D = 2 / 3 / 4",           "4   ( S³ ≅ SU(2) )"),
    ("Order 4",   "Vector render",                 "JSON → plate tensor",                          "PDF · PNG · SVG"),
]

# K=5 footnote — math content stays in English per existing handout convention
TT_K_FOOTNOTE = (
    "K = 5 metrics  :  Helmsman · Aitchison-step · Power Share · "
    "Activation Coefficient · navigation_2D"
)

# One-line flow chart for the tensor train (math content stays in English)
TT_FLOW_LINE = (
    "raw  →  [Adapter]  →  CSV  →  [CNT v3.1.0]  →  cnt_*.json  "
    "→  [CNQ v2.0.0]  →  cnq_*.json  →  [Render]  →  PDF · PNG · SVG"
)

SYMBOLS_LINE = (
    "<strong>D</strong> carriers · <strong>T</strong> timesteps · "
    "<strong>pᵢ</strong> portion · <strong>Gᵢ</strong> gain (dB) · "
    "<strong>F_c</strong> cutoff · <strong>τ</strong> group delay · "
    "<strong>n̂</strong> rotation axis · <strong>q</strong> unit quaternion · "
    "<strong>σ</strong> Helmsman · <strong>αⱼ</strong> Activation · "
    "<strong>πⱼ</strong> Power Share · <strong>η</strong> ILR coordinate · "
    "<strong>clr</strong> centred log-ratio · <strong>g(x)</strong> geometric mean · "
    "<strong>S^(D−1)</strong> simplex · <strong>S³</strong> 3-sphere ≅ SU(2)"
)

# ── Side-2 HTML block ────────────────────────────────────────────────────────
def render_side2(loc):
    L = LOCALES[loc]
    P = P2[loc]

    def table(rows, cols):
        head = "<tr>" + "".join(f'<th>{c}</th>' for c in cols) + "</tr>"
        body = ""
        for row in rows:
            body += "<tr>"
            for i, cell in enumerate(row):
                if i == 0:
                    body += f'<td class="op">{cell}</td>'
                elif i == 1:
                    body += f'<td class="sym">{cell}</td>'
                else:
                    body += f'<td class="fmla">{cell}</td>'
            body += "</tr>"
        return f"<table class='ops'><thead>{head}</thead><tbody>{body}</tbody></table>"

    coda_table    = table(ROWS_CODA,    (P['c_op'], P['c_sym'], P['c_formula']))
    hs_table      = table(ROWS_HS,      (P['c_op'], P['c_sym'], P['c_formula']))
    cnq_table     = table(ROWS_CNQ,     (P['c_op'], P['c_sym'], P['c_formula']))
    closure_table = table(ROWS_CLOSURE, (P['c_dom'], P['c_bud'], P['c_clos']))
    appar_table   = table(ROWS_APPAR,   (P['c_app'], P['c_reads'], P['c_out']))

    # Tensor-train table uses 4 columns (Order, Link, Mode, Rank) — needs a slightly
    # different table builder since the existing one is hard-coded to 3 columns.
    def table4(rows, cols):
        head = "<tr>" + "".join(f'<th>{c}</th>' for c in cols) + "</tr>"
        body = ""
        for row in rows:
            body += "<tr>"
            body += f'<td class="ord">{row[0]}</td>'
            body += f'<td class="op">{row[1]}</td>'
            body += f'<td class="fmla">{row[2]}</td>'
            body += f'<td class="fmla">{row[3]}</td>'
            body += "</tr>"
        return f"<table class='ops tt'><thead>{head}</thead><tbody>{body}</tbody></table>"

    tt_table_html = table4(ROWS_TT,
        (P['c_order'], P['c_link'], P['c_mode'], P['c_rank']))

    return f"""
<div class="page2">
  <h1 class="p2-title">{P['h_title']}</h1>
  <p class="p2-intro">{P['h_intro']}</p>

  <table class="twocol">
    <tr>
      <td>
        <h3 class="block">{P['h_coda']}</h3>
        {coda_table}
      </td>
      <td>
        <h3 class="block">{P['h_hs']}</h3>
        {hs_table}
      </td>
    </tr>
  </table>

  <h3 class="block">{P['h_cnq']}</h3>
  {cnq_table}

  <table class="twocol">
    <tr>
      <td>
        <h3 class="block">{P['h_closure']}</h3>
        {closure_table}
      </td>
      <td>
        <h3 class="block">{P['h_appar']}</h3>
        {appar_table}
      </td>
    </tr>
  </table>

  <h3 class="block">{P['h_tt']}</h3>
  {tt_table_html}
  <p class="tt-flow"><strong>{P['flow_label']}</strong> <span class="tt-flow-line">{TT_FLOW_LINE}</span></p>
  <p class="tt-footnote"><em>{TT_K_FOOTNOTE}</em> &nbsp;·&nbsp; <em>{P['hash_note']}</em></p>

  <h3 class="block">{P['h_sym']}</h3>
  <p class="symbols">{SYMBOLS_LINE}</p>

  <p class="p2-closing">{P['closing']}</p>
</div>
"""

# ── Override render() to insert side 2 ──────────────────────────────────────
# We re-exec the render function from v10 (with our LOCALES already loaded),
# then wrap it to append page 2.

# Pull the render function source out of v10
render_start = src.index("def render(loc):")
render_end = src.index("# ─── build", render_start)
render_src = src[render_start:render_end]
exec(render_src, globals())  # defines render(loc) using our globals

# Wrap render() with v11 side-2 injection
_render_v10 = render
def render(loc):
    html = _render_v10(loc)
    side2 = render_side2(loc)
    # Inject side2 before </body>
    return html.replace(
        "</body></html>",
        # Inject side-2-specific CSS + the side-2 HTML
        """
<style>
  .page2 { page-break-before: always; }
  .page2 .p2-title { font-size: 13pt; color: #1a3a5c; margin: 0 0 2px 0;
                     letter-spacing: 0.2px; }
  .page2 .p2-intro { font-size: 7.6pt; color: #444; font-style: italic;
                     margin: 0 0 5px 0; line-height: 1.30; }
  .page2 h3.block { font-size: 8.4pt; color: #1a3a5c; margin: 4px 0 2px 0;
                    border-bottom: 0.6px solid #cfd8e0; padding-bottom: 1px;
                    font-weight: bold; }
  .page2 table.twocol { width: 100%; border-collapse: collapse; margin: 0; }
  .page2 table.twocol > tbody > tr > td { width: 50%; vertical-align: top;
                                            padding: 0 5px 0 0; }
  .page2 table.twocol > tbody > tr > td + td { padding: 0 0 0 5px; }
  .page2 table.ops { width: 100%; border-collapse: collapse; margin: 1px 0 3px 0;
                     font-size: 7.0pt; }
  .page2 table.ops th { background: #1a3a5c; color: white;
                        font-weight: bold; padding: 2px 4px; text-align: left;
                        font-size: 6.9pt; letter-spacing: 0.1px; }
  .page2 table.ops td { padding: 1.8px 4px; vertical-align: top;
                        border-bottom: 0.5px solid #e8edf2;
                        line-height: 1.22; }
  .page2 table.ops tr:nth-child(even) td { background: #f9fbfd; }
  .page2 table.ops td.op { color: #1a3a5c; font-weight: bold;
                           width: 28%; white-space: nowrap; }
  .page2 table.ops td.sym { font-family: "Consolas","Monaco",monospace;
                            color: #8a5d00; width: 22%; direction: ltr;
                            font-size: 7.1pt; }
  .page2 table.ops td.fmla { font-family: "Consolas","Monaco",monospace;
                             color: #222; direction: ltr;
                             font-size: 7.0pt; }
  .page2 p.symbols { font-size: 7.1pt; color: #333; margin: 1px 0 3px 0;
                     line-height: 1.45; direction: ltr; }
  .page2 p.symbols strong { color: #1a3a5c; font-family: "Consolas","Monaco",monospace;
                            font-size: 7.0pt; }
  /* Tensor-train table (4-column variant) */
  .page2 table.ops.tt td.ord { color: #1a3a5c; font-weight: bold;
                                font-family: "Consolas","Monaco",monospace;
                                width: 13%; white-space: nowrap; font-size: 7.0pt; }
  .page2 table.ops.tt td.op { width: 28%; }
  .page2 table.ops.tt td.fmla { width: 29.5%; }
  .page2 p.tt-flow { font-size: 7.0pt; color: #222; margin: 3px 0 1px 0;
                     line-height: 1.30; direction: ltr;
                     font-family: "Consolas","Monaco",monospace; }
  .page2 p.tt-flow strong { color: #1a3a5c; font-family: inherit; }
  .page2 p.tt-flow .tt-flow-line { color: #333; }
  .page2 p.tt-footnote { font-size: 6.7pt; color: #555; margin: 1px 0 3px 0;
                         line-height: 1.30; direction: ltr; font-style: italic; }
  .page2 p.p2-closing { text-align: center; font-style: italic;
                        color: #1a3a5c; font-size: 7.4pt;
                        margin: 6px 0 0 0; line-height: 1.35;
                        border-top: 0.6px solid #cfd8e0; padding-top: 3px; }
</style>
""" + side2 + "\n</body></html>"
    )

# ── Build ───────────────────────────────────────────────────────────────────
WORKSPACE = "/sessions/epic-gracious-lovelace/mnt/Claude CoWorker"
REPO = f"{WORKSPACE}/Current-Repo/Hs/CODA-Association"
BASE = "Higgins_Decomposition_Handout_CoDaCommunity"

results = []
for loc in LOCALES:
    html = render(loc)
    doc = HTML(string=html).render()
    n_pages = len(doc.pages)
    suffix = "" if loc == "en" else f".{loc}"
    repo_path = f"{REPO}/{BASE}{suffix}.pdf"
    workspace_path = f"{WORKSPACE}/{BASE}{suffix}.pdf"
    try:
        doc.write_pdf(repo_path)
        doc.write_pdf(workspace_path)
        results.append((loc, n_pages, "OK both", repo_path))
    except PermissionError:
        backup = repo_path.replace(".pdf", "_v11.pdf")
        doc.write_pdf(backup)
        results.append((loc, n_pages, f"locked → {backup}", backup))

print("BUILD RESULTS (v11 — 2-side handout):")
for loc, pages, status, path in results:
    flag = "✓ 2pp" if pages == 2 else f"⚠ {pages}pp"
    print(f"  {loc.upper():3s}  {flag}  {status}")
print()
print("Sizes:")
import os
for loc, _, _, path in results:
    if os.path.exists(path):
        print(f"  {loc.upper():3s}  {os.path.getsize(path):>7d} B  {path}")
