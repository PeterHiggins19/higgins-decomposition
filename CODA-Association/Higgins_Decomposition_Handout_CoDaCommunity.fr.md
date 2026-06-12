# HIGGINS DECOMPOSITION (Hˢ) — version française

> **Statut de traduction : VERSION DE TRAVAIL — révision par expert francophone qualifié en attente.** Conforme à `HCI-CNQ/wrappers/WRAPPER_SCHEMA.md §11.1`. La version anglaise (`Higgins_Decomposition_Handout_CoDaCommunity.md`) fait foi ; en cas de divergence, s'y reporter. Registre visé : français international (BIPM).

---

**Opérationnalisation de l'analyse des données compositionnelles — une norme exécutable pour les chercheurs et les assistants d'IA qu'ils choisissent**

*« Surveillance compositionnelle de la dérive du mix énergétique sur le simplexe »*
**CoDaWork 2026 · Coimbra, Portugal · 1–5 juin**
Peter Higgins · Rogue Wave Audio / Binaural Test Lab · Markham, Ontario, Canada

---

## En chiffres

| 11 | 101 | 44 | 3 | 22 + 66 | ~220 |
|:--:|:--:|:--:|:--:|:--:|:--:|
| domaines validés | jeux de données de référence | ordres de grandeur | confirmations physiques au plancher IEEE | diapositives — exposé + déroulé cinéma | entrées du glossaire v3.0 |

---

## Ce que c'est

Aitchison a doté la discipline de sa géométrie en 1986 ; CoDaWork forme depuis quatre décennies des méthodologistes. **Hˢ regroupe les méthodes CoDa actuelles et en développement dans une norme opérationnelle exécutable** — sept phases, deux points de contrôle humains, sortie déterministe à chaînage de hachage, résultats identiques que les frappes proviennent d'un chercheur ou d'un assistant d'IA. Les mathématiques sont standard ; le cadre opérationnel peut être nouveau.

---

## Pourquoi opérationnaliser l'analyse compositionnelle

- **Mesurabilité.** Convertit la structure compositionnelle théorique en diagnostics reproductibles pas à pas : helmsman (chiralité du mouvement CLR), Power Share, Activation Coefficient, cap de navigation. Quantifiable, comparable, auditable.
- **Cohérence.** Schéma figé (CNT v3.1.0 / CNQ v2.0.0), pipeline figé, ré-exécutions octet-identiques entre machines, systèmes d'exploitation, BLAS et années. Même entrée, même sortie, toujours.
- **Test d'hypothèse.** Le même moteur qui produit un résultat produit le cadre de falsifiabilité (MC-4 — quatre voies de réfutation nommées) qui le renverserait. Pas de publication sans falsification.

---

## Avantages numériques et opérationnels par rapport aux pipelines CoDa ad hoc

- **Coordonnées orthonormées Helmert-ILR** — pas d'arbitraire dans le choix de la base ; base déterministe entre équipes.
- **atan2 pour les angles de helmsman et de navigation** — sûr aux abords de ±π ; ni perte de précision ni saut de signe à la frontière cyclique.
- **Provenance à chaînage de hachage** — SHA-256 du CSV brut jusqu'au JSON CNT, aux planches, au projecteur et à la figure du manuscrit. Un examinateur en 2030 peut prouver que rien n'a changé.
- **Déterminisme IEEE-floor inter-plateformes** — même entrée, même sortie, à chaque machine, à chaque fois. Vérifié sur la télémétrie des disques Backblaze, la polarisation du fond diffus cosmologique de Planck et les oscillations de neutrinos du Modèle Standard.
- **Doctrine de plage cohérente (CRD-1.0)** — comparaisons multi-porteurs calculées sur l'intersection des plages de tous les membres ; artefacts de dérive asymétrique éliminés.
- **Sorties versionnées par schéma** — chaque JSON déclare son schéma ; le corpus de la conférence est verrouillé à `3.1.0` / `cnq/2.0.0` et reste lisible indépendamment de la dérive des versions du moteur.

---

## La norme opérationnelle à trois couches

| Couche | Rôle | Ce qu'elle fait |
|---|---|---|
| **CNT v3.1.0** | mesurer | Clôture → CLR → Helmert-ILR → métriques compositionnelles pas à pas, helmsman, Power Share, Activation Coefficient, navigation, diagnostics, hachages. La source actuelle v3.2.0 ajoute `navigation_2d` pour la trajectoire du barycentre ACP Helmert-ILR. |
| **CNQ v2.0.0** | nommer l'algèbre | Tableaux de bord en vue quaternionique et diagnostics de structure d'ordre supérieur (cohérence conjointe CHSH, factorisation à quaternions jumeaux à D=8 dans le respect de la borne de Tsirelson). Compagnon algébrique de CNT. |
| **CCTT v1.0** | opérationnaliser | La norme exécutable. Sept phases (diagnostic → adaptateur *contrôle* → moteur → sorties → rendu → auto-vérification *contrôle* → présentation + journal). Deux contrôles humains ; tout le reste est déterministe. **Le dépôt forme à la fois le chercheur et l'assistant d'IA — même protocole, sortie identique vérifiable par hachage.** |

---

## Protocole CCTT en 7 phases

`[1] Diagnostic` → `[2] Adaptateur (contrôle)` → `[3] Moteur` → `[4] Sorties` → `[5] Rendu` → `[6] Auto-vérification (contrôle)` → `[7] Présentation + journal`

---

## Cinq points de vue dans l'exposé

- **Composition** — part de chaque porteur.
- **Helmsman** — plus grand déplacement CLR à un pas.
- **Trajectoire du helmsman** — quand la direction change.
- **Power Share** — part du mouvement CLR au carré attribuable à chaque porteur.
- **Activation Coefficient** — Power Share ÷ part initiale = « facteur de levain ».

---

## Preuves opérationnelles — ce que la norme fait apparaître

Un porteur peut être petit en part mais grand en travail structurel. **USA Solaire 2012 → 2013 :** 0,107 % de part initiale, 81,7 % du Power Share structurel, **Activation Coefficient ≈ 760×**.

La signature de dérive trompeuse trans-pays s'active dans **5 pays sur 9** (AUS, CHN, GBR, IND, JPN) et ne s'active *pas* en DEU (annuel), FRA, USA ou WLD. Le protocole discrimine ; il ne s'active pas à tort. **Une régression sur les parts brutes n'aurait fait apparaître ni l'un ni l'autre de ces résultats.**

---

## Onboarding standard — choisissez votre point d'entrée

1. **Participant à la conférence :** `CODA-Association/CONFERENCE_ATTENDEES.md` — suivi diapositive par diapositive.
2. **Exploration visuelle (zéro installation) :** `CODA-Association/CODAwork2026/data_outputs/codawork2026_projector.html`.
3. **Exécutez sur votre composition :** `QUICKSTART.md` + `ai-refresh/CCTT_QUICKSTART.md` — guide en 7 phases, manuel ou assisté par IA.
4. **Vérifier un résultat publié :** manuscrit + Informations complémentaires + JSON par pays + chaîne de hachages.
5. **Recherche de vocabulaire :** `HCI-CNT/handbook/GLOSSARY.md` v3.0 (~220 entrées : PCA, SVD, CLR/ILR, Helmert, CHSH, Tsirelson, Activation Coefficient, MC-1..MC-4).

---

## Contact et adoption

| Champ | Détails |
|---|---|
| **Exposé** | *« Surveillance compositionnelle de la dérive du mix énergétique sur le simplexe »*, CoDaWork 2026, Coimbra, 1–5 juin. Trouvez Peter pendant les sessions et les Q&R — heureux de faire une démonstration en direct du projecteur. |
| **Contact** | Peter Higgins — **PeterHiggins@RogueWaveAudio.com** · Rogue Wave Audio / Binaural Test Lab, Markham, Ontario, Canada |
| **Dépôt** | `github.com/PeterHiggins19/higgins-decomposition` · communauté : `CODA-Association/` · conférence : `CODA-Association/CODAwork2026/` |
| **Comment citer** | Higgins, P. (2026). *Compositional monitoring of energy-mix drift on the simplex.* CoDaWork 2026, Coimbra. Dépôt : github.com/PeterHiggins19/higgins-decomposition (commit dans `HS_FAST_REFRESH.json`). |
| **Comment adopter** | Forker le dépôt, exécuter le CCTT à 7 phases sur votre composition, déposer un `JOURNAL.md`. L'assistant d'IA suit les mêmes contrôles. Voir `ai-refresh/COMMUNITY_TEST_PACKET.json` pour le test d'adoption structuré. |
| **Licence** | Apache-2.0 (code) · CC BY 4.0 (documentation et figures). Entièrement open source — forker, auditer, étendre, attribuer. |

---

*L'instrument lit. L'expert décide. Les hachages portent les preuves. Le vocabulaire tient la ligne. L'IA suit le même protocole.*


---

## Verso — Opérations, symboles et carte de l'appareil

*Référence compacte des opérations effectuées par les méthodes CoDa, de ce qu'Hˢ ajoute par-dessus, de ce que CNQ ajoute dans la vue quaternion, d'où vient la fermeture dans chaque domaine, et quel appareil lit quoi.*

### Opérations centrales CoDa (la fondation qu'Aitchison a donnée au domaine en 1986)

| Opération | Symbole | Formule / définition |
|---|---|---|
| Closure | C(x) | x / Σᵢ xᵢ |
| Geometric mean | g(x) | (∏ᵢ xᵢ)^(1/D) |
| CLR (centred log-ratio) | clrᵢ(x) | log(xᵢ) − (1/D) Σⱼ log(xⱼ) |
| ILR (Helmert) | η(x) | Vᵀ · clr(x),   V·Vᵀ = I |
| Aitchison distance | d_Ait(x,y) | ‖clr(x) − clr(y)‖₂ |
| Perturbation | x ⊕ y | C(x ⊙ y)   — additive on the simplex |
| Power scaling | α ⊙ x | C(x^α)   — scalar action on the simplex |

### Opérations supplémentaires Hˢ (ce que le standard ajoute)

| Opération | Symbole | Formule / définition |
|---|---|---|
| Helmsman index | σ(t) | argmaxᵢ |clrᵢ(t+1) − clrᵢ(t)| |
| Aitchison-step | ‖Δclr(t)‖ | ‖clr(t+1) − clr(t)‖₂ |
| Power Share | πⱼ(t) | (Δclrⱼ)² / Σₖ (Δclrₖ)²,   Σ πⱼ = 1 |
| Activation Coefficient | αⱼ(t) | πⱼ(t) / ρⱼ(t)   (when ρⱼ ≥ 10⁻³) |
| Shannon entropy | H(t) | −Σⱼ ρⱼ ln ρⱼ |
| Effective carriers | K_eff(t) | exp(H(t)) |
| L2 drift | L2(p,q) | √Σᵢ (pᵢ − qᵢ)² |
| TV distance | TV(p,q) | (1/2) Σᵢ |pᵢ − qᵢ| |

### Opérations quaternioniques CNQ (la lecture de phase sur S³)

| Opération | Symbole | Formule / définition |
|---|---|---|
| Phase quaternion | q(t) | ∈ S³ ≅ SU(2) |
| Quaternion conjugate | q* | (a, −b, −c, −d) |
| Hamilton product | (p·q)_k | non-commutative quaternion multiplication |
| Quaternion sandwich | v' | q · v · q*   (rotation of 3-vector) |
| Quaternion log | log(q) | (atan2(|v|, a) / |v|) · v |
| Metric involution | M² | = I   ⟺   (q*)* = q |
| SLERP (spherical interp) | slerp(q₁,q₂,α) | sin((1−α)Ω)/sinΩ · q₁ + sin(αΩ)/sinΩ · q₂ |
| CHSH joint coherence | S | E(a,b) + E(a,b') + E(a',b) − E(a',b') |

### Contraintes de fermeture par domaine (le budget que la partition répartit)

| Domaine | Budget | Contrainte de fermeture |
|---|---|---|
| Acoustic (BTL) | c = 20·log₁₀(2) ≈ 6.02 dB | Σ Gᵢ = c   (4π → 2π baffle-step) |
| Electrical mix | 100 % generation | Σ pᵢ = 1   (coal+gas+hydro+nuclear+solar+wind+oil+other) |
| Geochemistry | 100 % weight | Σ wᵢ = 1   (major-element oxide fraction) |
| Macro-economic | 100 % GDP | Σ pᵢ = 1   (sectoral share) |
| ERB loudness (HCI-AUDIO) | 100 % perceptual | Σⱼ Σ_drivers = 1   (40 bands × 4 drivers) |

### Appareil en un coup d'œil — qui lit quoi

| Appareil | Lit | Sortie |
|---|---|---|
| CoDa community | static partition / one timestep | log-ratio biplot, distance matrix |
| CNT — tensor engine | trajectory amplitude / per-timestep | simplex coords, Helmsman, Power Share, navigation |
| CNQ — quaternion engine | phase trajectory / S³ rotation rates | quaternion path, CHSH, twin-quaternion factoring |
| HCI-AUDIO | 4-way listening-position field | ERB band × driver matrix, phase quaternions |
| HUF (umbrella) | governance | HUF-STD-001 (Publication), -002 (Tensor Train I/O), -003 (Linear Algebra Foundations) |

### Train tensoriel HUF-STD-002 — ordre, lien, mode et rang du pipeline

| Ordre | Lien | Mode (entrée → sortie) | Rang |
|---|---|---|---|
| **0** | Adapter | raw → CSV (T × D) | D = 2 … 9+ |
| **1** | CNT — closure + Helmert-ILR | (T, D) → (T, D − 1) | D − 1 |
| **2** | CNT — per-step viewpoints | (T, D − 1) → (T, K) | K = 5 metrics |
| **3** | CNT — depth tower + IR class | (T, K) → scalar block | regime label |
| **2-3** | CNQ — quaternion path | CNT JSON → (T, 4) at D = 2 / 3 / 4 | 4 ( S³ ≅ SU(2) ) |
| **4** | Vector render | JSON → plate tensor | PDF · PNG · SVG |

**Flux :** `raw → [Adapter] → CSV → [CNT v3.1.0] → cnt_*.json → [CNQ v2.0.0] → cnq_*.json → [Render] → PDF · PNG · SVG`

*K = 5 metrics: Helmsman · Aitchison-step · Power Share · Activation Coefficient · navigation_2D · Chaque lien émet SHA-256 ; chaîne reproductible de l'entrée brute à l'artefact final en une seule commande.*

### Légende des symboles

**D** carriers · **T** timesteps · **pᵢ** portion · **Gᵢ** gain (dB) · **F_c** cutoff · **τ** group delay · **n̂** rotation axis · **q** unit quaternion · **σ** Helmsman · **αⱼ** Activation · **πⱼ** Power Share · **η** ILR coordinate · **clr** centred log-ratio · **g(x)** geometric mean · **S^(D−1)** simplex · **S³** 3-sphere ≅ SU(2)

---

*Même entrée, même sortie, toujours. L'instrument lit. L'expert décide. Les hachages portent les reçus. Le vocabulaire tient la ligne. L'IA suit le même protocole.*
