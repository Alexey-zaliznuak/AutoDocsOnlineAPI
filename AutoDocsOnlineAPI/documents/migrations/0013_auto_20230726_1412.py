# Generated by Django 3.2 on 2023-07-26 11:12

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documents', '0012_auto_20230725_2233'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentDocumentPackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentPackage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100, unique=True, validators=[django.core.validators.MinLengthValidator(3)])),
            ],
            options={
                'verbose_name': 'Documents package',
                'verbose_name_plural': 'Documents packages',
            },
        ),
        migrations.RemoveConstraint(
            model_name='document',
            name='author_title_unique',
        ),
        migrations.AddField(
            model_name='documentpackage',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documentpackage', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='documentpackage',
            name='documents',
            field=models.ManyToManyField(related_name='DocumentDocumentPackage', to='documents.Document'),
        ),
        migrations.AddField(
            model_name='documentdocumentpackage',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documentdocumentpackage', to='documents.document'),
        ),
        migrations.AddField(
            model_name='documentdocumentpackage',
            name='document_package',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documentdocumentpackage', to='documents.documentpackage'),
        ),
    ]
