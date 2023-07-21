# Generated by Django 3.2 on 2023-07-21 19:58

from django.db import migrations, models
import documents.validators


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='name_in_document',
            field=models.CharField(help_text="name in document, prefer save add prefix '{{'and postfix '}}'", max_length=30, unique=True, validators=[documents.validators.name_in_document_validator], verbose_name='template name in document'),
        ),
    ]
