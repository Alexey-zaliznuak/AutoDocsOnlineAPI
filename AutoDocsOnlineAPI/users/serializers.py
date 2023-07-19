from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
        )


class SignUpSerializer(serializers.ModelSerializer):
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
        q = User.objects.filter(username=data['username'])

        if q.exists():
            user = q.get()

            if user.email_confirmed:
                raise ValidationError(
                    'User with this username already register'
                    'and confirm email'
                )

            raise ValidationError(
                'User with this username already register '
                'but not confirmed email'
            )

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
