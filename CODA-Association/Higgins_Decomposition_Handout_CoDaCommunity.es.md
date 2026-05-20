# HIGGINS DECOMPOSITION (Hˢ) — versión en español

> **Estado de la traducción: BORRADOR — pendiente de revisión por experto hispanohablante.** Conforme a `HCI-CNQ/wrappers/WRAPPER_SCHEMA.md §11.1`. La versión en inglés (`Higgins_Decomposition_Handout_CoDaCommunity.md`) es la canónica; en caso de discrepancia, atenerse a ella. Registro previsto: español científico internacional.

---

**Operacionalización del análisis de datos composicionales — un estándar ejecutable para investigadores y los asistentes de IA que elijan**

*«Monitorización composicional de la deriva del mix energético en el simplex»*
**CoDaWork 2026 · Coimbra, Portugal · 1–5 de junio**
Peter Higgins · Rogue Wave Audio / Binaural Test Lab · Markham, Ontario, Canadá

---

## En cifras

| 11 | 101 | 44 | 3 | 22 + 66 | ~220 |
|:--:|:--:|:--:|:--:|:--:|:--:|
| dominios validados | conjuntos de datos de referencia | órdenes de magnitud | confirmaciones físicas al piso IEEE | diapositivas — charla + rollo cinematográfico | entradas del glosario v3.0 |

---

## Qué es

Aitchison dio a la disciplina su geometría en 1986; CoDaWork lleva cuatro décadas formando metodólogos. **Hˢ empaqueta los métodos CoDa actuales y en desarrollo en un estándar operativo ejecutable** — siete fases, dos compuertas humanas, salida determinista con cadena de hash, resultados idénticos tanto si las pulsaciones provienen de un investigador como de un asistente de IA. Las matemáticas son estándar; el marco operativo puede ser nuevo.

---

## Por qué operacionalizar el análisis composicional

- **Mensurabilidad.** Convierte la estructura composicional teórica en diagnósticos reproducibles por paso: helmsman (quiralidad del movimiento CLR), Power Share, Activation Coefficient, rumbo de navegación. Cuantificable, comparable, auditable.
- **Coherencia.** Esquema fijo (CNT v3.1.0 / CNQ v2.0.0), tubería fija, re-ejecuciones byte a byte idénticas entre máquinas, sistemas operativos, BLAS y años. Misma entrada, misma salida, siempre.
- **Prueba de hipótesis.** El mismo motor que produce un resultado produce el marco de falsabilidad (MC-4 — cuatro vías de refutación nombradas) que lo derrocaría. Ninguna publicación sin falsabilidad.

---

## Ventajas numéricas y operativas sobre los pipelines CoDa ad hoc

- **Coordenadas ortonormales Helmert-ILR** — sin arbitrariedad en la elección de base; base determinista entre equipos.
- **atan2 para ángulos de helmsman y navegación** — seguro en torno a ±π; sin pérdida de precisión ni saltos de signo en la frontera cíclica.
- **Procedencia con cadena de hash** — SHA-256 desde el CSV bruto hasta el JSON CNT, las placas, el proyector y la figura del manuscrito. Un revisor en 2030 puede demostrar que nada cambió.
- **Determinismo IEEE-floor multiplataforma** — misma entrada, misma salida, cada máquina, cada vez. Verificado en telemetría de discos Backblaze, polarización del fondo cósmico de Planck y oscilaciones de neutrinos del Modelo Estándar.
- **Doctrina de Rango Coherente (CRD-1.0)** — comparaciones multi-portador calculadas sobre la intersección de los rangos de todos los miembros; artefactos de deriva asimétrica eliminados.
- **Salidas con esquema versionado** — cada JSON declara su esquema; el corpus de la conferencia está fijado en `3.1.0` / `cnq/2.0.0` y permanece legible con independencia de la deriva de versión del motor.

---

## El estándar operativo de tres capas

| Capa | Rol | Qué hace |
|---|---|---|
| **CNT v3.1.0** | medir | Cierre → CLR → Helmert-ILR → métricas composicionales por paso, helmsman, Power Share, Activation Coefficient, navegación, diagnósticos, hashes. La fuente actual v3.2.0 añade `navigation_2d` para la trayectoria del baricentro PCA Helmert-ILR. |
| **CNQ v2.0.0** | nombrar el álgebra | Tableros en vista cuaterniónica y diagnósticos de estructura de orden superior (coherencia conjunta CHSH, factorización con cuaterniones gemelos en D=8 respetando la cota de Tsirelson). Compañero algebraico de CNT. |
| **CCTT v1.0** | operacionalizar | El estándar ejecutable. Siete fases (diagnóstico → adaptador *compuerta* → motor → salidas → renderizado → autoverificación *compuerta* → presentación + diario). Dos compuertas humanas; todo lo demás determinista. **El repositorio entrena tanto al investigador como al asistente de IA — mismo protocolo, salida idéntica verificable por hash.** |

---

## Protocolo CCTT de 7 fases

`[1] Diagnóstico` → `[2] Adaptador (compuerta)` → `[3] Motor` → `[4] Salidas` → `[5] Renderizado` → `[6] Autoverificación (compuerta)` → `[7] Presentación + diario`

---

## Cinco puntos de vista en la charla

- **Composición** — cuota que tiene cada portador.
- **Helmsman** — mayor desplazamiento CLR en un paso.
- **Trayectoria del helmsman** — cuándo cambia la dirección.
- **Power Share** — cuánto del movimiento CLR al cuadrado hizo cada portador.
- **Activation Coefficient** — Power Share ÷ cuota inicial = «factor levadura».

---

## Evidencia operativa — lo que el estándar revela

Un portador puede ser pequeño en cuota pero grande en trabajo estructural. **USA Solar 2012 → 2013:** 0,107 % de cuota inicial, 81,7 % del Power Share estructural, **Activation Coefficient ≈ 760×**.

La firma de deriva engañosa entre países se activa en **5 de 9 países** (AUS, CHN, GBR, IND, JPN) y *no* se activa en DEU (anual), FRA, USA o WLD. El protocolo discrimina; no se activa en falso. **Una regresión sobre cuotas brutas no habría revelado ninguno de los dos hallazgos.**

---

## Onboarding estándar — elija su punto de entrada

1. **Asistente a la conferencia:** `CODA-Association/CONFERENCE_ATTENDEES.md` — seguimiento diapositiva a diapositiva.
2. **Exploración visual (sin instalación):** `CODA-Association/CODAwork2026/data_outputs/codawork2026_projector.html`.
3. **Ejecute sobre su propia composición:** `QUICKSTART.md` + `ai-refresh/CCTT_QUICKSTART.md` — guía de 7 fases, manual o asistida por IA.
4. **Verifique un número publicado:** manuscrito + Información Suplementaria + JSON por país + cadena de hash.
5. **Búsqueda de vocabulario:** `HCI-CNT/handbook/GLOSSARY.md` v3.0 (~220 entradas: PCA, SVD, CLR/ILR, Helmert, CHSH, Tsirelson, Activation Coefficient, MC-1..MC-4).

---

## Contacto y adopción

| Campo | Detalles |
|---|---|
| **Charla** | *«Monitorización composicional de la deriva del mix energético en el simplex»*, CoDaWork 2026, Coimbra, 1–5 de junio. Encuentre a Peter durante las sesiones y los Q&A — encantado de mostrar el proyector en vivo. |
| **Contacto** | Peter Higgins — **PeterHiggins@RogueWaveAudio.com** · Rogue Wave Audio / Binaural Test Lab, Markham, Ontario, Canadá |
| **Repositorio** | `github.com/PeterHiggins19/higgins-decomposition` · comunidad: `CODA-Association/` · conferencia: `CODA-Association/CODAwork2026/` |
| **Cómo citar** | Higgins, P. (2026). *Compositional monitoring of energy-mix drift on the simplex.* CoDaWork 2026, Coimbra. Repo: github.com/PeterHiggins19/higgins-decomposition (commit en `HS_FAST_REFRESH.json`). |
| **Cómo adoptar** | Haga un fork del repositorio, ejecute el CCTT de 7 fases sobre su composición, presente un `JOURNAL.md`. El asistente de IA sigue las mismas compuertas. Véase `ai-refresh/COMMUNITY_TEST_PACKET.json` para el test estructurado de adopción. |
| **Licencia** | Apache-2.0 (código) · CC BY 4.0 (documentación y figuras). Totalmente código abierto — fork, auditar, extender, atribuir. |

---

*El instrumento lee. El experto decide. Los hashes llevan los recibos. El vocabulario sostiene la línea. La IA sigue el mismo protocolo.*
