from django.shortcuts import get_list_or_404
from core.documents_fromatter import DocumentsFormatter
from django.http.response import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404 as _get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from documents.models import (
    Document,
    DocumentsPackage,
    Record,
    Template,
    UserDefaultTemplateValue,
)

from .filters import (
    FilterDocument,
    FilterDocumentPackage,
    FilterRecords,
    FilterTemplate,
    FilterUserDefaultTemplateValue,
)
from .permissions import (
    IsAuthor,
    SelfRelated,
    IsAuthorOrReadOnly,
    SelfRelatedOrIsDocumentsPackageAuthor,
)
from .serializers import (
    CreateUpdateRecordSerializer,
    CreateUpdateDocumentsPackageSerializer,
    CreateUpdateDocumentSerializer,
    DownloadRecordDocumentSerializer,
    CreateUpdateUserDefaultTemplateValueSerializer,
    GetDocumentsPackageSerializer,
    GetDocumentsPackageRecordsSerializer,
    GetDocumentSerializer,
    GetSelfRecordsSerializer,
    GetUserDefaultTemplateValueSerializer,
    TemplateSerializer,
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


class ListCreateViewSet(
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
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


class DocumentsPackageViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly,)
    http_method_names = HTTP_METHOD_NAMES_WITHOUT_PUT

    queryset = DocumentsPackage.objects.all()

    filterset_class = FilterDocumentPackage
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('^title',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetDocumentsPackageSerializer

        return CreateUpdateDocumentsPackageSerializer


class RecordsViewSet(ListCreateViewSet):
    permission_classes = (
        IsAuthenticated, SelfRelatedOrIsDocumentsPackageAuthor,
    )
    http_method_names = HTTP_METHOD_NAMES_WITHOUT_PUT

    filterset_class = FilterRecords
    filter_backends = (DjangoFilterBackend,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetSelfRecordsSerializer

        return CreateUpdateRecordSerializer

    def get_queryset(self):
        # To avoid mistakes during schema generation
        if not self.request.user.is_anonymous:
            return Record.objects.filter(
                user=self.request.user
            )

    @action(
        ['get'],
        False,
        url_path='documents_package/(?P<pk>[^/.]+)',
        permission_classes=(IsAuthor,),
        filterset_class=None,
    )
    def documents_package_records(self, request, pk=None):
        documents_package = get_list_or_404(DocumentsPackage, pk=pk)

        self.check_object_permissions(request, documents_package)

        records = get_list_or_404(Record, documents_package=documents_package)
        serializer = GetDocumentsPackageRecordsSerializer(records, many=True)

        return Response(serializer.data)

    @action(
        ['get'],
        True,
        url_path='download/(?P<document_id>[^/.]+)',
        permission_classes=(SelfRelatedOrIsDocumentsPackageAuthor,),
        filterset_class=None,
    )
    def download_filled_document(self, request, pk, document_id):
        templates_values_primitive = {}

        serializer = DownloadRecordDocumentSerializer(
            data={
                'record': pk,
                'document_id': document_id
            }
        )
        serializer.is_valid(raise_exception=True)

        record = serializer.validated_data.get('record')
        self.check_object_permissions(request, record)

        document_id = serializer.validated_data.get('document_id')
        document = record.documents_package.documents.get(
            pk=document_id
        )

        templates_values = record.templates_values.all()

        for tv in templates_values:
            templates_values_primitive[tv.template.name_in_document] = tv.value

        data = DocumentsFormatter(
                document.file.path,
                templates_values_primitive
            ).format()

        return FileResponse(
            data,
            filename=document.file.name.split('/')[-1]
        )


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
