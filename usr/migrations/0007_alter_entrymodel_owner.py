# Generated by Django 3.2.10 on 2022-01-10 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usr', '0006_entrymodel_pre_delete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrymodel',
            name='owner',
            field=models.EmailField(blank=True, max_length=330),
        ),
    ]
