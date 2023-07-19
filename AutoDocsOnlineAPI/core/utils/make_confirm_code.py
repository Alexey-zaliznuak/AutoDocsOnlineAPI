from os import urandom

from django.conf import settings


def make_confirm_code() -> str:
    """
    Return number as string with length = settings.CONFIRM_CODE_LENGTH .
    """
    code = ''
    while len(str(code)) < settings.CONFIRM_CODE_LENGHT:
        code += str(int.from_bytes(urandom(1), 'little'))

    return code[:settings.CONFIRM_CODE_LENGHT]
