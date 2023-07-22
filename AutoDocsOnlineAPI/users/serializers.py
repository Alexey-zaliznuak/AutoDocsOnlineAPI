from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.db.models import Q
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
        )


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        validators=(UnicodeUsernameValidator,),
        max_length=settings.USER_USERNAME_MAX_LENGTH
    )
    email = serializers.EmailField(max_length=settings.USER_EMAIL_MAX_LENGTH)
    first_name = serializers.CharField(
        max_length=settings.USER_FIRST_NAME_MAX_LENGTH
    )
    last_name = serializers.CharField(
        max_length=settings.USER_LAST_NAME_MAX_LENGTH
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
        )

    def validate_username(sef, value):
        if value == 'me':
            raise ValidationError('uncorrect username')

        return value

    def validate_password(self, value):
        validate_password(value)
        return make_password(value)

    def validate(self, data):
        """
        Default validate but delete accounts with same email/username
        if they have not confirmed their email address.
        This is useful if you used the registration
        but realized that you entered an incorrect address and/or username.
        """
        error = 'User with this {} already register and confirm email'
        username = data['username']
        email = data['email']

        if User.objects.filter(
            username=username,
            email_confirmed=True
        ).exists():
            raise ValidationError(error.format('username'))

        if User.objects.filter(email=email, email_confirmed=True).exists():
            raise ValidationError(error.format('email'))

        q = User.objects.filter(Q(username=username) | Q(email=data['email']))
        if q.exists():
            q.delete()

        return super().validate(data)


class SendConfirmCodeSerializer(serializers.Serializer):
    username = serializers.CharField()

    def validate_username(sef, username):
        if not User.objects.filter(username=username).exists():
            raise ValidationError('User with this username doesn`t exist')

        return username

    def validate(self, data):
        user = User.objects.get(username=data['username'])

        if user.email_confirmed:
            raise ValidationError('You already confirmed email adress')

        return super().validate(data)


class ConfirmEmailSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField(
        min_length=settings.CONFIRM_CODE_LENGHT,
        max_length=settings.CONFIRM_CODE_LENGHT
    )

    def validate_username(sef, username):
        if not User.objects.filter(username=username).exists():
            raise ValidationError('User with this username doesn`t exist')

        return username

    def validate(self, data):
        user = User.objects.get(username=data['username'])

        if user.email_confirmed:
            raise ValidationError('You already confirmed email adress')

        if user.confirmation_code != data['confirmation_code']:
            raise ValidationError('Uncorrect confirmation_code')

        return super().validate(data)


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
