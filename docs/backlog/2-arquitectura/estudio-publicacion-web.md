# Estudio de publicación: página web asistida para preparar subidas de video

- **Estado:** Handoff Ready (arquitectura) — **Fase 0 + Fase 1**
- **Creado:** 2026-06-04 · **Handoff:** 2026-06-04 (🏛️ Claude)
- **Prioridad:** P2 · **Cartera:** ingeniería
- **Tipo:** producto · infraestructura
- **Dueño sugerido:** 🧩 Codex (preflight) → 🔨 Antigravity (construcción `feat/estudio-publicacion-fase1`) → 🏛️ Claude (cierre)

> **Origen:** planificación 🧑 Octavio + 🤖 Claude, refinada por **🧩 Codex** (8 acotaciones, todas
> integradas) y verificada contra el código real. Alcance de **ESTA** tarjeta: el contrato del job
> (Fase 0) + la **página web que genera el JSON** (Fase 1). **Fase 2** (cola + agente + playlists +
> preflight server-side + reseña IA) va en una tarjeta separada para mantener el diff acotado.

## Decisiones cerradas (🧑 + 🏛️)
1. **Híbrida**: el video NUNCA sube al servidor. La web solo arma la orden de trabajo (JSON).
2. **MVP por etapas**: esta tarjeta es Fase 1 (sin IA server-side, sin cola, sin subir archivo).
3. **`copy` (título/descripción/contenido) es la fuente de verdad**; el agente lo respeta en Fase 2.
4. **Sin tokens/secretos en el JSON.** **Sin rutas absolutas** (solo `watch_folder` + `file_name`).

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
  "file": { "watch_folder": "default", "file_name": "fisica-sonido.mp4" },
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
  se sube) + `watch_folder` (select; en Fase 1 solo `"default"`); **Área→Asignatura→Tema** (selects
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
- **Límite del navegador** (sin ruta absoluta) → `watch_folder` + `file_name`; el archivo lo resuelve el agente (Fase 2).
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
_(Completar al finalizar, antes de mover a `backlog/6-finalizados/`.)_
