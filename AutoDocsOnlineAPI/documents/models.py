import uuid

from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models

from .validators import name_in_document_validator


class Template(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(
        "title",
        max_length=settings.TEMPLATE_TITLE_MAX_LENGTH,
        validators=[MinLengthValidator(settings.TEMPLATE_TITLE_MIN_LENGTH)],
        unique=True
    )
    name_in_document = models.CharField(
        "template name in document",
        unique=True,
        max_length=settings.TEMPLATE_NAME_IN_DOCUMENT_MAX_LENGTH,
        help_text=(
            "name in document, "
            f"prefer save add "
            f"prefix '{settings.TEMPLATE_NAME_IN_DOCUMENT_PREFIX}'"
            f"and postfix '{settings.TEMPLATE_NAME_IN_DOCUMENT_POSTFIX}'"
        ),
        validators=[
            name_in_document_validator,
            MinLengthValidator(settings.TEMPLATE_NAME_IN_DOCUMENT_MIN_LENGTH),
        ]
    )
    description = models.TextField(
        'description',
        unique=True,
        max_length=settings.TEMPLATE_DESCRIPTION_MAX_LENGTH
    )
    is_official = models.BooleanField(
        'official tag',
        blank=True,
        default=False,
    )

    class Meta:
        ordering = ["title"]
        verbose_name = 'Template'
        verbose_name_plural = "Templates"

    def __str__(self):
        return self.title
