# from django.conf import settings
# from django.contrib import admin

# from core.utils import short

# from .models import (
#     Template,
#     Document,
#     DocumentPackage,
#     DocumentDocumentPackage,
#     UserTemplateDefaultValue,
# )


# @admin.register(Template)
# class TemplateAdmin(admin.ModelAdmin):
#     list_display = ('title', 'is_official', 'name_in_document', 'description'
#     list_filter = ('is_official',)
#     search_fields = ('title', 'name_in_document', 'description',)
#     empty_value_display = '-empty-'


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
