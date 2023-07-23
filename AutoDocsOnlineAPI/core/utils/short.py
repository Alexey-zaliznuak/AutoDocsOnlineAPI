from django.conf import settings


def short(text, max_length):
    if len(text) > max_length:
        return text[:max_length] + settings.SHORT_END
    return text
