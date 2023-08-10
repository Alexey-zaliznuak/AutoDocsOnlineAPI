from core.email import send_confirm_code
from core.pagination import StandardResultsSetPagination
from core.utils import make_confirm_code
from djoser.permissions import CurrentUserOrAdminOrReadOnly
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .permissions import EmailConfirmed
from .serializers import (
    ChangePasswordSerializer,
    SendConfirmCodeSerializer,
    SignUpSerializer,
    UserSerializer,
    ConfirmEmailSerializer
)


class UserMixin(
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    pass


class UserViewSet(UserMixin):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, CurrentUserOrAdminOrReadOnly)
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter, )
    pagination_class = StandardResultsSetPagination
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch']

    @action(
        methods=['get', 'patch', 'delete'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        filter_backends=(),
        pagination_class=None,
        serializer_class=UserSerializer,
        lookup_field='username'
    )
    def me(self, request):
        self.kwargs.update(username=request.user.username)
        if request.method == 'PATCH':
            return self.partial_update(request, request.user.username)

        return self.retrieve(request, request.user.username)

    @action(["post"], detail=False, url_path='me/update_password')
    @swagger_auto_schema(
        request_body=ChangePasswordSerializer,
        operation_description='Update current password.',
    )
    def update_password(self, request):
        user = self.request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            # Check old password
            if not user.check_password(
                serializer.data.get("current_password")
            ):
                return Response(
                    {"current_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get("new_password"))
            user.save()

            return Response(status=status.HTTP_204_NO_CONTENT)


class AUTHApiView(viewsets.ViewSet):
    permission_classes = (AllowAny, )

    @action(methods=["post"], detail=False)
    @swagger_auto_schema(
        request_body=SignUpSerializer,
        operation_description="""
        User registration.
        After register, You should request code on 'auth/send_confirm_code'.
        You can`t use your account until you confirm your email.
        To confirm the email, see 'auth/confirm_email'.
        """,
    )
    def signup(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        User.objects.create(
            **serializer.validated_data,
        )

        return Response(request.data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=False)
    @swagger_auto_schema(
        request_body=ConfirmEmailSerializer,
        operation_description="""
        Email confirmation.
        After confirmation, you can get a jwt token (see jwt/).
        """,
    )
    def confirm_email(self, request):
        serializer = ConfirmEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(
            username=serializer.validated_data.get('username')
        )

        user.email_confirmed = True
        user.save()

        return Response(request.data, status=status.HTTP_200_OK)

    @action(["post"], False)
    @swagger_auto_schema(
        request_body=SendConfirmCodeSerializer,
        operation_description='Send confirmation code on user email',
    )
    def send_confirm_code(self, request):
        serializer = SendConfirmCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(
            username=serializer.validated_data.get('username')
        )

        user.confirmation_code = make_confirm_code()
        send_confirm_code(user)
        user.save()

        return Response(request.data, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (EmailConfirmed, )
