from django.shortcuts import get_list_or_404, get_object_or_404
from core.formatters import DocumentsFormatter, ExcelFormatter
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

    lookup_url_kwarg = 'template_pk'
    lookup_field = 'template_value__template__id'

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
        permission_classes=(IsAuthenticated, IsAuthor,),
        filterset_class=None,
    )
    def documents_package_records(self, request, pk=None):
        documents_package = get_object_or_404(DocumentsPackage, pk=pk)

        self.check_object_permissions(request, documents_package)

        records = get_list_or_404(Record, documents_package=documents_package)
        serializer = GetDocumentsPackageRecordsSerializer(records, many=True)

        return Response(serializer.data)

    @action(
        ['get'],
        False,
        url_path='documents_package/(?P<pk>[^/.]+)/download',
        permission_classes=(IsAuthenticated, IsAuthor,),
        filterset_class=None,
    )
    def download_documents_package_records(self, request, pk=None):
        documents_package = get_object_or_404(DocumentsPackage, pk=pk)
        self.check_object_permissions(request, documents_package)

        records = get_list_or_404(Record, documents_package=documents_package)
        templates = documents_package.templates

        excel, filename = ExcelFormatter(
            records, templates, title=documents_package.title
        ).make_excel_data_summary()

        return FileResponse(
            excel,
            filename=filename + '.xlsx'
        )

    @action(
        ['get'],
        True,
        url_path='download/(?P<document_id>[^/.]+)',
        permission_classes=(SelfRelatedOrIsDocumentsPackageAuthor,),
        filterset_class=None,
    )
    def download_filled_document(self, request, pk, document_id):
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

        formatted_document = DocumentsFormatter(
            document.file.path,
            templates_values
        ).format()

        return FileResponse(
            formatted_document,
            filename=document.file.name.split('/')[-1]
        )
