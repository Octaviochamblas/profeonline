# Auditoría C3 - Redis para rate-limit real del webhook

- **Fecha:** 2026-06-02
- **Autor/agente:** Codex
- **Alcance:** rama `feat/redis-cache-check`, system check de cache compartida, tests C3,
  documentación operacional y estado de configuración pendiente en Railway.
- **Estado:** vigente
- **Base auditada:** diff `main...HEAD` y tarjeta `docs/backlog/4-auditoria/c3-redis-rate-limit.md`.

## 1. Resumen ejecutivo

La implementación de Antigravity para C3 está técnicamente bien orientada y cumple el objetivo de
control preventivo: la app ahora avisa cuando corre con `DEBUG=False` y cache local (`LocMemCache`),
porque en ese escenario el rate-limit del webhook sigue siendo por worker y no compartido.

El warning `core.W001` no rompe `check --deploy --fail-level ERROR`, desaparece cuando existe
`REDIS_URL`, y está cubierto por tests unitarios. La parte de código es aprobable.

Lo que aún cierra el riesgo real no está en el repo: falta confirmar que el servicio web de Railway
tiene la variable `REDIS_URL` apuntando al Redis privado. Sin eso, el PR solo hace visible el riesgo;
no lo elimina en producción.

## 2. Evidencia revisada

### Archivos funcionales

- `apps/core/checks.py`
- `apps/core/apps.py`
- `apps/core/tests.py`
- `config/settings/production.py`
- `apps/content/views/api_video.py`

### Archivos de proceso/documentación

- `docs/backlog/4-auditoria/c3-redis-rate-limit.md`
- `docs/gobernanza/inventario-operacional.md`
- `docs/_coordinacion/ESTADO.md`

### Comandos ejecutados por Codex

```powershell
.venv\Scripts\python.exe manage.py test apps.core.tests.CacheBackendCheckTests --verbosity 1
.venv\Scripts\python.exe manage.py check
.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
git diff --check main...HEAD
```

Verificación con settings de producción:

```powershell
# Sin REDIS_URL
.venv\Scripts\python.exe manage.py check --deploy --fail-level ERROR --settings=config.settings.production

# Con REDIS_URL
.venv\Scripts\python.exe manage.py check --deploy --fail-level ERROR --settings=config.settings.production
```

Resultado local:

- `CacheBackendCheckTests`: 3 tests OK.
- `manage.py check`: sin issues en desarrollo.
- `makemigrations --check --dry-run`: sin cambios detectados.
- `git diff --check main...HEAD`: sin problemas.
- Producción sin `REDIS_URL`: aparece `core.W001`, exit 0.
- Producción con `REDIS_URL`: sin warning, exit 0.

## 3. Qué quedó bien implementado

### 3.1. El check detecta el riesgo correcto

`apps/core/checks.py` registra un system check que:

- No molesta en `DEBUG=True`.
- Evalúa el backend real de `caches["default"]`.
- Emite `Warning`, no `Error`, cuando `DEBUG=False` y el backend es `LocMemCache`.
- Usa un id propio: `core.W001`.

Ese comportamiento coincide con C3: el objetivo no era reescribir el rate-limit, sino evitar que
producción opere silenciosamente con cache por proceso.

### 3.2. Registro sin import circular

`apps/core/apps.py` importa `checks` en `ready()`:

```python
def ready(self):
    from . import checks  # noqa: F401
```

No observé import circular ni fallo de arranque en las verificaciones locales.

### 3.3. `REDIS_URL` sigue siendo la llave de activación

`config/settings/production.py` ya tenía la lógica esperada:

```python
REDIS_URL = os.environ.get("REDIS_URL")
if REDIS_URL:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": REDIS_URL,
        }
    }
```

Por eso el trabajo de infraestructura en Railway es suficiente para que Django use Redis sin otro
cambio de código.

### 3.4. Tests bien enfocados

`CacheBackendCheckTests` cubre:

- Warning con `DEBUG=False` + `LocMemCache`.
- Sin warning con `DEBUG=False` + `RedisCache`.
- Sin warning con `DEBUG=True` + `LocMemCache`.

Es una cobertura adecuada para el alcance C3.

## 4. Hallazgos

### P0 operacional - Falta confirmar `REDIS_URL` en Railway

El código ya avisa, pero el riesgo C3 solo se mitiga de verdad cuando el servicio web de Railway
tiene `REDIS_URL`.

Configuración esperada:

- Servicio: app Django/web, no el servicio Redis.
- Variable: `REDIS_URL`.
- Valor recomendado: referencia privada de Railway.

```text
${{ Redis.REDIS_URL }}
```

Si el servicio Redis tiene otro nombre, reemplazar `Redis` por el nombre exacto del servicio.

Riesgo si no se configura:

- El webhook sigue usando `LocMemCache`.
- El rate-limit sigue siendo por worker.
- El warning `core.W001` aparecerá en checks/logs, pero no corrige por sí solo el entorno.

Estado:

- **Pendiente de usuario en Railway.**

### P1 preventivo - El warning también aparece al iniciar tests específicos

Al correr `CacheBackendCheckTests`, Django imprime `core.W001` durante el system check inicial del
test runner. Los tests pasan, pero el warning aparece porque el runner puede ejecutar checks con
`DEBUG=False` y cache local.

Riesgo:

- Ruido en la suite completa.
- Posible confusión de agentes futuros, que podrían pensar que el warning implica fallo.

No lo considero bloqueante porque:

- `manage.py check` en desarrollo no muestra issues.
- `check --deploy --fail-level ERROR` sale con exit 0.
- El warning representa una condición real cuando `DEBUG=False`.

Recomendación futura:

- Si el ruido se vuelve molesto, mover el check a un tag/deploy check o añadir una condición de
  entorno explícita. No lo haría ahora porque el alcance C3 pidió precisamente avisar en producción
  sin cache compartida.

### P1 preventivo - C3 necesita verificación post-deploy

Después de mergear y redeployar, hay que comprobar que el warning desaparece en producción.

Evidencia deseada:

- Variable `REDIS_URL` existe en el servicio web.
- Redeploy terminado.
- Logs del servicio web sin `core.W001`.
- Sitio responde 200.
- Webhook mantiene su rate-limit usando cache compartida.

### P2 - El check solo alerta sobre `LocMemCache`

El check no avisa si alguien configura otro backend no compartido o inseguro para producción. Por
ejemplo, `DummyCache` también sería mala señal para rate-limit.

No bloquea C3 porque el riesgo real actual era el default `LocMemCache`, pero si el proyecto quiere
endurecer esta barrera, conviene una regla positiva:

- En producción, el backend de cache debe ser `RedisCache`, salvo excepción documentada.

Eso podría ser una mejora posterior si empiezan a aparecer más entornos.

## 5. Prevención de errores futuros

### Riesgo A - Crear Redis pero no conectarlo a la app web

Prevención:

- Documentar siempre que la variable se crea en el servicio Django, no en Redis.
- Usar referencia privada `${{ Redis.REDIS_URL }}` para evitar copiar secretos a mano.
- Confirmar con logs o `manage.py check --deploy` post-deploy.

### Riesgo B - Usar la URL pública de Redis

Prevención:

- En Railway, preferir `Private Network`.
- Evitar la pestaña Public salvo necesidad explícita, porque puede generar egress y exposición
  innecesaria.

### Riesgo C - Dar por cerrado C3 solo por mergear el código

Prevención:

- Mantener C3 como "mitigado parcialmente" hasta confirmar `REDIS_URL` en prod.
- Claude debe actualizar `matriz-riesgos.md` a verde solo después de esa confirmación.

### Riesgo D - Warning ignorado por costumbre

Prevención:

- Si C3 queda sin resolver por más de una sesión, crear una tarjeta de bloqueo operacional.
- Si el warning aparece en producción, tratarlo como P0 pendiente, aunque CI siga verde.

## 6. Checklist de cierre recomendado

Antes de marcar C3 como cerrado:

- [ ] PR de código C3 mergeado.
- [ ] Servicio Redis creado en Railway.
- [ ] Servicio web Django tiene `REDIS_URL=${{ Redis.REDIS_URL }}` o referencia equivalente.
- [ ] Redeploy del servicio web completado.
- [ ] Logs sin `core.W001`.
- [ ] `docs/gobernanza/matriz-riesgos.md` actualizado: C3 mitigado.
- [ ] `docs/backlog/4-auditoria/c3-redis-rate-limit.md` movida a finalizados por cierre.

## 7. Dictamen

Dictamen Codex:

- **Código funcional:** aprobado.
- **Tests del núcleo:** aprobados.
- **Diff vs. tarjeta:** fiel.
- **Cierre operacional:** pendiente de confirmar `REDIS_URL` en Railway.

Yo sí daría `audit:aprobado` al PR de código C3 si el PR contiene solo estos cambios. La mitigación
real del riesgo debe quedar condicionada al cierre de Railway: sin `REDIS_URL`, el warning funciona,
pero el rate-limit sigue siendo por worker.
