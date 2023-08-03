import base64

from django.core.files.base import ContentFile
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
                f"File must be base64 encoded string, not {type(data)}"
            )

        data = ContentFile(base64.b64decode(data), name=file_name)

        return super().to_internal_value(data)
