# Generated by Django 4.2.2 on 2023-09-01 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_prizes"),
    ]

    operations = [
        migrations.AlterField(
            model_name="prizes",
            name="a_prize",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="prizes",
            name="f_prize",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="prizes",
            name="r_prize",
            field=models.CharField(max_length=50),
        ),
    ]
