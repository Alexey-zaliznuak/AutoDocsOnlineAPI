from django.apps import apps
from django.conf import settings
from django.core import validators
from django.core.exceptions import ValidationError


def validate_title_not_same_in_official_templates(title):
    Template = apps.get_model('documents', 'Template')

    if Template.objects.filter(is_official=True, title=title).exists():
        raise ValidationError(
            "This title already exist in official template,"
            " you should use official templates instead create new."
        )


class NameInDocumentRegexValidator(validators.RegexValidator):
    """
    Check prefix, postfix and valid characters
    """
    def __init__(self, *args, **kwargs):
        prefix = settings.TEMPLATE_NAME_IN_DOCUMENT_PREFIX
        postfix = settings.TEMPLATE_NAME_IN_DOCUMENT_POSTFIX

        self.message = (
            "Enter a valid name in document. "
            "This value may contain only letters "
            "and '-'/'_' characters and start/end with "
            f"'{prefix}' and '{postfix}' respectively."
        )
        self.regex = rf"^{prefix}[a-zA-Z-_]+{postfix}\Z"

        super().__init__(*args, **kwargs)
