# Generated by Django 5.1.6 on 2025-03-26 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('POJOS', '0008_alter_bestofimportedjewellery_pojos'),
    ]

    operations = [
        migrations.AddField(
            model_name='pojos',
            name='sku',
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True, unique=True),
        ),
    ]
