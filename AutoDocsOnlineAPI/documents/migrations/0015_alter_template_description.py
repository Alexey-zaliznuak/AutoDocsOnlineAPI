# Generated by Django 3.2 on 2023-07-27 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0014_alter_documentdocumentpackage_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='description',
            field=models.TextField(blank=True, max_length=500, verbose_name='description'),
        ),
    ]
