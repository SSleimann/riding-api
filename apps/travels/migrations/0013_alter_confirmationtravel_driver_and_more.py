# Generated by Django 4.2.7 on 2024-02-03 16:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("drivers", "0003_alter_vehicles_driver_alter_vehicles_year"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("travels", "0012_confirmationtravel_check_driver_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="confirmationtravel",
            name="driver",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="confirmations",
                to="drivers.drivers",
            ),
        ),
        migrations.AlterField(
            model_name="confirmationtravel",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="confirmations",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="travel",
            name="request_travel",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="travel",
                to="travels.requesttravel",
            ),
        ),
        migrations.AlterField(
            model_name="travel",
            name="vehicle",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="travels",
                to="drivers.vehicles",
            ),
        ),
    ]