# Enlace cruzado Sistema A / Sistema B — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Sugerir y dejar confirmar un enlace cruzado "Ver también" entre un `Resource` (video, Sistema A) y el `KnowledgeNode` (Sistema B) al que corresponde, sin fusionar los datos de ambos sistemas.

**Architecture:** Modelo puente `ResourceNodeSuggestion` (OneToOne a `Resource`). Comando de management que corre un pipeline de 3 pasos (match determinístico de bloque por nombre → candidato atómico por similitud de texto dentro del bloque → corroboración de IA con prompt acotado) para recursos sin sugerencia previa. Vista de revisión staff-only con confirmación automática o manual (autocompletado). Bloque "Ver también" renderizado en ambos templates de detalle cuando existe una sugerencia confirmada.

**Tech Stack:** Django 6, SQLite (tests/local) / Postgres (producción), `difflib.SequenceMatcher` (stdlib, sin dependencia nueva), `apps.content.services.ai_generation_service.call_ai_structured_json` (ya existente, Gemini/OpenAI).

## Global Constraints

- No tocar `apps/content/services/publication_pipeline_service.py` ni la máquina de estados de `PublicationItem`.
- No incrustar el video como `NodeMedia` — solo enlace cruzado de navegación.
- No procesar el catálogo ya publicado (181 recursos) en esta versión — solo recursos sin ninguna fila `ResourceNodeSuggestion` existente, hacia adelante.
- Sin dependencias nuevas (nada de pgvector/sentence-transformers/Postgres-specific search) — todo el matching de texto usa `difflib` del stdlib, portable entre SQLite (tests) y Postgres (producción). Esto es una decisión de implementación tomada durante este plan (el spec sugería búsqueda nativa de Postgres; se cambia a `difflib` por portabilidad, sin romper el requisito "sin dependencia nueva").
- Modelo de IA económico/rápido para la corroboración — reusar `call_ai_structured_json` tal cual (ya usa `gemini-2.5-flash`/`gpt-4o-mini`), sin parámetros nuevos de modelo.
- Prompt de corroboración nunca incluye el contenido completo de un nodo (`explicacion`) ni la transcripción completa del video — solo nombre+objetivo de cada candidato y un extracto corto (≤800 caracteres) de transcripción si el título es insuficiente.
- Todo el trabajo es aditivo: nuevo modelo, nuevo servicio, nuevo comando, nuevas vistas/URLs, cambios pequeños y acotados en 2 templates existentes. Ningún modelo/vista/servicio existente se modifica en su comportamiento actual.
- Suite completa (`python manage.py test`) + `check --deploy` antes de push, según regla del proyecto (`CLAUDE.md`). Cada tarea de este plan corre solo su módulo (`apps.content`) durante desarrollo.

## File Structure

| Archivo | Responsabilidad | Tarea |
|---|---|---|
| `apps/content/models/resource_node_suggestion.py` | Crear — modelo `ResourceNodeSuggestion` (puente) | 1 |
| `apps/content/models/__init__.py` | Modificar — exportar el modelo nuevo | 1 |
| `apps/content/admin.py` | Modificar — registrar `ResourceNodeSuggestionAdmin` | 1 |
| `apps/content/migrations/0044_resourcenodesuggestion.py` | Generar (`makemigrations`) | 1 |
| `apps/content/services/node_matching_service.py` | Crear — los 3 pasos de matching + orquestador `generate_suggestion` | 2, 3, 4 |
| `apps/content/management/commands/suggest_resource_node_links.py` | Crear — comando que corre el pipeline sobre recursos sin sugerencia | 5 |
| `apps/content/views/node_suggestions.py` | Crear — revisión, confirmar, descartar, autocompletado | 6 |
| `apps/content/urls/publish_urls.py` | Modificar — 4 rutas nuevas | 6 |
| `templates/pages/node_suggestions_review.html` | Crear — cola de revisión staff-only | 6, 7 |
| `templates/base.html` | Modificar — link en menú de administrador | 7 |
| `apps/content/views/resource_detail.py` | Modificar — contexto `related_node` | 8 |
| `templates/pages/resource_detail.html` | Modificar — bloque "Ver también" | 8 |
| `apps/learn/views.py` | Modificar — contexto `related_resource` en `_recurso_view` | 9 |
| `templates/learn/node_detail.html` | Modificar — bloque "Ver también" | 9 |
| `apps/content/tests/test_resource_node_suggestion_model.py` | Crear | 1 |
| `apps/content/tests/test_node_matching_service.py` | Crear | 2, 3, 4 |
| `apps/content/tests/test_suggest_resource_node_links.py` | Crear | 5 |
| `apps/content/tests/test_node_suggestions_views.py` | Crear | 6 |
| `apps/content/tests/test_resource_node_cross_link.py` | Crear | 8 |
| `apps/learn/tests.py` | Modificar — agregar `NodeDetailCrossLinkTests` | 9 |

---

### Task 1: Modelo `ResourceNodeSuggestion`

**Files:**
- Create: `apps/content/models/resource_node_suggestion.py`
- Modify: `apps/content/models/__init__.py`
- Modify: `apps/content/admin.py`
- Create: `apps/content/migrations/0044_resourcenodesuggestion.py` (generado por `makemigrations`, no a mano)
- Test: `apps/content/tests/test_resource_node_suggestion_model.py`

**Interfaces:**
- Produces: `ResourceNodeSuggestion` con campos `resource` (OneToOne a `content.Resource`, `related_name="node_suggestion"`), `node` (FK nullable a `content.KnowledgeNode`, `related_name="resource_suggestions"`), `status` (`STATUS_SUGERIDO="sugerido"`, `STATUS_CONFIRMADO="confirmado"`, `STATUS_DESCARTADO="descartado"`, `STATUS_SIN_BLOQUE="sin_bloque"`), `origen` (`ORIGEN_IA="ia"`, `ORIGEN_MANUAL="manual"`), `ai_rationale` (Text), `ai_corrigio` (Bool), `created_at`, `confirmed_at`.

- [ ] **Step 1: Write the failing test**

```python
# apps/content/tests/test_resource_node_suggestion_model.py
from django.test import TestCase

from apps.content.models import (
    Area,
    KnowledgeNode,
    Resource,
    ResourceNodeSuggestion,
    Subject,
    Topic,
)


def _node(sid, code, name="N", node_type=KnowledgeNode.NODE_RECURSO):
    return KnowledgeNode.objects.create(
        semantic_id=sid, code=code, node_type=node_type, subject_abbr="MAT", name=name,
    )


class ResourceNodeSuggestionModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        area = Area.objects.create(name="Ciencias")
        subject = Subject.objects.create(name="Matemática Escolar", area=area)
        topic = Topic.objects.create(subject=subject, name="Fracciones")
        cls.resource = Resource.objects.create(title="Video de fracciones", topic=topic)
        cls.node = _node("MAT.A", "01.01.01.01", "Fracción propia")

    def test_creates_confirmed_suggestion(self):
        suggestion = ResourceNodeSuggestion.objects.create(
            resource=self.resource,
            node=self.node,
            status=ResourceNodeSuggestion.STATUS_CONFIRMADO,
            origen=ResourceNodeSuggestion.ORIGEN_IA,
            ai_rationale="Coincide en tema y título.",
        )
        self.assertEqual(self.resource.node_suggestion, suggestion)
        self.assertEqual(self.node.resource_suggestions.first(), suggestion)
        self.assertIn("Video de fracciones", str(suggestion))

    def test_node_can_be_null_for_sin_bloque(self):
        suggestion = ResourceNodeSuggestion.objects.create(
            resource=self.resource, node=None, status=ResourceNodeSuggestion.STATUS_SIN_BLOQUE,
        )
        self.assertIsNone(suggestion.node)
        self.assertIn("sin bloque", str(suggestion))

    def test_one_suggestion_per_resource(self):
        ResourceNodeSuggestion.objects.create(resource=self.resource, node=self.node)
        with self.assertRaises(Exception):
            ResourceNodeSuggestion.objects.create(resource=self.resource, node=self.node)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/Scripts/python.exe manage.py test apps.content.tests.test_resource_node_suggestion_model -v 2`
Expected: FAIL with `ImportError: cannot import name 'ResourceNodeSuggestion'`

- [ ] **Step 3: Write the model**

```python
# apps/content/models/resource_node_suggestion.py
from django.db import models


class ResourceNodeSuggestion(models.Model):
    """Sugerencia (o confirmación) de a qué KnowledgeNode corresponde un Resource.

    Puente de navegación entre Sistema A (Resource, video) y Sistema B
    (KnowledgeNode, /aprender/). No fusiona datos: solo habilita un enlace
    cruzado "Ver también" una vez confirmada.
    """

    STATUS_SUGERIDO = "sugerido"
    STATUS_CONFIRMADO = "confirmado"
    STATUS_DESCARTADO = "descartado"
    STATUS_SIN_BLOQUE = "sin_bloque"
    STATUS_CHOICES = [
        (STATUS_SUGERIDO, "Sugerido"),
        (STATUS_CONFIRMADO, "Confirmado"),
        (STATUS_DESCARTADO, "Descartado"),
        (STATUS_SIN_BLOQUE, "Sin bloque encontrado"),
    ]

    ORIGEN_IA = "ia"
    ORIGEN_MANUAL = "manual"
    ORIGEN_CHOICES = [
        (ORIGEN_IA, "IA"),
        (ORIGEN_MANUAL, "Manual"),
    ]

    resource = models.OneToOneField(
        "content.Resource",
        on_delete=models.CASCADE,
        related_name="node_suggestion",
        verbose_name="recurso",
    )
    node = models.ForeignKey(
        "content.KnowledgeNode",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="resource_suggestions",
        verbose_name="nodo",
    )
    status = models.CharField(
        max_length=12,
        choices=STATUS_CHOICES,
        default=STATUS_SUGERIDO,
        verbose_name="estado",
    )
    origen = models.CharField(
        max_length=8, choices=ORIGEN_CHOICES, blank=True, verbose_name="origen",
    )
    ai_rationale = models.TextField(blank=True, verbose_name="razón de la IA")
    ai_corrigio = models.BooleanField(
        default=False, verbose_name="la IA corrigió el candidato",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "sugerencia de nodo para recurso"
        verbose_name_plural = "sugerencias de nodo para recursos"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        target = self.node.name if self.node else "(sin bloque)"
        return f"{self.resource.title} -> {target} [{self.status}]"
```

- [ ] **Step 4: Registrar el modelo en `__init__.py`**

En `apps/content/models/__init__.py`, agregar al final:

```python
from .resource_node_suggestion import ResourceNodeSuggestion
```

- [ ] **Step 5: Generar y aplicar la migración**

Run: `.venv/Scripts/python.exe manage.py makemigrations content`
Expected: `Migrations for 'content': apps/content/migrations/0044_resourcenodesuggestion.py - Create model ResourceNodeSuggestion`

Run: `.venv/Scripts/python.exe manage.py migrate content`
Expected: `Applying content.0044_resourcenodesuggestion... OK`

- [ ] **Step 6: Run test to verify it passes**

Run: `.venv/Scripts/python.exe manage.py test apps.content.tests.test_resource_node_suggestion_model -v 2`
Expected: `Ran 3 tests ... OK`

- [ ] **Step 7: Registrar en el admin**

En `apps/content/admin.py`, agregar `ResourceNodeSuggestion` al bloque de imports de `apps.content.models` (orden alfabético, junto a `NodePrerequisite`/`Question`), y agregar, después de `NodePrerequisiteAdmin`:

```python
@admin.register(ResourceNodeSuggestion)
class ResourceNodeSuggestionAdmin(admin.ModelAdmin):
    list_display = ("resource", "node", "status", "origen", "ai_corrigio", "created_at")
    list_filter = ("status", "origen", "ai_corrigio")
    search_fields = ("resource__title", "node__name", "node__code")
    raw_id_fields = ("resource", "node")
```

- [ ] **Step 8: Commit**

```bash
git add apps/content/models/resource_node_suggestion.py apps/content/models/__init__.py apps/content/admin.py apps/content/migrations/0044_resourcenodesuggestion.py apps/content/tests/test_resource_node_suggestion_model.py
git commit -m "feat(content): modelo ResourceNodeSuggestion (puente Resource<->KnowledgeNode)"
```

---

### Task 2: Servicio de matching — Paso 1 (`find_matching_block`)

**Files:**
- Create: `apps/content/services/node_matching_service.py`
- Test: `apps/content/tests/test_node_matching_service.py`

**Interfaces:**
- Consumes: `KnowledgeNode` (modelo existente, campos `node_type`, `name`, `code`).
- Produces: `find_matching_block(resource) -> KnowledgeNode | None`. Usado por Task 4 (orquestador).

- [ ] **Step 1: Write the failing test**

```python
# apps/content/tests/test_node_matching_service.py
from django.test import TestCase

from apps.content.models import Area, KnowledgeNode, Resource, Subject, Topic
from apps.content.services.node_matching_service import find_matching_block


def _node(sid, code, name, node_type):
    return KnowledgeNode.objects.create(
        semantic_id=sid, code=code, node_type=node_type, subject_abbr="MAT", name=name,
    )


class FindMatchingBlockTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        area = Area.objects.create(name="Ciencias")
        cls.subject = Subject.objects.create(name="Matemática Escolar", area=area)
        cls.bloque_fracciones = _node(
            "MAT.FRAC", "01.03", "Fracciones", KnowledgeNode.NODE_BLOQUE,
        )
        cls.bloque_conjuntos = _node(
            "MAT.CONJ", "01.02", "Conjuntos y relaciones", KnowledgeNode.NODE_BLOQUE,
        )

    def test_matches_block_by_name_similarity(self):
        topic = Topic.objects.create(subject=self.subject, name="Fracciones")
        resource = Resource.objects.create(title="Suma de fracciones", topic=topic)
        match = find_matching_block(resource)
        self.assertEqual(match, self.bloque_fracciones)

    def test_returns_none_when_no_topic(self):
        resource = Resource.objects.create(title="Video suelto", topic=None)
        self.assertIsNone(find_matching_block(resource))

    def test_returns_none_when_no_reasonable_match(self):
        topic = Topic.objects.create(subject=self.subject, name="Termodinámica avanzada")
        resource = Resource.objects.create(title="Entropía y calor", topic=topic)
        self.assertIsNone(find_matching_block(resource))
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/Scripts/python.exe manage.py test apps.content.tests.test_node_matching_service -v 2`
Expected: FAIL with `ModuleNotFoundError: No module named 'apps.content.services.node_matching_service'`

- [ ] **Step 3: Write minimal implementation**

```python
# apps/content/services/node_matching_service.py
"""Matching entre Resource (Sistema A) y KnowledgeNode (Sistema B).

Pipeline de 3 pasos, sin dependencias nuevas: paso 1 y 2 usan difflib
(stdlib, portable entre SQLite y Postgres); paso 3 reusa
ai_generation_service.call_ai_structured_json como corroboración acotada.
"""
from difflib import SequenceMatcher

from apps.content.models import KnowledgeNode

BLOCK_MATCH_THRESHOLD = 0.5
MAX_LEAF_CANDIDATES = 20


def _similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, (a or "").lower().strip(), (b or "").lower().strip()).ratio()


def find_matching_block(resource) -> KnowledgeNode | None:
    """Paso 1: encuentra el bloque/tema de KnowledgeNode que mejor calza con el
    Topic del recurso, por similitud de nombre. None si no hay Topic o no hay
    match razonable (bajo BLOCK_MATCH_THRESHOLD)."""
    topic = resource.topic
    if topic is None:
        return None

    candidates = KnowledgeNode.objects.filter(
        node_type__in=[KnowledgeNode.NODE_BLOQUE, KnowledgeNode.NODE_TEMA],
    )
    best_node = None
    best_score = 0.0
    for node in candidates:
        score = _similarity(topic.name, node.name)
        if score > best_score:
            best_score = score
            best_node = node

    if best_score < BLOCK_MATCH_THRESHOLD:
        return None
    return best_node
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/Scripts/python.exe manage.py test apps.content.tests.test_node_matching_service -v 2`
Expected: `Ran 3 tests ... OK`

- [ ] **Step 5: Commit**

```bash
git add apps/content/services/node_matching_service.py apps/content/tests/test_node_matching_service.py
git commit -m "feat(content): paso 1 del matching Resource->KnowledgeNode (bloque por nombre)"
```

---

### Task 3: Servicio de matching — Paso 2 (`find_candidate_leaf_nodes`)

**Files:**
- Modify: `apps/content/services/node_matching_service.py`
- Modify: `apps/content/tests/test_node_matching_service.py`

**Interfaces:**
- Consumes: `find_matching_block` (Task 2).
- Produces: `find_candidate_leaf_nodes(block_node, resource) -> list[tuple[KnowledgeNode, float]]`, ordenado descendente por score, máximo 3 elementos. Usado por Task 4.

- [ ] **Step 1: Write the failing test**

Agregar al final de `apps/content/tests/test_node_matching_service.py`:

```python
from apps.content.services.node_matching_service import find_candidate_leaf_nodes


class FindCandidateLeafNodesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        area = Area.objects.create(name="Ciencias")
        subject = Subject.objects.create(name="Matemática Escolar", area=area)
        cls.topic = Topic.objects.create(subject=subject, name="Fracciones")
        cls.bloque = _node("MAT.FRAC", "01.03", "Fracciones", KnowledgeNode.NODE_BLOQUE)
        cls.tema = _node("MAT.FRAC.T1", "01.03.01", "Fracciones básicas", KnowledgeNode.NODE_TEMA)
        cls.tema.parent = cls.bloque
        cls.tema.save()
        cls.propia = _node("MAT.FRAC.PROPIA", "01.03.01.01", "Fracción propia", KnowledgeNode.NODE_RECURSO)
        cls.propia.parent = cls.tema
        cls.propia.save()
        cls.impropia = _node("MAT.FRAC.IMPROPIA", "01.03.01.02", "Fracción impropia", KnowledgeNode.NODE_RECURSO)
        cls.impropia.parent = cls.tema
        cls.impropia.save()

    def test_finds_best_leaf_by_title_similarity(self):
        resource = Resource.objects.create(title="Qué es una fracción propia", topic=self.topic)
        results = find_candidate_leaf_nodes(self.bloque, resource)
        self.assertGreater(len(results), 0)
        top_node, top_score = results[0]
        self.assertEqual(top_node, self.propia)
        self.assertGreater(top_score, 0)

    def test_returns_at_most_three_candidates(self):
        resource = Resource.objects.create(title="Fracciones en general", topic=self.topic)
        results = find_candidate_leaf_nodes(self.bloque, resource)
        self.assertLessEqual(len(results), 3)

    def test_empty_when_no_leaf_descendants(self):
        bloque_vacio = _node("MAT.VACIO", "01.09", "Bloque vacío", KnowledgeNode.NODE_BLOQUE)
        resource = Resource.objects.create(title="Video huérfano", topic=self.topic)
        self.assertEqual(find_candidate_leaf_nodes(bloque_vacio, resource), [])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/Scripts/python.exe manage.py test apps.content.tests.test_node_matching_service.FindCandidateLeafNodesTests -v 2`
Expected: FAIL with `ImportError: cannot import name 'find_candidate_leaf_nodes'`

- [ ] **Step 3: Write minimal implementation**

Agregar a `apps/content/services/node_matching_service.py`:

```python
def find_candidate_leaf_nodes(block_node, resource):
    """Paso 2: dentro de block_node (bloque o tema), busca los nodos hoja
    ('recurso') mas parecidos al titulo del recurso, via similitud de texto.
    Devuelve hasta 3 pares (node, score) ordenados de mayor a menor score.
    """
    leaves = list(
        KnowledgeNode.objects.filter(
            node_type=KnowledgeNode.NODE_RECURSO,
            code__startswith=f"{block_node.code}.",
        ).order_by("code")[:MAX_LEAF_CANDIDATES]
    )
    if not leaves:
        return []

    scored = [(leaf, _similarity(resource.title, leaf.name)) for leaf in leaves]
    scored.sort(key=lambda pair: pair[1], reverse=True)
    return scored[:3]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/Scripts/python.exe manage.py test apps.content.tests.test_node_matching_service -v 2`
Expected: `Ran 6 tests ... OK`

- [ ] **Step 5: Commit**

```bash
git add apps/content/services/node_matching_service.py apps/content/tests/test_node_matching_service.py
git commit -m "feat(content): paso 2 del matching Resource->KnowledgeNode (candidato atomico por texto)"
```

---

### Task 4: Servicio de matching — Paso 3 (corroboración IA) + orquestador

**Files:**
- Modify: `apps/content/services/node_matching_service.py`
- Modify: `apps/content/tests/test_node_matching_service.py`

**Interfaces:**
- Consumes: `apps.content.services.ai_generation_service.call_ai_structured_json(prompt, api_key=None) -> dict` (ya existente).
- Produces: `corroborate_with_ai(resource, candidate_leaf, alternatives) -> dict | None` y
  `generate_suggestion(resource) -> ResourceNodeSuggestion`. Usado por Task 5 (comando).

- [ ] **Step 1: Write the failing test**

Agregar al final de `apps/content/tests/test_node_matching_service.py`:

```python
from unittest.mock import patch

from apps.content.models import ResourceNodeSuggestion
from apps.content.services.node_matching_service import (
    corroborate_with_ai,
    generate_suggestion,
)


class CorroborateWithAiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        area = Area.objects.create(name="Ciencias")
        subject = Subject.objects.create(name="Matemática Escolar", area=area)
        topic = Topic.objects.create(subject=subject, name="Fracciones")
        cls.resource = Resource.objects.create(title="Fracción impropia explicada", topic=topic)
        cls.candidate = _node("MAT.A", "01.03.01.01", "Fracción propia", KnowledgeNode.NODE_RECURSO)
        cls.alt = _node("MAT.B", "01.03.01.02", "Fracción impropia", KnowledgeNode.NODE_RECURSO)

    @patch("apps.content.services.node_matching_service.call_ai_structured_json")
    def test_ai_confirms_candidate(self, mock_call):
        mock_call.return_value = {
            "chosen_id": self.candidate.id, "corrected": False, "rationale": "Coincide bien.",
        }
        result = corroborate_with_ai(self.resource, self.candidate, [self.alt])
        self.assertEqual(result["node"], self.candidate)
        self.assertFalse(result["ai_corrigio"])
        self.assertEqual(result["ai_rationale"], "Coincide bien.")

    @patch("apps.content.services.node_matching_service.call_ai_structured_json")
    def test_ai_corrects_to_alternative(self, mock_call):
        mock_call.return_value = {
            "chosen_id": self.alt.id, "corrected": True, "rationale": "El título dice impropia.",
        }
        result = corroborate_with_ai(self.resource, self.candidate, [self.alt])
        self.assertEqual(result["node"], self.alt)
        self.assertTrue(result["ai_corrigio"])

    @patch("apps.content.services.node_matching_service.call_ai_structured_json")
    def test_returns_none_when_ai_unavailable(self, mock_call):
        mock_call.side_effect = ValueError("sin llaves configuradas")
        result = corroborate_with_ai(self.resource, self.candidate, [self.alt])
        self.assertIsNone(result)


class GenerateSuggestionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        area = Area.objects.create(name="Ciencias")
        subject = Subject.objects.create(name="Matemática Escolar", area=area)
        cls.topic = Topic.objects.create(subject=subject, name="Fracciones")
        cls.bloque = _node("MAT.FRAC", "01.03", "Fracciones", KnowledgeNode.NODE_BLOQUE)
        cls.propia = _node("MAT.FRAC.PROPIA", "01.03.01.01", "Fracción propia", KnowledgeNode.NODE_RECURSO)

    @patch("apps.content.services.node_matching_service.call_ai_structured_json")
    def test_creates_sugerido_with_ai_confirmation(self, mock_call):
        mock_call.return_value = {
            "chosen_id": self.propia.id, "corrected": False, "rationale": "Calza.",
        }
        resource = Resource.objects.create(title="Qué es una fracción propia", topic=self.topic)
        suggestion = generate_suggestion(resource)
        self.assertEqual(suggestion.status, ResourceNodeSuggestion.STATUS_SUGERIDO)
        self.assertEqual(suggestion.node, self.propia)
        self.assertEqual(suggestion.origen, ResourceNodeSuggestion.ORIGEN_IA)

    def test_creates_sin_bloque_when_no_topic_match(self):
        area = Area.objects.create(name="Otra")
        subject = Subject.objects.create(name="Otra materia", area=area)
        topic = Topic.objects.create(subject=subject, name="Zzz sin relación alguna")
        resource = Resource.objects.create(title="Video random", topic=topic)
        suggestion = generate_suggestion(resource)
        self.assertEqual(suggestion.status, ResourceNodeSuggestion.STATUS_SIN_BLOQUE)
        self.assertIsNone(suggestion.node)

    def test_idempotent_does_not_duplicate(self):
        resource = Resource.objects.create(title="Fracción propia", topic=self.topic)
        with patch(
            "apps.content.services.node_matching_service.call_ai_structured_json",
            return_value={"chosen_id": self.propia.id, "corrected": False, "rationale": "x"},
        ):
            first = generate_suggestion(resource)
            second = generate_suggestion(resource)
        self.assertEqual(first.pk, second.pk)
        self.assertEqual(ResourceNodeSuggestion.objects.filter(resource=resource).count(), 1)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/Scripts/python.exe manage.py test apps.content.tests.test_node_matching_service.CorroborateWithAiTests apps.content.tests.test_node_matching_service.GenerateSuggestionTests -v 2`
Expected: FAIL with `ImportError: cannot import name 'corroborate_with_ai'`

- [ ] **Step 3: Write minimal implementation**

Agregar a `apps/content/services/node_matching_service.py` (al inicio, agregar el import; al final, las 2 funciones):

```python
from apps.content.services.ai_generation_service import call_ai_structured_json
```

```python
def _node_summary(node) -> str:
    content = getattr(node, "content", None)
    objetivo = (content.objetivo if content else "") or ""
    return f"{node.code} — {node.name}: {objetivo}".strip()


def corroborate_with_ai(resource, candidate_leaf, alternatives):
    """Paso 3: le pide a la IA confirmar o corregir el candidato del paso 2.

    alternatives: lista de 0 a 2 KnowledgeNode. Devuelve
    {'node': KnowledgeNode, 'ai_corrigio': bool, 'ai_rationale': str}, o None
    si la IA no está disponible o falla (se degrada al candidato de texto).
    """
    transcript_excerpt = (resource.transcript or "").strip()[:800]
    alt_lines = "\n".join(f"- id={n.id}: {_node_summary(n)}" for n in alternatives)

    prompt = (
        "Un video educativo necesita conectarse al nodo de conocimiento correcto.\n\n"
        f'Video: "{resource.title}"\n'
        + (f"Extracto de la transcripción: {transcript_excerpt}\n" if transcript_excerpt else "")
        + "\nCandidato sugerido por búsqueda de texto:\n"
        f"- id={candidate_leaf.id}: {_node_summary(candidate_leaf)}\n\n"
        "Alternativas cercanas:\n"
        f"{alt_lines if alt_lines else '(ninguna)'}\n\n"
        "¿Es el candidato sugerido el más adecuado para este video? Si no, ¿cuál de "
        "las alternativas calza mejor? Responde en JSON exacto:\n"
        '{"chosen_id": <id del nodo elegido>, "corrected": <true si elegiste una '
        'alternativa en vez del candidato, false si confirmaste el candidato>, '
        '"rationale": "<razón breve, 1-2 oraciones>"}'
    )

    try:
        data = call_ai_structured_json(prompt)
    except (ValueError, RuntimeError):
        return None

    chosen_id = data.get("chosen_id")
    rationale = str(data.get("rationale", ""))[:500]
    corrected = bool(data.get("corrected", False))

    options = {n.id: n for n in [candidate_leaf, *alternatives]}
    chosen_node = options.get(chosen_id, candidate_leaf)

    return {
        "node": chosen_node,
        "ai_corrigio": corrected and chosen_node.id != candidate_leaf.id,
        "ai_rationale": rationale,
    }


def generate_suggestion(resource):
    """Corre el pipeline de 3 pasos y crea el ResourceNodeSuggestion del recurso.

    Idempotente: si ya existe una fila para este recurso, la devuelve sin
    reprocesar (nunca crea una segunda).
    """
    from apps.content.models import ResourceNodeSuggestion

    existing = ResourceNodeSuggestion.objects.filter(resource=resource).first()
    if existing:
        return existing

    block_node = find_matching_block(resource)
    if block_node is None:
        return ResourceNodeSuggestion.objects.create(
            resource=resource, node=None, status=ResourceNodeSuggestion.STATUS_SIN_BLOQUE,
        )

    scored_candidates = find_candidate_leaf_nodes(block_node, resource)
    if not scored_candidates:
        return ResourceNodeSuggestion.objects.create(
            resource=resource, node=None, status=ResourceNodeSuggestion.STATUS_SIN_BLOQUE,
        )

    top_candidate = scored_candidates[0][0]
    alternatives = [pair[0] for pair in scored_candidates[1:3]]

    ai_result = corroborate_with_ai(resource, top_candidate, alternatives)
    if ai_result:
        node = ai_result["node"]
        ai_corrigio = ai_result["ai_corrigio"]
        ai_rationale = ai_result["ai_rationale"]
    else:
        node = top_candidate
        ai_corrigio = False
        ai_rationale = ""

    return ResourceNodeSuggestion.objects.create(
        resource=resource,
        node=node,
        status=ResourceNodeSuggestion.STATUS_SUGERIDO,
        ai_rationale=ai_rationale,
        ai_corrigio=ai_corrigio,
        origen=ResourceNodeSuggestion.ORIGEN_IA,
    )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/Scripts/python.exe manage.py test apps.content.tests.test_node_matching_service -v 2`
Expected: `Ran 12 tests ... OK`

- [ ] **Step 5: Commit**

```bash
git add apps/content/services/node_matching_service.py apps/content/tests/test_node_matching_service.py
git commit -m "feat(content): paso 3 (corroboracion IA) y orquestador generate_suggestion"
```

---

### Task 5: Comando `suggest_resource_node_links`

**Files:**
- Create: `apps/content/management/commands/suggest_resource_node_links.py`
- Test: `apps/content/tests/test_suggest_resource_node_links.py`

**Interfaces:**
- Consumes: `generate_suggestion(resource)` (Task 4).
- Produces: comando invocable con `call_command("suggest_resource_node_links")`; usado manualmente o por barrido periódico (no por este plan — la programación del barrido es decisión operativa del usuario, fuera de alcance de código).

- [ ] **Step 1: Write the failing test**

```python
# apps/content/tests/test_suggest_resource_node_links.py
from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase

from apps.content.models import (
    Area, KnowledgeNode, Resource, ResourceNodeSuggestion, Subject, Topic,
)


def _node(sid, code, name, node_type):
    return KnowledgeNode.objects.create(
        semantic_id=sid, code=code, node_type=node_type, subject_abbr="MAT", name=name,
    )


class SuggestResourceNodeLinksCommandTests(TestCase):
    def setUp(self):
        area = Area.objects.create(name="Ciencias")
        subject = Subject.objects.create(name="Matemática Escolar", area=area)
        self.topic = Topic.objects.create(subject=subject, name="Fracciones")
        _node("MAT.FRAC", "01.03", "Fracciones", KnowledgeNode.NODE_BLOQUE)
        _node("MAT.FRAC.PROPIA", "01.03.01", "Fracción propia", KnowledgeNode.NODE_RECURSO)

    def test_processes_unpublished_resources_only(self):
        Resource.objects.create(title="Borrador", topic=self.topic, is_published=False)
        call_command("suggest_resource_node_links", stdout=StringIO())
        self.assertEqual(ResourceNodeSuggestion.objects.count(), 0)

    def test_skips_resources_with_existing_suggestion(self):
        resource = Resource.objects.create(title="Fracción propia", topic=self.topic, is_published=True)
        ResourceNodeSuggestion.objects.create(resource=resource, node=None, status="sin_bloque")
        call_command("suggest_resource_node_links", stdout=StringIO())
        self.assertEqual(ResourceNodeSuggestion.objects.filter(resource=resource).count(), 1)

    @patch("apps.content.services.node_matching_service.call_ai_structured_json")
    def test_generates_suggestion_for_new_published_resource(self, mock_call):
        mock_call.side_effect = ValueError("sin llaves en test")
        resource = Resource.objects.create(title="Fracción propia", topic=self.topic, is_published=True)
        out = StringIO()
        call_command("suggest_resource_node_links", stdout=out)
        self.assertEqual(ResourceNodeSuggestion.objects.filter(resource=resource).count(), 1)
        self.assertIn("Sugerencias generadas: 1", out.getvalue())

    def test_continues_after_error_in_one_resource(self):
        ok_resource = Resource.objects.create(title="Fracción propia", topic=self.topic, is_published=True)
        broken_resource = Resource.objects.create(title="Otra", topic=self.topic, is_published=True)

        original = None
        import apps.content.services.node_matching_service as svc
        original = svc.generate_suggestion

        def flaky(resource):
            if resource.pk == broken_resource.pk:
                raise RuntimeError("fallo simulado")
            return original(resource)

        with patch("apps.content.management.commands.suggest_resource_node_links.generate_suggestion", side_effect=flaky):
            err = StringIO()
            call_command("suggest_resource_node_links", stdout=StringIO(), stderr=err)

        self.assertEqual(ResourceNodeSuggestion.objects.filter(resource=ok_resource).count(), 1)
        self.assertEqual(ResourceNodeSuggestion.objects.filter(resource=broken_resource).count(), 0)
        self.assertIn("fallo simulado", err.getvalue())
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/Scripts/python.exe manage.py test apps.content.tests.test_suggest_resource_node_links -v 2`
Expected: FAIL with `Unknown command: 'suggest_resource_node_links'`

- [ ] **Step 3: Write minimal implementation**

```python
# apps/content/management/commands/suggest_resource_node_links.py
from django.core.management.base import BaseCommand

from apps.content.models import Resource
from apps.content.services.node_matching_service import generate_suggestion


class Command(BaseCommand):
    help = (
        "Genera sugerencias de nodo de conocimiento (KnowledgeNode) para recursos "
        "(videos) publicados que aun no tienen ninguna ResourceNodeSuggestion."
    )

    def handle(self, *args, **options):
        resources = Resource.objects.filter(
            is_published=True,
            node_suggestion__isnull=True,
        )

        created = 0
        skipped = 0
        for resource in resources:
            try:
                generate_suggestion(resource)
                created += 1
            except Exception as exc:
                skipped += 1
                self.stderr.write(f"Error en recurso {resource.pk} ({resource.title}): {exc}")

        self.stdout.write(
            self.style.SUCCESS(f"Sugerencias generadas: {created}. Con error: {skipped}.")
        )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/Scripts/python.exe manage.py test apps.content.tests.test_suggest_resource_node_links -v 2`
Expected: `Ran 4 tests ... OK`

- [ ] **Step 5: Commit**

```bash
git add apps/content/management/commands/suggest_resource_node_links.py apps/content/tests/test_suggest_resource_node_links.py
git commit -m "feat(content): comando suggest_resource_node_links"
```

---

### Task 6: Vistas de revisión (confirmar/descartar/autocompletado) + URLs

**Files:**
- Create: `apps/content/views/node_suggestions.py`
- Modify: `apps/content/urls/publish_urls.py`
- Test: `apps/content/tests/test_node_suggestions_views.py`

**Interfaces:**
- Consumes: `ResourceNodeSuggestion`, `KnowledgeNode`, `apps.content.views.permissions.is_admin`.
- Produces: vistas `node_suggestions_review`, `confirm_node_suggestion`, `discard_node_suggestion`, `node_options`; URLs `content:node_suggestions_review`, `content:confirm_node_suggestion`, `content:discard_node_suggestion`, `content:node_options`. Usado por Task 7 (template).

- [ ] **Step 1: Write the failing test**

```python
# apps/content/tests/test_node_suggestions_views.py
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.content.models import (
    Area, KnowledgeNode, Resource, ResourceNodeSuggestion, Subject, Topic,
)

User = get_user_model()


def _node(sid, code, name, node_type):
    return KnowledgeNode.objects.create(
        semantic_id=sid, code=code, node_type=node_type, subject_abbr="MAT", name=name,
    )


class NodeSuggestionsViewsTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="password123",
        )
        self.student = User.objects.create_user(username="alumno", password="password123")

        area = Area.objects.create(name="Ciencias")
        subject = Subject.objects.create(name="Matemática Escolar", area=area)
        topic = Topic.objects.create(subject=subject, name="Fracciones")
        self.resource = Resource.objects.create(title="Fracción propia", topic=topic, is_published=True)
        self.node = _node("MAT.A", "01.03.01.01", "Fracción propia", KnowledgeNode.NODE_RECURSO)
        self.other_node = _node("MAT.B", "01.03.01.02", "Fracción impropia", KnowledgeNode.NODE_RECURSO)
        self.suggestion = ResourceNodeSuggestion.objects.create(
            resource=self.resource, node=self.node, status=ResourceNodeSuggestion.STATUS_SUGERIDO,
        )

    def test_review_requires_staff(self):
        self.client.login(username="alumno", password="password123")
        response = self.client.get(reverse("content:node_suggestions_review"))
        self.assertEqual(response.status_code, 302)

    def test_review_lists_pending_suggestions(self):
        self.client.login(username="admin", password="password123")
        response = self.client.get(reverse("content:node_suggestions_review"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fracción propia")

    def test_confirm_automatic_suggestion(self):
        self.client.login(username="admin", password="password123")
        response = self.client.post(
            reverse("content:confirm_node_suggestion", args=[self.suggestion.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.suggestion.refresh_from_db()
        self.assertEqual(self.suggestion.status, ResourceNodeSuggestion.STATUS_CONFIRMADO)
        self.assertEqual(self.suggestion.origen, ResourceNodeSuggestion.ORIGEN_IA)
        self.assertIsNotNone(self.suggestion.confirmed_at)

    def test_confirm_manual_override(self):
        self.client.login(username="admin", password="password123")
        response = self.client.post(
            reverse("content:confirm_node_suggestion", args=[self.suggestion.pk]),
            {"node_id": self.other_node.pk},
        )
        self.assertEqual(response.status_code, 200)
        self.suggestion.refresh_from_db()
        self.assertEqual(self.suggestion.node, self.other_node)
        self.assertEqual(self.suggestion.origen, ResourceNodeSuggestion.ORIGEN_MANUAL)

    def test_discard_suggestion(self):
        self.client.login(username="admin", password="password123")
        response = self.client.post(
            reverse("content:discard_node_suggestion", args=[self.suggestion.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.suggestion.refresh_from_db()
        self.assertEqual(self.suggestion.status, ResourceNodeSuggestion.STATUS_DESCARTADO)

    def test_node_options_filters_by_query(self):
        self.client.login(username="admin", password="password123")
        response = self.client.get(reverse("content:node_options"), {"q": "impropia"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["nodes"]), 1)
        self.assertIn("Fracción impropia", data["nodes"][0]["label"])

    def test_node_options_empty_query_returns_empty(self):
        self.client.login(username="admin", password="password123")
        response = self.client.get(reverse("content:node_options"))
        self.assertEqual(response.json()["nodes"], [])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/Scripts/python.exe manage.py test apps.content.tests.test_node_suggestions_views -v 2`
Expected: FAIL with `NoReverseMatch: 'node_suggestions_review' is not a registered namespace`

- [ ] **Step 3: Write the views**

```python
# apps/content/views/node_suggestions.py
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from apps.content.models import KnowledgeNode, ResourceNodeSuggestion
from apps.content.views.permissions import is_admin


@user_passes_test(is_admin)
def node_suggestions_review(request):
    pending = (
        ResourceNodeSuggestion.objects.filter(
            status__in=[
                ResourceNodeSuggestion.STATUS_SUGERIDO,
                ResourceNodeSuggestion.STATUS_SIN_BLOQUE,
            ]
        )
        .select_related("resource", "node")
        .order_by("-created_at")
    )
    return render(
        request, "pages/node_suggestions_review.html", {"suggestions": pending},
    )


@user_passes_test(is_admin)
@require_POST
def confirm_node_suggestion(request, suggestion_id):
    suggestion = get_object_or_404(ResourceNodeSuggestion, pk=suggestion_id)
    manual_node_id = request.POST.get("node_id")

    if manual_node_id:
        node = get_object_or_404(
            KnowledgeNode, pk=manual_node_id, node_type=KnowledgeNode.NODE_RECURSO,
        )
        suggestion.node = node
        suggestion.origen = ResourceNodeSuggestion.ORIGEN_MANUAL
    elif suggestion.node:
        suggestion.origen = ResourceNodeSuggestion.ORIGEN_IA
    else:
        return HttpResponse("No hay nodo para confirmar sin selección manual.", status=400)

    suggestion.status = ResourceNodeSuggestion.STATUS_CONFIRMADO
    suggestion.confirmed_at = timezone.now()
    suggestion.save()
    return HttpResponse("")


@user_passes_test(is_admin)
@require_POST
def discard_node_suggestion(request, suggestion_id):
    suggestion = get_object_or_404(ResourceNodeSuggestion, pk=suggestion_id)
    suggestion.status = ResourceNodeSuggestion.STATUS_DESCARTADO
    suggestion.save()
    return HttpResponse("")


@user_passes_test(is_admin)
def node_options(request):
    query = request.GET.get("q", "").strip()
    if not query:
        return JsonResponse({"nodes": []})

    nodes = KnowledgeNode.objects.filter(
        node_type=KnowledgeNode.NODE_RECURSO,
    ).filter(
        Q(name__icontains=query) | Q(code__icontains=query)
    )[:20]

    data = [{"id": n.id, "label": f"{n.code} — {n.name}"} for n in nodes]
    return JsonResponse({"nodes": data})
```

- [ ] **Step 4: Wire URLs**

En `apps/content/urls/publish_urls.py`, agregar el import (después del bloque de `structured_activation`):

```python
from apps.content.views.node_suggestions import (
    node_suggestions_review,
    confirm_node_suggestion,
    discard_node_suggestion,
    node_options,
)
```

Y agregar al final de `urlpatterns` (antes del `]` de cierre):

```python
    # Enlace cruzado Sistema A (Resource) <-> Sistema B (KnowledgeNode)
    path("publicar/sugerencias-nodos/", node_suggestions_review, name="node_suggestions_review"),
    path(
        "publicar/sugerencias-nodos/<int:suggestion_id>/confirmar/",
        confirm_node_suggestion,
        name="confirm_node_suggestion",
    ),
    path(
        "publicar/sugerencias-nodos/<int:suggestion_id>/descartar/",
        discard_node_suggestion,
        name="discard_node_suggestion",
    ),
    path("publicar/opciones/nodos/", node_options, name="node_options"),
```

- [ ] **Step 5: Create a minimal template so the view resolves**

```html
{# templates/pages/node_suggestions_review.html #}
{% extends "base.html" %}
{% block title %}Sugerencias de Nodos | ProfeOnline{% endblock %}
{% block content %}
<h1>Sugerencias de Nodos</h1>
<ul>
  {% for suggestion in suggestions %}
    <li>{{ suggestion.resource.title }} — {{ suggestion.node.name|default:"(sin bloque)" }}</li>
  {% endfor %}
</ul>
{% endblock %}
```

(Nota: esta plantilla mínima se reemplaza por la versión completa en la Task 7 — se crea acá solo para que la vista renderice y el test del Step 6 pase.)

- [ ] **Step 6: Run test to verify it passes**

Run: `.venv/Scripts/python.exe manage.py test apps.content.tests.test_node_suggestions_views -v 2`
Expected: `Ran 7 tests ... OK`

- [ ] **Step 7: Commit**

```bash
git add apps/content/views/node_suggestions.py apps/content/urls/publish_urls.py apps/content/tests/test_node_suggestions_views.py templates/pages/node_suggestions_review.html
git commit -m "feat(content): vistas de revision, confirmacion manual y autocompletado de nodos"
```

---

### Task 7: Template completo de revisión + link en menú admin

**Files:**
- Modify: `templates/pages/node_suggestions_review.html`
- Modify: `templates/base.html:117-125`

**Interfaces:**
- Consumes: `content:confirm_node_suggestion`, `content:discard_node_suggestion`, `content:node_options` (Task 6).

- [ ] **Step 1: Reemplazar la plantilla mínima por la versión completa**

```html
{# templates/pages/node_suggestions_review.html #}
{% extends "base.html" %}
{% load static %}

{% block title %}Sugerencias de Nodos | ProfeOnline{% endblock %}

{% block content %}
<div class="container" style="max-width: 900px; margin: 40px auto; padding: 0 20px;">
    <h1>Sugerencias de conexión Recurso ↔ Nodo</h1>
    <p style="color: #94a3b8; margin-bottom: 24px;">
        Revisa a qué nodo del árbol de conocimiento corresponde cada video. Confirma la
        sugerencia automática, busca uno manual, o descarta si no aplica.
    </p>

    {% if not suggestions %}
        <p>No hay sugerencias pendientes.</p>
    {% endif %}

    {% for suggestion in suggestions %}
    <div id="suggestion-{{ suggestion.pk }}" class="card mb-3" style="border: 1px solid #334155; border-radius: 8px; padding: 16px; margin-bottom: 16px;">
        <h3 style="margin: 0 0 8px 0;">{{ suggestion.resource.title }}</h3>
        <p style="margin: 0 0 4px 0; font-size: 0.85rem; color: #94a3b8;">
            Tema: {{ suggestion.resource.topic.name|default:"(sin tema)" }}
        </p>

        {% if suggestion.node %}
            <p style="margin: 8px 0;">
                <strong>Sugerencia automática:</strong> {{ suggestion.node.code }} — {{ suggestion.node.name }}
                {% if suggestion.ai_corrigio %}
                    <span style="color: #f59e0b;"> (la IA corrigió el candidato inicial — revisar con cuidado)</span>
                {% endif %}
            </p>
            {% if suggestion.ai_rationale %}
                <p style="margin: 0 0 8px 0; font-size: 0.9rem; color: #cbd5e1;">{{ suggestion.ai_rationale }}</p>
            {% endif %}
            <form hx-post="{% url 'content:confirm_node_suggestion' suggestion.pk %}"
                  hx-target="#suggestion-{{ suggestion.pk }}" hx-swap="outerHTML"
                  style="display: inline;">
                <button type="submit" class="btn btn-primary">Confirmar sugerencia</button>
            </form>
        {% else %}
            <p style="margin: 8px 0; color: #f59e0b;">Sin bloque encontrado automáticamente.</p>
        {% endif %}

        <details style="margin-top: 12px;">
            <summary style="cursor: pointer;">Buscar nodo manualmente</summary>
            <div style="margin-top: 8px;">
                <input type="text" placeholder="Buscar por nombre o código..."
                       hx-get="{% url 'content:node_options' %}"
                       hx-trigger="keyup changed delay:300ms"
                       hx-target="#node-results-{{ suggestion.pk }}"
                       name="q" class="form-control" style="max-width: 400px;">
                <div id="node-results-{{ suggestion.pk }}" style="margin-top: 8px;"></div>
            </div>
        </details>

        <form hx-post="{% url 'content:discard_node_suggestion' suggestion.pk %}"
              hx-target="#suggestion-{{ suggestion.pk }}" hx-swap="outerHTML"
              style="display: inline; margin-top: 8px;">
            <button type="submit" class="btn btn-secondary">Descartar</button>
        </form>
    </div>
    {% endfor %}
</div>
{% endblock %}
```

- [ ] **Step 2: Template del resultado del autocompletado (respuesta JSON consumida a mano)**

El endpoint `node_options` devuelve JSON, no HTML — se consume con un pequeño script inline para pintar botones clicables. Agregar antes de `{% endblock %}` en el mismo archivo:

```html
<script nonce="{{ csp_nonce }}">
document.body.addEventListener('htmx:afterRequest', function (evt) {
    if (!evt.detail.pathInfo || !evt.detail.pathInfo.requestPath.includes('/opciones/nodos/')) return;
    var target = evt.detail.target;
    try {
        var data = JSON.parse(evt.detail.xhr.responseText);
        target.innerHTML = '';
        data.nodes.forEach(function (node) {
            var btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'btn btn-sm';
            btn.textContent = node.label;
            btn.style.marginRight = '6px';
            btn.style.marginBottom = '6px';
            btn.addEventListener('click', function () {
                var form = target.closest('.card').querySelector('form[hx-post*="confirmar"]');
                var hidden = form.querySelector('input[name="node_id"]');
                if (!hidden) {
                    hidden = document.createElement('input');
                    hidden.type = 'hidden';
                    hidden.name = 'node_id';
                    form.appendChild(hidden);
                }
                hidden.value = node.id;
                form.querySelector('button[type="submit"]').textContent = 'Confirmar: ' + node.label;
            });
            target.appendChild(btn);
        });
    } catch (e) { /* respuesta no-JSON, ignorar */ }
});
</script>
```

- [ ] **Step 3: Agregar el link en el menú de administrador**

En `templates/base.html`, reemplazar:

```html
                                    <a href="{% url 'content:learning_guide_review' %}">Guías ProfeOnline</a>
                                    <a href="{% url 'core:analytics_dashboard' %}">Analítica</a>
```

por:

```html
                                    <a href="{% url 'content:learning_guide_review' %}">Guías ProfeOnline</a>
                                    <a href="{% url 'content:node_suggestions_review' %}">Sugerencias de Nodos</a>
                                    <a href="{% url 'core:analytics_dashboard' %}">Analítica</a>
```

- [ ] **Step 4: Verificar manualmente en navegador**

Levantar el servidor local, loguearse como superusuario, ir a "Opciones de Administrador" → "Sugerencias de Nodos", confirmar que la página carga sin error 500 y que el link aparece en el menú.

- [ ] **Step 5: Run full content test suite to check no regression**

Run: `.venv/Scripts/python.exe manage.py test apps.content -v 1`
Expected: `OK` (mismo número de tests que antes de este plan + los nuevos de las tasks 1-6)

- [ ] **Step 6: Commit**

```bash
git add templates/pages/node_suggestions_review.html templates/base.html
git commit -m "feat(content): plantilla completa de revision de sugerencias + link en menu admin"
```

---

### Task 8: "Ver también" en `resource_detail.html`

**Files:**
- Modify: `apps/content/views/resource_detail.py`
- Modify: `templates/pages/resource_detail.html:102`
- Test: `apps/content/tests/test_bank_analytics.py` → nuevo archivo `apps/content/tests/test_resource_node_cross_link.py`

**Interfaces:**
- Consumes: `ResourceNodeSuggestion` (Task 1), `KnowledgeNode` propiedades `asignatura_slug`/`eje_slug`/`bloque_slug`/`tema_slug`/`slug` (ya existentes en `apps/content/models/knowledge.py`).

- [ ] **Step 1: Write the failing test**

```python
# apps/content/tests/test_resource_node_cross_link.py
from django.test import TestCase
from django.urls import reverse

from apps.content.models import (
    Area, KnowledgeNode, Resource, ResourceNodeSuggestion, Subject, Topic,
)


def _chain(subject_abbr="MAT"):
    asignatura = KnowledgeNode.objects.create(
        semantic_id="MAT", code="00", node_type=KnowledgeNode.NODE_ASIGNATURA,
        subject_abbr=subject_abbr, name="Matemáticas",
    )
    eje = KnowledgeNode.objects.create(
        semantic_id="MAT.FUND", code="01", node_type=KnowledgeNode.NODE_EJE,
        subject_abbr=subject_abbr, name="Fundamentos", parent=asignatura,
    )
    bloque = KnowledgeNode.objects.create(
        semantic_id="MAT.FUND.FRAC", code="01.03", node_type=KnowledgeNode.NODE_BLOQUE,
        subject_abbr=subject_abbr, name="Fracciones", parent=eje,
    )
    tema = KnowledgeNode.objects.create(
        semantic_id="MAT.FUND.FRAC.T1", code="01.03.01", node_type=KnowledgeNode.NODE_TEMA,
        subject_abbr=subject_abbr, name="Fracciones básicas", parent=bloque,
    )
    recurso = KnowledgeNode.objects.create(
        semantic_id="MAT.FUND.FRAC.T1.PROPIA", code="01.03.01.01", node_type=KnowledgeNode.NODE_RECURSO,
        subject_abbr=subject_abbr, name="Fracción propia", parent=tema, is_published=True,
    )
    return recurso


class ResourceDetailCrossLinkTests(TestCase):
    def setUp(self):
        area = Area.objects.create(name="Ciencias")
        subject = Subject.objects.create(name="Matemática Escolar", area=area)
        topic = Topic.objects.create(subject=subject, name="Fracciones")
        self.resource = Resource.objects.create(
            title="Fracción propia", topic=topic, is_published=True,
        )
        self.node = _chain()

    def test_shows_cross_link_when_confirmed(self):
        ResourceNodeSuggestion.objects.create(
            resource=self.resource, node=self.node,
            status=ResourceNodeSuggestion.STATUS_CONFIRMADO,
        )
        response = self.client.get(reverse("content:resource_detail", args=[self.resource.slug]))
        self.assertContains(response, "Ver también")
        self.assertContains(response, "Fracción propia")

    def test_no_cross_link_without_confirmed_suggestion(self):
        ResourceNodeSuggestion.objects.create(
            resource=self.resource, node=self.node,
            status=ResourceNodeSuggestion.STATUS_SUGERIDO,
        )
        response = self.client.get(reverse("content:resource_detail", args=[self.resource.slug]))
        self.assertNotContains(response, "Ver también")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/Scripts/python.exe manage.py test apps.content.tests.test_resource_node_cross_link -v 2`
Expected: FAIL — `test_shows_cross_link_when_confirmed` falla porque "Ver también" no está en la respuesta.

- [ ] **Step 3: Agregar el contexto en la vista**

En `apps/content/views/resource_detail.py`, dentro de `get_context_data`, después del bloque de `learning_guide` (antes de `context["structured_data_json_list"]`):

```python
        # Enlace cruzado a Sistema B (KnowledgeNode), si hay una sugerencia confirmada.
        suggestion = getattr(resource, "node_suggestion", None)
        if suggestion and suggestion.status == suggestion.STATUS_CONFIRMADO and suggestion.node:
            context["related_node"] = suggestion.node
        else:
            context["related_node"] = None
```

- [ ] **Step 4: Agregar el bloque en el template**

En `templates/pages/resource_detail.html`, después de `{% include "includes/quiz_section.html" %}` (línea 102), agregar:

```html
        {% if related_node %}
            <section class="resource-related-node" style="margin: 24px 0; padding: 16px; border: 1px solid #334155; border-radius: 8px;">
                <p style="margin: 0 0 8px 0; font-size: 0.85rem; color: #94a3b8;">Ver también</p>
                <a href="{% url 'learn:recurso' asignatura_slug=related_node.asignatura_slug eje_slug=related_node.eje_slug bloque_slug=related_node.bloque_slug tema_slug=related_node.tema_slug recurso_slug=related_node.slug %}">
                    {{ related_node.name }} (guía interactiva en /aprender/)
                </a>
            </section>
        {% endif %}
```

- [ ] **Step 5: Run test to verify it passes**

Run: `.venv/Scripts/python.exe manage.py test apps.content.tests.test_resource_node_cross_link -v 2`
Expected: `Ran 2 tests ... OK`

- [ ] **Step 6: Commit**

```bash
git add apps/content/views/resource_detail.py templates/pages/resource_detail.html apps/content/tests/test_resource_node_cross_link.py
git commit -m "feat(content): enlace 'Ver tambien' de Resource hacia el nodo confirmado"
```

---

### Task 9: "Ver también" en `node_detail.html`

**Files:**
- Modify: `apps/learn/views.py:152-184` (`_recurso_view`)
- Modify: `templates/learn/node_detail.html:602`
- Test: `apps/learn/tests.py` → nueva clase en el mismo archivo

**Interfaces:**
- Consumes: `ResourceNodeSuggestion` reverse relation `node.resource_suggestions` (Task 1).

- [ ] **Step 1: Write the failing test**

Agregar al final de `apps/learn/tests.py`:

```python
from apps.content.models import (
    Area, Resource, ResourceNodeSuggestion, Subject, Topic,
)


class NodeDetailCrossLinkTests(TestCase):
    def setUp(self):
        self.node = KnowledgeNode.objects.create(
            semantic_id="MAT.FUND.FRAC.T1.PROPIA", code="01.03.01.01",
            node_type=KnowledgeNode.NODE_RECURSO, subject_abbr="MAT",
            name="Fracción propia", is_published=True,
        )
        area = Area.objects.create(name="Ciencias")
        subject = Subject.objects.create(name="Matemática Escolar", area=area)
        topic = Topic.objects.create(subject=subject, name="Fracciones")
        self.resource = Resource.objects.create(
            title="Video de fracción propia", topic=topic, is_published=True, slug="video-fraccion-propia",
        )

    def test_shows_cross_link_when_confirmed(self):
        ResourceNodeSuggestion.objects.create(
            resource=self.resource, node=self.node,
            status=ResourceNodeSuggestion.STATUS_CONFIRMADO,
        )
        response = self.client.get(f"/aprender/{self.node.slug}/")
        self.assertContains(response, "Ver también")
        self.assertContains(response, "Video de fracción propia")

    def test_no_cross_link_without_confirmed_suggestion(self):
        response = self.client.get(f"/aprender/{self.node.slug}/")
        self.assertNotContains(response, "Ver también")
```

Nota: usar la ruta directa `/aprender/{slug}/` (como ya hace el resto de `apps/learn/tests.py`, que resuelve el nodo por su slug más profundo sin depender de la jerarquía completa en la URL) en vez de `reverse("learn:recurso", ...)`.

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/Scripts/python.exe manage.py test apps.learn.tests.NodeDetailCrossLinkTests -v 2`
Expected: FAIL — no aparece "Ver también" en la respuesta.

- [ ] **Step 3: Agregar el contexto en la vista**

En `apps/learn/views.py`, la función `_recurso_view` hoy termina así:

```python
def _recurso_view(request, node, breadcrumbs, prerequisites):
    from apps.content.services.node_assessment_service import get_node_mastery

    content = getattr(node, "content", None)
    noindex = not node.is_published or content is None or content.is_draft

    youtube_id = None
    other_media = []
    for m in node.media.all():
        if (
            m.kind == NodeMedia.KIND_VIDEO_YOUTUBE
            and m.video_kind == NodeMedia.VIDEO_KIND_EXPLICACION
            and youtube_id is None
        ):
            youtube_id = _youtube_id(m.url)
        else:
            other_media.append(m)

    return render(
        request,
        "learn/node_detail.html",
        {
            "node": node,
            "content": content,
            "youtube_id": youtube_id,
            "other_media": other_media,
            "practice_bank": _build_practice_bank(node),
            "prerequisites": prerequisites,
            "breadcrumbs": breadcrumbs,
            "noindex": noindex,
            "mastery": get_node_mastery(request.user, node),
        },
    )
```

Reemplazar por (agrega el cálculo de `related_resource` y la entrada correspondiente en el dict de contexto, todo lo demás igual):

```python
def _recurso_view(request, node, breadcrumbs, prerequisites):
    from apps.content.services.node_assessment_service import get_node_mastery

    content = getattr(node, "content", None)
    noindex = not node.is_published or content is None or content.is_draft

    youtube_id = None
    other_media = []
    for m in node.media.all():
        if (
            m.kind == NodeMedia.KIND_VIDEO_YOUTUBE
            and m.video_kind == NodeMedia.VIDEO_KIND_EXPLICACION
            and youtube_id is None
        ):
            youtube_id = _youtube_id(m.url)
        else:
            other_media.append(m)

    confirmed_suggestion = (
        node.resource_suggestions.filter(status="confirmado")
        .select_related("resource")
        .first()
    )
    related_resource = confirmed_suggestion.resource if confirmed_suggestion else None

    return render(
        request,
        "learn/node_detail.html",
        {
            "node": node,
            "content": content,
            "youtube_id": youtube_id,
            "other_media": other_media,
            "practice_bank": _build_practice_bank(node),
            "prerequisites": prerequisites,
            "breadcrumbs": breadcrumbs,
            "noindex": noindex,
            "mastery": get_node_mastery(request.user, node),
            "related_resource": related_resource,
        },
    )
```

- [ ] **Step 4: Agregar el bloque en el template**

En `templates/learn/node_detail.html`, después de `</section>` que cierra `assessment-section-root` (línea 602), agregar:

```html
    {% if related_resource %}
    <section class="learn-section">
        <p style="margin: 0 0 8px 0; font-size: 0.85rem; color: #94a3b8;">Ver también</p>
        <a href="{% url 'content:resource_detail' related_resource.slug %}">
            {{ related_resource.title }} (video en la biblioteca de recursos)
        </a>
    </section>
    {% endif %}
```

- [ ] **Step 5: Run test to verify it passes**

Run: `.venv/Scripts/python.exe manage.py test apps.learn.tests.NodeDetailCrossLinkTests -v 2`
Expected: `Ran 2 tests ... OK`

- [ ] **Step 6: Run full apps.learn and apps.content suites (no regression)**

Run: `.venv/Scripts/python.exe manage.py test apps.learn apps.content -v 1`
Expected: `OK`

- [ ] **Step 7: Commit**

```bash
git add apps/learn/views.py templates/learn/node_detail.html apps/learn/tests.py
git commit -m "feat(learn): enlace 'Ver tambien' del nodo hacia el recurso confirmado"
```

---

## Verificación final (antes de push)

- [ ] Run: `.venv/Scripts/python.exe manage.py test` (suite completa, ~6 min, regla del proyecto: correr solo una vez, antes de pushear)
- [ ] Run: `.venv/Scripts/python.exe manage.py check --deploy`
- [ ] Run: `.venv/Scripts/python.exe manage.py makemigrations --check` (confirmar que no quedó ninguna migración pendiente sin generar)
- [ ] Verificar manualmente en navegador local: subir/crear un `Resource` de prueba con un `Topic` cuyo nombre calce con un bloque real del árbol, correr `python manage.py suggest_resource_node_links`, confirmar la sugerencia en `/publicar/sugerencias-nodos/`, y verificar que el link "Ver también" aparece en ambos lados.
