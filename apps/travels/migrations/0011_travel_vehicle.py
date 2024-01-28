# Generated by Django 4.2.7 on 2024-01-25 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("drivers", "0003_alter_vehicles_driver_alter_vehicles_year"),
        ("travels", "0010_alter_travel_driver_alter_travel_request_travel_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="travel",
            name="vehicle",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="travels",
                to="drivers.vehicles",
            ),
        ),
    ]
