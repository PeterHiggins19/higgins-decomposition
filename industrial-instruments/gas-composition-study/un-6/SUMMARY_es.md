# Estudios composicionales de gases y fluidos Hˢ — Resumen (ES)

*2026‑06‑11. Motor: CN‑TT v4. Abierto, reproducible, con niveles de certeza. **Traducción provisional pendiente de revisión por experto nativo** (convención HUF); la versión en inglés es la canónica.*

Hˢ es un instrumento determinista y abierto que lee la **composición** de un gas o un fluido a lo largo del tiempo — *qué componente impulsa cada cambio, cuándo cambia el régimen y si un cambio es real o un fallo del sensor* — sin pérdida y con una huella (hash) reproducible. Es la **cuarta categoría de monitorización (MC‑4)**: la que lee las proporciones, que las alarmas de umbral pasan por alto.

Cuatro estudios abiertos y reproducibles (cada uno: un generador transparente, una ejecución real del motor, una figura, la ciencia y una fuente de datos pública objetivo):

1. **Soporte vital en circuito cerrado O₂/CO₂/N₂** — durante la mayor parte del ensayo cada alarma de un solo canal permaneció en verde mientras la composición se movía claramente (el coste de la «ceguera a las proporciones»).
2. **Agua producida de petróleo y gas** (CoDaWork 2026, Engle et al.; base pública USGS Produced Waters) — se detecta la transición de formación y se tratan de forma determinista los valores por debajo del límite de detección.
3. **Gas sanguíneo / alveolar** (cuatro partes, leídas **exactamente** como un cuaternión) — O₂ y CO₂ se identifican como los impulsores de la desaturación durante una apnea.
4. **Atmósfera de cabina de nave espacial** (tipo ISS) — se sigue el ciclo de eliminación de CO₂ y se **detecta un evento de contaminante traza**, atribuido al canal correcto.

**Por qué es público:** para que cualquiera, en cualquier campo, pueda leer su propia composición de gas o fluido con un único instrumento determinista y **compartir los resultados en beneficio de todos**. El instrumento lee; el experto decide; las huellas llevan los comprobantes.
