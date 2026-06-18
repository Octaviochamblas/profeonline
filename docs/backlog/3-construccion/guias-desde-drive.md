# Guías desde Google Drive (elegir archivos de una carpeta como biblioteca)

- **Estado:** En construcción (fast-track 🧑 → 🏛️ Claude, 2026-06-16)
- **Creado:** 2026-06-16 · **Autor:** 🏛️ Claude (sesión con 🧑 Octavio)
- **Prioridad:** P2 · **Cartera:** educativa / producto
- **Tipo:** producto · infraestructura
- **Dueño:** 🏛️ Claude (construcción directa este sesión, por pedido del 🧑) → 🧩 Codex (auditoría).
  🧑 Usuario: infra de Google (service account + compartir carpeta).

> Fast-track: el 🧑 pidió redactar y construir en la misma sesión. Idea → construcción directa.

## Origen / contexto
Sale de la sesión 2026-06-16. Hoy las guías de referencia (`QuizGuide`, modo documento del banco
de preguntas) solo se cargan **subiendo un archivo** o **pegando texto** en `/publicar/guias/`.
Octavio quiere **elegir archivos desde una carpeta de Google Drive** (su "biblioteca"): dejar los
documentos en una carpeta de Drive y que el panel los liste para importarlos como guías.

## Objetivo (una frase)
Permitir al admin **listar e importar documentos desde una carpeta de Google Drive** (solo lectura)
para crearlos como `QuizGuide`, sin tener que descargar y resubir cada archivo a mano.

## Decisiones cerradas (🧑 + 🏛️, 2026-06-16)
1. **Enfoque "carpeta = biblioteca"** con **service account** (no OAuth por usuario, no Google Picker):
   más simple para un panel solo-admin y **no toca la CSP** (todo del lado del servidor).
2. **Carpeta configurable desde el panel**: se pega la **URL/ID de la carpeta** en el formulario;
   default tomado del setting `GUIDES_DRIVE_FOLDER_ID`. Sin modelo nuevo ni migración en v1.
3. **Secreto único:** `GOOGLE_SERVICE_ACCOUNT_JSON` (el JSON del service account) en variables de
   entorno. El ID de carpeta no es secreto.
4. **Tipos soportados:** Google Docs nativos (`export` a texto), PDF (pypdf) y .txt/.md (descarga).
   Word `.docx` queda como hoy (degradado si `python-docx` no está instalado — limitación previa).
5. **Carpeta plana** (sin recursión a subcarpetas) en v1.
6. **Dependencia liviana:** se usa `google-auth` + `requests` (REST de Drive directo); NO el cliente
   completo `google-api-python-client`. Import perezoso (degrada con elegancia si falta el paquete),
   igual que `pypdf`/`python-docx` en `guide_service`.

## Prerrequisitos del 🧑 (infra Google — fuera del código)
1. Crear un **service account** en Google Cloud y habilitar la **Drive API**.
2. Descargar su **clave JSON** y cargarla en Railway como `GOOGLE_SERVICE_ACCOUNT_JSON`
   (el contenido del JSON, en una sola variable).
3. **Compartir la carpeta** de Drive con el email del service account (rol *Lector*).
4. (Opcional) Cargar `GUIDES_DRIVE_FOLDER_ID` con el ID de la carpeta por defecto.

## Fuentes a leer (rutas concretas)
- `apps/content/views/quiz_guides.py` — vista actual de guías (subir/pegar). Se extiende.
- `apps/content/services/guide_service.py` — `extract_guide_text` / `normalize_text` (se reutilizan).
- `apps/content/models/quiz_guide.py` — modelo `QuizGuide` (no cambia).
- `templates/pages/quiz_guides.html` — UI de guías (se agrega sección "Desde Drive").
- `apps/content/urls/publish_urls.py` — rutas del estudio.
- `config/settings/base.py` — patrón `os.environ.get` (ver `GEMINI_API_KEY`).

## Propuesta (arquitectura)
- **`apps/content/services/drive_service.py`** (nuevo):
  - `is_configured()` → hay `GOOGLE_SERVICE_ACCOUNT_JSON`.
  - `parse_folder_id(url_or_id)` → extrae el ID de un link de carpeta de Drive o lo devuelve tal cual.
  - `list_folder_files(folder_id)` → `[{id, name, mime}]` de la carpeta (filtra a tipos soportados).
  - `fetch_file(file_id)` → `{name, mime, text}` (export si es Google Doc; download + extractor si no).
  - REST de Drive vía `AuthorizedSession` de `google-auth`, scope `drive.readonly`. Import perezoso.
- **Vista** `quiz_guides`: si llega `?drive_folder=…` (GET), lista los archivos y los muestra como
  checklist. Nuevo POST `import_drive_guides`: importa los seleccionados (cada uno → `QuizGuide`),
  con los mismos vínculos (asignatura/tema/recurso) que el alta manual.
- **URL** nueva: `publicar/guias/importar-drive/`.
- **Template**: sección "Desde Drive" (input de carpeta + listar + checklist + importar). Sin JS
  inline (server-rendered). Si Drive no está configurado, muestra una nota en vez del formulario.

## No-objetivos (FUERA)
- ❌ Google Picker / OAuth por usuario. ❌ Subcarpetas recursivas. ❌ Sincronización automática
  (se importa a demanda). ❌ Editar el contenido importado (se usa el extractor actual).
  ❌ Storage de los binarios (solo se guarda el texto en `QuizGuide.content_text`, como hoy).

## Criterios de aceptación (verificables)
- [ ] Barrera verde: `test` · `check --deploy` · `makemigrations --check --dry-run` (sin migraciones).
- [ ] `import_drive_guides` y el listado rechazan a no-superuser (302/403).
- [ ] `parse_folder_id` extrae el ID de un link `…/folders/<id>` y de un ID pelado.
- [ ] Con Drive mockeado: listar muestra los archivos; importar crea `QuizGuide` con el texto y los
      vínculos elegidos.
- [ ] Drive no configurado → la página muestra la nota y no rompe (no se llama a la API).
- [ ] Si toca CSS → cache-buster `?v=N` subido.

## Plan de pruebas
- **Unit/Vistas** (`apps/content/tests/test_drive_guides.py`): `parse_folder_id`; permisos;
  listado con servicio mockeado; importación crea guías + vínculos; estado "no configurado".
- **QA manual (🧑):** tras cargar el service account y compartir la carpeta, listar e importar un
  documento real y verificar que el modo documento lo usa al generar.

## Riesgos / rollback
- **Credenciales mal cargadas** → la página degrada con un mensaje claro; no rompe el resto del panel.
- **Dependencia `google-auth`** → import perezoso; si falta, mensaje "instalá google-auth", el resto
  de las guías (subir/pegar) sigue funcionando.
- **Cuotas de Drive API** → uso bajo (listar/descargar a demanda); free tier sobra. Rollback = quitar
  la sección del template + la ruta (no hay migración que revertir).

---

## Qué se hizo (build 2026-06-16, 🏛️ Claude — pendiente infra del 🧑 + auditoría)

- **`apps/content/services/drive_service.py` (nuevo):** `is_configured()`, `parse_folder_id()`
  (link `…/folders/<id>`, `?id=<id>` o ID pelado), `list_folder_files()` y `fetch_file()` (export de
  Google Docs / download + extractor para PDF/txt). REST de Drive v3 con `AuthorizedSession` de
  `google-auth`, scope `drive.readonly`, import perezoso y errores 403/404 traducidos a mensajes claros.
- **`config/settings/base.py`:** `GOOGLE_SERVICE_ACCOUNT_JSON` y `GUIDES_DRIVE_FOLDER_ID` (vía `os.environ`).
- **`requirements.txt`:** + `google-auth==2.38.0`.
- **`apps/content/views/quiz_guides.py`:** helper `_set_guide_links` (DRY entre alta manual e import);
  `_drive_context` lista la carpeta solo si el admin pulsa "Listar" y Drive está configurado (degrada
  con mensaje si no); nueva vista `import_drive_guides` (POST, solo-admin) que importa los archivos
  elegidos como `QuizGuide` con sus vínculos.
- **`apps/content/urls/publish_urls.py`:** ruta `publicar/guias/importar-drive/`.
- **`templates/pages/quiz_guides.html`:** sección "📂 Desde Google Drive" (input carpeta → listar →
  checklist + vínculos → importar). Sin JS inline; sin tocar la CSP.
- **`templates/base.html`:** link "Guías de referencia" en el navbar staff (antes la página solo se
  alcanzaba por URL).
- **Tests** `apps/content/tests/test_drive_guides.py` (13): parseo de IDs, permisos, listado (mock),
  importación + vínculos, "no configurado" no llama a la API, errores mostrados con gracia. Verde,
  junto a los 16 tests de guías preexistentes. `check` y `makemigrations --check` OK (sin migraciones).

### Validación end-to-end (2026-06-16, carpeta real "Material Académico")
Con el service account `profeonline-guias@…` y la carpeta compartida, se validó contra Drive real
(credencial leída de archivo local, nunca commiteada). Hallazgos y ajustes:

- **La biblioteca está anidada** (Material Académico → Libros / Matemáticas / … → subcarpetas →
  documentos). El listado plano del v1 daba 0. **Ajuste:** `list_folder()` ahora devuelve también
  las **subcarpetas** y la UI permite **navegar (drill-down)** con `?drive_folder=<id>` (volver = atrás
  del navegador). Auto-lista la carpeta por defecto al entrar.
- **Tus PDFs propios extraen bien** ("1 Números.pdf" 3577 chars, "Tablas…" 2347). ✅
- **`.docx` daba 0** por falta de `python-docx`. **Ajuste:** + `python-docx==1.1.2` (arregla también la
  subida manual de Word, que fallaba en silencio). Revalidado: "1 Números.docx" → 2546 chars. ✅
- **PDFs escaneados** (libros de "Libros") no extraen texto (son imágenes; pypdf no hace OCR).
  **Limitación aceptada** (OCR fuera de alcance). El import **descarta** archivos sin texto y avisa
  cuáles, sin crear guías vacías.
- Tablas dentro de `.docx` extraen poco (python-docx lee solo párrafos) — menor.

**Estado:** integración validada de punta a punta para el material real del profe. 29 tests verde
(13 Drive + 16 guías) · `check` OK · sin migraciones.

**Falta:** QA manual del 🧑 desde la UI, cargar las variables en Railway (`GOOGLE_SERVICE_ACCOUNT_JSON`
+ `GUIDES_DRIVE_FOLDER_ID`) antes de mergear a `main`, auditoría 🧩 Codex y push/PR.
