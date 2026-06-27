"""Capa 3 — Banco de ejercicios por ítems, anclado al grafo de conocimiento.

Modelos NUEVOS y aditivos (decisión D2): `ItemGroup` agrupa ejercicios por
intención pedagógica dentro de un recurso; `NodeExercise` es el banco único
(decisión D3) de ejercicios de ese recurso. No tocan el Sistema A
(`Question`/`Resource`). La medición del alumno (capas 4–5) se difiere (D4).
"""

from django.db import models

from .knowledge import KnowledgeNode


# Plantilla estándar de grupos pedagógicos (handoff §4.4). El orden refleja la
# progresión Comprender → Reconocer → Resolver → Variar → Aplicar → Evaluar.
STANDARD_ITEM_GROUPS = [
    {
        "code": "conceptuales",
        "title": "Preguntas conceptuales",
        "level": "comprender",
        "purpose": "Verificar las ideas clave antes de calcular.",
    },
    {
        "code": "reconocimiento",
        "title": "Reconocimiento",
        "level": "reconocer",
        "purpose": "Identificar elementos, datos o procedimientos.",
    },
    {
        "code": "procedimiento_basico",
        "title": "Ejercicios básicos",
        "level": "resolver",
        "purpose": "Aplicar el procedimiento principal en casos simples.",
    },
    {
        "code": "variacion_controlada",
        "title": "Variación controlada",
        "level": "variar",
        "purpose": "Resolver casos donde cambia una dificultad a la vez.",
    },
    {
        "code": "contextualizados",
        "title": "Problemas contextualizados",
        "level": "aplicar",
        "purpose": "Aplicar el recurso en situaciones expresadas en lenguaje verbal.",
    },
    {
        "code": "tipo_paes",
        "title": "Preguntas tipo PAES",
        "level": "aplicar",
        "purpose": "Resolver preguntas con formato y distractores similares a PAES.",
    },
    {
        "code": "mixto",
        "title": "Desafío mixto",
        "level": "evaluar",
        "purpose": "Comprobar dominio sin avisar el tipo exacto de ejercicio.",
    },
]


class ItemGroup(models.Model):
    """Bloque pedagógico de preguntas dentro de un recurso (nodo hoja).

    No es una pregunta: agrupa ejercicios por intención pedagógica. La
    progresión estándar va de `comprender` a `evaluar` (ver `STANDARD_ITEM_GROUPS`).
    """

    LEVEL_COMPRENDER = "comprender"
    LEVEL_RECONOCER = "reconocer"
    LEVEL_RESOLVER = "resolver"
    LEVEL_VARIAR = "variar"
    LEVEL_APLICAR = "aplicar"
    LEVEL_EVALUAR = "evaluar"
    LEVEL_CHOICES = [
        (LEVEL_COMPRENDER, "Comprender"),
        (LEVEL_RECONOCER, "Reconocer"),
        (LEVEL_RESOLVER, "Resolver"),
        (LEVEL_VARIAR, "Variar"),
        (LEVEL_APLICAR, "Aplicar"),
        (LEVEL_EVALUAR, "Evaluar"),
    ]

    node = models.ForeignKey(
        KnowledgeNode,
        on_delete=models.CASCADE,
        related_name="item_groups",
        verbose_name="nodo",
    )
    code = models.CharField(max_length=40, verbose_name="código")
    title = models.CharField(max_length=120, verbose_name="título")
    purpose = models.TextField(blank=True, verbose_name="propósito")
    level = models.CharField(
        max_length=12, choices=LEVEL_CHOICES, verbose_name="nivel"
    )
    order = models.PositiveSmallIntegerField(default=0, verbose_name="orden")
    required_for_mastery = models.BooleanField(
        default=False, verbose_name="requerido para dominio"
    )
    is_published = models.BooleanField(default=True, verbose_name="publicado")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["node", "order"]
        verbose_name = "grupo de ítems"
        verbose_name_plural = "grupos de ítems"
        constraints = [
            models.UniqueConstraint(
                fields=["node", "code"], name="unique_item_group_per_node"
            ),
        ]

    def __str__(self) -> str:
        return f"{self.title} — {self.node}"


class NodeExercise(models.Model):
    """Ejercicio del banco, anclado a un recurso (nodo) y a un `ItemGroup`.

    Banco ÚNICO (D3): el mismo pool sirve para la práctica visible. La evaluación
    formal (futura) muestreará variantes no vistas desde ejercicios con
    `kind=template` (generadores). En la práctica las respuestas son visibles.
    """

    KIND_ITEM = "item"
    KIND_TEMPLATE = "template"
    KIND_CHOICES = [
        (KIND_ITEM, "Ejercicio concreto"),
        (KIND_TEMPLATE, "Patrón / generador"),
    ]

    FORMAT_MULTIPLE_CHOICE = "multiple_choice"
    FORMAT_OPEN_ANSWER = "open_answer"
    FORMAT_TRUE_FALSE = "true_false"
    FORMAT_MATCHING = "matching"
    FORMAT_COMPLETION = "completion"
    FORMAT_DEVELOPMENT = "development"
    FORMAT_CHOICES = [
        (FORMAT_MULTIPLE_CHOICE, "Selección múltiple"),
        (FORMAT_OPEN_ANSWER, "Respuesta abierta"),
        (FORMAT_TRUE_FALSE, "Verdadero / Falso"),
        (FORMAT_MATCHING, "Términos pareados"),
        (FORMAT_COMPLETION, "Completación"),
        (FORMAT_DEVELOPMENT, "Desarrollo"),
    ]

    DIFFICULTY_BASICA = "basica"
    DIFFICULTY_MEDIA = "media"
    DIFFICULTY_AVANZADA = "avanzada"
    DIFFICULTY_CHOICES = [
        (DIFFICULTY_BASICA, "Básica"),
        (DIFFICULTY_MEDIA, "Media"),
        (DIFFICULTY_AVANZADA, "Avanzada"),
    ]

    # Reusa el vocabulario de competencia del grafo (M1/M2/U).
    COMPETENCIA_CHOICES = KnowledgeNode.COMPETENCIA_CHOICES

    SOURCE_NOTEBOOKLM = "notebooklm_extraction"
    SOURCE_MANUAL = "manual"
    SOURCE_GENERATED = "generated"
    SOURCE_REWRITTEN = "rewritten"
    SOURCE_KIND_CHOICES = [
        (SOURCE_NOTEBOOKLM, "Extracción NotebookLM"),
        (SOURCE_MANUAL, "Manual"),
        (SOURCE_GENERATED, "Generado"),
        (SOURCE_REWRITTEN, "Reescrito"),
    ]

    STATUS_DRAFT = "draft"
    STATUS_READY = "ready"
    STATUS_REVIEW_REQUIRED = "review_required"
    STATUS_PUBLISHED = "published"
    STATUS_ARCHIVED = "archived"
    STATUS_CHOICES = [
        (STATUS_DRAFT, "Borrador"),
        (STATUS_READY, "Listo"),
        (STATUS_REVIEW_REQUIRED, "Requiere revisión"),
        (STATUS_PUBLISHED, "Publicado"),
        (STATUS_ARCHIVED, "Archivado"),
    ]

    stable_id = models.CharField(
        max_length=120,
        blank=True,
        default="",
        verbose_name="id estable",
        help_text="Llave idempotente para reimportar sin duplicar.",
    )
    node = models.ForeignKey(
        KnowledgeNode,
        on_delete=models.CASCADE,
        related_name="exercises",
        verbose_name="nodo",
    )
    item_group = models.ForeignKey(
        ItemGroup,
        on_delete=models.CASCADE,
        related_name="exercises",
        verbose_name="grupo de ítems",
    )
    kind = models.CharField(
        max_length=10, choices=KIND_CHOICES, default=KIND_ITEM, verbose_name="tipo"
    )
    format = models.CharField(
        max_length=20,
        choices=FORMAT_CHOICES,
        default=FORMAT_MULTIPLE_CHOICE,
        verbose_name="formato",
    )
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default=DIFFICULTY_BASICA,
        verbose_name="dificultad",
    )
    competencia = models.CharField(
        max_length=2, choices=COMPETENCIA_CHOICES, blank=True, verbose_name="competencia"
    )
    prompt = models.TextField(verbose_name="enunciado")
    choices = models.JSONField(default=list, blank=True, verbose_name="alternativas")
    correct_answer = models.TextField(blank=True, verbose_name="respuesta correcta")
    solution_steps = models.TextField(blank=True, verbose_name="solución paso a paso")
    explanation = models.TextField(blank=True, verbose_name="explicación")
    conceptual_checks = models.JSONField(
        default=list, blank=True, verbose_name="chequeos conceptuales"
    )
    prerequisites = models.JSONField(
        default=list, blank=True, verbose_name="prerrequisitos detectados"
    )
    pattern = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="patrón generador",
        help_text="Variables/restricciones cuando kind=template. Vacío en ejercicios concretos.",
    )
    paes_style = models.BooleanField(default=False, verbose_name="estilo PAES")
    source_title = models.CharField(
        max_length=200, blank=True, verbose_name="fuente (título)"
    )
    source_location = models.CharField(
        max_length=200, blank=True, verbose_name="fuente (ubicación)"
    )
    source_reference = models.TextField(blank=True, verbose_name="fuente (referencia)")
    source_kind = models.CharField(
        max_length=24,
        choices=SOURCE_KIND_CHOICES,
        default=SOURCE_MANUAL,
        verbose_name="origen",
    )
    status = models.CharField(
        max_length=16,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
        verbose_name="estado",
    )
    legal_review = models.BooleanField(default=False, verbose_name="revisión legal")
    rewrite_required = models.BooleanField(
        default=False, verbose_name="requiere reescritura"
    )
    duplicate_candidate = models.BooleanField(
        default=False, verbose_name="posible duplicado"
    )
    notes = models.TextField(blank=True, verbose_name="notas")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="orden")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["item_group", "order"]
        verbose_name = "ejercicio del nodo"
        verbose_name_plural = "ejercicios del nodo"
        constraints = [
            models.UniqueConstraint(
                fields=["stable_id"],
                condition=~models.Q(stable_id=""),
                name="unique_node_exercise_stable_id",
            ),
        ]
        indexes = [
            models.Index(fields=["node", "status"]),
            models.Index(fields=["item_group", "order"]),
        ]

    def __str__(self) -> str:
        return f"[{self.get_difficulty_display()}] {self.prompt[:60]}"

    @property
    def is_published(self) -> bool:
        return self.status == self.STATUS_PUBLISHED


def ensure_standard_item_groups(node):
    """Crea (idempotente) los grupos de ítems estándar para un nodo.

    Devuelve la lista de `ItemGroup` en orden de progresión. Reejecutarlo no
    duplica: usa `get_or_create` por (node, code).
    """
    groups = []
    for order, spec in enumerate(STANDARD_ITEM_GROUPS, start=1):
        group, _ = ItemGroup.objects.get_or_create(
            node=node,
            code=spec["code"],
            defaults={
                "title": spec["title"],
                "purpose": spec["purpose"],
                "level": spec["level"],
                "order": order,
            },
        )
        groups.append(group)
    return groups
