from django.conf import settings


def short(
        text: str,
        max_length: int = 20,
        short_end: str = settings.SHORT_END
) -> str:
    """
    if necessary, truncates the string to the specified value.
    """
    if len(text) > max_length:
        return text[:max_length] + short_end
    return text
