# Generated by Django 4.2.7 on 2023-12-13 18:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("travels", "0003_alter_requesttravel_driver"),
    ]

    operations = [
        migrations.AlterField(
            model_name="requesttravel",
            name="created_time",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]