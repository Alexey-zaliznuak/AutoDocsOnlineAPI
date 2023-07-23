from django.contrib import admin

from .models import Template, UserTemplateValue


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_official', 'name_in_document', 'description',)
    list_filter = ('is_official',)
    search_fields = ('title', 'name_in_document', 'description',)


@admin.register(UserTemplateValue)
class UserTemplateValueAdmin(admin.ModelAdmin):
    list_display = ('user', 'template', 'value', 'pk',)
    search_fields = ('title', 'name_in_document', 'description',)
