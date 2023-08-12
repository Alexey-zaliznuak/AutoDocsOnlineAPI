import pandas as pd
from os import getenv as env
from django.core.management.base import BaseCommand
from users.models import User
from documents.models import Template
from pathlib import PurePath

DATA_DIR = PurePath(__file__).parent / 'data'
ROWS_NAMES_INDEX = 1


def loadcsv(file_name: str):
    return pd.read_csv(f'{file_name}.csv', index_col=False, keep_default_na=False)

def check_admin_exists():
    if not User.objects.filter(
        username=env('DJANGO_SUPERUSER_USERNAME')
    ).exists():
        raise RuntimeError('Administartor user not found.')

def clear_row(row):
    if not row or not isinstance(row, str):
        return row

    _ = ['"', "'"]
    if row[0] in _:
        row = row[1:]
    if row[-1] in _:
        row = row[:-1]

    return row


class Command(BaseCommand):
    objects_list = ['templates']

    def handle(self, **options):
        check_admin_exists()

        for obj in self.objects_list:
            if obj in options.keys():
                self.__getattribute__('load_' + obj)()
                print(f'import {obj} completed successfully')

    def add_arguments(self, parser):
        for obj in self.objects_list:
            parser.add_argument(
                f'--{obj}',
                action='store_true',
                default=False,
                help=f'load {obj} data'
            )

    def load_model(self, model, csv_path = None):
        "For easy loads simple models."

        csv = loadcsv(csv_path or DATA_DIR / model.__class__.__name__.lower())
        rows_names = csv.axes[ROWS_NAMES_INDEX]

        data = [
            model(
                **{key: clear_row(row[key]) for key in rows_names}
            )
            for _, row in csv.iterrows()
        ]
        model.objects.bulk_create(data)

    def load_templates(self):
        csv = loadcsv(DATA_DIR / 'templates')
        rows_names = csv.axes[ROWS_NAMES_INDEX]

        def get_row_data(row, key):
            if key == 'author':
                return User.objects.get(username=row[key])

            if key == 'description' and not row[key]:
                return row['title']

            return row[key]

        data = [
            Template(
                **{
                    key: clear_row(get_row_data(row, key))
                    for key in rows_names
                }
            )
            for _, row in csv.iterrows()
        ]

        Template.objects.bulk_create(data)
