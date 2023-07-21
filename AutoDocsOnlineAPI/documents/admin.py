from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Template


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_official', 'name_in_document', 'description',)
    list_filter = ('is_official',)
    search_fields = ('title', 'name_in_document', 'description',)
