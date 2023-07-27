# Generated by Django 3.2 on 2023-07-27 14:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documents', '0002_auto_20230727_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='documentdocumentpackage',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='document_packages', to='documents.document'),
        ),
        migrations.AlterField(
            model_name='documentpackage',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='document_packages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='documenttemplate',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='documents.template'),
        ),
        migrations.AlterField(
            model_name='record',
            name='document_package',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to='documents.documentpackage'),
        ),
        migrations.AlterField(
            model_name='record',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='recordtemplatevalue',
            name='template_value',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to='documents.templatevalue'),
        ),
        migrations.AlterField(
            model_name='templatevalue',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='values', to='documents.template'),
        ),
        migrations.AlterField(
            model_name='userdefaulttemplatevalue',
            name='template_value',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='default_users_values', to='documents.templatevalue'),
        ),
        migrations.AlterField(
            model_name='userdefaulttemplatevalue',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='default_template_values', to=settings.AUTH_USER_MODEL),
        ),
    ]
