from pathlib import Path
from django.conf import settings


def make_documents_directory_path(document, filename):
    return (
        f'{document.author.id}/{settings.DOCUMENTS_FOLDER_NAME}/{filename}'
    )
