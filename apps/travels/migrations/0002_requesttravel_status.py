# Generated by Django 4.2.7 on 2023-12-13 15:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("travels", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="requesttravel",
            name="status",
            field=models.CharField(
                choices=[("P", "Pending"), ("T", "Taked")],
                default="P",
                max_length=1,
                verbose_name="request travel's status",
            ),
        ),
    ]