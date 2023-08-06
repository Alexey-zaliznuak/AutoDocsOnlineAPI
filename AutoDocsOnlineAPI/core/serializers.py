import base64

from django.core.files.base import ContentFile
from rest_framework import serializers


class Base64FileField(serializers.FileField):
    default_error_messages = serializers.FileField.default_error_messages | {
        'invalid_format': 'File must have "docx" format.',
        'invalid_data_type': (
            'File must be base64 encoded string, not {data_type}'
        )
    }

    def to_internal_value(self, data):
        # 'data:doc_name;docx;base64;{base64 data}'
        params, data = data.split(';base64;')
        doc_name, tipe = params.split(';')
        doc_name = doc_name.split(":")[1]
        file_name = doc_name + '.' + tipe

        if tipe != 'docx':
            self.fail('invalid_format')

        # decode to base 64
        if not isinstance(data, str):
            self.fail('invalid_data_type', data_type=type(data))

        data = ContentFile(base64.b64decode(data), name=file_name)

        return super().to_internal_value(data)
