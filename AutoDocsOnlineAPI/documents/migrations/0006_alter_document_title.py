# Generated by Django 3.2 on 2023-07-30 14:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0005_alter_template_name_in_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='title',
            field=models.CharField(max_length=150, validators=[django.core.validators.MinLengthValidator(7)]),
        ),
    ]
