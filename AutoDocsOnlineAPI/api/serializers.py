import base64

from django.core.files.base import ContentFile
from documents.models import Document, DocumentsPackage
from rest_framework import serializers


class Base64FileField(serializers.FileField):
    def to_internal_value(self, data):
        # 'data:doc_name;docx;base64;{base64 data}'
        params, data = data.split(';base64;')
        doc_name, tipe = params.split(';')
        doc_name = doc_name.split(":")[1]
        file_name = doc_name + '.' + tipe

        # decode to base 64
        if not isinstance(data, str):
            raise serializers.ValidationError(
                f"file must be base64 encoded string, not {type(data)}"
            )
        with open("ADocument.docx", 'w') as f:
            f.write(data)

        data = ContentFile(base64.b64decode(data), name=file_name)

        return super().to_internal_value(data)


class DocumentSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(
        pk_field=serializers.CharField(),
        source='owner.username',
        read_only=True
    )
    file = Base64FileField()

    class Meta:
        fields = '__all__'
        model = Document
        read_only_fields = ('owner',)


class DocumentsPackageSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(
        pk_field=serializers.CharField(),
        source='owner.username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = DocumentsPackage
        read_only_fields = ('owner',)
