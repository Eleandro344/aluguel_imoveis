# Generated by Django 4.1.3 on 2024-09-24 21:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0003_conteudo_alter_registerlocation_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="Banner",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "imagem",
                    models.ImageField(
                        blank=True, null=True, upload_to="imagens/banners/"
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="Conteudo",
        ),
        migrations.AlterModelOptions(
            name="registerlocation",
            options={
                "ordering": ["-id"],
                "verbose_name": "Registrar Locação",
                "verbose_name_plural": "Registrar Locação",
            },
        ),
    ]
