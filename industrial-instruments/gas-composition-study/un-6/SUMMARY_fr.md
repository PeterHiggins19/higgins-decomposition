# Études compositionnelles de gaz et de fluides Hˢ — Résumé (FR)

*2026‑06‑11. Moteur : CN‑TT v4. Ouvert, reproductible, à niveaux de certitude. **Traduction provisoire en attente de révision par un expert natif** (convention HUF) ; la version anglaise fait foi.*

Hˢ est un instrument déterministe et ouvert qui lit la **composition** d'un gaz ou d'un fluide au fil du temps — *quel composant pilote chaque changement, quand le régime bascule, et si un changement est réel ou une panne de capteur* — sans perte et avec une empreinte (hash) reproductible. C'est la **quatrième catégorie de surveillance (MC‑4)** : celle qui lit les rapports, que les alarmes de seuil ignorent.

Quatre études ouvertes et reproductibles (chacune : un générateur transparent, une exécution réelle du moteur, une figure, la science, et une source de données publique cible) :

1. **Support‑vie en boucle fermée O₂/CO₂/N₂** — pendant l'essentiel de l'essai, chaque alarme mono‑canal restait au vert alors que la composition bougeait nettement (le coût de la « cécité aux rapports »).
2. **Eaux de production pétrole & gaz** (CoDaWork 2026, Engle et al. ; base publique USGS Produced Waters) — la transition de formation est détectée et les valeurs sous le seuil de détection traitées de façon déterministe.
3. **Gaz sanguin / alvéolaire** (quatre parties, lues **exactement** comme un quaternion) — O₂ et CO₂ sont désignés comme moteurs de la désaturation lors d'une apnée.
4. **Atmosphère de cabine spatiale** (type ISS) — le cycle d'élimination du CO₂ est suivi et un **événement de contaminant à l'état de trace est détecté** et attribué au bon canal.

**Pourquoi public :** pour que chacun, dans tout domaine, puisse lire sa propre composition de gaz ou de fluide avec un seul instrument déterministe et **partager les résultats au bénéfice de tous**. L'instrument lit ; l'expert décide ; les empreintes portent les preuves.
