from django.contrib import admin

from .models import Template, DefaultUserTemplateValue


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_official', 'name_in_document', 'description',)
    list_filter = ('is_official',)
    search_fields = ('title', 'name_in_document', 'description',)


@admin.register(DefaultUserTemplateValue)
class DefaultUserTemplateValueAdmin(admin.ModelAdmin):
    list_display = ('user', 'template', 'value', 'pk',)
    search_fields = ('title', 'name_in_document', 'description',)
