from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0035_learningguide_originality_checked_at_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="topic",
            name="structured_bank_staging",
            field=models.BooleanField(
                default=False,
                help_text=(
                    "Permite preparar/clasificar el banco estructurado del tema en los "
                    "paneles admin SIN exponerlo a los alumnos. La activación real "
                    "(encender el flag) la hace el gate."
                ),
                verbose_name="banco estandarizado en preparación",
            ),
        ),
    ]
