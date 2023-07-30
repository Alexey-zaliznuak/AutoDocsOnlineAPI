from django.contrib import admin

from core.admin import object_url
from core.utils import short

from .models import (
    Template,
    TemplateValue,
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
