# Generated by Django 3.2 on 2023-08-09 19:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0004_alter_record_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='record',
            options={'ordering': ['creation_date'], 'verbose_name': 'Record', 'verbose_name_plural': 'Records'},
        ),
    ]