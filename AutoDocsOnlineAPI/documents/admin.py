from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe

from core.admin import object_url
from core.utils import short

from .models import (
    Category,
    Template,
    TemplateValue,
    Record,
    Document,
    DocumentsPackage,
    DocumentTemplate,
    RecordTemplateValue,
    DocumentDocumentsPackage,
    UserDefaultTemplateValue,
)


HTML_NEW_LINE = '<br \\>'
HTML_LINK = '<a href={url}>{title}</a>'


class DocumentDocumentsPackageInline(admin.TabularInline):
    model = DocumentDocumentsPackage
    fk_name = 'documents_package'
    extra = 1


class DocumentTemplateInline(admin.TabularInline):
    model = DocumentTemplate
    fk_name = 'document'
    extra = 1


class RecordTemplateValueInline(admin.TabularInline):
    model = RecordTemplateValue
    fk_name = 'record'
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description_',
        'pk'
    )
    search_fields = (
        'title',
        'description',
    )
    empty_value_display = '-empty-'

    @admin.display(empty_value='unknown', description="description")
    def description_(self, obj):
        return short(obj.description)


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author_',
        'name_in_document',
        'category_',
        'is_official',
        'description_',
        'pk'
    )
    list_filter = ('is_official', 'category__title')
    search_fields = (
        'title',
        'name_in_document',
        'description',
        'author__username',
    )
    empty_value_display = '-empty-'

    @admin.display(empty_value='unknown', description="description")
    def description_(self, obj):
        return short(obj.description)

    @admin.display(empty_value='unknown', description="author")
    def author_(self, obj):
        return object_url(obj.author)

    @admin.display(empty_value='unknown', description="category")
    def category_(self, obj):
        if obj.category:
            return object_url(obj.category)


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
        return mark_safe(HTML_LINK.format(
            url=settings.MEDIA_URL + str(obj.file),
            title='download'
        ))


@admin.register(DocumentsPackage)
class DocumentsPackageAdmin(admin.ModelAdmin):
    inlines = [DocumentDocumentsPackageInline]
    list_display = (
        'title_',
        'author',
        'documents_',
        'description_',
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

    @admin.display(empty_value='unknown', description="description")
    def description_(self, obj):
        return short(obj.description)


@admin.register(DocumentDocumentsPackage)
class DocumentDocumentsPackageAdmin(admin.ModelAdmin):
    list_display = (
        'documents_package_',
        'document_',
        'pk_',
    )
    empty_value_display = '-empty-'

    @admin.display(empty_value='unknown', description="documents_package")
    def documents_package_(self, obj):
        return object_url(obj.documents_package)

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


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    inlines = [RecordTemplateValueInline]
    list_display = (
        'user_',
        'documents_package_',
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

    @admin.display(empty_value='unknown', description="documents_package")
    def documents_package_(self, obj):
        return object_url(obj.documents_package)

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
