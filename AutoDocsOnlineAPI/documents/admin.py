from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe

from core.admin import object_url
from core.utils import short

from .models import (
    Template,
    TemplateValue,
    Record,
    Document,
    DocumentPackage,
    DocumentTemplate,
    RecordTemplateValue,
    DocumentDocumentPackage,
    UserDefaultTemplateValue,
)


HTML_NEW_LINE = '<br \\>'


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'name_in_document',
        'is_official',
        'description_',
        'pk'
    )
    list_filter = ('is_official',)
    search_fields = ('title', 'name_in_document', 'description',)
    empty_value_display = '-empty-'

    @admin.display(empty_value='unknown', description="description")
    def description_(self, obj):
        return short(obj.description)


@admin.register(TemplateValue)
class TemplateValueAdmin(admin.ModelAdmin):
    list_display = (
        'template_',
        'value_',
        'pk_',
    )
    search_fields = ('template__title', 'value',)
    empty_value_display = '-empty-'

    @admin.display(empty_value='unknown', description="pk")
    def pk_(self, obj):
        return object_url(obj, obj.pk)

    @admin.display(empty_value='unknown', description="template")
    def template_(self, obj):
        return object_url(obj.template)

    @admin.display(empty_value='unknown', description="value")
    def value_(self, obj):
        return short(obj.value)


@admin.register(UserDefaultTemplateValue)
class UserDefaultTemplateValueAdmin(admin.ModelAdmin):
    list_display = (
        'user_',
        'template_value_',
        'pk_',
    )
    search_fields = ('user__username',)
    empty_value_display = '-empty-'

    @admin.display(empty_value='unknown', description="pk")
    def pk_(self, obj):
        return object_url(obj, obj.pk)

    @admin.display(empty_value='unknown', description="user")
    def user_(self, obj):
        return object_url(obj.user)

    @admin.display(empty_value='unknown', description="template_value")
    def template_value_(self, obj):
        return object_url(
            obj.template_value,
            short(
                str(obj.template_value),
                settings.ADMIN_USER_DEFAULT_TEMPLATE_VALUE_SHORT_LENGTH
            )
        )


class DocumentTemplateInline(admin.TabularInline):
    model = DocumentTemplate
    fk_name = 'document'
    extra = 1


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    inlines = [DocumentTemplateInline]
    list_display = (
        'title',
        'author_',
        'templates_',
        'description_',
        'file_',
        'pk',
    )
    search_fields = ('title', 'author__username',)
    empty_value_display = '-empty-'

    @admin.display(empty_value='unknown', description="author")
    def author_(self, obj):
        return object_url(obj.author)

    @admin.display(empty_value='unknown', description="templates")
    def templates_(self, obj):
        return mark_safe(
            HTML_NEW_LINE.join(map(object_url, obj.templates.all()))
        )

    @admin.display(empty_value='unknown', description="description")
    def description_(self, obj):
        return short(obj.description)

    @admin.display(empty_value='unknown', description="file")
    def file_(self, obj):
        # TODO
        return 'link'


class DocumentDocumentPackageInline(admin.TabularInline):
    model = DocumentDocumentPackage
    fk_name = 'document_package'
    extra = 1


@admin.register(DocumentPackage)
class DocumentPackageAdmin(admin.ModelAdmin):
    inlines = [DocumentDocumentPackageInline]
    list_display = (
        'title_',
        'author',
        'documents_',
        'pk',
    )
    search_fields = ('title', 'author__username',)
    empty_value_display = '-empty-'

    @admin.display(empty_value='unknown', description="title")
    def title_(self, obj):
        return short(obj.title)

    @admin.display(empty_value='unknown', description="documents")
    def documents_(self, obj):
        return mark_safe(
            HTML_NEW_LINE.join(map(object_url, obj.documents.all()))
        )


@admin.register(DocumentDocumentPackage)
class DocumentDocumentPackageAdmin(admin.ModelAdmin):
    list_display = (
        'document_package_',
        'document_',
        'pk_',
    )
    empty_value_display = '-empty-'

    @admin.display(empty_value='unknown', description="document_package")
    def document_package_(self, obj):
        return object_url(obj.document_package)

    @admin.display(empty_value='unknown', description="document")
    def document_(self, obj):
        return object_url(obj.document)

    @admin.display(empty_value='unknown', description="pk")
    def pk_(self, obj):
        return object_url(obj, obj.pk)


@admin.register(DocumentTemplate)
class DocumenTemplateAdmin(admin.ModelAdmin):
    list_display = (
        'document_',
        'template_',
        'pk_',
    )
    empty_value_display = '-empty-'

    @admin.display(empty_value='unknown', description="template")
    def template_(self, obj):
        return object_url(obj.template)

    @admin.display(empty_value='unknown', description="document")
    def document_(self, obj):
        return object_url(obj.document)

    @admin.display(empty_value='unknown', description="pk")
    def pk_(self, obj):
        return object_url(obj, obj.pk)


class RecordTemplateValueInline(admin.TabularInline):
    model = RecordTemplateValue
    fk_name = 'record'
    extra = 1


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    inlines = [RecordTemplateValueInline]
    list_display = (
        'user_',
        'document_package_',
        'templates_values_',
        'pk_',
    )
    search_fields = ('user__username',)
    empty_value_display = '-empty-'

    @admin.display(empty_value='unknown', description="user")
    def user_(self, obj):
        return object_url(obj.user)

    @admin.display(empty_value='unknown', description="templates_values")
    def templates_values_(self, obj):
        return mark_safe(
            HTML_NEW_LINE.join(map(object_url, obj.templates_values.all()))
        )

    @admin.display(empty_value='unknown', description="document_package")
    def document_package_(self, obj):
        return object_url(obj.document_package)

    @admin.display(empty_value='unknown', description="pk")
    def pk_(self, obj):
        return object_url(obj, obj.pk)


@admin.register(RecordTemplateValue)
class RecordTemplateValueAdmin(admin.ModelAdmin):
    list_display = (
        'record_',
        'template_value_',
        'pk_',
    )
    empty_value_display = '-empty-'

    @admin.display(empty_value='unknown', description="record")
    def record_(self, obj):
        return object_url(obj.record)

    @admin.display(empty_value='unknown', description="template_value")
    def template_value_(self, obj):
        return object_url(obj.template_value)

    @admin.display(empty_value='unknown', description="pk")
    def pk_(self, obj):
        return object_url(obj, obj.pk)
