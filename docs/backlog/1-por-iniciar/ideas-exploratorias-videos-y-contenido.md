# Ideas exploratorias — producción de video con IA y presentación de contenido

> **Nota de formato:** esto NO es una tarjeta lista para arquitectura (no usa
> `_plantilla.md`). Es un **registro vivo de ideas sueltas**, con análisis de
> relación/sinergia y pros/contras, para decidir más adelante cuál (si alguna) se
> convierte en tarjeta formal con handoff. Se agregan ideas nuevas al final,
> manteniendo las anteriores.

**Creado:** 2026-08-08 · **Autor:** 🧑 (Octavio) + 🏛️ Claude (registro y análisis)

---

## Idea A — Rediseño "cuento ilustrado" de `node_detail.html`

**De dónde salió:** conversación de esta sesión, al mismo tiempo que el rediseño del
rail de hitos ya implementado en `node_detail.html`.

**La idea, en palabras del usuario:** usar las zonas en blanco de la página del nodo
(donde hoy no hay nada escrito) como si fuera un paisaje/ilustración de fondo que se
pueda apreciar — que las clases se sientan "como un cuento", con fotos/ilustraciones en
medio del contenido, y **el texto superpuesto en medio de la foto** (no la foto como
adorno al lado, sino el texto integrado dentro de la ilustración).

**Estado:** solo mencionada y aclarada una vez — **no se llegó a brainstorming formal**
(se priorizó el sistema de auditoría primero, ver Idea B). Falta: definir de dónde
salen las ilustraciones (¿generadas por IA, una por nodo? ¿reutilizadas por bloque/eje?
¿ilustradas a mano?), y si esto convive con el rail de hitos ya construido o lo
reemplaza.

**Sinergia con otras ideas:** ver §"Relación entre ideas" más abajo — se conecta
directamente con la Idea 1 (producción de video con IA) por el pipeline de generación de
imágenes.

---

## Idea B — Sistema de auditoría universal de contenido + autoregistro por commit

**Estado:** ✅ **ya tiene spec formal completo y aprobado**, commiteado en
[`docs/superpowers/specs/2026-08-08-auditoria-contenido-nodos-design.md`](../../superpowers/specs/2026-08-08-auditoria-contenido-nodos-design.md).
No se repite el detalle acá — ese documento es la fuente de verdad. Resumen de una línea:
un comando (`audit_node_content`) + un hook de pre-commit que verifican y registran
automáticamente si cada recurso cumple el checklist §5 de `pauta-contenido.md` (12
secciones, checkpoints, ejemplos, banco de ejercicios), sin bloquear commits.

**Sinergia con otras ideas:** mínima/indirecta — es sobre *corrección y completitud del
texto*, no sobre *cómo se presenta visualmente* ni sobre producción de video. No hay
overlap técnico real con las ideas A o 1 (ver abajo, honestidad ante todo: no fuerzo una
conexión que no existe).

---

## Idea 1 — Clases grabadas con croma + escenarios + animación por IA

**La idea, en palabras del usuario:** grabar una clase real explicándole algo a alguien
(con croma/pantalla verde), pero organizada **por escenarios**: dentro de cada escenario
la escena se mantiene visualmente constante (misma pose/plano/fondo), para que después
se pueda generar una imagen/ilustración de ese escenario concreto, y pedirle a una IA que
**anime esa imagen**. El profesor (persona real, sobre croma) va explicando en vivo,
sincronizado con lo que se va mostrando/animando en pantalla.

En otras palabras: es una técnica híbrida — **profesor real (croma) + fondo/escena
animada por IA**, cortada en bloques ("escenarios") para que cada uno tenga una
ilustración y animación propias, en vez de un video 100% en vivo o 100% animado.

### Cómo se lograría (flujo concreto)

1. **Guion/escaleta previa:** decidir de antemano en qué "escenarios" se divide la
   explicación (ej. escenario 1 = plantear el problema, escenario 2 = desarrollar la
   fórmula, escenario 3 = ejemplo numérico, escenario 4 = conclusión). Esto es trabajo de
   planificación, no de software.
2. **Grabación con croma:** el profesor graba cada escenario (o la clase completa,
   después cortada en esos tramos), con fondo verde/croma. Software de captura: OBS
   Studio (gratis, chroma key en vivo) o cualquier cámara + remoción de fondo en
   post-producción (ej. filtro `chromakey`/`colorkey` de `ffmpeg`, sin costo).
3. **Generación de imagen por escenario:** por cada escenario, un prompt a un generador
   de imágenes IA (DALL-E, Midjourney, Stable Diffusion, Gemini/Imagen, etc. — herramienta
   externa, no forma parte de este repo) que capture la idea visual de ese tramo.
4. **Animación de la imagen:** esa imagen fija se pasa a una herramienta de
   imagen→video IA (Runway, Kling, Pika, Luma, etc.) para animarla.
5. **Composición final:** se monta el profesor (ya sin fondo verde) sobre/junto a la
   escena animada, sincronizado en tiempo con la narración — edición de video estándar
   (DaVinci Resolve, Premiere, CapCut, o `ffmpeg` programático).

### Lo bueno

- Técnica real y usada hoy en producción de contenido educativo/YouTube (híbrido
  talking-head + motion graphics) — no es ciencia ficción, es alcanzable con
  herramientas que ya existen.
- El croma y la remoción de fondo son gratis (OBS/ffmpeg) — el costo real está solo en
  la generación de imagen/animación IA.
- Se conecta con infraestructura que **ya existe en el proyecto** (ver sinergia abajo):
  el pipeline de ingesta de transcripciones de YouTube (`backfill_transcripts`,
  `apps/content/services/publication_pipeline_service.py`) ya sabe leer un video y sacar
  su transcripción/documento canónico — podría extenderse para proponer automáticamente
  los cortes de "escenario" + un prompt de imagen por escenario, en vez de hacerlo 100%
  a mano.

### Lo malo (honesto, sin endulzar)

1. **Es mayormente producción de video, no código de sitio web.** El grueso del trabajo
   (grabar, croma, generar imágenes, animar, montar) pasa **fuera** de este repo Django,
   en herramientas de video/IA externas — parecido a cómo hoy el `profeonline-uploader`
   (Node, fuera de este repo) es el que sube contenido, no Python. Este repo, en el mejor
   caso, solo **recibe** el video terminado (como ya hace hoy con YouTube).
2. **Consistencia visual entre escenarios es un problema real y no resuelto en general:**
   generar varias imágenes IA por separado (una por escenario) tiende a dar estilos,
   paletas y "personajes" distintos entre sí si no se fija una referencia — el video
   final puede verse visualmente inconexo entre tramos. Se puede mitigar (guía de estilo
   fija, mismo seed/referencia en cada generación) pero no se elimina del todo.
3. **Costo y tiempo por video:** las herramientas de imagen→video IA de buena calidad
   cobran por segundo generado — a escala (muchos temas × muchos escenarios) el costo y
   el tiempo de producción por clase pueden ser altos comparado con un video hablado
   normal o una guía de texto.
4. **Sincronización fina:** que la animación calce con el ritmo real de la explicación
   hablada (que varía) casi siempre requiere ajuste manual de timeline, no es
   "generar y listo".
5. **Riesgo pedagógico:** una animación IA con aspecto pulido pero con un error visual
   (un gráfico mal proporcionado, una fórmula animada incorrectamente) se ve igual de
   "autoritativa" que una correcta — necesita la misma revisión de calidad que ya se le
   exige al contenido de texto (ver Idea B).

### Relación con las otras ideas — ¿hay sinergia real?

- **Con la Idea A (cuento ilustrado):** **sí, sinergia directa y concreta.** Ambas ideas
  necesitan lo mismo en el fondo: **una ilustración por concepto/escenario, generada por
  IA, con estilo consistente.** Si se construye un pipeline de "tema → prompt de imagen →
  ilustración" para los videos (Idea 1), la MISMA ilustración (o la misma guía de estilo)
  podría reusarse como fondo de la página del nodo en `node_detail.html` (Idea A) — un
  solo trabajo de generación de arte, dos superficies de consumo (video + web). Evita
  duplicar el esfuerzo de diseño visual.
- **Con la Idea B (auditoría):** **poca o ninguna sinergia técnica directa.** Son
  preocupaciones distintas (corrección de texto vs. producción audiovisual). La única
  conexión indirecta: si algún día el video animado reemplaza o resume una sección de
  `NodeContent`, la auditoría debería eventualmente saber que ese campo "está cubierto
  por video" en vez de exigir el texto — pero eso es especulativo y no hace falta
  resolverlo ahora.
- **Con infraestructura ya existente en el repo:** el pipeline de transcripción/ingesta
  de YouTube (`publication_pipeline_service.py`) es el punto de enganche natural — los
  videos que resulten de la Idea 1, una vez subidos a YouTube, entrarían al mismo camino
  que el contenido audiovisual de hoy (transcripción → documento canónico → guía/preguntas),
  sin necesidad de un pipeline paralelo nuevo para "recibir" el video.

### Sugerencias (no pedidas explícitamente, pero relevantes)

1. **Probar en chico antes de comprometerse:** un solo tema, de punta a punta manual
   (grabar, 3-4 escenarios, generar imágenes, animar 1 solo, montar) — para medir tiempo
   y costo real por video antes de decidir si esto se vuelve el método estándar de
   producción.
2. **Definir una guía de estilo visual fija primero** (referencia de personaje/paleta/
   estilo de ilustración) y usarla como input constante en cada generación de imagen —
   ataca directamente el problema #2 de consistencia.
3. **Reusar el pipeline de transcripción existente** para generar automáticamente una
   primera propuesta de cortes de escenario + prompt de imagen por escenario a partir del
   guion/transcripción, que el usuario después ajusta a mano en vez de planificar desde
   cero.
4. **Tratar esto como pipeline externo de producción** (como el uploader Node), no como
   una feature para construir dentro del repo Django — mantiene la separación de
   responsabilidades que ya sigue el proyecto.

---

## Resumen de relaciones (tabla)

| Par de ideas | ¿Sinergia? | Por qué |
|---|---|---|
| A (cuento ilustrado) ↔ 1 (video+IA) | ✅ Sí, fuerte | Ambas necesitan el mismo insumo: ilustración IA por concepto, con estilo consistente. Un solo pipeline de arte podría alimentar a las dos. |
| A (cuento ilustrado) ↔ B (auditoría) | ❌ No directa | Una es visual/presentación, la otra es completitud de texto. No comparten código ni datos. |
| 1 (video+IA) ↔ B (auditoría) | ❌ No directa (por ahora) | Producción audiovisual vs. corrección de contenido escrito. Conexión solo hipotética a futuro. |

**Siguiente paso sugerido:** si se quiere avanzar, lo más eficiente sería brainstormear
la Idea A (cuento ilustrado) y la Idea 1 (video+IA) **juntas**, ya que comparten el
mismo insumo de fondo (ilustración por concepto) — en vez de diseñarlas por separado y
descubrir la sinergia después.

---

## Idea 1b — Mapa conceptual por escenas como guion, en formato Reel de Instagram

**De dónde salió:** al profundizar la Idea 1, se aclaró que el "mega mapa conceptual"
que el usuario quiere para explicar y mostrar cada cosa es, específicamente, una
**herramienta de planificación de video** (no algo que viva en la página web) — la IA
propone el mapa a partir del `NodeContent` ya existente de un recurso, agrupado en
escenas. Se construyó un demo concreto con contenido real (no inventado) para validar la
idea antes de diseñarla formalmente:

**Demo (Artifact):** https://claude.ai/code/artifact/f11575f9-1566-45fa-b201-6c08b2620e2b
— mapa conceptual de "Identificación de los Números Naturales (ℕ)"
(`MAT.NUM.ENTEROS_CONJUNTO.NATURALES`), agrupado automáticamente en 4 escenas (Plantear
la idea → Formalizar → Ejemplo resuelto → Error común), cada subconcepto etiquetado con
el campo exacto de `NodeContent` del que sale.

**El giro nuevo (esta conversación):** el usuario propone usar esa misma estructura de
escenas como **formato de Reel para Instagram** — contenido corto vertical, no la clase
completa. Cada "escena" del mapa (que ya está pensada como un tramo autocontenido y
visualmente constante, ver Idea 1) calza naturalmente con la duración y el ritmo de un
Reel (uno de los 4 tramos = un Reel de ~15-30s, o los 4 encadenados = un Reel de tema
completo).

### Por qué tiene sentido (lo bueno)

- **Reusa el mismo insumo que la Idea 1 y la Idea A** — no es una cuarta idea aislada,
  es una salida de distribución más para el mismo mapa/guion generado por IA. Un mapa,
  tres consumos posibles: clase larga (Idea 1), fondo de página web (Idea A), Reel corto
  (esta idea).
- Los Reels premian justo lo que ya exige la Idea 1: escenas cortas, visualmente
  constantes, con una sola idea por tramo — no hay que replanificar el formato desde
  cero para adaptarlo a IG.
- Sirve como **marketing/adquisición** (visibilidad, tráfico hacia el sitio) más que
  como el contenido educativo principal — un objetivo de negocio distinto y
  complementario al de la Idea 1 (que es contenido de clase completo).

### Lo malo / a tener en cuenta

- Formato verticalidad (9:16) — la composición del croma + escena animada de la Idea 1
  probablemente necesite encuadre distinto al de un video horizontal de clase; no es
  un simple recorte automático.
- Un Reel vive de gancho/ritmo (primeros 1-2 segundos) más que de precisión pedagógica
  completa — puede tentar a simplificar de más un concepto matemático hasta perder
  exactitud; conviene revisión de contenido igual que cualquier otro material (ver
  Idea B, aunque no aplica directo a video).
- Es otro canal de producción/publicación (Instagram) que no tiene hoy ningún pipeline
  de recepción en este repo (a diferencia de YouTube, que sí entra por
  `publication_pipeline_service.py`) — si se quiere trazabilidad (qué Reel corresponde a
  qué nodo), habría que decidir cómo/si se registra en el sitio.

### Relación con las demás ideas

Refuerza aún más la sinergia entre A y 1 ya detectada: ahora hay **tres** salidas
posibles del mismo mapa conceptual generado por IA (clase larga, fondo de página, Reel),
no dos. No cambia la relación con la Idea B (auditoría) — sigue sin sinergia directa.
