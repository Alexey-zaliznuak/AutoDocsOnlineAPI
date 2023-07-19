from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path(
        '',
        RedirectView.as_view(
            url=reverse_lazy('schema-swagger-ui')
        ),
        name='index'
    )
]
