# HIGGINS DECOMPOSITION (Hˢ) — النسخة العربية

> **حالة الترجمة: مسودة — في انتظار مراجعة خبير عربي متخصص.** بموجب `HCI-CNQ/wrappers/WRAPPER_SCHEMA.md §11.1`. النسخة الإنجليزية (`Higgins_Decomposition_Handout_CoDaCommunity.md`) هي المرجع الأساسي؛ في حال الاختلاف يُرجع إليها. المسجل المستهدف: العربية العلمية الفصحى. *ملاحظة العرض: ماركداون لا يدعم اتجاه RTL بشكل كامل — العرض المختلط مقبول لمسودة.*

---

**تشغيل تحليل البيانات التركيبية — معيار قابل للتنفيذ للباحثين ومساعدي الذكاء الاصطناعي الذين يختارونهم**

*"المراقبة التركيبية لانحراف مزيج الطاقة على البسيط (simplex)"*
**CoDaWork 2026 · كويمبرا، البرتغال · 1–5 يونيو/حزيران**
Peter Higgins · Rogue Wave Audio / Binaural Test Lab · ماركهام، أونتاريو، كندا

---

## بالأرقام

| 11 | 101 | 44 | 3 | 22 + 66 | ~220 |
|:--:|:--:|:--:|:--:|:--:|:--:|
| مجالات مُتحقَّق منها | مجموعات بيانات مرجعية | رتبة من حيث المقدار | تأكيدات فيزيائية على مستوى IEEE-floor | شرائح — العرض + الشريط السينمائي | مدخلات قاموس v3.0 |

---

## ما هذا

أعطى Aitchison للحقل هندسته عام 1986؛ ودرّبت CoDaWork أربعة عقود من المنهجيين. **يجمع Hˢ طرق CoDa الحالية والمتطورة في معيار تشغيلي قابل للتنفيذ** — سبع مراحل، نقطتا تحقق بشري، مخرجات حتمية بسلسلة هاش، ونتائج متطابقة سواء صدرت ضغطات المفاتيح من باحث أو من مساعد ذكاء اصطناعي. الرياضيات قياسية؛ الإطار التشغيلي قد يكون جديدًا.

---

## لماذا تشغيل التحليل التركيبي

- **القابلية للقياس.** يحوّل البنية التركيبية النظرية إلى تشخيصات قابلة للتكرار خطوة بخطوة: helmsman (يدوية حركة CLR)، Power Share، Activation Coefficient، توجّه الملاحة. قابل للقياس والمقارنة والتدقيق.
- **الاتساق.** مخطط ثابت (CNT v3.1.0 / CNQ v2.0.0)، خط أنابيب ثابت، إعادة تشغيل متطابقة بايتًا ببايت عبر الآلات وأنظمة التشغيل ومكتبات BLAS والسنوات. المدخل نفسه، المخرج نفسه، دائمًا.
- **اختبار الفرضيات.** المحرّك نفسه الذي ينتج النتيجة يُنتج إطار التزييف (MC-4 — أربعة مسارات نقض مُسمّاة) الذي قد يُسقطها. لا نشر بدون قابلية تزييف.

---

## مزايا عددية وتشغيلية مقارنةً بخطوط أنابيب CoDa الارتجالية

- **إحداثيات Helmert-ILR متعامدة معيارية** — لا تعسف في اختيار الأساس؛ أساس حتمي بين الفرق.
- **atan2 لزوايا helmsman والملاحة** — آمن حول ±π؛ لا فقدان دقّة ولا قفزات إشارة عند حدود الدورة.
- **مصدرية بسلسلة هاش** — SHA-256 من CSV الخام عبر CNT JSON واللوحات والمسقط ورسم المخطوطة. مراجع في 2030 يستطيع إثبات أن لا شيء قد تغيّر.
- **حتمية IEEE-floor عبر المنصّات** — المدخل نفسه، المخرج نفسه، كل آلة، كل مرة. تم التحقق على بيانات أقراص Backblaze، واستقطاب الإشعاع الكوني الميكروي لـ Planck، وتذبذبات النيوترينو في النموذج القياسي.
- **مذهب النطاق المتسق (CRD-1.0)** — المقارنات متعددة الحوامل تُحسب على تقاطع نطاقات جميع الأعضاء؛ تُزال آثار الانحراف غير المتماثل.
- **مخرجات بمخطط مُرقَّم** — كل JSON يُعلن مخططه؛ ذخيرة المؤتمر مُثبّتة عند `3.1.0` / `cnq/2.0.0` وتبقى قابلة للقراءة بمعزل عن انحراف نسخ المحرّك.

---

## المعيار التشغيلي ثلاثي الطبقات

| الطبقة | الدور | ما تفعله |
|---|---|---|
| **CNT v3.1.0** | يقيس | الإغلاق → CLR → Helmert-ILR → مقاييس تركيبية خطوة بخطوة، helmsman، Power Share، Activation Coefficient، الملاحة، التشخيصات، الهاشات. المصدر الحالي v3.2.0 يُضيف `navigation_2d` لمسار مركز ثقل Helmert-ILR PCA. |
| **CNQ v2.0.0** | يسمّي الجبر | لوحات معلومات بمنظور رباعي وتشخيصات بنية من مرتبة أعلى (ترابط CHSH المشترك، تحليل بكواتيرنيونات توأم عند D=8 مع احترام حد Tsirelson). رفيق جبري لـ CNT. |
| **CCTT v1.0** | يُشغّل | المعيار القابل للتنفيذ. سبع مراحل (تشخيص → مُحوّل *نقطة تحقق* → محرّك → مخرجات → عرض → تحقق ذاتي *نقطة تحقق* → تقديم + سجل). نقطتا تحقق بشريّتان؛ كل ما عدا ذلك حتمي. **يدرّب المستودع كلًا من الباحث ومساعد الذكاء الاصطناعي — البروتوكول نفسه، مخرج متطابق قابل للتحقق بالهاش.** |

---

## بروتوكول CCTT بسبع مراحل

`[1] تشخيص` → `[2] مُحوّل (نقطة تحقق)` → `[3] محرّك` → `[4] مخرجات` → `[5] عرض` → `[6] تحقق ذاتي (نقطة تحقق)` → `[7] تقديم + سجل`

---

## خمس وجهات نظر في العرض

- **التركيب** — حصة كل حامل.
- **Helmsman** — أكبر إزاحة CLR في خطوة.
- **مسار Helmsman** — متى يتغيّر اتجاه التوجيه.
- **Power Share** — كم من حركة CLR التربيعية أنجزها كل حامل.
- **Activation Coefficient** — Power Share ÷ الحصة الابتدائية = "معامل الخميرة".

---

## أدلة تشغيلية — ما يكشفه المعيار

يمكن لحامل أن يكون صغير الحصة كبير الأثر الهيكلي. **USA Solar 2012 → 2013:** حصة ابتدائية 0.107٪، 81.7٪ من Power Share الهيكلي، **Activation Coefficient ≈ 760×**.

تفعّل توقيع الانحراف المخادع عبر الدول في **5 من 9 دول** (AUS، CHN، GBR، IND، JPN) ولا يتفعّل في DEU (سنوي)، FRA، USA، أو WLD. البروتوكول يميّز؛ ولا يطلق إنذارات كاذبة. **انحدار على الحصص الخام لن يكشف أيًا من هاتين النتيجتين.**

---

## انطلاقة قياسية — اختر نقطة دخولك

1. **حضور المؤتمر:** `CODA-Association/CONFERENCE_ATTENDEES.md` — متابعة شريحة بشريحة.
2. **استكشاف مرئي (دون تثبيت):** `CODA-Association/CODAwork2026/data_outputs/codawork2026_projector.html`.
3. **شغّل على تركيبك الخاص:** `QUICKSTART.md` + `ai-refresh/CCTT_QUICKSTART.md` — كتيّب من 7 مراحل، يدويًا أو بمساعدة الذكاء الاصطناعي.
4. **تحقق من رقم منشور:** المخطوطة + المعلومات التكميلية + JSON لكل دولة + سلسلة الهاش.
5. **البحث في المصطلحات:** `HCI-CNT/handbook/GLOSSARY.md` v3.0 (~220 مدخلًا: PCA، SVD، CLR/ILR، Helmert، CHSH، Tsirelson، Activation Coefficient، MC-1..MC-4).

---

## التواصل والتبنّي

| الحقل | التفاصيل |
|---|---|
| **العرض** | *"المراقبة التركيبية لانحراف مزيج الطاقة على البسيط"*، CoDaWork 2026، كويمبرا، 1–5 يونيو/حزيران. ابحث عن Peter خلال الجلسات وفترات الأسئلة — يسعده استعراض المسقط مباشرة. |
| **التواصل** | Peter Higgins — **PeterHiggins@RogueWaveAudio.com** · Rogue Wave Audio / Binaural Test Lab، ماركهام، أونتاريو، كندا |
| **المستودع** | `github.com/PeterHiggins19/higgins-decomposition` · المجتمع: `CODA-Association/` · المؤتمر: `CODA-Association/CODAwork2026/` |
| **كيفية الاقتباس** | Higgins, P. (2026). *Compositional monitoring of energy-mix drift on the simplex.* CoDaWork 2026, Coimbra. المستودع: github.com/PeterHiggins19/higgins-decomposition (الالتزام مذكور في `HS_FAST_REFRESH.json`). |
| **كيفية التبنّي** | اعمل fork للمستودع، شغّل CCTT بسبع مراحل على تركيبك، أودِع `JOURNAL.md`. يتبع مساعد الذكاء الاصطناعي نقاط التحقق نفسها. انظر `ai-refresh/COMMUNITY_TEST_PACKET.json` لاختبار تبنٍّ مهيكل. |
| **الترخيص** | Apache-2.0 (الشيفرة) · CC BY 4.0 (الوثائق والأشكال). مفتوح المصدر بالكامل — يُسمح بالاشتقاق والتدقيق والتوسيع مع الإسناد. |

---

*الأداة تقرأ. الخبير يقرر. الهاشات تحمل الإيصالات. المصطلحات تحفظ الخط. ويتبع الذكاء الاصطناعي البروتوكول نفسه.*


---

## الوجه الثاني — العمليات والرموز وخريطة الجهاز

*مرجع مضغوط للعمليات التي تنفذها أساليب CoDa، وما يضيفه H^s فوقها، وما يضيفه CNQ في رؤية الكواتيرنيون، ومن أين يأتي الإغلاق في كل مجال، وأي جهاز يقرأ ماذا.*

### عمليات CoDa الأساسية (الأساس الذي قدّمه Aitchison للحقل عام 1986)

| العملية | الرمز | الصيغة / التعريف |
|---|---|---|
| Closure | C(x) | x / Σᵢ xᵢ |
| Geometric mean | g(x) | (∏ᵢ xᵢ)^(1/D) |
| CLR (centred log-ratio) | clrᵢ(x) | log(xᵢ) − (1/D) Σⱼ log(xⱼ) |
| ILR (Helmert) | η(x) | Vᵀ · clr(x),   V·Vᵀ = I |
| Aitchison distance | d_Ait(x,y) | ‖clr(x) − clr(y)‖₂ |
| Perturbation | x ⊕ y | C(x ⊙ y)   — additive on the simplex |
| Power scaling | α ⊙ x | C(x^α)   — scalar action on the simplex |

### عمليات H^s التكميلية (ما يضيفه المعيار)

| العملية | الرمز | الصيغة / التعريف |
|---|---|---|
| Helmsman index | σ(t) | argmaxᵢ |clrᵢ(t+1) − clrᵢ(t)| |
| Aitchison-step | ‖Δclr(t)‖ | ‖clr(t+1) − clr(t)‖₂ |
| Power Share | πⱼ(t) | (Δclrⱼ)² / Σₖ (Δclrₖ)²,   Σ πⱼ = 1 |
| Activation Coefficient | αⱼ(t) | πⱼ(t) / ρⱼ(t)   (when ρⱼ ≥ 10⁻³) |
| Shannon entropy | H(t) | −Σⱼ ρⱼ ln ρⱼ |
| Effective carriers | K_eff(t) | exp(H(t)) |
| L2 drift | L2(p,q) | √Σᵢ (pᵢ − qᵢ)² |
| TV distance | TV(p,q) | (1/2) Σᵢ |pᵢ − qᵢ| |

### عمليات الكواتيرنيون CNQ (قراءة الطور على S³)

| العملية | الرمز | الصيغة / التعريف |
|---|---|---|
| Phase quaternion | q(t) | ∈ S³ ≅ SU(2) |
| Quaternion conjugate | q* | (a, −b, −c, −d) |
| Hamilton product | (p·q)_k | non-commutative quaternion multiplication |
| Quaternion sandwich | v' | q · v · q*   (rotation of 3-vector) |
| Quaternion log | log(q) | (atan2(|v|, a) / |v|) · v |
| Metric involution | M² | = I   ⟺   (q*)* = q |
| SLERP (spherical interp) | slerp(q₁,q₂,α) | sin((1−α)Ω)/sinΩ · q₁ + sin(αΩ)/sinΩ · q₂ |
| CHSH joint coherence | S | E(a,b) + E(a,b') + E(a',b) − E(a',b') |

### قيود الإغلاق عبر المجالات (الميزانية التي يوزّعها التقسيم)

| المجال | الميزانية | قيد الإغلاق |
|---|---|---|
| Acoustic (BTL) | c = 20·log₁₀(2) ≈ 6.02 dB | Σ Gᵢ = c   (4π → 2π baffle-step) |
| Electrical mix | 100 % generation | Σ pᵢ = 1   (coal+gas+hydro+nuclear+solar+wind+oil+other) |
| Geochemistry | 100 % weight | Σ wᵢ = 1   (major-element oxide fraction) |
| Macro-economic | 100 % GDP | Σ pᵢ = 1   (sectoral share) |
| ERB loudness (HCI-AUDIO) | 100 % perceptual | Σⱼ Σ_drivers = 1   (40 bands × 4 drivers) |

### الجهاز بنظرة واحدة — من يقرأ ماذا

| الجهاز | يقرأ | المخرج |
|---|---|---|
| CoDa community | static partition / one timestep | log-ratio biplot, distance matrix |
| CNT — tensor engine | trajectory amplitude / per-timestep | simplex coords, Helmsman, Power Share, navigation |
| CNQ — quaternion engine | phase trajectory / S³ rotation rates | quaternion path, CHSH, twin-quaternion factoring |
| HCI-AUDIO | 4-way listening-position field | ERB band × driver matrix, phase quaternions |
| HUF (umbrella) | governance | HUF-STD-001 (Publication), -002 (Tensor Train I/O), -003 (Linear Algebra Foundations) |

### قطار HUF-STD-002 الموتري — الترتيب والرابط والنمط والرتبة في خط الأنابيب

| الترتيب | الرابط | النمط (مدخل → مخرج) | الرتبة |
|---|---|---|---|
| **0** | Adapter | raw → CSV (T × D) | D = 2 … 9+ |
| **1** | CNT — closure + Helmert-ILR | (T, D) → (T, D − 1) | D − 1 |
| **2** | CNT — per-step viewpoints | (T, D − 1) → (T, K) | K = 5 metrics |
| **3** | CNT — depth tower + IR class | (T, K) → scalar block | regime label |
| **2-3** | CNQ — quaternion path | CNT JSON → (T, 4) at D = 2 / 3 / 4 | 4 ( S³ ≅ SU(2) ) |
| **4** | Vector render | JSON → plate tensor | PDF · PNG · SVG |

**التدفق:** `raw → [Adapter] → CSV → [CNT v3.1.0] → cnt_*.json → [CNQ v2.0.0] → cnq_*.json → [Render] → PDF · PNG · SVG`

*K = 5 metrics: Helmsman · Aitchison-step · Power Share · Activation Coefficient · navigation_2D · كل رابط يصدر SHA-256؛ السلسلة قابلة للتكرار من المدخلات الخام إلى المنتج النهائي بأمر واحد.*

### مفتاح الرموز

**D** carriers · **T** timesteps · **pᵢ** portion · **Gᵢ** gain (dB) · **F_c** cutoff · **τ** group delay · **n̂** rotation axis · **q** unit quaternion · **σ** Helmsman · **αⱼ** Activation · **πⱼ** Power Share · **η** ILR coordinate · **clr** centred log-ratio · **g(x)** geometric mean · **S^(D−1)** simplex · **S³** 3-sphere ≅ SU(2)

---

*نفس المُدخل ونفس المُخرج دائمًا. الأداة تقرأ. الخبير يقرر. الهاشات تحمل الإيصالات. المصطلحات تحفظ الخط. ويتبع الذكاء الاصطناعي البروتوكول نفسه.*
