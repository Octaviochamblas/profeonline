from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0025_resourcequizconfig"),
    ]

    operations = [
        migrations.AddField(
            model_name="topic",
            name="education_level",
            field=models.CharField(
                blank=True,
                choices=[
                    ("escolar", "Escolar (hasta 13 años)"),
                    ("media", "Media preuniversitaria (14-17 años)"),
                    ("universitaria", "Universitaria (18+)"),
                ],
                default="",
                max_length=20,
                verbose_name="nivel educativo",
            ),
        ),
    ]
