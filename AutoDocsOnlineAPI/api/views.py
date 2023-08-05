from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated

from documents.models import (
    Template
)

from .filters import (
    FilterTemplate,
)
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    TemplateSerializer,
)


HTTP_METHOD_NAMES_WITHOUT_PUT = ('get', 'post', 'patch', 'delete',)


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

# class RecordViewSet(viewsets.ModelViewSet):
#     ...

# class DocumentViewSet(viewsets.ModelViewSet):
#     serializer_class = DocumentSerializer
#     permission_classes = (IsAuthenticated, IsAuthorOrReadOnly,)

#     @action(["get"], Trueurl_name='download_document', permission_classes=())
#     def download(self, request, pk):
#         context_400 = {"Access denied": "document is private"}
#         document = Document.objects.get(pk=pk)

#         if not document.public and request.user != document.owner:
#             return Response(context_400, status=status.HTTP_400_BAD_REQUEST)

#         response = FileResponse(open(document.file.path, 'rb'))
#         return response

#     def get_queryset(self):
#         # protect “AnonymousUser” is not a valid UUID
#         if not self.request.user.is_anonymous:
#             new_queryset = Document.objects.filter(owner=self.request.user)
#             return new_queryset

#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)


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
