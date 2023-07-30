from django.conf import settings
from django.contrib import admin

from core.admin import object_url
from core.utils import short

from .models import (
    Record,
    Document,
    Template,
    TemplateValue,
    DocumentPackage,
    DocumentTemplate,
    RecordTemplateValue,
    DocumentDocumentPackage,
    UserDefaultTemplateValue,
)


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'name_in_document',
        'is_official',
        'description_',
    )
    list_filter = ('is_official',)
    search_fields = ('title', 'name_in_document', 'description',)
    empty_value_display = '-empty-'

    @admin.display(empty_value='unknown', description="description")
    def description_(self, template):
        return short(template.description)


@admin.register(TemplateValue)
class TemplateValueAdmin(admin.ModelAdmin):
    list_display = (
        'pk_',
        'template_',
        'value_',
    )
    search_fields = ('template__str__', 'value',)
    empty_value_display = '-empty-'

    @admin.display(empty_value='unknown', description="template")
    def template_(self, template_value):
        return object_url(template_value.template)

    @admin.display(empty_value='unknown', description="value")
    def value_(self, template_value):
        return short(template_value.value)

    @admin.display(empty_value='unknown', description="pk")
    def pk_(self, template_value):
        return object_url(template_value, template_value.pk)


# @admin.register(Record)
# class RecordAdmin(admin.ModelAdmin):
#     list_display = (
#         'user_',
#         'document_package_',
#         'templates_values_',
#         'pk',
#     )
#     search_fields = ('user__username',)
#     empty_value_display = '-empty-'

#     @admin.display(empty_value='unknown', description="user")
#     def user_(self, record):
#         return object_url(record.user)

#     @admin.display(empty_value='unknown', description="templates_values")
#     def templates_values_(self, record):
#         return ' '.join(map(str, record.templates_values.all()))

#     @admin.display(empty_value='unknown', description="document_package")
#     def document_package_(self, record):
#         return object_url(record.document_package)



# @admin.register(UserTemplateDefaultValue)
# class UserTemplateDefaultValueAdmin(admin.ModelAdmin):
#     list_display = ('user', 'template', 'value', 'pk',)
#     search_fields = ('title', 'name_in_document', 'description',)
#     empty_value_display = '-empty-'


# @admin.register(Document)
# class DocumentAdmin(admin.ModelAdmin):
#     list_display = (
#         'title_',
#         'author',
#         'pk',
#     )
#     search_fields = ('title', 'author__username',)
#     empty_value_display = '-empty-'

#     @admin.display(empty_value='unknown', description="title_")
#     def title_(self, document):
#         return short(document.title, settings.DOCUMENT_TITLE_SHORT_LENGTH)


# @admin.register(DocumentPackage)
# class DocumentPackageAdmin(admin.ModelAdmin):
#     list_display = (
#         'title_',
#         'author',
#         'documents_',
#         'pk',
#     )
#     search_fields = ('title', 'author__username',)
#     empty_value_display = '-empty-'

#     @admin.display(empty_value='unknown', description="title_")
#     def title_(self, package):
#         return short(
#             package.title, settings.DOCUMENT_PACKAGE_TITLE_SHORT_LENGTH
#         )

#     @admin.display(empty_value='unknown', description="documents")
#     def documents_(self, package):
#         return '\n'.join(map(str, package.document.all()))


# @admin.register(DocumentDocumentPackage)
# class DocumentDocumentPackageAdmin(admin.ModelAdmin):
#     list_display = (
#         'title_',
#         'document',
#         'document_package',
#         'pk',
#     )
#     search_fields = ('title',)
#     empty_value_display = '-empty-'

#     @admin.display(empty_value='unknown', description="title_")
#     def title_(self, package):
#         return short(
#             package.title,
#             settings.DOCUMENT_DOCUMENT_PACKAGE_TITLE_SHORT_LENGTH
#         )

#     @admin.display(empty_value='unknown', description="documents")
#     def documents_(self, package):
#         return '\n'.join(map(str, package.document.all()))
