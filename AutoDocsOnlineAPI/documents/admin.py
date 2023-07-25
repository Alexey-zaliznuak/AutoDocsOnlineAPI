from django.conf import settings
from django.contrib import admin

from core.utils import short

from .models import Document, Template, UserTemplateDefaultValue


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_official', 'name_in_document', 'description',)
    list_filter = ('is_official',)
    search_fields = ('title', 'name_in_document', 'description',)


@admin.register(UserTemplateDefaultValue)
class UserTemplateDefaultValueAdmin(admin.ModelAdmin):
    list_display = ('user', 'template', 'value', 'pk',)
    search_fields = ('title', 'name_in_document', 'description',)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        'title_',
        'author',
        'pk',
    )
    search_fields = ('title', 'author__username',)
    empty_value_display = '-пусто-'

    @admin.display(empty_value='unknown', description="title_")
    def title_(self, document):
        return short(document.title, settings.DOCUMENT_TITLE_SHORT_LENGTH)
