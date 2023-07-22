# Generated by Django 3.2 on 2023-07-22 19:40

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='template',
            name='title',
            field=models.CharField(max_length=100, unique=True, verbose_name='title'),
        ),
    ]