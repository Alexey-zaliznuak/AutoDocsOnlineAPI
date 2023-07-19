from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, AUTHApiView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('auth', AUTHApiView, basename='auth')


urlpatterns = [
    path('', include(router.urls)),

    re_path(
        r"^auth/jwt/create/?",
        CustomTokenObtainPairView.as_view(),
        name="jwt-create"
    ),
    re_path(
        r"^auth/jwt/refresh/?",
        TokenRefreshView.as_view(),
        name="jwt-refresh"
    ),
    re_path(
        r"^auth/jwt/verify/?",
        TokenVerifyView.as_view(),
        name="jwt-verify"
    ),
]
