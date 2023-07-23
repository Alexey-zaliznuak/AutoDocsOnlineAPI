import uuid

from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models

from core.utils import make_documents_directory_path
from users.models import User

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
        max_length=settings.TEMPLATE_DESCRIPTION_MAX_LENGTH,
        blank=True,
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


class DefaultUserTemplateValue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        models.CASCADE,
        related_name='%(class)s'
    )
    template = models.ForeignKey(
        Template,
        models.CASCADE,
        related_name='%(class)s'
    )
    value = models.CharField(
        max_length=settings.USER_TEMPLATE_VALUE_VALUE_MAX_LENGTH,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'template'),
                name='default_user_template_unique'
            )
        ]
        verbose_name = 'DefaultUserTemplateValue'
        verbose_name_plural = "DeafaultUserTemplateValues"

    def __str__(self):
        short_length = settings.USER_TEMPLATE_VALUE_SHORT_VALUE_LENGTH

        value = (
            self.value[:short_length] + '...'
            if len(self.value) > short_length
            else self.value
        )
        return ' '.join(map(str, [self.user, self.template, value]))


class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(
        User,
        models.CASCADE,
        related_name='%(class)s'
    )
    title = models.CharField(
        max_length=settings.DOCUMENT_TITLE_MAX_LENGTH,
        validators=[MinLengthValidator(settings.DOCUMENT_TITLE_MAX_LENGTH)]
    )
    description = models.TextField(
        unique=True,
        max_length=settings.DOCUMENT_DESCRIPTION_MAX_LENGTH,
        blank=True
    )
    file = models.FileField(
        upload_to=make_documents_directory_path,
    )
    pub_date = models.DateTimeField(
        'date of publication', auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='author_title_unique'
            )
        ]
        verbose_name = 'Document'
        verbose_name_plural = "Documents"

    def __str__(self):
        return self.title
