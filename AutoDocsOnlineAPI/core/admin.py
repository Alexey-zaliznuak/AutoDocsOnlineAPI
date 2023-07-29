from django.urls import reverse
from django.utils.safestring import mark_safe


def object_url(obj, title) -> str:
    """
    Return mark save html link on edit object in django admin panel.
    :param title string - link on obj
    :param obj for create link on it
    """
    url = reverse(
        f'admin:{obj._meta.app_label}'
        f'_{obj._meta.object_name.lower()}_change',
        kwargs={'object_id': obj.pk}
    )
    return mark_safe(
        f'<a target="_blank" href={url}>{title or obj}</a>'
    )
