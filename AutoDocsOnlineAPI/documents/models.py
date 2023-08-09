import uuid

from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models

from core.utils import make_documents_directory_path, short
from core.models import CreatedModel
from users.models import User

from .validators import NameInDocumentRegexValidator


class Template(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(
        User,
        models.CASCADE,
        related_name='templates'
    )
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
            f"must have "
            f"prefix '{settings.TEMPLATE_NAME_IN_DOCUMENT_PREFIX}'"
            f"and postfix '{settings.TEMPLATE_NAME_IN_DOCUMENT_POSTFIX}'"
        ),
        validators=[
            NameInDocumentRegexValidator(),
            MinLengthValidator(settings.TEMPLATE_NAME_IN_DOCUMENT_MIN_LENGTH),
        ]
    )
    description = models.TextField(
        'description',
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


class TemplateValue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    template = models.ForeignKey(
        Template,
        models.CASCADE,
        related_name='values'
    )
    value = models.CharField(
        max_length=settings.TEMPLATE_VALUE_VALUE_MAX_LENGTH,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('template', 'value'),
                name='template_value_unique'
            )
        ]
        verbose_name = 'TemplateValue'
        verbose_name_plural = "TemplateValues"

    def __str__(self):
        short_value = short(self.value, )
        return ' '.join(map(str, [self.template, short_value]))


class UserDefaultTemplateValue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        models.CASCADE,
        related_name='default_templates_values'
    )
    template_value = models.ForeignKey(
        TemplateValue,
        models.CASCADE,
        related_name='default_users_values',
    )

    class Meta:
        verbose_name = 'UserDefaultTemplateValue'
        verbose_name_plural = "UserDefaultTemplateValues"

    def __str__(self):
        return ' '.join(map(str, [self.user, self.template_value]))


class Document(CreatedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(
        User,
        models.CASCADE,
        related_name='documents'
    )
    title = models.CharField(
        max_length=settings.DOCUMENT_TITLE_MAX_LENGTH,
        validators=[MinLengthValidator(settings.DOCUMENT_TITLE_MIN_LENGTH)]
    )
    description = models.TextField(
        max_length=settings.DOCUMENT_DESCRIPTION_MAX_LENGTH,
        blank=True
    )
    file = models.FileField(
        upload_to=make_documents_directory_path,
    )
    templates = models.ManyToManyField(Template, through='DocumentTemplate')

    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = "Documents"

    def __str__(self):
        return ' '.join(map(str, [self.author, self.title]))


class DocumentsPackage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(
        max_length=settings.DOCUMENTS_PACKAGE_TITLE_MAX_LENGTH,
        validators=[
            MinLengthValidator(settings.DOCUMENTS_PACKAGE_TITLE_MIN_LENGTH)
        ],
        unique=True
    )
    author = models.ForeignKey(
        User,
        models.CASCADE,
        related_name='documents_packages'
    )
    documents = models.ManyToManyField(
        Document, through='DocumentDocumentsPackage'
    )

    class Meta:
        verbose_name = 'Documents package'
        verbose_name_plural = "Documents packages"

    def __str__(self):
        return ' '.join(map(str, [self.author, self.title]))


class Record(CreatedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        models.CASCADE,
        related_name='records'
    )
    documents_package = models.ForeignKey(
        DocumentsPackage,
        models.CASCADE,
        related_name='records'
    )
    templates_values = models.ManyToManyField(
        TemplateValue,
        through='RecordTemplateValue',
    )

    class Meta:
        verbose_name = 'Record'
        verbose_name_plural = "Records"

    def __str__(self):
        return ' '.join(
            map(
                str,
                [self.user, self.documents_package, self.creation_date]
            )
        )


class DocumentDocumentsPackage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(
        Document,
        models.CASCADE,
        related_name='documents_packages'
    )
    documents_package = models.ForeignKey(
        DocumentsPackage,
        models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('document', 'documents_package'),
                name='document_documents_package_unique'
            )
        ]
        verbose_name = 'DocumentDocumentsPackage'
        verbose_name_plural = "DocumentDocumentsPackages"

    def __str__(self):
        return ' '.join(map(str, [self.document, self.documents_package]))


class DocumentTemplate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(
        Document,
        models.CASCADE,
    )
    template = models.ForeignKey(
        Template,
        models.CASCADE,
        related_name='documents'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('document', 'template'),
                name='document_template_unique'
            )
        ]
        verbose_name = 'DocumentTemplate'
        verbose_name_plural = "DocumentTemplates"

    def __str__(self):
        return ' '.join(map(str, [self.document, self.template]))


class RecordTemplateValue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    record = models.ForeignKey(Record, models.CASCADE)
    template_value = models.ForeignKey(
        TemplateValue,
        models.CASCADE,
        related_name='records'
    )
