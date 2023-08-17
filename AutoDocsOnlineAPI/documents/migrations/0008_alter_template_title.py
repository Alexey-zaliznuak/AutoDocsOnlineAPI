# Generated by Django 3.2 on 2023-08-15 08:16

import django.core.validators
from django.db import migrations, models
import documents.validators


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0007_alter_template_name_in_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='title',
            field=models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(3), documents.validators.validate_title_not_same_in_official_templates], verbose_name='title'),
        ),
    ]