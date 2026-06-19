import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0028_resource_transcript"),
    ]

    operations = [
        migrations.AddField(
            model_name="quizguide",
            name="canonical_resource",
            field=models.OneToOneField(
                blank=True,
                help_text="Recurso cuya transcripción originó esta guía canónica.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="canonical_quiz_guide",
                to="content.resource",
                verbose_name="recurso canónico",
            ),
        ),
        migrations.CreateModel(
            name="PublicationItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("batch_id", models.CharField(max_length=64)),
                ("source_filename", models.CharField(max_length=255)),
                ("youtube_video_id", models.CharField(blank=True, max_length=32)),
                ("youtube_url", models.URLField(blank=True)),
                ("youtube_privacy", models.CharField(default="unlisted", max_length=20)),
                ("state", models.CharField(choices=[("uploaded", "Subido"), ("transcript_pending", "Transcripción pendiente"), ("context_ready", "Contexto listo"), ("metadata_ready", "Metadatos listos"), ("questions_ready", "Preguntas listas"), ("published", "Publicado"), ("failed", "Fallido")], default="uploaded", max_length=24)),
                ("resume_state", models.CharField(blank=True, max_length=24)),
                ("taxonomy", models.JSONField(blank=True, default=dict)),
                ("instructions", models.TextField(blank=True)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("target_counts", models.JSONField(blank=True, default=dict)),
                ("last_error", models.TextField(blank=True)),
                ("attempts", models.PositiveSmallIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("canonical_guide", models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="publication_item", to="content.quizguide")),
                ("resource", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="publication_items", to="content.resource")),
            ],
            options={"ordering": ["created_at", "id"]},
        ),
        migrations.AddConstraint(
            model_name="publicationitem",
            constraint=models.UniqueConstraint(fields=("batch_id", "source_filename"), name="unique_publication_batch_file"),
        ),
        migrations.AddField(
            model_name="question",
            name="audit_data",
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name="question",
            name="generation_key",
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AddField(
            model_name="question",
            name="publication_item",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="questions", to="content.publicationitem"),
        ),
        migrations.AddConstraint(
            model_name="question",
            constraint=models.UniqueConstraint(condition=models.Q(("generation_key", ""), _negated=True), fields=("publication_item", "generation_key"), name="unique_pipeline_question_key"),
        ),
    ]
