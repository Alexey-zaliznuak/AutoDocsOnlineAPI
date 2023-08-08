from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.generics import get_object_or_404 as _get_object_or_404
from rest_framework.permissions import IsAuthenticated

from documents.models import (
    Document,
    Template,
    UserDefaultTemplateValue,
)

from .filters import (
    FilterDocument,
    FilterTemplate,
    FilterUserDefaultTemplateValue,
)
from .permissions import SelfRelated, IsAuthorOrReadOnly
from .serializers import (
    GetDocumentSerializer,
    TemplateSerializer,
    CreateUpdateDocumentSerializer,
    GetUserDefaultTemplateValueSerializer,
    CreateUpdateUserDefaultTemplateValueSerializer,
)


HTTP_METHOD_NAMES_WITHOUT_PUT = ('get', 'post', 'patch', 'delete',)


class GetCreateUpdateViewSet(
    viewsets.mixins.CreateModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    "Model viewset without delete."
    pass


class TemplateViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)
    http_method_names = HTTP_METHOD_NAMES_WITHOUT_PUT

    queryset = Template.objects.all()
    serializer_class = TemplateSerializer

    filterset_class = FilterTemplate
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('^title',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class DocumentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly,)
    http_method_names = HTTP_METHOD_NAMES_WITHOUT_PUT

    queryset = Document.objects.all()

    filterset_class = FilterDocument
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('^title',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetDocumentSerializer

        return CreateUpdateDocumentSerializer


class UserDefaultTemplateValueViewSet(GetCreateUpdateViewSet):
    permission_classes = (IsAuthenticated, SelfRelated,)
    http_method_names = HTTP_METHOD_NAMES_WITHOUT_PUT

    lookup_url_kwarg = 'template_title'
    lookup_field = 'template_value__template__title'

    filterset_class = FilterUserDefaultTemplateValue
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('^template__title',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetUserDefaultTemplateValueSerializer

        return CreateUpdateUserDefaultTemplateValueSerializer

    def get_queryset(self):
        # To avoid mistakes during schema generation
        if not self.request.user.is_anonymous:

            return UserDefaultTemplateValue.objects.filter(
                user=self.request.user
            )

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_url_kwarg]}

        obj = _get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)

        return obj


# @action(["get"], Trueurl_name='download_document', permission_classes=())
# def download(self, request, pk):
#     context_400 = {"Access denied": "document is private"}
#     document = Document.objects.get(pk=pk)

#     if not document.public and request.user != document.owner:
#         return Response(context_400, status=status.HTTP_400_BAD_REQUEST)

#     response = FileResponse(open(document.file.path, 'rb'))
#     return response

# class DocumentsPackageViewSet(viewsets.ModelViewSet):
#     queryset = DocumentsPackage.objects.all()
#     serializer_class = DocumentsPackageSerializer
#     permission_classes = (IsAuthorOrReadOnly,)

#     def get_queryset(self):
#         # protect “AnonymousUser” is not a valid UUID
#         if not self.request.user.is_anonymous:
#             new_queryset = DocumentsPackage.objects.filter(
#                 owner=self.request.user
#             )
#             return new_queryset

#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
