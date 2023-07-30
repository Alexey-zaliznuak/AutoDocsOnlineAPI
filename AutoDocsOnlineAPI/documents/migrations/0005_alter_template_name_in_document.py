# Generated by Django 3.2 on 2023-07-29 18:14

import django.core.validators
from django.db import migrations, models
import documents.validators


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0004_auto_20230728_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='name_in_document',
            field=models.CharField(help_text="name in document, prefer save add prefix '{{'and postfix '}}'", max_length=30, unique=True, validators=[documents.validators.validate_name_in_document, django.core.validators.MinLengthValidator(7)], verbose_name='template name in document'),
        ),
    ]