# Generated by Django 5.1.6 on 2025-03-20 11:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('POJOS', '0002_alter_pojos_display_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pojos',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pojos', to='POJOS.category'),
        ),
    ]
