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

## Orden visible de alternativas

El orden de autoría o persistencia de las alternativas no tiene significado
pedagógico y nunca debe permitir inferir la respuesta correcta. La interfaz
baraja las cuatro alternativas una sola vez al cargar cada comprobación,
práctica o evaluación. Una recarga genera un orden nuevo, pero el orden se
mantiene estable mientras el estudiante responde.

El barajado sólo mueve elementos visuales: conserva el identificador y el valor
de cada alternativa, por lo que la corrección y el historial continúan
asociándose a la opción seleccionada, no a las letras A, B, C o D.

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
