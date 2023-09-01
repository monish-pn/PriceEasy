# Generated by Django 4.2.2 on 2023-09-01 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Contact",
            fields=[
                ("s_no", models.AutoField(primary_key=True, serialize=False)),
                ("Name", models.CharField(max_length=255)),
                ("Email", models.CharField(max_length=20)),
                ("Content", models.TextField()),
            ],
        ),
    ]
