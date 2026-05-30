# 🔌 Guía de Integración: Publicación Automática de Videos (Codex)

Esta especificación técnica detalla cómo configurar la automatización en **Codex** para que, al momento de procesar o subir un video en YouTube, realice una llamada al webhook de **ProfeOnline** y cree de manera inmediata la página del recurso educativo asociada al video.

---

## 🎯 Especificación del EndPoint

*   **URL del Webhook (Desarrollo):** `http://127.0.0.1:8000/recursos/api/recursos/crear-video/`
*   **URL del Webhook (Producción):** `https://[tudominio]/recursos/api/recursos/crear-video/`
*   **Método HTTP:** `POST`
*   **Content-Type:** `application/json`

---

## 🛡️ Autenticación

Para que la petición sea aceptada, Codex debe enviar el token de seguridad configurado en el servidor (`API_SECRET_TOKEN`) en las cabeceras HTTP.

### Cabecera HTTP Requerida
```http
X-Api-Token: [TU_TOKEN_SECRETO]
```

*Opcionalmente, se puede enviar en el formato estándar Bearer:*
```http
Authorization: Bearer [TU_TOKEN_SECRETO]
```

---

## 📥 Formato de Datos de Entrada (Request Body)

Codex debe enviar un objeto JSON con los siguientes campos:

| Campo | Tipo | Requerido | Descripción | Ejemplo |
| :--- | :--- | :---: | :--- | :--- |
| `title` | String | **Sí** | Título original del video en YouTube (para el recurso). | `"Cálculo II: Clase 2: Integrales Trigonométricas"` |
| `video_url` | String | **Sí** | Enlace válido del video de YouTube (formato estándar o corto). | `"https://www.youtube.com/watch?v=E2WA5KSbj6A"` |
| `description` | String | No | Breve descripción SEO del recurso (debe estar limpia de prefijos/códigos). | `"Aprende el método definitivo para resolver integrales trigonométricas."` |
| `content` | String | No | Apuntes o cuerpo de la clase en formato **Markdown** (se mostrará abajo del reproductor). | `"### Sobre esta clase\nEn esta sesión..."` |
| `subject_slug` | String | No | Slug de la asignatura para asociarlo automáticamente. | `"calculo-ii"` |
| `level_slugs` | Array | No | Slugs de los niveles educativos permitidos. | `["preuniversitario"]` |
| `is_published` | Boolean | No | `true` para hacerlo visible de inmediato, `false` para guardarlo como borrador. | `true` |

### Ejemplo de Payload (JSON)
```json
{
  "title": "Cálculo II: Clase 2: Integrales Trigonométricas - Teoría y Ejercicios Resueltos",
  "video_url": "https://www.youtube.com/watch?v=E2WA5KSbj6A",
  "description": "Aprende el método definitivo para resolver integrales trigonométricas mediante sustitución y cambio de variables.",
  "content": "### 🎥 Sobre esta clase\nEn esta sesión abordamos el estudio de **Integrales Trigonométricas** dentro del tema de **Integrales y técnicas de integración** en la asignatura de **Cálculo II**.\n\n### 🎯 ¿Qué aprenderás en este recurso?\n- **Análisis detallado:** Cómo identificar el tipo de integral y seleccionar la identidad trigonométrica correcta.\n- **Método de resolución:** Procedimientos paso a paso para reducir y simplificar expresiones complejas.\n- **Tips académicos:** Fórmulas clave y errores algebraicos comunes en exámenes.",
  "subject_slug": "calculo-ii",
  "level_slugs": ["preuniversitario"],
  "is_published": true
}
```

---

## 📤 Formato de Respuesta (Response Body)

El webhook procesará el video y devolverá el enlace directo de la página web que acaba de activar:

### Respuesta Exitosa (`201 Created` / `200 OK`)
```json
{
  "ok": true,
  "created": true,
  "resource_id": 186,
  "slug": "calculo-ii-clase-2-integrales-trigonometricas-teoria-y-ejercicios-resueltos",
  "url": "http://127.0.0.1:8000/recursos/calculo-ii-clase-2-integrales-trigonometricas-teoria-y-ejercicios-resueltos/"
}
```

---

## 📝 Script de Prueba (Python)

Puedes entregar este script a Codex para validar la conexión y creación automática desde su entorno de ejecución:

```python
import requests

webhook_url = "http://127.0.0.1:8000/recursos/api/recursos/crear-video/"
headers = {
    "Content-Type": "application/json",
    "X-Api-Token": "tu_token_secreto_aqui"
}

payload = {
    "title": "Física I: Clase 1: Análisis Gráfico del Movimiento",
    "video_url": "https://www.youtube.com/watch?v=hmJwOiZA530",
    "description": "Estudio cinemático detallado para comprender gráficos de posición y velocidad en función del tiempo.",
    "content": "### 🎥 Sobre esta clase\nClase de cinemática lineal enfocada en interpretación de gráficos.",
    "subject_slug": "fisica-i",
    "level_slugs": ["secundaria", "preuniversitario"],
    "is_published": True
}

response = requests.post(webhook_url, json=payload, headers=headers)
print(response.json())
```

---

## Importacion directa de playlists de YouTube

Para crear paginas agrupadas por area, asignatura y tema desde una playlist, usa el comando de management:

```bash
python manage.py import_youtube_resources \
  --playlist-url "https://www.youtube.com/playlist?list=PLAYLIST_ID" \
  --area "Matematica" \
  --subject "Matematica Escolar" \
  --topic "Numeros Enteros"
```

Requisitos:

- Configurar `YOUTUBE_API_KEY` en Railway o pasar `--youtube-api-key`.
- El comando crea el area, la asignatura y el tema si no existen.
- Cada entidad queda con slug y pagina publica:
  - `/areas/<slug>/`
  - `/asignaturas/<slug>/`
  - `/temas/<slug>/`
  - `/recursos/<slug>/`

Opciones utiles:

```bash
python manage.py import_youtube_resources \
  --playlist-id "PLAYLIST_ID" \
  --area "Matematica" \
  --subject "Matematica Escolar" \
  --topic "Numeros Enteros" \
  --level "Escolar" \
  --limit 10
```

Para importar videos sueltos:

```bash
python manage.py import_youtube_resources \
  --video-url "https://www.youtube.com/watch?v=VIDEO_ID" \
  --area "Fisica" \
  --subject "Fisica I" \
  --topic "Cinematica"
```
