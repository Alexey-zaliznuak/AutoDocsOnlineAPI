from django.http import FileResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .permissions import IsOwnerOrReadOnlyPermission
from .serializers import DocumentSerializer, DocumentsPackageSerializer

from documents.models import Document, DocumentsPackage


class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnlyPermission,)

    @action(["get"], Trueurl_name='download_document', permission_classes=())
    def download(self, request, pk):
        context_400 = {"Access denied": "document is private"}
        document = Document.objects.get(pk=pk)

        if not document.public and request.user != document.owner:
            return Response(context_400, status=status.HTTP_400_BAD_REQUEST)

        response = FileResponse(open(document.file.path, 'rb'))
        return response

    def get_queryset(self):
        # protect “AnonymousUser” is not a valid UUID
        if not self.request.user.is_anonymous:
            new_queryset = Document.objects.filter(owner=self.request.user)
            return new_queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DocumentsPackageViewSet(viewsets.ModelViewSet):
    queryset = DocumentsPackage.objects.all()
    serializer_class = DocumentsPackageSerializer
    permission_classes = (IsOwnerOrReadOnlyPermission,)

    def get_queryset(self):
        # protect “AnonymousUser” is not a valid UUID
        if not self.request.user.is_anonymous:
            new_queryset = DocumentsPackage.objects.filter(
                owner=self.request.user
            )
            return new_queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
