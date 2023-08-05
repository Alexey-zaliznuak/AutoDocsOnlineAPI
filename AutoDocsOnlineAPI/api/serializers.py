from rest_framework import serializers

from documents.models import Template


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = (
            'id',
            'title',
            'author',
            'description',
            'is_official',
            'name_in_document',
        )
        read_only_fields = ('id', 'author', 'is_official',)


# class DocumentSerializer(serializers.ModelSerializer):
#     author = serializers.PrimaryKeyRelatedField(
#         read_only=True
#     )
#     file = Base64FileField()

#     class Meta:
#         fields = '__all__'
#         model = Document


# class DocumentsPackageSerializer(serializers.ModelSerializer):
#     owner = serializers.PrimaryKeyRelatedField(
#         pk_field=serializers.CharField(),
#         source='owner.username',
#         read_only=True
#     )

#     class Meta:
#         fields = '__all__'
#         model = DocumentsPackage
#         read_only_fields = ('owner',)
