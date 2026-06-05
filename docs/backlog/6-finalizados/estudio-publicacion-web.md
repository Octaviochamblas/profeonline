# Estudio de publicación: página web asistida para preparar subidas de video

- **Estado:** Handoff Ready (arquitectura) — **Fase 0 + Fase 1** · **Preflight 🧩 Codex ✅** (sin objeciones bloqueantes, 2026-06-04)
- **Creado:** 2026-06-04 · **Handoff:** 2026-06-04 (🏛️ Claude)
- **Prioridad:** P2 · **Cartera:** ingeniería
- **Tipo:** producto · infraestructura
- **Dueño sugerido:** 🧩 Codex (preflight) → 🔨 Antigravity (construcción `feat/estudio-publicacion-fase1`) → 🏛️ Claude (cierre)

> **Origen:** planificación 🧑 Octavio + 🤖 Claude, refinada por **🧩 Codex** (8 acotaciones, todas
> integradas) y verificada contra el código real. Alcance de **ESTA** tarjeta: el contrato del job
> (Fase 0) + la **página web que genera el JSON** (Fase 1). **Fase 2** (cola + agente + playlists +
> preflight server-side + reseña IA) va en una tarjeta separada para mantener el diff acotado.

## 🔄 REVISIÓN 2026-06-04 — SIMPLIFICACIÓN (SUPERSEDE lo de abajo)
🧑 Octavio pidió una versión **mucho más simple** tras ver la página construida. **Esta sección
manda**; lo de más abajo (Objetivo/Propuesta/Contrato `upload-job/v1`/criterios) queda **obsoleto**
salvo lo que se reutilice. La tarjeta vuelve a `3-construccion/` para que 🔨 Antigravity **recorte**
la implementación en la **misma rama** `feat/estudio-publicacion-fase1`. **Sin migraciones.**

**Idea:** elegir varios videos (por nombre), elegir solo **Área/Asignatura/Tema/Módulo** + **Playlist**
+ una **indicación libre**, y descargar **una orden de lote**. Codex hace el resto tal cual
(título, descripción, miniatura, subida y publicación por el webhook) por **cada** archivo.

**Decisiones 🧑:** (1) archivos = `<input type=file multiple>` que captura **solo nombres** (no sube
contenido); (2) **mantener** creación inline `+ Crear`; (3) **misma config para todo el lote**;
(4) **sin niveles** en la UI (puede heredar de `Topic.levels`); (5) **sin** privacidad, miniatura,
copy en la web, duplicados ni título por video (lo hace Codex).

**ELIMINAR:** vistas `publish_copy_preview.py` y `publish_duplicates.py` (+ sus rutas en
`publish_urls.py`, exports en `views/__init__.py` y sus tests); en template/JS: secciones de copy,
miniatura (paleta/texto/`class_label`), privacidad, alertas de duplicados y título por recurso.

**MANTENER:** `subject_options`/`module_options`, `topic_options`, `publish_inline_create` (con CSRF
+ `name = name or title`), `youtube_utils.extract_playlist_id`, `resource_copy.py` (lo usa el comando
`import_youtube_resources`), y el enlace de nav en `base.html`.

**MODIFICAR `publish_studio.py`:** GET solo con `areas`. POST: recibir `file_names` (lista, campo
oculto JSON) + slugs de taxonomía (mismas validaciones de pertenencia ya escritas) + playlist
existente opcional (`extract_playlist_id`) o solicitud de crear playlist nueva + `instructions`; validar **≥1 archivo** y **área+asig+tema**;
devolver la **orden de lote** `.json` (attachment).

**JS `publish_studio.js`:** leer `File.name`, listar con DOM API (sin `innerHTML` interpolado),
poblar campo oculto `file_names`; **no** subir contenido (el `<input type=file>` queda sin `name`/
fuera del POST). Mantener selects dependientes, modales inline (CSRF), `extract_playlist_id` y el
bloqueo de descarga si faltan archivos/área/asignatura/tema o si falta el título al crear una playlist nueva.

**Contrato nuevo (batch) → documentar en `docs/gobernanza/inventario-operacional.md`** (reemplaza `upload-job/v1`):
```json
{ "schema": "profeonline.upload-batch/v1",
  "files": ["clase1.mp4", "clase2.mp4"],
  "taxonomy": {"area_slug": "...", "subject_slug": "...", "topic_slug": "...", "module_slug": null},
  "youtube": {"playlist_id": "PLxxx", "playlist_title": "...", "create_playlist": false, "new_playlist": null},
  "instructions": "texto libre aplicado a todos los videos del lote" }
```

**Tests:** quitar copy-preview y duplicados; agregar `test_publish_batch_requires_files_and_taxonomy`
y `test_publish_batch_json_has_files_and_slugs`. Mantener permiso staff, `subject_options`, inline-create.

---

## Decisiones cerradas (🧑 + 🏛️)  ·  ⚠️ histórico (versión compleja, ver REVISIÓN arriba)
1. **Híbrida**: el video NUNCA sube al servidor. La web solo arma la orden de trabajo (JSON).
2. **MVP por etapas**: esta tarjeta es Fase 1 (sin IA server-side, sin cola, sin subir archivo).
3. **`copy` (título/descripción/contenido) es la fuente de verdad**; el agente lo respeta en Fase 2.
4. **Sin tokens/secretos en el JSON.** **Sin rutas absolutas** (solo nombres de archivo en `files`).

## 🔴 Hechos verificados contra el código (vinculantes)
- **URL real del webhook = `/api/recursos/crear-video/`** (prod `https://www.profeonline.cl/api/recursos/crear-video/`).
  `apps.content.urls` se monta en `""` ([config/urls.py:46](config/urls.py)) y la ruta es
  `path("api/recursos/crear-video/", …)` ([resource_urls.py:26](apps/content/urls/resource_urls.py)).
  El doc `docs/_archivo/2026-05-30-documentos-antiguos/codex-webhook-integration.md` dice
  `/recursos/api/...` (**desactualizado**) → **corregirlo** en esta tarjeta.
- **El webhook NO recibe `area_slug` ni `module_slug`** ([api_video.py:82-90](apps/content/views/api_video.py)):
  solo `subject_slug`, `topic_slug`, `level_slugs` (+ title/video_url/description/content/is_published).
  `area_slug`/`module_slug` viajan en el job **solo para UI/organización**.
- **`Level` es M2M**, no hijo de la cadena Área→Asignatura→Tema
  ([resource.py:54](apps/content/models/resource.py)) → selector **múltiple**.
- **CRUD existentes** = `CreateView` + ModelForm con redirect ([subject_create.py](apps/content/views/subject_create.py),
  topic_create, level_create, module_create). Slugs **auto** en `Model.save()` (verificado en
  [area.py:20-32](apps/content/models/area.py); mismo patrón en Subject/Topic/Resource).

## 🟢 Refinamientos del preflight (🧩 Codex, 2026-06-04) — VINCULANTES
Sin objeciones bloqueantes. **JSON server-side confirmado** (POST → `Content-Disposition: attachment`).
Tres precisiones que el builder DEBE respetar:
1. **`SubjectForm` no incluye `area`** ([content_forms.py](apps/content/forms/content_forms.py)): el
   endpoint inline de **asignatura** debe recibir `area_id` y **setear `subject.area`** desde el área
   seleccionada antes de `save()` (o usar un form inline propio con `area`).
2. **`ModuleForm` no incluye `topic` ni `levels`** y `Module.subject` es **obligatorio**
   ([module.py](apps/content/models/module.py)): el endpoint inline de **módulo** debe setear `subject`
   (obligatorio) y, si aplica, `topic`/`levels` desde el contexto elegido tras validar el form.
   `module_slug` sigue siendo **solo organizativo** (no va al webhook) → el módulo es **opcional** en
   Fase 1; si complica, puede diferirse sin bloquear el resto.
3. **NO cambiar la firma de `build_resource_copy(video, subject, topic)`** (reemplaza la "firma
   sugerida" de la sección *Servicio* de más abajo): moverla al servicio **manteniendo la firma** y
   reimportándola en `import_youtube_resources.py` (wrapper compatible). Para la vista previa sin URL,
   construir `video = {"title": <titulo>, "video_url": ""}` y que la función **tolere `video_url` vacío**
   (omite la sección `### Video`). Igual criterio para `clean_video_title`.

## 🟠 Revisión del plan del builder (🏛️ Claude, 2026-06-04) — atender antes/durante construcción
El plan de implementación de 🔨 Antigravity quedó **aprobado con ajustes**. Incorporar:

**🔴 Corregir sí o sí (errores reales):**
1. **`Module` usa `title`, no `name`** ([module.py:6](apps/content/models/module.py)): el endpoint inline
   devuelve `{ok, id, name, slug}` uniforme → reventará para módulo. Resolver con
   `label = getattr(obj, "name", None) or getattr(obj, "title", None)` (o devolver `title`).
2. **CSRF en los POST AJAX**: `publish_inline_create` y el POST de `publish_studio` **no** son
   `csrf_exempt` (a diferencia del webhook). El template necesita `{% csrf_token %}` y
   `publish_studio.js` debe enviar el header `X-CSRFToken`, o darán **403**.
3. **Ubicación del contrato `upload-job/v1`**: `codex-webhook-integration.md` vive en
   `docs/_archivo/…` (carpeta **histórica**). Corregir la URL ahí (donde está el error), pero
   **documentar el contrato canónico en un lugar vigente** (doc nuevo en `docs/` o
   `docs/gobernanza/inventario-operacional.md`). No enterrar la fuente de verdad en `_archivo`.

**🟡 Conviene afinar:**
4. **Validación server-side, no solo JS**: el POST debe **rechazar** un job incompleto (sin
   asignatura/tema/nivel, o playlist sin `skip_playlist`) también en el servidor. Agregar test
   `test_publish_post_rejects_incomplete_job`.
5. **Mapeo IDs→slugs en el POST**: dejar explícito que convierte `area_id`/`subject_id`/`topic_id`/
   `level_ids` a `area_slug`/`subject_slug`/`topic_slug`/`level_slugs` (justifica el server-side).
6. **`user_passes_test(is_admin)` redirige (302) a login** para usuario normal (no 403); ajustar la
   expectativa del test (acepta 302).
7. **CSS y CSP**: estilos en CSS **externo** (`estilos.css`) con cache-buster `?v=N`; **nada** de
   `style=""`/`onclick=""` inline en los modales (rompe la CSP con nonce).

**🟢 Menores:**
8. **Enlace de navegación**: ubicar el archivo real del nav de staff (el plan usa placeholders) y
   seguir el patrón de los CRUD existentes.
9. **Consistencia de permisos**: `subject_options` queda `is_admin` pero reusa `topic_options`, hoy
   **público**. No es fuga (los temas son públicos); anotarlo por si se homogeneíza.

## Objetivo (una frase)
Página interna (**solo staff**) que arma la orden de trabajo (`profeonline.upload-job/v1`) con
selectores dependientes, creación inline de taxonomía, vista previa de copy, detección de
duplicados y aviso de incompleto, y la **descarga como `.json`** — para que publicar sea rápido y
con red de seguridad. El JSON lo consume luego el script local de Codex (igual que hoy, pero sin prosa).

## Fuentes a leer (rutas concretas)
- Webhook + contrato actual: `apps/content/views/api_video.py`.
- Selector dependiente de referencia: `apps/content/views/topic_options.py` (ruta `temas/opciones/`, `name="content:topic_options"`).
- Copy a extraer a servicio: `apps/content/management/commands/import_youtube_resources.py`
  (`clean_video_title` líneas 117-125, `build_resource_copy` líneas 128-156).
- CRUD/forms a reutilizar inline: `SubjectForm`, `TopicForm`, `LevelForm`, `ModuleForm` (y `AreaForm` si existe;
  `apps/content/forms/`); vistas `*_create.py`.
- Protección staff: `is_admin` ([permissions.py](apps/content/views/permissions.py)) y `AdminRequiredMixin` ([mixins.py](apps/content/views/mixins.py)).
- Validación YouTube (para extraer `playlist_id` de un link): `get_youtube_id` y patrones de URL en `resource_detail` / `import_youtube_resources.extract_playlist_id`.
- Rutas: `apps/content/urls/__init__.py` (`app_name="content"`).

## Contrato del job (Fase 0 — documentar, sin código de runtime)
Documentar el esquema en `codex-webhook-integration.md` (junto con la corrección de URL):

```json
{
  "schema": "profeonline.upload-job/v1",
  "file": { "file_name": "fisica-sonido.mp4" },
  "youtube": { "privacy": "public", "playlist_id": "PLxxxx", "playlist_title": "Física", "skip_playlist": false },
  "taxonomy": { "area_slug": "fisica", "subject_slug": "fisica-escolar", "topic_slug": "sonido",
                "module_slug": null, "level_slugs": ["mediapreuniversitario"] },
  "thumbnail": { "class_label": "", "main_text": "Sonido y efecto Doppler",
                 "palette": "azul-profeonline", "ai_panel_instructions": "…" },
  "copy": { "title": "…", "description": "…", "content_md": "…" },
  "ai_instructions": "Tono educativo, SEO de clases particulares.",
  "publish": { "is_published": true }
}
```
- `privacy` ∈ {`public`,`unlisted`,`private`}. `class_label` = **string opcional** (admite "Clase 2.45", "1.12", "").
- Playlist: `playlist_id` **obligatorio** salvo `skip_playlist: true`.

## Propuesta — arquitectura (Fase 1)

### Servicio reutilizable (`apps/content/services/resource_copy.py`)
- **Mover** `clean_video_title` y `build_resource_copy` aquí; **reimportarlas** desde
  `import_youtube_resources.py` (no cambiar comportamiento del comando → sus tests siguen verdes).
- **Adaptar** `build_resource_copy` para que `video_url` sea **opcional**: si viene vacío, omitir
  la sección `### Video` (en Fase 1 aún no hay URL de YouTube). Firma sugerida:
  `build_resource_copy(clean_title, subject, topic, video_url="")`.

### Vista principal (`apps/content/views/publish_studio.py`, protegida `is_admin`)
- `publish_studio(request)` (GET) → renderiza `templates/pages/publish_studio.html` con: áreas
  activas, niveles activos, paletas disponibles (constante simple), opciones de privacidad.
- **No** persiste nada (Fase 1 solo descarga). El armado final del JSON puede ser client-side (JS)
  o server-side (POST que devuelve el `.json` con `Content-Disposition: attachment`). **Preferir
  server-side** para validar y normalizar slugs/`playlist_id` en un solo lugar.

### Endpoints AJAX (todos `is_admin`)
- `subject_options(request)` (nuevo, `apps/content/views/subject_options.py`): `?area_id=` → asignaturas activas del área (patrón calcado de `topic_options`).
- Reusar **`topic_options`** existente para Asignatura→Tema.
- `publish_copy_preview(request)`: recibe `title`, `subject_id`, `topic_id` → devuelve
  `{title, description, content_md}` usando el servicio. Editable en el form (fuente de verdad).
- `publish_duplicates(request)`: recibe `title`, `topic_id` → busca en `Resource` del **mismo tema**
  por `slug == slugify(title)` o `title__iexact`/`title__icontains`; devuelve `[{title, url}]`.

### Creación inline (endpoints JSON que reutilizan los ModelForm existentes)
- Un endpoint POST por entidad (`apps/content/views/publish_inline_create.py`), `is_admin`,
  que instancia el ModelForm correspondiente (`AreaForm`/`SubjectForm`/`TopicForm`/`LevelForm`/`ModuleForm`),
  y si es válido guarda y responde `{ok, id, name, slug}` (el slug lo genera el `save()` del modelo).
  Si hay errores, `{ok:false, errors}` con 400. El front abre un modal, postea, y **refresca el
  selector** correspondiente sin recargar la página.
- Reutiliza la validación existente; **no** duplicar lógica de slug.

### Template (`templates/pages/publish_studio.html`)
- Formulario con: **archivo** (`<input type=file>` solo para capturar `file_name`; el archivo **no**
  se sube); **Área→Asignatura→Tema** (selects
  dependientes vía AJAX) + **Módulo** opcional; **Niveles** (checkbox múltiple); **privacidad**;
  **playlist** (campo link/ID + casilla "subir sin playlist") ; **paleta** + **texto miniatura** +
  **class_label** + **ai_panel_instructions**; **copy** (título/descripción/`content_md` editable con
  botón "Generar"); **`ai_instructions`** (textarea). Botón **"Descargar orden de trabajo (.json)"**.
- **JS externo** (`static/js/publish_studio.js`, **no inline**, CSP usa nonce): selects dependientes,
  llamada a preview/duplicados, extracción de `playlist_id` desde un link de YouTube, validación de
  incompleto (bloquea descarga si falta asignatura/tema/nivel/privacidad o playlist sin `skip_playlist`).
- **Extracción `playlist_id`**: de `…list=PLxxxx` tomar el parámetro `list`; si el usuario pega solo el ID, usarlo tal cual.

### Rutas (`apps/content/urls/`, namespace `content`)
- `publicar/estudio/` → `name="publish_studio"`
- `publicar/opciones/asignaturas/` → `name="subject_options"`
- `publicar/copy/preview/` → `name="publish_copy_preview"`
- `publicar/duplicados/` → `name="publish_duplicates"`
- `publicar/crear/<entidad>/` → `name="publish_inline_create"` (entidad ∈ area/asignatura/tema/nivel/modulo)
- Enlace en navegación staff (donde están los CRUD actuales).

## No-objetivos (FUERA de esta tarjeta)
- ❌ Subir el archivo de video al servidor / Railway. ❌ Cola `VideoUploadJob` y endpoints del agente (Fase 2).
- ❌ Sync real de playlists / OAuth de YouTube (Fase 2). ❌ Reseña de IA (server-side o agente) (Fase 2/3).
- ❌ Generar miniatura/descripción definitivas (las hace el script local). ❌ Enviar `area_slug`/`module_slug` al webhook.
- ❌ Tokens en el JSON. ❌ Tocar `script-src` de la CSP (JS externo entra por `'self'`).

## Criterios de aceptación (verificables)
- [ ] `GET /publicar/estudio/` → 200 para superusuario; usuario normal → 302/403.
- [ ] `subject_options` devuelve solo asignaturas activas del área; `topic_options` (reusado) filtra por asignatura.
- [ ] Crear inline (área/asignatura/tema/nivel/módulo) responde `{ok, id, name, slug}` y el selector se refresca.
- [ ] `publish_copy_preview` devuelve `{title, description, content_md}` sin requerir `video_url`.
- [ ] `publish_duplicates` advierte ante un título/slug repetido en el mismo tema.
- [ ] El `.json` descargado valida el contrato: incluye `area_slug`, `subject_slug`, `topic_slug`,
      `level_slugs`, `playlist_id` **o** `skip_playlist:true`, `class_label`; **NO** contiene tokens.
- [ ] La descarga se **bloquea** si falta asignatura, tema, nivel, privacidad, o playlist sin `skip_playlist`.
- [ ] Doc `codex-webhook-integration.md` corregido con `/api/recursos/crear-video/`.
- [ ] Comando `import_youtube_resources` intacto (tests existentes verdes tras mover el servicio).
- [ ] CSP intacta (JS externo, sin inline). Si toca CSS → cache-buster `?v=N`.
- [ ] Barrera verde: `test` · `check --deploy` · `makemigrations --check --dry-run`.

## Plan de pruebas
- **Automáticas** (`apps/content/tests/`):
  - `test_publish_studio_requires_staff` (200 superuser / 302-403 anónimo y normal).
  - `test_subject_options_filters_by_area`, reusar/extender test de `topic_options`.
  - `test_copy_preview_omits_video_section_without_url`, `test_resource_copy_service_importable_from_command`.
  - `test_publish_duplicates_flags_same_topic_title`.
  - `test_inline_create_subject_returns_json_and_slug` (+ caso inválido 400).
  - Servicio: `build_resource_copy` con y sin `video_url`.
- **QA manual:** `runserver` (`config.settings.local`) como superusuario → selects dependientes,
  crear inline refresca, duplicado advierte, incompleto bloquea, abrir el `.json` descargado y
  validar campos. Previsualizar con **URL local** (economía de tokens, no capturas).

## Riesgos / rollback
- **Mover `clean_video_title`/`build_resource_copy`** podría romper el comando → mitigado
  reimportándolas desde el servicio (los tests de `import_youtube_resources` deben seguir verdes).
- **Límite del navegador** (sin ruta absoluta) → solo `file_name`; el archivo lo resuelve el agente (Fase 2).
- **Duplicados imperfectos en Fase 1** (sin estado de archivos) → solo título/slug en el tema; el
  dedupe por archivo y por ID de YouTube llega en Fase 2 + el webhook (red de seguridad final).
- **Rollback**: Fase 1 es **aditiva** (vistas/rutas/JS/servicio nuevos; sin migraciones). Revertir =
  quitar rutas/vistas/JS nuevos y restaurar las dos funciones en el comando.

## Preflight para 🧩 Codex
- Confirmar nombres reales de los ModelForms (`AreaForm`/`SubjectForm`/`TopicForm`/`LevelForm`/`ModuleForm`)
  y que `Subject`/`Topic`/`Level` autogeneran slug en `save()` como `Area`.
- Confirmar la firma actual de `build_resource_copy` (usa `video["title"]`, `video["video_url"]`,
  `subject.name`, `topic.name`) y que hacerla `video_url` opcional no rompe el comando.
- Verificar el namespace/inclusión de URLs y que `topic_options` es reutilizable tal cual.
- Confirmar que la CSP (`apps/core/middleware.py`) permite `static/js/publish_studio.js` por `'self'`.
- Señalar si conviene armar el JSON server-side (POST→attachment) vs client-side (recomendado server-side).

## Construcción para 🔨 Antigravity
Rama `feat/estudio-publicacion-fase1`. Diff acotado: servicio `resource_copy.py` (+ reimport en el
comando), vistas/endpoints (`publish_studio`, `subject_options`, `publish_copy_preview`,
`publish_duplicates`, `publish_inline_create`), rutas, `templates/pages/publish_studio.html`,
`static/js/publish_studio.js` (externo), corrección del doc de webhook, tests, barrera verde.
**Sin migraciones.** Completar "Qué se hizo".

## Iteración posterior — Fase 2 (tarjeta separada)
Cola `VideoUploadJob` + endpoints `/api/upload-jobs/siguiente/`, `/api/upload-jobs/<id>/resultado/`,
`/api/upload-agent/heartbeat/`; sync de playlists (OAuth en el agente) + "+ Crear playlist";
selector real de archivos; **preflight** antes de subir a YouTube; **reintento idempotente**
(guarda `video_id`); reseña de IA por el agente Codex; estado en vivo en la web.

---

## Qué se hizo

Se implementó el Estudio de Publicación (Versión Simplificada - Batch) en la rama `feat/estudio-publicacion-fase1` resolviendo todos los criterios solicitados y las precisiones de la revisión:

1. **Esquema de Lote `profeonline.upload-batch/v1`:**
   - Se removió por completo el esquema complejo individual y se implementó la orden de lote para múltiples videos.
   - El contrato canónico se documentó en `docs/gobernanza/inventario-operacional.md`.
   - Se agregaron las claves `schema`, `files` (lista de nombres), `taxonomy` (slugs mapeados), `youtube` (`playlist_id`, `playlist_title`, `create_playlist` y `new_playlist`), e `instructions` en el JSON descargable.

2. **Limpieza de Vistas Obsoletas:**
   - Se eliminaron las vistas `publish_copy_preview.py` y `publish_duplicates.py`.
   - Se removieron sus exportaciones en `apps/content/views/__init__.py` y sus rutas asociadas en `apps/content/urls/publish_urls.py`.

3. **Vista de Lote y Validaciones en `publish_studio.py`:**
   - El método `POST` implementa un parseo defensivo robusto para `file_names` con try-except atrapando `json.JSONDecodeError`, `TypeError` y `ValueError` retornando un `HttpResponse` de estado 400 en caso de malformación o de no ser una lista de strings.
   - La orden descargable omite la carpeta vigilada; el agente local resuelve la carpeta base por su propia configuración.
   - Se valida la pertenencia taxonómica (Área activa &rarr; Asignatura activa &rarr; Tema activo) y el estado publicado del módulo opcional.
   - La playlist se valida y normaliza de forma opcional (si viene vacía se asume sin playlist y no genera error).

4. **UI/UX y Scripts con CSP:**
   - `templates/pages/publish_studio.html`: Se actualizó para tener un `<input type="file" multiple>` que lee solo los nombres de los archivos. No envía el archivo al servidor (sin atributo `name`), poblando el campo oculto JSON.
   - `static/js/publish_studio.js`: Maneja de forma XSS-safe (DOM API con `createElement` y `textContent`) la previsualización de archivos y el renderizado de la caja de warnings dinámicos sin recurrir a `innerHTML` con interpolación de variables.
   - La playlist vacía se trata como "sin playlist" directamente sin checkboxes innecesarios como `skip_playlist`.

5. **Pruebas y Verificaciones:**
   - Rediseñado `apps/content/tests/test_publish_studio.py` sumando cobertura para el JSON batch (`profeonline.upload-batch/v1`), exclusión de archivos/taxonomía, inconsistencias taxonómicas, entidades inactivas, parseo defensivo y creación de playlist nueva.
   - Todos los tests pasaron exitosamente (14 en la suite local del estudio, 232/232 en total).
   - Verificados checks estáticos: `makemigrations --check --dry-run` (sin cambios), `check --deploy` (OK) y `node --check static/js/publish_studio.js` (OK).
