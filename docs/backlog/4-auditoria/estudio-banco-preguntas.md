# Estudio de banco de preguntas (autoría admin: generar · configurar · editar)

- **Estado:** Handoff Ready (arquitectura) — pendiente preflight 🧩 Codex
- **Creado:** 2026-06-13 · **Autor del handoff:** 🏛️ Claude (sesión con 🧑 Octavio)
- **Prioridad:** P2 · **Cartera:** educativa / producto
- **Tipo:** producto · pedagogía · infraestructura
- **Dueño sugerido:** 🏛️ Claude (handoff + cierre) → 🧩 Codex (preflight + auditoría) →
  🔨 Antigravity (construcción `feat/estudio-banco-preguntas`). 🧑 Usuario: infra de storage + QA.

> Una tarjeta está **Ready** solo si todos los campos están completos (ver
> `docs/gobernanza/proceso-multiagente.md` §3). Este handoff es grande: se construye **por fases**,
> cada fase puede ser su propio PR/rama. Las fases 1–3 no dependen de infra nueva; la **Fase 4
> (multimodal) está BLOQUEADA** hasta que el 🧑 configure almacenamiento externo.

## Origen / contexto
Surge de la sesión 2026-06-13. Octavio quiere dejar de cargar preguntas por el admin de Django y
tener un **estudio propio solo-admin** para: (1) generar el banco con control fino de cantidades y
distribución, (2) orientar la IA con **imágenes + descripción**, y (3) **ver y editar** preguntas y
alternativas. El generador IA ya existe (`apps/content/services/ai_generation_service.py`, Gemini
2.5 Flash, multimodal y gratis) y ya publica directo; este feature lo envuelve en un flujo de autoría
con configuración por recurso.

## Decisiones cerradas (🧑 + 🏛️, 2026-06-13)
1. **Estructura por nivel** (se mantienen los 3 niveles: Definición / Ejercicios / Aplicación).
2. **Pools separados por modo** (práctica ≠ evaluación): default **15 práctica + 10 evaluación por
   nivel**. Nada de `mode="ambas"` en contenido nuevo.
3. **Cuántas aparecen por intento:** default **5 práctica / 3 evaluación** por nivel (configurable).
4. **Distribución por nivel** del total: configurable por recurso.
5. **Política de evaluación:** 3 intentos mientras no se apruebe; **recuperación practicando 5/5
   correctas** (sube el umbral actual de 80% → 100%); **repetir evaluaciones aprobadas libremente,
   sin re-otorgar XP/estrellas** (no inflar progreso; se conserva el mejor resultado).
6. **Imágenes de orientación: se conservan** (ligadas al recurso, para regenerar) → **requiere
   storage externo** (Railway borra media en cada deploy).
7. **Flujo de generación:** la IA produce **borrador**; el admin revisa/edita y **publica en lote**
   (reemplaza el "publicar directo" temporal de esta sesión, que queda como opción configurable).
8. **Generación en tandas** (HTMX, lotes ~5) con barra de progreso, para no chocar con el timeout de
   gunicorn (~30s en prod).

## Objetivo (una frase)
Dar al administrador un **estudio solo-admin** para generar (con IA orientada por imágenes y texto),
**configurar por recurso** (totales, distribución por nivel, cuántas aparecen, política de intentos) y
**editar** el banco de preguntas/alternativas, sin pasar por el admin de Django.

## Fuentes a leer (rutas concretas)
- `apps/content/services/ai_generation_service.py` — generador actual (Gemini/OpenAI/mock); aquí se
  agrega soporte multimodal (`inline_data`) y el paso de instrucciones/imágenes.
- `apps/content/services/evaluation_service.py` — `QUESTIONS_PER_LEVEL`, `MAX_EVAL_ATTEMPTS`,
  `PRACTICE_RECOVERY_THRESHOLD`, `get_questions_for_quiz`, `get_attempts_info`, `_can_recover`,
  `submit_quiz`. **La config por recurso reemplaza estas constantes** (con fallback a los defaults).
- `apps/content/models/question.py` — `Question` (level, mode, status, order) y `Choice`.
- `apps/content/models/resource.py` — `Resource` (ya usa `FileField upload_to`).
- `apps/content/views/publish_studio.py` + `apps/content/urls/publish_urls.py` +
  `apps/content/views/permissions.py` (`is_admin = superuser`) — **patrón a replicar** (página
  solo-admin, `@user_passes_test(is_admin)`).
- `templates/pages/publish_studio.html` + `static/js/publish_studio.js` — patrón de UI/JS (cascada de
  taxonomía, CSRF helper) reutilizable.
- `apps/content/admin.py` (acción `generar_preguntas_ia_action`) — lógica de generación a migrar/compartir.
- `config/settings/base.py` y `production.py` — `STORAGES` (hoy `FileSystemStorage`), `MEDIA_URL/ROOT`.
- `apps/core/middleware.py` — CSP con nonce (todo JS externo o con `nonce="{{ csp_nonce }}"`; sin inline).

## Modelo de datos (propuesta)
### `ResourceQuizConfig` (OneToOne → `Resource`)
Config por recurso; si no existe, se usan defaults globales (constantes actuales).
- `counts` — `JSONField` con la matriz nivel×modo. Esquema:
  ```json
  {"1": {"practice": {"pool": 15, "shown": 5}, "eval": {"pool": 10, "shown": 3}},
   "2": {...}, "3": {...}}
  ```
  Validado por el form (enteros ≥0; `shown ≤ pool`).
- `pass_threshold` — `FloatField` default 1.0 (5/5).
- `max_attempts` — `PositiveSmallIntegerField` default 3.
- `recovery_rule` — `CharField(choices=["practice_5_5","none"])` default `practice_5_5`.
- `allow_retake_passed` — `BooleanField` default True.
- `autopublish` — `BooleanField` default False (generar en borrador).

Helper `get_quiz_config(resource)` → objeto efectivo (config del recurso fundida con defaults
globales). **Todo el runtime del quiz pasa a leer de aquí** (Fase 5).

### `ResourceGenerationAsset` (FK → `Resource`)  — Fase 4
- `image` — `ImageField(upload_to="generation/assets/")` (storage externo).
- `description` — `TextField(blank=True)` (orientación de la IA).
- `created_at`. Varias por recurso. Se envían como contexto multimodal al generar.

> Alternativa considerada y descartada para v1: modelo normalizado `QuizLevelConfig` (FK+level+mode).
> El `JSONField` es suficiente (no se consulta por SQL, solo se lee por recurso) y evita 6 filas/recurso.

## Arquitectura — las 3 piezas (todas solo-admin, namespace `content`)
### A. Estudio de generación — `GET/POST /publicar/preguntas/`
- **Dos modos de selección de recursos** (decisión 2026-06-14):
  1. **Por tema:** selector de Tema → se marcan automáticamente todos sus recursos (checklist);
     el admin puede desmarcar los que no quiera.
  2. **Individual:** checkboxes libres agrupados por Asignatura › Tema para seleccionar recursos sueltos.
  - La config de generación se define **una sola vez** y se aplica a todos los recursos seleccionados.
  - La IA genera recurso por recurso en secuencia.
- Inputs: **pool por nivel/modo** (práctica/evaluación por separado), **cuántas aparecen por intento**,
  modo borrador/autopublish.
- **Imágenes + descripción** (Fase 4): multipart; se guardan como `ResourceGenerationAsset`.
- **Generación en tandas:** un endpoint `POST /publicar/preguntas/generar-tanda/` que genera **un
  lote chico** (p. ej. 5 de un (nivel, modo)) y devuelve una fila de progreso; el front encadena
  llamadas HTMX (`hx-trigger="load"` en la fila siguiente) hasta completar la matriz. Cada request
  corto ⇒ a prueba de timeout.

### Puntos de acceso (decisión 2026-06-14)
- **Navbar** (`base.html`, bloque `{% if user.is_staff %}`): nuevo link "Banco de Preguntas"
  → `{% url 'content:question_studio' %}` entre "Estudio de Publicación" y "Analítica".
- **Página de recurso** (`templates/pages/resource_detail.html` o equiv.): botón admin-only
  "Gestionar preguntas" → `{% url 'content:question_review' resource.slug %}`. Solo visible
  para `user.is_staff`.

### B. Página de revisión/edición — `GET /publicar/preguntas/<slug>/`
- Tabla de `Question` del recurso (filtros nivel/modo/estado).
- **Edición inline HTMX**: enunciado, explicación, alternativas (texto + cuál es correcta), orden,
  estado. Crear/borrar pregunta y alternativa a mano. **Publicar/archivar en lote**.
- Endpoints HTMX dedicados (`.../editar/<id>/`, `.../alternativa/<id>/`, etc.), todos `is_admin`.

### C. Runtime del quiz (Fase 5) — leer config por recurso
- `get_questions_for_quiz` usa `counts[level][mode].shown` (default 5/3) y solo el pool del modo.
- `get_attempts_info` / `submit_quiz` usan `pass_threshold`, `max_attempts`, `recovery_rule`,
  `allow_retake_passed`. Quitar el bloqueo "ya aprobaste" del `quiz_start`; al re-aprobar, **no
  re-otorgar XP** (guardar en `gamification_service`: si el nivel ya estaba aprobado, no premiar).

## Fases (orden por valor/riesgo)
1. **Config por recurso** — modelo `ResourceQuizConfig` + `get_quiz_config()` + migración + tests.
2. **Página de edición/revisión** (pieza B) — valor inmediato sobre lo ya generado; bajo riesgo.
3. **Estudio de generación** (pieza A, sin imágenes) — total/distribución/cuántas + generación en
   tandas en borrador.
4. **Multimodal** (imágenes + descripción) — **BLOQUEADA por infra** (storage externo). Soporte
   `inline_data` en el servicio + `ResourceGenerationAsset`.
5. **Wire al runtime** (pieza C) — 5/3 configurable, recuperación 5/5, repetir aprobadas sin re-XP.

## No-objetivos (FUERA)
- ❌ Reemplazar el admin de Django para otros modelos. ❌ Editor WYSIWYG/LaTeX (KaTeX es otra tarjeta).
- ❌ Generación asíncrona con cola/worker (las tandas HTMX bastan). ❌ Versionado/historial de
  preguntas. ❌ Traer la config a un panel global (es por recurso). ❌ Storage externo en este PR
  (es prerrequisito de infra del 🧑, no código de feature).

## Criterios de aceptación (verificables)
- [ ] Barrera verde: `test` · `check --deploy` · `makemigrations --check --dry-run`.
- [ ] Todas las páginas/endpoints nuevos rechazan no-superuser (302/403) — test de permisos.
- [ ] **Fase 1:** `get_quiz_config(resource)` devuelve la config del recurso o los defaults globales;
      test de fallback y de override.
- [ ] **Fase 2:** editar enunciado/alternativa/estado por HTMX persiste y revalida (exactamente una
      correcta por pregunta); publicar en lote cambia estado; CSP intacta (sin inline).
- [ ] **Fase 3:** generar crea N preguntas en **borrador** según la matriz; las tandas no superan
      ~10s cada una; la barra llega a 100% sin recargar.
- [ ] **Fase 5:** un recurso con `counts` custom muestra esa cantidad en el quiz; recuperación exige
      5/5; una evaluación aprobada puede repetirse y **no** suma XP la 2ª vez (test de gamificación).
- [ ] Si toca CSS → cache-buster `?v=N` subido.

## Plan de pruebas
- **Unit:** `get_quiz_config` (fallback/override); validación de `counts` (`shown ≤ pool`); selección
  por modo respeta pools separados; recuperación 5/5; no-doble-XP al re-aprobar.
- **Vistas:** permisos `is_admin` en las 3 piezas; edición inline (happy + inválido: 0 o 2 correctas);
  generación en tanda (mock IA en tests, como hoy en `test_ai_generation`).
- **QA manual (🧑):** generar un recurso completo; editar y publicar; rendir el quiz y verificar
  cantidades/recuperación/repetir-aprobada; (Fase 4) subir imagen y ver que orienta la generación.

## Riesgos / rollback
- **Timeout de generación** → mitigado con tandas chicas HTMX (riesgo principal del feature).
- **Migración de config** → aditiva (modelo nuevo, OneToOne opcional); rollback = revertir migración.
- **Romper el quiz al cambiar las constantes por config (Fase 5)** → mantener defaults idénticos a
  los actuales; feature flag implícito (sin `ResourceQuizConfig` ⇒ comportamiento actual). Rollback
  por fase (cada una su PR).
- **Storage externo (Fase 4)** → si el 🧑 no lo configura, la Fase 4 no se construye; las fases 1–3 y
  5 no dependen de él. Coste/credenciales de S3/Cloudinary = decisión del 🧑.
- **Costo IA** → Gemini 2.5 Flash free tier; las tandas permiten cortar a mitad sin perder lo creado.

## Preflight para 🧩 Codex
- Confirmar firma real de `generate_questions_for_resource` y que el `inline_data` de Gemini 2.5
  Flash acepta imágenes como se plantea (Fase 4).
- Validar que mover el runtime a `get_quiz_config` no rompe `test_evaluation` (60 tests) ni la
  gamificación (XP/estrellas/skills); enumerar todos los usos de `QUESTIONS_PER_LEVEL`.
- Revisar N+1 en la página de edición (prefetch de `choices`) y en la selección por pools.
- Confirmar el patrón de storage externo recomendado (django-storages+S3 vs Cloudinary) y su impacto
  en `Resource.file` existente.

## Construcción para 🔨 Antigravity
Rama `feat/estudio-banco-preguntas`. Construir **por fases** (PRs separados sugeridos): F1 config →
F2 edición → F3 generación → (F4 multimodal, si hay storage) → F5 runtime. JS externo o con nonce
(CSP), CSS externo con cache-buster. Completar "Qué se hizo".

---

## Qué se hizo

- **Modelo de Configuración (`Fase 1`):** Implementamos `ResourceQuizConfig` que mapea mediante una relación `OneToOne` cada recurso a su configuración (JSON con límites por nivel/modo, intentos máximos, umbral de aprobación, regla de recuperación, retoma de aprobados y autopublicación).
- **Consistencia y Fallbacks:** Creamos el helper `get_quiz_config` que consolida la configuración con los defaults globales idénticos a los del sistema preexistente para evitar regresiones.
- **Panel de Edición Inline y Acciones en Lote (`Fase 2`):** Construimos la vista de revisión (`question_review`) con endpoints HTMX para crear, actualizar y borrar preguntas y alternativas en la misma página de forma dinámica. Se implementó una barra de acciones en lote (publicar, archivar, eliminar) y scripts con nonces para cumplir con las directrices de seguridad (CSP).
- **Estudio de Generación por Tandas (`Fase 3`):** Desarrollamos el panel de selección múltiple jerárquico por Tema o de forma individual, y un endpoint de HTMX secuencial que procesa recurso por recurso (tanda por tanda) para eludir los timeouts de red de la IA, mostrando una barra de progreso interactiva en tiempo real y logs en consola.
- **Generador con IA:** Se extendió `generate_questions_for_resource` para permitir guardar opcionalmente las preguntas en estado `"borrador"` o `"publicada"`.
- **Runtime de Quiz y Gamificación (`Fase 5`):** Adaptamos `evaluation_service.py` y `gamification_service.py` para usar las configuraciones por recurso en el examen del alumno, obligar la regla de recuperación perfecta (100% de aciertos en práctica) y permitir repetir evaluaciones aprobadas sin duplicación de estrellas o XP.
- **Tests y Validación:** Escribimos pruebas unitarias robustas que cubren todas las facetas (fallbacks, overrides, validaciones de pool/mostradas, re-tomas y gamificación) y se ejecutó la suite completa (180 tests) resultando en verde.
