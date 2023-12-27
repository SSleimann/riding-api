# Generated by Django 4.2.7 on 2023-12-26 14:01

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("drivers", "0003_alter_vehicles_driver_alter_vehicles_year"),
        ("travels", "0005_remove_requesttravel_driver_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="requesttravel",
            name="expires",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="requesttravel",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="req_travels",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="Travel",
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
                    "origin",
                    django.contrib.gis.db.models.fields.PointField(
                        geography=True, srid=4326
                    ),
                ),
                (
                    "destination",
                    django.contrib.gis.db.models.fields.PointField(
                        geography=True, srid=4326
                    ),
                ),
                ("taked_date", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("D", "Done travel"),
                            ("I", "Travel in course"),
                            ("C", "Cancelled travel"),
                        ],
                        default="I",
                        max_length=1,
                        verbose_name="travels status",
                    ),
                ),
                (
                    "driver",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="travels",
                        to="drivers.drivers",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="travels",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]