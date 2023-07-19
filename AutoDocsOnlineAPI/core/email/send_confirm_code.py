from django.conf import settings

from users.models import User


def send_confirm_code(user: User):
    user.email_user(
        subject=settings.USER_SEND_CONFIRM_CODE_EMAIL_SUBJECT,
        message=settings.USER_SEND_CONFIRM_CODE_EMAIL_MESSAGE.format(
            code=user.confirmation_code
        ),
        from_email=settings.EMAIL_HOST_USER,
    )
