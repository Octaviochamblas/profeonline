# Estándar editorial de recursos teóricos

## Contrato backend

El perfil vigente es:

```json
{
  "guide": {
    "profile": "teorico-interactivo-v1"
  }
}
```

Cuando el perfil está presente, tanto el paquete completo como la etapa de contenido
deben superar estas compuertas antes de escribir:

- nueve secciones editoriales en el orden canónico vigente;
- pregunta de activación, propósito, prerrequisitos y recorrido;
- explicación sencilla y explicación formal desarrolladas por separado;
- ejemplo con qué se hace, por qué, regla aplicada y comprobación;
- procedimiento general con variaciones;
- diferencias integradas con errores y correcciones;
- cierre específico;
- exactamente tres comprobaciones formativas;
- briefs para imagen conceptual e infografía completa.

La validación vive en:

- `apps/content/services/editorial_guide_service.py`;
- `apps/content/services/publication_pipeline_service.py`;
- `apps/content/services/reading_checkpoint_service.py`.

El perfil no se persiste en `Resource`: identifica y valida el contrato del paquete.
Las comprobaciones normalizadas se guardan en `Resource.reading_checkpoints`.

Los paquetes históricos sin perfil continúan aceptándose para mantenimiento. Un
perfil desconocido se rechaza. No se debe eliminar esta compatibilidad sin una
migración editorial explícita del catálogo.

## Fuente de autoría

La plantilla, el constructor y las reglas completas viven en el repositorio hermano:

```text
profeonline-uploader/docs/estandar-recurso-teorico-interactivo.md
profeonline-uploader/theoretical_resource_profile.mjs
```

El backend valida; no genera ni completa contenido faltante.
