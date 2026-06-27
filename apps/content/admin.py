from django.contrib import admin
from django.contrib import messages
from django.template.response import TemplateResponse
from django.utils.html import format_html

from apps.content.services.ai_generation_service import generate_questions_for_resource
from apps.content.models import (
    Area,
    Choice,
    KnowledgeNode,
    Level,
    Module,
    NodePrerequisite,
    Question,
    QuestionErrorReport,
    QuizAttempt,
    Resource,
    Subject,
    Topic,
    TopicEvaluationAttempt,
    UserSkill,
    UserStreak,
    XPEvent,
)


@admin.register(KnowledgeNode)
class KnowledgeNodeAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "node_type",
        "name",
        "subject_abbr",
        "axis_abbr",
        "competencia",
        "is_published",
    )
    list_filter = (
        "node_type",
        "subject_abbr",
        "axis_abbr",
        "competencia",
        "dificultad",
        "is_published",
    )
    search_fields = ("semantic_id", "code", "name")
    raw_id_fields = ("parent",)
    ordering = ("subject_abbr", "code")
    list_per_page = 100


@admin.register(NodePrerequisite)
class NodePrerequisiteAdmin(admin.ModelAdmin):
    list_display = ("node", "requires", "kind", "min_mastery")
    list_filter = ("kind",)
    search_fields = ("node__semantic_id", "requires__semantic_id")
    raw_id_fields = ("node", "requires")


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "is_active")
    search_fields = ("name", "description")
    list_filter = ("is_active",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("order", "name")


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "area", "is_active")
    search_fields = ("name",)
    list_filter = ("area", "is_active")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "is_active")
    search_fields = ("name", "description")
    list_filter = ("subject", "is_active")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "is_active")
    search_fields = ("name", "description")
    list_filter = ("is_active",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("order", "name")


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "subject", "topic", "is_published", "created_at")
    search_fields = ("title", "description", "content")
    list_filter = ("subject", "topic", "is_published")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("levels",)
    actions = ["generar_preguntas_ia_action"]

    @admin.action(description="Generar preguntas con IA")
    def generar_preguntas_ia_action(self, request, queryset):
        # Si se envió la confirmación del formulario intermedio
        if "apply" in request.POST:
            try:
                levels = [int(v) for v in request.POST.getlist("levels") if v in ("1", "2", "3")]
                mode = request.POST.get("mode", "ambas")
                count = int(request.POST.get("count", 20))
            except (ValueError, TypeError):
                levels = [1, 2, 3]
                mode = "ambas"
                count = 20

            if not levels:
                levels = [1, 2, 3]

            success_count = 0
            for resource in queryset:
                resource_ok = True
                for level in levels:
                    try:
                        generate_questions_for_resource(
                            resource=resource,
                            level=level,
                            mode=mode,
                            count=count,
                        )
                    except Exception as e:
                        resource_ok = False
                        self.message_user(
                            request,
                            f"Error en '{resource.title}' nivel {level}: {e}",
                            level=messages.ERROR,
                        )
                if resource_ok:
                    success_count += 1

            if success_count > 0:
                niveles_str = ", ".join(f"N{l}" for l in levels)
                self.message_user(
                    request,
                    f"Se publicaron {count} preguntas × {len(levels)} niveles ({niveles_str}) para {success_count} recurso(s).",
                    level=messages.SUCCESS,
                )
            return None

        # Si no se ha enviado el formulario, renderizar la página intermedia
        context = {
            **self.admin_site.each_context(request),
            "queryset": queryset,
            "action_checkbox_name": admin.helpers.ACTION_CHECKBOX_NAME,
            "title": "Generar preguntas con IA",
        }
        return TemplateResponse(
            request,
            "admin/content/resource/generate_ai_questions_confirm.html",
            context,
        )


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("title", "subject", "topic", "order", "is_published", "created_at")
    search_fields = ("title", "objective", "description")
    list_filter = ("subject", "topic", "is_published")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("levels",)


# ---------------------------------------------------------------------------
# Evaluación gamificada
# ---------------------------------------------------------------------------


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4
    min_num = 2
    fields = ("text", "is_correct", "order")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("short_text", "resource", "level", "mode", "status", "choices_count")
    list_filter = ("level", "mode", "status", "resource__subject")
    search_fields = ("text", "resource__title")
    list_editable = ("status",)
    inlines = [ChoiceInline]
    raw_id_fields = ("resource",)
    ordering = ("resource", "level", "order")

    @admin.display(description="Enunciado")
    def short_text(self, obj):
        return obj.text[:100] + "…" if len(obj.text) > 100 else obj.text

    @admin.display(description="Alternativas")
    def choices_count(self, obj):
        return obj.choices.count()

    def has_change_permission(self, request, obj=None):
        if (
            obj
            and obj.scope in {"evaluacion_nivel", "prueba_final"}
            and obj.evaluation_sessions.exists()
        ):
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if (
            obj
            and obj.scope in {"evaluacion_nivel", "prueba_final"}
            and obj.evaluation_sessions.exists()
        ):
            return False
        return super().has_delete_permission(request, obj)


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "resource",
        "level",
        "mode",
        "score_display",
        "passed",
        "attempt_number",
        "created_at",
    )
    list_filter = ("passed", "level", "mode")
    search_fields = ("user__username", "resource__title")
    readonly_fields = (
        "user",
        "resource",
        "level",
        "mode",
        "score",
        "total",
        "passed",
        "attempt_number",
        "created_at",
    )
    ordering = ("-created_at",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    @admin.display(description="Puntaje")
    def score_display(self, obj):
        return f"{obj.score}/{obj.total}"


@admin.register(TopicEvaluationAttempt)
class TopicEvaluationAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "topic",
        "score_display",
        "percentage",
        "passed",
        "attempt_number",
        "created_at",
    )
    list_filter = ("passed", "topic__subject")
    search_fields = ("user__username", "topic__name")
    readonly_fields = (
        "user",
        "topic",
        "score",
        "total",
        "percentage",
        "passed",
        "attempt_number",
        "created_at",
    )
    ordering = ("-created_at",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    @admin.display(description="Puntaje")
    def score_display(self, obj):
        return f"{obj.score}/{obj.total}"


@admin.register(QuestionErrorReport)
class QuestionErrorReportAdmin(admin.ModelAdmin):
    list_display = (
        "short_question",
        "user",
        "reason",
        "status",
        "created_at",
    )
    list_filter = ("status", "reason")
    list_editable = ("status",)
    search_fields = ("question__text", "user__username", "comment")
    raw_id_fields = ("question", "user", "attempt")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)

    @admin.display(description="Pregunta")
    def short_question(self, obj):
        text = obj.question.text
        return text[:80] + "…" if len(text) > 80 else text


@admin.register(XPEvent)
class XPEventAdmin(admin.ModelAdmin):
    list_display = ("user", "event_type", "amount", "resource", "topic", "created_at")
    list_filter = ("event_type", "created_at")
    search_fields = ("user__username", "event_key", "resource__title", "topic__name")
    readonly_fields = (
        "user",
        "event_type",
        "amount",
        "event_key",
        "resource",
        "topic",
        "quiz_attempt",
        "topic_attempt",
        "metadata",
        "created_at",
    )
    ordering = ("-created_at",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "topic", "created_at")
    list_filter = ("topic__subject", "created_at")
    search_fields = ("user__username", "name", "topic__name")
    readonly_fields = ("user", "topic", "name", "unlocked_by_attempt", "created_at")
    ordering = ("-created_at",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(UserStreak)
class UserStreakAdmin(admin.ModelAdmin):
    list_display = ("user", "current_count", "longest_count", "last_activity_date")
    search_fields = ("user__username",)
    readonly_fields = (
        "user",
        "current_count",
        "longest_count",
        "last_activity_date",
        "updated_at",
    )
    ordering = ("-current_count",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
