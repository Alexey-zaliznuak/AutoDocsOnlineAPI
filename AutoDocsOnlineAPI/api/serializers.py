from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.serializers import Base64FileField, ModelWithUpdateForM2MFields
from documents.models import (
    Document,
    DocumentsPackage,
    Record,
    Template,
    TemplateValue,
    UserDefaultTemplateValue,
)
from users.serializers import UserSerializer


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


class GetDocumentTemplateSerializer(TemplateSerializer):
    "The same as TemplateSerializer but do not have author field."
    class Meta:
        model = Template
        fields = (
            'id',
            'title',
            'description',
            'is_official',
            'name_in_document',
        )
        read_only_fields = ('id', 'author', 'is_official',)


class GetDocumentSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    templates = GetDocumentTemplateSerializer(many=True)

    class Meta:
        model = Document
        fields = (
            'id',
            'author',
            'title',
            'description',
            'file',
            'templates',
            'creation_date',
        )


class CreateUpdateDocumentSerializer(ModelWithUpdateForM2MFields):
    file = Base64FileField(required=True)
    templates = serializers.PrimaryKeyRelatedField(
        queryset=Template.objects.all(), many=True
    )

    class Meta:
        model = Document
        fields = (
            'id',
            'author',
            'title',
            'description',
            'file',
            'templates',
            'creation_date',
        )
        read_only_fields = ('id', 'author', 'creation_date')

    def create(self, validated_data):
        templates = validated_data.pop('templates')

        document = Document.objects.create(**validated_data)
        document.templates.set(templates)

        return document


class CreateUpdateTemplateValueSerializer(serializers.ModelSerializer):
    template = serializers.PrimaryKeyRelatedField(
        queryset=Template.objects.all()
    )
    value = serializers.CharField(
        max_length=settings.TEMPLATE_VALUE_VALUE_MAX_LENGTH
    )

    class Meta:
        model = UserDefaultTemplateValue
        fields = (
            'template',
            'value',
        )
        read_only_fields = ('id',)


class GetUserDefaultTemplateValueSerializer(serializers.ModelSerializer):
    value = serializers.CharField(source='template_value.value')
    template = TemplateSerializer(source='template_value.template')

    class Meta:
        model = UserDefaultTemplateValue
        fields = (
            'id',
            'template',
            'value',
        )
        read_only_fields = ('id',)


class CreateUpdateUserDefaultTemplateValueSerializer(
    serializers.ModelSerializer
):
    template_value = CreateUpdateTemplateValueSerializer()

    class Meta:
        model = UserDefaultTemplateValue
        fields = (
            'template_value',
        )

    def create(self, validated_data):
        template_value = validated_data.pop('template_value')
        template_value, _ = TemplateValue.objects.get_or_create(
            **template_value
        )

        obj = UserDefaultTemplateValue.objects.create(
            **validated_data,
            template_value=template_value
        )

        return obj

    def update(self, instance, validated_data):
        # You can`t change template

        template_value = validated_data.pop('template_value', None)

        if template_value:
            template_value, _ = TemplateValue.objects.get_or_create(
                template=instance.template_value.template,
                value=template_value['value']
            )
            instance.template_value = template_value

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance


class GetDocumentsPackageDocumentSerializer(serializers.ModelSerializer):
    templates = GetDocumentTemplateSerializer(many=True)

    class Meta:
        model = Document
        fields = (
            'id',
            'title',
            'description',
            'file',
            'templates',
        )


class GetDocumentsPackageSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    documents = GetDocumentsPackageDocumentSerializer(many=True)

    class Meta:
        model = DocumentsPackage
        fields = (
            'id',
            'title',
            'author',
            'documents',
        )


class CreateUpdateDocumentsPackageSerializer(ModelWithUpdateForM2MFields):
    documents = serializers.PrimaryKeyRelatedField(
        queryset=Document.objects.all(), many=True
    )

    class Meta:
        model = DocumentsPackage
        fields = (
            'title',
            'author',
            'documents',
        )
        read_only_fields = ('author',)

    def create(self, validated_data):
        documents = validated_data.pop('documents')

        documents_package = DocumentsPackage.objects.create(**validated_data)
        documents_package.documents.set(documents)

        return documents_package


class GetSimpleTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = (
            'id',
            'title',
        )


class GetSimpleDocumentsPackageSerializer(
    serializers.ModelSerializer
):
    """
    Serializer for serialize DocumentPackage
    return only id and title value
    """
    class Meta:
        model = DocumentsPackage
        fields = (
            'id',
            'title'
        )


class GetSimpleTemplateValueSerializer(serializers.ModelSerializer):
    template = GetSimpleTemplateSerializer()

    class Meta:
        model = TemplateValue
        fields = (
            'template',
            'value',
        )


class GetSelfRecordsSerializer(serializers.ModelSerializer):
    documents_package = GetSimpleDocumentsPackageSerializer()
    templates_values = GetSimpleTemplateValueSerializer(many=True)

    class Meta:
        model = Record
        fields = (
            'id',
            'documents_package',
            'templates_values',
            'creation_date',
        )


class GetDocumentsPackageRecordsSerializer(serializers.ModelSerializer):
    templates_values = GetSimpleTemplateValueSerializer(many=True)

    class Meta:
        model = Record
        fields = (
            'user',
            'templates_values',
            'creation_date',
        )


class CreateUpdateRecordSerializer(serializers.ModelSerializer):
    templates_values = CreateUpdateTemplateValueSerializer(many=True)

    class Meta:
        model = Record
        fields = (
            'documents_package',
            'templates_values',
        )
        read_only_fields = (
            'creation_date',
        )
        create_only_fields = 'documents_package'

    def create(self, validated_data):
        templates_values = validated_data.pop('templates_values')

        for index, template_value in enumerate(templates_values):
            templates_values[index], _ = TemplateValue.objects.get_or_create(
                **template_value
            )

        record = Record.objects.create(**validated_data)
        record.templates_values.set(templates_values)

        return record

    def validate_templates_values(self, value):
        templates = []

        for template_value in value:
            template = template_value.get('template')

            if template in templates:
                raise ValidationError('Duplicate templates')

            templates.append(template)

        return value

    def validate(self, data):
        templates_values = data.get('templates_values')
        templates = data.get('documents_package').templates
        request_templates = map(
            lambda el: el.get('template'), templates_values
        )

        if len(templates_values) != len(templates):
            raise ValidationError(
                "Uncorrect templates for this document package."
            )

        if set(request_templates) != set(templates):
            raise ValidationError('Uncorrect templates')

        return super().validate(data)


class DownloadRecordDocumentSerializer(serializers.Serializer):
    record = serializers.PrimaryKeyRelatedField(
        queryset=Record.objects.all()
    )
    document_id = serializers.UUIDField()

    def validate(self, data):
        record = data.get('record')
        document_id = data.get('document_id')

        if not record.documents_package.documents.filter(
            pk=document_id
        ).exists():
            raise ValidationError(
                "Document with this id and "
                "related with this record does not exist."
            )

        return data
