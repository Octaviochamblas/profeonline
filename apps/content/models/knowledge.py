from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings


class KnowledgeNode(models.Model):
    """Nodo del grafo de conocimiento (árbol autorreferente / adjacency list).

    Jerarquía: Asignatura > Eje > Bloque > Tema > Recurso.
    El recurso (hoja) es la unidad atómica aprendible. La identidad estable y única
    global es `semantic_id` (ej. MAT.NUM.ENTEROS_CONJUNTO.NATURALES); `code` (EE.BB.TT.RR)
    es solo para mostrar/ordenar y es único por asignatura, no global.
    """

    NODE_ASIGNATURA = "asignatura"
    NODE_EJE = "eje"
    NODE_BLOQUE = "bloque"
    NODE_TEMA = "tema"
    NODE_RECURSO = "recurso"
    NODE_TYPE_CHOICES = [
        (NODE_ASIGNATURA, "Asignatura"),
        (NODE_EJE, "Eje"),
        (NODE_BLOQUE, "Bloque"),
        (NODE_TEMA, "Tema"),
        (NODE_RECURSO, "Recurso"),
    ]

    COMPETENCIA_CHOICES = [
        ("M1", "M1 — PAES obligatoria"),
        ("M2", "M2 — PAES electiva"),
        ("U", "U — Universitario / fuera de foco PAES"),
    ]

    DIFICULTAD_CHOICES = [
        ("basica", "Básica"),
        ("media", "Media"),
        ("avanzada", "Avanzada"),
    ]

    semantic_id = models.CharField(
        max_length=120,
        unique=True,
        verbose_name="id semántico",
        help_text="Llave eterna y única global. Ej: MAT.NUM.ENTEROS_CONJUNTO.NATURALES",
    )
    code = models.CharField(
        max_length=20,
        verbose_name="código",
        help_text="EE.BB.TT.RR para mostrar/ordenar. Único por asignatura.",
    )
    node_type = models.CharField(
        max_length=12,
        choices=NODE_TYPE_CHOICES,
        verbose_name="tipo de nodo",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="padre",
    )
    subject_abbr = models.CharField(
        max_length=10,
        verbose_name="asignatura (abrev.)",
        help_text="MAT | FIS | QUI",
    )
    axis_abbr = models.CharField(
        max_length=10,
        blank=True,
        verbose_name="eje (abrev.)",
        help_text="NUM | ALG | GEO | EST | FUND (vacío en asignatura)",
    )
    name = models.CharField(max_length=200, verbose_name="nombre")
    slug = models.SlugField(max_length=220, unique=True)
    order = models.PositiveSmallIntegerField(default=0, verbose_name="orden")
    competencia = models.CharField(
        max_length=2,
        blank=True,
        choices=COMPETENCIA_CHOICES,
        verbose_name="competencia",
    )
    dificultad = models.CharField(
        max_length=10,
        blank=True,
        choices=DIFICULTAD_CHOICES,
        verbose_name="dificultad",
    )
    cursos = models.JSONField(default=list, blank=True, verbose_name="cursos")
    is_published = models.BooleanField(default=False, verbose_name="publicado")

    class Meta:
        ordering = ["subject_abbr", "code"]
        verbose_name = "nodo de conocimiento"
        verbose_name_plural = "nodos de conocimiento"
        constraints = [
            models.UniqueConstraint(
                fields=["subject_abbr", "code"],
                name="unique_code_per_subject",
            )
        ]
        indexes = [
            models.Index(fields=["node_type"]),
            models.Index(fields=["subject_abbr", "axis_abbr"]),
        ]

    def __str__(self) -> str:
        return f"[{self.code}] {self.name}"

    @property
    def is_leaf(self) -> bool:
        return self.node_type == self.NODE_RECURSO

    @property
    def ancestors_chain(self):
        if not hasattr(self, "_cached_chain"):
            chain = []
            cur = self
            while cur:
                chain.append(cur)
                cur = cur.parent
            chain.reverse()
            self._cached_chain = chain
        return self._cached_chain

    @property
    def asignatura_slug(self) -> str:
        chain = self.ancestors_chain
        return chain[0].slug if len(chain) > 0 else ""

    @property
    def eje_slug(self) -> str:
        chain = self.ancestors_chain
        return chain[1].slug if len(chain) > 1 else ""

    @property
    def bloque_slug(self) -> str:
        chain = self.ancestors_chain
        return chain[2].slug if len(chain) > 2 else ""

    @property
    def tema_slug(self) -> str:
        chain = self.ancestors_chain
        return chain[3].slug if len(chain) > 3 else ""


    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name) or slugify(self.semantic_id)
            slug = base_slug
            counter = 1
            while (
                KnowledgeNode.objects.filter(slug=slug)
                .exclude(pk=self.pk)
                .exists()
            ):
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class NodeContent(models.Model):
    """Contenido pedagógico de un nodo hoja (recurso).

    Texto tipo AlonsoFormula: objetivo, explicación, procedimiento, ejemplos.
    El campo `estado` controla indexación SEO: borrador → noindex.
    """

    ESTADO_BORRADOR = "borrador"
    ESTADO_PUBLICADO = "publicado"
    ESTADO_CHOICES = [
        (ESTADO_BORRADOR, "Borrador"),
        (ESTADO_PUBLICADO, "Publicado"),
    ]

    node = models.OneToOneField(
        KnowledgeNode,
        on_delete=models.CASCADE,
        related_name="content",
        verbose_name="nodo",
    )
    objetivo = models.TextField(blank=True, verbose_name="objetivo")
    introduccion = models.TextField(blank=True, verbose_name="introducción")
    resumen = models.TextField(blank=True, verbose_name="resumen (IA)")
    explicacion = models.TextField(blank=True, verbose_name="explicación")
    procedimiento = models.JSONField(default=list, blank=True, verbose_name="procedimiento")
    ejemplos = models.JSONField(default=list, blank=True, verbose_name="ejemplos")
    errores_frecuentes = models.JSONField(
        default=list, blank=True, verbose_name="errores frecuentes"
    )
    estado = models.CharField(
        max_length=12,
        choices=ESTADO_CHOICES,
        default=ESTADO_BORRADOR,
        verbose_name="estado",
    )
    fuente = models.TextField(blank=True, verbose_name="fuente")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    published_at = models.DateTimeField(
        null=True, blank=True, verbose_name="publicado el"
    )

    class Meta:
        verbose_name = "contenido del nodo"
        verbose_name_plural = "contenidos de nodos"

    def __str__(self) -> str:
        return f"Contenido: {self.node}"

    @property
    def is_draft(self) -> bool:
        return self.estado == self.ESTADO_BORRADOR

    def save(self, *args, **kwargs):
        # Sella la primera publicación; no se vuelve a tocar al re-guardar.
        if self.estado == self.ESTADO_PUBLICADO and self.published_at is None:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)


class NodeMedia(models.Model):
    """Video u otro archivo multimedia asociado a un nodo de conocimiento."""

    KIND_VIDEO_YOUTUBE = "video_youtube"
    KIND_FILE = "file"
    KIND_EXTERNAL = "external"
    KIND_CHOICES = [
        (KIND_VIDEO_YOUTUBE, "Video de YouTube"),
        (KIND_FILE, "Archivo"),
        (KIND_EXTERNAL, "Enlace externo"),
    ]

    VIDEO_KIND_EXPLICACION = "explicacion"
    VIDEO_KIND_EJERCICIOS = "ejercicios_resueltos"
    VIDEO_KIND_COMPLEMENTARIO = "complementario"
    VIDEO_KIND_CHOICES = [
        (VIDEO_KIND_EXPLICACION, "Explicación"),
        (VIDEO_KIND_EJERCICIOS, "Ejercicios resueltos"),
        (VIDEO_KIND_COMPLEMENTARIO, "Complementario"),
    ]

    node = models.ForeignKey(
        KnowledgeNode,
        on_delete=models.CASCADE,
        related_name="media",
        verbose_name="nodo",
    )
    kind = models.CharField(max_length=16, choices=KIND_CHOICES, verbose_name="tipo")
    video_kind = models.CharField(
        max_length=20,
        choices=VIDEO_KIND_CHOICES,
        blank=True,
        verbose_name="subtipo de video",
    )
    url = models.URLField(blank=True, verbose_name="URL")
    file = models.FileField(upload_to="node_media/", blank=True, verbose_name="archivo")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="orden")

    class Meta:
        ordering = ["order"]
        verbose_name = "media del nodo"
        verbose_name_plural = "medias del nodo"

    def __str__(self) -> str:
        return f"{self.get_kind_display()}: {self.node}"


class NodePrerequisite(models.Model):
    """Arista del DAG de prerrequisitos: `node` requiere haber dominado `requires`.

    En F1 solo se define el esquema. La carga del DAG y la validación de aciclicidad
    se implementan en F6.
    """

    KIND_REQUERIDO = "requerido"
    KIND_RECOMENDADO = "recomendado"
    KIND_CHOICES = [
        (KIND_REQUERIDO, "Requerido"),
        (KIND_RECOMENDADO, "Recomendado"),
    ]

    node = models.ForeignKey(
        KnowledgeNode,
        on_delete=models.CASCADE,
        related_name="prerequisites",
        verbose_name="nodo",
    )
    requires = models.ForeignKey(
        KnowledgeNode,
        on_delete=models.CASCADE,
        related_name="required_by",
        verbose_name="requiere",
    )
    kind = models.CharField(
        max_length=12,
        choices=KIND_CHOICES,
        default=KIND_REQUERIDO,
        verbose_name="tipo",
    )
    min_mastery = models.FloatField(default=0.75, verbose_name="dominio mínimo")

    class Meta:
        verbose_name = "prerrequisito"
        verbose_name_plural = "prerrequisitos"
        constraints = [
            models.UniqueConstraint(
                fields=["node", "requires"],
                name="unique_node_prerequisite",
            )
        ]

    def __str__(self) -> str:
        return f"{self.node.code} ← {self.requires.code} ({self.kind})"


class NodeAssessmentQuestion(models.Model):
    """Pregunta de evaluación formal de un nodo de conocimiento."""
    STATUS_BORRADOR = "borrador"
    STATUS_PUBLICADA = "publicada"
    STATUS_ARCHIVADA = "archivada"
    STATUS_CHOICES = [
        (STATUS_BORRADOR, "Borrador"),
        (STATUS_PUBLICADA, "Publicada"),
        (STATUS_ARCHIVADA, "Archivada"),
    ]

    LEVEL_DEFINICION = 1
    LEVEL_EJERCICIOS = 2
    LEVEL_PROBLEMAS = 3
    LEVEL_CHOICES = [
        (LEVEL_DEFINICION, "Definición"),
        (LEVEL_EJERCICIOS, "Ejercicios simples"),
        (LEVEL_PROBLEMAS, "Problemas de aplicación"),
    ]

    node = models.ForeignKey(
        KnowledgeNode,
        on_delete=models.CASCADE,
        related_name="assessment_questions",
        verbose_name="nodo",
    )
    level = models.PositiveSmallIntegerField(
        choices=LEVEL_CHOICES,
        verbose_name="nivel",
    )
    text = models.TextField(verbose_name="enunciado")
    explanation = models.TextField(blank=True, verbose_name="explicación")
    status = models.CharField(
        max_length=12,
        choices=STATUS_CHOICES,
        default=STATUS_BORRADOR,
        verbose_name="estado",
    )
    generation_key = models.CharField(
        max_length=64,
        blank=True,
        verbose_name="llave de generación",
    )
    order = models.PositiveIntegerField(default=0, verbose_name="orden")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "pregunta de evaluación de nodo"
        verbose_name_plural = "preguntas de evaluación de nodos"

    def __str__(self) -> str:
        return f"[{self.get_level_display()}] {self.node.name}: {self.text[:50]}"


class NodeAssessmentChoice(models.Model):
    """Alternativa para una pregunta de evaluación formal de nodo."""
    question = models.ForeignKey(
        NodeAssessmentQuestion,
        on_delete=models.CASCADE,
        related_name="choices",
        verbose_name="pregunta",
    )
    text = models.CharField(max_length=500, verbose_name="texto")
    is_correct = models.BooleanField(default=False, verbose_name="es correcta")
    order = models.PositiveIntegerField(default=0, verbose_name="orden")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "alternativa de evaluación"
        verbose_name_plural = "alternativas de evaluación"

    def __str__(self) -> str:
        return f"{self.text[:50]} ({'Correcta' if self.is_correct else 'Incorrecta'})"


class NodeAssessmentAttempt(models.Model):
    """Intento de evaluación formal de un nodo realizado por un alumno."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="node_assessment_attempts",
        verbose_name="usuario",
    )
    node = models.ForeignKey(
        KnowledgeNode,
        on_delete=models.CASCADE,
        related_name="assessment_attempts",
        verbose_name="nodo",
    )
    level = models.PositiveSmallIntegerField(verbose_name="nivel")
    score = models.PositiveSmallIntegerField(verbose_name="aciertos")
    total = models.PositiveSmallIntegerField(verbose_name="total de preguntas")
    passed = models.BooleanField(verbose_name="aprobado")
    attempt_number = models.PositiveSmallIntegerField(verbose_name="número de intento")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="creado el")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "intento de evaluación de nodo"
        verbose_name_plural = "intentos de evaluación de nodos"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "node", "level", "attempt_number"],
                name="unique_user_node_level_attempt",
            )
        ]

    def __str__(self) -> str:
        return f"{self.user.email} - {self.node.name} L{self.level} - Intento {self.attempt_number} ({'Aprobado' if self.passed else 'Reprobado'})"


class NodeAssessmentAnswer(models.Model):
    """Respuesta específica dada por un usuario en un intento de evaluación."""
    attempt = models.ForeignKey(
        NodeAssessmentAttempt,
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name="intento",
    )
    question = models.ForeignKey(
        NodeAssessmentQuestion,
        on_delete=models.CASCADE,
        related_name="attempt_answers",
        verbose_name="pregunta",
    )
    selected_choice = models.ForeignKey(
        NodeAssessmentChoice,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="alternativa seleccionada",
    )
    is_correct = models.BooleanField(verbose_name="es correcta")

    class Meta:
        verbose_name = "respuesta de intento de evaluación"
        verbose_name_plural = "respuestas de intentos de evaluación"

    def __str__(self) -> str:
        return f"{self.attempt} - {self.question.id}: {self.is_correct}"
