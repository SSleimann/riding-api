# Generated by Django 4.2.7 on 2023-12-27 14:30

import apps.travels.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("travels", "0006_requesttravel_expires_alter_requesttravel_user_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="requesttravel",
            name="expires",
            field=models.DateTimeField(
                default=apps.travels.models.request_travel_exp_time
            ),
        ),
        migrations.AddConstraint(
            model_name="travel",
            constraint=models.CheckConstraint(
                check=models.Q(("user", models.F("driver")), _negated=True),
                name="prevent self traveling",
            ),
        ),
    ]
