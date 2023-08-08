from django_filters import (
    FilterSet,
    ModelChoiceFilter,
    BooleanFilter,
)

from documents.models import Document, Template, UserDefaultTemplateValue
from users.models import User


class FilterTemplate(FilterSet):
    author = ModelChoiceFilter(
        queryset=User.objects.all(),
        to_field_name='username'
    )
    is_official = BooleanFilter(method='filter_is_official')

    def filter_is_official(self, queryset, field_name, value):
        queryset = queryset.filter(
            is_official=value
        )
        return queryset

    class Meta:
        model = Template
        fields = ('author', 'is_official')


class FilterDocument(FilterSet):
    author = ModelChoiceFilter(
        queryset=User.objects.all(),
        to_field_name='username'
    )

    class Meta:
        model = Document
        fields = ('author',)


class FilterUserDefaultTemplateValue(FilterSet):
    is_official = BooleanFilter(method='filter_is_official')

    def filter_is_official(self, queryset, field_name, value):
        queryset = queryset.filter(
            template__is_official=value
        )
        return queryset

    class Meta:
        model = UserDefaultTemplateValue
        fields = ('is_official',)